from django.contrib import admin

# Register your models here.
from discovery_frontend.models import Location


class LocationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Location, LocationAdmin)
