from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth import login
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from .forms import RegisterForm
from .forms import ProfileForm
from .forms import checkoutForm
from .forms import PriceFilter
from .forms import RegisterForm

from functools import reduce

from django.db.models import Count

from .models import Kala
from .models import Manufactor
from .models import Comment
from .models import KalaInst
from .models import kalaCat
from .models import cart
from .models import color as KColor
from .models import contact_us as contact
from .models import States
from .models import MyUsers
from .models import coupon
from .models import Salled
from .models import PSize

from django.template import loader
from django.db.models import Q
import operator


class KalaListView(generic.ListView):
    model = Kala
    context_object_name = 'kala'
    template_name = 'index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(KalaListView, self).get_context_data(**kwargs)
        
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kala': Kala.objects.all(),
            'OffKala' : offkala,
            'mostSalled' : mostsalled,
            'Manufactors': Manufactor.objects.all(),
            'is_authenticated' : self.request.user.is_authenticated,
        })
        return context

def KalaDetailView(request, kalaslug):
    k = get_object_or_404(Kala, slug = kalaslug)
    akala = Kala.objects.filter(cat = k.cat)
    comments = Comment.objects.filter(Kala__id = k.id)
    # inst = KalaInst.objects.filter(kala = k).filter(~Q(instock = 0))
    
    inst = []
    i = KalaInst.objects.filter(kala = k)
    for a in i:
        if a.instock != 0:
            inst.append(a)

    if request.user.is_authenticated:
            is_authenticated = True
    else:
            is_authenticated = False

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'addComment' in request.POST:
                text = request.POST['text']
                c = Comment.objects.create(writer = request.user, body = text, Kala = k)
                c.save()
            elif 'addCart' in request.POST:
                colorid = request.POST['Color']
                salerid = request.POST['Saller']
                sizeid = request.POST['Size']
                UsersProducts = cart.objects.filter(username = request.user, Payed = 'F')
                Found = False
                for i in UsersProducts:
                    if i.saler == KalaInst.objects.get(id = salerid) and \
                        i.size == PSize.objects.get(id = sizeid) and \
                        i.color == KColor.objects.get(id = colorid):
                        i.count += 1
                        i.save()
                        Found = True
                        break

                if not Found:    
                    addCart = cart.objects.create(username= request.user, product= k,
                                                    size = PSize.objects.get(id = sizeid),
                                                    color= KColor.objects.get(id= colorid),
                                                    saler= KalaInst.objects.get(id = salerid))
    if inst:
        context = {
            'kala' : k,
            'Allkala' : akala,
            'comments' : comments,
            'inst' : inst,
            'is_authenticated' : is_authenticated,
            'finst': inst[0],
        }
    else:
        context = {
            'kala' : k,
            'Allkala' : akala,
            'comments' : comments,
            'is_authenticated' : is_authenticated,
        }
    return render(request, 'kalaDetail.html', context)

def CategoryOrInstockSluger(catslug):
    if catslug.lower() == 'for-men':
        kalasCat = kalaCat.objects.filter(gen = 'm')
        kalas = Kala.objects.filter(cat__in = kalasCat)
        cate = kalaCat.objects.get(id = 20)
    elif catslug.lower() == 'for-woman':
        kalasCat = kalaCat.objects.filter(gen = 'f')
        kalas = Kala.objects.filter(cat__in = kalasCat)
        cate = kalaCat.objects.get(id = 21)
    elif catslug.lower() == 'special-for-sports':
        kalasCat = kalaCat.objects.filter(gen = 's')
        kalas = Kala.objects.filter(cat__in = kalasCat)
        cate = kalaCat.objects.get(id = 22)
    else:
        kalasCat = get_object_or_404(kalaCat, slug = catslug)
        kalas = kalasCat.category.all()
        cate = kalasCat

    return kalas, cate

def JustInstock(kalas):
    lstKalas = []
    for i in kalas:
        if i.kalainst.filter(~Q(instock = 0)):
            lstKalas.append(i)
    return lstKalas

def MaxMinPrice(kalas, minPrice, maxPrice):
    lstKalas = []
    for i in kalas:
        if i.kalainst.filter(~Q(instock = 0)):
            if i.kalainst.filter(price__lte = maxPrice):
                if len(i.kalainst.filter(price__gt = minPrice)):
                    lstKalas.append(i)
    return lstKalas

