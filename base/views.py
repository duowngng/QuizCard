from django.shortcuts import render, redirect
from.models import Set
from .forms import SetForm

def home(request):
    sets = Set.objects.all()
    context = {'sets':sets}
    return render(request, 'base/home.html', context)

def set(request, pk):
    set = Set.objects.get(id=pk)
    context = {'set': set}
    return render(request, 'base/set.html', context)

def createSet(request):
    form = SetForm()
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/set_form.html', context)

def updateSet(request, pk):
    set = Set.objects.get(id=pk)
    form = SetForm(instance=set)
    if request.method == 'POST':
        form = SetForm(request.POST, instance=set)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/set_form.html', context)

def deleteSet(request,pk):
    set = Set.objects.get(id=pk)
    if request.method == 'POST':
        set.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':set})
