from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpRequest

from django.http import Http404

import re
header_regexp = re.compile( r'^(HTTP_.+$|CONTENT_TYPE|CONTENT_LENGTH)$' )

def helloWorld( request ):
	
	try:

		data = "This is brand new hello world!\n"

		for key in request.GET.keys():
			data += ( str( key ) + ": " + str( request.GET.get( key ) ) + '\n' )

		for key in request.POST.keys():
			data += ( str( key ) + ": " + str( request.POST.get( key ) ) + '\n' )
			

		for key in request.META.keys():

			if ( header_regexp.match( key ) and request.META.get( key ) ):

				data += ( str( key ) + ": " + str( request.META.get( key ) ) + '\n' )
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')

def mainPage( request ):

	try:

		data = "mainPage here!\n"
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')

def hotQuestions( request ):

	try:

		data = "HotQuestions here!\n"
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')


def hotQuestions( request ):

	try:

		data = "HotQuestions here!\n"
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')

def taggedQuestions( request, tag=None ):

	try:

		data = "taggedQuestions here!\n" + str( tag ) + '\n'
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')

def singleQuestion( request, questionID=None ):

	try:

		data = "singleQuestion here!\n" + str( questionID ) + '\n'
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')

def login( request ):

	try:

		data = "login here!\n"
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')

def signup( request ):

	try:

		data = "signup here!\n"
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')

def ask( request ):

	try:

		data = "makeQuestion here!\n"
		
		return HttpResponse( data, content_type='text/plain' )

	except:
		raise Http404('Something went horribly wrong')






	


