from django.shortcuts import render, redirect
from django.views.generic import TemplateView,View,CreateView,UpdateView,DeleteView,DetailView,ListView
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm,InventoryItemForm,StaffForm,IssueOutForm,UploadForm
from .models import inventoryItem,Category,Staff,Department,IssueOut
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from inventoryMnanagemnet.settings import LOW_QUANTITY
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import csv
from .decorators import allowed_user,admin_only,unauthenticated_user
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
 #from django.contrib.auth.views import LogoutView



# Create your views here.



class Index( TemplateView):
    template_name = 'inventory/index.html'
   

@method_decorator(admin_only, name='dispatch') 
class Dashboard(LoginRequiredMixin, View):
    
    
    
    def get(self, request):
        items = inventoryItem.objects.filter(user=self.request.user.id).order_by('id')

        low_inventory = inventoryItem.objects.filter(
          user = self.request.user.id,
          quantity__lte=LOW_QUANTITY
        )
        if low_inventory.count() > 0:
            if low_inventory.count()> 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item has low inventory')
        low_inventory_ids = inventoryItem.objects.filter(

            user=self.request.user.id,
            quantity__lte=LOW_QUANTITY


        ).values_list('id', flat=True)



        return render(request, 'inventory/dashboard.html', {'items':items, 'low_inventory_ids': low_inventory_ids})
#@method_decorator(admin_only, name='dispatch') 




@method_decorator(unauthenticated_user, name='dispatch')
class SignUpView(View):

    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #form.save()
            user = form.save(commit=False)  # Don't save yet
            user.save()
            group_name = form.cleaned_data['Group']
            group = Group.objects.filter(name=group_name).first()


            if group:
                user.groups.add(group)
            #user.groups.add(group)


            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],

                #group = Group.object.get(name='Staff')
                #user.groups.add(group)
            )

            #if user:
                #login(request, user)
                #return redirect('index')



            login(request, user)
            return redirect('index')
        return render(request, 'inventory/signup.html', {'form': form})
    






####
@method_decorator(admin_only, name='dispatch') 
class AddItem(LoginRequiredMixin, CreateView):
        model = inventoryItem
        form_class = InventoryItemForm
        template_name ='inventory/item_form.html'
        success_url = reverse_lazy('dashboard')


        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            return context
        


        def form_valid(self, form):
            form.instance.user = self.request.user
            return  super().form_valid(form)
        






@method_decorator(admin_only, name='dispatch') 
class UpdateItem(LoginRequiredMixin, UpdateView):
    model = inventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')


@method_decorator(admin_only, name='dispatch') 
class DeleteItem(LoginRequiredMixin, DeleteView):
    model = inventoryItem
    template_name = 'inventory/delete_item.html'

    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'



@method_decorator(admin_only, name='dispatch') 
class ViewItem(LoginRequiredMixin, DetailView):
    model = inventoryItem
    template_name='inventory/view_item.html'







@login_required
@method_decorator(admin_only, name='dispatch') 
def Searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        items = inventoryItem.objects.all().filter(name__icontains=search)
        return render(request, 'searchbar.html', {'items':items})

 

        model = inventoryItem


@method_decorator(admin_only, name='dispatch') 
class AddStaff(LoginRequiredMixin, CreateView):
        model = Staff
        form_class = StaffForm
        template_name ='inventory/add_staff.html'
        success_url = reverse_lazy('staff')


        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['departments'] = Department.objects.all()
            return context
        
     
        



@method_decorator(admin_only, name='dispatch') 
class StaffView(LoginRequiredMixin, ListView):
    model = Staff
    template_name='staff.html'
    context_object_name='persons'



@method_decorator(admin_only, name='dispatch') 

class UpdateStaff(LoginRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'inventory/add_staff.html'
    success_url = reverse_lazy('staff')


@method_decorator(admin_only, name='dispatch') 
class DeleteStaff(LoginRequiredMixin, DeleteView):

    model = Staff
    template_name = 'inventory/delete_staff.html'

    success_url = reverse_lazy('staff')
    context_object_name = 'persons'



@method_decorator(admin_only, name='dispatch') 
class ViewStaff(LoginRequiredMixin, DetailView):
    model = Staff
    template_name='inventory/view_staff.html'



@method_decorator(admin_only, name='dispatch') 

class IssueOutItem(LoginRequiredMixin,CreateView):
    model = IssueOut
    form_class = IssueOutForm
    template_name = 'inventory/Issue_form.html'
    #success_url = reverse_lazy('dashboard')



    def form_valid(self,form):
        issue_out = form.save()



        inventoryItem = issue_out.inventoryItem
        quantity_issued = issue_out.quantity


        if inventoryItem:
            from django.db.models import F 
            try:
                inventoryItem.quantity = F('quantity') - quantity_issued
                inventoryItem.save()
            except Exception as e:
                issue_out.delete()

                form.add_error(None, f"Error updating inventory: {e}")

                return self.form_invalid(form)
        return super().form_valid(form)
    


    def get_success_url(self):
        return reverse_lazy('dashboard')
        


        









@method_decorator(admin_only, name='dispatch') 

def get_inventory_quantity(request, inventory_id):
    try:
        item = inventoryItem.objects.get(id=inventory_id)
        return JsonResponse({'quantity': item.quantity})
    except inventoryItem.DoesNotExist:
        return JsonResponse({'quantity': 0})








@login_required
@allowed_user(allowed_roles='Admin')
# csv import view
def import_data(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                if file.name.endswith('csv'):
                    decoded_file = file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(decoded_file)
                    for row in reader:
                            user = request.user


                            category_name= row.get('category',).strip()
                    if category_name:
                                try:
                                 
                                 category, created = Category.objects.get_or_create(name="Transportation")
                                 category, created = Category.objects.get_or_create(name="Raw Materials")
                                 inventoryItem.objects.create(
                # ... other fields
                                category=category,
                                name = row['name'],
                                quantity = row['quantity'],
                                user=user
                            )

                                except Exception as e:  # Catch any exception during category lookup/creati
                                     print(f"Error processing category '{category_name}': {e}")
                                     form.add_error(None, f"Error processing category '{category_name}': {e}")
                                     return render(request, 'inventory/import.html', {'form': form})
                    else:
                              print(f"Warning: Category missing for item: {row['name']}")




                                 #category fix

                                 #category fix
                         
                              inventoryItem.objects.create(
                            name = row['name'],
                           # category=row['category'],
                            quantity = row['quantity'],
                            #issue_out_status = row['issue_out_status'],
                            #field5 = row['date_created'],
                           user=user
                            
                            

                        )


                else:
                  raise ValueError("Invalid file format. Only CSV")

                return redirect('dashboard')  # Redirect on success
            except Exception as e: # Catch exceptions during import
                form.add_error(None, f"Error during import: {e}")  # Display error message
                return render(request, 'inventory/import.html', {'form': form})


    else:
        form= UploadForm()
    return render(request, 'inventory/import.html', {'form':form})
                




def staff_apply(request):
    context={}
    return render(request, 'inventory/staff-apply.html', context)
 





"""
class staff_apply(TemplateView):
    template_name = 'inventory/staff-apply.html'


    """







# views.py
"""
from django.contrib.auth.views import LoginView
from django.urls import reverse

class CustomLoginView(LoginView):
    def get_redirect_url(self):
        # Check if the user is in the 'Staff' group
        if self.request.user.groups.filter(name="Staff").exists():
            return reverse('staff_apply')  # Redirect staff users to 'staff_apply' view
        return super().get_redirect_url()  # Redirect admins to default (usually index)




"""