from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image', 'stock_quantity', 
                 'is_featured', 'weight', 'dimensions']
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 4}),
        #     'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        #     'stock_quantity': forms.NumberInput(attrs={'min': '0'}),
        #     'weight': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             Column('name', css_class='form-group col-md-8 mb-0'),
    #             Column('category', css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Field('description'),
    #         Row(
    #             Column('price', css_class='form-group col-md-4 mb-0'),
    #             Column('stock_quantity', css_class='form-group col-md-4 mb-0'),
    #             Column('weight', css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Field('dimensions'),
    #         Field('image'),
    #         Field('is_featured'),
    #         Submit('submit', 'Enregistrer le produit', css_class='btn btn-warning btn-lg mt-3')
    #     )
