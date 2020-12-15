"""restomansys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/',views.report,name='report'),
    path('users/',views.allUsers,name='users'),
    path('edit-users/',views.editAllUsers,name='edit_users'),
    path('edit-all-users/',views.saveEditedUser,name='edited_users'),
    path('',views.signin,name='signin'),
    path('register/',views.signup,name='register'),
    path('setting/',views.accountsetting,name='setting'),
    path('profile/',views.profilepage,name='profile'),
    path('editprofile/',views.edituser,name='edit_profile'),
    path('editpass/',views.editpassword,name='edit_pass'),
    path('editmpass/',views.editMpassword,name='edit_m_pass'),
    path('signout/',views.signout,name='signout'),
    path('dashboard/',views.dash_board,name='dashboard'),
    path('sales/',views.sales,name='sales'),
    path('logs/',views.restrologs,name='logs'),
    path('table/',views.tables,name='table'),
    path('menu/<int:id>',views.menuitem,name='menu'),
    path('gen-bill/<int:id>',views.genBill,name='genbill'),
    path('gen-tax-bill/<int:id>',views.genTaxBill,name='gentaxbill'),
    path('print-bill/<int:id>',views.printbill,name='printbill'),
    path('print-tax-bill/<int:id>',views.printbill1,name='printbill1'),
    path('del-dis/<int:id>',views.removedis,name='removedis'),
    path('del-tax-dis/<int:id>',views.removedis1,name='removedis1'),
    path('ptr-ord/<int:id>',views.printOrd,name='printOrd'),
    path('ptr-it/<int:id>',views.printit,name='printit'),
    path('release-table/<int:id>',views.releaseTable,name='releaseTable'),
    path('close-table/<int:id>',views.closeTable,name='closeTable'),
    path('change-table/<int:id>',views.changetable,name='changetable'),
    path('change-cate/<int:id>',views.changeMenuCate,name='changeMenuCate'),
    path('table-order/<int:id>',views.tableorder,name='tableorder'),
    path('item-delete/<int:id>',views.deletefromtable,name='delitem'),
    path('item-serve/<int:id>',views.serveitem,name='serveitem'),
    path('item-unserve/<int:id>',views.unserveitem,name='unserveitem'),
    path('menu-delete/<int:id>',views.deletefrommenu,name='delmenu'),
    path('category-delete/<int:id>',views.deletefrommenucat,name='delmenucat'),
    path('table-delete/<int:id>',views.deletetable,name='deleteTable'),
    path('item-edit/<int:id>',views.editqty,name='editqty'),
    path('menu-edit/<int:id>',views.editMenu,name='editMenu'),
    path('category-edit/<int:id>',views.editMenuCategory,name='editMenuCategory'),
    path('table-edit/<int:id>',views.editTable,name='editTable'),
    path('order/',views.orderitem,name='order'),
    path('merge-table/',views.mergeTable,name='merge_table'),
    path('unmerge-table/<int:id>',views.unmergeTable,name='unmerge_table'),
    path('add-menu/<int:id>',views.addMenu,name='addMenu'),
    path('add-table/',views.addTables,name='addTables'),
    path('forgot-password/',views.forgot,name='forgot'),
    path('reset-password/',views.reset_pass,name='reset'),
    path('reset-confirm/<int:id>',views.reset_pass_complete,name='resetcomplete'),
    path('reserved-table/',views.reservedTable,name='reservedTable'),
    path('add-reservation/',views.addReservation,name='addReservation'),
    path('add-item/<int:id>',views.addmoreitems,name='addmoreitems'),
    path('add-item-conf/<int:id>',views.additemstotable,name='additem'),
    path('send-cbms/<int:id>',views.sendToCBMS,name='cbms'),
    path('send-cbms-all/',views.sendAllToCBMS,name='cbmsauto'),
    path('send-cbms-manual/',views.sendToCBMSmanual,name='cbmsmanual'),
    path('eula/',views.eula,name='eula'),
    path('policy/',views.privacyAndPolicy,name='policy')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
