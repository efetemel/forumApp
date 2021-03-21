from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import string
from datetime import datetime
import pytz
import locale
from random import *
from .models import User
from .models import Post
from .models import ForgotPassword


def index(request):
  userID = ""
  posts = Post.objects.order_by('-id')
  trend = Post.objects.order_by('-like_count')
  try:
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    context = {
      'is_login': 'true',
      'posts': posts,
      'trends': [trend[0], trend[1], trend[2]],
      'user': user,
    }
    writeLog('Sayfa Görüntülenmesi', 'İndex')
    response = render(request, 'index.html', context)
  except:
    context = {
      'is_login': 'false',
      'posts': posts,
      'trends': [trend[0], trend[1], trend[2]],
    }
    writeLog('Sayfa Görüntülenmesi', 'İndex')
    response = render(request, 'index.html', context)
  return response


def login(request):
  posts = Post.objects.order_by('-id')
  trend = Post.objects.order_by('-like_count')
  response = ""
  if 'email' in request.POST and 'password' in request.POST:
    writeLog('Sayfa Görüntülenmesi', 'Login')
    try:
      email = request.POST['email']
      password = request.POST['password']
      user = User.objects.get(email=email)
      if password == user.password:
        request.session['userID'] = user.userID
        context = {
          'is_login': 'true',
          'posts': posts,
          'trends': [trend[0], trend[1], trend[2]],
          'user': user,
        }
        response = render(request, 'index.html', context)
      else:
        response = render(request, 'login.html')
    except:
      response = render(request, 'login.html')
  else:
    writeLog('Sayfa Görüntülenmesi', 'Login')

    try:
      userID = request.session['userID']
      user = User.objects.get(userID=userID)
      context = {
        'is_login': 'true',
        'posts': posts,
        'trends': [trend[0], trend[1], trend[2]],
        'user': user,
      }
      response = render(request, 'index.html', context)
    except:
      response = render(request, 'login.html')
  return response


def logout(request):
  posts = Post.objects.order_by('-id')
  trend = Post.objects.order_by('-like_count')
  try:
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    request.session['userID'] = ""
    context = {
      'is_login': 'false',
      'posts': posts,
      'trends': [trend[0], trend[1], trend[2]],
    }
    response = render(request, 'index.html', context)
  except:
    context = {
      'is_login': 'false',
      'posts': posts,
      'trends': [trend[0], trend[1], trend[2]],
    }
    response = render(request, 'index.html', context)
  return response


def profile(request, username):
  try:
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user.username).order_by('-id')
    trend = Post.objects.order_by('-like_count')
    is_login = 'false'
    myUserId = ""
    try:
      myUserId = request.session['userID']
    except:
      myUserId = ""
    if myUserId != "":
      if myUserId == user.userID:  # profil bizim
        is_login = 'true'
        context = {
          'is_login': is_login,
          'posts': posts,
          'user': user,
        }
        response = render(request, 'profiles/my-profile.html', context)
      else:  # profil başkasının
        is_login = 'true'
        context = {
          'is_login': is_login,
          'posts': posts,
          'user': user,
        }
        response = render(request, 'profiles/profile.html', context)
    else:
      is_login = 'false'
      context = {
        'is_login': is_login,
        'posts': posts,
        'user': user,
      }
      response = render(request, 'profiles/profile.html', context)
  except:
    print("hata!")
    response = redirect("/")

  return response


def register(request):
  if 'username' in request.POST and 'email' in request.POST and 'password' in request.POST and 'rpassword' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST:
    try:
      username = request.POST['username']
      password = request.POST['password']
      rpassword = request.POST['rpassword']
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      email = request.POST['email']
      user = ""
      try:
        user = User.objects.get(username=username)
        user2 = User.objects.get(email=email)
        response = redirect("/")
      except:
        if password == rpassword:
          newUser = User(
            userID='2',
            username=username,
            fullname=first_name + ' ' + last_name,
            email=email,
            birtdate='',
            password=password,
            last_join='',
            about='me',
            me_flow='0',
            flow='0'
          )
          newUser.save()
          sendMailRegister(email, first_name)
          response = redirect("/")
        else:
          response = redirect("/")
    except:
      response = redirect("/")
  else:
    response = render(request, 'register.html')
  return response


def forgot_password(request):
  if 'username' in request.POST and 'email' in request.POST:
    try:
      email = request.POST['email']
      username = request.POST['username']
      user = User.objects.get(email=email.strip())
      if username.strip() == user.username:
        locale.setlocale(locale.LC_ALL, 'turkish')
        now = datetime.now()
        tarih = now.strftime("%c")
        characters = string.ascii_letters + string.digits
        password = "".join(choice(characters) for x in range(randint(5, 6)))
        statusMail = sendMailPassword(user.email, user.fullname, password, tarih)
        count = ForgotPassword.objects.all()
        count = len(count)
        status = '0' #0 = forgot
        request.session['status'] = status
        forgotPss = ForgotPassword(
          passwordID=count + 1,
          username=user.username.strip(),
          password=password,
          status=status
        )
        forgotPss.save()
        context = {
          'status': status
        }
        response = render(request, 'code-verification.html', context)
      else:
        context = {
          'status': '2'  # 2 = 0:except
        }
        response = redirect('/', context)
    except:
      context = {
        'status': '2'  # 2 = 0:except
      }
      response = redirect('/', context)
  else:
    context = {
      'status': '0'
    }
    response = render(request, 'forgot-password.html', context)
  return response


