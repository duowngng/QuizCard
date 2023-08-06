from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from.models import Set, Topic, Card
from.forms import SetForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
    
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong, please try again')

    context = {'page':page, 'form':form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    sets = Set.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
        )
    topics = Topic.objects.all()
    set_count = sets.count()
    context = {'sets':sets, 'topics':topics, 'set_count':set_count}
    return render(request, 'base/home.html', context)

def set(request, pk):
    set = Set.objects.get(id=pk)
    set_cards = set.card_set.all().order_by('-created')
    
    if request.method == 'POST':
        card = Card.objects.create(
            set = set,
            front = request.POST.get('front'),
            back = request.POST.get('back'),
        )
        return redirect('set', pk=set.id)
    
    context = {'set': set, 'set_cards': set_cards}
    return render(request, 'base/set.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    sets = user.set_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'sets':sets, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createSet(request):
    form = SetForm()
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/set_form.html', context)

@login_required(login_url='login')
def updateSet(request, pk):
    set = Set.objects.get(id=pk)
    form = SetForm(instance=set)
    
    if request.user != set.user:
        return HttpResponse('You are not allowed to update this set')
    
    if request.method == 'POST':
        form = SetForm(request.POST, instance=set)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/set_form.html', context)

@login_required(login_url='login')
def deleteSet(request,pk):
    set = Set.objects.get(id=pk)
    
    if request.user != set.user:
        return HttpResponse('You are not allowed to delete this set')
    
    if request.method == 'POST':
        set.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':set})

@login_required(login_url='login')
def deleteCard(request, spk, cpk):
    set = Set.objects.get(id=spk)
    card = Card.objects.get(id=cpk)
    
    if request.user != set.user:
        return HttpResponse('You are not allowed to delete')
    
    if request.method == 'POST':
        card.delete()
        return redirect('set', pk=set.id)
    
    return render(request, 'base/delete.html', {'obj':card})
