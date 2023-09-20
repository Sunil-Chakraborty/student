from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.db.models import Avg,Sum
from django.http import HttpResponse
from django.forms import formset_factory, inlineformset_factory, modelformset_factory

from .forms import (
    ProductTCBForm,
    ProductSCBForm,
    CustomerForm,
    SelectCustomerForm,
    SalesItemFormset,
    SalesEditFormSet,    
    StockForm,
    DocForm,
    )
from .forms import SalesItemForm,SalesEditForm
    
from account.models import Account
from . models import Product, Customer,SalesBill,SalesBillDetails,Stock,SalesItem
from student_app.templatetags.custom_filters import *
from django.db import IntegrityError
from django.views.generic import (
    View,
    ListView,
    CreateView, 
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.db import IntegrityError
from django.http import JsonResponse


def prod_TCB_create(request,*args, **kwargs):
   
    user_id = request.session['user_id']
    account = Account.objects.get(id=user_id)
    
    if request.method == 'POST':
       
        ProductTCBFormSet = formset_factory(ProductTCBForm, extra=4)
        formset = ProductTCBFormSet(request.POST)
        
        
        if formset.is_valid():
            for form in formset:
                if form.has_changed():                                        
                    matl = form.save(commit=False)
                    matl.prod_tag="01"
                                        
                    grd=str(matl.grade.id)
                    
                    if len(grd) == 1:
                        grd="0"+grd
                        
                    matl.prod_code = str(matl.prod_tag)+str(matl.fab_type)+grd+str(matl.edge)
                     
                    matl.prod_des = "TCB "+str(matl.get_fab_type_display())+str(matl.get_fab_str_display())+" "+str(matl.grade.name)+" "+str(matl.get_edge_display())
                    matl.email = account
                    
                    try:
                        matl.prod_code = str(matl.prod_tag)+str(matl.fab_type)+str(matl.fab_str)+grd+str(matl.edge)
                       
                        form.save()
                    except IntegrityError:
                        error_message =  "<b>"+matl.prod_des+"</b> already exists.<br> Please enter a unique combination."
                        return render(request, 'product/product_tcb_create.html', {'error_message': error_message})
            
            
            return redirect('product:prod-tcb-crud')
    else:
       
        ProductTCBFormSet = formset_factory(ProductTCBForm, extra=4)
        formset = ProductTCBFormSet()
        
    context = {
        'formset': formset,
                
    }
    return render(request, 'product/product_tcb_create.html', context)


def prod_TCB_CRUD(request):

    user_id = request.session['user_id']
    account = Account.objects.get(id=user_id)
    
    qs=Product.objects.all()          
        
    context={
        "queryset":qs,
        
    }
    return render(request, "product/CRUD_table_form.html", context)


def edit_tcb_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductTCBForm(request.POST, instance=product)
        if form.is_valid():
            matl = form.save(commit=False)
            grd=str(matl.grade.id)
            if len(grd) == 1:
                grd="0"+grd
                        
            matl.prod_des = "TCB "+str(matl.get_fab_type_display())+str(matl.get_fab_str_display())+" "+str(matl.grade.name)+" "+str(matl.get_edge_display())
            try:
                matl.prod_code = str(matl.prod_tag)+str(matl.fab_type)+str(matl.fab_str)+grd+str(matl.edge)
                form.save()
                return redirect('product:prod-tcb-crud')
            except IntegrityError:
                error_message =  "<b>"+matl.prod_des+"</b> already exists.<br> Please enter a unique combination."
                return render(request, 'product/edit_tcb_row.html', {'error_message': error_message})

    else:
        form = ProductTCBForm(instance=product)

    return render(request, 'product/edit_tcb_row.html', {'form': form, 'product': product})
      
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == "POST":
        product.delete()
        return redirect("product:prod-tcb-crud")
        
    context = {'product':product}
    
    return render(request, 'product/product_delete.html', context)

def customer_list(request):

    user_id = request.session['user_id']
    account = Account.objects.get(id=user_id)
    
    customers = Customer.objects.all()
    for customer in customers:
        print(customer.pk)
    # Rest of your view code
    
    qs=Customer.objects.all()          
        
    context={
        "queryset":qs,
        "customers":customers,
    }
    return render(request, "product/customer_list.html", context)

class CustomerCreateView(SuccessMessageMixin, CreateView):
    
    model = Customer
    form_class = CustomerForm
    success_url = '/product/customers/'    
    success_message = "Customer has been created successfully"
    template_name = "product/edit_customer.html"
   
    def form_valid(self, form):
        user_id = self.request.session['user_id']
        account = Account.objects.get(id=user_id)
        form.instance.fk_email = account
        return super().form_valid(form)
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Customer'
        context["savebtn"] = 'Add Customer'
        return context     

class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    success_url = '/product/customers/'
    success_message = "Customer details has been updated successfully"
    template_name = "product/edit_customer.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Customer'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Customer'
        context["customer_pk"] = self.object.pk
        return context
    
    def form_valid(self, form):
        user_id = self.request.session['user_id']
        account = Account.objects.get(id=user_id)
        form.instance.fk_email = account
        return super().form_valid(form)        
    
    
    
class CustomerListView(ListView):
    model = Customer
    template_name = "product/customer_list1.html"
    queryset = Customer.objects.filter(is_deleted=False)    
    

class CustomerDeleteView(View):
    template_name = "product/delete_customer.html"
    success_message = "Customer has been deleted successfully"

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, self.template_name, {'object' : customer})

    def post(self, request, pk):  
        customer = get_object_or_404(Customer, pk=pk)
        customer.is_deleted = True
        
        user_id = self.request.session['user_id']
        account = Account.objects.get(id=user_id)
        customer.fk_email = account
       
        customer.save()
        
        messages.success(request, self.success_message)
        return redirect('product:customers-list')


