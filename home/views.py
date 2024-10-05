from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import RegistrationForm
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.utils.encoding import force_str
from django.views import View
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetView
from django.contrib.auth import authenticate, login
from .models import Message
from django.contrib.auth.decorators import login_required
import bonggoQuery
from django.utils import timezone
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout


def send_verification_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Activate your BonggoQuery account'
    message = render_to_string('authentication/activation_email.html', {
        'user': user,
        'activation_url': f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/"
    })

    
    
    # Create the email
    email = EmailMessage(mail_subject,message, settings.EMAIL_HOST_USER, [user.email])
    email.content_subtype = "html"  # Set the subtype to HTML
    
    # Attach the HTML message
    email.send()
   

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.is_active = False  # Set the user as inactive initially
            user.save()
            send_verification_email(user, request)  # Send verification email
            messages.success(request, "Registration successful! Please check your email to activate your account.")
            
            return redirect('Home:login')  # Redirect to your login page or home
    else:
        form = RegistrationForm()
    return render(request, 'authentication/registration.html', {'form': form})




def activate_account(request, uidb64, token):
    try:
        # Decode the UID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('Home:login')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('Home:register')



# Create your views here.
def index(request):
    return render(request, "home/index.html")


# accounts/views.py


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Correct usage of the login function
            return redirect('Home:chat')  # Redirect to home or any desired page
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'authentication/login.html')


#   --------------------------- LOG OUT ---------------------------------------------
def custom_logout(request):
    logout(request)
    return redirect('Home:login')


# --------------------------------------  IMPLEMENTING THE CORE CHAT ------------------------------------
def getResponse(message_content):
    res = bonggoQuery.Query.normal_query.printing(message_content)
    return res # Sample response



@csrf_exempt  # CSRF exemption for testing with JSON data
@login_required  # Ensure user is logged in to send and receive messages
def chat_view(request):
    if request.method == "GET":
        return render(request, 'gpt/core.html')  # Render the chat template

    elif request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"error": "Message content cannot be empty."}, status=400)

        # Get the bot's response
        bot_response = getResponse(user_message)

        # Save the message and response in the Message model, linked to the current user
        new_message = Message.objects.create(
            user=request.user,
            content=user_message,
            response=bot_response
        )

        return JsonResponse({"response": bot_response})

    return JsonResponse({"error": "Invalid request"}, status=400)

