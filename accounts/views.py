from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser
import random
import string
from django.core.cache import cache # For storing OTPs temporarily

# --- Signup View ---
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- OTP Password Reset Views ---

# Helper function to generate OTP
def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

# Helper function to simulate sending OTP (In a real app, integrate with SMS API like Twilio)
def send_otp_to_phone(phone_number, otp):
    # In a real application, you would integrate with an SMS gateway here.
    # For demonstration, we'll just print it to the console and store in cache.
    print(f"Simulating OTP send to {phone_number}: {otp}")
    # Store OTP in cache with phone number as key for verification, e.g., for 5 minutes
    cache.set(f'otp_{phone_number}', otp, 300) # OTP valid for 5 minutes (300 seconds)
    return True

def password_reset_phone(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            otp = generate_otp()
            if send_otp_to_phone(phone_number, otp):
                # Store the phone number in session to use in the next step
                request.session['reset_phone_number'] = phone_number
                messages.success(request, "An OTP has been sent to your phone number.")
                return redirect('password_reset_verify_otp')
            else:
                messages.error(request, "Failed to send OTP. Please try again.")
        except CustomUser.DoesNotExist:
            messages.error(request, "No user found with that phone number.")
    return render(request, 'registration/password_reset_phone.html')

def password_reset_verify_otp(request):
    phone_number = request.session.get('reset_phone_number')
    if not phone_number:
        messages.error(request, "Please request a password reset first.")
        return redirect('password_reset_phone')

    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = cache.get(f'otp_{phone_number}')

        if user_otp == stored_otp:
            # OTP is valid, allow user to set new password
            # Clear OTP from cache after successful verification
            cache.delete(f'otp_{phone_number}')
            messages.success(request, "OTP verified. You can now set a new password.")
            return redirect('password_reset_confirm_new')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, 'registration/password_reset_verify_otp.html', {'phone_number': phone_number})

def password_reset_confirm_new(request):
    phone_number = request.session.get('reset_phone_number')
    if not phone_number:
        messages.error(request, "Please complete the OTP verification process.")
        return redirect('password_reset_phone')

    try:
        user = CustomUser.objects.get(phone_number=phone_number)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found for password reset.")
        return redirect('password_reset_phone')

    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 and new_password1 == new_password2:
            user.set_password(new_password1)
            user.save()
            # Clear phone number from session after password reset
            del request.session['reset_phone_number']
            messages.success(request, "Your password has been reset successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match or are empty.")
    return render(request, 'registration/password_reset_confirm_new.html')
