# Create user
# Change user

from django import forms


class CreateUser(forms.Form):
    user_name = forms.CharField(label='Name', max_length=64, required=True)
    email = forms.EmailField(label='E-mail', max_length=128, required=True)

    # Phones should be reconstructed
    # by adding regex + frontend
    phone = forms.CharField(label='Phone', max_length=16)
    m_phone = forms.CharField(label='Mobile phone', max_length=16)

    status = forms.ChoiceField(label='Status', choices=[(True, 'Active'), (False, 'Inactive')])
