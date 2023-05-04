from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from .forms import *

urlpatterns = [
    # path('', views.home, name='home'),
    path("", views.ProductView.as_view(), name="home"),
    # -----------------------Cart---------------------------- #
    path("product-detail/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="show-cart"),
    path("plus_cart/", views.plus_cart), path("minus_cart/", views.minus_cart),
    path("remove_cart/", views.remove_cart),
    # -----------------------Cart---------------------------- #
    
    path("buy/", views.buy_now, name="buy-now"),
    
    path("address/", views.address, name="address"),
    path("remove_address/", views.remove_address),
    
    path("orders/", views.orders, name="orders"),
    path("mobile/", views.mobile, name="mobile"),
    path("mobile/<slug:data>", views.mobile, name="mobiledata"),
    path("checkout/", views.checkout, name="checkout"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    
    path("profile/", views.ProfileViews.as_view(), name="profile"),
    
    # -----------------------User Form---------------------------- #
    path("registration/", views.CustomerRegistrationView.as_view(), name="customerregistration"),
    # dùng class-based view "LoginView" thì không cần dẫn trong views.py nữa thay vào đó là dẫn trong template_name
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="user/login.html",
            authentication_form=LoginForm,
            success_url="/",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),  
      
    path("logout", auth_views.LogoutView.as_view(next_page="/accounts/login/"), name="logout"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="user/password_change.html",
            form_class=PasswordChangeForm,
            success_url="/password_change_done/",
        ),
        name="password_change",
    ),
    path(
        "password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="user/password_change_done.html"),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="user/password_reset.html", form_class=PasswordResetForm),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetView.as_view(template_name="user/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user/password_reset_confirm.html", form_class=PasswordSetForm
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetView.as_view(template_name="user/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    # --------------------------------------------------- #
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
