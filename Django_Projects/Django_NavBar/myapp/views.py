from django.shortcuts import render,redirect
from .models import Contact,User
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth.models import User

# Create your views here.


# Home Page - index.html
def index(request):
	return render(request,'index.html')


# header.html --> Contact.html
def contact(request):
	if request.method=="POST":
		Contact.objects.create(
				name = request.POST['name'],
				email = request.POST['email'],
				mobile = request.POST['mobile'],
				remarks = request.POST['remarks'],
			)
		msg = "Contact Saved Successfully"
		contacts = Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else :
		contacts = Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'contacts':contacts})


# header.html --> SignUp.html
def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email = request.POST['email'])
			msg = "Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST["password"] == request.POST["cpassword"]:		
				User.objects.create(
						fname = request.POST['fname'],
						lname = request.POST['lname'],
						email = request.POST['email'],
						mobile = request.POST['mobile'],
						address = request.POST['address'],
						password = request.POST['password'],
						profile_picture = request.FILES['profile_picture'],
					)
				msg = "User Sign Up Successfully"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg = "Password And Confirm Password Does Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else :
		return render(request,'signup.html')


# header.html --> login.html
def login(request):
	if request.method == "POST" :
		try:
			user = User.objects.get(email = request.POST['email'])
			if user.password == request.POST['password'] :
				request.session['email'] = user.email
				request.session['fname'] = user.fname
				request.session['profile_picture'] = user.profile_picture.url
				return render(request,'index.html')
			else :
				msg = "Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg = "Email Not resigestered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')


# login.html and header.html --> logout.html
def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_picture']
		msg = "User Logged Out Successfully"
		return render(request,'login.html',{'msg':msg})
	except:
		msg = "User Logged Out Successfully"
		return render(request,'login.html',{'msg':msg})


# logout.html and login.html --> change-password.html
def change_password(request):
	if request.method == "POST" :
		user = User.objects.get(email = request.session['email'])
		if user.password == request.POST['old_password'] :
			if request.POST['new_password'] == request.POST['cnew_password'] :
				user.password = request.POST['new_password']
				user.save()
				del request.session['email']
				del request.session['fname']
				msg = "Password Changed Successfully"
				return render(request,'login.html',{'msg':msg})
			else :
				msg = "New Password And Confirm New Password Does Not Matched"
				return render(request,'change-password.html',{'msg':msg})
		else :
			msg = "Old Password Does Not Matched"
			return render(request,'change-password.html',{'msg':msg})
	else:
		return render(request,'change-password.html')


# Forgot Password
def forgot_password(request) :
	if request.method == "POST" :
		try :
			user = User.objects.get(email = request.POST['email'])
			otp = random.randint(1000,9999)
			subject = 'OTP for Forgot Password'
			message = 'Hello ' + user.fname + ', Your OTP For Forgot Password Is ' + str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email,] 
			send_mail( subject, message, email_from, recipient_list )
			request.session['otp'] = otp
			request.session['email_otp'] = user.email
			return render(request,'otp.html')
		except Exception as e:
			print(e)
			msg = "Email Is Not Registered"
			return render(request,'forgot-password.html',{'msg':msg})
	else :
		return render(request,'forgot-password.html')


# Verify OTP
def verify_otp(request):
	otp = int(request.POST['otp'])
	if otp == int(request.session['otp']) :
		del request.session['otp']
		return render(request,'new-password.html')
	else :
		msg = "Invalid OTP"
		return render(request,'otp.html',{'msg':msg})


# new-password.html
def new_password(request):
	if request.POST['new_password'] == request.POST['cnew_password']:
		user = User.objects.get(email = request.session['email_otp'])
		user.password = request.POST['new_password']
		user.save()
		del request.session['email_otp']
		msg = "Password Updated Successfully"
		return render(request,'login.html',{'msg':msg})
	else :
		msg = "New Password and Confirm New Password Does Not Matched"
		return render(request,'new-password.html',{'msg':msg})


# Profile
def profile(request) :
	user = User.objects.get(email = request.session['email'])
	if request.method == "POST" :
		user.fname = request.POST['fname']
		user.lname = request.POST['lname']
		user.mobile = request.POST['mobile']
		user.address = request.POST['address']
		try :
			user.profile_picture = request.FILES['profile_picture']
		except :
			pass
		user.save()
		msg = "Profile Updated Successfully"
		request.session['profile_picture'] = user.profile_picture.url
		return render(request,'profile.html',{'user':user,'msg':msg})
	else :
		return render(request,'profile.html',{'user':user})

def home(request):
    # Assuming you want to display some posts on the home page
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_id = request.POST.get('author_id')

        try:
            author = User.objects.get(id=author_id)
        except User.DoesNotExist:
            # Handle case where author does not exist
            return render(request, 'create_post.html', {'users': User.objects.all(), 'error_message': 'Invalid author ID'})

        Post.objects.create(title=title, content=content, author=author)
        return redirect('index')  # Assuming 'index' is the name of the view for the homepage
    else:
        users = User.objects.all()
        return render(request, 'create_post.html', {'users': users})