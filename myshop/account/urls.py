from django.urls import path,include
from account import views
urlpatterns = [
    path('login/',views.login),
    path('profile/',views.profile),
    path('logout/',views.logout),
    path('signup/',views.signup),
    path('forgot/',views.forgot)
]
