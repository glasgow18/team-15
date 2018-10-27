from django.contrib import admin

# Register your models here.
from discovery_frontend.models import Location, KeyWord, Category, Review, Activity, Warnings, ContactDetail


class LocationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Location, LocationAdmin)
admin.site.register(KeyWord, LocationAdmin)
admin.site.register(Category, LocationAdmin)
admin.site.register(Activity, LocationAdmin)
admin.site.register(Review, LocationAdmin)
admin.site.register(Warnings, LocationAdmin)
admin.site.register(ContactDetail, LocationAdmin)


