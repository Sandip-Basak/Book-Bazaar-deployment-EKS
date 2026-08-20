from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from user.models import *
from store.models import *
from django.contrib import messages
from datetime import date

# Create your views here.
@login_required(login_url='/signin')
def profile(request):

    if request.method == 'POST':
        user_data = User_Data.objects.get(user=request.user)
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_photo = request.FILES.get('profile_photo')
        # Update user data
        print(profile_photo)
        user_data.phone = phone
        user_data.address = address
        if profile_photo:
            user_data.profile_photo = profile_photo
        user_data.save()

    if request.user.is_authenticated:
        user_data=User_Data.objects.get(user=request.user.id)
        data={
            'user_data': user_data
        }
    return render(request,"profile.html",data)

@login_required(login_url='/signin')
def signout(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/signin')
def wishlist(request):
    if request.user.is_authenticated:
        user_data=User_Data.objects.get(user=request.user.id)
        data={
            'user_data': user_data
        }
    wl=Wishlist.objects.filter(user=request.user.id)
    data["wishlist"]=wl
    return render(request,"wishlist.html",data)

@login_required(login_url='/signin')
def cart(request):
    if request.user.is_authenticated:
        user_data=User_Data.objects.get(user=request.user.id)
        data={
            'user_data': user_data
        }
    cl=Cart.objects.filter(user=request.user.id)
    data["cart"]=cl
    return render(request,"cart.html",data)

@login_required(login_url='/signin')
def purchase(request):
    cl=Cart.objects.filter(user=request.user.id)
    for i in cl:
        inventory=Inventory.objects.get(book=i.book)
        inventory.quantity-=1
        inventory.sales+=1
        inventory.save()

        new_order=Orders(user=request.user, book=i.book, date=date.today())
        new_order.save()

        i.delete()
    messages.success(request, "Order Placed")
    return redirect("/profile")

@login_required(login_url='/signin')
def orders(request):
    if request.user.is_authenticated:
        user_data=User_Data.objects.get(user=request.user.id)
        data={
            'user_data': user_data
        }
    ol=Orders.objects.filter(user=request.user.id)
    data["order"]=ol
    return render(request, "orders.html", data)
