from cars.models import Car
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CarReviewForm, FinanceCalculatorForm
from .models import Car, CarReview
from django.http import HttpResponseRedirect
from cars.forms import CarModelForm
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, View
from django.shortcuts import get_object_or_404

class HomePageView(TemplateView):
    template_name = 'home.html'

class SobreTemplateView(TemplateView):
    template_name ='sobre_view.html'

class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains=search)
        return cars


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CarReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        form = CarReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = self.request.user
            review.save()
            return self.render_to_response(self.get_context_data(object=car))
        else:
            return self.render_to_response(self.get_context_data(object=car))
    

class CalculateFinanceView(View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        
        # Obter os dados do formulário
        price_str = request.POST.get('price', '').replace(',', '.')  # Substitui ',' por '.' se houver
        price = float(price_str) if price_str else 0
        interest_rate = float(request.POST.get('interest_rate', 0))
        loan_term = int(request.POST.get('loan_term', 0))
        
        # Validar os dados recebidos
        if price <= 0 or interest_rate <= 0 or loan_term <= 0:
            messages.error(request, 'Por favor, preencha todos os campos corretamente.')
            return HttpResponseRedirect(reverse('car_detail', kwargs={'pk': pk}))
        
        # Converter a taxa de juros anual para mensal
        monthly_interest_rate = interest_rate / 100 / 12
        
        # Calcular o número total de pagamentos
        num_payments = loan_term * 12
        
        # Calcular o pagamento mensal usando a fórmula de amortização constante (Price)
        if monthly_interest_rate > 0:
            monthly_payment = (price * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**-num_payments)
        else:
            monthly_payment = price / num_payments
        
        # Arredondar para 2 casas decimais
        monthly_payment = round(monthly_payment, 2)
        
        # Exibir o resultado como mensagem
        finance_message = f'O pagamento mensal estimado é de R$ {monthly_payment:.2f}'
        messages.info(request, finance_message)  # Usando messages.info para uma mensagem informativa
        
        return HttpResponseRedirect(reverse('car_detail', kwargs={'pk': pk}))

@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'

class CarReviewCreateView(LoginRequiredMixin, CreateView):
    model = CarReview
    form_class = CarReviewForm
    template_name = 'car_detail.html'

    def form_valid(self, form):
        car = get_object_or_404(Car, pk=self.kwargs['car_id'])
        form.instance.car = car
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.kwargs['car_id']})