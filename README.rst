.. warning:: This package is not in active development. It's likely not functional
             with the latest Python and/or Django version. If you like to take over
             the project please contact me. 

====================
django-frontendadmin
====================

django-frontendadmin is a set of templatetags to allow an easy and unobstrusive
way to edit model-data in the frontend of your page.

Example project
===============

This package provides an easy example project, a weblog with comments. Here is
a quick step-by-step guide how to get this running quickly:

1. Open your terminal and cd to the ``django-frontendadmin/example_project/`` directory.
2. ``$ ./manage.py syncdb`` and create a superuser.
3. ``$ ./manage.py runserver`` and point your browser to ``http://127.0.0.1:8000/admin/``.
4. Authenticate yourself with the username/password you provided in step 2.
5. Go to the frontpage ``http://127.0.0.1:8000/`` and start playing.
6. Put some beer in your fridge and call me. :-)

Quick installation instruction
==============================

1. Put ``frontendadmin`` in your ``INSTALLED_APPS`` in the settings.py of your
   django project.

2. Add ``django.core.context_processors.request`` to your ``TEMPLATE_CONTEXT_PROCESSORS``
   in the settings.py of your django project. If this is not available (default since
   some days) put this snippet into your settings::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.request',
        'django.core.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
    )

3. Include frontendadmin urls in your urlsconf::

    (r'^frontendadmin/', include('frontendadmin.urls')),

4. Load the ``frontendadmin_tags`` library in every template you want to use
   the frontendamin links. (see below)::

    {% load frontendadmin_tags %}

5. There are three templatetags to either create, change or delete objects::

    {% frontendadmin_add queryset_of_objects label_for_link %}
    {% frontendadmin_change object_to_change label_for_link %}
    {% frontendadmin_delete object_to_delete label_for_link %}

   Assumed that you have a weblog application and using generic-views, your
   template might look so::

    {% for entry in object_list %}
    <div>
      <h2>{{ entry.title }}</h2>
      {{ entry.body }}
    <div>
    {% endfor %}

   A proper implementation of frontendadmin would be::

    {% frontendadmin_add object_list %}
    {% for entry in object_list %}
    <div>
      <h2>{{ entry.title }}</h2>
      {{ entry.body }}
      {% frontendadmin_change entry %}
      {% frontendadmin_delete entry %}
    <div>
    {% endfor %}

   Custom labels can be used as the last argument to any tag::

    {% frontendadmin_add object_list 'Post an entry' %}
    {% for entry in object_list %}
    <div>
      <h2>{{ entry.title }}</h2>
      {{ entry.body }}
      {% frontendadmin_change entry 'Edit this entry' %}
      {% frontendadmin_delete entry 'Remove it permanently' %}
    <div>
    {% endfor %}

6. Thats all. Frontendadmin will automatically check whether the current user has
   add/change/delete permissions for the given model.

   Frontendadmin has build-in ajax support using the jquery library. See the
   template-sources for details.

Custom Configuration
====================
1. Admin forms will be used if registered with the model you are trying to use. If you have
   a model admin called ``EntryAdmin`` registered with ``django.contrib.admin.site`` then 
   frontendadmin will use any form associated with, specified in ``EntryAdmin.Meta.form``.

2. You can also set which forms will be used for a specific model. The forms may
   be in your codebase, or anywhere on your python path. This is handy for custom widgets
   like split datetime fields and WYSIWYG editors. Set the following settings
   directives to see custom forms in action::

    FRONTEND_FORMS = {
        'blog.entry': 'blog.forms.EntryForm',
    }

   In this example, the ``entry`` model in the ``blog`` app will be rendered with
   the ``EntryForm`` within the ``blog.forms`` module. The key for the
   dictionary is ``app_label`` . ``model_name`` and must be all lower case.
   The value of the dictionary is ``module_name`` . ``form_class`` and must match
   the capitalization of the actual module. 

3. You may define which fields to include or exclude on a per model basis
   from inside your settings. Here is a snippet that blocks a user from being
   able to change the ``user`` field on their profile and limits them to only
   information that they should be able to edit::

    FRONTEND_EXCLUDES = {
        'profiles.userprofile': ('user',)
    }
    FRONTEND_INCLUDES = {
        'profiles.userprofile': ('address1','address2','avatar')
    }

   This will include the ``address1``, ``address2``, and ``avatar`` fields
   and exclude the ``user`` field from the form. Notice the key for both
   dictionaries is ``app_label`` . ``model_name`` and must be all lower case.

   
4. Custom form templates will be used by default if they exist. For a model
   named ``entry`` in the app ``blog`` the frontendadmin will try to use
   ``frontendadmin/blog_entry_form.html`` for the full form and ``frontendadmin/blog_entry_form_ajax.html``
   for the ajax form. If they do not exist, the defaults will be used.

License
=======

The application is licensed under the ``New BSD License``. See the LICENSE File
for details.
