from django.contrib import admin
from .models import Menu,MenuCategory,Table,Order,Bill,BillNo,Profilepic
# Register your models here.
admin.site.register(Menu)
admin.site.register(MenuCategory)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(Bill)
admin.site.register(Profilepic)

