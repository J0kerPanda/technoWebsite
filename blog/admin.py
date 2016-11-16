from django.contrib import admin

from blog.models import Tag, Question, Answer, Profile, Vote

# Register your models here.

admin.site.register( Tag )
admin.site.register( Question )
admin.site.register( Answer )
admin.site.register( Profile )
admin.site.register( Vote )


