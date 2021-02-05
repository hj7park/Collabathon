from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import Post,Comment,User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import SignUpForm,CommentForm,EditForm,PostForm
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

# def home(request):
#     return render(request, 'home.html')

# def about(request):
#     return render(request, 'about.html')

# def singup_method(request):
#   #request.POST['name']
#   return


#any time you want to access Users object,

def signup(request):
  error_message = ''
  if request.method == 'POST':
      # This is how to create a 'user' form object
      # that includes the data from the browser
      user_form = SignUpForm(request.POST)
      if user_form.is_valid():
          user_form.save()
          u  = user_form.cleaned_data.get('email')
          p = user_form.cleaned_data.get('password1')
          user = authenticate(username=u,password=p)
          if user is not None:
            dj_login(request, user)
            return redirect('post_index')
          else:
            # authenticated failed
            error_message = 'Invalid sign up - try again'
      else:
        error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = SignUpForm()
  context = {'form': form,'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def login(request):
  error_message = ''
  email = request.POST['email']
  password = request.POST['password']
  user = authenticate(username=email,password=password)
  if user is not None:
      dj_login(request, user)
      return redirect('post_index')
  else:
      # authenticated failed
      error_message = 'Invalid sign up - try again'
      return redirect('post_index')

# @login_required
# def signup_info(request):
#   profile_form =ProfileForm()
#   context = {'profile_form': profile_form}
#   return render(request, 'registration/signup-info.html', context)


# def add_user(request):
#   form = ProfileForm(request.POST)
#   if form.is_valid():
#     new_profile = form.save(commit=False)
#     new_profile.user_id = request.user.id
#     new_profile.save()
#   return redirect('post_index')



def post_index(request):
  posts = Post.objects.all()
  form = SignUpForm()
  error_message = 'Invalid sign up - try again'
  context = {'posts': posts ,'form': form,'error_message': error_message}
  return render(request, 'posts/index.html', context)

@login_required
def post_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  # tempComments = post.comment_set.all()

  # comments ={}


  # for comment in tempComments:
  #     print(type(User.objects.get(id=comment.user_id)))
  #     print(User.objects.get(id=comment.user_id))
  #     print(comment.user_id)
      

  comment_form = CommentForm()
  return render(request, 'posts/detail.html', { 'post': post , 'comment_form': comment_form})

class postCreate(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
      # Assign the logged in user (self.request.user)
      form.instance.author = self.request.user  # form.instance is the Post
      return super().form_valid(form)

class postUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title','content']


class postDelete(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = '/'

class commentCreate(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['content']

    def get_success_url(self):
      return reverse('post_detail', kwargs={'post_id': self.kwargs['pk']})

    def form_valid(self, form):
      form.instance.user =self.request.user
      form.instance.post_id = self.kwargs['pk']
      return super().form_valid(form)

class commentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    fields = ['content']

    def get_success_url(self):
      return reverse('post_detail', kwargs={'post_id': self.kwargs['pk']})

    # def form_valid(self, form):
    #   form.instance.user =self.request.user
    #   form.instance.post_id = self.kwargs['pk']
    #   return super().form_valid(form)

class commentDelete(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
      form.instance.user = self.request.user
      form.instance.post = self.kwargs['pk']
      return super().form_valid(form)

# @login_required
# def add_comment(request, post_id):
#   form = CommentForm(request.POST)
#   if form.is_valid():
#     comment = form.save(commit=False)
#     comment.post_id = post_id
#     comment.user_id = request.user.id
#     comment.save()
#   return redirect('post_detail', post_id=post_id)

# @login_required
# def update_comment(request, post_id):
#   form = CommentForm(request.POST)
#   if form.is_valid():
#     comment = form.save(commit=False)
#     comment.post_id = post_id
#     comment.save()
#   return redirect('post_detail', post_id=post_id)

# @login_required
# def delete_comment(request, post_id):
#   form = CommentForm(request.POST)
#   if form.is_valid():
#     comment = form.save(commit=False)
#     comment.post_id = post_id
#     comment.save()
#   return redirect('post_detail', post_id=post_id)
