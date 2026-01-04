from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Tag(models.Model):
        name = models.CharField(max_length=50, unique=True)

        def __str__(self):
            return self.name
    
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class LikeAndRating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_ratings')
    liked = models.BooleanField(default=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user') # Ensure one like/rating per user per post

    def __str__(self):
        return f'{"Like" if self.liked else "Dislike"} by {self.user} on {self.post}'
    
