from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Show

def index(request):
    shows = Show.objects.all()
    return render(request, 'shows/show_list.html', {'shows': shows})

def new(request):
    return render(request, 'shows/new_show.html')

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        network = request.POST['network']
        release_date = request.POST['release_date']
        description = request.POST['description']
        show = Show.objects.create(title=title, network=network, release_date=release_date, description=description)
        return redirect('shows:detail', show.id)

def detail(request, id):
    show = get_object_or_404(Show, pk=id)
    return render(request, 'shows/show_detail.html', {'show': show})

def edit(request, id):
    show = get_object_or_404(Show, pk=id)
    return render(request, 'shows/edit_show.html', {'show': show})

def update(request, id):
    if request.method == 'POST':
        show = get_object_or_404(Show, pk=id)
        show.title = request.POST['title']
        show.network = request.POST['network']
        show.release_date = request.POST['release_date']
        show.description = request.POST['description']
        show.save()
        return redirect('shows:detail', show.id)

def destroy(request, id):
    show = get_object_or_404(Show, pk=id)
    show.delete()
    return redirect('shows:index')

