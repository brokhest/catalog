from django.contrib import admin
from django.db.models import ExpressionWrapper, DecimalField
from .models import Category, Product, Cart, Promo

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    list_filter = ('parent_category', )
    list_editable = ('parent_category', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "promo", "promo_price", 'image_preview' )
    list_filter = ('promo', "category", )
    # readonly_fields = ('image_preview', )
    list_editable = ("price", "category", "promo", )

    def promo_price(self, obj):
        return obj.get_price()
        products = Product.objects.all()
        res = []
        data = {}
        for product in products:
            res.append({"promo price": product.get_price()})
        return res

    def image_preview(self, obj):
        return obj.image_preview()

    image_preview.allow_tags = True


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "products_name", "products_number", "total_summ", "status")
    list_display_links = ("id", )
    filter_horizontal = ('products', )
    list_filter = ("status", )

    @staticmethod
    def products_name(obj):
        products = obj.products.all()
        return [product.name for product in obj.products.all()]

    @staticmethod
    def products_number(obj):
        return obj.products.all().count()
    products_number.short_description = 'number of products'

    @staticmethod
    def total_summ(obj):
        return obj.get_summ()
    total_summ.admin_order_field = 'total'
    total_summ.short_description = 'total'


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', )
    list_editable = ('discount', )


