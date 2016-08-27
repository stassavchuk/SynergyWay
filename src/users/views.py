from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from sql.database import Database
from forms import CreateUser


def users(request):
    template = loader.get_template('users.html')
    db = Database()
    user_list = db.get_all_users()
    context = dict(user_list=user_list)
    return HttpResponse(template.render(context, request))


def create(request):
    template = loader.get_template('create.html')
    form = CreateUser()
    context = dict(form=form)
    return HttpResponse(template.render(context, request))


def edit(request, user_id):
    template = loader.get_template('edit.html')
    db = Database()
    user_data = db.get_user_data(user_id)
    context = dict(user_data=user_data)
    return HttpResponse(template.render(context, request))


def courses(request):
    template = loader.get_template('courses.html')
    db = Database()
    course_list = db.get_all_courses()
    context = dict(course_list=course_list)
    return HttpResponse(template.render(context, request))
