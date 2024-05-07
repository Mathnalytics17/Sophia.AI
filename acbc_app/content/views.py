from django.shortcuts import render, get_object_or_404, redirect
from .models import Library, Group, File
from .utils import FileUploadForm, hash_pdf
from django.http import HttpResponse


# View all libraries
def library_list(request):
    libraries = Library.objects.all()
    return render(request, 'content/libraries.html', {'libraries': libraries})


def user_library(request):
    library = Library.objects.filter(user=request.user).first()
    print(f"User: {request.user}")
    print(f"Library: {library}")
    library_files = File.objects.filter(library=library)
    print(f"Files: {library_files}")

    return render(request, 'content/user_library.html', {'library_files': library_files})


def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            # Extract file extension and save it
            file_instance.extension = file_instance.file.name.split('.')[-1]
            file_instance.save()
            return redirect('user_library')  # Adjust redirection as needed
    else:
        form = FileUploadForm()
    return render(request, 'content/file_upload.html', {'form': form})


def hash_pdf_view(request, file_id):
    file_instance = get_object_or_404(File, pk=file_id)

    if file_instance.extension.lower() == 'pdf':
        hash_value = hash_pdf(file_instance.file.path)

        # Save the hash to the database
        file_instance.hash = hash_value
        file_instance.save()

        # Redirect to the file detail view, passing the file's ID
        return redirect('file_detail', file_id=file_instance.id)

    return HttpResponse({'error': 'File is not a PDF'}, status=400)


def file_detail(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    return render(request, 'content/file_detail.html', {'file': file})


# Create a new library
def library_create(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        library = Library.objects.create(user=request.user, name=name)
        return redirect('library_list')
    return render(request, 'content/library_form.html')


# Update a library
def library_update(request, pk):
    library = get_object_or_404(Library, pk=pk)
    if request.method == "POST":
        library.name = request.POST.get('name', '')
        library.save()
        return redirect('library_list')
    return render(request, 'content/library_form.html', {'library': library})


# Delete a library
def library_delete(request, pk):
    library = get_object_or_404(Library, pk=pk)
    if request.method == "POST":
        library.delete()
        return redirect('library_list')
    return render(request, 'content/library_confirm_delete.html', {'library': library})


# Group views
# List groups in a library
def group_list(request, library_id):
    library = get_object_or_404(Library, pk=library_id)
    groups = Group.objects.filter(library=library)
    return render(request, 'content/group_list.html', {'library': library, 'groups': groups})


# Create a new group
def group_create(request, library_id):
    library = get_object_or_404(Library, pk=library_id)
    if request.method == "POST":
        name = request.POST.get('name', '')
        Group.objects.create(library=library, name=name)
        return redirect('group_list', library_id=library.id)
    return render(request, 'content/group_form.html', {'library': library})


# Update an existing group
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        group.name = request.POST.get('name', '')
        group.save()
        return redirect('group_list', library_id=group.library.id)
    return render(request, 'content/group_form.html', {'group': group})


# Delete a group
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    library_id = group.library.id
    if request.method == "POST":
        group.delete()
        return redirect('group_list', library_id=library_id)
    return render(request, 'content/group_confirm_delete.html', {'group': group})


# List files in a group
def file_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    files = File.objects.filter(group=group)
    return render(request, 'content/file_list.html', {'group': group, 'files': files})


# Create a new file
def file_create(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == "POST":
        file = request.FILES.get('file')
        title = request.POST.get('title', '')
        File.objects.create(group=group, file=file, title=title)
        return redirect('file_list', group_id=group.id)
    return render(request, 'content/file_form.html', {'group': group})


# Update an existing file
def file_update(request, pk):
    file = get_object_or_404(File, pk=pk)
    if request.method == "POST":
        file.title = request.POST.get('title', '')
        if 'file' in request.FILES:
            file.file = request.FILES['file']
        file.save()
        return redirect('file_list', group_id=file.group.id)
    return render(request, 'content/file_form.html', {'file': file})


# Delete a file
def file_delete(request, pk):
    file = get_object_or_404(File, pk=pk)
    group_id = file.group.id
    if request.method == "POST":
        file.delete()
        return redirect('file_list', group_id=group_id)
    return render(request, 'content/file_confirm_delete.html', {'file': file})
