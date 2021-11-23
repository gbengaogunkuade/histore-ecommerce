from django.urls import path
from product import views



app_name = 'product'


urlpatterns = [
    path('', views.home, name='home'),
    path('savedproducts/', views.savedproducts, name='savedproducts'),
    path('contact/', views.contact, name='contact'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('empty_order_summary/', views.empty_order_summary, name='empty_order_summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('sell_product/', views.sell_product, name='sell_product'),
    path('payment/cash/', views.payment_cash, name='payment_cash'),
    path('payment/success/', views.success, name='success'),
    path('payment/cancel/', views.cancel, name='cancel'),
    path('purchased/', views.purchased, name='purchased'),
    path('search/', views.search, name='search'),
    path('search_result/', views.search_result, name='search_result'),
    path('multi_search/', views.multi_search, name='multi_search'),  # new addition (multi_search feature)
    path('computer_electronics/', views.computer_electronics, name='computer_electronics'),
    path('phones_tablets/', views.phones_tablets, name='phones_tablets'),
    path('fashions_styles/', views.fashions_styles, name='fashions_styles'),
    path('home_kitchen/', views.home_kitchen, name='home_kitchen'),
    path('drinks_wine/', views.drinks_wine, name='drinks_wine'),
    path('kids_toys/', views.kids_toys, name='kids_toys'),
    path('others/', views.others, name='others'),


    path('<slug>/', views.detail, name='detail'),
    path('<slug>/update_product/', views.update_product, name='update_product'),
    path('<slug>/delete_product/', views.delete_product, name='delete_product'),

    path('<slug>/save_this_product_from_detail/', views.save_this_product_from_detail, name='save_this_product_from_detail'),
    path('<slug>/save_this_product_from_order_summary/', views.save_this_product_from_order_summary, name='save_this_product_from_order_summary'),

    path('<slug>/unsave_this_product_from_detail/', views.unsave_this_product_from_detail, name='unsave_this_product_from_detail'),
    path('<slug>/unsave_this_product_from_order_summary/', views.unsave_this_product_from_order_summary, name='unsave_this_product_from_order_summary'),
    path('<slug>/unsave_this_product_from_savedproducts/', views.unsave_this_product_from_savedproducts, name='unsave_this_product_from_savedproducts'),

    # path('add_single_item_to_cart/<slug>/', views.add_single_item_to_cart, name='add_single_item_to_cart'),
    path('<slug>/add_single_item_to_cart/', views.add_single_item_to_cart, name='add_single_item_to_cart'),
    # path('remove_single_item_from_cart/<slug>/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('<slug>/remove_single_item_from_cart/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    # path('remove_items_from_cart/<slug>/', views.remove_items_from_cart, name='remove_items_from_cart'),
    path('<slug>/remove_items_from_cart/', views.remove_items_from_cart, name='remove_items_from_cart'),
]