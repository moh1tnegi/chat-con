from django.shortcuts import render
from .forms import ContactForm
# from . import models
import logging

logging.basicConfig(filename='/home/mohit/Documents/git_repos/Chatting_web_app/log.txt', level=logging.DEBUG, filemode='w')
logger = logging.getLogger()
logger.debug('#logging starts!')


def login_auth(*args):
    pass

def registration(**kwargs):
    pass

def dashboard(request):
    logger.debug("inside dashboard")
    context = {'flag': 1}

    if request.method == 'POST':
        logger.debug("bkl")
        uname = request.POST['uname']
        context = {'uname': uname, 'flag': 0}

        passwd = request.POST['passwd']
        phnum = request.POST.get('phnum', 0)

        if phnum:
            #  sign up in progress
            fname = request.POST.get('fname', 0)
            lname = request.POST.get('lname', 0)
            email = request.POST.get('email', 0)
            auth = registration({'fname':fname, 'lname':lname, 'uname':uname, 'passwd':passwd, 'phnum':phnum})
        else:
            auth = login_auth((uname, passwd))

        if auth:
            # start session
            pass
        else:
            # resend authentication
            pass

    return render(request, 'interface/index.html', context)


def login_form(request):
    return render(request, 'interface/login.html')


def signup_form(request):
    return render(request, 'interface/signup.html')


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'interface/contact.html', {'form': form})
