""" We don't need CommentView as it is child of PostView and there urls will
be created automagically. """
from .views import PostView


urlpatterns = PostView().get_urlpatterns('')

"""
urlpatterns += AnyOtherAllInOneView().get_urlpatterns('other_object_name/')
"""
