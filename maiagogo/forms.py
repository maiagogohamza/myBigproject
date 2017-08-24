# make sure this is at the top if it isn't already
from django import forms
from maiagogo.models import Post, Comment, Category, Page, UserProfile
from django.contrib.auth.models import User
# our new form
class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    contact_phone=forms.IntegerField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)
    #cc_myself = forms.BooleanField(required=False)

# the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['contact_phone'].label = "Your phone no:"
        self.fields['content'].label = "What do you want to say?"

class  PostForm(forms.ModelForm):
       title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Title of Your Post', 'class':'form-control'}))
       text = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder':'Text', 'class':'form-control'})) 
       class Meta:
           model = Post
           fields = ('title', 'text')

class UserForm(forms.ModelForm):
      username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username', 'class':'form-control'})) 
      email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'email', 'class':'form-control'}))
      password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', 'class':'form-control'}))
  

      class Meta:
          model = User
          fields = ('username', 'email', 'password')

class	CommentForm(forms.ModelForm):
        class	Meta:
           model = Comment
           fields = ('author',	'text')

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder':'Please enter the category name', 'class':'form-control'}))
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # An inline class to provide additional information on the form.
    class Meta:
# Provide an association between the ModelForm and a model
       model = Category

class PageForm(forms.ModelForm):
   title = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder':'Please enter the title of the page', 'class':'form-control'}))
   url = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Please enter the URL of the page', 'class':'form-control'}))
   views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
  
   class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign keys
        fields = ('title', 'url')

   def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        # If url is not empty and doesn't start with 'http://' add 'http://' to the beginning
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

class UserProfileForm(forms.ModelForm):
      bio=forms.CharField(max_length=252, required=False)
      location = forms.CharField(required=False)
      birthday=forms.DateField(required=False)
      website = forms.URLField(help_text="Please enter your website.", required=False)
      picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

      class Meta:
          model = UserProfile
          fields = ['bio', 'location','birthday','website', 'picture']
