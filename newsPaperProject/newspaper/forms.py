from django.forms import ModelForm, forms, Textarea, Select, TextInput
from .models import Post, Category
from django import forms


class PostForm(ModelForm):

# ==============================================================================

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
            label='Категория',
            widget=forms.SelectMultiple(attrs={
            'type': 'text',
            'name': 'category',
            'placeholder': 'Категория не выбрана',
            'class': 'form-control me-2',
        }))

    class Meta:
        model = Post
        
        fields = ['author', 'post_type', 'category', 'title', 'text']
        widgets = {
            'author': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите имя автора'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите тип статьи'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название статьи'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст статьи'
            }),
        }
# =====================================================