from django.db import models
from PIL import Image
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/')
    parent_category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('show_subcategory', kwargs={'subcategory_slug': self.slug})

    def __str__(self):
        return f"{self.parent_category.name} - {self.name}"

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image_small = models.ImageField(upload_to='products_small/')
    image_medium = models.ImageField(upload_to='products_medium/')
    image_large = models.ImageField(upload_to='products_large/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image_small) as img_small:
            img_small = img_small.resize((100, 100))
            img_small.save(self.image_small.path)

        with Image.open(self.image_medium) as img_medium:
            img_medium = img_medium.resize((300, 300))
            img_medium.save(self.image_medium.path)

        with Image.open(self.image_large) as img_large:
            img_large = img_large.resize((600, 600))
            img_large.save(self.image_large.path)

    def get_absolute_url(self):
        return reverse('show_product', kwargs={'product_slug': self.slug})

    def __str__(self):
        return f"{self.subcategory.parent_category.name} - {self.subcategory.name} - {self.name}"

    class Meta:
        ordering = ['name']


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина {self.user.username}:"

    def total_quantity(self):
        return sum([item.quantity for item in self.items.all()])

    def total_price(self):
        return sum([item.total_price() for item in self.items.all()])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}шт. {self.product.name} - {self.product.price}руб"

    def total_price(self):
        return self.product.price * self.quantity