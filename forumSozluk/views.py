from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django import template
from django.template.loader import render_to_string
import string
from datetime import datetime
import pytz
import locale
from random import *
from .models import Category
from .models import User
from .models import Post
from .models import Like
from .models import ForgotPassword
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic.list import ListView
import os


salt1 = "YhC2s95g8BC9tNC4NSd9yaqi*/|"
salt2 = "|VvnCWbGrW9dcvbE09DfmDaADIf"


def metinSifrele(metin):
  sifreliMetin = salt1+metin+salt2
  gonderilecekMetin = ""
  for i in sifreliMetin:
    gonderilecekMetin += chr(ord(i)+7)
  return gonderilecekMetin


def metinCoz(sifreliMetin):
  gonderilecekMetin = ""
  for i in sifreliMetin:
    gonderilecekMetin += chr(ord(i)-7)
  indexNo = gonderilecekMetin.find('|')
  hash1 = gonderilecekMetin[indexNo]
  yeniMetin = gonderilecekMetin[indexNo+1:len(gonderilecekMetin)]
  indexNo2 = yeniMetin.find('|')
  totalLen = len(yeniMetin[0:yeniMetin.find('|')])
  hash2 = yeniMetin[indexNo2-totalLen:len(yeniMetin)]
  lastMetin = hash2.find('|')
  cozulmusMetin = hash2[indexNo2-totalLen:lastMetin]
  return cozulmusMetin