# used to select the customer
class SelectCustomerView(View):
    form_class = SelectCustomerForm
    template_name = 'product/select_customer.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # gets selected customer and redirects to 'SalesCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            customerid = request.POST.get("customer")
            customer = get_object_or_404(Customer, id=customerid)
            return redirect('product:new-sales', customer.pk)
        return render(request, self.template_name, {'form': form})


# used to generate a bill object and save items
class SalesCreateView(View):
                                                    
    template_name = 'product/new_sales.html'
    
    
    def get(self, request, pk):
        formset = SalesItemFormset(request.GET or None, prefix='sales_item')  # renders an empty formset
        
        customerobj = get_object_or_404(Customer, pk=pk)
        qs = SalesItem.objects.filter(cust_id=customerobj.id)
        
        
        context = {
            'formset': formset,
            'customer': customerobj,
            "queryset": qs,
           
        }
        return render(request, self.template_name, context)


    def post(self, request, pk):
        formset = SalesItemFormset(request.POST, prefix='sales_item')
        customerobj = get_object_or_404(Customer, pk=pk)
        print('l-263',customerobj)              
       
        msg_tag = "No item has been addded"                                   
        
        # Create a separate form for the 'docno' and 'docdt' fields
        doc_form = DocForm(request.POST)  # Replace 'YourDocForm' with your actual form class name
        
       

        if formset.is_valid() and doc_form.is_valid():        
            for form in formset:         
                if form.has_changed():
                    billitem = form.save(commit=False)
                    
                    if form.cleaned_data['stock']:
                        billitem.cust_id = customerobj.id
                        billitem.belt_no = form.cleaned_data['stock'].belt_no     
                        billitem.prod_des = form.cleaned_data['item_text_content']
                        billitem.quantity = form.cleaned_data['item_qty_content']
                        billitem.totalprice = form.cleaned_data['perprice']*form.cleaned_data['item_qty_content']
                        billitem.doc_no = request.POST['docno']
                        billitem.doc_dt = request.POST['docdt']
                        # gets the stock item
                        stock = get_object_or_404(Stock, belt_no=billitem.belt_no)       # gets the item
                        # updates status of stock db
                        stock.is_deleted = True                              # updates quantity
                        # saves bill item and stock
                        stock.save()
                        
                    try:  
                        billitem.save()
                       
                       
                    except IntegrityError:
                        error_message =  "<b>"+str(billitem.belt_no)+"</b> already exists. Please enter a unique Belt No."
                        messages.error(request, error_message)
                        return render(request, self.template_name, {'formset': formset, 'customer': customerobj})
                    
                    msg_tag = "Sales items have been registered successfully"    
                    messages.success(request, msg_tag)
                    msg_tag=""
               
            messages.info(request, msg_tag)

            #return render(request, self.template_name, context)
            #return redirect('product:select-customer')
            return redirect(request.path)
            #messages.info(request, "No item has been created..!")

        else:
            formset = SalesItemFormset(request.POST, prefix='sales_item')
            doc_form = DocForm(request.POST)  # Replace 'YourDocForm' with your actual form class name
            print('formset is not valid')
           
        
        context = {
            'formset': formset,
            'customer': customerobj,
            'doc_form': doc_form,  # Pass the doc_form to the template
            
        }
        return render(request, self.template_name, context)


