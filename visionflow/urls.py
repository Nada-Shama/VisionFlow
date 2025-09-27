from django.contrib import admin
from django.urls import path
from vision_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path("profile/<int:user_id>/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<int:user_id>/add_design/", views.add_design, name="add_design"),
    path('design/<int:num>/', views.design, name='design'),
    path('new/',views.new,name='new'),
    path('upload/',views.upload,name='upload'),   
    path('category/<int:category_id>/', views.category, name='category'),
 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)