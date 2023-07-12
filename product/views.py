from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.db.models import Avg,Sum
from django.http import HttpResponse
from django.forms import formset_factory, inlineformset_factory
from .forms import (
    ProductTCBForm,
    ProductSCBForm,
    CustomerForm,
    SelectCustomerForm,
    SalesItemFormset,
    )
    
from account.models import Account
from . models import Product, Customer,SalesBill
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
                     
                    matl.prod_des = "TCB "+str(matl.get_fab_type_display())+" "+str(matl.grade.name)+" "+str(matl.get_edge_display())
                    matl.email = account
                    
                    try:
                        matl.prod_code = str(matl.prod_tag)+str(matl.fab_type)+grd+str(matl.edge)
                       
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
                        
            matl.prod_des = "TCB "+str(matl.get_fab_type_display())+" "+str(matl.grade.name)+" "+str(matl.get_edge_display())
            try:
                matl.prod_code = str(matl.prod_tag)+str(matl.fab_type)+grd+str(matl.edge)
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
        formset = SalesItemFormset(request.GET or None)                      # renders an empty formset
        customerobj = get_object_or_404(Customer, pk=pk)                        # gets the supplier object
        context = {
            'formset'   : formset,
            'customer'  : customerobj,
        }                                                                       # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = SalesItemFormset(request.POST)                             # recieves a post method for the formset
        customerobj = get_object_or_404(Customer, pk=pk)                        # gets the supplier object
        if formset.is_valid():
            # saves bill
            billobj = CustomerBill(customer=customerobj)                        # a new object of class 'PurchaseBill' is created with supplier field set to 'supplierobj'
            billobj.save()                                                      # saves object into the db
            # create bill details object
            billdetailsobj = SalesBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)       # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity += billitem.quantity                              # updates quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(request, "Sales items have been registered successfully")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = SalesItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'customer'  : customerobj
        }
        return render(request, self.template_name, context)



# shows the list of bills of all purchases 
class SalesView(ListView):
    model = SalesBill
    template_name = "product/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10
