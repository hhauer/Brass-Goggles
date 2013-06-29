from django.contrib import admin
from Laboratory.models import Element, Resource, ProductionEvent

admin.site.register(Element)
admin.site.register(Resource)
admin.site.register(ProductionEvent)