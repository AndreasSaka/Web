from . import views
from django.views.generic.base import RedirectView
from rest_framework import routers 
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path,include

router = routers.DefaultRouter()
router.register('customer', views.CustomerView)
router.register('product', views.ProductView)
router.register('order', views.OrderView)

urlpatterns = [
     path('home/', views.home_page, name='home'),
     path('about/', views.about_page, name='about'),
     path('contact/', views.contact_page, name='contact'),
     path('user_registration/', views.customer_registration, name='user_registration'),
     path('login/', views.user_login, name='user_login'),
     path('logout/', views.user_logout, name='user_logout'),
     path('profile/', views.user_profile, name='profile'),
     path('monitor/', views.monitor, name='monitor'),
     path('mouse/', views.mouse, name='mouse'),
     path('keyboard/', views.keyboard, name='keyboard'),
     path('cart/', views.cart, name='cart'),
     path('checkout/', views.checkout, name='checkout'),
     path('update_item/', views.updateItem, name="update_item"),
     path('process_order/', views.processOrder, name="process_order"),
     re_path(r'^$', views.APIRoot.as_view()),
     path('', include(router.urls)),
     path('api-auth/', include('rest_framework.urls')),
     path('api/', views.api_view1, name='api_view'),
     path('login_api/', views.login_api, name='login_api'),
]