# shows the list of bills of all purchases 
class SalesView(ListView):
    model = SalesBill
    template_name = "product/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10

def prod_stock_create(request,*args, **kwargs):
   
    user_id = request.session['user_id']
    account = Account.objects.get(id=user_id)
    
    
    if request.method == 'POST':
       
        StockFormSet = formset_factory(StockForm, extra=4)
        formset = StockFormSet(request.POST)
        
        
        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    stock = form.save(commit=False)                    
                    stock.fk_email = account
                    product = form.cleaned_data['prod_des']
                    stock.name = product.prod_code
                    stock.doc_no = stock.doc_no.upper()
                    stock.belt_no = stock.belt_no.upper()                    
                    
                    try:
                        stock.item_text = product
                        stock.save()
                    except IntegrityError as e:
                        # Handle the error when saving the Stock instance with duplicate "belt_no"
                        # Add an error message to the form for the "belt_no" field
                        form.add_error('belt_no', 'A stock with this Belt_no already exists.')

                    
            return redirect('product:stock-list')
    else:
       
        StockFormSet = formset_factory(StockForm, extra=4)
        formset = StockFormSet()
        
    context = {
        'formset': formset,
              
    }
    return render(request, 'product/stock_create.html', context)

class StockListView(ListView):
    model = Stock
    template_name = "product/stock_list.html"
    queryset = Stock.objects.filter(is_deleted=False)    

def edit_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock_item = form.save(commit=False)
            stock_item.save()
            return redirect('product:stock-list')
        
    else:
        form = StockForm(instance=stock)

    return render(request, 'product/edit_stock.html', {'form': form})

def stock_delete(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    
    if request.method == "POST":
        stock.delete()
        return redirect("product:stock-list")
        
    context = {'stock':stock}
    
    return render(request, 'product/stock_delete.html', context)



def get_stock_data_view(request, stockInstanceId):
    stock_instance = get_object_or_404(Stock, pk=stockInstanceId)
    

    stock_data = {
            'stock_id':stock_instance.id,                
            'item_text': stock_instance.item_text,
            'item_qty': stock_instance.quantity,            
            # Add more data fields as needed...
    }

    
    print("l-387 Stock Data:", stock_data)  # Add this line to print the stock data to the server log

    return JsonResponse(stock_data)
    
    
    #return JsonResponse(stock_data)


def edit_sales_item(request, doc_no):
    # Filter the queryset to retrieve only records with the specified doc_no
    sales_items = SalesItem.objects.filter(doc_no=doc_no)

    # Initialize other variables (customer, doc_no, doc_dt) as needed
    customer = None
    doc_no = None
    doc_dt = None

    for sales_item in sales_items:        
        if not customer:
            customer = get_object_or_404(Customer, pk=sales_item.cust_id)
            doc_no = sales_item.doc_no
            doc_dt = sales_item.doc_dt
    
    formset = modelformset_factory(SalesItem, form=SalesEditForm, extra=0)(queryset=sales_items, prefix='sales_item')
    forms_with_errors = [form for form in formset if form.errors]        
    
    if request.method == 'POST':
        formset = modelformset_factory(SalesItem, form=SalesEditForm, extra=0)(request.POST, queryset=sales_items, prefix='sales_item')
        
        if formset.is_valid():
       
            if formset.has_changed():
                formset.save()
                messages.success(request, "Record has been modified!")
                return redirect(request.path)
                #return redirect('product:new-sales', customer.id)  # Use customer_id instead of customer.pk
            messages.info(request, "No Changes made!")
        
    context = {
        'formset': formset,
        'forms_with_errors': forms_with_errors,
        'customer': customer,
        'doc_no': doc_no,
        'doc_dt': doc_dt,
    }

    return render(request, 'product/edit_sales_item.html', context)


def delete_sales_item(request, pk):
    # Filter the queryset to retrieve only records with the specified doc_no
    
    sales_item = get_object_or_404(SalesItem, id=pk)
    customer = get_object_or_404(Customer, pk=sales_item.cust_id)  
            
    if request.method == 'POST':
        # Check if the user has confirmed the deletion
        if request.POST.get('confirm_delete'):
            # gets the stock item
            stock = get_object_or_404(Stock, belt_no=sales_item.belt_no)       # gets the item
            # updates status of stock db
            stock.is_deleted = False                          # updates quantity
            # saves bill item and stock
            stock.save()
            sales_item.delete()
            return redirect('product:new-sales', customer.id)  # Replace 'product:some_url' with the desired URL name

    return render(request, 'product/delete_sales_item.html', {'sales_item': sales_item})
