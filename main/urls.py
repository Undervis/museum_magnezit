from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:id>', views.item, name='item'),
    path('login', views.MainLoginView.as_view(), name='login'),
    path('logout', views.MainLogout.as_view(), name='logout'),
    path('create', views.create, name='create'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('delete/<int:pk>', views.delete, name='delete'),
]