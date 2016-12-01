import random

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from blog.models import Tag, Question, Answer, Profile, Vote


class Command( BaseCommand ):
	help = 'Adds test data to base'


	def add_arguments( self, parser ):
		parser.add_argument( 
			'-q',
			type = int, 
			action = 'store',
			dest = 'questionsCount',
			default = 30,
			help = 'Number of questions' )

		parser.add_argument( 
			'-p',
			type = int,  
			action = 'store',
			dest = 'profilesCount',
			default = 15,
			help = 'Number of profiles' )

		parser.add_argument( 
			'-t',
			type = int,  
			action = 'store',
			dest = 'tagsCount',
			default = 20,
			help = 'Number of questions' )


	def randomBoolean( self ):
		return ( random.randint( 0, 2 ) > 0 )


	def addProfile( self, userNumber ):
		newUser = User.objects.create( 
			username = 'User' + str( userNumber ), 
			email = 'user' + str( userNumber ) + '@user.com' )
		newUser.save()
		newProfile = Profile.objects.create( 
			user = newUser, 
			nickname = 'User' + str( userNumber ),
			rating = random.randint( -100, 100 ) )
		newProfile.image.name = 'user' + str( ( newProfile.id % 5 ) + 1 ) + '.png'
		newProfile.save()


	def addTag( self, tagNumber ):
		newTag = Tag.objects.create( caption = 'Tag' + str( tagNumber ) )
		newTag.save()


	def generateLikes( self, relatedObject ):
		for profile in Profile.objects.all():
			if self.randomBoolean():
				if self.randomBoolean():
					newVote = Vote.objects.create( profile = profile, is_positive = True, related_object = relatedObject )

				else:
					newVote = Vote.objects.create( profile = profile, is_positive = False, related_object = relatedObject )


	def addAnswer( self, question, author, answerNumber ):
		newAnswer = Answer.objects.create( 
			text = ( 'Answer' + str ( answerNumber ) + ' ' ) * 5,
			question = question,
			correct = self.randomBoolean(),
			author = author )
		newAnswer.save()
		self.generateLikes( newAnswer )


	def addQuestion( self, author, questionNumber ):
		newQuestion = Question.objects.create(
			caption = 'Question' + str( questionNumber ), 
			text = ( 'question' + str( questionNumber ) + ' ' ) * 10,
			author = author )
		newQuestion.save()

		while ( newQuestion.tags.count() < min( 5, Tag.objects.count() ) ):
			index = random.randint( 0, Tag.objects.count() - 1 )
			tag = Tag.objects.all()[ index ]
			if ( tag not in newQuestion.tags.all() ):
				newQuestion.tags.add( tag )

		limit = random.randint( 2, 6 )
		for i in range( 0, limit ):
			index = random.randint( 0, Profile.objects.count() - 1 )
			answerAuthor = Profile.objects.all()[ index ]
			self.addAnswer( newQuestion, answerAuthor, i )

		self.generateLikes( newQuestion )


	def handle( self, *args, **options ):
		for i in range( Profile.objects.count() + 1, Profile.objects.count() + options[ 'profilesCount' ] + 1 ):
			self.addProfile( i )

		self.stdout.write( self.style.SUCCESS( 'Profiles generated' ) )

		for i in range( Tag.objects.count() + 1, Tag.objects.count() + options[ 'tagsCount' ] + 1 ):
			self.addTag( i )

		self.stdout.write( self.style.SUCCESS( 'Tags generated' ) )

		for i in range( Question.objects.count() + 1, Question.objects.count() + options[ 'questionsCount' ] + 1 ):
			index = random.randint( 0, Profile.objects.count() - 1 )
			author = Profile.objects.all()[ index ]
			self.addQuestion( author, i )
			self.stdout.write( self.style.SUCCESS( 'Question ' + str( i ) + ' generated' ) )

		self.stdout.write( self.style.SUCCESS( 'Generated data successfully' ) )