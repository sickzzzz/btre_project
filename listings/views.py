from django.shortcuts import get_object_or_404, render
from .models import Listing
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .choices import state_choices, price_choices, bedroom_choices

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    
    paging = Paginator(listings, 6)
    page_number = request.GET.get('page')
    page_listings = paging.get_page(page_number) 

    context = {
        'listings': page_listings,
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    query_set = Listing.objects.order_by('-list_date')
    
    #Keyword
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query_set = query_set.filter(description__icontains=keywords)    
    
    #City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            query_set = query_set.filter(city__iexact=city)
    
    #State
    if 'state' in request.GET:
        state  = request.GET['state']
        if state:
            query_set = query_set.filter(state__iexact=state)

    #Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            query_set = query_set.filter(bedrooms__lte=bedrooms)
    
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_set = query_set.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': query_set,
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)