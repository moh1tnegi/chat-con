from django.shortcuts import render
from .forms import ContactForm
# from . import models
import logging

logging.basicConfig(filename='log.txt', level=logging.DEBUG, filemode='w')
logger = logging.getLogger()
logger.debug('#logging starts!')


def dashboard(request):
    logger.debug("inside dashboard")
    context = {'flag': 1}
    if request.method == 'POST':
        logger.debug("bkl")
        uname = request.POST['uname']
        # passwd = request.POST['passwd']
        if request.POST.get('phn_num', 0):
            #  sign up in progress
            if request.POST.get('email', 0):
                context['email'] = request.POST['email']
        context = {'uname': uname}
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
