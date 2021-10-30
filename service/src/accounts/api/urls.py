from django.urls import path, include
from . import views

urlpatterns = [
    path('me/', views.AuthView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('authors/', views.AuthorView.as_view({'get': 'list'})),
    path('authors/<int:pk>', views.AuthorView.as_view({'get': 'retrieve'})),
    path('cocial-link', views.AuthorLinkView.as_view({
        'get': 'list',
        'post': 'create',
        })),
    path('cocial-link/<int:id>', views.AuthorLinkView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
        })),

    path('register/', views.Register.as_view()),
    path('login/', views.Login.as_view()),
]
