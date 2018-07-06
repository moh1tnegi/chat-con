from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .forms import ContactForm
from . import models

import json
import re
# import logging

# logging.basicConfig(filename='/home/mohit/Documents/git_repos/chat-con/debug.log',
#                     level=logging.DEBUG,
#                     filemode='w')
# logger = logging.getLogger()
# logger.debug('#logging starts!')
sentinel = 1  # is it login or signup request?


def login_auth(*args):
    try:
        user = models.User.objects.get(pk=args[0])
        pas = models.User.objects.filter(pk=args[0], password=args[1])
        if pas:
            user.is_online = True
            user.save()
            return 1
        else: return 0
    except ObjectDoesNotExist:
        return 0


def registration(**kwargs):
    unm = kwargs.get('uname', 0)
    pwd = kwargs.get('passwd', 0)
    pnm = kwargs.get('phnum', 0)

    if unm and pwd and pnm:
        try:
            models.User.objects.get(pk=unm)
            yield from (0, {'error': "Username already taken!"})
            return
        except ObjectDoesNotExist:
            pass

        if not re.match(r'^\d{9}\d$', pnm):
            yield from (0, {'error': "Enter a valid phone number!"})
            return

        try:
            user = models.User()
            user.firstname = kwargs.get('fname', 0)
            user.lastname = kwargs.get('lname', 0)
            user.username = unm
            user.password = pwd
            user.phn_numb = pnm
            user.is_online = True
            user.save()
        except IntegrityError:
            yield from(0, {'error': "Phone number already exist!"})
            return
        yield from(1, 0)

    else:
        yield from (0, 0)


def dashboard(request):
    _users_ = models.User.objects.filter(is_online__exact=True)
    online_users = []

    for usr in _users_:
        online_users.append(usr.username + ' - (' + usr.firstname + ' ' + usr.lastname + ')')

    try:
        uname = models.User.objects.get(username__exact=request.session.get('username'), password__exact=request.session.get('usr_pass', 0))
        uname.is_online = True
        uname.save()
        return render(request, 'chat/index.html', {
            'user_session': uname,
            'full_name': uname.firstname + ' ' + uname.lastname,
            'online': online_users,
            })
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        uname = request.POST['uname']
        passwd = request.POST['passwd']
        phnum = request.POST.get('phnum', 0)
        error = ''

        if sentinel:
            #  sign up in progress
            fname = request.POST.get('fname', 0)
            lname = request.POST.get('lname', 0)
            auth, error = registration(fname=fname, lname=lname, uname=uname, passwd=passwd, phnum=phnum)
        else:
            # login in progress
            auth = login_auth(uname, passwd)

        if auth:
            # start session
            request.session['username'] = uname
            request.session['usr_pass'] = passwd
            request.session['session_up'] = True
            U = models.User.objects.get(pk=uname)
            return render(request, 'chat/index.html', {
                'user_session': uname,
                'full_name': U.firstname + ' ' + U.lastname,
                'online': online_users,
            })

        else:
            # resend form
            if not sentinel:
                error = {'error': 'Wrong username or password!'}
                return render(request, 'chat/login.html', error)
            else:
                if not error:
                    error = {'error': 'Fields with (*) are mandatory!'}
                return render(request, 'chat/signup.html', error)
    return render(request, 'chat/index.html')


def login_form(request):
    if request.session.get('session_up', 0):
        return redirect('http://127.0.0.1:8000')
    global sentinel
    sentinel = 0
    return render(request, 'chat/login.html')


def signup_form(request):
    if request.session.get('session_up', 0):
        return redirect('http://127.0.0.1:8000')
    global sentinel
    sentinel = 1
    return render(request, 'chat/signup.html')


def log_out(request):
    u = models.User.objects.get(username__exact=request.session['username'])
    u.is_online = False
    u.save()
    del request.session['username']
    del request.session['usr_pass']
    request.session['session_up'] = False
    return redirect('http://127.0.0.1:8000')


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'chat/contact.html', {'form': form, 'user_session': request.session.get('username', 0)})