class CategoryListView(generic.ListView):
    model = Kala
    context_object_name = 'kalas'
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('CategoryPriceFilter', kwargs={'catslug' : self.kwargs['catslug'],'minPrice' : minPrice, 'maxPrice' : maxPrice}))
        return HttpResponseRedirect(reverse('CategoryListViewInstock', kwargs={'catslug' : self.kwargs['catslug']}))
     
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        catslug = self.kwargs['catslug']
        lst = CategoryOrInstockSluger(catslug)
        form = PriceFilter()
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : lst[0],
            'OffKala' : offkala,
            'cate' : lst[1],
            'brands' : Manufactor.objects.all(),
            'mostsalled' : mostsalled,
            'form' : form,
            'is_authenticated' : self.request.user.is_authenticated,
        })
        return context


class CategoryListViewInstock(CategoryListView):
    model = Kala
    context_object_name = 'kalas'
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('CategoryPriceFilter', kwargs={'catslug' : self.kwargs['catslug'],'minPrice' : minPrice, 'maxPrice' : maxPrice}))
        return HttpResponseRedirect(reverse('CategoryListViewInstock', kwargs={'catslug' : self.kwargs['catslug']}))
        
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        catslug = self.kwargs['catslug']
        lst = CategoryOrInstockSluger(catslug)
        form = PriceFilter()
        kalas = JustInstock(lst[0])
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : kalas,
            'OffKala' : offkala,
            'cate' : lst[1],
            'brands' : Manufactor.objects.all(),
            'mostsalled' : mostsalled,
            'is_authenticated' : self.request.user.is_authenticated,
            'form' : form,
        }) 
        return context


class CategoryPriceFilterListView(generic.ListView):
    model = Kala
    context_object_name = 'kalas'
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('CategoryPriceFilter', kwargs={'catslug' : self.kwargs['catslug'],'minPrice' : minPrice, 'maxPrice' : maxPrice}))
        return HttpResponseRedirect(reverse('CategoryListViewInstock', kwargs={'catslug' : self.kwargs['catslug']}))
  
    def get_context_data(self, **kwargs):
        context = super(CategoryPriceFilterListView, self).get_context_data(**kwargs)
        minPrice = int(self.kwargs['minPrice'])
        maxPrice = int(self.kwargs['maxPrice'])
        lst = CategoryOrInstockSluger(self.kwargs['catslug'])
        kalas = MaxMinPrice(lst[0], minPrice, maxPrice)
        form = PriceFilter()
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : kalas,
            'OffKala' : offkala,
            'cate' : lst[1],
            'brands' : Manufactor.objects.all(),
            'mostsalled' : mostsalled,
            'is_authenticated' : self.request.user.is_authenticated,
            'form' : form,
        })
        return context
    

class BrandListView(generic.ListView):
    model = Kala
    context_object_name = 'kalas'
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('BrandPriceFilter', kwargs={'brandslug' : self.kwargs['brandslug'],'minPrice' : minPrice, 'maxPrice' : maxPrice}))
         
    def get_context_data(self, **kwargs):
        context = super(BrandListView, self).get_context_data(**kwargs)
        maker = get_object_or_404(Manufactor, slug = self.kwargs["brandslug"])
        products = maker.manufactor.all()
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : products,
            'OffKala' : offkala,
            'brand': maker,
            'mostsalled' : mostsalled,
            'brands' : Manufactor.objects.all(),
            'is_authenticated' : self.request.user.is_authenticated,
            'form' : PriceFilter(),
        })
        return context

class BrandListViewInstock(generic.ListView):
    model = Kala
    context_object_name = 'kalas'
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('BrandPriceFilter', kwargs={'brandslug' : self.kwargs['brandslug'],'minPrice' : minPrice, 'maxPrice' : maxPrice}))
        
    def get_context_data(self, **kwargs):
        context = super(BrandListViewInstock, self).get_context_data(**kwargs)
        maker = get_object_or_404(Manufactor, slug = self.kwargs["brandslug"])
        products = JustInstock(maker.manufactor.all())
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : products,
            'OffKala' : offkala,
            'brand': maker,
            'mostsalled' : mostsalled,
            'brands' : Manufactor.objects.all(),
            'is_authenticated' : self.request.user.is_authenticated,
            'form' : PriceFilter(),
        })
        return context

