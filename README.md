# Django-eccomerce for Learning HTML/CSS

# Read more..

Untuk membuat model hingga menampilkan halaman template HTML di Django, Anda perlu mengikuti beberapa langkah dasar. Berikut adalah langkah-langkah umumnya:

1. **Membuat Aplikasi Django**: Pastikan Anda telah membuat aplikasi Django menggunakan perintah `django-admin startproject namaproyek`.
2. **Membuat Aplikasi**: Buat aplikasi di dalam proyek Django Anda dengan menggunakan perintah `python manage.py startapp namaaplikasi`.
(Langka 1, 2 telah dijelaskan dalam pertemuan sebelumnya)
3. **Definisikan Model**: Dalam file `models.py` di aplikasi Anda, definisikan model Anda dengan properti dan relasi yang sesuai.
>Model telah tersedia.. Scroll down.
4. **Migrasi Database**: Jalankan perintah `python manage.py makemigrations` dan `python manage.py migrate` untuk membuat dan menerapkan migrasi ke basis data.
5. **Membuat Tampilan (Views)**: Buat tampilan di file `views.py` aplikasi Anda untuk menangani permintaan HTTP dan berinteraksi dengan model.
>Views telah tersedia.. Scroll down.
6. **Definisikan URL**: Tentukan URL untuk tampilan Anda di dalam file `urls.py` aplikasi Anda atau proyek Anda. 
>URL telah tersedia.. Scroll down.
7. **Buat Template HTML**: Buat file template HTML di dalam direktori `templates` di dalam direktori aplikasi Anda.
>HTML telah tersedia.. Scroll down.

8. **Jalankan Server Django**: Jalankan server pengembangan Django dengan perintah `python manage.py runserver`.

9. **Akses Halaman**: Buka browser dan akses halaman yang sesuai dengan URL yang telah Anda tentukan, misalnya `http://localhost:8000/`.

Dengan mengikuti langkah-langkah ini, Anda dapat membuat model, menampilkan data dari model tersebut di halaman template HTML, dan menangani permintaan HTTP menggunakan Django. Pastikan untuk menyesuaikan nama model, tampilan, URL, dan template sesuai dengan kebutuhan aplikasi Anda.

# PROJECT ECCOMERCE

# Buat Model:

## 1. Definisikan kelas model:
[File Model.py](https://github.com/hermantoXYZ/django-eccomerce/edit/main/accounts/models.py)
```
# tambahkan model Category, Product, Order, OrderItem, Costumer
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Adding the quantity field
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Calculated subtotal based on quantity and product price

    def save(self, *args, **kwargs):
        # Calculate subtotal based on product price and quantity
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name
    

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='page_images/')
    created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, max_length=255)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
#DevelopHermantoXYZ

```
## 2. Migrasi Basis Data:

Buat migrasi dengan menjalankan perintah 
```
python manage.py makemigrations
```
Terapkan migrasi dengan menjalankan perintah 
```
python manage.py migrate
```


## 3. Untuk menampilkan model-model yang Anda buat di Django Admin, Anda dapat melakukan langkah-langkah berikut:

[File Admin.py](https://github.com/hermantoXYZ/django-eccomerce/blob/main/accounts/admin.py)
```
from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Customer, Page


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)

admin.site.register(Page)
```

untuk memastikan, cek dashboard admin login ke 
- http://127.0.0.1:8000/admin/ 

![Admin Dashboard](https://github.com/hermantoXYZ/django-eccomerce/blob/main/screenshot/2.JPG)

## 4. Buat sebuah fungsi tampilan baru di views.py untuk menampilkan models.py

[File views.py](https://github.com/hermantoXYZ/django-eccomerce/blob/main/accounts/views.py)

```
from django.shortcuts import render
#tambahkan product dalam views.py
from .models import Product, Order, Page
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderForm

#Product List
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Menampilkan Product list di home.html
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# Menampilkan Product Detail
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

# Menampilkan order Create
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

# Menampilkan Page Detail
def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'page_detail.html', {'page': page})
```


## 5 Tambahkan pola URL yang mengarah ke fungsi

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/create/', views.order_create, name='order_create'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]

```

## 6 Buat Formulir untuk memasukan data pesanan
> Anda perlu membuat formulir untuk memasukkan data pesanan. Buatlah file forms.py dalam aplikasi Anda dan tambahkan formulir seperti ini:

```
#accounts\forms.py
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    # Tambahkan field quantity ke dalam form
    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'address', 'products', 'total_price', 'quantity']

```
[File Forms.py](https://github.com/hermantoXYZ/django-eccomerce/blob/main/accounts/forms.py)



## 7 Menampilkan daftar halaman di template HTML

[File Template HTML](https://github.com/hermantoXYZ/django-eccomerce/tree/main/templates)

![List HTMl](https://github.com/hermantoXYZ/django-eccomerce/blob/main/screenshot/1.JPG)

## Page website Eccomerce
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/products/ (list products)
- http://127.0.0.1:8000/products/1/ (order detail)
- http://127.0.0.1:8000/orders/ (list order)
- http://127.0.0.1:8000/order/create/?product_id=1 (buat pesanan)
- http://127.0.0.1:8000/page/about/ etc


![List Galery](https://github.com/hermantoXYZ/django-eccomerce/blob/main/screenshot/3.JPG)
![List Galery](https://github.com/hermantoXYZ/django-eccomerce/blob/main/screenshot/4.JPG)
![List Galery](https://github.com/hermantoXYZ/django-eccomerce/blob/main/screenshot/5.JPG)
![List Galery](https://github.com/hermantoXYZ/django-eccomerce/blob/main/screenshot/6.JPG)
![List Galery](https://github.com/hermantoXYZ/django-eccomerce/blob/main/screenshot/7.JPG)


## License <a name="license"></a>
XYZHermanto. Check `LICENSE`.
