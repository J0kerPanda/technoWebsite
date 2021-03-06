from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse, Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST

from blog.models import Tag, Question, Answer, Profile, Vote

import blog_forms as blogForms
import json
import requests

def makeBase( request ):

	result = { 
		'hotTags': cache.get( 'popular_tags' ),
		'bestMembers': cache.get( 'best_members' ),
	}

	if ( request.user.is_authenticated ):
		result[ 'profile' ] = Profile.objects.get_by_login( request.user.username )

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
	currentQuestion = get_object_or_404( Question, id = questionID )

	if ( request.method == 'POST' ):
		form = blogForms.AnswerForm( request.POST )

		if ( not request.user.is_authenticated ):
			form.add_error( None, 'You must be logged in to post answers' )
		
		if ( form.is_valid() ):
			newAnswer = form.save( currentQuestion, Profile.objects.get_by_login( request.user.username ) )
			anchor = '#answer' + str( newAnswer.id )
			response = requests.post( 'http://asksemenov.com/publish-answers/',
				params = { 'cid' : 5 },
				data = json.dumps( { 'answer': render_to_string( 'singleanswer.html', { 'answer': newAnswer } ) } )
				)
			anchor = '#answer' + str( newAnswer.id )
			return HttpResponseRedirect( '/question/' + questionID + '/' + anchor )

	else:
		form = blogForms.AnswerForm()

	result = makeBase( request )
	result[ 'form' ] = form
	result[ 'question' ] = currentQuestion
	return render( request, 'answer.html', result )
	

def siteLogin( request ):
	redirectURL = '/'
	if ( request.GET.get( 'continue' ) ):
		redirectURL = request.GET.get( 'continue', '/' )

	if ( request.user.is_authenticated ):
		return HttpResponseRedirect( redirectURL )

	if ( request.method == 'POST' ):
		form = blogForms.LoginForm( request.POST )

		if ( form.is_valid() ):
			username = form.cleaned_data[ 'login' ]
			password = form.cleaned_data[ 'password' ]
			user = authenticate( username = username, password = password )

			if user is not None:
				login( request, user )
				return HttpResponseRedirect( redirectURL )

			form.add_error( None, 'Invalid login/password')

	else:
		form = blogForms.LoginForm()

	result = makeBase( request )
	result[ 'form' ] = form
	return render( request, 'login.html', result )


def signup( request ):
	if ( request.user.is_authenticated ):
		return HttpResponseRedirect( '/' )

	if ( request.method == 'POST' ):
		form = blogForms.NewUserForm( request.POST, request.FILES )
		
		if ( form.is_valid() ):
			form.save()
			username = form.cleaned_data[ 'login' ]
			password = form.cleaned_data[ 'password' ]
			user = authenticate( username = username, password = password )
			login( request, user )
			return HttpResponseRedirect( '/' )

	else:
		form = blogForms.NewUserForm()

	result = makeBase( request )
	result[ 'form' ] = form
	return render( request, 'signup.html', result )


@login_required( redirect_field_name='continue' )
def ask( request ):

	if ( request.method == 'POST' ):
		form = blogForms.AskForm( request.POST )
		
		if ( form.is_valid() ):
			newQuestion = form.save( Profile.objects.get_by_login( request.user.username ) )
			return HttpResponseRedirect( '/question/' + str( newQuestion.id ) + '/' )

	else:
		form = blogForms.AskForm()

	result = makeBase( request )
	result[ 'form' ] = form
	return render( request, 'ask.html', result )


@login_required( redirect_field_name='continue' )
def settings( request ):

	if ( request.method == 'POST' ):
		form = blogForms.ChangeSettingsForm( request.POST, request.FILES )

		if ( form.is_valid() ):

			if ( not request.user.check_password( form.cleaned_data[ 'password' ] ) ):
				form.add_error( 'password', 'Incorrect password' )

			else:
				form.save( Profile.objects.get_by_login( request.user.username ) )
				form = blogForms.ChangeSettingsForm()

	else:
		form = blogForms.ChangeSettingsForm()

	result = makeBase( request )
	result[ 'form' ] = form
	return render( request, 'settings.html', result )


def siteLogout( request ):
	redirectURL = '/'
	if( request.META.get( 'HTTP_REFERER' ) ):
		redirectURL = request.META.get( 'HTTP_REFERER', '/' )

	if ( request.user.is_authenticated ):
		logout( request )
		return HttpResponseRedirect( redirectURL )

	return HttpResponseRedirect( redirectURL )


def votes( request ):
	data = {}

	try:

		if ( request.user.is_authenticated ):

			if ( request.method == 'GET' ):
				objectID = request.GET[ 'object_id' ]
				objectType = request.GET[ 'object_type' ]

			elif ( request.method == 'POST' ):
				objectID = request.POST[ 'object_id' ]
				objectType = request.POST[ 'object_type' ]

			else:
				raise Exception( '405' )

			if ( objectType == 'question' ):
				objectType = ContentType.objects.get( model = 'question' )
				voteObject = Question.objects.get( id = objectID )

			elif ( objectType == 'answer' ):
				objectType = ContentType.objects.get( model = 'answer' )
				voteObject = Answer.objects.get( id = objectID )

			else:
				raise Exception( '400' )

			profile = Profile.objects.get_by_login( request.user.username )

			if ( Vote.objects.filter( profile = profile, related_type = objectType, related_id = voteObject.id ) ):
				raise Exception( '500' )

			if ( request.method == 'POST' ):
				voteType = request.POST.get( 'vote_type' )

				if ( voteType == 'like' ):
					voteType = True

				elif ( voteType == 'dislike' ):
					voteType = False

				else:
					raise Exception( '400' )

				newVote = Vote.objects.create( profile = profile, is_positive = voteType, related_object = voteObject )
				voteObject.refresh_from_db()
				data[ 'new_rating' ] = voteObject.rating

		else:
			data[ 'error' ] = '403';

	except ( ObjectDoesNotExist, KeyError ) as err:
		data[ 'error' ] = '404';

	except Exception as err:
		data[ 'error' ] = str( err )

	finally:

		if not data.get( 'error' ):
			data[ 'error' ] = '200';

		return JsonResponse( data )

def correct( request ):
	data = {}

	try:

		if ( request.user.is_authenticated ):

			if ( request.method == 'GET' ):
				questionID = request.GET[ 'question_id' ]

			elif ( request.method == 'POST' ):
				questionID = request.POST[ 'question_id' ]

			else:
				raise Exception( '400' )

			question = Question.objects.get( id = questionID )
			profile = Profile.objects.get_by_login( request.user.username )

			if ( question.author == profile ):

				if ( request.method == 'POST' ):
					answer = Answer.objects.get( id = request.POST[ 'answer_id' ] )
					answer.correct = not answer.correct
					answer.save()

			else:
				raise Exception( '500' )

		else:
			data[ 'error' ] = '403';

	except ( ObjectDoesNotExist, KeyError ) as err:
		data[ 'error' ] = '404';

	except Exception as err:
		data[ 'error' ] = str( err )

	finally:
		if not data.get( 'error' ):
			data[ 'error' ] = '200';

		return JsonResponse( data )
			



			









	



	


