from django.urls import path

from product.views import (
	prod_TCB_create,
    prod_TCB_CRUD,
    edit_tcb_product,
    product_delete,
    
    customer_list,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerListView,
    CustomerDeleteView,
    
    SalesView,
    SelectCustomerView,
    SalesCreateView,
    
	)
  
 
app_name = 'product'

urlpatterns = [    
    path('prod-tcb-create/', prod_TCB_create, name='prod-tcb-create'),
    path('prod-tcb-crud/', prod_TCB_CRUD, name='prod-tcb-crud'),
    path('edit-tcb-product/<str:product_id>/', edit_tcb_product, name='edit-tcb-product'),
    path('delete/<str:product_id>/', product_delete, name='product-delete'),
    
    path('customer1/', customer_list, name='customer1'),
    path('customer/new', CustomerCreateView.as_view(), name='new-customer'),   
    path('customers/<pk>/edit', CustomerUpdateView.as_view(), name='edit-customer'),
    path('customers/', CustomerListView.as_view(), name='customers-list'),
    path('customer/<pk>/delete', CustomerDeleteView.as_view(), name='delete-customer'),

    path('sales/', SalesView.as_view(), name='sales-list'), 
    path('sales/new', SelectCustomerView.as_view(), name='select-customer'), 
    path('sales/new/<pk>', SalesCreateView.as_view(), name='new-sales'),
    #path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    
]