from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Category, Product, Order, OrderItem
from .cart import Cart
import logging
import uuid

logger = logging.getLogger(__name__)

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    context = {
        'products': products,
        'categories': categories,
        'query': query,
    }
    logger.info(f'Product list view accessed, showing {products.count()} products')
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    context = {
        'product': product,
    }
    logger.info(f'Product detail view accessed for {product.name}')
    return render(request, 'store/product_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/category_detail.html', context)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock >= quantity:
        cart.add(product=product, quantity=quantity)
        messages.success(request, f'{product.name} added to cart')
        logger.info(f'Product {product.name} added to cart')
    else:
        messages.error(request, f'Sorry, only {product.stock} items available')
    
    return redirect('store:product_detail', slug=product.slug)

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} removed from cart')
    return redirect('store:cart_detail')

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Your cart is empty')
        return redirect('store:cart_detail')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            order_id=str(uuid.uuid4())[:8].upper(),
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            postal_code=request.POST['postal_code'],
            city=request.POST['city'],
        )
        
        # Create order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
            # Update product stock
            product = item['product']
            product.stock -= item['quantity']
            product.save()
        
        # Calculate total cost
        order.total_cost = cart.get_total_price()
        order.save()
        
        # Clear cart
        cart.clear()
        
        messages.success(request, f'Order {order.order_id} placed successfully!')
        logger.info(f'Order {order.order_id} created for user {request.user.username}')
        
        return redirect('store:order_detail', order_id=order.order_id)
    
    return render(request, 'store/checkout.html', {'cart': cart})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})
