from django.http import HttpResponse

def here(request):
	return HttpResponse('<p>hey there kiddo!')