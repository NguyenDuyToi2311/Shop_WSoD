from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# def home(request):
    # return render(request, 'main/home.html')
class ProductView(View):
    def get(sefl, request):
        total_item = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        shoes = Product.objects.filter(category='S')
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user = request.user))
        context = {'topwears':topwears, 'bottomwears':bottomwears, 'shoes':shoes, 'total_item':total_item}
        return render(request, 'main/home.html', context)
        


# def product_detail(request):
#    return render(request, 'productdetail.html')
# tạo product view kế thừa từ View
# truy suất tất cả product sử dụng get lấy gí trị theo ID(pk khóa ngoại)

class ProductDetailView(View):
    def get(sefl, request, pk):
        total_item=0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user = request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        context = {'product': product, 'footer':True, 'item_already_in_cart':item_already_in_cart, 'total_item':total_item} 
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
    

# get() truy vấn 1 đối tượng duy nhất từ csdl và trả về đối tượng đó
# filter() truy vấn lấy tập hợp các đối tượng từ csdl trả về chứa tất cả các đối tượng thỏa mãn điều kiện được chỉ định
# GET.get()là phương thức của đối tượng request trong Django, dùng để truy xuất các tham số truy vấn trong đường dẫn url
@login_required
@csrf_exempt
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')
    
    # if request.method == 'POST' and request.is_ajax():
        
    #     product_id = request.POST('product_id')
    #     quantity = request.POST('quantity', 1)
    #     product = get_object_or_404(Product, id=product_id)
    #     # try:
    #     cart_item = Cart.objects.get(cart_user=user, product=product)
    #     cart_item.quantity += int(quantity)
    #     cart_item.save()
    #     # except Cart.DoesNotExist:
    #     # cart_item = Cart(cart=Cart.objects.get_or_create(user=user)[0], product=product, quantity=quantity)
    #     # cart_item.save()
    #     response_data = {'success': True}
    #     return JsonResponse(response_data)
    # return redirect('/')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 10.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.final_price)
                amount += tempamount
                total_amount = amount+ shipping_amount
        context = {'cart':cart, 'total_amount':total_amount, 'amount':amount,'shipping_amount':shipping_amount}
        return render(request, 'general/addtocart.html', context)
    else:
        return redirect('login')
# Trong Django, Q là một đối tượng để xây dựng các truy vấn phức tạp hơn với các biểu thức logic "OR", AND NOT
# xây dựng các truy vấn có chứa nhiều điều kiện và kết hợp chúng lại với nhau

# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id =  request.GET['prod_id']
#         c= Cart.objects.get(Q(product=prod_id) & Q(user = request.user)) 
#         c.quantity+=1
#         c.save()
#         amount = 0.0
#         shipping_amount = 10.0
#         cart_product = [p for p in Cart.objects.all() if p.user == request.user]
#         for p in cart_product:
#             tempamount= (p.quantity * p.product.final_price)
#             amount += tempamount
#             total_amount = amount+ shipping_amount
#         data={
#             'quantity':c.quantity,
#             'amount': amount,
#             'total_amount': total_amount
#         },
#         return JsonResponse(data)
def plus_cart(request):
    user = request.user
    if request.method == 'GET': # kiểm tra yếu cầu có GET hay không
        prod_id = request.GET['prod_id'] 
        # lấy ID sản phẩm mà người dùng muốn thêm vào giỏ hàng từ tham số của request.GET.
        c, created = Cart.objects.get_or_create(user=user, product_id=prod_id)
        
        if not created:
            c.quantity += 1
            c.save()
        # Sử dụng hàm get_or_create() để tìm hoặc tạo một đối tượng Cart mới, liên kết với sản phẩm và người dùng hiện tại. 
        # Nếu đối tượng đã tồn tại trước đó, chúng ta tăng số lượng lên 1 và lưu lại
        amount = 0.0
        shipping_amount = 10.0
        cart_products = Cart.objects.filter(user=user) # lấy tất cả sản phẩm trong giỏ hàng
        for cart_product in cart_products:
            # chúng ta tính toán tổng số tiền hiện tại của giỏ hàng bằng cách lấy giá của 
            # từng sản phẩm và nhân với số lượng tương ứng, sau đó cộng dồn lại với nhau.
            tempamount = (cart_product.quantity * cart_product.product.final_price)
            amount += tempamount
            total_amount = amount + shipping_amount
        data = {
            'quantity': c.quantity, 
            'amount': amount,
            'total_amount': total_amount
        }
        return JsonResponse(data)
