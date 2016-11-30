from django import forms

class NewUserForm( forms.Form ):

	login = forms.CharField( 
		required = True, 
		label = 'Login', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your login here' } ) )
	email = forms.EmailField( 
		required = True, 
		label = 'Email', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your email here' } ) )
	password = forms.CharField( 
		required = True, 
		label = 'Password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your password here' } ) )
	passwordConfirm = forms.CharField( 
		required = True, 
		label = 'Confirm password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Reenter password here' } ) )
	avatar = forms.ImageField( 
		required = False, 
		label = 'Avatar',
		widget = forms.ClearableFileInput( attrs={ 'class': 'form-control-file' } ) )


class ChangeSettingsForm( forms.Form ):
	login = forms.CharField( 
		required = False, 
		label = 'Login', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your login here' } ) )
	email = forms.EmailField( 
		required = False, 
		label = 'Email', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write new email here' } ) )
	password = forms.CharField( 
		required = False, 
		label = 'Password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Write new password here' } ) )
	passwordConfirm = forms.CharField( 
		required = False, 
		label = 'Confirm password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Reenter new password here' } ) )
	avatar = forms.ImageField( 
		required = False, 
		label = 'Avatar',
		widget = forms.ClearableFileInput( attrs={ 'class': 'form-control-file' } ) )

class LoginForm( forms.Form ):
	login = forms.CharField( 
		required = True, 
		label = 'Login', 
		widget = forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your login here' } ) )
	password = forms.CharField( 
		required = True, 
		label = 'Password', 
		widget = forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': 'Write your password here' } ) )