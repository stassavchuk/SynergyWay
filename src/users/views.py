from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from sql.database import Database
from forms import UserForm
from django.views.generic import View
import json


class CreateUserView(View):
    def get(self, request):
        template = loader.get_template('create.html')
        form = UserForm()
        context = dict(form=form)
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        # try:
        form = UserForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            db = Database()
            db.add_user(**data)
            template = loader.get_template('create.html')
            form = UserForm(request.POST)
            context = dict(form=form, success=True)
            return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('create.html')
            form = UserForm(request.POST)
            context = dict(form=form)
            return HttpResponse(template.render(context, request))
        # except BaseException as e:
        #     return HttpResponse(status=400)


class UserListView(View):
    def get(self, request):
        template = loader.get_template('users.html')
        db = Database()
        user_list = db.get_all_users()
        context = dict(user_list=user_list)
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.POST['user_id']
        template = loader.get_template('users.html')
        db = Database()
        db.delete_user(user_id)
        user_list = db.get_all_users()
        context = dict(user_list=user_list)
        return HttpResponse(template.render(context, request))


class EditUserView(View):
    def get(self, request, user_id):
        template = loader.get_template('edit.html')
        db = Database()
        user_data = db.get_user_data(user_id)[0]
        all_courses = db.get_all_courses()

        # ---
        db.update_records(user_id, [1, 2, 3])
        # ---

        user_courses = db.get_user_courses(user_id)

        all_courses = json.dumps(all_courses)
        user_courses = json.dumps(user_courses)

        data = {
            'user_name': user_data[1],
            'email': user_data[2],
            'status': user_data[3],
            'phone': user_data[4],
            'm_phone': user_data[5]
        }
        form = UserForm(data)
        form.fields['user_name'].widget.attrs['readonly'] = True
        context = dict(form=form, all_courses=all_courses, user_courses=user_courses)
        return HttpResponse(template.render(context, request))

    def post(self, request, user_id):
        form = UserForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data

            print data

            template = loader.get_template('edit.html')
            form = UserForm(request.POST)
            context = dict(form=form, success=True)
            return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('edit.html')
            form = UserForm(request.POST)
            context = dict(form=form)
            return HttpResponse(template.render(context, request))


class CoursesView(View):
    def get(self, request):
        template = loader.get_template('courses.html')
        db = Database()
        course_list = db.get_all_courses()
        context = dict(course_list=course_list)
        return HttpResponse(template.render(context, request))
