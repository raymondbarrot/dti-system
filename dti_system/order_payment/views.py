from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OrderPaymentItem
from .forms import UserRegisterForm, OrderPaymentItemForm

# Create your views here.
class Index(TemplateView):
    template_name = 'order_payment/index.html'

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = OrderPaymentItem.objects.all()
        return render(request, 'order_payment/dashboard.html', {'items': items})

class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'order_payment/signup.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request, user)
            return redirect('index')
        
        return render(request, 'order_payment/signup.html', {'form': form})
    
class AddItem(LoginRequiredMixin, CreateView):
    model = OrderPaymentItem
    form_class = OrderPaymentItemForm
    template_name = 'order_payment/item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
