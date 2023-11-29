from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.db.models import F, Sum, Avg, Count
from datetime import datetime, timedelta
from pprint import pprint

# Create your views here.


def index(request):
    chart = BloodTypes.objects.all()
    count = Request.objects.filter(status='Pending').count()
    coun = Request.objects.filter(status='Rejected').count()
    cou = Request.objects.filter(status='Accepted').count()
    all = User.objects.all().count()
    #u = BloodTypes.objects.aggregate(avg=Sum('pint'))
    total = BloodTypes.objects.filter(name='O+').aggregate(avg=Sum('pint'))
    total_o_negative = BloodTypes.objects.filter(name='O-').aggregate(avg=Sum('pint'))
    total_a_positive = BloodTypes.objects.filter(name='A+').aggregate(avg=Sum('pint'))

    rp = Request.objects.filter(blood__name='O+').aggregate(cal=Sum('pint'))
    rn = Request.objects.filter(blood__name='O-').aggregate(cal=Sum('pint'))
    ra = Request.objects.filter(blood__name='A+').aggregate(cal=Sum('pint'))
    ran = Request.objects.filter(blood__name='A-').aggregate(cal=Sum('pint'))

    p = Donor.objects.filter(blood__name='O+').aggregate(cal=Sum('pint'))
    n = Donor.objects.filter(blood__name='O-').aggregate(cal=Sum('pint'))
    a = Donor.objects.filter(blood__name='A+').aggregate(cal=Sum('pint'))
    an = Donor.objects.filter(blood__name='A-').aggregate(cal=Sum('pint'))

    o_positive = total['avg'] + p['cal']
    o_negative = total_o_negative['avg'] + n['cal']
    a_positive = total_a_positive['avg'] + a['cal']
    u = o_negative + o_positive + a_positive

    o_positive = p['cal'] - rp['cal']
    print(o_positive)
    o_negative = n['cal'] - rn['cal']
    a_positive = a['cal'] - ra['cal']
    a_negative = an['cal'] - ran['cal']

    context = {
        'chart': chart,
        'count': count,
        'coun': coun,
        'cou': cou,
        'all': all,
        'u': u,
        'o_positive': o_positive,
        'o_negative': o_negative,
        'a_positive': a_positive,
        'a_negative': a_negative,

    }
    return render(request, 'donor/index.html', context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Welcome Please Login')
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'donor/register.html', {'form': form})


def make_request(request):
    total = BloodTypes.objects.aggregate(sum=Sum('pint'))
    total_0_positive = BloodTypes.objects.filter(name='O+').aggregate(avg=Sum('pint'))
    total_o_negative = BloodTypes.objects.filter(name='O-').aggregate(avg=Sum('pint'))
    total_a_positive = BloodTypes.objects.filter(name='A+').aggregate(avg=Sum('pint'))
    rp = Request.objects.filter(blood__name='O+').aggregate(cal=Sum('pint'))
    rn = Request.objects.filter(blood__name='O-').aggregate(cal=Sum('pint'))
    ra = Request.objects.filter(blood__name='A+').aggregate(cal=Sum('pint'))
    o_positive = total_0_positive['avg'] - rp['cal']
    o_negative = total_o_negative['avg'] - rn['cal']
    a_positive = total_a_positive['avg'] - ra['cal']
    u = o_negative + o_positive + a_positive
    p = Donor.objects.filter(blood__name='O+').aggregate(cal=Sum('pint'))
    n = Donor.objects.filter(blood__name='O-').aggregate(cal=Sum('pint'))
    a = Donor.objects.filter(blood__name='A+').aggregate(cal=Sum('pint'))

    o_positive = p['cal'] - rp['cal']
    o_negative = n['cal'] - rn['cal']
    a_positive = a['cal'] - ra['cal']
    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            pint = form.cleaned_data['pint']
            instance = form.save(commit=False)
            instance.name = request.user
            if pint > o_positive or pint > a_positive or pint > o_negative:
                messages.error(request, f'Sorry, we do not have up to the required amount of blood in our bank')
                return redirect('index')
            else:
                instance.save()
                messages.success(request, f'{request.user.username}, We are here to save a life, we will get back in 5 minutes')
                return render(request, 'donor/make_request.html', {'form': form})
    else:
        form = RequestForm()
    context = {
            'form': form,
            'u': u,
            'o_positive': o_positive,
            'o_negative': o_negative,
            'a_positive': a_positive,

            }
    return render(request, 'donor/make_request.html', context)


def request_view(request):
    emg = Request.objects.filter(name=request.user.id)
    return render(request, 'donor/request_view.html', {'emg': emg})


def donors(request):
    #u = BloodTypes.objects.aggregate(avg=Sum('pint'))
    u = BloodTypes.objects.filter(name='O+').aggregate(avg=Sum('pint'))
    p = Donor.objects.filter(blood__name='O+').aggregate(cal=Sum('pint'))
    print(u['avg'] + p['cal'])
    today = datetime.now()
    don = today + timedelta(seconds=20)
    #t = res - u['avg'] - 1

    user = User.objects.filter(username=request.user)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = request.user
            
            instance.save()
            '''new = BloodTypes(pint=t)
            new.save()'''
            messages.success(request, f'Thank your {request.user.first_name} for your donation, You have saved a life')
            return redirect('index')
    else:
        form = DonationForm()
    context = {
        'user': user,
        'form': form,

    }
    return render(request, 'donor/donors.html', context)


def profile(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'donor/profile.html', {'profile': profile})


def profile_edit(request, pk):
    update = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=update)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=update)
    return render(request, 'donor/profile_edit.html', {'form': form, 'update': update})