class BrandPriceFilter(generic.ListView):
    model = Kala
    context_object_name = 'kalas'
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('BrandPriceFilter', kwargs={'brandslug' : self.kwargs['brandslug'],'minPrice' : minPrice, 'maxPrice' : maxPrice}))
     
    def get_context_data(self, **kwargs):
        context = super(BrandPriceFilter, self).get_context_data(**kwargs)
        maker = get_object_or_404(Manufactor, slug = self.kwargs["brandslug"])
        products = MaxMinPrice(maker.manufactor.all(), self.kwargs['minPrice'], self.kwargs['maxPrice'])
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : products,
            'OffKala' : offkala,
            'brand': maker,
            'mostsalled' : mostsalled,
            'brands' : Manufactor.objects.all(),
            'is_authenticated' : self.request.user.is_authenticated,
            'form' : PriceFilter(),
        })
        return context


def BrandCategorySluger(catslug, manu):
    if catslug.lower() == 'for-men':
        kalasCat = kalaCat.objects.filter(gen = 'm')
        kalas = manu.manufactor.filter(cat__in = kalasCat)
        cate = kalaCat.objects.get(id = 20)
    elif catslug.lower() == 'for-woman':
        kalasCat = kalaCat.objects.filter(gen = 'f')
        kalas = manu.manufactor.filter(cat__in = kalasCat)
        cate = kalaCat.objects.get(id = 21)
    elif catslug.lower() == 'special-for-sports':
        kalasCat = kalaCat.objects.filter(gen = 's')
        kalas = manu.manufactor.filter(cat__in = kalasCat)
        cate = kalaCat.objects.get(id = 22)
    else:
        kalasCat = get_object_or_404(kalaCat, slug = catslug)
        kalas = manu.manufactor.filter(cat = kalasCat)
        cate = kalasCat

    return kalas, cate

class BrandCategory(generic.ListView):
    model = Kala
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('BrandCategoryPriceFilter', kwargs={'catslug' : self.kwargs['catslug'],'brandslug' : self.kwargs['brandslug'],'minPrice' : minPrice, 'maxPrice' : maxPrice}))
    
    def get_context_data(self, **kwargs):
        context = super(BrandCategory, self).get_context_data(**kwargs)
        brand = self.kwargs['brandslug']
        catslug = self.kwargs['catslug']
        manu = get_object_or_404(Manufactor, slug = brand)
        lst = BrandCategorySluger(catslug, manu)
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : lst[0],
            'OffKala' : offkala,
            'cate' : lst[1],
            'mostsalled' : mostsalled,
            'brand': manu,
            'brands' : Manufactor.objects.all(),
            'is_authenticated' : self.request.user.is_authenticated,
            'form' : PriceFilter(),
        })
        return context

class BrandCategoryInstock(generic.ListView):
    model = Kala
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('BrandCategoryPriceFilter', kwargs={'catslug' : self.kwargs['catslug'],'brandslug' : self.kwargs['brandslug'],'minPrice' : minPrice, 'maxPrice' : maxPrice}))
    
    def get_context_data(self, **kwargs):
        context = super(BrandCategoryInstock, self).get_context_data(**kwargs)
        brand = self.kwargs['brandslug']
        catslug = self.kwargs['catslug']
        manu = get_object_or_404(Manufactor, slug = brand)
        lst = BrandCategorySluger(catslug, manu)
        kalas = JustInstock(lst[0])
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : kalas,
            'OffKala' : offkala,
            'cate' : lst[1],
            'mostsalled' : mostsalled,
            'brand': manu,
            'brands' : Manufactor.objects.all(),
            'is_authenticated' : self.request.user.is_authenticated,
            'form' : PriceFilter(),
        })
        return context

