from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"


# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "home-page.html", context)


def checkout(request):
    return render(request, "checkout-page.html")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "products.html", context)
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(

        item=item,
        user=request.user,
        ordered=False,


    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "this item quantity was updated")
        else:

            order.items.add(order_item)
            messages.info(request, "this item was added to your cart")
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "this item was added to your cart")
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # checks order  item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(

                item=item,
                user=request.user,
                ordered=False,
            )[0]
            order.items.remove(order_item)
            messages.info(request, "this item was removed from your cart")
            return redirect("core:product", slug=slug)
        else:
            # add a message saying user doesnt have a order
            messages.info(request, "this item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying user doesnt have a order
        messages.info(request, "no activate order")
        return redirect("core:product", slug=slug)
