from django.contrib import admin
from .models import Produto
from .models import Categoria
from .models import Cliente
from .models import Fornecedore
from .models import Pedido

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'categoria']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register your models here.
admin.site.register(Produto,AdminProduct)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Fornecedore)