from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import AssignedReview, Example


# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "POST" and 'sign_in' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to a home page or specific section of the app
        else:
            # Return an 'invalid login' error message specific to sign-in attempt
            return render(request, 'myapp/home.html', {'error': 'Invalid username or password.'})
    elif request.method == "POST" and 'sign_up' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        # Create a new user account
        return redirect('index')
    context = {
        'user': request.user,
        'sign_in_visibility': 'hidden' if request.user.is_authenticated else 'visible',
    }
    return render(request, 'myapp/home.html', context)


def sign_in(request):
    return render(request, 'myapp/sign_in.html', {})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='index')
def expert(request):
    context = {'navigation_items': [
        {'name': 'Home', 'url': 'index'},
        {'name': 'Be an Expert', 'url': 'expert'},

    ]}
    return render(request, 'myapp/Be an Expert.html', context)


def explore(request):
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Be an Explorer', 'url': 'explorer'},
        ]
    }
    return render(request, 'myapp/Be an Explorer.html', context)


def review_menu(request):
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Be an Reviewer', 'url': 'review'},
            {'name': 'Conduct a Review', 'url': 'review'},
        ]
    }
    return render(request, 'myapp/Be an Reviewer.html', context)


@login_required(login_url='index')
def review(request, example_id):
    # Fetch the example first (optional: add error handling if example does not exist)
    example = get_object_or_404(Example, pk=example_id)
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Be a Reviewer', 'url': 'review'},
            # Assuming you have a separate view or page for becoming a reviewer
            {'name': 'Conduct a Review', 'url': 'review_example', 'params': {'example_id': example_id}},
            # Assuming you need to pass parameters for clarity
        ],
        'example': example,
    }

    if not request.user.profile.is_instructor:
        try:
            assignment = AssignedReview.objects.get(example_id=example.id, reviewer=request.user.profile)
        except AssignedReview.DoesNotExist:
            return HttpResponseForbidden("You are not assigned to review this example.")

        if request.method == 'POST':
            # Process the review submission
            assignment.completed = True
            assignment.save()
            return redirect('review')  # Ensure this URL is properly named and defined in your urls.py

        context['assignment'] = assignment  # Add assignment to context if needed in the template

    return render(request, 'myapp/Show Review Examples.html', context)


def new_workout(request):
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Create a new worked-out example', 'url': 'new_workout'},
        ]
    }
    return render(request, 'myapp/Create a new worked-out example.html', context)
