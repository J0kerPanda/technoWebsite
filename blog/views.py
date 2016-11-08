from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
		self.id = int( caption )
		self.caption = caption
		self.rating = 5
		self.text = text
		self.tags = [ str( caption ), str( caption ), str( caption ) ]
		self.answersCount = answersCount

class Answer:

	def __init__( self, caption, text ):
		self.caption = caption
		self.rating = 10
		self.text = text

def makeBase():

	hotTags = []
	bestMembers = []

	for i in range( 10 ):
			hotTags.append( str( i ) )

	for i in range( 10 ):
		bestMembers.append( str( i ) )

	return {

		'user': User( 'Antony', False ),
		'hotTags': hotTags,
		'bestMembers': bestMembers,
	}

def Paginate( request, container, pageCount ):

	paginator = Paginator( container, pageCount )

	pageNumber = request.GET.get( 'page' )

	try:
		page = paginator.page( pageNumber )

	except PageNotAnInteger:
		page = paginator.page( 1 )

	except EmptyPage:
		page = paginator.page( paginator.num_pages )

	pageNumbers = []

	for i in range( -2, 3 ):
		if ( page.number + i ) in paginator.page_range:
			pageNumbers.append( page.number + i )

	return page, pageNumbers


def mainPage( request ):

	result = makeBase();
	
	questions = []

	for i in range( 40 ):
		questions.append( Question( str( i ), ( str( i ) + " " ) * 200 , i ) )

	result[ 'questions' ], result[ 'pageNumbers' ] = Paginate( request, questions, 5 )
	
	return render( request, 'index.html', result )

def hotQuestions( request ):

	try:

		result = makeBase();
		
		questions = []

		for i in range( 40 ):
			questions.append( Question( str( i ), ( str( i ) + " " ) * 200 , i ) )

		result[ 'questions' ], result[ 'pageNumbers' ] = Paginate( request, questions, 5 )
		
		return render( request, 'hotquestions.html', result )
	except:
		raise Http404('Something went horribly wrong')

def taggedQuestions( request, tag=None ):

	try:

		result = makeBase();
		
		questions = []

		for i in range( 40 ):
			questions.append( Question( str( i ), ( str( i ) + " " ) * 200 , i ) )

		result[ 'questions' ], result[ 'pageNumbers' ] = Paginate( request, questions, 5 )
		result[ 'tag' ] = tag
		
		return render( request, 'questiontags.html', result )
	except:
		raise Http404('Something went horribly wrong')

def answer( request, questionID=None ):

	try:
		result = makeBase()
		
		answers = []

		for i in range( 10 ):
			answers.append( Answer( str( i ), ( str( i ) + " " ) * 150 ) )

		question = Question( str( questionID ), 'a ' * 200, 0 )
		question.tags = [ 'Work', 'on', 'this' ]

		result[ 'answers' ] = answers
		result[ 'question' ] = question

		return render( request, 'answer.html', result )
	except:
		raise Http404('Something went horribly wrong')
	
def login( request ):

	try:

		result = makeBase()
		
		return render( request, 'login.html', result )
	except:
		raise Http404('Something went horribly wrong')

def signup( request ):

	try:

		result = makeBase()
		
		return render( request, 'signup.html', result )
	except:
		raise Http404('Something went horribly wrong')

def ask( request ):

	try:

		result = makeBase()
		
		return render( request, 'ask.html', result )
	except:
		raise Http404('Something went horribly wrong')






	


