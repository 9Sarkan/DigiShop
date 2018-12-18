from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.KalaListView.as_view(), name = 'index'),
    path('kala/<slug:kalaslug>/', views.KalaDetailView, name = 'KalaDetailView'),
    path('category/<slug:catslug>/', views.CategoryListView.as_view(), name = 'CategoryListView'),
    path('category/<slug:catslug>/instock/', views.CategoryListViewInstock.as_view(), name = 'CategoryInstock'),
    path('category/<slug:catslug>/instock/<int:minPrice>/<int:maxPrice>/', views.CategoryPriceFilterListView.as_view(), name = 'CategoryPriceFilter'),
    path('brands/<slug:brandslug>/', views.BrandListView.as_view(), name = 'BrandListView'),
    path('brands/<slug:brandslug>/instock/', views.BrandListViewInstock.as_view(), name = 'BrandListViewInstock'),
    path('brands/<slug:brandslug>/instock/<int:minPrice>/<int:maxPrice>/', views.BrandPriceFilter.as_view(), name = 'BrandPriceFilter'),
    path('category/<slug:catslug>/<slug:brandslug>/', views.BrandCategory.as_view(), name= 'BrandCategory'),
    path('category/<slug:catslug>/<slug:brandslug>/instock/', views.BrandCategoryInstock.as_view(), name= 'BrandCategoryInstock'),
    path('category/<slug:catslug>/<slug:brandslug>/instock/<int:minPrice>/<int:maxPrice>/', views.BrandCategoryPriceFilter.as_view(), name= 'BrandCategoryPriceFilter'),
    path('login', views.user_login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('logout', views.user_logout, name = 'logout'),
    path('cart', views.cart_view, name = 'cart'),
    path('about-us', views.about_us, name='about'),
    path('contact-us', views.contact_us, name="contact_us"),
    path('checkout', views.checkout, name = 'checkout'),
    path('profile', views.profile, name = 'profile'),
    path('brands', views.brands, name='brands'),
    path('checkout/done', views.done, name = 'done'),
    path('private', views.private, name = 'private'),
    path('rules', views.rules, name = 'rules'),
    path('search', views.search.as_view(), name = 'search'),
]

handler404 = views.error_404
handler500 = views.error_500