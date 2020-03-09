from builtins import print

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from Restaurant.models import MenuCategory, Menu, Table, Order, Bill, BillNo, masterPass, Profilepic, MergeTable
from Restaurant.forms import MenuCategoryForm, UserPicForm
from django.http import Http404
from django.db.models import Sum
from datetime import datetime,time


@login_required(login_url='signin')
def report(request) :
    if request.user.is_superuser :
        # if request.method == 'GET' :
        #     return render(request, 'report.html')
        # date = request.POST['date']
        bill = Bill.objects.all()
        print(bill)
        context = {
            'bill' : bill
        }
        return render(request, 'report.html', context)
    return redirect('dashboard')


def signin(request) :
    if request.user.is_authenticated :
        return redirect('dashboard')
    if request.method == 'GET' :
        return render(request, 'login.html')
    else :
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        print(user)
        if user is not None :
            login(request, user)
            return redirect('dashboard')
        else :
            messages.add_message(request, messages.ERROR, "Your username and password doesn't match!!!")
            return redirect('signin')


def signup(request) :
    if request.user.is_authenticated :
        return redirect('dashboard')
    if request.method == 'GET' :
        return render(request, 'register.html')
    else :
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        un = request.POST['username']
        e = request.POST.get('email')
        mp = request.POST['mpass']
        m = masterPass.objects.get(id=1)
        p1 = request.POST['password']
        p2 = request.POST['password_repeat']
        if mp == m.password :
            if p1 == p2 :
                u = User(username=un, first_name=fn, last_name=ln)
                u.set_password(p1)
                u.save()
                user = User.objects.get(username=un)
                pic = Profilepic(user_id=user.id)
                pic.save()
                messages.add_message(request, messages.SUCCESS, "Your account is registered!!!")
                return redirect('signin')
            else :
                messages.add_message(request, messages.ERROR, "Your confirmation password doesn't match!!!")
                return redirect('register')
        else :
            messages.add_message(request, messages.ERROR, "Your master password doesn't match!!!")
            return redirect('register')


@login_required(login_url='signin')
def profilepage(request) :
    u = User.objects.get(id=request.user.id)
    picid = u.profilepic.id
    pic = Profilepic.objects.get(id=picid)
    form = UserPicForm(request.POST or None, request.FILES or None, instance=pic)
    if form.is_valid() :
        form.save()
        messages.add_message(request, messages.SUCCESS, "Profile picture changed successfully!!!")
        return redirect('profile')
    context = {
        'form' : form,
        'pic' : pic
    }
    return render(request, 'profile.html', context)



def edituser(request) :
    # u = request.POST['username']
    f = request.POST['firstname']
    l = request.POST['lastname']
    user = User.objects.get(pk=request.user.id)
    # user.username=u
    user.first_name = f
    user.last_name = l
    user.save()
    messages.add_message(request, messages.SUCCESS, "Your account is successfully changed!!!")
    return redirect('profile')


def editpassword(request) :
    p = request.POST['oldpass']
    p1 = request.POST['pass1']
    p2 = request.POST['pass2']
    u = request.user
    user = authenticate(username=u, password=p)
    if user is not None :
        user = User.objects.get(id=request.user.id)
        if p1 == p2 :
            user.set_password(p1)
            user.save()
            messages.add_message(request, messages.SUCCESS, "Your password is changed, Please Login again")
            return signout(request)
        else :
            messages.add_message(request, messages.ERROR, "Your confirm password doesn't match!!!")
            return redirect('profile')
    else :
        messages.add_message(request, messages.ERROR, "Your old password doesn't match!!!")
        return redirect('profile')

def editMpassword(request) :
    p = request.POST['oldMpass']
    p1 = request.POST['mpass1']
    p2 = request.POST['mpass2']
    mp = masterPass.objects.get(id=1)
    if p == mp.password :
        if p1 == p2 :
            mp.password = p1
            mp.save()
            messages.add_message(request, messages.SUCCESS, "Your master password is changed, Please Login again!!!")
            return signout(request)
        else :
            messages.add_message(request, messages.ERROR, "Your confirm master password doesn't match!!!")
            return redirect('profile')
    else :
        messages.add_message(request, messages.ERROR, "Your old master password doesn't match!!!")
        return redirect('profile')


def signout(request) :
    logout(request)
    messages.add_message(request, messages.ERROR, "You've been logged out!")
    return redirect('signin')


