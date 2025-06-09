
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from store.models import Product
from category.models import Category

from carts.models import Cart, CartItem
from carts.views import _cart_id

def store(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        page = request.GET.get('page')
        paginator = Paginator(products, 4)
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        page = request.GET.get('page')
        page = page or 1
        paginator = Paginator(products, 25)
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context=context)


def product_detail(request, category_slug, product_slug=None):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id =_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e
        
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
        product_count = products.count()
    context = {
        'products': products,
        'keyword': keyword,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)