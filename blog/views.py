from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpRequest

from django.http import Http404

class User:

	def __init__( self, name, loginStatus ):
		self.name = name
		self.loggedIn = loginStatus

class Question:

	def __init__( self, caption, text, answersCount ):
		self.caption = caption
		self.rating = 5
		self.text = text
		self.tags = [ str( caption ), str( caption ), str( caption ) ]
		self.answersCount = answersCount

def mainPage( request ):

	try:

		hotTags = []
		bestMembers = []
		questions = []

		for i in range( 10 ):
			hotTags.append( str( i ) )

		for i in range( 10 ):
			bestMembers.append( str( i ) )

		for i in range( 10 ):
			questions.append( Question( str( i ), ( str( i ) + " " ) * 200 , i ) )
		
		return render( request, 'index.html', {

			'user': User( 'Antony', False ),
			'questions': questions,
			'hotTags': hotTags,
			'bestMembers': bestMembers,
			})
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

		hotTags = []
		bestMembers = []
		questions = []

		for i in range( 10 ):
			hotTags.append( str( i ) )

		for i in range( 10 ):
			bestMembers.append( str( i ) )

		for i in range( 10 ):
			questions.append( Question( str( i ), ( str( i ) + " " ) * 200 , i ) )
		
		return render( request, 'questiontags.html', {

			'user': User( 'Antony', False ),
			'questions': questions,
			'hotTags': hotTags,
			'bestMembers': bestMembers,
			'tag': tag,
			})

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






	


