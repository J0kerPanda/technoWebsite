from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.contrib.auth.models import User
from blog.models import Tag, Question, Answer, Profile, Vote

from django.utils import timezone


class Command( BaseCommand ):
	help = 'Adds test data to base'


	def handle( self, *args, **options ):
		dateLimit = timezone.now() - timezone.timedelta( days = 92 )

		popularTags = Tag.objects.filter( question__postDate__gte = dateLimit )
		popularTags = popularTags.annotate( questionCount = models.Count( 'question' ) ).order_by( '-questionCount' )[:10]
		cache.set( 'popular_tags', popularTags )

		bestMembers = Profile.objects.filter( question__postDate__gte = dateLimit, answer__postDate__gte = dateLimit )
		bestMembers  = bestMembers.annotate( questionCount = models.Count( 'question' ), answerCount = models.Count( 'answer' ) ).order_by( '-questionCount', '-answerCount' )[:10]
		cache.set( 'best_members', bestMembers )
