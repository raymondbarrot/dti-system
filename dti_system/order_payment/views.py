from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OrderPaymentItem
from .forms import UserRegisterForm, OrderPaymentItemForm
from django.contrib import messages

# Create your views here.
class Index(TemplateView):
    template_name = 'order_payment/index.html'

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = OrderPaymentItem.objects.all()

        new_order_payment = OrderPaymentItem.objects.filter(
			status="NEW"
		)

        if new_order_payment.count() > 0:
            if new_order_payment.count() > 1:
                messages.info(request, f'There are {new_order_payment.count()} new items.')
            else:
                messages.info(request, f'There is {new_order_payment.count()} new item')

        new_order_payment_ids = OrderPaymentItem.objects.filter(
			status="NEW"
		).values_list('id', flat=True)

        return render(request, 'order_payment/dashboard.html', {'items': items, 'new_order_payment_ids': new_order_payment_ids})

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
        form.instance.created_by = self.request.user.username
        form.instance.serial_number = str(datetime.now().year) + "-" + str(datetime.now().month)
        return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
    model = OrderPaymentItem
    form_class = OrderPaymentItemForm
    template_name = 'order_payment/item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.last_update_by = self.request.user.username
        return super().form_valid(form)

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = OrderPaymentItem
	template_name = 'order_payment/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'