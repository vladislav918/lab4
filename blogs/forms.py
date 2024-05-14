from django import forms
from .models import Post, Comment
from django_ckeditor_5.widgets import CKEditor5Widget


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["name", "description", "featured_image", "category", "tag"]
        widgets = {
              'description': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="description"
              )
          }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["name", "description", "featured_image", "category"]
        widgets = {
              'description': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="description"
              )
          }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
              'body': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="comment"
              )
          }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False