@login_required(login_url='signin')
def dash_board(request) :
    data = MenuCategory.objects.all()
    form = MenuCategoryForm(request.POST or None, request.FILES or None)
    if form.is_valid() :
        form.save()
        messages.add_message(request, messages.SUCCESS, "Menu Category created successfully!!!")
        return redirect('dashboard')
    context = {
        'form' : form,
        'category' : data
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='signin')
def editMenuCategory(request, id) :
    data = MenuCategory.objects.get(pk=id)
    form = MenuCategoryForm(request.POST or None, request.FILES or None, instance=data)
    if form.is_valid() :
        form.save()
        messages.add_message(request, messages.SUCCESS, "Category Updated successfully")
        return redirect('dashboard')
    context = {
        'form' : form,
        'cate' : data
    }
    return render(request, 'edit_menu_category.html', context)


@login_required(login_url='signin')
def tables(request) :
    data = MergeTable.objects.all()
    data1 = Table.objects.all()
    context = {
        'merge' : data,
        'table' : data1,
    }
    return render(request, 'table.html', context)


@login_required(login_url='signin')
def tableorder(request, id) :
    table = Table.objects.filter(id=id)
    tab = Table.objects.get(id=id)
    for t in table:
        table_merged = t.merged
        if table_merged==1:
            merge = MergeTable.objects.get(Q(table1_id=t.id) | Q(table2_id=t.id))
            table1 = Table.objects.filter(id= merge.table1.id) | Table.objects.filter(id= merge.table2.id)
            data = Order.objects.filter(table_id=merge.table1.id) | Order.objects.filter(table_id=merge.table2.id)
        else:
            table1 = table
            data = Order.objects.filter(table_id=id)
    context = {
        'order' : data,
        'table1' : table1,
        'table' : tab
    }
    return render(request, 'tabledetail.html', context)


@login_required(login_url='signin')
def menuitem(request, id) :
    data = Menu.objects.filter(category_id=id)
    cate = MenuCategory.objects.get(id=id)
    allCate = MenuCategory.objects.all()
    tab = Table.objects.filter(reserved=0)
    context = {
        'menu' : data,
        'cate' : cate,
        'table' : tab,
        'allCate' : allCate
    }
    return render(request, 'menu.html', context)


@login_required(login_url='signin')
def orderitem(request) :
    m = request.POST['menu']
    t = request.POST['table']
    qty = request.POST['qty']
    ps = 0
    ob = request.user.id
    form = Order(table_id=t, menu_id=m, quantity=qty, printsts=ps, orderedby_id=ob)
    form.save()
    data = Table.objects.get(id=t)
    data.occupied = 1
    data.save()
    messages.add_message(request, messages.SUCCESS, "Your order has been placed.")
    return redirect('table')

@login_required(login_url='signin')
def printOrd(request, id) :
    data = Order.objects.filter(table_id=id, printsts=0)
    table = Table.objects.get(id=id)
    context = {
        'order' : data,
        't' : table
    }
    return render(request, 'print_order.html', context)

@login_required(login_url='signin')
def printit(request,id):
    data = Order.objects.filter(table_id=id, printsts=0)
    for d in data:
        d.printsts=1
        d.save()
    return tableorder(request,id)


@login_required(login_url='signin')
def genBill(request, id) :
    billno = BillNo.objects.get(id=1)
    data = Order.objects.filter(table_id=id, printsts=1)
    a=0
    for d in data:
        a += 1
    if a == 0:
        return redirect('dashboard')
    table = Table.objects.get(id=id)
    context = {
        'order' : data,
        'table' : table,
        'billno' : billno,
    }
    return render(request, 'gen_bill.html', context)


@login_required(login_url='signin')
def releaseTable(request, id) :
    table = Table.objects.get(id=id)
    tablename = table.title
    data = Order.objects.filter(table_id=id)
    data.delete()
    t = request.POST['totalamount']
    b = request.POST['billnum']
    bill = Bill(table=tablename, total=t, billnum=b, billuser=request.user)
    bill.save()
    billno = BillNo.objects.get(id=1)
    billno.number = billno.number + 1
    billno.save()
    table.occupied = 0
    if table.title == 'Karaoke':
        table.occupiedHour = '00:00:00'
    table.save()
    messages.add_message(request, messages.SUCCESS, "Table Successfully released!!")
    return redirect('table')


@login_required(login_url='signin')
def closeTable(request, id) :
    table = Table.objects.get(pk=id)
    table.occupied = 0
    table.save()
    return redirect('table')


