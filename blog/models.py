# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, UserManager


class TagManager( models.Manager ):
	def most_popular( self ):
		return super( TagManager, self ).annotate( questionCount = models.Count( 'question' ) ).order_by( '-questionCount' )


class Tag( models.Model ):
	caption = models.CharField( null = False, blank = False, max_length = 20 )
	objects = TagManager()


	def __str__( self ):
		return self.caption


	class Meta:
		verbose_name = "Тэг"
		verbose_name_plural = "Тэги"


class QuestionManager( models.Manager ):
	def most_popular( self ):
		return super( QuestionManager, self ).order_by( '-rating' )


	def tagged_as_any( self, *requestedTags ):
		rtList = list( requestedTags )
		return super( QuestionManager, self ).filter( tags__in=rtList ).distinct().order_by( 'rating' )


	def tagged_as_strict( self, *requestedTags ):
		rtList = list( requestedTags )
		result = self.tagged_as_any( *requestedTags )

		for requestedTag in requestedTags:
			result = result.filter( tags__id=requestedTag.id )

		result.order_by( 'rating' )
		return result


class Question( models.Model ):
	caption = models.CharField( null = False, blank = False, max_length = 100 )
	rating = models.IntegerField( default = 0 )
	text = models.TextField( null = False, blank = False )
	tags = models.ManyToManyField( 'Tag' )
	objects = QuestionManager()


	def __str__( self ):
		return self.caption + " " + self.text + ": " + str( self.rating )


	class Meta:
		verbose_name = "Вопрос"
		verbose_name_plural = "Вопросы"


class Answer( models.Model ):
	rating = models.IntegerField( default = 0 )
	text = models.TextField( null = False, blank = False )
	question = models.ForeignKey( 'Question', null = False, blank = False, on_delete = models.CASCADE )


	def __str__( self ):
		return self.text


	class Meta:
		verbose_name = "Ответ"
		verbose_name_plural = "Ответы"


class Profile( models.Model ):
	user = models.OneToOneField( User, null = False, blank = False, on_delete = models.CASCADE )
	image = models.ImageField( max_length = 100 ) #set-default?


	def __str__( self ):
		return self.user.username


	class Meta:
		verbose_name = "Профиль"
		verbose_name_plural = "Профили"
