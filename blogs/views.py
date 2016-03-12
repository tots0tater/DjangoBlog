from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.shortcuts import redirect

from django.utils import timezone
from datetime import datetime

# This allows us to receive all of our data
# from our local database.
from .models import BlogPost, Comment
from django.contrib.auth.models import User


class IndexView(generic.TemplateView):
    template_name = 'blogs/index.html'
    num_comments = { }

    def get_blogs(self):
        """
        Returns the published blog posts.
        """
        # We would ideally like to limit the number of blogs
        # listed, but given the time requirements, I don't think
        # that's going to happen.
        blogs = BlogPost.objects.filter(
            pub_date__lte = timezone.now()    
        ).order_by('-pub_date')

        for blog in blogs:
            # Setting our num_comments dictionary by getting
            # the number of comments from a particular blog post
            self.num_comments[blog.id] = len(Comment.objects.filter(blog_post = blog.id))

        return blogs

def post_blog(request):
    """
    When the user is a verified as being a superuser,
    they can add a blog post from this page.
    """
    title = request.POST.get("post-title")
    body = request.POST.get("post-body")

    blog = BlogPost(post_title=title, post_text=body, pub_date=timezone.now())
    blog.save()

    return redirect('/blogs/')

class RegisterView(generic.TemplateView):
    template_name = 'registration/register.html'

class BlogView(generic.DetailView):
    """
    A view that will link to a blog post. In this view,
    the blog post will have comments visible.
    """
    model = BlogPost
    template_name = 'blogs/blog_post.html'

    def get_queryset(self):
        return BlogPost.objects.filter(pub_date__lte = timezone.now())


def logout_view(request):
    logout(request)
    return redirect('/blogs/')

def create_account(request):
    """
    This function gets POST data from our register.html
    page and creates a user from that information.
    """
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    email = request.POST.get('email', False)

    # Then they didn't enter one of the fields
    if (not username or not password or not email):
        return render(request, 'registration/register.html', {
            'error_message': "ERROR. You didn't fill out every field."
        })
    
    # Otherwise, we create a user.
    User.objects.create_user(username, email, password)
    # Authenticate before we login ...
    user = authenticate(username=username, password=password)
    # ... and log them in
    login(request, user)
    return redirect('/blogs/')

def post_comment(request):
    """
    This function gets POST data from the blog_post.html
    and submits a comment to a particular blog post.
    """
    text = request.POST.get("comment-textarea", False)
    blog_id = request.POST.get("blog-id", False)
    id = request.user.id

    # Create a new comment based off of these inputs
    comment = Comment(comment_text=text, blog_post_id=blog_id, user_id=id)
    comment.save()

    # Go back to the post once we make it.
    return redirect('/blogs/' + str(blog_id))

def delete_comment(request):
    """
    This function gets POST data from the blog_post.html
    and submits a deletes to a particular blog post.
    """
    # Find our comment from the comment id and delete
    comment_id = request.POST.get("comment-id", False)
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()

    blog_id = request.POST.get("blog-id", False)
    return redirect('/blogs/' + str(blog_id))

def edit_comment(request):
    """
    This function gets POST data from the blog_post.html
    and edits a comment to a particular blog post.
    """
    comment_id = request.POST.get("comment-id", False)
    edit_text = request.POST.get("edit-comment-textbox", False)

    # Get our comment from our primary key and update it
    comment = Comment.objects.get(pk=comment_id)
    comment.comment_text = edit_text
    comment.pub_date = datetime.now()
    comment.save()

    blog_id = request.POST.get("blog-id", False)
    return redirect('/blogs/' + str(blog_id))