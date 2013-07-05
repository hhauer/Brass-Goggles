from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F
from models import Resource, Element, ProductionEvent

from django.http import HttpResponse

import datetime
from django.utils import timezone

@login_required
def index(request):
    produced = []
    production_complete = ProductionEvent.objects.filter(user=request.user, finished__lte=timezone.now())
    
    for product in production_complete:
        (p1, _) = Resource.objects.get_or_create(user=request.user, type=product.product)
        p1.amount = F('amount') + product.product_amount
        p1.save()
        
        message = "{} units of {} were produced.".format(product.product_amount, product.product.name)
        
        if product.byproduct is not None:
            (p2, _) = Resource.objects.get_or_create(user=request.user, type=product.byproduct)
            p2.amount = F('amount') + product.byproduct_amount
            message += " Additionally {} units of {} were produced as a byproduct.".format(product.byproduct_amount, product.byproduct.name)
            p2.save()
        
        product.delete()
        produced.append(message)
    
    in_production = ProductionEvent.objects.filter(user=request.user)
    
    return render(request, 'Laboratory/index.html', {
                                                     'produced' : produced,
                                                     'in_production' : in_production })

@login_required
def inventory(request):
    inventory = Resource.objects.filter(user=request.user)
    return render(request, 'Laboratory/inventory.html', {'inventory':inventory})
    
def periodic_table(request):
    elements = Element.objects.all()
    return render(request, "Laboratory/periodic_table.html", {'elements': elements})

def element_detail(request, element):
    ele = get_object_or_404(Element, name=element)
    return render(request, "Laboratory/element.html", {'element': ele})

def debug_test_production(request):
    try:
        ProductionEvent.objects.generate_resource(user=request.user, p1='Cheese', p1_amount=10, td=datetime.timedelta(minutes=10), costs={'Love' : 1, 'Hyrule': 1}) 
    except ProductionEvent.LowResources:
        return HttpResponse("Not enough resources.")

    return HttpResponse("Now producing cheese.")

