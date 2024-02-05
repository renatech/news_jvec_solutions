from django.db import models
from django.shortcuts import reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    post_number = models.IntegerField(null=True, blank=True, default=0)
    posted_by = models.CharField(max_length=200,default="")
    hacker_news_id = models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_like')

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-date').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
