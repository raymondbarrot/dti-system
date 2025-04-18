from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OrderPaymentItem
from .forms import UserRegisterForm, OrderPaymentItemForm
from django.contrib import messages
from num2words import num2words

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

def num2words_pesos(amount):
        whole_number, centavos = str(amount).split('.')
        whole_number_words = num2words(int(whole_number))
        centavos_words = num2words(int(centavos))
        return f"{whole_number_words} pesos and {centavos_words} cents"
    
class AddItem(LoginRequiredMixin, CreateView):
    model = OrderPaymentItem
    form_class = OrderPaymentItemForm
    template_name = 'order_payment/item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_by = self.request.user.username

        total = 0

        if form.instance.fee_type_1_amount is not None:
            total = total + form.instance.fee_type_1_amount
        
        if form.instance.fee_type_2_amount is not None:
            total = total + form.instance.fee_type_2_amount
        
        if form.instance.fee_type_3_amount is not None:
            total = total + form.instance.fee_type_3_amount

        if form.instance.dst is not None:
            total = total + form.instance.dst

        if form.instance.surcharge is not None:
            total = total + form.instance.surcharge

        form.instance.total_amount = total
        form.instance.amount_in_words = num2words_pesos(total)
        # form.instance.amount_in_words = num2words(total, to='currency', lang='en', separator=' and', currency='USD')

        return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
    model = OrderPaymentItem
    form_class = OrderPaymentItemForm
    template_name = 'order_payment/item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        oldItem = OrderPaymentItem.objects.get(pk=form.instance.pk)
        form.instance.user = self.request.user
        form.instance.last_update_by = self.request.user.username

        if form.instance.status != oldItem.status and form.instance.status == 'APPROVED':
            form.instance.approver_username = self.request.user.username
            form.instance.signature_url = self.request.user.userprofile.signature.url
            form.instance.acting_accountant = self.request.user.first_name + " " + self.request.user.last_name

        return super().form_valid(form)

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = OrderPaymentItem
	template_name = 'order_payment/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'

class ViewItem(LoginRequiredMixin, DetailView):
    model = OrderPaymentItem
    template_name = 'order_payment/view_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_payment"] = self.get_object
        return context