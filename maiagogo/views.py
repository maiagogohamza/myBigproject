from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from maiagogo.models import Post, Category, Page, Comment, UserProfile
from maiagogo.forms import ContactForm, CommentForm, CategoryForm, PageForm, UserForm,  PostForm, UserProfileForm
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
#from django.python import userAuthentication


# Create your views here.
def Sage(request):
  cat_list = get_category_list()
  return render(request, 'MathSage.html',{'cats':cat_list})

def home(request):
  return render(request, 'index.html',{})

def mentor(request):
  return render(request, 'blog.html',{ })

def browser(request):
  return render(request, 'bzbase.html',{})

def blog(request):
   cat_list = get_category_list()
   posts=Post.objects.order_by('-created_date')
   return render(request, 'blogpost2.html',{'posts': posts, 'cats':cat_list})

def post_detail(request, pk):
    cat_list = get_category_list()
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post, 'cats':cat_list})

@login_required
def post_new(request):
        cat_list = get_category_list()
	if request.method == "POST":
           form	= PostForm(request.POST)
	   if form.is_valid():
		post = form.save(commit=False)
		post.author = request.user
		post.published_date = timezone.now()
		post.save()
		return	redirect('post_detail',	pk=post.pk)
	else:
	      form = PostForm()
	return	render(request,	'post_edit.html', {'form': form, 'cats': cat_list})

@login_required
def post_edit(request, pk):
    cat_list = get_category_list()
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'cats': cat_list})



def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):
    cat_list = get_category_list()
    category_list=Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]
    for category in category_list:
        category.url = encode_url(category.name)
    context_dict={'categories':category_list, 'pages':page_list, 'cats': cat_list}
    return render(request, 'inndex.html', context_dict)

def get_category_list():
    cat_list = Category.objects.all()
    for cat in cat_list:
       cat.url = encode_url(cat.name)
    return cat_list

def category(request, category_name_url):
    cat_list = get_category_list()
    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}
    context_dict['cats'] = cat_list
    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    try:
    # Can we find a category with the given name?
    # If we can't, the .get() method raises a DoesNotExist exception.
    # So the .get() method returns one model instance or raises an exception.
       category = Category.objects.get(name__iexact=category_name)
    # Retrieve all of the associated pages.
    # Note that filter returns >= 1 model instance.
       pages = Page.objects.filter(category=category).order_by('-views')
    # Adds our results list to the template context under name pages.
       context_dict['pages'] = pages
    # We also add the category object from the database to the context dictionary.
    # We'll use this in the template to verify that the category exists.
       context_dict['category'] = category
    except Category.DoesNotExist:
    # We get here if we didn't find the specified category.
    # Don't do anything - the template displays the "no category" message for us.
       pass
#Go render the response and return it to the client.
    return render(request, 'category.html', context_dict)


def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()

    return HttpResponse(likes)

def track_url(request):
    page_id = None
    url = '/maiagogo/browser_home/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
               page = Page.objects.get(id=page_id)
               page.views = page.views + 1
               page.save()
               url = page.url
            except:
               pass
    return redirect(url)

def contact(request):
    form_class = ContactForm
    cat_list = get_category_list()
    # new logic!
    Sent=False
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            contact_phone=request.POST.get('contact_phone', '')

            # Email the profile with the 
            # contact information
            template = get_template('contact_template.txt')
            context = Context({'contact_name': contact_name, 'contact_email': contact_email, 'form_content': form_content,
            'contact_phone':contact_phone})
            content = template.render(context)

            email = EmailMessage("New contact form submission", content,"Your website" +'', ['youremail@gmail.com'],
 headers = {'Reply-To': contact_email }
            )
            email.send()
            Sent=True
            #return redirect('contact')
            
    return render(request, 'contact.html', {'form': form_class, 'Sent':Sent, 'cats':cat_list})

