from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def users(request):
    template = loader.get_template('users.html')
    context = {}
    return HttpResponse(template.render(context, request))


def create(request):
    template = loader.get_template('create.html')
    context = {}
    return HttpResponse(template.render(context, request))


def edit(request, user_id):
    template = loader.get_template('edit.html')
    context = {}
    return HttpResponse(template.render(context, request))


def courses(request):
    template = loader.get_template('courses.html')
    context = {}
    return HttpResponse(template.render(context, request))
