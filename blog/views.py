from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpRequest

from django.http import Http404

class User:

	def __init__( self, name, loginStatus ):
		self.name = name;
		self.loggedIn = loginStatus

def mainPage( request ):

	hotTags = []
	bestMembers = []

	for i in range( 10 ):
		hotTags.append( str( i ) )

	for i in range( 10 ):
		bestMembers.append( str( i ) );
	
	return render( request, 'base.html', {

		'user': User( 'Antony', True ),
		'hotTags': hotTags,
		'bestMembers': bestMembers,
		})

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






	


