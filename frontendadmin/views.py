# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import get_model
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from django.views.decorators.cache import never_cache

from frontendadmin.forms import FrontendAdminModelForm, DeleteRequestForm

def check_permission(request, mode_name, app_label, model_name):
    '''
    Check for proper permissions. mode_name may be either add, change or delete.
    '''
    p = '%s.%s_%s' % (app_label, mode_name, model_name)
    if request.user.has_perm(p):
        return True
    return False

def _get_instance(request, mode_name, app_label, model_name, instance_id=None):
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
        # get form for model
        instance_form = modelform_factory(model, form=FrontendAdminModelForm)
        # if instance_id is set, grab this model object
        if instance_id:
            instance = model.objects.get(pk=instance_id)
            return model, instance_form, instance
        return model, instance_form
    # Model does not exist
    except AttributeError:
        return HttpResponseForbidden('This model does not exist!')

def _handle_cancel(request, instance=None):
    '''
    Handles clicks on the 'Cancel' button in forms. Returns a redirect to the
    last page, the user came from. If not given, to the detail-view of
    the object.

    Last fallback is a redirect to the common success page.
    '''
    if request.POST.get('_cancel', False):
        if request.GET.get('next', False):
            return HttpResponseRedirect(request.GET.get('next'))
        if instance and hasattr(instance, 'get_absolute_url'):
            return HttpResponseRedirect(instance.get_absolute_url())
        return HttpResponseRedirect(reverse('frontendadmin_success')) # TODO: Abbruchtemplate
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

def _get_template(request, template_name, ajax_template_name):
    '''
    Returns wether the ajax or the normal (full html blown) template.
    '''

    try:
        if request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
            return ajax_template_name
    except KeyError:
        pass
    return template_name

@never_cache
@login_required
def add(request, app_label, model_name, mode_name='add',
                            template_name='frontendadmin/form.html',
                            ajax_template_name='frontendadmin/form_ajax.html'):

    # Get model, instance_form and instance for arguments
    instance_return = _get_instance(request, mode_name, app_label, model_name)
    if isinstance(instance_return, HttpResponseForbidden):
        return instance_return
    model, instance_form = instance_return

    # Handle cancel request
    cancel = _handle_cancel(request)
    if cancel:
        return cancel

    if request.method == 'POST':
        form = instance_form(request.POST)
        if form.is_valid():
            instance = form.save()
            # Give the user a nice message
            request.user.message_set.create(
                message=ugettext(u'Your %(model_name)s was added successfully' % \
                    {'model_name': model._meta.verbose_name}))
            # Return to last page
            return _handle_repsonse(request, instance)
    else:
        form = instance_form()

    template_context = {
        'action': 'add',
        'action_url': request.build_absolute_uri(),
        'model_title': model._meta.verbose_name,
        'form': form,
    }

    return render_to_response(
        _get_template(request, template_name, ajax_template_name),
        template_context,
        RequestContext(request)
    )

@never_cache
@login_required
def change(request, app_label, model_name, instance_id, mode_name='change',
                                           template_name='frontendadmin/form.html',
                                           ajax_template_name='frontendadmin/form_ajax.html'):

    # Get model, instance_form and instance for arguments
    instance_return = _get_instance(request, mode_name, app_label, model_name, instance_id)
    if isinstance(instance_return, HttpResponseForbidden):
        return instance_return
    model, instance_form, instance = instance_return

    # Handle cancel request
    cancel = _handle_cancel(request)
    if cancel:
        return cancel

    if request.method == 'POST':
        form = instance_form(request.POST, instance=instance)
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
        _get_template(request, template_name, ajax_template_name),
        template_context,
        RequestContext(request)
    )


@never_cache
@login_required
def delete(request, app_label, model_name, instance_id, mod_name='delete',
                               template_name='frontendadmin/form.html',
                               ajax_template_name='frontendadmin/form_ajax.html',
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
        _get_template(request, template_name, ajax_template_name),
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
