from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
import os
# Create your models here.

# on_delete = models.cascade định nghĩa hành vi khi đối tượng liên kết bị xóa, thường dùng cho khóa ngoại

# tạo ra tên file mới cho file upload dựa trên thời gian hiện tại và tên file gốc
# nếu dùng vào field hình ảnh thì dùng "upload_to= namefile"
def getFileName(requset, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join('uploads/', new_filename)

# chú ý đang sử dụng tuple
STATE_CHOICES = (
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Daman and Hiu', 'Daman and Hiu'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES=(
    ('H', 'Hat'),
    ('S', 'Shoe'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
    ('MB', 'Mobile')
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20)
    product_image = models.ImageField(upload_to="productimg")

    def __str__(self):
        return str(self.id)
    
    @property
    def final_price(self):
        return self.selling_price - self.discounted_price

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    
    # PositiveSmallIntegerField số không âm(nguyên dương) từ 0 -> 32767
    # PositiveIntegerField số không âm(nguyên dương) từ 0 -> 2147483647
    # số lượng thì không âm, dùng "positive small" tiết kiệm bộ nhớ và dùng cho dữ liệu nhỏ  

    def __str__(self):
        return str(self.id)

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 50, choices=STATE_CHOICES,default='Pending')
    