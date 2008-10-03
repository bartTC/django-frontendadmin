====================
django-frontendadmin
====================

django-frontendadmin is a set of templatetags to allow an easy and unobstrusive
way to edit model-data in the frontend of your page.

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

    {% frontendadmin_add queryset_of_objects %}
    {% frontendadmin_change object_to_change %}
    {% frontendadmin_delete object_to_delete %}

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

6. Thats all. Frontendadmin will automatically check whether the current user has
   add/change/delete permissions for the given model.

   Frontendadmin has build-in ajax support using the jquery library. See the
   template-sources for details.

License
=======

The application is licensed under the ``New BSD License``. See the LICENSE File
for details.
