# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime


class TagManager( models.Manager ):
	def rating_sorted( self ):
		return super( TagManager, self ).annotate( questionCount = models.Count( 'question' ) ).order_by( '-questionCount' )


class Tag( models.Model ):
	caption = models.CharField( unique = True, null = False, blank = False, max_length = 20 )
	objects = TagManager()


	def __str__( self ):
		return str( self.caption )


	class Meta:
		verbose_name = "Тэг"
		verbose_name_plural = "Тэги"


class QuestionManager( models.Manager ):
	def rating_sorted( self ):
		return super( QuestionManager, self ).order_by( '-rating', '-postDate' )


	def date_sorted( self ):
		return super( QuestionManager, self ).order_by( '-postDate', '-rating' )


	def tagged_as_any( self, *requestedTags ):
		rtList = list( requestedTags )
		return super( QuestionManager, self ).filter( tags__caption__in = rtList ).distinct().order_by( '-rating' )


	def tagged_as_strict( self, *requestedTags ):
		rtList = list( requestedTags )
		result = self.tagged_as_any( *requestedTags )

		for requestedTag in requestedTags:
			result = result.filter( tags__caption = requestedTag )

		result.order_by( '-rating' )
		return result


class Question( models.Model ):
	caption = models.CharField( null = False, blank = False, max_length = 100 )
	rating = models.IntegerField( null = False, default = 0 )
	text = models.TextField( null = False, blank = False )
	tags = models.ManyToManyField( 'Tag' )
	postDate = models.DateTimeField( null = False, blank = True, auto_now_add = True )
	author = models.ForeignKey( 'Profile', null = False, blank = False, on_delete = models.CASCADE )
	objects = QuestionManager()


	def answersList( self ):
		return self.answer_set.order_by( '-correct', '-rating' )


	def answersCount( self ):
		return self.answer_set.count()


	def __str__( self ):
		return str( self.author ) + ": " + str( self.caption ) + ", " + str( self.rating )


	class Meta:
		verbose_name = "Вопрос"
		verbose_name_plural = "Вопросы"


class Answer( models.Model ):
	rating = models.IntegerField( null = False, default = 0 )
	text = models.TextField( null = False, blank = False )
	correct = models.BooleanField( null = False, blank = False, default = False )
	question = models.ForeignKey( 'Question', null = False, blank = False, on_delete = models.CASCADE )
	author = models.ForeignKey( 'Profile', null = False, blank = False, on_delete = models.CASCADE )


	def __str__( self ):
		return str( self.question ) + ": " + str( self.text )[:10] + "..., " + str( self.rating )

	class Meta:
		verbose_name = "Ответ"
		verbose_name_plural = "Ответы"


class ProfileManager( models.Manager ):
	def rating_sorted( self ):
		return super( ProfileManager, self ).order_by( '-rating' )


	def get_by_username( self, name ):
		return super( ProfileManager, self ).get( user__username=name )


class Profile( models.Model ):
	user = models.OneToOneField( User, null = False, blank = False, on_delete = models.CASCADE )
	image = models.ImageField( null = True, blank = True, max_length = 100 )
	rating = models.IntegerField( null = False, default = 0 )
	objects = ProfileManager()


	def username( self ):
		return str( self.user.username )


	def __str__( self ):
		return self.username()


	class Meta:
		verbose_name = "Профиль"
		verbose_name_plural = "Профили"


class Vote( models.Model ):
	profile = models.ForeignKey( 'Profile', null = False, blank = False, on_delete = models.CASCADE )
	is_positive = models.BooleanField( null = False, blank = False, default = True )
	related_type = models.ForeignKey( ContentType )
	related_id = models.PositiveIntegerField( null = False )
	related_object = GenericForeignKey( 'related_type', 'related_id' )


	def __str__( self ):
		return str( self.profile ) + " " + str( self.is_positive ) + ": " + str( self.related_object )


	def save( self, *args, **kwargs ):
		if self.is_positive:
			self.related_object.rating += 1
		else:
			self.related_object.rating -= 1

		self.related_object.save()
		super( Vote, self ).save( *args, **kwargs )


	class Meta:
		verbose_name = "Лайк/Дизлайк"
		verbose_name_plural = "Лайки/Дизлайки"

	
