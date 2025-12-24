from apps.core import text
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.hashers import make_password

from .enums import UserGenderEnum, UserRoleEnum
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone_number",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("phone_number",)


class LoginForm(forms.Form):
    phone_number = forms.CharField(label="شماره تماس", max_length=15)
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone_number")
        password = cleaned_data.get("password")

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist as err:
            raise forms.ValidationError(text.user_not_found) from err

        if not user.check_password(password):
            raise forms.ValidationError(text.password_incorrect)

        if not user.is_active:
            raise forms.ValidationError(text.disabled_user)

        cleaned_data["user"] = user
        return cleaned_data


class AthleteSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "national_id",
            "payment_day",
            "gender",
            "image",
        ]
        widgets = {
            "gender": forms.Select(choices=UserGenderEnum.choices),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"]
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(text.phone_already_exists)
        return phone

    def clean_national_id(self):
        nid = self.cleaned_data["national_id"]
        if User.objects.filter(national_id=nid).exists():
            raise forms.ValidationError(text.national_id_already_exists)
        return nid

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = UserRoleEnum.ATHLETE
        user.set_unusable_password()
        user.is_active = False
        if commit:
            user.save()
        return user


class CoachSignupForm(forms.ModelForm):
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="تکرار رمز عبور", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "national_id",
            "payment_day",
            "gender",
            "image",
        ]
        widgets = {
            "gender": forms.Select(choices=UserGenderEnum.choices),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"]
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(text.phone_already_exists)
        return phone

    def clean_national_id(self):
        nid = self.cleaned_data["national_id"]
        if User.objects.filter(national_id=nid).exists():
            raise forms.ValidationError(text.national_id_already_exists)
        return nid

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("رمز عبور و تکرار آن یکسان نیستند.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = UserRoleEnum.COACH
        user.password = make_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        return user


class PromoteToCoachForm(forms.Form):
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="تکرار رمز عبور", widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("رمز عبور و تکرار آن یکسان نیستند.")
        return cleaned_data
