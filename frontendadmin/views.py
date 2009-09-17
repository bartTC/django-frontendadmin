# -*- coding: utf-8 -*-
from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import get_model
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.utils.translation import ugettext
from django.views.decorators.cache import never_cache
from django.utils.importlib import import_module
from django.conf import settings
from django.forms import CharField

from forms import DeleteRequestForm, FrontendAdminModelForm
from widgets import CKEditor

EXCLUDES = getattr(settings, 'FRONTEND_EXCLUDES', {})
FIELDS = getattr(settings, 'FRONTEND_FIELDS', {})
FORMS = getattr(settings, 'FRONTEND_FORMS', {})
CKEDITORS = getattr(settings, 'FRONTEND_CKEDITOR_FIELDS', {})

def import_function(s):
    """
    Import a function given the string formatted as
    `module_name.function_name`  (eg `django.utils.text.capfirst`)
    """
    a = s.split('.')
    j = lambda x: '.'.join(x)
    return getattr(import_module(j(a[:-1])), a[-1])

def check_permission(request, mode_name, app_label, model_name):
    '''
    Check for proper permissions. mode_name may be either add, change or delete.
    '''
    p = '%s.%s_%s' % (app_label, mode_name, model_name)
    return request.user.has_perm(p)

def _get_instance(request, mode_name, app_label, model_name, instance_id=None,
                                            form=None,
                                            form_fields=None,
                                            form_exclude=None):
    '''
    Returns the model and an instance_form for the given arguments. If an primary
    key (instance_id) is given, it will return also the instance.

    If the user has no permission to add, change or delete the object, a
    HttpResponse is returned.
    '''
    # Check for permission to add/change/delete this object
    if not check_permission(request, mode_name, app_label, model_name):
        return HttpResponseForbidden('You have no permission to do this!')

    try:
        model = get_model(app_label, model_name)
    # Model does not exist
    except AttributeError:
        return HttpResponseForbidden('This model does not exist!')
    label = '%s.%s' % (app_label, model_name)
    # get form for model
    if label in FORMS and not form:
        form = import_function(FORMS[label])
    elif model in site._registry and not form:
        form = site._registry[model].form
    elif form is None:
        form = FrontendAdminModelForm
    
    if label in EXCLUDES:
        form_exclude = EXCLUDES[label]
    if label in FIELDS:
        form_fields = FIELDS[label]
    if label in CKEDITORS:
        if not hasattr(form,'declared_fields'):
            setattr(form,'declared_fields',{})
        for field in CKEDITORS[label]:
            form.declared_fields.update({field:CharField(widget=CKEditor())})
    instance_form = modelform_factory(model, form=form,
                                      fields=form_fields, exclude=form_exclude)
    # if instance_id is set, grab this model object
    if instance_id:
        instance = model.objects.get(pk=instance_id)
        return model, instance_form, instance
    return model, instance_form


def _handle_cancel(request, instance=None):
    '''
    Handles clicks on the 'Cancel' button in forms. Returns a redirect to the
    last page, the user came from. If not given, to the detail-view of
    the object. Last fallback is a redirect to the common success page.
    '''
    if request.POST.get('_cancel', False):
        if request.GET.get('next', False):
            return HttpResponseRedirect(request.GET.get('next'))
        if instance and hasattr(instance, 'get_absolute_url'):
            return HttpResponseRedirect(instance.get_absolute_url())
        return HttpResponseRedirect(reverse('frontendadmin_success'))
    return None

def _handle_repsonse(request, instance=None):
    '''
    Handles redirects for completet form actions. Returns a redirect to the
    last page, the user came from. If not given, to the detail-view of
    the object. Last fallback is a redirect to the common success page.
    '''
    if request.GET.get('next', False):
        return HttpResponseRedirect(request.GET.get('next'))
    if instance and hasattr(instance, 'get_absolute_url'):
        return HttpResponseRedirect(instance.get_absolute_url())
    return HttpResponseRedirect(reverse('frontendadmin_success'))

def _get_template(request, app_label, model_name):
    '''
    Returns wether the ajax or the normal (full html blown) template.
    '''
    template_name = request.is_ajax() and 'form_ajax.html' or 'form.html'
    try:
        name = 'frontendadmin/%s_%s_%s' % (app_label, model_name, template_name)
        get_template(name)
        return name
    except TemplateDoesNotExist:
        return 'frontendadmin/%s' % template_name