@login_required(login_url='signin')
def deletefromtable(request, id) :
    do = Order.objects.get(pk=id)
    id1 = do.table.id
    do.delete()
    messages.add_message(request, messages.ERROR, "Item removed successfully")
    return tableorder(request, id1)


@login_required(login_url='signin')
def editqty(request, id) :
    data = Order.objects.get(pk=id)
    id1 = data.table.id
    newqty = request.POST['qty']
    data.quantity = newqty
    data.save()
    return tableorder(request,id1)


@login_required(login_url='signin')
def addMenu(request, id) :
    title = request.POST['title']
    price = request.POST['price']
    add = Menu(title=title,price=price,category_id=id)
    add.save()
    messages.add_message(request,messages.SUCCESS,"Menu Item added successfully")
    return menuitem(request,id)

def reservedTable(request):
    if request.user.is_staff:
        table = Table.objects.all()
        if request.method == 'GET':
            context = {
                'table' : table
            }
            return render(request,'reserved.html',context)
        context = {
            'table' : table
        }
        id = request.POST['tblid']
        res = Table.objects.get(id=id)
        res.reserved = 0
        res.save()
        print(res.title)
        messages.add_message(request,messages.ERROR,"Table reservation cancelled of table "+res.title)
        return render(request,'table.html',context)
    messages.add_message(request,messages.ERROR,"Not Authorized")
    return tables(request)

def addReservation(request):
    if request.user.is_staff:
        table = Table.objects.all()
        id = request.POST['table']
        res = Table.objects.get(id=id)
        res.reserved=1
        res.save()
        messages.add_message(request,messages.SUCCESS,"Table - "+res.title+" is reserved")
        return render(request,'reserved.html',context={'table':table})
    messages.add_message(request,messages.ERROR,"Not Authorized")
    return tables(request)



@login_required(login_url='signin')
def addTables(request) :
    t = request.POST['title']
    form = Table(title=t, occupied=0,reserved=0,merged=0)
    form.save()
    messages.add_message(request, messages.SUCCESS, "Table created successfully!!!")
    return redirect('table')


@login_required(login_url='signin')
def editMenu(request, id) :
    data = Menu.objects.get(pk=id)
    id1 = data.category.id
    menuTitle = request.POST['title']
    price = request.POST['price']
    data.title = menuTitle
    data.price = price
    data.save()
    messages.add_message(request, messages.SUCCESS, "Menu Update successfully")
    return menuitem(request, id1)

def changeMenuCate(request, id) :
    data = Menu.objects.get(pk=id)
    cate = request.POST['newCategory']
    print(cate,data.category_id)
    data.category_id = cate
    data.save()
    print(data.category.id)
    return menuitem(request, cate)

@login_required(login_url='signin')
def editTable(request, id) :
    data = Table.objects.get(pk=id)
    newtitle = request.POST['newtitle']
    data.title = newtitle
    data.save()
    return tables(request)


@login_required(login_url='signin')
def deletefrommenu(request, id) :
    dm = Menu.objects.get(pk=id)
    id1 = dm.category.id
    dm.delete()
    messages.add_message(request, messages.ERROR, "Item deleted successfully")
    return menuitem(request, id1)


@login_required(login_url='signin')
def deletefrommenucat(request, id) :
    dm = MenuCategory.objects.get(pk=id)
    dm.delete()
    messages.add_message(request, messages.ERROR, "Item deleted successfully")
    return redirect('dashboard')


@login_required(login_url='signin')
def deletetable(request, id) :
    t = Table.objects.get(pk=id)
    t.delete()
    messages.add_message(request, messages.ERROR, "Table deleted successfully")
    return redirect('table')


def forgot(request) :
    if request.method == 'GET' :
        user = User.objects.all()
        context = {
            'user' : user
        }
        return render(request, 'forgot_password.html', context)


def reset_pass(request) :
    u = request.POST['user']
    m = request.POST['mpass']
    user = User.objects.get(id=u)
    mp = masterPass.objects.get(id=1)
    if m == mp.password :
        context = {
            'user' : user
        }
        return render(request, 'reset.html', context)
    else :
        messages.add_message(request, messages.ERROR, "Your master password doesn't match!!!")
        return redirect('forgot')

