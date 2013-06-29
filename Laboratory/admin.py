from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from Laboratory.models import Element, Resource, ProductionEvent

class UserResourceInline(admin.TabularInline):
    model = Resource
    can_delete = False

class UserProductionInline(admin.TabularInline):
    model = ProductionEvent

class UserAdmin(UserAdmin):
    inlines = (UserResourceInline, UserProductionInline, )
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Element)