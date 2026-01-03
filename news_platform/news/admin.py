from django.contrib import admin
# Точка перед models означает "из текущей папки"
from .models import Tovar, Category

admin.site.register(Tovar)
admin.site.register(Category)