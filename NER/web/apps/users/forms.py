from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django import forms
from .models import InviteCode
from django.contrib.auth import get_user_model
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    invite_code = forms.CharField(max_length=100, required=True, help_text="Enter your invite code here. If you don't have one, please write an email to admin@domain.com to request an invite code.")

    def clean_invite_code(self):
        code = self.cleaned_data.get('invite_code')
        try:
            invite = InviteCode.objects.get(code=code, is_active=True)
        except InviteCode.DoesNotExist:
            raise forms.ValidationError("This invite code is invalid or has already been used.")
        return code

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        invite_code_str = self.cleaned_data.get('invite_code')
        invite_code = InviteCode.objects.get(code=invite_code_str)
        invite_code.user = user  # Link the invite code to the user who redeems it
        invite_code.is_active = False  # Mark the invite code as consumed
        invite_code.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

# forms.py

from .models import InviteCode

class InviteCodeForm(forms.ModelForm):
    class Meta:
        model = InviteCode
        fields = []  # No fields are needed from the user