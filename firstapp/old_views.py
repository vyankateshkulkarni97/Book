from django.shortcuts import render , HttpResponse , redirect 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
from .models import Book
# from django.contrib.auth.models import Book

# Create your views here.
@csrf_exempt
def home(request):
    print(request.method)
    if request.method == "POST":
        data =request.POST 
        bid = data.get("book_id")
        name = data.get("book_name")
        qty = data.get("book_qty")
        price = data.get("book_price")
        author = data.get("book_author")
        is_pub = data.get("book_is_pub")
        # print(id,name,qty,price,author,is_pub)
        if is_pub == "Yes":
            is_pub =True
        else:
            is_pub = False

        if not bid:
            Book.objects.create(name=name,qty=qty,price=price,author=author,is_published=is_pub)
        else:
            book_obj = Book.objects.get(id=bid)
            book_obj.name = name
            book_obj.qty = qty
            book_obj.price = price
            book_obj.author = author
            book_obj.is_published = is_pub
            book_obj.save()

        return redirect("home_page")
        # return HttpResponse("Data Successful Add....!")
    elif request.method == "GET":
        return render (request ,"home_old.html" , context={"person":"vyankatesh"})# 27:26
def show_book(request):
    return render(request,"show_book.html",{"books": Book.objects.filter(is_active=True), "active":True})

def update_book(request , pk):
    book_obj = Book.objects.get(id = pk)
    return render(request,"home.html", context={"single_book":book_obj})

def delete_book(request , pk):
    Book.objects.get(id=pk).delete()
    return redirect("all_active_books") 

def soft_delete_book(request , pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = False
    book_obj.save()
    return redirect("all_inactive_books")

def show_inactive_book(request):
    return render(request, "show_book.html",{"books" :Book.objects.filter(is_active=False), "inactive":True})

def restore_book(request , pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = True
    book_obj.save()
    return redirect("all_active_books")

from .forms import BookForm , AddressForm
# from django.contrib.auth.forms import UserCreationForm

def book_form(request):
    form = BookForm()
    if request.method == 'POST':
        print(request.POST)
        form = BookForm(data=request.POST)
        if form.is_valid():
            print(form.cleand_data)
            form.save()
            return HttpResponse("Successfully Registered!!!")
    else:
        context = {'form':form }
        return render(request, "book-form.html",context=context)

# simpleisbetterthancomplex

# from django import AddressForm 1:1

def sibtc(request):
    return render(request, "sibtc.html", {"form":AddressForm()})




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@csrf_exempt
def index(request):
    book_list = Book.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(book_list, 3)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, 'index.html', { 'books': books })


  
# from django.views import View  

# class NewView(View):  
#     def get(self, request):  
#         # View logic will place here  
#         return HttpResponse('in get response')  
#     def post(self, request):  
#         # View logic will place here  
#         return HttpResponse('in post response') 
#     def put(self, request):  
#         return HttpResponse('in get response') 
#     def patch(self, request):  
#         return HttpResponse('in patch response') 
#     def delete(self, request):  
#         return HttpResponse('in delete response') 

# CRUD
from django.views.generic.edit import CreateView  # 49:54
  
class BookCreate(CreateView):   # ccbv.co.uk refere
    model = Book 
    fields = '__all__'  
    success_url  = "/cbv_book/"

from django.views.generic.list import ListView

class BookRetrieve(ListView):
    model = Book
    context_object_name = "all_books"
    queryset = Book.objects.filter(is_active=1)
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    # def get_queryset(self):
    #     return Book.objects.filter(is_active=0)

from django.views.generic.detail import DetailView  

class BookDetail(DetailView):  
    model = Book

from django.views.generic.edit import UpdateView  # ccbv.co.uk refere
class BookUpdate(UpdateView):  
    model = Book
    # fields = "__all__"

# from django.views.generic.edit import TwmplateView  # ccbv.co.uk refere
# class Temlate(TemplateView):
#     template_name = "home.html"
#     extra_context = {"name":"vyankatesh"}

# https://www.javatpoint.com/django-class-based-generic-views

from django.http import HttpResponse
import csv
# --------------------------------------book cvs  expot --------------------------------------------
@csrf_exempt
def csv_export(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename="Export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Book_id','Name','Qty','Price','Author','Is_published','Is_active'])

    books = Book.objects.all().values_list('id','name','qty','price','author','is_published','is_active')
    for book in books:
        writer.writerow(book)
    return response

@csrf_exempt
def upload_csv(request): # validations
    file = request.FILES["csv_file"]
    # print(file)
    decoded_file = file.read().decode('utf-8').splitlines()
    expected_header = [ 'name' , "qty" , "author" , "is_published"]    
    actual_header = decoded_file[0].split(" , ").sort
    if expected_header != actual_header:
        return HttpResponse(" Error Headers are not Equal check the CSV file")
    elif expected_header == actual_header:
        reader = csv.DictReader(decoded_file)
        lst = []
        for element in reader:
            is_pub = element.get("is_published")
            print(is_pub)
            if is_pub == "TRUE":
                is_pub = True 
            else:
                is_pub = False
            lst.append(Book(name=element.get("name"), qty=element.get("qty"), price=element.get("price"), author=element.get("author"), is_published=is_pub))
        # print(reader)
    # print(lst)
    Book.objects.bulk_create(lst)
    return HttpResponse("success") 

def fun(request):
    return request


#--------------- assingment 9 :-------------------------------------------------
#------------- exel file excel  # only one book excel active book and inactive ----------
from django.http import HttpResponse
import xlwt
from openpyxl import Workbook
@csrf_exempt
def create_excel(request): 
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sample_book.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Book Data') # this will make a sheet named Book Data

    row_num = 0
    columns = ['Name','Qty','Price','Author','is_published','is_active' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num]) 
    rows = Book.objects.all().values_list('name','qty','price','author','is_published','is_active')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])
    wb.save(response)
    return response

