from django.shortcuts import render, redirect
from .models import Show

# View to list all shows
def index(request):
    shows = Show.objects.all()
    return render(request, 'shows/show_list.html', {'shows': shows})

# View to display details of a specific show
def show_detail(request, id):
    try:
        show = Show.objects.get(id=id)
    except Show.DoesNotExist:
        return redirect('shows:index')
    return render(request, 'shows/show_detail.html', {'show': show})

# View to add a new show
def new_show(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        network = request.POST.get('network')
        release_date = request.POST.get('release_date')
        description = request.POST.get('description')
        
        show = Show.objects.create(
            title=title,
            network=network,
            release_date=release_date,
            description=description
        )
        return redirect('shows:detail', id=show.id)
    return render(request, 'shows/new_show.html')

# View to edit an existing show
def edit_show(request, id):
    try:
        show = Show.objects.get(id=id)
    except Show.DoesNotExist:
        return redirect('shows:index')
    
    if request.method == 'POST':
        show.title = request.POST.get('title')
        show.network = request.POST.get('network')
        show.release_date = request.POST.get('release_date')
        show.description = request.POST.get('description')
        show.save()
        return redirect('shows:detail', id=show.id)
    return render(request, 'shows/edit_show.html', {'show': show})

# View to delete a show
def delete_show(request, id):
    try:
        show = Show.objects.get(id=id)
    except Show.DoesNotExist:
        return redirect('shows:index')
    
    if request.method == 'POST':
        show.delete()
        return redirect('shows:index')
    return render(request, 'shows/show_detail.html', {'show': show})