class BrandCategoryPriceFilter(generic.ListView):
    model = Kala
    template_name = 'Category.html'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        form = PriceFilter(request.POST)
        if form.is_valid():
            minPrice = form.cleaned_data['minPrice']
            maxPrice = form.cleaned_data['maxPrice']
            return HttpResponseRedirect(reverse('BrandCategoryPriceFilter', kwargs={'catslug' : self.kwargs['catslug'], 'brandslug' : self.kwargs['brandslug'], 'minPrice' : minPrice, 'maxPrice' : maxPrice}))

    def get_context_data(self, **kwargs):
        context = super(BrandCategoryPriceFilter, self).get_context_data(**kwargs)
        brand = self.kwargs['brandslug']
        catslug = self.kwargs['catslug']
        maxPrice = self.kwargs['maxPrice']
        minPrice = self.kwargs['minPrice']
        manu = get_object_or_404(Manufactor, slug = brand)
        lst = BrandCategorySluger(catslug, manu)
        kalas = MaxMinPrice(lst[0], minPrice, maxPrice)
        offkala = KalaInst.objects.filter(~Q(off= 0))
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'kalas' : kalas,
            'OffKala' : offkala,
            'cate' : lst[1],
            'mostsalled' : mostsalled,
            'brand': manu,
            'brands' : Manufactor.objects.all(),
            'is_authenticated' : self.request.user.is_authenticated,
            'form' : PriceFilter(),
        })
        return context

def is_authenticated(user):
    return not user.is_authenticated

