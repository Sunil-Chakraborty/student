from django.urls import path

from product.views import (
	prod_TCB_create,
    prod_TCB_CRUD,
    edit_tcb_product,
    product_delete,
    prod_stock_create,
    
    customer_list,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerListView,
    CustomerDeleteView,
    
    SalesView,
    SelectCustomerView,
    SalesCreateView,
    edit_sales_item,
    delete_sales_item,
    
    StockListView,
    edit_stock,
    stock_delete,
    
    get_stock_data_view,
    
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
    path('edit_sales_item/<str:doc_no>/', edit_sales_item, name='edit_sales_item'),
    path('delete_sales_item/<int:pk>/', delete_sales_item, name='delete-sales-item'),
    
    path('stock-create/', prod_stock_create, name='stock-create'),
    path('stock/', StockListView.as_view(), name='stock-list'),
    path('edit-stock/<str:stock_id>/', edit_stock, name='edit-stock'),
    path('delete-stock/<str:stock_id>/', stock_delete, name='stock-delete'),
 
    path('get_stock_data_view/<int:stockInstanceId>', get_stock_data_view, name='get_stock_data_view'),

]