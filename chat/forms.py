from django import forms


class SignUpForm(forms.Form):
    fname = forms.CharField(max_length=50)
    lname = forms.CharField(max_length=50)
    passwd = forms.CharField(max_length=32, widget=forms.PasswordInput)

    username = forms.CharField(max_length=80)
    phn_num = forms.CharField(max_length=13)

    source = forms.CharField(max_length=50, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()

        fname = cleaned_data.get('fname')
        lname = cleaned_data.get('lname')
        passwd = cleaned_data.get('passwd')

        username = cleaned_data.get('username')
        phn_num = cleaned_data.get('phn_num')

        if not username:
            raise forms.ValidationError("You've to enter a username.")
        elif not passwd:
            raise forms.ValidationError("You've to enter a valid password.")
        elif not phn_num:
            raise forms.ValidationError("Enter a valid phone number to verify the account.")


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
