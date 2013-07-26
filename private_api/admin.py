from django.contrib import admin
from private_api.models import Game, GameTask

class GameAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

admin.site.register(Game, GameAdmin)
admin.site.register(GameTask)