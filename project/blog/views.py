from supergeneric.views import AllInOneView

from .forms import PostForm, CommentForm
from .models import Post, Comment


class CommentView(AllInOneView):
    """ Leave default values for most attributes """
    
    context_object_name = 'comment'
    model = Comment
    form_class = CommentForm
    owner_field_name = 'author'
    create_form_in_list = True
    
    @classmethod
    def get_queryset(cls, request, **kwargs):
        """ There is parent_context from Post Detail View in kwargs if
            kwargs['as_child'] set to True """
        
        if 'as_child' in kwargs and 'post' in kwargs['parent_context']:
            post = kwargs['parent_context']['post']
            queryset = post.comment_set.all()
        else:
            queryset = None
        
        return queryset


class PostView(AllInOneView):
    """ Provide all values explicitly """
    
    paginate_by = 20
    list_template_name = 'post_list.html'
    detail_template_name = 'post.html'
    form_template_name = 'post_form.html'
    delete_template_name = 'post_delete.html'
    context_object_name = 'post'
    model = Post
    form_class = PostForm
    require_login_to_create = True
    require_owner_to_update = True
    owner_field_name = 'author'
    children = (
        ('comment', CommentView),
    )
