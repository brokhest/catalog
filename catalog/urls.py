from django.urls import path
from .views import ProductView, CategoryView, PromoView, CartView, BestProductView

urlpatterns =[
    path('best_products', BestProductView.as_view()),
    path('products', ProductView.as_view()),
    path('products/<int:pk>', ProductView.as_view()),
    path('category', CategoryView.as_view()),
    path('category/<int:pk>', CategoryView.as_view()),
    path('promo', PromoView.as_view()),
    path('promo/<int:pk>', PromoView.as_view()),
    path('carts', CartView.as_view()),
    path('carts/<int:pk>', CartView.as_view())
]