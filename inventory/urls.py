from django.contrib import admin
from django.urls import path
from .views import Index,SignUpView,Dashboard, AddItem,UpdateItem,DeleteItem,ViewItem,Searchbar,AddStaff,StaffView,UpdateStaff, DeleteStaff,IssueOutItem, get_inventory_quantity,import_data,staff_apply
from django.contrib.auth import views as auth_views
#from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard' ),
    #path('signup/', SignUpView.as_view(), name='signup'),
    
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/login.html'), name='logout'),
   path('add-item/', AddItem.as_view(), name ='add-item'),
   path('edit-item/<int:pk>', UpdateItem.as_view(), name='edit-item'),
   path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
   path('view-item/<int:pk>', ViewItem.as_view(), name='view-item'),
    path('add-staff/', AddStaff.as_view(), name='add-staff'),
    path('signup/', SignUpView.as_view(), name='signup' ),


   path('search/', views.Searchbar, name='searchbar'),
    path('staff/', StaffView.as_view(), name='staff'),
  path('edit-staff/<int:pk>', UpdateStaff.as_view(), name='edit-staff'),
   path('delete-staff/<int:pk>', DeleteStaff.as_view(), name='delete-staff'),
   path('issue-out/<int:pk>', IssueOutItem.as_view(), name='issue-out'),


    path('get-inventory-quantity/<int:inventory_id>/', get_inventory_quantity, name='get_inventory_quantity'),
     path('import-data/', views.import_data, name='import-data'),
     path('staff-apply/', views.staff_apply, name='staff-apply' ),
    # path('login/', CustomLoginView.as_view(), name='login'),


 
]
