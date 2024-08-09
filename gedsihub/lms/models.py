from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    position = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.title} (Course: {self.course.title})'

class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('video', 'Video'),
        ('image', 'Image'),
    ]

    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    text_content = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.get_content_type_display()} Content in {self.module.title}'

class Assessment(models.Model):
    module = models.OneToOneField(Module, related_name='assessment', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Module")
    questions = models.JSONField(null=True)  # Simplified, you can expand this model based on assessment needs
    passing_grade = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'Assessment for {self.module.title}'

class Certificate(models.Model):
    user = models.ForeignKey(User, related_name='certificates', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='certificates', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Certificate for {self.user.username} - {self.module.title}'

class Enrollment(models.Model):
    user = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    progress = models.PositiveIntegerField(default=0)  # Percentage of course completed
    enrolled_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title}'

class Flair(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Forum(models.Model):
    module = models.ForeignKey(Module, related_name='forums', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flairs = models.ManyToManyField(Flair, related_name='forums')
    user = models.ForeignKey(User, related_name='forums', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} in {self.module.title}'

class Comment(models.Model):
    forum = models.ForeignKey(Forum, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.forum.title}'
