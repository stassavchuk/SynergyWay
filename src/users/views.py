import json

from django.template import loader
from django.http import HttpResponse
from django.views.generic import View

from forms import UserForm, CoursesForm
from sql.database import Database


class CreateUserView(View):
    def get(self, request):
        template = loader.get_template('create.html')
        form = UserForm()
        context = dict(form=form)
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
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


class UserListView(View):
    def get(self, request):
        template = loader.get_template('users.html')
        db = Database()
        user_list = db.get_all_users()
        context = dict(user_list=user_list)
        return HttpResponse(template.render(context, request))

    def post(self, request):
        """
        Using to delete user from database.
        :param request: request
        :return: response
        """
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
        user_courses = db.get_user_courses(user_id)

        data = {
            'user_name': user_data[1],
            'email': user_data[2],
            'status': user_data[3],
            'phone': user_data[4],
            'm_phone': user_data[5]
        }
        form = UserForm(data)
        form.fields['user_name'].widget.attrs['readonly'] = True

        hidden_form = CoursesForm()

        all_courses = json.dumps(all_courses)
        user_courses = json.dumps(user_courses)
        context = dict(form=form, all_courses=all_courses, user_courses=user_courses, hidden_form=hidden_form)
        return HttpResponse(template.render(context, request))

    def post(self, request, user_id):
        form = UserForm(request.POST or None)
        hidden_form = CoursesForm(request.POST or None)

        if form.is_valid() and hidden_form.is_valid():
            data = form.cleaned_data
            user_courses = hidden_form.cleaned_data.get('courses')

            db = Database()
            db.update_records(user_id, user_courses)
            db.update_user(user_id=user_id, **data)

            all_courses = db.get_all_courses()
            user_courses = db.get_user_courses(user_id)

            template = loader.get_template('edit.html')
            all_courses = json.dumps(all_courses)
            user_courses = json.dumps(user_courses)
            form.fields['user_name'].widget.attrs['readonly'] = True
            context = dict(form=form, success=True, all_courses=all_courses, user_courses=user_courses)

            return HttpResponse(template.render(context, request))
        else:
            db = Database()
            all_courses = db.get_all_courses()
            user_courses = db.get_user_courses(user_id)

            template = loader.get_template('edit.html')
            form = UserForm(request.POST)
            hidden_form = CoursesForm(request.POST)
            form.fields['user_name'].widget.attrs['readonly'] = True
            context = dict(form=form, hidden_form=hidden_form, all_courses=all_courses, user_courses=user_courses)
            return HttpResponse(template.render(context, request))


class CoursesView(View):
    def get(self, request):
        template = loader.get_template('courses.html')
        db = Database()
        course_list = db.get_all_courses()
        context = dict(course_list=course_list)
        return HttpResponse(template.render(context, request))