def minus_cart(request):
    user = request.user
    if request.method == 'GET': # kiểm tra yếu cầu có GET hay không
        prod_id = request.GET['prod_id'] 
        # lấy ID sản phẩm mà người dùng muốn thêm vào giỏ hàng từ tham số của request.GET.
        c, created = Cart.objects.get_or_create(user=user, product_id=prod_id)
        
        # if not created:
        #     c.quantity -= 1
        #     c.save()
        # tạo disable cho javascript để khi sản phẩm bé hơn 1 thì không cho dùng minus  
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
            disable = False
        else:
            disable = True
        # Sử dụng hàm get_or_create() để tìm hoặc tạo một đối tượng Cart mới, liên kết với sản phẩm và người dùng hiện tại. 
        # Nếu đối tượng đã tồn tại trước đó, chúng ta tăng số lượng lên 1 và lưu lại
        amount = 0.0
        shipping_amount = 10.0
        cart_products = Cart.objects.filter(user=user) # lấy tất cả sản phẩm trong giỏ hàng
        for cart_product in cart_products:
            # chúng ta tính toán tổng số tiền hiện tại của giỏ hàng bằng cách lấy giá của 
            # từng sản phẩm và nhân với số lượng tương ứng, sau đó cộng dồn lại với nhau.
            tempamount = (cart_product.quantity * cart_product.product.final_price)
            amount += tempamount
            total_amount = amount + shipping_amount
        data = {
            'quantity': c.quantity, 
            'amount': amount,
            'total_amount': total_amount
        }
        return JsonResponse(data)
def remove_cart(request):
    user = request.user
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(user=user, product_id=prod_id)        
        c.delete()
        cart_products = Cart.objects.filter(user=user)
        amount=0
        shipping_amount = 10
        if cart_products:
            for cart_product in cart_products:
                tempamount = (cart_product.quantity * cart_product.product.final_price)
                amount += tempamount
            total_amount = amount + shipping_amount
        else:
            total_amount = 0
        data = {
            'amount': amount,
            'total_amount': total_amount
        }
        return JsonResponse(data)


@login_required
def address(request):
    add = Customer.objects.filter(user = request.user)
    customer_count = Customer.objects.filter(user=request.user).count()
    context = {'add':add, 'active':'btn-primary', 'customer_count':customer_count}
    return render(request, 'general/address.html', context)

def remove_address(request):
    user = request.user
    if request.method =="GET":
        id = request.GET['id']
        try:
            cus = Customer.objects.get(user=user, id=id)
            cus.delete()
            return JsonResponse({'message': 'Delete success'})
        except Customer.DoesNotExist:
            return JsonResponse({'message': 'Customer not found'}, status=404)
    

@login_required
def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_item = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 10.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.final_price)
                amount += tempamount
            total_amount = amount+ shipping_amount
        context = {'cart_item':cart_item, 'total_amount':total_amount, 'amount':amount,'add':add}
        return render(request, 'general/checkout.html', context)

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid') # lấy custid bên html đồng với name trong thẻ
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OderPlaced(user =user, customer=customer, product = c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
    
@login_required    
def orders(request):
    order = OderPlaced.objects.filter(user=request.user)
    context = {'order': order}
    return render(request, 'general/orders.html', context)


def buy_now(request):
    return render(request, 'general/buynow.html')


@method_decorator(login_required, name='dispatch')  
class ProfileViews(View):
    def get(self, request):
        form = CustomerProfileForm()
        context = {'form':form, 'active':'btn-primary'}
        return render(request, 'user/profile.html', context)

    def post(self, request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            state = form.cleaned_data['state']
            reg = Customer(user = usr, name = name, address=address, state=state)
            reg.save()
            messages.success(request, "Update Profile Success")
        context = {'form':form, 'active':'btn-primary'}
        return render(request, 'user/profile.html', context)


# def login(request):
#     return render(request, 'user/login.html')

#def customerregistration(request):
#    return render(request, 'user/customerregistration.html')

class CustomerRegistrationView(View):
    # Phương thức get() sẽ trả về trang đăng ký với form rỗng để người dùng điền thông tin
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {'form':form, 'menu':True, 'footer':True}
        return render(request, 'user/customerregistration.html', context)

    def post(self, request):
        # method luôn là POST nên không cần if "request.method =='post'" lại
        # nếu vẫn dùng "request.method =='post'" Python sẽ hiểu đây là một set các string
        # thay vì là một danh sách các string
        form = CustomerRegistrationForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exist")
            else:
                messages.success(request, "Registered successfully")
                form.save()
                return redirect('login')
            
        context = {'form':form, 'menu':True, 'footer':True}
        return render(request, 'user/customerregistration.html', context)
    
    # Phương thức post() sẽ xử lý form khi người dùng submit và 
    # lưu thông tin khách hàng vào database nếu form hợp lệ
    # Nếu form không hợp lệ, view sẽ hiển thị lại trang đăng ký với 
    # các thông tin người dùng đã điền và thông báo lỗi.
    


