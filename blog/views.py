from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpRequest

# Create your views here.

def helloWorld( request ):
	try:
		
		return HttpResponse( 'hello world\n', content_type='text/plain' )

	except:
		raise Http404

	


