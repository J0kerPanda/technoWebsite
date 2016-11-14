from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, UserManager


class Tag( models.Model ):
	caption = models.CharField( null = False, blank = False, max_length = 20 )

	def __str__( self ):
		return self.caption


class Question( models.Model ):
	caption = models.CharField( null = False, blank = False, max_length = 100 )
	rating = models.IntegerField( default = 0 )
	text = models.TextField( null = False, blank = False )
	tags = models.ManyToManyField( 'Tag' )

	def __str__( self ):
		return self.caption + " " + self.text


class Answer( models.Model ):
	rating = models.IntegerField( default = 0 )
	text = models.TextField( null = False, blank = False )
	question = models.ForeignKey( 'Question', null = False, blank = False, on_delete = models.CASCADE )

	def __str__( self ):
		return self.text


class Profile( models.Model ):
	user = models.OneToOneField( User, null = False, blank = False )
	image = models.ImageField( max_length=100 )
	#create custom manager based on UserManager() ?
