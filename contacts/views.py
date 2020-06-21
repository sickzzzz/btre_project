from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail

def contact(request):
    if request.method == "POST":
        listing = request.POST['listing']
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email'] 
        
        if request.user.is_authenticated:
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=request.user.id)
            if has_contacted:
                messages.error(request, 'You have already submitted inquiry for this listing')
                return redirect('/listings/' + listing_id) 

        contact = Contact(  listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message,user_id=user_id)
        contact.save()
        
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for listing ' + listing + '. Please sign into admin pane for further info .',
            'pratyushrath1@gmail.com',
            ['forhypstar15@gmail.com', realtor_email],
            fail_silently=False
        )
        
        messages.success(request, 'Your enquiry has been submitted and a realtor will soon contact you .')
        return redirect('/listings/' + listing_id)