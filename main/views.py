from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import *
from .models import *


class MainLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('/')


class MainLogout(LogoutView):
    next_page = '/login'


@login_required(login_url='/login')
@permission_required('item.delete_item', raise_exception=True)
def delete(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=pk)
        files = File.objects.filter(itemId=pk)
        photos = Photo.objects.filter(itemId=pk)
        files.delete()
        item.delete()
        photos.delete()
        return redirect('home')


@login_required(login_url='/login')
def home(request):
    categories = Category.objects.all()
    category_req = request.GET.get('category')
    fond_req = request.GET.get('fond')
    all_items_count = Item.objects.all().count()

    if category_req and not fond_req:
        category = Category.objects.get(pk=category_req)
        cat_id = category.id
        cat_sets = [category.id]
        for cat in category.get_descendants():
            cat_sets.append(cat.id)

        cat_sets.append(0)
        query_list = str(tuple(cat_sets))
        items = Item.objects.extra(where=['category_id in ' + query_list + ''])

    elif fond_req and not category_req:
        cat_id = 0
        fond = Fond.objects.get(pk=fond_req)
        items = Item.objects.filter(fonds=fond)

    elif fond_req and category_req:
        fond = Fond.objects.get(pk=fond_req)
        category = Category.objects.get(pk=category_req)
        cat_id = category.id
        cat_sets = [category.id]
        for cat in category.get_descendants():
            cat_sets.append(cat.id)

        cat_sets.append(0)
        query_list = str(tuple(cat_sets))
        cat_query = Item.objects.extra(where=['category_id in ' + query_list + ''])
        items = cat_query.filter(fonds=fond)

    else:
        items = Item.objects.all()
        cat_id = 0

    fonds = Fond.objects.all()
    return render(request, 'main/home.html',
                  {'cat': cat_id, 'items': items, 'items_count': all_items_count, 'cats': categories, 'fonds': fonds})


@login_required(login_url='/login')
def item(request, id):
    item_info = get_object_or_404(Item, pk=id)
    files = File.objects.filter(itemId=id)
    photos = Photo.objects.filter(itemId=id)
    photos_len = [i for i in range(1, len(photos) + 1)]
    category = Category.objects.get(pk=item_info.category_id)
    cats = category.get_ancestors()
    fonds = Fond.objects.filter(item=id)

    if request.user.has_perm('item.delete_item'):
        can_delete = True
    else:
        can_delete = False

    if request.method == 'POST':
        file_edit_form = FileEditForm(request.POST, request.FILES)
        photo_edit_form = PhotoEditForm(request.POST, request.FILES)

        print(request.POST, request.FILES)
        fs = FileSystemStorage(location='static/media')

        if request.FILES.get('fileEdit'):
            if file_edit_form.is_valid():
                uploaded_file = file_edit_form.cleaned_data['fileEdit']
                file_id = request.POST.get('id')
                fs.save(uploaded_file, uploaded_file)
                file = File.objects.get(id=file_id)
                file.fileDoc = 'static/media/' + uploaded_file.name
                file.save()
            else:
                print(file_edit_form.errors)

        if request.FILES.get('photoEdit'):
            if photo_edit_form.is_valid():
                uploaded_file = photo_edit_form.cleaned_data['photoEdit']
                photo_id = request.POST.get('id-photo-modal')
                fs.save(uploaded_file, uploaded_file)
                photo = Photo.objects.get(id=photo_id)
                photo.filePhoto = 'static/media/' + uploaded_file.name
                photo.save()
                return redirect('/item/' + str(id))
            else:
                print(photo_edit_form.errors)
    else:
        file_edit_form = FileEditForm
        photo_edit_form = PhotoEditForm

    return render(request, 'main/item.html',
                  {'item': item_info,
                   'files': files,
                   'fonds': fonds,
                   'photos': photos,
                   'category': category,
                   'photos_len': photos_len,
                   'file_edit': file_edit_form,
                   'photo_edit': photo_edit_form,
                   'cats': cats, 'can_delete': can_delete})


@login_required(login_url='/login')
def create(request):
    error = ''
    photo = 'static/no_photo.jpg'
    if request.method == 'POST':
        main_form = ItemForm(request.POST, request.FILES)
        file_form = files_formset(request.POST, request.FILES)
        photo_form = photos_formset(request.POST, request.FILES)
        if main_form.is_valid() and file_form.is_valid() and photo_form.is_valid():
            pre_save = main_form.save(commit=False)
            pre_save.last_editor = request.user
            main_form.save(commit=True)
            fs = FileSystemStorage(location='static/media')
            for f in file_form.cleaned_data:
                if 'fileDoc' in f:
                    itemId = Item.objects.all().last().id
                    uploaded_file = f['fileDoc']
                    fs.save(uploaded_file, uploaded_file)
                    file = File(fileDoc='static/media/' + uploaded_file.name, itemId=itemId)
                    file.save()
                else:
                    continue

            for f in photo_form.cleaned_data:
                if 'filePhoto' in f:
                    itemId = Item.objects.all().last().id
                    uploaded_file = f['filePhoto']
                    fs.save(uploaded_file, uploaded_file)
                    photo = Photo(filePhoto='static/media/' + uploaded_file.name, itemId=itemId)
                    photo.save()
                else:
                    continue

            return redirect('home')
        else:
            error = [main_form.errors, file_form.errors, photo_form.errors]
    else:
        main_form = ItemForm
        file_form = files_formset
        photo_form = photos_formset

    return render(request, 'main/create.html',
                  {'main_form': main_form, 'photo': photo, "file_form": file_form, 'photo_form': photo_form,
                   'error': error})


@login_required(login_url='/login')
def edit(request, pk):
    error = ''
    item_form = get_object_or_404(Item, pk=pk)
    photo = item_form.image.name
    if request.method == 'POST':
        main_form = ItemForm(request.POST, request.FILES, instance=item_form)
        file_form = files_formset(request.POST, request.FILES)
        photo_form = photos_formset(request.POST, request.FILES)
        if main_form.is_valid() and file_form.is_valid() and photo_form.is_valid():
            pre_save = main_form.save(commit=False)
            pre_save.last_editor = request.user
            main_form.save(commit=True)
            fs = FileSystemStorage(location='static/media')
            for f in file_form.cleaned_data:
                if 'fileDoc' in f:
                    uploaded_file = f['fileDoc']
                    fs.save(uploaded_file, uploaded_file)
                    file = File(fileDoc='static/media/' + uploaded_file.name, itemId=pk)
                    file.save()
                else:
                    continue

            for f in photo_form.cleaned_data:
                if 'filePhoto' in f:
                    uploaded_file = f['filePhoto']
                    fs.save(uploaded_file, uploaded_file)
                    photo = Photo(filePhoto='static/media/' + uploaded_file.name, itemId=pk)
                    photo.save()
                else:
                    continue
            return redirect('/item/' + str(pk))
        else:
            error = [main_form.errors, file_form.errors, photo_form.errors]
    else:
        main_form = ItemForm(instance=item_form)
        file_form = files_formset()
        photo_form = photos_formset()

    return render(request, 'main/edit.html',
                  {'main_form': main_form, "file_form": file_form, 'photo_form': photo_form, 'error': error,
                   'photo': photo, 'item_id': pk})