@never_cache
@login_required
def add(request, app_label, model_name, mode_name='add',
                            form_fields=None,
                            form_exclude=None):

    # Get model, instance_form and instance for arguments
    instance_return = _get_instance(request, mode_name, app_label, model_name,
                                                                   form_fields=form_fields,
                                                                   form_exclude=form_exclude)
    if isinstance(instance_return, HttpResponseForbidden):
        return instance_return
    model, instance_form = instance_return

    # Handle cancel request
    cancel = _handle_cancel(request)
    if cancel:
        return cancel
    template_context = {
        'action': 'add',
        'action_url': request.build_absolute_uri(),
        'model_title': model._meta.verbose_name,
    }
    if request.method == 'POST':
        form = instance_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            # Give the user a nice message
            request.user.message_set.create(
                message=ugettext(u'Your %(model_name)s was added successfully' % \
                    {'model_name': model._meta.verbose_name}))
            # Return to last page
            return _handle_repsonse(request, instance)
        template_context.update(form=form)
        return render_to_response('frontendadmin/form_ajax.html',template_context)
    else:
        form = instance_form()

    template_context.update(form=form)
    return render_to_response(
        _get_template(request, app_label, model_name),
        template_context,
        RequestContext(request)
    )

@never_cache
@login_required
def change(request, app_label, model_name, instance_id, mode_name='change',
                                           form_fields=None,
                                           form_exclude=None):

    # Get model, instance_form and instance for arguments
    instance_return = _get_instance(request, mode_name, app_label, model_name,
                                                           instance_id,
                                                           form_fields=form_fields,
                                                           form_exclude=form_exclude)
    if isinstance(instance_return, HttpResponseForbidden):
        return instance_return
    model, instance_form, instance = instance_return

    # Handle cancel request
    cancel = _handle_cancel(request)
    if cancel:
        return cancel

    if request.method == 'POST':
        form = instance_form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
            # Give the user a nice message
            request.user.message_set.create(
                message=ugettext(u'Your %(model_name)s was changed successfully' % \
                    {'model_name': model._meta.verbose_name}))
            # Return to success page
            return _handle_repsonse(request)
    else:
        form = instance_form(instance=instance)

    template_context = {
        'action': 'change',
        'action_url': request.build_absolute_uri(),
        'model_title': model._meta.verbose_name,
        'form': form,
    }

    return render_to_response(
        _get_template(request, app_label, model_name),
        template_context,
        RequestContext(request)
    )


@never_cache
@login_required
def delete(request, app_label, model_name, instance_id,
                               delete_form=DeleteRequestForm):

    # Get model, instance_form and instance for arguments
    instance_return = _get_instance(request, mod_name, app_label, model_name, instance_id)
    if isinstance(instance_return, HttpResponseForbidden):
        return instance_return
    model, instance_form, instance = instance_return

    # Handle cancel request
    cancel = _handle_cancel(request)
    if cancel:
        return cancel

    if request.method == 'POST':
        form = delete_form(request.POST)
        if form.is_valid():
            instance.delete()
            # Give the user a nice message
            request.user.message_set.create(
                message=ugettext(u'Your %(model_name)s was deleted.' % \
                    {'model_name': model._meta.verbose_name}))
            # Return to last page
            return HttpResponseRedirect(reverse('frontendadmin_success_delete'))
    else:
        form = delete_form()

    template_context = {
        'action': 'delete',
        'action_url': request.build_absolute_uri(),
        'model_title': model._meta.verbose_name,
        'form': form,
    }

    return render_to_response(
        _get_template(request, app_label, model_name),
        template_context,
        RequestContext(request)
    )

def success(request, template_name='frontendadmin/success.html'):
    '''
    First, a view would redirect to the last page the user came from. If
    this is not available (because somebody fiddled in the url), we redirect
    to this common success page.

    Normally a user should never see this page.
    '''
    return render_to_response(template_name, {}, RequestContext(request))

def success_delete(request, template_name='frontendadmin/success_delete.html'):
    '''
    Normally a view would redirect to the last page. After delete from a object
    in a detail-view, there is no "last page" so we redirect to a unique, shiny
    success-page.
    '''
    return render_to_response(template_name, {}, RequestContext(request))
