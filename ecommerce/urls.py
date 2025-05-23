from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.product_list, name='home'),  
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<int:pk>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('ajouter-au-panier/<int:product_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.afficher_panier, name='panier'),
    path('allProducts/', views.product, name='products'),
    path('supprimer-du-panier/<int:product_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('commander/', views.create_order_from_cart, name='create_order_from_cart'),
    path('mes-commandes/', views.order_list, name='order_list'),
    path('commande/<int:order_id>/', views.order_detail, name='order_detail'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

