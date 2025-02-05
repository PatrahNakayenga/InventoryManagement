from django.http import HttpResponse


from django.shortcuts import redirect

def unauthenticated_user(view_func):
     def wrapped_func(request, *args, **kwargs):

          if request.user.is_authenticated:
               return redirect('index')
          else:
               return view_func(request, *args, **kwargs)
     return wrapped_func






def allowed_user(allowed_roles=[]):
    def decorator(view_func):
            def wrapper_func(request, *args,**kwargs):


                group = None
                if request.user.groups.exists():
                     group = request.user.groups.all()[0].name

                if group in allowed_roles:
                     return view_func(request, *args, **kwargs)
                else:
                     return HttpResponse('You are not authorised to view')
                     
            return wrapper_func
    return decorator







def admin_only(view_func):
     
     def wrapper_func( request, *args,**kwargs):




                group = None
                if request.user.groups.exists():
                     group = request.user.groups.all()[0].name

                if group == 'Staff':
                      return redirect('staff-apply')

                if group == 'Admin':
                     return view_func(request, *args, **kwargs)
                
                return redirect('index')               
     return wrapper_func