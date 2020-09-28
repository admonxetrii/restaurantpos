from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.
def mycustomvalidator(value) :
    if len(value) > 1 :
        return True
    else :
        raise ValidationError("Must have more than 1 characters.")


def val2(value) :
    if '@' in value or '#' in value or '*' in value :
        raise ValidationError("Title cannot have special charaters.")
    else :
        return True

class Profilepic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='User/', null=False, blank=False)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args,**kwargs)

    def save(self, *args, **kwargs) :
        # delete old file when replacing by updating the file
        try :
            this = Profilepic.objects.get(id=self.id)
            if this.image != self.image :
                this.image.delete(save=False)
        except :
            pass  # when new photo then we do nothing, normal case
        super(Profilepic, self).save(*args, **kwargs)

class MenuCategory(models.Model) :
    title = models.CharField(max_length=100, unique=True, validators=[mycustomvalidator, val2])
    image = models.ImageField(upload_to='CategoryMenu/', null=True, blank=True)

    def __str__(self) :
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args,**kwargs)

    def save(self, *args, **kwargs) :
        # delete old file when replacing by updating the file
        try :
            this = MenuCategory.objects.get(id=self.id)
            if this.image != self.image :
                this.image.delete(save=False)
        except :
            pass  # when new photo then we do nothing, normal case
        super(MenuCategory, self).save(*args, **kwargs)


class Menu(models.Model) :
    title = models.CharField(max_length=200, unique=True, validators=[mycustomvalidator, val2])
    price = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)

    def __str__(self) :
        return self.title

    class Meta :
        db_table = "menu"


class Table(models.Model):
    title = models.CharField(max_length=100, unique=True, validators=[mycustomvalidator, val2])
    occupied = models.IntegerField(null=True,blank=True)
    occHrs = models.IntegerField(null=True,blank=True)
    occMin = models.IntegerField(null=True,blank=True)
    reserved = models.IntegerField(null=True,blank=True)
    merged = models.IntegerField(null=True,blank=True)
    disval = models.FloatField(null=True,blank=True)

    def __str__(self) :
        return self.title



class Order(models.Model) :
    order_date = models.DateField(auto_now=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False,blank=False)
    printsts = models.IntegerField(null=True,blank=True)
    orderedby = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) :
        table = self.table.title
        dash = " - "
        menu = self.menu.title
        return table + dash + menu


class Bill(models.Model):
    fiscalyrs = models.CharField(max_length=50,null=True,blank=True)
    billnum = models.CharField(max_length=50,null=True,blank=True)
    bill_date = models.CharField(max_length=50,null=True)
    table = models.CharField(max_length=50,null=True,blank=True)
    amnt = models.FloatField(null=True,blank=True)
    discount = models.FloatField(null=True,blank=True)
    taxable_amnt = models.FloatField(null=True,blank=True)
    tax_amnt = models.FloatField(null=True,blank=True)
    total_amnt = models.FloatField(null=True,blank=True)
    sync_ird = models.IntegerField(null=True,blank=True)
    billprt = models.IntegerField(null=True,blank=True)
    billactive = models.IntegerField(null=True,blank=True)
    bill_time = models.TimeField(auto_now=True,null=True)
    billuser = models.CharField(max_length=64,null=True,blank=True)
    is_realtime = models.BooleanField(null=True,blank=True)
    payment_method = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self) :
        return self.billnum

class BillNo(models.Model):
    number = models.IntegerField(unique=True)

class masterPass(models.Model):
    password = models.CharField(max_length=50)


# class Inventory(models.Model) :
#     title = models.CharField(max_length=200, validators=[mycustomvalidator, val2])
#     quantity = models.IntegerField(null=False, blank=False)
#
#     def __str__(self) :
#         return self.title

#
# class MenuInventory(models.Model) :
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)

class MergeTable(models.Model):
    table1 = models.ForeignKey(Table,on_delete=models.CASCADE,related_name='table1')
    table2 = models.ForeignKey(Table,on_delete=models.CASCADE,related_name='table2')

# class TableDiscount(models.Model):
#     table = models.ForeignKey(Table,on_delete=models.CASCADE)
#     disval = models.FloatField(null=True,blank=True)

class RestoLogs(models.Model):
    datentime = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    activity = models.TextField(max_length=250)

