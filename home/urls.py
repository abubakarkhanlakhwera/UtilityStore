from django.urls import path
from . import views
from authapp import views as v1

urlpatterns = [
    path('', v1.home_redirect, name='home_redirect'),  # Redirects to the appropriate view
    path('home/', v1.home, name='home'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('items/<str:store_type>/', views.items_by_store_type, name="items_by_store_type"), 
    path('item/detail/<int:item_id>/', views.item_detail, name='item_detail'),  
    path('item/price/<int:item_id>/', views.item_price, name='item_price'),
    
    # For deleting Store  
    path('store/<int:store_id>/delete/', views.delete_store, name="delete_store"),
    path('stores/', views.store_list, name="store_list"),
    
    # For editing Store
    path('store/<int:store_id>/edit/', views.edit_store, name="edit_store"),
    
    # For editing Item
    path('item/<int:item_id>/edit/', views.edit_item, name="edit_item"),  # Add this line
    
    # For deleting Item
    path('item/<int:item_id>/delete/', views.delete_item, name="delete_item"),  # Add this line
    #for hidding store
    path('hide_store/<int:store_id>/', views.hide_store, name='hide_store'),
    # For searching items
    path('search/', views.search_items, name='search_items'), 
]
