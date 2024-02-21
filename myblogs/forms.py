from django import forms
from django.forms import ModelForm
from .models import blog_post, Comment

class Blog_Form(ModelForm):
    class Meta:
        model = blog_post
        fields = '__all__'
        exclude =['like_count', 'view_count']

class BlogPost_Form(ModelForm):
    class Meta:
        model = blog_post
        fields = '__all__'

class CommentForm(ModelForm):
     class Meta:
          model=Comment
          fields="__all__"
          exclude = ['post', 'created_date', 'author']
          widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add Comments', 'rows': 3})  # Adjust rows as per your requirement
        }