def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code change
    cat_list = get_category_list()
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
       # Attempt to grab information from the raw form information.
       # Note that we make use of both UserForm and UserProfileForm.
       user_form = UserForm(data=request.POST)
       #profile_form = UserProfileForm(data=request.POST)
       # If the two forms are valid...
       if user_form.is_valid(): #and profile_form.is_valid():
          # Save the user's form data to the database.
          user = user_form.save()
          # Now we hash the password with the set_password method.
          # Once hashed, we can update the user object.
          user.set_password(user.password)
          user.save()
          # Now sort out the UserProfile instance.
          # Since we need to set the user attribute ourselves, we set commit=False.
          # This delays saving the model until we're ready to avoid integrity problems.
          #profile = profile_form.save(commit=False)
          #profile.user = user
           # Did the user provide a profile picture?
           # If so, we need to get it from the input form and put it in the UserProfile model.
          #if 'picture' in request.FILES:
              #profile.picture = request.FILES['picture']
          # Now we save the UserProfile model instance.
          #profile.save()
# Update our variable to tell the template registration was successful.
          registered = True
# Invalid form or forms - mistakes or something else?
# Print problems to the terminal.
# They'll also be shown to the user.
       else:
               print user_form.errors #profile_form.errors
# Not a HTTP POST, so we render our form using two ModelForm instances.
# These forms will be blank, ready for user input.
    else:
          user_form = UserForm()
          #profile_form = UserProfileForm()
# Render the template depending on the context.
    return render(request, 'register.html', {'user_form': user_form,'registered': registered, 'cats':cat_list} )

def user_login(request):
        cat_list = get_category_list()
        context_dict = {}
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user is not None:
			# Is the account active? It could have been disabled.
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/maiagogo/#feature')
			else:
                                context_dict['cats'] = cat_list
                                context_dict['disabled_account'] = True
				# An inactive account was used - no logging in!
				return render(request, 'login.html', context_dict)
		else:
			# Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
                        context_dict['cats'] = cat_list
                        context_dict['bad_details'] = True
			return render(request, 'login.html', context_dict)
			# The request is not a HTTP POST, so display the login form.
			# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'login.html', {'cats':cat_list})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/maiagogo/')

def add_comment_to_post(request, pk):
    cat_list = get_category_list()
    post = get_object_or_404(Post,pk=pk)
    if request.method=="POST":
       form = CommentForm(request.POST)
       if form.is_valid():
          comment = form.save(commit=False)
          comment.post=post
          comment.save()
          return redirect('post_detail', pk=post.pk)
    else:
           form	=CommentForm()
    return render(request, 'add_comment_to_post.html', {'form':form, 'cats':cat_list})

@login_required
def comment_approve(request,	pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

@login_required
def add_category(request): 
    cat_list=get_category_list()
    if request.method == 'POST': 
        form = CategoryForm(request.POST) 
        if form.is_valid(): 
            form.save(commit=True) 
            return HttpResponseRedirect('/maiagogo/#feature') 
        else: 
            print form.errors 
    else: 
        form = CategoryForm() 
    return render(request, 'add_category.html', {'form': form ,'cats': cat_list}) 


@login_required
def add_page(request, category_name_url):
    cat_list = get_category_list()
    context_dict = {}
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            cat = Category.objects.get(name=category_name)
            page.category = cat
            
            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict['category_name_url']= category_name_url
    context_dict['category_name'] =  category_name
    context_dict['form'] = form
    context_dict['cats'] = cat_list

    return render( request, 'add_page.html', context_dict)


def SaveProfile(request):
    saved = False
    if request.method == "POST":
#Get the posted form
       MyProfileForm = ProfileForm(request.POST, request.FILES)
       if MyProfileForm.is_valid():
          profile = Profile()
          profile.name = request.user
          profile.picture = MyProfileForm.cleaned_data["picture"]
          profile.save()
          saved = True
       else:
         MyProfileForm = Profileform()
    return render(request, 'saved.html', locals())


def SaveProfile(request):
    saved = False
    if request.method == "POST":
#Get the posted form
       MyProfileForm = ProfileForm(request.POST, request.FILES)
       if MyProfileForm.is_valid():
          profile = Profile()
          profile.name = MyProfileForm.cleaned_data["name"]
          profile.picture = MyProfileForm.cleaned_data["picture"]
          profile.save()
          saved= True
       else:
          MyProfileForm = Profileform()
    return render(request, 'saved.html', locals())

    
 
