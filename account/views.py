from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserCreateForm, LoginForm, UserUpdateForm
from django_email_verification import send_email
from django.contrib.auth.decorators import login_required
from django.contrib import messages

User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            user = User.objects.create_user(
                username=user_username, 
                email=user_email, 
                password=user_password
            )

            user.is_active = False

            send_email(user)

            return redirect('account:email-verification-sent')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


def login_user(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
         
        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('account:login')
    
    else:
        return render(request, 'account/login/login.html', {'form': form})
    
@login_required(login_url='account:login')
def dashboard_user(request):
    return render(request, 'account/dashboard/dashboard.html')


@login_required(login_url='account:login')
def logout_user(request):
    session_keys = list(request.session.keys())

    for key in session_keys:
        if key == 'session_key':
            continue
        del request.session[key]
    logout(request)
    return redirect('account:login')

@login_required(login_url='account:login')
def profile_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('account:dashboard')
        
    form = UserUpdateForm(instance=request.user)
    return render(request, 'account/dashboard/profile-management.html', {'form': form})


@login_required(login_url='account:login')
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('account:login')
    else:
        return render(request, 'account/dashboard/account-delete.html')
    







