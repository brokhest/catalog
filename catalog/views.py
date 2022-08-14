from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from .models import Product, Category, Promo, Cart
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

# Create your views here.


class BestProductView(APIView):
    @staticmethod
    def get(request):
        data = []
        for product in Product.best_products.all():
            record = {
                'name': product.name,
                'cathegory': product.category.name if product.category is not None else None,
                'price': product.get_price(),
                'pk': product.pk,
                'image': product.image.url
            }
            data.append(record)
        return JsonResponse(data, safe=False)



class ProductView(APIView):
    @staticmethod
    def get(request):
        data = []
        for product in Product.objects.all():
            record = {
                'name': product.name,
                'cathegory': product.category.name if product.category is not None else None,
                'price': product.get_price(),
                'pk': product.pk,
                'image': product.image.url
            }
            data.append(record)
        return JsonResponse(data, safe=False)

    @staticmethod
    def post(request):
        product = Product(name=request.data.get('name'),
                          category=get_object_or_404(Category.objects.all(), name=request.data.get('category'))
                          if 'category' in request.data else None,
                          price=request.data.get('price'),
                          image=request.data.get('image'),
                          promo=get_object_or_404(Promo.objects.all(), name=request.data.get('promo'))
                          if 'promo' in request.data else None,
                          )
        product.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request, pk):
        product = get_object_or_404(Product.objects.all(), pk=pk)
        if 'name' in request.data:
            product.name = request.data.get('name')
        if 'category' in request.data:
            category = get_object_or_404(Category.objects.all(), name=request.data.get('category'))
            product.category=category
        if 'price' in request.data:
            product.price = request.data.get('price')
        if 'promo' in request.data:
            promo = get_object_or_404(Promo.objects.all(), name= request.data.get('promo'))
            product.promo = promo
        if 'image' in request.data:
            product.image = request.data.get('image')
        product.save()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk):
        product = get_object_or_404(Product.objects.all(), pk=pk)
        product.delete()
        return Response(status=status.HTTP_200_OK)

class CategoryView(APIView):
    @staticmethod
    def get(request):
        data = []
        for category in Category.objects.all():
            record = {
                'name':category.name,
                'parent': category.parent_category.name if category.parent_category is not None else None,
                'pk': category.pk
            }
            data.append(record)
        return JsonResponse(data, safe=False)

    @staticmethod
    def post(request):
        category = Category(
            name=request.data.get('name'),
            parent_category=get_object_or_404(Category.objects.all(), name=request.data.get('parent'))
            if 'parent' in request.data else None
        )
        category.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(request, pk):
        category = get_object_or_404(Category.objects.all(), name=request.data.get('name'))
        category.delete()
        return Response(status=status.HTTP_200_OK)


class PromoView(APIView):

    @staticmethod
    def get(request):
        data = []
        for promo in Promo.objects.all():
            record = {
                'name': promo.name,
                'discount': promo.discount,
                'pk': promo.pk
            }
            data.append(record)
        return JsonResponse(data, safe=False)

    @staticmethod
    def post(request):
        promo = Promo(
            name=request.data.get('name'),
            discount=request.data.get('discount')
        )
        promo.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request, pk):
        promo = get_object_or_404(Promo.objects.all(), pk=pk)
        if 'name' in request.data:
            promo.name = request.data.get('name')
        if 'discount' in request.data:
            promo.discount = request.data.get('discount')
        promo.save()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk):
        promo = get_object_or_404(Promo.objects.all(), pk=pk)
        promo.delete()
        return Response(status=status.HTTP_200_OK)


class CartView(APIView):
    @staticmethod
    def get(request):
        data = []
        for cart in Cart.objects.all():
            products = []
            for product in cart.products.all():
                products.append(product.name)
            record = {
                'products': products,
                'price': cart.get_summ(),
                'prod_num': cart.products.all().count(),
                'status': cart.get_status_display()
            }
            data.append(record)
        return JsonResponse(data, safe=False)

    @staticmethod
    def post(request):
        cart = Cart.objects.create()
        for prod in request.data.get('products'):
            product = get_object_or_404(Product.objects.all(), name=prod)
            cart.products.add(product)
        cart.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request, pk):
        cart = get_object_or_404(Cart.objects.all(), pk=pk)
        if 'add_prod' in request.data:
            for prod in request.data.get('add_prod'):
                product = get_object_or_404(Product.objects.all(), name=prod)
                cart.products.add(product)
        if 'remove_prod' in request.data:
            for prod in request.data.get('remove_prod'):
                product = get_object_or_404(Product.objects.all(), name=prod)
                cart.products.remove(product)
        if 'status' in request.data:
            cart.status = 'status'
        cart.save()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk):
        cart = get_object_or_404(Cart.objects.all(), pk=pk)
        cart.delete()
        return Response(status=status.HTTP_200_OK)









