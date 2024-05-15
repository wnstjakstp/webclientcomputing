from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)


    LEVEL_CHOICES = [(i, str(i)) for i in range(1, 6)]
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)

    SKILL_CHOICES = [
        ('front', 'Front-end'),
        ('back', 'Back-end'),
        ('grammar', 'Grammar'),
        ('database', 'Database'),
    ]
    skill = models.CharField(max_length=10, choices=SKILL_CHOICES, default='grammar')

    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
        ('html', 'HTML'),
        ('sql', 'SQL'),
        ('react', 'React'),
        ('spring', 'Spring'),
    ]
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='python')

    def __str__(self):
        return self.nickname  # 문자열 표현 추가

    class Meta:
        db_table = "profile"  # 테이블 이름 직접 지정

