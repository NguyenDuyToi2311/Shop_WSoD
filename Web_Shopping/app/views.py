from django.shortcuts import render
from django.views import View
from .models import *
# def home(request):
    # return render(request, 'main/home.html')
class ProductView(View):
    def get(sefl, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        shoes = Product.objects.filter(category='S')
        #pr = Product.objects.all()
        context = {'topwears':topwears, 'bottomwears':bottomwears, 'shoes':shoes}
        return render(request, 'main/home.html', context)
        #return render(request, 'main/home.html', {'pr':pr})


#def product_detail(request):
#    return render(request, 'productdetail.html')
# tạo product view kế thừa từ View
# truy suất tất cả product sử dụng get lấy gí trị theo ID(pk khóa ngoại)
class ProductDetailView(View):
    def get(sefl, request, pk):
        product = Product.objects.get(pk=pk)
        context = {'product': product, 'footer':True} 
        return render(request, 'main/productdetail.html', context)


def mobile(request, data=None):
    if data== None:
        mobiles = Product.objects.filter(category="MB")
    elif data == "Xiaomi" or data == "Samsung" or data=="Apple":
        mobiles = Product.objects.filter(category="MB").filter(brand=data)
    elif data == "below":
        mobiles = Product.objects.filter(category="MB").filter(selling_price__lt=1000)
    elif data == "above":
        mobiles = Product.objects.filter(category="MB").filter(selling_price__gt=1000)
    context = {'mobiles':mobiles, 'footer':True}
    return render(request, 'mobile.html', context)
    



def add_to_cart(request):
    return render(request, 'general/addtocart.html')

def buy_now(request):
    return render(request, 'general/buynow.html')

def address(request):
    return render(request, 'general/address.html')

def checkout(request):
    return render(request, 'general/checkout.html')

def orders(request):
    return render(request, 'general/orders.html')

def profile(request):
    return render(request, 'user/profile.html')

def change_password(request):
    return render(request, 'user/changepassword.html')

def login(request):
    return render(request, 'user/login.html')

def customerregistration(request):
    return render(request, 'user/customerregistration.html')




