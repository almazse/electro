from django.db import models
from django.db.models import CharField
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> CharField:
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self) -> CharField:
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, related_name='products', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=150, db_index=True, unique=True)
    main_photo = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    photo_1 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    photo_2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    photo_3 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField()
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=True)
    available = models.BooleanField(default=True)
    rait = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self) -> CharField:
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

