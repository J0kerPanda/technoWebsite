from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import Http404

from django.contrib.auth.models import User
from blog.models import Tag, Question, Answer, Profile, Vote

import blog_forms as blogForms

def makeBase( request ):

	result = { 
		'hotTags': Tag.objects.rating_sorted()[:10],
		'bestMembers': Profile.objects.rating_sorted()[:10],
	}

	if ( request.user.is_authenticated ):
		result[ 'profile' ] = Profile.objects.get_by_username( '123' )

	else:
		result[ 'profile' ] = None

	return result
		


def Paginate( request, container, perPage ):
	paginator = Paginator( container, perPage )
	pageNumber = request.GET.get( 'page' ) #gets page from get parameters

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
	result = makeBase( request );
	questions = Question.objects.date_sorted()
	result[ 'questions' ], result[ 'pageNumbers' ] = Paginate( request, questions, 5 )
	return render( request, 'index.html', result )
	


def hotQuestions( request ):
	result = makeBase( request )
	questions = Question.objects.rating_sorted()
	result[ 'questions' ], result[ 'pageNumbers' ] = Paginate( request, questions, 5 )
	return render( request, 'hotquestions.html', result )


def taggedQuestions( request, tag=None ):
	result = makeBase( request );
	questions = Question.objects.tagged_as_strict( tag )
	result[ 'questions' ], result[ 'pageNumbers' ] = Paginate( request, questions, 5 )
	result[ 'tag' ] = tag
	return render( request, 'questiontags.html', result )


def answer( request, questionID=None ):
	result = makeBase( request )
	result[ 'question' ] = get_object_or_404( Question, id = questionID )
	return render( request, 'answer.html', result )
	

def login( request ):
	result = makeBase( request )

	if ( request.method == 'POST' ):

		form = blogForms.LoginForm( request.POST )

	else:

		form = blogForms.LoginForm()

	result[ 'form' ] = form
	return render( request, 'login.html', result )


def signup( request ):
	result = makeBase( request )

	if ( request.method == 'POST' ):

		form = blogForms.NewUserForm( request.POST, request.FILES )
		
		if ( form.is_valid() ):

			newUser = User.objects.create( 
			username = form.cleaned_data[ 'login' ], 
			email = form.cleaned_data[ 'email' ],
			password = form.cleaned_data[ 'password' ] )
			newUser.save()
			newProfile = Profile.objects.create( 
				user = newUser, 
				rating = 0 )

			if ( form.cleaned_data[ 'avatar' ] ):
				newProfile.image = form.cleaned_data[ 'avatar' ]
			newProfile.save()

			return HttpResponseRedirect( '/' )

	else:

		form = blogForms.NewUserForm()

	result[ 'form' ] = form
	return render( request, 'signup.html', result )


def ask( request ):
	result = makeBase( request )
	return render( request, 'ask.html', result )

def settings( request ):
	result = makeBase( request )

	if ( request.method == 'POST' ):

		form = blogForms.ChangeSettingsForm( request.POST, request.FILES )

	else:

		form = blogForms.ChangeSettingsForm()

	result[ 'form' ] = form
	return render( request, 'settings.html', result )

def logout( request ):

	if ( request.user.is_authenticated ):

		return HttpResponseRedirect( '/' )

	return HttpResponseRedirect( '/' )
	






	


