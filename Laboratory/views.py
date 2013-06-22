from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from models import Resource, Element

@login_required
def index(request):
    inventory = Resource.objects.filter(user=request.user)
    return render(request, 'Laboratory/index.html', {'inventory':inventory})

def periodic_table(request):
    elements = Element.objects.all()
    return render(request, "Laboratory/periodic_table.html", {'elements': elements})

def element_detail(request, element):
    ele = get_object_or_404(Element, name=element)
    return render(request, "Laboratory/element.html", {'element': ele})