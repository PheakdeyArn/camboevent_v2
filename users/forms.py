from allauth.account.forms import SignupForm
from django import forms
from .models import User
from content.models.city import City

# from content.models import EventDetailPage

from .models import CommentEvent
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=CommentEvent.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = CommentEvent
        fields = ('name', 'parent', 'email', 'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        CommentEvent.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)



class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    # phone_number = forms.CharField(max_length=100)
    job = forms.CharField(max_length=100)
    # city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="(Nothing)")

    class Meta:
        model = User
        fields = ('email', 'last_name', 'phone_number', 'job')

    def signup(self, request, user):
        # Save your user
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # user.phone_number = self.cleaned_data['phone_number']
        user.job = self.cleaned_data['job']
        # user.city = self.cleaned_data['city']
        user.save()

        print(user)

        # user.profile.nationality = self.cleaned_data['nationality']
        # user.profile.gender = self.cleaned_data['bio']
        # user.user.save()
        return user

# class CustomSignupForm(SignupForm):
#
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)
#     phone_number = forms.CharField(max_length=100)
#     job = forms.CharField(max_length=100)
#
#     class Meta:
#
#         model = User
#         fields = ('email', 'last_name', 'phone_number', 'job')
#
#     def save(self, request):
#         # Ensure you call the parent class's save.
#         # .save() returns a User object.
#         user = super(CustomSignupForm, self).save(request)
#
#         # Add your own processing here.
#
#         # You must return the original result.
#         return user
