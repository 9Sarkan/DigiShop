from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email

from .models import MyUsers
from .models import States

class RegisterForm(forms.Form):
    username = forms.CharField(max_length= 30, min_length= 4, label= 'نام کاربری', widget=forms.TextInput(attrs={'class':"form-control", 'id':"input-username", 'placeholder': "نام کاربری", }))
    first_name = forms.CharField(max_length= 30, min_length= 3, label= 'نام', widget=forms.TextInput(attrs={'class':"form-control", 'id':"input-firstname", 'placeholder':"نام", }))
    last_name = forms.CharField(max_length= 50, min_length= 3, label= 'نام خانوادگی', widget=forms.TextInput(attrs={'class':"form-control", 'id':"input-lastname", 'placeholder':"نام خانوادگی"}))
    email = forms.EmailField(label= 'ایمیل', widget=forms.TextInput(attrs={'class':"form-control", 'id':"input-email", 'placeholder':"آدرس ایمیل"}))
    password= forms.CharField(max_length= 50, label= 'رمز عبور', min_length= 6, widget=forms.TextInput(attrs={'type':"password", 'class':"form-control", 'id':"input-password", 'placeholder':"رمز عبور"}))
    Confirm = forms.CharField(max_length= 50, label= 'تایید رمز عبور', min_length= 6, widget=forms.TextInput(attrs={'type':"password", 'class':"form-control", 'id':"input-password", 'placeholder':"تایید رمز عبور"}))
    phone = forms.CharField(max_length= 15, label = 'شماره موبایل', min_length= 11, widget=forms.TextInput(attrs={'class' : 'form-control', 'id' : 'input-phone', 'placeholder' : 'شماره موبایل'}))

    def clean_username(self):
        data = self.cleaned_data['username']
        u = User.objects.filter(username = data)
        if len(u) != 0:
            raise ValidationError(_('نام کاربری تکراری میباشد لطفا یک نام دیگر را انتخاب کنید.'))
        else:
            return data

    def clean_Confirm(self):
        data1 = self.cleaned_data['password']
        data2 = self.cleaned_data['Confirm']
        if data1 != data2:
            raise ValidationError(_('لطفا پسورد را چک کنید'))
        else:
            return data1

    def clean_email(self):
        data = self.cleaned_data['email']
        validate_email(data)
        return data
    
    def clean_phone(self):
        data = self.cleaned_data['phone']
        if not data.isdigit():
            raise ValidationError(_('شماره موبایل باید فقط شامل اعداد باشد.'))
        elif '+' in data:
            raise ValidationError(_("لطفا به جای علامت '+' از 00 استفاده کنید."))
        return data

    class Meta:
        model = MyUsers


