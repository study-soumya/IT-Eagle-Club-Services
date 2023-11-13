from django.shortcuts import(
    render,
    redirect,
    get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse



def index_view(request):
    context = {
        'members':MembersModel.objects.all(),
        'services':ServicesModel.objects.all()
    }
    return render(request, 'index.html', context)

def our_work_view(request):
    return render(request, 'our_work.html')

User = get_user_model()

def register_view(request):
    try:
        if request.method == "POST":
            data = request.POST
            uname = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')

            if not uname:
                messages.error(request, "Username cannot be empty!")
            elif not password:
                messages.error(request, "Please enter a valid password.")
            elif password != confirm_password:
                messages.error(request, "Passwords do not match")
            else:
                check_user = User.objects.filter(username=uname).first()
                if check_user:
                    messages.warning(request, "User already exists with this name! Please choose another one...")
                else:
                    user = User.objects.create_user(
                        username=uname,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    user.full_name = f"{first_name} {last_name}"
                    user.save()
                    return redirect('login')

        return render(request, 'register.html')

    except Exception as e:
        print(e)
        messages.error(request, "An error occurred during registration.")

    return render(request, 'register.html')


def login_view(request):
    try:
        if request.method == 'POST':
            data = request.POST
            username = data.get('username')
            password = data.get('password')
            
            if not username:
                messages.error(request, "Username not found")
            
            elif not password:
                messages.error(request, "Password not found")
            else:
                check_user = User.objects.filter(username=username).first()
            
                if check_user is None:
                    messages.error(request,'Invalid credentials.')
                else:
                    user = authenticate(request, username=username, password=password)
                
                    if user:
                        login(request, user)
                        return redirect('index')
                    else:
                        messages.error(request,'Incorrect Password or Username!')
                        
        return render(request, 'login.html')

    except Exception as e:
        print(e)
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



# About Us View
@login_required(login_url='login')
def about_us_view(request):
    return render(request, 'about_us.html')


# Section View

@login_required(login_url='login')
def see_services(request):
    context = {}
    try:
        service_objs = ServicesModel.objects.filter(user=request.user)
        context['service_objs'] = service_objs
    except Exception as e:
        print(e)
    return render(request, 'see_services.html', context)

@login_required(login_url='login')
def add_services(request):
    try:
        if request.method == "POST":
            form = ServiceForm(request.POST)
            user = request.user
            title = request.POST.get('title')
            icon = request.POST.get('icon')
            image = request.FILES.get('image')
            
            if form.is_valid():
                description = form.cleaned_data['description']
                service = ServicesModel.objects.create(
                    user=user, title=title, icon=icon, description=description, image=image, 
                )
                
                return redirect('index')
            
    except Exception as e:
        print(e)
    
    return render(request, 'add_service.html', {'form':ServiceForm})


@login_required(login_url='login')
def services_detail(request, slug):
    context = {}
    try:
        service = get_object_or_404(ServicesModel, slug=slug)
        context['service'] = service
    except Exception as e:
        print(e)
    
    return render(request, 'service_detail.html', context)


@login_required(login_url='login')
def update_services(request, slug):
    try:
        service = get_object_or_404(ServicesModel,slug=slug)
        
        if service.user != request.user:
            return redirect('index')
        
        if request.method == 'POST':
            form = ServiceForm(request.POST, request.FILES, instance=service)
            title = request.POST.get('title')
            icon = request.POST.get('icon')
            image = request.FILES.get('image')
            
            service.title = title
            service.icon = icon
            if image:
                service.image = image
            
            if form.is_valid():
                form.save()
                return redirect('index')
        
        else:
            form = ServiceForm(instance=service)
            
    except Exception as e:
        print(e)
    
    return render(request, 'update_service.html', {'service':service, 'form':form})


@login_required(login_url='login')
def delete_services(request, id):
    context = {}
    try:
        services = get_object_or_404(ServicesModel, id=id)
        if request.method == 'POST':
            services.delete()
            return redirect('index')
        context['services'] = services
    except Exception as e:
        print(e)
    
    return render(request, 'confirm_delete_service.html', context)


# Members View

@login_required(login_url='login')
def members_detail(request, slug):
    context = {}
    try:
        member = MembersModel.objects.filter(slug=slug).first()
        member_objs = MembersModel.objects.filter(user=request.user)
        context['member'] = member
    except Exception as e:
        print(e)
    return render(request, 'members_detail.html', context)

@login_required(login_url='login')
def see_members(request):
    context = {}
    try:
        member_objs = MembersModel.objects.filter(user=request.user)
        context['member_objs'] = member_objs
    except Exception as e:
        print(e)
    return render(request, 'see_members.html', context)

@login_required(login_url='login')
def add_members(request):
    try:
        if request.method == 'POST':
            form = MemberForm(request.POST)
            user = request.user
            name = request.POST.get('fullName')
            username = request.POST.get('username')
            company_name = request.POST.get('company-name')
            job_title = request.POST.get('job-title')
            job_designation = request.POST.get('job-designation')
            work_experience = request.POST.get('work-experience')
            email = request.POST.get('email')
            profile_image = request.FILES.get('image')
            
            if form.is_valid():
                description = form.cleaned_data['description']
                member = MembersModel.objects.create(
                    user=user, name=name, username=username, company_name=company_name, job_title=job_title, job_designation=job_designation, work_experience=work_experience, email=email, description=description, profile_image=profile_image
                )
                return redirect('index')
    except Exception as e:
        print(e)
    
    return render(request, 'add_member.html', {'form':MemberForm})

@login_required(login_url='login')
def update_members(request, slug):
    try:
        member = get_object_or_404(MembersModel,slug=slug)
        
        if member.user != request.user:
            return redirect('index')
        
        if request.method == 'POST':
            form = MemberForm(request.POST, request.FILES, instance=member)
            name = request.POST.get('fullName')
            username = request.POST.get('username')
            company_name = request.POST.get('company-name')
            job_title = request.POST.get('job-title')
            job_designation = request.POST.get('job-designation')
            work_experience = request.POST.get('work-experience')
            email = request.POST.get('email')
            profile_image = request.FILES.get('image')
            
            member.name = name
            member.username = username
            member.company_name = company_name
            member.job_title = job_title
            member.job_designation = job_designation
            member.work_experience = work_experience
            member.email = email
            if profile_image:
                member.profile_image = profile_image
            
            if form.is_valid():
                form.save()
                return redirect('members_detail', slug=member.slug)
        
        else:
            form = MemberForm(instance=member)
            
    except Exception as e:
        print(e)
    
    return render(request, 'update_member.html', {'member':member, 'form':form})


@login_required(login_url='login')
def delete_members(request, id):
    context = {}
    try:
        member = MembersModel.objects.get(id=id)
        
        if request.method == 'POST':
            member.delete()
            return redirect('see_members')
        context['member'] = member
    
    except Exception as e:
        print(e)
    
    return render(request, 'confirm_delete_member.html', context)

# Contact Us view
@login_required(login_url='login')
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        message = request.POST.get('message')

        # Compose the email message
        subject = 'Contact Form Submission'
        email_message = f'Name: {name}\nEmail: {email}\nMobile Number: {mobile_number}\nMessage: {message}'

        try:
            # Send the email using Django's send_mail function
            send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
            messages.success(request, f'Thank you {name} for your message. We will get back to you soon!')

        except Exception as e:
            print(e)
            messages.error(request, 'Oops! Something went wrong while sending the email.')

    return render(request, 'index.html')