from django import forms

class NewUserForm( forms.Form ):

	login = forms.CharField( required = True, label = 'Login', help_text = 'Write your login here' )
	email = forms.EmailField( required = True, label = 'Email', help_text = 'Write your email here' )
	nickname = forms.CharField( required = True, label = 'Nickname', help_text = 'Write your nickname here' )
	password = forms.CharField( required = True, label = 'Password', help_text = 'Write your password here', widget = forms.PasswordInput )
	passwordConfirm = forms.CharField( required = True, label = 'Confirm password', help_text = 'Reenter your password here', widget = forms.PasswordInput )
	avatar = forms.ImageField( required = False, label = 'Avatar' )


class ChangeSettingsForm( forms.Form ):
	email = forms.EmailField( required = False, label = 'Email', help_text = 'Write new email here' )
	nickname = forms.CharField( required = False, label = 'Nickname', help_text = 'Write new nickname here'  )
	password = forms.CharField( required = False, label = 'Password', help_text = 'Write new password here', widget = forms.PasswordInput )
	passwordConfirm = forms.CharField( required = False, label = 'Confirm password', help_text = 'Reenter new password here', widget = forms.PasswordInput )
	avatar = forms.ImageField( required = False, label = 'Avatar' )

class LoginForm( forms.Form ):
	login = forms.CharField( required = True, label = 'Login', help_text = 'Write your login here' )
	password = forms.CharField( required = True, label = 'Password', help_text = 'Write your password here', widget = forms.PasswordInput )