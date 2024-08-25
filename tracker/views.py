from django.urls import reverse_lazy  
from django.views import generic  
from django.contrib.auth import login  
from django.contrib.auth.decorators import login_required  
from django.utils.decorators import method_decorator  
from .forms import CustomUserCreationForm  
from .models import CustomUser  
from django.contrib.auth.mixins import LoginRequiredMixin  
from django.contrib.auth import logout  
from django.shortcuts import redirect 
from django.views import View

class RegisterView(generic.CreateView):  
    form_class = CustomUserCreationForm  
    template_name = 'tracker/register.html'  
    success_url = reverse_lazy('login')  

    def form_valid(self, form):  
        user = form.save()  
        login(self.request, user)  # Automatically allows logged in after registration.  
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')  
class ProfileView(LoginRequiredMixin, generic.TemplateView):  
    template_name = 'tracker/profile.html'  
    login_url = 'login'  # Optional: Set a specific login URL, defaults to '/accounts/login/'  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['user'] = self.request.user  
        return context
    
class CustomLogoutView(View):  
    def get(self, request, *args, **kwargs):  
        logout(request)  # Log the user out  
        return redirect('logout_confirm')  # Redirect to the custom logout confirmation page 
    
# class Home()