from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Produto,Categoria,Pedido,Fornecedore,Cliente
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from django.views import View

# Create your views here.

class Main(View):

     def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    if quantity < Produto.get_products_by_id(product)[0].quantity:
                        cart[product] = quantity+1
                    else:
                        print(quantity)
                        print(Produto(product).quantity)
  
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
  
        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')
  
     def get(self, request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
  
  
def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Categoria.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Produto.get_all_products_by_categoryid(categoryID)
    else:
        products = Produto.get_all_products()
  
    data = {}
    data['products'] = products
    data['categories'] = categories
  
    print('Você : ', request.session.get('email'))
    return render(request, 'store.html', data)


class Cart(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    if quantity < Produto(product).quantity:
                        cart[product] = quantity+1
                    else:
                        print(quantity)
                        print(Produto.get_products_by_id(product)[0].quantity)
  
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        return redirect('homepage')
        

    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Produto.get_products_by_id(ids)
        size=len(products)
        print(products)
        return render(request , 'cart.html' , {'products' : products, 'size' : size} )

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        customer = request.session.get('customer')
        print("customer:",customer)
        cart = request.session.get('cart')
        products = Produto.get_products_by_id(list(cart.keys()))
        print(address, customer, cart, products)
        if Cliente.get_customer_by_id(customer) != False:
            customer_aux=Cliente.get_customer_by_id(customer)
            print("cliente:",customer_aux)
            print("email:", customer_aux.email)
            print("teste: ", customer)
            print("Entrou no if")
            customer_aux.save()
            for product in products:
                print(cart.get(str(product.id)))
                order = Pedido(customer=customer_aux,
                            product=product,
                            address=address,
                            quantity=cart.get(str(product.id)))
                order.updatePrice()
                product.quantity -= order.quantity
                product.save() 
                order.save()
            request.session['cart'] = {}
            return redirect('homepage')
        else:
            return redirect('login')

    def get(self, request):
        cart = request.session.get('cart')
        products = Produto.get_products_by_id(list(cart.keys()))

        data={'items':products}
  
        return render(request , 'checkout.html' , data )


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Cliente.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Inválido !!'
        else:
            error_message = 'Senha ou usuário inválidos!'

        print (email, password)
        return render (request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        name = postData.get ('name')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'name': name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Cliente (name=name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer (customer)

        if not error_message:
            print (name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.registra()
            return redirect('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.name):
            error_message = "Insira seu nome"
        elif len (customer.name) < 3:
            error_message = 'O nome deve ter pelo menos 3 caracteres'
        elif not customer.phone:
            error_message = 'Insira seu telefone (com DDD)'
        elif len (customer.phone) < 10 or len (customer.phone) > 11:
            error_message = 'O número de telefone deve ter 10 ou 11 algarismos'
        elif len (customer.password) < 5:
            error_message = 'A senha deve ter pelo menos 5 dígitos'
        elif len (customer.email) < 5:
            error_message = 'O email deve ter pelo menos 5 dígitos'
        elif customer.isExists():
            error_message = 'Esse email já está registrado'
        # saving

        return error_message



def home(request):
    return HttpResponse("Hello world! Home do coiso de DB ;)")