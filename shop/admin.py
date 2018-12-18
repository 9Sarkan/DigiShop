from django.contrib import admin
from .models import *
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime

def export_as_json(ModelAdmin, request, queryset):
    response = HttpResponse(content_type = 'Application/json')
    serializers.serialize('json', queryset, stream = response)
    return response

def make_instock_zero(ModelAdmin, request, queryset):
    result = queryset.update(instock = 0)
    if result == 1:
        m = 'a product'
    else:
        m = '{} products'.format(result)
    ModelAdmin.message_user(request, '{0} in stock status changed to 0'.format(m))

def make_sent(ModelAdmin, request, queryset):
    result = queryset.update(sent= True)
    if result == 1:
        m = 'a product'
    else:
        m = '{} products'.format(result)
    ModelAdmin.message_user(request, '{0} sent.'.format(m))

def make_expire(ModelAdmin, request, queryset):
    result = queryset.update(expire= datetime.now())
    if result == 1:
        m = 'a coupen'
    else:
        m = '{} coupens'.format(result) 
    ModelAdmin.message_user(request, '{} Expired!.'.format(m))
    

export_as_json.short_description = 'export selected objects as json'.title()
make_instock_zero.short_description = 'Make selected kalas in stock zero'.title()
make_sent.short_description = 'Make selected products sent'.title()
make_expire.short_description = 'Make selected coupens expired'.title()

class KalaInstInline(admin.TabularInline):
    model = KalaInst

admin.site.register(Kala)
class KalaAdmin(admin.ModelAdmin):
    list_display = ['slug' ,'name','id', 'manu',]
    search_fields = ('name', 'manu',)
    list_filter = ('manu',)
    ordering = ('name', )
    # prepopulated_fields = {'slug' : ('name', 'manu',)}
    actions = [export_as_json, make_instock_zero]
    inlines = [KalaInstInline]
    fieldsets = (
        (None, {
            "fields": (
                'slug', 'name', 'manu','cat'
            ),
        }),
        ('Detail', {
            "fields" :(
                'size', 'color', 'desc'
            ),
        }),
        ('Pictures', {
            'fields': (
               'pic0',   'pic1',   'pic2',   'pic3',
            ),
        }),
    )
    

@admin.register(kalaCat)
class KalaCatAdmin(admin.ModelAdmin):
    list_display = ['slug' ,'name', 'gen','id']
    search_fields = ('name', )
    prepopulated_fields = {'slug' : ('name', 'gen',)}
    fieldsets = (
        (None, {
            "fields": (
                'slug',
            ),
        }),
        ('Detail', {
            "fields": (
                'name', 'gen'
            ),
        }),
    )
    
    actions = [export_as_json, ]

@admin.register(Manufactor)
class ManufactorAdmin(admin.ModelAdmin):
    list_display = ['slug','name', 'id']
    search_fields = ('name','slug', )
    prepopulated_fields = {'slug' : ('name',)}
    actions = [export_as_json, ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['writer', 'status', 'date', 'Kala',]
    search_fields = ('writer', 'Kala')
    list_filter = ('status',)

@admin.register(color)
class colorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']

@admin.register(KalaInst)
class KalaInstAdmin(admin.ModelAdmin):
    list_display = ['saler', 'price', 'instock', 'id',]
    search_fields = ('saler','kala',)

@admin.register(MyUsers)
class MyUsersAdmin(admin.ModelAdmin):
    search_fields = ('address',)

@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]

@admin.register(cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['username', 'product', 'Payed',]
    search_fields = ('username','product')
    list_filter = ('username', 'Payed', )

@admin.register(contact_us)
class Contact(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ('name', 'email', )
    actions = [export_as_json,]

@admin.register(coupon)
class Coupon(admin.ModelAdmin):
    list_display = ['code', 'off','count', 'expire',]
    search_fields = ('code', 'expire', )
    actions = [make_expire, ]

@admin.register(Salled)
class Salled(admin.ModelAdmin):
    list_display = ['user','display_products', 'state', 'city', 'total', 'date', 'sent',]
    search_fields = ('user', 'state', 'city', 'FollowUpCode',)
    list_filter = ['state', 'city', 'sent', 'user', ]
    actions = [make_sent, export_as_json,]

    def display_products(self, object):
        return ', '.join([p.product.name for p in object.products.all()])

    display_products.short_description = 'Product'

@admin.register(PSize)
class size(admin.ModelAdmin):
    list_display = ['sizeno', 'id',]