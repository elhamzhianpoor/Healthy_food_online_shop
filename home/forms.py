from django import forms
from home.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body','rate']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


