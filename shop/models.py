from django.db import models
from django.contrib.auth.models import User
import random
from time import gmtime, strftime
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from tinymce import HTMLField


class coupon(models.Model):
    code = models.CharField(max_length= 20)
    count = models.IntegerField()
    off = models.IntegerField(help_text= 'Off precent')
    expire = models.DateTimeField(verbose_name= 'Expire Date')

    def __str__(self):
        return "Code : {0} - Count : {1}".format(self.code, self.count)

    def is_expire(self):
        if self.expire < timezone.now():
            return True
        else:
            return False

        class Meta:
            verbose_name_plural = "Coupons"

    

class States(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name_plural = "State Table"

class MyUsers(models.Model):
    KHABAR_CHOISES = {
        ('TRUE', 'مشترک خبرنامه'),
        ('FALSE', 'عدم اشتراک در خبرنامه'),
    }
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'MyUsers')
    phone = models.CharField(max_length = 15)
    city = models.CharField(max_length = 100, null= True, blank = True)
    state = models.ForeignKey(States, on_delete = models.CASCADE, null= True, blank = True)
    address = models.CharField(max_length = 500, null= True, blank = True)
    postcode = models.CharField(max_length = 10, null = True, blank = True)
    KhabarName = models.CharField(max_length = 5, choices = KHABAR_CHOISES, default = 'FALSE', null= True, blank = True)

    def __str__(self):
        return "Username : {0}, Email : {1}".format(self.user.username, self.user.email)

    class Meta:
        verbose_name_plural = "Normal Users"

class color(models.Model):
    name = models.CharField(max_length = 20, help_text = "Enter a Color for Product")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Product Colors"

