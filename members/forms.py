from django import forms
from .models import Member

class MemberCreateForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('__all__')


class ProfilePictureForm(MemberCreateForm):

    class Meta:
        model = Member
        fields = ('profile_pic', )