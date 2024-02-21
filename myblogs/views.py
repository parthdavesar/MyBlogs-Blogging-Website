from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from .models import blog_category, blog_post, Comment, contact_info, subscription_info, likes
from .forms import BlogPost_Form, CommentForm, Blog_Form
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q

# Create your views here.

def home(request):
    x=blog_category.objects.all()
    print(x)
    if request.method == 'GET':
        return render(request,'myblogs/home.html', {"category":x})
    elif request.method == 'POST':
        email = request.POST.get('subscription_email')
        y = subscription_info(s_email=email)
        y.save()
        return render(request,'myblogs/home.html',{"category":x , "feedback": "Thank you for the subscription!"})
    
def contact(request):
    if request.method == 'GET':
        return render(request, 'myblogs\contact.html')
    elif request.method == 'POST':
        email = request.POST.get('user_email')
        message = request.POST.get('message')
        x = contact_info(u_email = email, u_message = message)
        x.save()
        return render(request, 'myblogs\contact.html', {'feedback':'Your message has been recorded'})

def ck(request):
    x=BlogPost_Form()
    return render(request,'myblogs/ck.html',{"x":x})

def allblogs(request):
    y=blog_post.objects.all()
    # Pagination
    p = Paginator(y, 3)  # Show 3 blogs per page
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request,'myblogs/allblogs.html',{"y":page_obj})

def add_blog(request):
    x = Blog_Form()  
    if request.method == "GET":
        return render(request,'myblogs/add_blog.html',{"x":x})
    else:
        form = Blog_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request,'myblogs/add_blog.html',{"x":x})

def blog_details(request, blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    user = request.user
    if user.is_authenticated:
        isLiked = likes.objects.filter(user=user, post__id=blog_id).exists()
        z=obj.view_count
        z=z+1
        obj.view_count=z
        obj.save()
        print(obj)
        print(blog_id)
        return render(request,'myblogs/blog_details.html', {"obj":obj, "isLiked":isLiked})
    else:
        z=obj.view_count
        z=z+1
        obj.view_count=z
        obj.save()
        print(obj)
        print(blog_id)
        return render(request,'myblogs/blog_details.html', {"obj":obj})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'myblogs/loginuser.html', {'form': AuthenticationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password')
        user = authenticate(request, username = a, password = b)
        if user is None:
            return render(request, 'myblogs\loginuser.html', {'form':AuthenticationForm(), 'error':'Invalid Credentials'})
        else:
            login(request, user)
            return redirect('home')

def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')
        
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'myblogs/signupuser.html', {'form': UserCreationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password1')
        c = request.POST.get('password2')
        if b==c:
            if(User.objects.filter(username=a)):
                return render(request, 'myblogs\signupuser.html', {'form':UserCreationForm(), 'error':'Username already exists! Try again with a different username'})
            else:
                user = User.objects.create_user(username=a, password=b)
                user.save()
                login(request,user)
                return redirect('home')
        else:
            return render(request, 'myblogs\signupuser.html', {'form':UserCreationForm(), 'error':'Password do not match! Try again'})

def blogfilter(request):
    # Extract the category from the request parameters
    category_name = request.GET.get('category')

    # If a category is provided, filter blog posts by that category, otherwise, get all blog posts
    if category_name:
        blogs = blog_post.objects.filter(blog_cat__blog_cat=category_name)
    else:
        blogs = blog_post.objects.all()

    return render(request, 'myblogs/blogfilter.html', {"blogs": blogs, "category": category_name})

def findproduct(request):
    if request.method == "POST":
        x = request.POST.get('prod_search')
        mydata = blog_category.objects.filter(Q(blog_cat__icontains = x) | Q(blogcat_description__icontains = x))
        if mydata:
            return render(request, 'myblogs/home.html', {"category":mydata})
        else:
            return render(request, 'myblogs/home.html', {"warning":'No such item found'})

def add_like(request, blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    user = request.user
    newLike = likes(user=user, post=obj)
    newLike.save()
    y=obj.like_count
    y=y+1
    obj.like_count=y
    obj.save()
    return redirect('blog_details', obj.id)

def unlike(request, blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    user = request.user
    #remove from likes model
    likes.objects.filter(user=user, post=obj).delete()
    y=obj.like_count
    y=y-1
    obj.like_count=y
    obj.save()
    return redirect('blog_details', obj.id)

def add_comment(request, blog_id):
    post = get_object_or_404(blog_post, pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.created_at = timezone.now()  # Add this line to save the current timestamp
            comment.save()
            return redirect('blog_details', blog_id=post.id)

def delete_comment(request, blog_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect( 'blog_details', blog_id=blog_id)

def edit_comment(request, blog_id, comment_id):
    # Retrieve the comment object
    comment = Comment.objects.get(id=comment_id)
    
    if request.method == 'POST':
        # Process the form submission
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_details', blog_id=blog_id)
    else:
        # Populate the form with existing comment data
        form = CommentForm(instance=comment)
    
    return render(request, 'myblogs/edit_comment.html', {'form': form})
