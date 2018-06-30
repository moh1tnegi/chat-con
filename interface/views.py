from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.safestring import mark_safe

from .forms import ContactForm
from . import models
from .phNumVeriVald import legit_ph_num

import json
import re
import logging

logging.basicConfig(filename='/home/mohit/Documents/git_repos/Chatting_web_app/log.txt',
                    level=logging.DEBUG,
                    filemode='w')
logger = logging.getLogger()
logger.debug('#logging starts!')
sentinel = 1  # is it login or signup request?


def login_auth(*args):
    try:
        models.User.objects.get(pk=args[0])
        pas = models.User.objects.filter(pk=args[0], password=args[1])
        return 1 if pas else 0
    except ObjectDoesNotExist:
        return 0


def registration(**kwargs):
    unm = kwargs.get('uname', 0)
    pwd = kwargs.get('passwd', 0)
    pnm = kwargs.get('phnum', 0)

    if unm and pwd and pnm and legit_ph_num(pnm):
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
            user.save()
        except IntegrityError:
            yield from(0, {'error': "Phone number already exist!"})
            return
        yield from(1, 0)

    else:
        yield from (0, 0)


def dashboard(request):
    try:
        uname = models.User.objects.get(pk=request.session.get('username', 'mohit_negi'))
        models.User.objects.get(username__exact=uname, password__exact=request.session.get('usr_pass', 0))
        request.session['session_up'] = True
        return render(request, 'interface/index.html', {
            'user_session': uname, 
            'contacts': ['Mohit', ]
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
            return render(request, 'interface/index.html', {'user_session': uname})

        else:
            # resend form
            if not sentinel:
                error = {'error': 'Wrong username or password!'}
                return render(request, 'interface/login.html', error)
            else:
                if not error:
                    error = {'error': 'Fields with (*) are mandatory!'}
                return render(request, 'interface/signup.html', error)
    return render(request, 'interface/index.html')


def login_form(request):
    if request.session.get('session_up', 0):
        return redirect('http://127.0.0.1:8000')
    global sentinel
    sentinel = 0
    return render(request, 'interface/login.html')


def signup_form(request):
    if request.session.get('session_up', 0):
        return redirect('http://127.0.0.1:8000')
    global sentinel
    sentinel = 1
    return render(request, 'interface/signup.html')


def log_out(request):
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
    return render(request, 'interface/contact.html', {'form': form})
