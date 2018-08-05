from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, 
                           widget=forms.TextInput({'class': 'form-control mb-2'}))
    email = forms.EmailField(widget=forms.TextInput({'class': 'form-control mb-2'}))
    to = forms.EmailField(widget=forms.TextInput({'class': 'form-control mb-2'}))
    comment = forms.CharField(widget=forms.Textarea({'class': 'form-control mb-2'}), required=False)
