from django import forms
from .models import postRecord,userRecord

CHOICES =(('Politics','Politics'),('Sports','Sports'),('Others','Others'))

class savePost(forms.Form):
	#author = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter the Authors Name'}),label='Post Author :', max_length=250)
	postTitle = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter the Post Title'}),label='Post Title :', max_length=250)
	postType = forms.ChoiceField(label='Post Type :', widget=forms.Select, choices = CHOICES)
	picture = forms.FileField(label='Post File :', widget=forms.FileInput(attrs={'placeholder':'Enter the Post Title'}))
	postBody = forms.CharField(label='Post Contents :', widget=forms.Textarea(attrs={'placeholder':'Enter the Post Contents'}))
	#tank = forms.IntegerField(widget=forms.HiddenInput(), initial=123) 
	#author = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter the Authors Name',value="Sherif"}),label='Post Author :', max_length=250)
	#postType = forms.ChoiceField(label='Post Type :', widget=forms.RadioSelect, choices = CHOICES)
	#postType = forms.ChoiceField(label='Post Type :', widget=forms.TextInput(attrs={'class':'special','size':'40','required':'false'}))
	#cc_myself = forms.BooleanField(required=False)  postTitle postBody postType
	#TextInput	-	text,	NumberInput	-	number,	EmailInput	-	email,	URLInput	-	url,	PasswordInput	-	password,	HiddenInput	-	hidden,	DateInput	-	text,	DateTimeInput	-	text,	TimeInput	-	text,	Textarea	-	textarea,	CheckboxInput	-	checkbox,	Select - <select> with <option> values as <choices> in django,	SelectMultiple	-	allow multiple option select,	RadioSelect - group of radio buttons like RadioGroup in android - it has optional value like choices in select,	CheckboxSelectMultiple	 - multiple selction from more than check boxes, FileInput	-	file, ClearableFileInput	-	file with an addition checkbox to help u select file choose,
	
class LoginPost(forms.Form):
	userID = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Your User ID'}),label='User ID :', max_length=250)
	userPassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Your Password'}),label='User Password :', max_length=250)