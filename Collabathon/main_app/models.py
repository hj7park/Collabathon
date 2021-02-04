from django.db import models
# Import the User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from tinymce.models import HTMLField
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from django.contrib.postgres.fields import ArrayField

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    newsLetter = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE) #user_id
#     name = models.CharField(max_length=100)
#     newsletter = models.BooleanField(default=False)
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = HTMLField()
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    # user(one) to Post(many)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    # author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.id})


class Image(models.Model):
    url = models.CharField(max_length=200)
    # Post(one) to Images(many)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Photo for post_id: {self.post_id} @{self.url}"

class Category(models.Model):
    category = ArrayField(models.CharField(max_length=200), blank=True)
    # Post(one) to Categorys(many)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Tag(models.Model):
    tag = ArrayField(models.CharField(max_length=200), blank=True)
    # Post(one) to Tags(many)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.CharField(max_length=250)
     # user(one) to Comments(many)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']