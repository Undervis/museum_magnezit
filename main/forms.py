from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from mptt.forms import TreeNodeChoiceField

from .models import *
from django.forms import *


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "date_story", "isArchived", "category", 'fonds', "image", 'index', 'comment']
        category = TreeNodeChoiceField(queryset=Category.objects.all())
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'id': 'titleInput'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'style': "height: 10rem",
                'id': 'descriptionInput',
            }),
            "category": Select(attrs={
                'class': 'form-select',
                'id': 'categoryInput',
                'value': ''
            }),
            "fonds": SelectMultiple(attrs={
                'class': 'form-select',
                'id': 'fondsInput',
                'multiple': True,
                'size': 5
            }),
            "date_story": TextInput(attrs={
                'class': 'form-control',
                'id': 'storyDateInput'
            }),
            "index": TextInput(attrs={
                'class': 'form-control',
                'id': 'indexInput',
            }),
            "image": FileInput(attrs={
                'class': 'form-control',
                'id': 'formFileMultiple',
                'style': 'font-family: BrutalType'
            }),
            "comment": Textarea(attrs={
                'class': 'form-control',
                'style': "height: 10rem; font-family: BrutalType",
                'id': 'commentInput',
            }),
            "isArchived": CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'isArchivedInput',
            }),
        }


class FileForm(forms.Form):
    fileDoc = forms.FileField(widget=FileInput(attrs={
        'class': 'form-control my-1',
        'id': 'filesInput',
        'style': 'font-family: BrutalType'
    }))


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PhotoForm(forms.Form):
    filePhoto = forms.FileField(widget=FileInput(attrs={
        'class': 'form-control my-1',
        'id': 'photosInput',
        'style': 'font-family: BrutalType'
    }))


files_formset = formset_factory(form=FileForm, extra=5, max_num=5)
photos_formset = formset_factory(form=PhotoForm, extra=5, max_num=5)