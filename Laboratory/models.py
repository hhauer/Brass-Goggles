from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import F

class Element(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.SlugField(max_length=3)
    
    number = models.SmallIntegerField("atomic number")
    weight = models.DecimalField("atomic weight", max_digits=5, decimal_places=2)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['number']

class Resource(models.Model):
    type = models.ForeignKey(Element, related_name='+')
    user = models.ForeignKey(User)
    
    amount = models.IntegerField()
    
    def __unicode__(self):
        return self.user.username + ' - ' + self.type.name
    
    class Meta:
        unique_together = ('type', 'user')

# TODO: Django 1.6, move to proper transactions.
class ProductionManager(models.Manager):
    def generate_resource(self, user, p1, p1_amount,  td, costs, p2=None, p2_amount=None):
        # p1 is the primary product and p2 is the byproduct. Shortened for readability.
        if not user or not p1 or not costs:
            raise Exception('Incorrect call to generate_resource.')
        
        p1 = Element.objects.get(name=p1)
        if p2 is not None:
            p2 = Element.objects.get(name=p2)
        
        # We need somewhere to store the resources as they're found.
        found_costs = []
        
        inventory = Resource.objects.filter(user=user)
        
        for name, amount in costs.items():
            r = inventory.get(type__name=name)
            if r.amount < amount:
                raise ProductionEvent.LowResources
            else:
                found_costs.append(r)
        
        # We made it through finding all the resources without raising an exception, which means that
        # we found them all and the player had enough. So now we build the productionevent and then deduct
        # costs. I do this in this order so as not to penalize the user if something goes wrong at this stage.
        
        event = ProductionEvent(user=user, product=p1, byproduct=p2, product_amount=p1_amount, byproduct_amount=p2_amount, finished=timezone.now() + td)
        event.save()
        
        for r in found_costs:
            r.amount = F('amount') - costs[r.type.name]
            r.save()
            
class ProductionEvent(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Element, related_name='+')
    product_amount = models.IntegerField()
    
    byproduct = models.ForeignKey(Element, related_name='+', null=True)
    byproduct_amount = models.IntegerField(null=True)
    
    finished = models.DateTimeField()
    
    objects = ProductionManager()
    
    def __unicode__(self):
        if self.byproduct is not None:
            return self.user.username + " producing: " + self.product.name + " and " + self.byproduct.name
        else:
            return self.user.username + " producing: " + self.product.name
    
    class LowResources(Exception):
        pass
