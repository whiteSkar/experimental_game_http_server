from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_user(request):
    user_name = request.POST['user_name']
    print(user_name)
    
    return HttpResponse(user_name)

