from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import password_validation
from django import forms
from users.models import Profile

class NameInput(forms.MultiWidget):
    def __init__(self, attrs=None, first_attrs=None, last_attrs=None):
        widgets = (
            forms.TextInput(
                attrs=attrs if first_attrs is None else first_attrs,
            ),
            forms.TextInput(
                attrs=attrs if last_attrs is None else last_attrs,
            ),
        )
        super().__init__(widgets, attrs=attrs)

    template_name = 'main_app/forms/widgets/name.html'
    def decompress(self, name):
        if name:
            return [name['first_name'], name['last_name']]
        return ['', '']

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        if not isinstance(value, list):
            value = self.decompress(value)
        
        final_attrs = context['widget']['attrs']
        final_attrs.pop('type', None)
        id_ = final_attrs.get('id')
        subwidgets = []
        for i, widget in enumerate(self.widgets):
            widget_name = '%s_%s' % (name, i)
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                widget.attrs['id'] = '%s_%s' % (id_, i)
            subwidgets.append(widget.get_context(widget_name, widget_value, widget.attrs)['widget'])
        context['widget']['subwidgets'] = subwidgets
        return context

class NameField(forms.MultiValueField):
    def __init__(self, **kwargs):
        super().__init__([
            forms.CharField(), forms.CharField()
        ], **kwargs)

    def compress(self, data_list):
        print(data_list)
        return {'first_name':data_list[0], 'last_name':data_list[1]}

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length = 254, widget = forms.TextInput(attrs = {'class':'form-control'}))
    password = forms.CharField(label = "Password", widget = forms.PasswordInput(attrs = {'class':'form-control'}))

class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs = {"class":"form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs = {"class":"form-control"}),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs = {"class":"form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs = {"class":"form-control"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    field_order = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        profile = Profile.objects.get(user=user)
        profile.email = self.cleaned_data['email']
        if commit:
            profile.save()
        return profile