from django.contrib import admin

from .models import Users, Category, Desgin, Comment

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at')
    search_fields = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Desgin)
class DesginAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user_uploaded', 'category', 'created_at')
    search_fields = ('title', 'category__name', 'user_uploaded__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'design', 'created_at')
    search_fields = ('user__username', 'design__title', 'text')
