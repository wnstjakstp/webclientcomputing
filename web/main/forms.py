from django import forms
from .models import Comment, Lecture

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']

class LectureFilterForm(forms.Form):
    LEVEL_CHOICES = [('all', 'All')] +[(i, str(i)) for i in range(1, 6)]  # 1부터 5까지의 레벨

    SKILL_CHOICES = [
        ('all','All'),
        ('front', 'Front-end'),
        ('back', 'Back-end'),
        ('grammar', 'Grammar'),
        ('database', 'Database'),
    ]
    
    LANGUAGE_CHOICES = [
        ('all','All'),
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
        ('HTML', 'HTML'),
        ('SQL', 'SQL'),
        ('react', 'React'),
        ('spring', 'Spring'),

    ]

    level = forms.ChoiceField(choices=LEVEL_CHOICES, required=False, label='레벨')
    skill = forms.ChoiceField(choices=SKILL_CHOICES, required=False, label='기술')
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=False, label='언어')