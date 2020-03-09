from django import forms
from .models import Menu,Order,Table,MenuCategory,Profilepic


class OrderForm(forms.ModelForm) :
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control'}))

    class Meta :
        model = Order
        fields = ['quantity',]

class UserPicForm(forms.ModelForm):

    class Meta :
        model = Profilepic
        fields = ['image',]


class MenuForm(forms.ModelForm) :
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','min':'1'}))
    category = forms.ModelChoiceField(queryset=MenuCategory.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Menu
        fields = '__all__'

class MenuCategoryForm(forms.ModelForm) :
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = MenuCategory
        fields = '__all__'

class TableForm(forms.ModelForm) :
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = Table
        fields = ['title',]
