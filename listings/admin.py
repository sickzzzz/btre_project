from django.contrib import admin
from .models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'list_date', 'price', 'realtor')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    list_filter = ('realtor',)
    list_per_page = 25  
    search_fields = ('title', 'city', 'state', 'zipcode', 'address', 'description')

admin.site.register(Listing, ListingAdmin)
    