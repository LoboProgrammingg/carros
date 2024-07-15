from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import NewCarCreateView, CarsListView, CarDetailView, CarUpdateView
from cars.views import HomePageView, CarDeleteView, SobreTemplateView, CarReviewCreateView, CalculateFinanceView
from accounts.views import register_view, login_view, logout_view, update_profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('register/', register_view, name='register'),
    path('login', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('update_profile/', update_profile_view, name='update_profile'),
    path('car/<int:pk>/calculate_finance/', CalculateFinanceView.as_view(), name='calculate_finance'),
    path('cars/', CarsListView.as_view(), name='cars_list'),
    path('new_car/', NewCarCreateView.as_view(), name='new_car'),
    path('sobre/', SobreTemplateView.as_view(), name='sobre'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('car/<int:car_id>/add_review/', CarReviewCreateView.as_view(), name='add_car_review'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
