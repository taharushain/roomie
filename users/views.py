from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		profile_form = ProfileUpdateForm(request.POST, request.FILES)

		if form.is_valid() and profile_form.is_valid():
			user = form.save()
			user.refresh_from_db()
			profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)

			profile_form.full_clean()
			profile_form.save()

			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created, You are now able to log in.')
			return redirect('login')
	else:
		form = UserRegisterForm()
		profile_form = ProfileUpdateForm()

	return render(request, 'users/register.html',{'form': form, 'profile_form': profile_form})

@login_required
def profile(request):

	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, f'Your account has been updated.')
			return redirect('profile')
	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'user_form': user_form,
		'profile_form': profile_form
	}
	return render(request, 'users/profile.html', context)