def verification(request):
  if 'pass' in request.POST:
    try:
      password = request.POST['pass']
      user = ForgotPassword.objects.get(password=password.strip())
      if user.status == '0':
        myUser = User.objects.get(username=user.username)
        user.status = '1'
        user.save()
        forgotPass = ForgotPassword.objects.get(username=user.username)
        forgotPass.status = '1'
        forgotPass.save()
        request.session['pasStatus'] = '1'
        request.session['pasUser'] = myUser.username
        response = render(request, 'change-password.html')
      else:
        user.status = '3'
        user.save()
        response = redirect("/")
    except:
      context = {
        'status': 'Şifre sıfırlama süresi doldu!'
      }
      response = render(request, 'forgot-password.html', context)
  else:
    try:
      code = request.session['status']
      if code == '0':
        response = render(request, 'code-verification.html')
      else:
        context = {
          'status': '3'
        }
        response = redirect("/", context)
    except:
      context = {
        'status': '3'
      }
      response = redirect("/", context)
  return response


def changePassword(request):
  response = ""
  if 'pass' in request.POST and 'rpass' in request.POST:
    try:
      password = request.POST['pass']
      password2 = request.POST['rpass']
      if password == password2:
        try:
          status = request.session['pasStatus']
          if status == '1':
            request.session['pasStatus'] = '2'
            username = request.session['pasUser']
            request.session['pasUser'] = ''
            user = User.objects.get(username=username)
            user.password = password
            user.save()
            forgotPass = ForgotPassword.objects.get(username=username)
            forgotPass.delete()
            context = {
              'status': 'İşlem başarıyla tamamlandı'
            }
            response = render(request, "login.html", context)
          else:
            writeLog('Change Password', 'Şifre sıfırlama süresi doldu')
            context = {
              'status': 'Şifre sıfırlama süresi doldu!'
            }
            response = redirect('/', context)
        except:
          writeLog('Change Password', 'Şifre sıfırlama işleminde hata oluştu')
          context = {
            'status': 'Şifre sıfırlama işleminde hata oluştu!'
          }
          response = redirect('/', context)
      else:
        writeLog('Change Password', 'Girdiğiniz şifreler uyuşmuyor')
        context = {
          'status': 'Girdiğiniz şifreler uyuşmuyor!'
        }
        response = redirect('/', context)
    except:
      writeLog('Change Password', 'Hata oluştu')
      context = {
        'status': 'Hata oluştu!'
      }
      response = redirect('/', context)
  else:
    writeLog('Change Password', 'Hata oluştu')
    context = {
      'status': 'Hata oluştu!'
    }
    response = redirect('/', context)
  return response


def sendMailPassword(emailAddress, username, password, date):
  try:

    template = render_to_string('password-template.html', {'name': username, 'password': password, 'date': date})
    sendEmail = EmailMessage(
      'forumSözlük Şifre Sıfırlama işleminiz için güvenlik kodu!',
      template,
      settings.EMAIL_HOST_USER,
      [emailAddress],
    )
    sendEmail.fail_silently = False
    sendEmail.send()
    response = redirect('/')
  except:
    response = 'Hata!'
  return response


def sendMailRegister(emailAddress, username):
  try:
    template = render_to_string('register-template.html', {'name': username})
    sendEmail = EmailMessage(
      'forumSözlük Kayıt işleminiz başarıyla tamamlanmıştır!',
      template,
      settings.EMAIL_HOST_USER,
      [emailAddress],
    )
    sendEmail.fail_silently = False
    sendEmail.send()
    response = 'OK'
  except:
    response = 'Hata!'
  return response

def writeLog(procName,procDetail):
  locale.setlocale(locale.LC_ALL, 'turkish')
  now = datetime.now()
  tarih = now.strftime("%c")
  msg = tarih+' - '+procName+': '+procDetail
  logFile = open('logs/log.txt',"r+",encoding="utf-8")
  for item in readLog():
    logFile.write(item)
  logFile.write(''+msg+'\n')
  logFile.close()

def readLog():
  dosya = open("logs/log.txt", "r+",encoding="utf-8")
  dizi = dosya.readlines()
  dosya.close()
  return dizi

def trends(request):
  trend = Post.objects.order_by('-like_count')
  try:
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    context = {
      'is_login': 'true',
      'trends': trend,
      'user': user,
    }
    writeLog('Sayfa görüntülenmesi', 'Trend')
    response = render(request,'trends.html',context)
  except:
    context = {
      'is_login': 'false',
      'trends': trend,
    }
    writeLog('Sayfa görüntülenmesi', 'Trend')
    response = render(request, 'trends.html', context)
  return response

