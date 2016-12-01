from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from blog.models import Tag, Question, Answer, Profile, Vote

class LoginForm( forms.Form ):
	login = forms.CharField( 
		required = True, 
		label = 'Login', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your login here' } ) )
	password = forms.CharField( 
		required = True, 
		label = 'Password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your password here' } ) )


class NewUserForm( forms.Form ):
	login = forms.CharField( 
		required = True, 
		label = 'Login', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your login here' } ) )
	nickname = forms.CharField( 
		required = True, 
		label = 'Nickname', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your nickname here' } ) )
	email = forms.EmailField( 
		required = True, 
		label = 'Email', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your email here' } ) )
	password = forms.CharField( 
		required = True, 
		label = 'Password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your password here' } ),
		validators = [ validate_password ] )
	passwordConfirm = forms.CharField( 
		required = True, 
		label = 'Confirm password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Reenter password here' } ) )
	avatar = forms.ImageField( 
		required = False, 
		label = 'Avatar',
		widget = forms.ClearableFileInput( attrs={ 'class': 'form-control-file' } ) )


	def clean( self ):
		cleaned_data = super( NewUserForm, self ).clean()
		password = cleaned_data.get( 'password', False )
		passwordConfirm = cleaned_data.get( 'passwordConfirm', False )

		if password and passwordConfirm:
			if password != passwordConfirm:
				self.add_error( 'passwordConfirm', 'Passwords must match' )

		username = cleaned_data.get( 'login', False )
		if username:
			try:
				Profile.objects.get_by_login( username )
				self.add_error( 'login', 'User already exists' )

			except:
				pass

		nickname = cleaned_data.get( 'nickname', False )
		if nickname:
			try:
				Profile.objects.get_by_nickname( nickname )
				self.add_error( 'nickname', 'Nickname already taken' )

			except:
				pass


	def save( self ):
		newUser = User.objects.create( 
		username = self.cleaned_data[ 'login' ], 
		email = self.cleaned_data[ 'email' ] )
		newUser.set_password( self.cleaned_data[ 'password' ] )
		newUser.save()

		newProfile = Profile.objects.create( 
			user = newUser,
			nickname = self.cleaned_data[ 'nickname' ],
			rating = 0 )

		if ( self.cleaned_data[ 'avatar' ] ):
			newProfile.image = self.cleaned_data[ 'avatar' ]
		newProfile.save()


class ChangeSettingsForm( forms.Form ):
	nickname = forms.CharField( 
		required = False, 
		label = 'Nickname', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write new nickname here' } ) )
	email = forms.EmailField( 
		required = False, 
		label = 'Email', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write new email here' } ) )
	password = forms.CharField( 
		required = True, 
		label = 'Password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your password here' } ) )
	passwordConfirm = forms.CharField( 
		required = True, 
		label = 'Confirm password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Reenter your password here' } ) )
	avatar = forms.ImageField( 
		required = False, 
		label = 'Avatar',
		widget = forms.ClearableFileInput( attrs={ 'class': 'form-control-file' } ) )


	def clean( self ):
		cleaned_data = super( ChangeSettingsForm, self ).clean()
		password = cleaned_data.get( 'password', False )
		passwordConfirm = cleaned_data.get( 'passwordConfirm', False )

		if password and passwordConfirm:
			if password != passwordConfirm:
				self.add_error( 'passwordConfirm', 'Passwords must match' )

		nickname = cleaned_data.get( 'nickname', False )
		if nickname:
			try:
				Profile.objects.get_by_nickname( nickname )
				self.add_error( 'nickname', 'Nickname already taken' )

			except:
				pass

	def save( self, profile ):

		if ( self.cleaned_data[ 'nickname' ] ):
			profile.nickname = self.cleaned_data[ 'nickname' ]

		if ( self.cleaned_data[ 'email' ] ):
			profile.user.email = self.cleaned_data[ 'email' ]

		if ( self.cleaned_data[ 'avatar' ] ):
			profile.image = self.cleaned_data[ 'avatar' ]

		profile.save()