class ProfileForm(forms.Form):
    KHABAR_CHOISES = {
        ('TRUE', 'مشترک خبرنامه'),
        ('FALSE', 'عدم اشتراک در خبرنامه'),
    }
    def CHOICES():
        s = States.objects.all()
        lst = []
        for i in s:
            lst.append((i.id, i.name))
        return tuple(lst)
    first_name = forms.CharField(max_length= 50, label= 'نام', widget=forms.TextInput(attrs={'type':"text", 'class':"form-control", 'id':"input-firstname", 'placeholder':"نام"}))
    last_name = forms.CharField(max_length= 50, label= 'نام خانوادگی', widget=forms.TextInput(attrs={'type':"text", 'class':"form-control", 'id':"input-lastname", 'placeholder':"نام خانوادگی"}))
    state = forms.ChoiceField(required = False, label = 'استان',choices=CHOICES(), widget=forms.Select(attrs={'class':"form-control", 'id':"input-state", }))
    city = forms.CharField(required = False, max_length=100, label = 'شهر', min_length=5, widget=forms.TextInput(attrs = {'type':"text", 'class':"form-control", 'id':"input-ciry", 'placeholder':"شهر",}))
    address = forms.CharField(required = False, max_length= 500, label = 'آدرس', widget= forms.TextInput(attrs={'type':"text", 'class':"form-control", 'id':"input-address", 'placeholder':"آدرس",}))
    postcode = forms.CharField(required = False, max_length= 10, label = 'کد پستی', widget= forms.TextInput(attrs={'type':"text", 'class':"form-control", 'id':"input-postcode", 'placeholder':"کد پستی",}))
    password= forms.CharField(required = False, max_length= 50, label= 'رمز عبور', min_length= 6, widget=forms.TextInput(attrs={'type':"password", 'class':"form-control", 'id':"input-password", 'placeholder':"رمز عبور"}))
    Confirm = forms.CharField(required = False, max_length= 50, label= 'تایید رمز عبور', min_length= 6, widget=forms.TextInput(attrs={'type':"password", 'class':"form-control", 'id':"input-password", 'placeholder':"تایید رمز عبور"}))
    phone = forms.CharField(max_length= 15, label = 'شماره موبایل', min_length= 11, widget=forms.TextInput(attrs={'class' : 'form-control', 'id' : 'input-phone', 'placeholder' : 'شماره موبایل'}))
    KhabarName = forms.ChoiceField(label = 'خبرنامه',choices= KHABAR_CHOISES, widget= forms.Select(attrs={'class':"form-control", 'id':"input-khabarname",}))

    def clean_postcode(self):
        data = self.cleaned_data['postcode']
        if not data.isdigit():
            raise ValidationError(_('کد پستی فقط شامل اعداد است.'))
        elif len(data) != 10:
            raise ValidationError(_('کد پستی باید 10 رقم باشد.'))
        return data

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if not data.isdigit():
            raise ValidationError(_('شماره موبایل باید فقط شامل اعداد باشد.'))
        elif '+' in data:
            raise ValidationError(_("لطفا به جای علامت '+' از 00 استفاده کنید."))
        return data

    def clean_Confirm(self):
        data1 = self.cleaned_data['password']
        data2 = self.cleaned_data['Confirm']
        if data1 != data2:
            raise ValidationError(_('لطفا پسورد را چک کنید'))
        else:
            return data1

    class Meta:
        model = MyUsers


class checkoutForm(forms.Form):
    def CHOICES():
        s = States.objects.all()
        lst = []
        for i in s:
            lst.append((i.id, i.name))
        return tuple(lst)
    company = forms.CharField(required= False, max_length= 200, label= 'شرکت', widget= forms.TextInput(attrs={'class':"form-control", 'id':"input-payment-company", 'placeholder':"شرکت", 'name':"company"}))
    address = forms.CharField(max_length= 500, label= 'آدرس', widget= forms.TextInput(attrs={'class':"form-control", 'id':"input-address", 'placeholder':"آدرس", 'name':"address"}))
    postcode = forms.CharField(max_length= 10, label= 'کد پستی', widget= forms.TextInput(attrs={'class':"form-control", 'id':"input-post-code", 'placeholder':"کد پستی", 'name':"postcode"}))
    city = forms.CharField(max_length= 50, label= 'شهر', widget= forms.TextInput(attrs={'class':"form-control", 'id':"input-city", 'placeholder':"شهر", 'name':"city"}))
    state = forms.ChoiceField(label = 'استان',choices=CHOICES(), widget=forms.Select(attrs={'class':"form-control", 'id':"input-state", 'placeholder':"استان", 'name':'state'}))
    desc = forms.CharField(required = False, label= 'توضیحات', widget= forms.Textarea(attrs={'rows':"4", 'class':"form-control", 'id':"confirm_comment", 'name':"desc"}))

    def clean_postcode(self):
        data = self.cleaned_data['postcode']
        if not data.isdigit():
            raise ValidationError(_('کد پستی فقط شامل اعداد است.'))
        elif len(data) != 10:
            raise ValidationError(_('کد پستی باید 10 رقم باشد.'))
        return data

class PriceFilter(forms.Form):
    minPrice = forms.IntegerField(required = False, label = 'از', widget= forms.TextInput(attrs={'type' : 'number', 'value' : '0'}))
    maxPrice = forms.IntegerField(required = False, label = 'تا', widget= forms.TextInput(attrs={'type' : 'number', 'value' : '0'}))

    def clean_minProce(self):
        data = self.cleaned_data['minPrice']
        dataMax = self.cleaned_data['maxPrice']
        if data > dataMax:
            raise ValidationError(_("مقدار نادرست است لطفا چک کنید!"))
        return data

    def clean_minProce(self):
        dataMin = self.cleaned_data['minPrice']
        data = self.cleaned_data['maxPrice']
        if data < dataMin:
            raise ValidationError(_("مقدار نادرست است لطفا چک کنید!"))
        return data
    