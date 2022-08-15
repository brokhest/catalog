from django.db import models
from django.utils.html import mark_safe, format_html


# Create your models here.

# менеджер, возвращающий товары с лучшей ценой в своей категории
class ProductManager(models.Manager):
    def get_queryset(self):
        pk_list = list()
        for category in Category.objects.all():
            qs = super().get_queryset().filter(category=category)
            if not qs.exists():
                continue
            min = qs.first()
            for product in qs:
                if product.get_price() < min.get_price() : min = product
            pk_list.append(min.pk)
        return self.model.objects.filter(pk__in=pk_list)


class Category(models.Model):

    name = models.CharField(max_length=20, unique=True)
    parent_category = models.ForeignKey("Category", related_name="parent", on_delete=models.CASCADE, null=True,
                                        blank=True)

    def __str__(self):
        return self.name


class Promo(models.Model):
    discount = models.DecimalField(max_digits=2, decimal_places=2)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='')
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    promo = models.ForeignKey(Promo, related_name='promo', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.image.delete(self.image.name)
        super().delete()

    def get_price(self):
        if self.promo:
            return self.price * (1-self.promo.discount)
        return self.price

    def image_preview(self):
        return format_html('<img src ="{0}" width="auto" height="150px">'.format(self.image.url))

    objects = models.Manager()
    best_products = ProductManager()


class Cart(models.Model):
    status_choices = (
        ('a', 'creating'),
        ('b', 'confirmed'),
        ('c', 'waiting for payment'),
        ('d', 'preparing'),
        ('f', 'closed'),
    )
    products = models.ManyToManyField(Product)
    # id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=1, choices=status_choices, default='a')

    def __str__(self):
        return str(self.id)

    def get_summ(self):
        summ = 0
        for product in self.products.all():
            summ += product.get_price()
        return summ