@user_passes_test(is_authenticated)
def user_login(request):
    error = None
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username = email, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                error = 'این اکانت غیرفعال میباشد لطفا با تیم ساپورت تماس برقرار کنید'
                context = {
                    'error' : error,
                    'is_authenticated' : False, 
                }
                return render(request, 'login.html', context)
        else:
            error = 'ایمیل یا پسورد اشتباه می باشد لطفا دوباره سعی نمایید'
            context = {
                'error' : error,
                'is_authenticated' : False, 
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html')

@user_passes_test(is_authenticated)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['Confirm']
            phone = form.cleaned_data['phone']
            u = User.objects.create_user(username, email, password)
            u.last_name = last_name
            u.first_name = first_name
            u.save()
            myu = MyUsers.objects.create(user = User.objects.get(username = username), phone = phone)
            myu.save()
            user = authenticate(username= username, password= password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisterForm()    
    return render(request, 'register.html', { 'is_authenticated' : False, 'form' : form, })

@login_required(redirect_field_name = "")
def user_logout(requset):
    logout(requset)
    return HttpResponseRedirect(reverse('index'))

@login_required(redirect_field_name = '')
def cart_view(request):
    objs = cart.objects.filter(username = request.user, Payed = 'F')
    if request.method == 'POST':
        if 'update' in request.POST:
            slug = request.POST.get('product_slug')
            count = request.POST.get('quantity')
            product_obj = Kala.objects.get(slug = slug)
            for obj in objs:
                if obj.product == product_obj:
                    obj.count = int(count)
                    obj.save()
                    break
        if 'delete' in request.POST:
            slug = request.POST.get('product_slug')
            count = request.POST.get('quantity')
            product_obj = Kala.objects.get(slug = slug)
            for obj in objs:
                if obj.product == product_obj:
                    print('-----   Found : True   -----')
                    obj.delete()
                    break
        if 'applyCoupon' in request.POST:
            code = request.POST.get('couponCode')
            error = None
            try:
                co = coupon.objects.get(code = code)
                if co.is_expire():
                    error = 'تاریخ استفاده از این کوپن به پایان رسیده است!'
                elif not co.count > 0:
                    error = 'تعداد استفاده از این کوپن به پایان رسیده است!'
                else:
                    for obj in objs:
                        obj.coupon = co
                        obj.save()
                    return HttpResponseRedirect(reverse('checkout'))
            except coupon.DoesNotExist:
                error = 'کد کوپن نادرست می باشد!'
            
            if error != None:
                context = {
                    'carts' : objs,
                    'is_authenticated' : True,
                    'error' : error,
                }
            return render(request, 'cart.html', context)
    
    context = {
        'carts' : objs,
        'is_authenticated' : True,
    }
    return render(request, 'cart.html', context)


def error_404(request):
    return render(request, '404.html')

def error_500(request):
    return render(request, '500.html')

def about_us(request):
    return render(request, 'about-us.html')

def contact_us(request):
    context = {}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        description = request.POST['description']
        call = contact.objects.create(name = name, email = email, desc = description)
        call.save()
        context = {
            'sent' : True,
        }
    return render(request, 'contact-us.html', context)

@login_required(redirect_field_name = "")
def checkout(request):
    usr = MyUsers.objects.get(user = request.user)
    carts = cart.objects.filter(username = request.user, Payed = 'F')
    tPrice = 0
    for i in carts:
        tPrice += i.total()
    final = 0
    for i in carts:
        final += i.totalPrice()
    CFinal = 0
    for i in carts:
        CFinal += i.finallyPrice()
    gift = tPrice - final
    tax = tPrice * 0.09
    coupon = final - CFinal
    sendCost = 5000 * len(carts)
    toPay = CFinal + tax + sendCost

    if request.method == 'POST':
        form = checkoutForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            postcode = form.cleaned_data['postcode']
            state = form.cleaned_data['state'] 
            description = form.cleaned_data['desc']  
            sell = Salled.objects.create(user= request.user, company= company,
                                        address = address, zip_code= postcode,
                                        state= States.objects.get(id = state),
                                        city= city, total_price= CFinal, send_price= sendCost, tax= tax,
                                        total= toPay, desc= description)
                
            for c in carts:
                sell.products.add(c)
                instance = c.saler
                instance.instock -= 1
                instance.save()
                c.Payed = 'T'
                c.save()

            sell.save()
            return HttpResponseRedirect(reverse('done'))
    else:
        form = checkoutForm(initial={'address' : usr.address, 'city' : usr.city, 'state' : usr.state, 'postcode' : usr.postcode})

    context = {
        'form' : form,
        'state' : States.objects.all(),
        'not_authenticated' : False,
        'carts' : carts,
        'totalPrice': tPrice,
        'finalPrice' : final,
        'gift' : gift,
        'tax' : tax,
        'coupon': coupon,
        'sendCost' : sendCost,
        'toPay': toPay,
        'is_authenticated' : True,
        'usr' : usr,
    }
    return render(request, 'checkout.html', context)


@login_required(redirect_field_name = "",login_url = 'login')
def profile(request):
    usr = MyUsers.objects.get(user = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            usr.phone = form.cleaned_data['phone']
            usr.state = States.objects.get(id = form.cleaned_data['state'])
            usr.city = form.cleaned_data['city']
            usr.address = form.cleaned_data['address']
            usr.postcode = form.cleaned_data['postcode']
            usr.KhabarName = form.cleaned_data['KhabarName']
            usr.save()
            u = User.objects.get(username= request.user.username)
            passfield = form.cleaned_data["Confirm"]
            if passfield != "":
                u.set_password(form.cleaned_data["Confirm"])
            u.last_name = form.cleaned_data['last_name']
            u.first_name = form.cleaned_data['first_name']
            u.save()
            user = authenticate(username= u.username, password= u.password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ProfileForm(initial={'first_name' : usr.user.first_name, 'last_name' : usr.user.last_name, 'state' : usr.state, 'city':usr.city, 'address':usr.address, 'phone': usr.phone, 'KhabarName': usr.KhabarName})

    context = {
        'is_authenticated' : True,
        'usr' : usr,
        'form' : form,
    }
    return render(request, 'profile.html', context)

def brands(request):
    context = {
        'brands' : Manufactor.objects.all(),
        'is_authenticated' : request.user.is_authenticated,
    }
    return render(request, 'brands.html', context)

    
@login_required(redirect_field_name = "")
def done(request):
    s = Salled.objects.filter(user = request.user)
    context = {
        'is_authenticated' : True,
        'sall' : s,
    }
    return render(request, 'done.html', context)

def private(request):
    context = {
        'is_authenticated' : request.user.is_authenticated,
    }
    return render(request, 'private.html', context)

def rules(request):
    context = {
        'is_authenticated' : request.user.is_authenticated,
    }
    return render(request, 'rules.html', context)

class search(KalaListView):
    """
        Display a Product List filtered by search query
    """
    paginate_by = 20
    template_name = 'search.html'
    context_object_name = 'kalas'

    def get_queryset(self):
        result = super(search, self).get_queryset()

        query = self.request.GET.get('search')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                (Q(name__icontains = q) for q in query_list))
            )
        return result

    def get_context_data(self, **kwargs):
        context = super(search, self).get_context_data(**kwargs)
        mostsalled = cart.objects.annotate(num_kalas = Count('saler')).order_by('-num_kalas')[:5]
        context.update({
            'is_authenticated' : self.request.user.is_authenticated,
            'OffKala' : KalaInst.objects.filter(~Q(off= 0)),
            'mostsalled' : mostsalled,
        })
        return context
    
    # def reduce(func, items):
    #     result = items.pop()
    #     for item in items:
    #         result = func(result, item)
    #     return result

    # def and_(a, b):
    #     return a and b