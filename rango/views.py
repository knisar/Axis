from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
import urllib2
import dum
@login_required
def restricted(request):
    return HttpResponse("you can see this because you are logged in")

def index(request):
    request.session.set_test_cookie()
    context_dict = {'boldmessage': "I am bold font from the context"}
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': pages_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits
    
    #conn = httplib.HTTPSConnection("curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'REV-API-KEY: 4PtxtYemYvKvgNTRGo0srL1CKoN2EqCBiITz' --header 'REV-APP-ID: Axis_hack' -d '{'data': ['speed','keyfeatures']} ' 'http://sandbox.reverieinc.com/v2/localization?target_lang=hindi&source_lang=english'")
    #conn.request("GET", "/")
    #r1 = conn.getresponse()
    #print r1.status, r1.responseMap
    #data1 = r1.read()
    #conn.request("GET", "/")
    #r2 = conn.getresponse()
    #print r2.status, r2.reason

    #data2 = r2.read()
    #conn.close()
    return render(request, 'rango/index.html', context_dict)
    return response
    

def about(request):

	context = {'message': "I serve static media"}
	return render(request, 'rango/about.html', context)

def category(request, category_name_slug):

    # Create a context dictionary which we can pass t000000o the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)
@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            
            # Now call the index() view.
            # The user will be shown the homepage.
            return add_page(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html/', {'form': form})

@login_required
def add_page(request):
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():

            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = PageForm()

    return render(request,'rango/add_page.html',{'form': form})


def register(request):
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()
    register = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() & profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            register = True
            profile.save()

        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'rango/register.html',{'user_form': user_form,'profile_form': profile_form,'register': register})

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your account is inactive")
        else:
            print "invalid details {0}, {1}".format(username,password)
            return HttpResponse("Invalid login details")

    else:
        return render(request,'rango/login.html',{})
@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/rango/')
def translate(request):
    html=""
    lang=""
    if request.method == "POST":
        url = request.POST.get("urlz")
        lang = request.POST.get("ops")
        print lang
        print url
        
        if(url!=""):
            html=dum.accept(url,lang)
        else:
            print "error"

    else:
        return HttpResponse("not working")  

    return render(request,'rango/index.html',{"response": html})


