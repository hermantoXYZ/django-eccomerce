from django.shortcuts import render
#tambahkan product dalam views.py
from .models import Product, Order, Page
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderForm


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, product_id):
    # Dapatkan objek produk berdasarkan ID atau tampilkan 404 jika tidak ditemukan
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

def order_create(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            total_price = product.price * quantity  # Hitung total harga
            order = form.save(commit=False)
            order.total_price = total_price
            order.save()  # Simpan objek Order terlebih dahulu
            order.products.add(product, through_defaults={'quantity': quantity})
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm(initial={'products': [product]})
    return render(request, 'order_create.html', {'form': form})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'page_detail.html', {'page': page})