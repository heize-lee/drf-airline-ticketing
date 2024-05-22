from django.shortcuts import render
from django.http import JsonResponse

def signup(request):
    return JsonResponse({"hello":"world"})