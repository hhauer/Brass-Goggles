from django.db import models
from django.contrib.auth.models import User

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
    