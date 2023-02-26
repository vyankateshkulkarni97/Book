"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstapp import old_views
from Users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', old_views.home ,name="home_page"),
    path('books/',old_views.show_book , name="all_active_books"),
    path('update/<int:pk>/',old_views.update_book , name="update_book"),
    path('delete/<int:pk>/',old_views.delete_book , name="delete_book"),
    path('softdelete/<int:pk>/',old_views.soft_delete_book , name="soft_delete_book"),
    path('inactive-books/',old_views.show_inactive_book , name="all_inactive_books"),
    path('restore-books/<int:pk>/',old_views.restore_book , name="restore_books"),
    
    path('book-form/',old_views.book_form, name="book_form"),
    path('sibtc-form/',old_views.sibtc, name="sibtc"),
    # spilte views
    # path('view_a/',views.view_a, name="view_a"),
    # path('view_b/',views.view_b, name="view_b"),
    # path('view_c/',views.view_c, name="view_c"),
    # path('view_d/',views.view_d, name="view_d"),
    path("index/",old_views.index , name="index"),

    # User url
    path('register/',user_views.register_request , name="register"),
    path('login/',user_views.login_request , name="login_user"),
    path('logout/',user_views.logout_user , name="logout_user"),

    # create and upload -csv file url
    path('csvexport/',old_views.csv_export , name="csv_export"),
    path('upload-csv/',old_views.upload_csv , name="upload_csv"),
    path('download-csv/',old_views.download_csv , name="download_csv"),

    # create Excel file:-inactive_book
    path('create-excel/',old_views.create_excel , name="create_excel"),
    path('active_book-excel/',old_views.active_book_excel , name="active_book"),

    # text file read  
     path('readfile', old_views.readfile,  name="readfile"),

    # raw query 
     path('rawqueries', old_views.raw_queries,  name="raw_queries"),





# class based views 
# path("cbv/",old_views.NewView.as_view(), name="cbv")
    path('cbv_book/', old_views.BookCreate.as_view(), name = 'Book_Create'),
    path('retrieve/', old_views.BookRetrieve.as_view(), name = 'BookRetrieve'),
    path('retrieve/<int:pk>/', old_views.BookDetail.as_view(), name = 'BookDetail'), 
    path('Update/<int:pk>/', old_views.BookUpdate.as_view(), name = 'BookUpdate'),    



]

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:  # development server only
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)