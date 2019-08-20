from django.urls import path, include
from .views import PaymentView, HomePageView

urlpatterns =  [
    path('payment/', PaymentView.as_view(), name = 'payment'),
    path('dashboard/', HomePageView.as_view()),
]