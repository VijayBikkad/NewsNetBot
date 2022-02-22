from django.contrib.auth.backends import UserModel
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from news.models import User
from django.contrib.auth import authenticate, login,logout
from django.conf import settings
from django.core.mail import send_mail 

# Create your views here.
import requests
from bs4 import BeautifulSoup

# GEtting news from Times of India

toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')

toi_headings = toi_soup.find_all('h2')

toi_headings = toi_headings[2:-13] 


toi_news = []

for th in toi_headings:
    toi_news.append(th.text)





ht_r = requests.get("https://www.lokmat.com/career/")
ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.findAll("h2")
ht_headings = ht_headings[2:-2]
ht_news = []

for hth in ht_headings:
    ht_news.append(hth.text)

@login_required(login_url='login')
def index(req):
    return render(req, 'news/index.html', {'toi_news':toi_news, 'ht_news': ht_news})

#define login view 
def login_view(request):
    if request.method == "POST":
        username=request.POST['username']
        password = request.POST['password']
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("Invalid data")
    elif request.method == "GET":
        return render(request,"news/login.html")

@login_required(login_url='login')  
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    if request.method == 'GET':
        return render(request,'news/register.html')

    elif request.method =="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        print("post recieved")
        print(username, email, password)
        try:
            user=User.objects.create_user(username,email,password)
            user.save()
            subject = "news Account created"
            email_body = "Congratulations! Your news account has been successfully created."
            email_from = settings.EMAIL_HOST_USER
            recipents = [email,]
            print(subject, email_body, email_from, recipents)
            send_mail(subject=subject, message=email_body, from_email=email_from, recipient_list=recipents, fail_silently=False,)
        except:
            print("Error occurred...")
            return HttpResponseRedirect(reverse('login'))
        login(request, user)
         return HttpResponseRedirect(reverse('home'))
    