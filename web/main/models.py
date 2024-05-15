from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class Lecture(models.Model):
    title = models.CharField(max_length=100)
    site = models.CharField(max_length=25)
    language = models.CharField(max_length = 25)
    level = models.IntegerField()
    skill = models.CharField(max_length= 20)
    image = models.ImageField(upload_to='home/', null =True)

    class Meta:
        db_table = "lecture"

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.content + " | " +str(self.user)
    

class UserLecture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    # 추가적인 필드를 필요에 따라 정의할 수 있습니다.
    class Meta:
        db_table = "my_lecture"

