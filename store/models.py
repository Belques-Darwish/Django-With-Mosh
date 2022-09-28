from django.db import models
from django.utils.translation import gettext_lazy as _


class Promotion(models.Model):
    """
    Promotion class for add promotion to the product
    """
    descritption = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    """
    Collection class is for products
    """
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Product(models.Model):
    """
    Product class is the tabel that store data about products
    """
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField()
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Price"))
    inventory = models.IntegerField(verbose_name=_("Inventory"))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_("Last Update"))
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion)


class Customer(models.Model):
    """
    Customer class is the tabel that store data about customers
    """
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=255, verbose_name=_("Phone"))
    birth_date = models.DateField(null=True, verbose_name=_("Birthdate"))
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    class Meta:
        db_table = 'store_customers'


class Order(models.Model):
    """
    Order Class that show the orders
    """
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENTSTATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
        (PAYMENT_STATUS_FAILED,'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Placed At"))
    payment_status = models.CharField(max_length=1, choices=PAYMENTSTATUS_CHOICES, default=PAYMENT_STATUS_PENDING, verbose_name=_("Payment Status"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Customer"))


class OrderItem(models.Model):
    """
    OrderItem class to represent relation between order and item,
    and relation between product and item
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Product"))
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name=_("Order"))
    quantity = models.PositiveSmallIntegerField(verbose_name=_("Quantity"))
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Unit Price"))


class Address(models.Model):
    """
    Address class is that to describe the address for customer
    """
    street = models.CharField(max_length=255, verbose_name=_("Street"))
    city = models.CharField(max_length=255, verbose_name=_("City"))
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"))
    zip = models.CharField(max_length=255, verbose_name=_("ZIP"))


class Cart(models.Model):
    """
    Cart class is to shopping cart
    """
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_("Cart"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    quantity = models.PositiveSmallIntegerField(verbose_name=_("Quantity"))
    