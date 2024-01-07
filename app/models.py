from django.db import models
import uuid

class Registered_Users(models.Model):
    email = models.EmailField(max_length=80)
    password = models.CharField(max_length=20)
    user_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


    def __str__(self):
        return f'{self.email}  -  {self.password}'


class Client(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.name} | {self.lastname} | {self.phone} | {self.email}'


class Salesman(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=80)
    employment_date = models.DateField()
    position = models.CharField(max_length=50)
    products = models.ManyToManyField("Product", related_name='salesmen_products')

    def __str__(self):
        return f'{self.name} | {self.lastname} | {self.phone} | {self.email} | {self.employment_date} | {self.position}'


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=350)

    def __str__(self):
        return f'{self.name} --- {self.description}'


class Sales(models.Model):
    client = models.ForeignKey("Client", on_delete=models.RESTRICT, related_name='sales')
    salesman = models.ForeignKey("Salesman", on_delete=models.RESTRICT, related_name='sales')
    product = models.ManyToManyField("Product", related_name='sales')
    sales_date = models.DateTimeField()
    cash_amount = models.FloatField()

    def get_products(self):
        lst = []
        for i in self.product.all():
            lst.append(f"{i.name} \\ {i.description}")

        return " | ".join(lst)

    def __str__(self):
        return f'{self.client} | {self.salesman} | {self.get_products()} | {self.sales_date} | {self.cash_amount}'