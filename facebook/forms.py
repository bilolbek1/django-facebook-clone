from django.forms import ModelForm
from .models import Post, Review



class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'text',]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # Other form initialization code if needed
        # self.fields['image'].required = True



class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text']