class Manufactor(models.Model):
    slug = models.SlugField(allow_unicode = True)
    name = models.CharField(max_length = 100)
    logo = models.ImageField(upload_to = 'ManuLogo/', default = 'media/static/ManuLogo/no-image.jpg', null = True, blank = True, width_field='imagewidth', height_field='imageheigth')
    imagewidth = models.PositiveIntegerField(editable = False, default = 50)
    imageheigth = models.PositiveIntegerField(editable = False, default = 50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manufactors"


class kalaCat(models.Model):
    GEN_CHOICES = {
        ("m",'Men'),
        ("f",'female'),
        ("o",'Not mind'),
        ('s', 'Special for sports')
    }
    slug = models.SlugField(allow_unicode= True)
    name = models.CharField(max_length = 100)
    gen = models.CharField(max_length = 1, choices = GEN_CHOICES, default = 'o')

    def __str__(self):
        return "{0} - {1}".format(self.name, self.gen)

    class Meta:
        unique_together = (("name", "gen"), ) 
        verbose_name_plural = "Product Categories"


class PSize(models.Model):
    sizeno = models.CharField(max_length = 20, help_text = "Enter a Size for Product")

    def __str__(self):
        return self.sizeno

    class Meta:
        verbose_name_plural = "Product Sizes"

class Kala(models.Model):
    slug = models.SlugField(allow_unicode= True)
    name = models.CharField(max_length = 150)
    manu = models.ForeignKey(Manufactor, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Manufactor', related_name='manufactor')
    size = models.ManyToManyField(PSize , help_text = "Select sizes for Product")
    mindesc = models.CharField(max_length = 200)
    color= models.ManyToManyField(color , help_text = "Select Colors for Product")
    pic0 = models.ImageField(upload_to= 'KalaImages/{0}'.format(strftime("%Y%m%d - %H%M%S",gmtime())), default = 'static/no-image.jpg', width_field="imagewidth", height_field="imageheigth")
    pic1 = models.ImageField(upload_to= 'KalaImages/{0}'.format(strftime("%Y%m%d - %H%M%S",gmtime())), default = 'static/no-image.jpg', null = True, blank = True)
    pic2 = models.ImageField(upload_to= 'KalaImages/{0}'.format(strftime("%Y%m%d - %H%M%S",gmtime())), default = 'static/no-image.jpg', null = True, blank = True)
    pic3 = models.ImageField(upload_to= 'KalaImages/{0}'.format(strftime("%Y%m%d - %H%M%S",gmtime())), default = 'static/no-image.jpg', null = True, blank = True)
    cat = models.ForeignKey(kalaCat, on_delete=models.SET_NULL, null =True, verbose_name = 'Category', related_name= 'category')
    desc = HTMLField('Description')
    imagewidth = models.PositiveIntegerField(editable = False, default = 220)
    imageheigth = models.PositiveIntegerField(editable = False, default = 330)
    
    # def save(self, *args, **kwargs):
    #     if self._state.adding:
    #         last_id = self.objects.all().aggregate(largest = models.Max('id'))['largest']
    #         if last_id != None:
    #             self.id = last_id + 1
    #     super(Kala, self).save(*args,**kwargs)

    def __str__(self):
        return '{} - {}'.format(self.name, self.manu)

    # def NewPrice(self):
    #     if self.off != 0:
    #         return self.price - (self.price * (self.off / 100))
    #     else:
    #         return self.price

    class Meta:
        verbose_name_plural = "Products"


class KalaInst(models.Model):
    kala = models.ForeignKey(Kala, on_delete = models.CASCADE, related_name= 'kalainst')
    saler = models.ForeignKey(User, on_delete = models.CASCADE)
    price = models.BigIntegerField(verbose_name= "Price")
    off = models.IntegerField(default=0)
    instock = models.IntegerField()

    def __str__(self):
        return "{0} : {1}".format(self.id, self.saler)

    def NewPrice(self):
        if self.off == 0:
            return self.price
        else:
            return  self.price - ((self.price) * (self.off /100))

    class Meta:
        verbose_name_plural = "Product Instances" 


class Comment(models.Model):
    STATUS_CHOICES = {
        ('t', "It's Ok"),
        ('w', "Waiting")
    }
    writer = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    body = models.CharField(max_length = 500)
    date = models.DateField(auto_now_add= True)
    Kala = models.ForeignKey(Kala, on_delete = models.SET_NULL, null = True)
    status = models.CharField(max_length = 1, choices = STATUS_CHOICES, default = 'w')

    class Meta:
        verbose_name_plural = "Comments"

class cart(models.Model):
    SEND_CHOICES = {
        ('T', "Payed"),
        ('F', 'Not Payed')
    }
    username = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Kala, verbose_name=_("Products"), on_delete=models.CASCADE)
    color = models.ForeignKey(color, on_delete=models.CASCADE, related_name= 'color')
    size = models.ForeignKey(PSize, on_delete=models.CASCADE,related_name= 'size')
    saler = models.ForeignKey(KalaInst, on_delete=models.CASCADE, related_name= 'instance', null = True)
    count = models.IntegerField(default= 1)
    coupon = models.ForeignKey(coupon, on_delete=models.CASCADE, null= True, blank= True)
    Payed = models.CharField(max_length = 1, choices = SEND_CHOICES, default = 'F')

    def __str__(self):
        return "Product : {0} - Saler : {1} - User : {2}  ".format(self.product.name, self.saler.saler, self.username)

    def total(self):
        return self.saler.price * self.count

    def totalPrice(self):
        if self.saler.off != 0:
            return int(self.total() * (1 - (self.saler.off / 100)))
        else:
            return self.total()

    def finallyPrice(self):
        if self.coupon:
            return int(self.totalPrice() * (1 - (self.coupon.off / 100)))
        return self.totalPrice()

    class Meta:
        verbose_name_plural = "Carts"


class Salled(models.Model):
    SEND_CHOICES = {
        ('T','Packege sent'),
        ('F','Packege Wait for send'),
        ('B','Back to Store'),
    }
    FollowUpCode = models.CharField(default= '{}{}'.format(random.randint(10,99),strftime('%Y%m%d%H%M%S',gmtime())), max_length = 20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Buyer')
    products = models.ManyToManyField(cart, verbose_name= 'Products')
    company = models.CharField(max_length= 200, null= True, blank = True)
    address = models.CharField(max_length= 500)
    zip_code = models.CharField(max_length= 10, verbose_name = 'Zip Code')
    state = models.ForeignKey(States, on_delete= models.CASCADE)
    city = models.CharField(max_length= 50)
    total_price = models.BigIntegerField(help_text = 'Total Price With offers & Coupons')
    send_price = models.IntegerField()
    tax = models.IntegerField()
    total = models.BigIntegerField(help_text = 'Total Price With offers, Coupons, tax & send price.')
    desc = models.TextField(null= True, blank= True)
    date = models.DateField(auto_now= True)
    sent = models.CharField(help_text= 'Is package sent?', default= 'F', verbose_name= 'Send Status', choices = SEND_CHOICES, max_length = 1)

    def followup(self):
        r = random.randint(10000,99999) 
        return '{}{}'.format(r, self.id)

    def __str__(self):
        return "{0} - {1}".format(self.user.username, self.date)

    class Meta:
        verbose_name_plural = "Salled"


class contact_us(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    desc = models.TextField()

    def __str__(self):
        return "{0}, {1}".format(self.name, self.email)

    class Meta:
        verbose_name_plural = "Contact us Table"