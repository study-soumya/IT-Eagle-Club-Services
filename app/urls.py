from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('our-work', our_work_view, name='our_work'),
    
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('about-us/', about_us_view, name='about_us'),
    
    path('add-services/', add_services, name='add_services'),
    path('services-detail/<slug>', services_detail, name='services_detail'),
    path('update-services/<slug>', update_services, name='update_services'),
    path('delete-services/<id>', delete_services, name='delete_services'),
    path('see-services/', see_services, name='see_services'),
    
    path('add-members/', add_members, name='add_members'),
    path('members-detail/<slug>', members_detail, name='members_detail'),
    path('update-members/<slug>', update_members, name='update_members'),
    path('delete-members/<id>', delete_members, name='delete_members'),
    path('see-members/', see_members, name='see_members'),
    
    path('contact-us/', contact_us, name='contact_us'),
]
