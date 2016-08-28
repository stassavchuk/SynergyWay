from django import forms
from django.core.exceptions import ValidationError
import re


class CreateUserForm(forms.Form):
    user_name = forms.CharField(label='Name', max_length=64, required=False)
    email = forms.CharField(label='E-mail', max_length=128, required=False)

    # Phones should be reconstructed
    # by adding regex + frontend
    phone = forms.CharField(label='Phone', max_length=16, required=False)
    m_phone = forms.CharField(label='Mobile phone', max_length=16, required=False)

    status = forms.ChoiceField(label='Status', choices=[(True, 'Active'), (False, 'Inactive')], required=False)

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if not user_name:
            raise ValidationError('This field is required')
        return user_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('This field is required')

        email_pattern = r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$'
        if not re.match(email_pattern, email):
            raise ValidationError('Please enter a valid email address!')

        return email


class EditUserForm(forms.Form):
    pass
