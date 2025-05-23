from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Order , OrderLine
from django.contrib.auth.decorators import login_required
from .forms import ProductForm , RegisterForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'product_list.html', {'products': products, 'categories': categories})

def product(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'allProducts.html', {'products': products, 'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'ProductDetails.html', {'product': product})

@login_required
def create_order_from_cart(request):
    panier = request.session.get('panier', {})

    if not panier:
        return redirect('afficher_panier')  # Rediriger si panier vide

    # Créer la commande
    order = Order.objects.create(user=request.user)

    # Créer chaque ligne de commande
    for product_id, quantity in panier.items():
        product = get_object_or_404(Product, id=product_id)
        OrderLine.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

    # Vider le panier
    request.session['panier'] = {}

    return render(request, 'order_success.html', {'order': order})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return render(request, 'product_confirm_delete.html', {'product': product})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def ajouter_au_panier(request, product_id):
    produit = get_object_or_404(Product, id=product_id)
    
    panier = request.session.get('panier', {})

    if str(product_id) in panier:
        panier[str(product_id)] += 1
    else:
        panier[str(product_id)] = 1

    request.session['panier'] = panier

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def afficher_panier(request):
    panier = request.session.get('panier', {})
    produits = []
    total = 0

    for product_id, quantity in panier.items():
        produit = get_object_or_404(Product, id=product_id)
        sous_total = produit.price * quantity
        total += sous_total
        produits.append({
            'produit': produit,
            'quantite': quantity,
            'sous_total': sous_total
        })

    return render(request, 'panier.html', {'produits': produits, 'total': total})


def supprimer_du_panier(request, product_id):
    panier = request.session.get('panier', {})
    if str(product_id) in panier:
        del panier[str(product_id)]
        request.session['panier'] = panier
    return redirect('panier')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')

    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    return render(request, 'order_detail.html', {'order': order})

def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'dashboard.html', {
        'total_products': total_products,
        'total_categories': total_categories,
    })
    else:
        return HttpResponse("Vous n'avez pas accès à cette page.")
