from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from store.forms import *
from django.contrib import messages
from store.models import *
from user.models import *


# Create your views here.
def home(request):
    best_sellers=Inventory.objects.order_by('-sales')[:4]
    latest_books = Book.objects.order_by('-date')[:4]
    data={
        'best_sellers': best_sellers,
        'latest_books': latest_books
    }
    if request.user.is_authenticated:
        user_data=User_Data.objects.get(user=request.user.id)
        data['user_data']=user_data
    return render(request, "index.html", data)

def signin(request):
    if request.user.is_authenticated:
        return redirect("/profile")
    if request.method == "POST":
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return redirect('/profile')
        else:
            messages.warning(request, "Invalid Login Credentials")
    else:
        form = SignInForm()
    data = {'form': form}
    return render(request, 'signin.html', data)

def signup(request):
    if request.user.is_authenticated:
        return redirect("/profile")
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                u=form.save()
                user_data=User_Data(user=u)
                user_data.save()
                messages.success(request, "Account Created")
            except Exception as e:
                print(e)
                messages.warning(request, "Some Error Occured")
    else:
        form = SignUpForm()
    data = {"form": form}
    return render(request, "signup.html", data)

def store(request, type="all"):
    if type=="all":
        books=Book.objects.all()
        name='Our Entire Collection'
    elif type=="latest-books":
        books=Book.objects.order_by('-date')
        name='Our Latest Collection'
    elif type=="best-sellers":
        top_inventory = Inventory.objects.order_by('-sales')
        books = [inventory.book for inventory in top_inventory]
        name='Best Sellers of all time'
    data={
            'books': books,
            'name': name
        }
    if request.user.is_authenticated:
        user_data=User_Data.objects.get(user=request.user.id)
        data['user_data']=user_data

    return render(request,"store.html",data)

def product(request, id):
    book=Book.objects.get(bid=id)
    top_inventory = Inventory.objects.order_by('-sales')
    best_sellers = [inventory.book for inventory in top_inventory]
    data={
        'book': book,
        'best_sellers': best_sellers
    }
    if request.user.is_authenticated:
        user_data=User_Data.objects.get(user=request.user.id)
        data['user_data']=user_data

    if(Wishlist.objects.filter(book=id, user=request.user.id).exists()):
        data['wishlist']=True
    else:
        data['wishlist']=False

    if(Cart.objects.filter(book=id, user=request.user.id).exists()):
        data['cart']=True
    else:
        data['cart']=False

    return render(request, "product.html", data)

@login_required(login_url='/signin')
def update_wishlist(request, type, id):
    if(type=="add"):
        if(Wishlist.objects.filter(book=id, user=request.user.id).exists()):
            messages.warning(request, "Item already Exists")
        else:
            new_data=Wishlist(book=Book.objects.get(bid=id), user=request.user)
            new_data.save()
            messages.success(request, "Item added to wishlist")
    elif(type=="remove"):
        if(Wishlist.objects.filter(book=id, user=request.user.id).exists()):
            data=Wishlist.objects.get(book=id, user=request.user.id)
            data.delete()
        else:
            messages.warning(request, "Item dosen't exist")
    
    return redirect(f"/book/{id}")

@login_required(login_url='/signin')
def update_cart(request, type, id):
    if(type=="add"):
        if(Cart.objects.filter(book=id, user=request.user.id).exists()):
            messages.warning(request, "Item already Exists")
        else:
            new_data=Cart(book=Book.objects.get(bid=id), user=request.user)
            new_data.save()
            messages.success(request, "Item added to Cart")
    elif(type=="remove"):
        if(Cart.objects.filter(book=id, user=request.user.id).exists()):
            data=Cart.objects.get(book=id, user=request.user.id)
            data.delete()
        else:
            messages.warning(request, "Item dosen't exist")
    
    return redirect(f"/book/{id}")

