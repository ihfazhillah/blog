from django import forms
from .models import Comment

class BsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BsModelForm, self).__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            classes = self.fields[field].widget.attrs.get('class')

            if classes is not None:
                classes += ' form-control mb-2'
            else:
                classes = 'form-control mb-2'

            self.fields[field].widget.attrs.update({
                'class': classes
            })

class CommentForm(BsModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

