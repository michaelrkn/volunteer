from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Volunteer, Friend

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'username', 'password1', 'password2',)


class VolunteerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VolunteerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('submit', 'CREATE MY PAGE', css_class='btn-primary'))

    class Meta:
        model = Volunteer
        # error_messages = {
        #     NON_FIELD_ERRORS: {
        #         'unique': "This URL is taken",
        #     }
        # }
        fields = ['slug','zip_code','phone','can_text']

class FriendForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FriendForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = Friend
        fields = ['first_name','last_name','city','state']

class FriendFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# class OutvoteForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(OutvoteForm, self).__init__(*args, **kwargs)
#
#         self.helper = FormHelper(self)
#
#         self.helper.layout.append(Submit('submit', 'Submit', css_class='btn-primary'))
#
#     class Meta:
#         model = Volunteer
#
#         fields = ['phone']