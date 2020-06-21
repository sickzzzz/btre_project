from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')        
    else:
        return render(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Check passwords
        if password == password2:
            #Username check
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is taken')
                return redirect('register')
            else:
                #Email-id check
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'The email-id is already registered')
                    return redirect('register')
                else:
                    #Verified
                    user = User.objects.create_user(username=username, \
                                                    email=email, \
                                                    first_name=first_name, \
                                                    last_name=last_name, \
                                                    password=password
                                                )
                    user.save() 
                    messages.success(request, 'You are succesfully registered and now Login')
                    return redirect('login')               
        else:
            messages.error(request, 'Passwords are not the same')
            return redirect('register')
    else:  
        return render(request, 'accounts/register.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are logged out')
        return redirect('index')
    


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)