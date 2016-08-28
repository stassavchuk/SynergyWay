from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from sql.database import Database
from forms import CreateUserForm
from django.views.generic import View


class CreateUserView(View):
    def get(self, request):
        template = loader.get_template('create.html')
        form = CreateUserForm()
        context = dict(form=form)
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        try:
            form = CreateUserForm(request.POST or None)
            if form.is_valid():
                return HttpResponse('OK', status=200)
            else:
                template = loader.get_template('create.html')
                form = CreateUserForm(request.POST)
                context = dict(form=form)
                return HttpResponse(template.render(context, request))
        except BaseException as e:
            return HttpResponse(status=400)


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
        user_data = db.get_user_data(user_id)
        context = dict(user_data=user_data)
        return HttpResponse(template.render(context, request))


class CoursesView(View):
    def get(self, request):
        template = loader.get_template('courses.html')
        db = Database()
        course_list = db.get_all_courses()
        context = dict(course_list=course_list)
        return HttpResponse(template.render(context, request))
