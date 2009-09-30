from django import template
from django.db.models import Model
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from views import check_permission


def frontendadmin_add(context, queryset_object, **kwargs):

    # Check if `queryset_object` is a queryset
    if not isinstance(queryset_object, QuerySet):
        raise template.TemplateSyntaxError, "'%s' argument must be a queryset" % queryset_object

    app_label = queryset_object.model._meta.app_label
    model_name = queryset_object.model._meta.module_name

    template_context = {
        'add_link': reverse('frontendadmin_add', kwargs={
            'app_label': app_label,
            'model_name': model_name,
        }),
        'next_link': context['request'].path,
        'label': kwargs.pop('label',None),
    }

    # Check for permission
    if check_permission(request=context['request'], mode_name='add',
                                                    app_label=app_label,
                                                    model_name=model_name):
        template_context['has_permission'] = True
    return 'frontendadmin/link_add.html', template_context

frontendadmin_add.function = 1
frontendadmin_add.takes_context = 1
frontendadmin_add.is_inclusion = 1

def frontendadmin_change(context, model_object, **kwargs):

    # Check if `model_object` is a model-instance
    if not isinstance(model_object, Model):
        raise template.TemplateSyntaxError, "'%s' argument must be a model-instance" % model_object

    app_label = model_object._meta.app_label
    model_name = model_object._meta.module_name

    template_context = {
        'edit_link': reverse('frontendadmin_change', kwargs={
            'app_label': app_label,
            'model_name': model_name,
            'instance_id': model_object.pk,
        }),
        'next_link': context['request'].path,
        'label': kwargs.pop('label',None),
    }

    # Check for permission
    if check_permission(request=context['request'], mode_name='change',
                                                    app_label=app_label,
                                                    model_name=model_name):
        template_context['has_permission'] = True
    return 'frontendadmin/link_edit.html', template_context

frontendadmin_change.function = 1
frontendadmin_change.takes_context = 1
frontendadmin_change.is_inclusion = 1


def frontendadmin_delete(context, model_object, **kwargs):

    # Check if `model_object` is a model-instance
    if not isinstance(model_object, Model):
        raise template.TemplateSyntaxError, "'%s' argument must be a model-instance" % model_object

    app_label = model_object._meta.app_label
    model_name = model_object._meta.module_name

    template_context = {
        'delete_link': reverse('frontendadmin_delete', kwargs={
            'app_label': app_label,
            'model_name': model_name,
            'instance_id': model_object.pk,
        }),
        'next_link': context['request'].path,
        'label': kwargs.pop('label',None),
    }

    # Check for permission
    if check_permission(request=context['request'], mode_name='delete',
                                                    app_label=app_label,
                                                    model_name=model_name):
        template_context['has_permission'] = True
    return 'frontendadmin/link_delete.html', template_context

frontendadmin_delete.function = 1
frontendadmin_delete.takes_context = 1
frontendadmin_delete.is_inclusion = 1

def frontendadmin_common_css():
    return 'frontendadmin/common.css', {}
frontendadmin_common_css.function = 1
frontendadmin_common_css.is_inclusion = 1

def frontendadmin_common_js():
    return 'frontendadmin/common.js', {}
frontendadmin_common_js.function = 1
frontendadmin_common_js.is_inclusion = 1