# --------------------------------excel -- active book sheet , inactive sheet--------------------------
from openpyxl import Workbook , worksheet 
@csrf_exempt
def active_book_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="All_book.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    Active_sheet = wb.add_sheet('Active_Book') # this will make a sheet named Active Book
    Inactive_sheet =wb.add_sheet('inactive_book') # this will make a sheet named inactive Book
# ------------------------------Active book----------------------------------
    row_num = 0   # this will make a sheet named Active Book start from index = 0
    columns = ['Name','Qty','Price','Author','is_published','is_active' ]
    for col_num in range(len(columns)): # create columns and row in Active book
        Active_sheet.write(row_num, col_num, columns[col_num]) # in sheet write the row and colums given columns list for the Active book
    rows = Book.objects.filter(is_active=True).values_list('name','qty','price','author','is_published','is_active') # show_active_book 
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            Active_sheet.write(row_num, col_num, row[col_num]) # wirte the data from database into Active book
# ------------------------In-Active book-------------------------------------------
    row_num = 0   # this will make a sheet named inactive Book start from index = 0
    column = ['Name','Qty','Price','Author','is_published','is_active' ]
    for col_num in range(len(columns)):   # create columns and row in inactive book
        Inactive_sheet.write(row_num, col_num, column[col_num]) # in sheet write the row and colums given columns list for the inactive book
    row1 = Book.objects.filter(is_active=False).values_list('name','qty','price','author','is_published','is_active') # show_inactive_book 
    for row in row1:
        row_num += 1
        for col_num in range(len(row)):
            Inactive_sheet.write(row_num, col_num, row[col_num]) # wirte the data from database into inactive book
    wb.save(response) # save the workbook in Active data and Inactive data in worksheet
    return response
    


#---------------------- download sample file----------------------------------

import csv
@csrf_exempt
def download_csv(request):

    data = open(r'D:\python program\library\Library\media\test1.csv', 'r')
    print(data)
    response = HttpResponse(data , content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename="sample.csv"'
    return response



#-------------------------- read text file and show its content on UI views-------------------------- 
from django.core.files import File
from django.http import HttpResponse
@csrf_exempt
def readfile(request):    
    file = request.FILES["txt_file"].read()
    return HttpResponse(file)
    

#---------------- raw queries - using objects . raw (select * from books;) -- csv me dalna---------------

from django.db import connection
def raw_queries(request):
    data = connection.cursor()
    data.execute("SELECT * FROM vk_db.firstapp_book;")
    r = data.fetchall()
    # print(r) cursor
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename="All_Books.csv"'
    writer = csv.writer(response)
    writer.writerow(['Book_ID','Name','Qty','Price','Author','Is_Published','Is_Active'])
    for book in r:
        writer.writerow(book)
    return response




