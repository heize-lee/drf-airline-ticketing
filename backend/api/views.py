from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup(request):
    if request.method=="POST":
        firstName=request.POST['firstName']
        lastName=request.POST['lastName']
        email=request.POST['email']
        password=request.POST['password']

        print(f'DB에 {firstName},{lastName},{email},{password} 정보 등록 되었습니다.')



        return JsonResponse({"회원가입 성공!"})
    return JsonResponse({"hello":"world"})