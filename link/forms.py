from django import forms


class UrlForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(
        attrs={'placeholder': 'Paste your link here...'}))
    short_url = forms.CharField(widget=forms.HiddenInput(), required=False)
