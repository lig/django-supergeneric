from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    DeleteView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator


class AllInOneViewBase(type):
    
    def __new__(cls, *args, **kwargs):
        
        cls = type.__new__(cls, *args, **kwargs)
        
        class OwnerObjectMixin(object):
            def get_owner_object(self, queryset=None):
                object = SingleObjectMixin.get_object(self, queryset=queryset)
                if getattr(object, cls.owner_field_name) == self.request.user:
                    return object
                else:
                    raise Http404
        
        class AIOListView(ListView):
            pass
        
        class AIODetailView(DetailView):
            pass
        
        class AIOCreateView(CreateView):
            if cls.require_owner_to_update:
                def form_valid(self, form):
                    self.object = form.save(commit=False)
                    setattr(self.object, cls.owner_field_name, self.request.user)
                    self.object.save()
                    return FormMixin.form_valid(self, form)
            if cls.require_login_to_create:
                @method_decorator(login_required)
                def dispatch(self, request, *args, **kwargs):
                    return super(AIOCreateView, self).dispatch(request, *args, **kwargs)
        
        class AIOUpdateView(OwnerObjectMixin, UpdateView):
            if cls.require_owner_to_update:
                get_object = OwnerObjectMixin.get_owner_object
            if cls.require_login_to_create:
                @method_decorator(login_required)
                def dispatch(self, request, *args, **kwargs):
                    return super(AIOUpdateView, self).dispatch(request, *args, **kwargs)
        
        class AIODeleteView(OwnerObjectMixin, DeleteView):
            def get_success_url(self):
                return reverse('%s-list' % cls.context_object_name)
            if cls.require_owner_to_update:
                get_object = OwnerObjectMixin.get_owner_object
            if cls.require_login_to_create:
                @method_decorator(login_required)
                def dispatch(self, request, *args, **kwargs):
                    return super(AIODeleteView, self).dispatch(request, *args, **kwargs)
        
        cls.ListView = AIOListView
        cls.DetailView = AIODetailView
        cls.CreateView = AIOCreateView
        cls.UpdateView = AIOUpdateView
        cls.DeleteView = AIODeleteView
        
        return cls


class AllInOneView(object):
    __metaclass__ = AllInOneViewBase
    
    paginate_by = None
    list_template_name = None
    detail_template_name = None
    form_template_name = None
    delete_template_name = None
    context_object_name = None
    model = None
    form_class = None
    require_login_to_create = True
    require_owner_to_update = True
    owner_field_name = None
    
    def as_list_view(self, *args, **kwargs):
        return self.ListView.as_view(
            template_name=self.list_template_name,
            model=self.model,
            context_object_name='%s_list' % self.context_object_name,
            paginate_by=self.paginate_by)
    
    def as_detail_view(self, *args, **kwargs):
        return self.DetailView.as_view(
            template_name=self.detail_template_name,
            model=self.model,
            context_object_name=self.context_object_name)
    
    def as_create_view(self, *args, **kwargs):
        return self.CreateView.as_view(
            template_name=self.form_template_name,
            model=self.model,
            context_object_name=self.context_object_name,
            form_class=self.form_class)
    
    def as_update_view(self, *args, **kwargs):
        return self.UpdateView.as_view(
            template_name=self.form_template_name,
            model=self.model,
            context_object_name=self.context_object_name,
            form_class=self.form_class)
    
    def as_delete_view(self, *args, **kwargs):
        return self.DeleteView.as_view(
            template_name=self.delete_template_name,
            model=self.model)
    
    def get_urlpatterns(self, url_prefix):
        return patterns('',
            url(r'^%s$' % url_prefix, self.as_list_view(),
                name='%s-list' % self.context_object_name),
            url(r'^%s(?P<pk>\d+)/$' % url_prefix, self.as_detail_view(),
                name=self.context_object_name),
            url(r'^%sadd/$' % url_prefix, self.as_create_view(),
                name='%s-add' % self.context_object_name),
            url(r'^%s(?P<pk>\d+)/edit/$' % url_prefix, self.as_update_view(),
                name='%s-edit' % self.context_object_name),
            url(r'^%s(?P<pk>\d+)/delete/$' % url_prefix, self.as_delete_view(),
                name='%s-delete' % self.context_object_name))
