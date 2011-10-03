import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
from django.db import models
from django.utils.unittest import TestCase

from supergeneric.views import AllInOneView


class DjangoSupergenericTests(TestCase):

    def test_001_pk_name_generation(self):
        """
        Tests that all AllInOneView class attributes could be calculated from 
        Model class only.
        """
        class TestModel(models.Model):
            class Meta:
                app_label = 'test'

        class TestAllInOneView(AllInOneView):
            model = TestModel

        self.assertEqual(TestAllInOneView.pk_name, 'testallinoneview_pk',
            'pk_name generation fail')

    def test_002_get_queryset_security(self):
        """
        Tests on Github#3 "Honor EmptyQuerySet".
        """
        class TestModel(models.Model):
            class Meta:
                app_label = 'test'

        class TestAllInOneView(AllInOneView):
            model = TestModel

            @classmethod
            def get_queryset(cls, request, **kwargs):
                eqs = models.query.EmptyQuerySet()
                eqs.test_flag = True
                return eqs

        list_view = TestAllInOneView.ListView()
        list_view.request = object()
        list_view.kwargs = {}

        qs = list_view.get_queryset()
        self.assertTrue(qs.test_flag,
            'Github#3 "Honor EmptyQuerySet" regression fail')
