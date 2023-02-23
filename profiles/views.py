from django.shortcuts import render

# Create your views here.


def profie(request):
    """Display the User's profile"""

    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)
