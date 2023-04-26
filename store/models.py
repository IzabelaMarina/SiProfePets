from django.db import models
import datetime

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Categoria.objects.all()
  
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100)
  
    # to save the data
    def registra(self):
        self.save()
  
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Cliente.objects.get(email=email)
        except:
            return False
    
    @staticmethod
    def get_customer_by_id(ids):
        try:
            return Cliente.objects.get(id=ids)
        except:
            return False
  
    def isExists(self):
        
        print("cliente:")
        print(self.email)
        if Cliente.objects.filter(email=self.email):
            return True
  
        return False

class Fornecedore(models.Model):
    nome = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    delivery_time = models.DurationField()
  
    # to save the data
    def registra(self):
        self.save()
  
    @staticmethod
    def get_fornecedor_by_name(name):
        try:
            return Fornecedore.objects.get(nome=name)
        except:
            return False
  
    def isExists(self):
        if Fornecedore.objects.filter(nome=self.nome):
            return True
  
        return False

class Produto(models.Model):
    name = models.CharField(max_length=60)
    price = models.FloatField(default=0)
    custo = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    fornecedor = models.ForeignKey(Fornecedore,on_delete=models.CASCADE,default=1)
    descrição = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(default=None, upload_to='store/static/products')
  
    @staticmethod
    def get_products_by_id(ids):
        return Produto.objects.filter(id__in=ids)
  
    @staticmethod
    def get_all_products():
        return Produto.objects.all()
  
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Produto.objects.filter(categoria=category_id)
        else:
            return Produto.get_all_products()

class Pedido(models.Model):
    product = models.ForeignKey(Produto,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Cliente,
                                 on_delete=models.CASCADE)
    address = models.CharField(max_length=50, default='', blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
  
    def placeOrder(self):
        self.save()
    
    def updatePrice(self):
        self.price = self.product.price*self.quantity
  
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Pedido.objects.filter(customer=customer_id).order_by('-date')