def index(request):
  userID = ""
  post_list = Post.objects.order_by('-publish_date')
  paginator = Paginator(post_list, 10)
  page = request.GET.get('page', 1)
  category = Category.objects.order_by('-categoryCount')
  try:
    if int(page) > int(paginator.num_pages):
      posts = ""
    else:
      try:
        posts = paginator.page(page)
      except PageNotAnInteger:
        posts = paginator.page(1)
      except EmptyPage:
        posts = paginator.page(paginator.num_pages)
  except:
    return redirect("/")
  trends = Post.objects.order_by('-like_count')
  try:
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    allLikes = Like.objects.order_by('-likeDate').filter(likeAuthor=user.username)
    context = {
      'is_login': 'true',
      'posts': posts,
      'trends': [trends[0], trends[1], trends[2]],
      'user': user,
      'mylikes':allLikes,
      'category':category
    }
    writeLog('Sayfa Görüntülenmesi', 'İndex')
    response = render(request, 'index.html', context)
  except:
    context = {
      'is_login': 'false',
      'posts': posts,
      'trends': [trends[0], trends[1], trends[2]],
      'category': category
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
      cEmail = metinSifrele(email)
      cPassword = metinSifrele(password)
      user = User.objects.get(email=cEmail)
      if cPassword == user.password:
        request.session['userID'] = user.userID
        context = {
          'is_login': 'true',
          'posts': posts,
          'trends': [trend[0], trend[1], trend[2]],
          'user': user,
        }
        response = redirect("/", context)
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
      response = redirect("/", context)
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
    response = redirect("/", context)
  except:
    context = {
      'is_login': 'false',
      'posts': posts,
      'trends': [trend[0], trend[1], trend[2]],
    }
    response = redirect("/", context)
  return response


def profile(request, username):
  try:
    user = User.objects.get(username=username)
    post_list = Post.objects.filter(author=user.username).order_by('-id')
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page', 1)
    try:
      if int(page) > int(paginator.num_pages):
        posts = ""
      else:
        try:
          posts = paginator.page(page)
        except PageNotAnInteger:
          posts = paginator.page(1)
        except EmptyPage:
          posts = paginator.page(paginator.num_pages)
    except:
      return redirect("/")
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
        print("burda")
        is_login = 'true'
        context = {
          'is_login': is_login,
          'posts': posts,
          'myuser': user,
        }
        response = render(request, 'profiles/profile.html', context)
    else:
      is_login = 'false'
      context = {
        'is_login': is_login,
        'posts': posts,
        'myuser': user,
      }
      response = render(request, 'profiles/profile.html', context)
  except:
    print("hata!")
    response = redirect("/")

  return response

from django.core.files.storage import FileSystemStorage


def register(request):
  if 'username' in request.POST and 'email' in request.POST and 'date' in request.POST and 'password' in request.POST and 'rpassword' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST and 'image' in request.FILES:
    try:
      username = request.POST['username']
      password = request.POST['password']
      rpassword = request.POST['rpassword']
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      email = request.POST['email']
      image = request.FILES['image']
      date = request.POST['date']
      fs = FileSystemStorage()
      filename = fs.save("profile/"+username+".jpg", image)

      uploaded_file_url = fs.url(filename)
      print(uploaded_file_url)
      user = ""
      try:
        user = User.objects.get(username=username)
        user2 = User.objects.get(email=email)
        response = redirect("/")
      except:
        count = ""
        try:
          count = User.objects.all()
        except:
          count = 0
        if password == rpassword:
          characters = string.ascii_letters + string.digits
          ID = "".join(choice(characters) for x in range(randint(3, 50)))
          newUser = User(
            userID=ID,
            username=username.lower().strip(),
            photo=uploaded_file_url,
            fullname=first_name + ' ' + last_name,
            email=metinSifrele(email),
            birtdate=date,
            password=metinSifrele(password),
            last_join='',
            about='me',
            me_flow='0',
            flow='0'
          )
          request.session['userID'] = ID
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
    paginator = Paginator(trend, 5)
    page = request.GET.get('sss', 1)
    user = User.objects.get(userID=userID)

    try:
      if int(page) > int(paginator.num_pages):
        trends = ""
        print("bura mı")
      else:
        try:
          trends = paginator.page(page)
          print("burda 1")
        except PageNotAnInteger:
          trends = paginator.page(1)
          print("burda 2")
        except EmptyPage:
          trends = paginator.page(paginator.num_pages)
          print("burda 3")
    except:
      return redirect("/")
    print(trends)
    context = {
      'is_login': 'true',
      'trends': trends,
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


def createPost(request):
  trend = Post.objects.order_by('-like_count')
  if 'content' in request.POST and 'title' in request.POST and 'category' in request.POST:
    try:

      content = request.POST['content']
      title = request.POST['title']
      category = request.POST['category']
      totalPost = Post.objects.all()
      totalLenPost = len(totalPost)+1
      if content !="" and len(content) <= 500 and title !="":
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        now = datetime.now()
        tarih = now.strftime("%c")
        tarih = tarih[0:len(tarih)-3]
        characters = string.ascii_letters + string.digits
        ID = "".join(choice(characters) for x in range(randint(5, 20)))
        try:
          existPost = Post.objects.get(postID=ID)
          ID = "".join(choice(characters) for x in range(randint(5, 25)))
        except:
          pass
        postCreated = Post.objects.create(
          postID=ID,
          postPreview=title,
          category=category,
          content=content,
          author=user.username,
          publish_date=tarih,
          like_count="0"
        )
        postCreated.save()
        if category !="":
          try:
            try:
              existCategory = Category.objects.get(categoryName=category)
              tableTotalCategory = len(Category.objects.all())
              totalCategory = int(existCategory.categoryCount) + 1
              existCategory.categoryCount = totalCategory
              existCategory.save()
              print("vardı güncellendi!")
            except:
              tableTotalCategory = len(Category.objects.all())
              totalCategory = tableTotalCategory + 1
              categoryNew = Category.objects.create(
                categoryID=totalCategory,
                categoryName=category,
                categoryCount="1"
              )
              categoryNew.save()
              print("kategori oluşturuldu!")
          except:
            print("sıkıntılı")
        writeLog('Post Oluşturuldu!', 'Create Post')
      else:
        writeLog('Post Oluşturulamadı!', 'Create Post')
    except:
      writeLog('Post Oluşturulamadı!', 'Create Post')
    response = redirect("/")
  else:
      writeLog('Sayfa yönlendirmesi', 'Create Post')
      response = redirect('/')
  return response

def like(request):
  if 'id' in request.POST:
    try:
      id = request.POST['id'][3:len(request.POST['id'])]
      post = Post.objects.get(postID=id)
      try:
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        try:
          likeExist = Like.objects.get(likeID=id,likeAuthor=user.username)
          print("bulundu")
          postTotal = post.like_count
          post.like_count = int(postTotal) - 1
          post.save()
          likeExist.delete()
          print("Oldu gibi :D")
        except:
          postTotal = post.like_count
          post.like_count = int(postTotal) + 1
          post.save()
          now = datetime.now()
          tarih = now.strftime("%c")
          tarih = tarih[0:len(tarih) - 3]
          newLike = Like(likeID=post.postID,postAuthor=post.author,likeAuthor=user.username,likeDate=tarih)
          newLike.save()
      except:
        pass
    except:
      pass
  else:
    pass
  return redirect("/")


def details(request,postID):
  userID = ""
  trends = Post.objects.order_by('-like_count')
  category = Category.objects.order_by('-categoryCount')
  try:
    onePost = Post.objects.get(postID=postID)
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    allLikes = Like.objects.order_by('-likeDate').filter(likeAuthor=user.username)
    context = {
      'is_login': 'true',
      'posts': [onePost],
      'trends': [trends[0], trends[1], trends[2]],
      'user': user,
      'mylikes': allLikes,
      'category':category,
    }
    writeLog('Sayfa Görüntülenmesi', 'details')
    response = render(request, 'details.html', context)
  except:
    try:
      onePost = Post.objects.get(postID=postID)
      context = {
        'is_login': 'false',
        'posts': [onePost],
        'trends': [trends[0], trends[1], trends[2]],
        'category': category,
      }
      writeLog('Sayfa Görüntülenmesi', 'details')
      response = render(request, 'details.html', context)
    except:
      response = redirect("/")
  return response




#Settings
def mysettings(request,username):
  try:
    user = User.objects.get(username=username)
    userID = request.session['userID']
    if user.userID == userID:
      mEmail = metinCoz(user.email)
      mPassword = metinCoz(user.password)
      context = {
        'is_login': 'true',
        'user': user,
        'set':'true',
        'mEmail':mEmail,
        'mPassword':mPassword,
      }
      response = render(request, 'settings.html', context)
    else:
      response = redirect("/")
  except:
    response = redirect("/")
  return response

from django.http import JsonResponse
from django.core import serializers

def nameChange(request):
  try:

    print("giriyor")
    currentName = request.POST['currentName']
    print("giriyor 2")

    newName = request.POST['newName']
    print("giriyor 3")

    password = request.POST['password']
    sifreliPassword = metinSifrele(password)
    user = User.objects.get(username=currentName)
    print("user bulundu")
    if user.password == sifreliPassword:
      print("şifreler eşleşti")
      try:
        user2 = User.objects.get(username=newName)
        print("yeni username de kullanıcı bulundu")
        response = redirect("/")
      except:
        oldname = user.username
        user.username = newName
        print("kullanıcı adı güncelleniyor")
        user.save()
        print("kullanıcı adı güncellendi")
        os.rename('C:\\Users\\efetemel\\Desktop\\forumApp\media\\profile\\'+oldname+'.jpg', 'C:\\Users\\efetemel\\Desktop\\forumApp\media\\profile\\'+user.username+'.jpg')
        try:
          print("giriyor")
          print(oldname)
          post = Post.objects.get(author=oldname)
          print("buldu")
          post.author = user.username
          print("eşitledi")
          post.save()
          print("kaydetti")
        except:
          print("burraa")
          try:
            print(oldname)
            posts = Post.objects.filter(author=oldname)
            print("girdi")
            for post in posts:
              print(post.author+" old")
              post.author = user.username
              print(post.author +" new")
              post.save()
          except:
            pass
        try:
          like = Like.objects.get(likeAuthor=oldname)
          like.likeAuthor = user.username
          like.save()
        except:
          pass
        try:
          like = Like.objects.get(postAuthor=oldname)
          like.postAuthor = user.username
          like.save()
        except:
          pass
        response = JsonResponse({'username': user.username},status=200)
    else:
      print("bura mı?")
      response = JsonResponse({'username': ""}, status=400)
  except:
    print("user bulunamadı")
    response = JsonResponse({'username': ""},status=400)
  return response

def fullnamechange(request):
  currentFullName = request.POST['currentFullName']
  newFirstName = request.POST['newFirstName']
  newLastName = request.POST['newLastName']
  password = request.POST['fullPassword']
  sifreliPassword = metinSifrele(password)
  print("bilgiler alındı giriyor")
  try:
    user = User.objects.get(fullname=currentFullName)
    print("user çekildi")
    if user.password == sifreliPassword:
      print("pass doğrulandı")
      fullName = newFirstName +" "+newLastName
      print("name ler birleştiridi")
      user.fullname = fullName.title()
      print("eşitlendi")
      user.save()
      print("savelendi")
      response = JsonResponse({'fullname': user.fullname},status=200)
    else:
      response = JsonResponse({'fullname': ""},status=400)
  except:
    response = JsonResponse({'fullname': ""},status=400)
  return response


def emailchange(request):
  currentEmail = request.POST['currentEmail']
  newEmail = request.POST['newEmail']
  password = request.POST['emailPassword']
  sifreliCurrentEmail = metinSifrele(currentEmail)
  sifreliNewEmail = metinSifrele(newEmail)
  sifreliPassword = metinSifrele(password)
  print("bilgiler alındı giriyor")
  print(currentEmail)
  try:
    user = User.objects.get(email=sifreliCurrentEmail)
    print("user çekildi")
    if user.password == sifreliPassword:
      try:
        print("yeni epostada user varmı bakılıyor")
        user2 = User.objects.get(email=sifreliNewEmail)
        print("bulundu!")
      except:
        user.email = newEmail
        user.save()
        print("bilgiler kaydedildi")
      response = JsonResponse({'email':sifreliNewEmail},status=200)
    else:
      response = JsonResponse({'email': ""},status=400)
  except:
    response = JsonResponse({'email': ""},status=400)
  return response


def passwordchange(request):
  currentEmailPassword = request.POST['currentEmailPassword']
  currentPassword = request.POST['currentPassword']
  newPassword = request.POST['newPassword']
  sifreliEmail = metinSifrele(currentEmailPassword)
  sifreliCurrentPassword = metinSifrele(currentPassword)
  sifreliNewPassword = metinSifrele(newPassword)
  print("bilgiler alındı giriyor")
  try:
    user = User.objects.get(email=sifreliEmail)
    print("user çekildi")
    if user.password == sifreliCurrentPassword:
      user.password = sifreliNewPassword
      user.save()
      print("bilgiler kaydedildi")
      response = JsonResponse({'password':sifreliNewPassword}, status=200)
    else:
      response = JsonResponse({'email': ""},status=400)
  except:
    response = JsonResponse({'email': ""},status=400)
  return response


def categories(request):

  try:
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    category = Category.objects.order_by('-categoryCount')
    context = {
      'is_login': 'true',
      'user': user,
      'category': category
    }
    response = render(request, "categories.html",context)
  except:
    context = {
      'is_login': 'false',
      'category': category
    }
    response = render(request, "categories.html", context)
  return response

def selectcategory(request,category):
  try:
    print("1")
    existCategory = Category.objects.get(categoryName=category)
    print("2")
    print(existCategory.categoryName)
    existPost = Post.objects.filter(category=existCategory.categoryName)
    print("3")
    trends = Post.objects.order_by('-like_count')
    try:
      userID = request.session['userID']
      user = User.objects.get(userID=userID)
      context = {
        'posts': existPost,
        'is_login': 'true',
        'categoryName':category,
        'trends': [trends[0], trends[1], trends[2]],
      }
    except:
      context = {
        'posts':existPost,
        'is_login': 'false',
        'categoryName': category,
        'trends': [trends[0], trends[1], trends[2]],
      }
    return render(request,"selectcategory.html",context)
  except:
    return redirect("/")

def search(request):
  if 'term' in request.GET:
    searchText = request.GET.get('term')
    searchPost = User.objects.filter(username__icontains=searchText)
    titles = list()
    for post in searchPost:
      titles.append(post.username)
    return JsonResponse(titles,safe=False)
  else:
    return redirect("/")