def time_diff(time_str1, time_str2):
    t1 = datetime.strptime(time_str1, '%H:%M')
    t2 = datetime.strptime(time_str2, '%H:%M')
    dt = abs(t2 - t1)
    return time(dt.seconds // 3600, (dt.seconds // 60) % 60).strftime('%H:%M')


def reset_pass_complete(request, id) :
    user = User.objects.get(id=id)
    p1 = request.POST['pass1']
    p2 = request.POST['pass2']
    if p1 == p2 :
        user.set_password(p1)
        user.save()
        messages.add_message(request, messages.SUCCESS, "Your password is change!!!")
        return redirect('signin')
    else :
        messages.add_message(request, messages.ERROR, "Your confirm password doesn't match!!!")
        context = {
            'user' : user
        }
        return render(request, 'reset.html', context)

@login_required(login_url='signin')
def changetable (request, id):
    # oldTable = Table.objects.get(id=id)
    # t = request.POST['newTable']
    # newTable = Table.objects.get(id=t)
    # nt = newTable.title
    # ot = oldTable.title
    # tmpNt = nt
    # tmpOt = ot
    # tmp = "temp"
    # newTable.title = tmp
    # newTable.save()
    # oldTable.title = tmpNt
    # oldTable.save()
    # newTable.title = tmpOt
    # newTable.save()

    oldTable = Table.objects.get(id=id)
    t = request.POST['newTable']
    newTable = Table.objects.get(id=t)
    orders = Order.objects.filter(table_id=id)
    for o in orders:
        o.table_id = newTable.id
        o.save()
    newTable.occupied = 1
    newTable.save()
    oldTable.occupied = 0
    oldTable.save()
    return tables(request)


@login_required(login_url='signin')
def allUsers(request):
    if request.user.is_superuser:
        users = User.objects.all()
        context = {
            'users' : users
        }
        return render(request,'users.html',context)
    return redirect('dashboard')

@login_required(login_url='signin')
def editAllUsers(request):
    if request.user.is_superuser:
        users = User.objects.all()
        context = {
            'users' : users
        }
        return render(request,'editusers.html',context)
    return redirect('dashboard')

@login_required(login_url='signin')
def saveEditedUser(request):
    if request.user.is_superuser:
        users = User.objects.all()
        for u in users:
            stf = request.POST['stf_'+str(u.id)]
            adm = request.POST['adm_'+str(u.id)]
            act = request.POST['act_'+str(u.id)]
            u.is_staff = stf
            u.is_superuser = adm
            u.is_active = act
            u.save()

        return allUsers(request)

# def delete_user(request,username):
#     mpass = request.POST['mpass']
#     data = masterPass.objects.get(id=1)
#     users = User.objects.all()
#     u = User.objects.get(username=username)
#     if mpass==data.password:
#         u.delete()
#         u.save()
#         context = {
#             'data' : data,
#             'users' : users
#         }
#         print(u.username, u.id)
#         messages.add_message(request,messages.SUCCESS,"User Deleted!!")
#         return render(request,'users.html',context)
#     context1 = {
#         'users' : users
#     }
#     messages.add_message(request,messages.ERROR,"Not Authorized!!!")
#     return render(request,'editusers.html',context1)

def additemstotable(request, id):
    if request.method == 'GET' :
        table = Table.objects.get(id=id)
        menu = Menu.objects.all()
        context = {
            'menu' : menu,
            'table' : table
        }
        return render(request, 'allitem.html',context)
    m = request.POST['menu']
    qty = request.POST['qty']
    ps = 0
    ob = request.user.id
    form = Order(table_id=id, menu_id=m, quantity=qty, printsts=ps, orderedby_id=ob)
    form.save()
    data = Table.objects.get(id=id)
    data.occupied = 1
    data.save()
    messages.add_message(request, messages.SUCCESS, "Your order has been placed.")
    return tableorder(request,id)

def mergeTable(request):
    t1 = request.POST['tbl1']
    t2 = request.POST['tbl2']
    tbl1 = Table.objects.get(id=t1)
    tbl2 = Table.objects.get(id=t2)
    order = Order.objects.filter(table_id=tbl2)
    for o in order:
        o.table_id = tbl1
        o.save()
    tbl1.merged = 1
    tbl2.merged = 1
    tbl2.occupied = 0
    tbl1.save()
    tbl2.save()
    merge = MergeTable(table1_id=t1,table2_id=t2)
    merge.save()
    return tables(request)

def unmergeTable(request,id):
    mt = MergeTable.objects.get(id=id)
    tbl1 = Table.objects.get(id=mt.table1.id)
    tbl1.merged=0
    tbl1.save()
    tbl2 = Table.objects.get(id=mt.table2.id)
    tbl2.merged=0
    tbl2.save()
    mt.delete()
    return tables(request)
