from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import NewCarCreateView, CarsListView, CarDetailView,MyCarListView, CarUpdateView, HomePageView, CarDeleteView, SobreTemplateView, CarReviewCreateView, CalculateFinanceView
from accounts.views import register_view, login_view, logout_view, update_profile_view, confirm_email, CustomPasswordResetView
from django.contrib.auth import views as auth_views
from accounts.views import CustomPasswordResetCompleteView, CustomPasswordResetConfirmView, check_email_exists
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('register/', register_view, name='register'),
    path('confirm/<uidb64>/<token>/', confirm_email, name='confirm_email'),
    path('senha/recuperar/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('senha/recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('senha/recuperar/confirmar/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('senha/recuperar/concluido/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('ajax/check_email/', check_email_exists, name='check_email_exists'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('update_profile/', update_profile_view, name='update_profile'),
    path('car/<int:pk>/calculate_finance/', CalculateFinanceView.as_view(), name='calculate_finance'),
    path('cars/', CarsListView.as_view(), name='cars_list'),
    path('new_car/', NewCarCreateView.as_view(), name='new_car'),
    path('my-cars/', MyCarListView.as_view(), name='my_cars'),
    path('sobre/', SobreTemplateView.as_view(), name='sobre'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('car/<int:car_id>/add_review/', CarReviewCreateView.as_view(), name='add_car_review'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
