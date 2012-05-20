from django import template
from django.db.models import Model
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from frontendadmin.views import check_permission
 
register = template.Library()
 
@register.inclusion_tag('frontendadmin/link_add.html', takes_context=True)
def frontendadmin_add(context, queryset_object, label=None):
 
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
        'next_link': context['request'].META['PATH_INFO'],
        'label': label,
    }
 
    # Check for permission
    if check_permission(request=context['request'], mode_name='add',
                                                    app_label=app_label,
                                                    model_name=model_name):
        template_context['has_permission'] = True
    else:
        template_context['has_permission'] = False
    context.update(template_context)
    return context
 
@register.inclusion_tag('frontendadmin/link_edit.html', takes_context=True)
def frontendadmin_change(context, model_object, label=None):
 
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
        'next_link': context['request'].META['PATH_INFO'],
        'label': label,
    }
 
    # Check for permission
    if check_permission(request=context['request'], mode_name='change',
                                                    app_label=app_label,
                                                    model_name=model_name):
        template_context['has_permission'] = True
    else:
        template_context['has_permission'] = False
    context.update(template_context)
    return context
 
@register.inclusion_tag('frontendadmin/link_delete.html', takes_context=True)
def frontendadmin_delete(context, model_object, label=None):
 
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
        'next_link': context['request'].META['PATH_INFO'],
        'label': label,
    }
 
    # Check for permission
    if check_permission(request=context['request'], mode_name='delete',
                                                    app_label=app_label,
                                                    model_name=model_name):
        template_context['has_permission'] = True
    else:
        template_context['has_permission'] = False
    context.update(template_context)
    return context
 
@register.inclusion_tag('frontendadmin/common.css')
def frontendadmin_common_css():
    return {}
 
@register.inclusion_tag('frontendadmin/common.js')
def frontendadmin_common_js():
    return {}
    
