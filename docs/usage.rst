=====
Usage
=====

To use drf-querystringfilter in a project::

    import drf_querystringfilter


Configure your view to use it::

    class DemoModelView(ListAPIView):
        filter_backends = (QueryStringFilterBackend,)
        filter_fields = ['username', 'email', 'is_staff', 'date_joined']
        filter_blacklist = ['.*__']  # disable any join


Filtering
=========

.. _exact:
.. _iexact:

exact/iexact
------------
::

    ?username=admin

.. _contains:
.. _substring:

contains
--------
::

    ?email__contains=@gmail

    objects.filter(email__contains="@gmail")


.. _gt:
.. _greater_than:


gt/gte
------
::

    ?int__gt=5

    objects.filter(int__gt=5)

lt/lte
------
::

    ?int__lt=5

    objects.filter(int__lt=5)


is
--
::

    ?flag__is=1
    ?flag__is=true

    objects.filter(flag=True)


or ::

    ?flag__is=0
    ?flag__is=false

    objects.filter(flag=False)

isnull
------
::

    ?flag__isnull=true
    ?flag__isnull=false


    objects.filter(flag=True)


not
---
::

    ?name__not=abc


    objects.exclude(name="abc")

in
--
::

    ?id__in=1,2,4

    objects.filter(id__in=[1,2,3])


not_in
------
::

    ?id__not_in=1,2,4

    objects.exclude(id__in=[1,2,3])

inarray
-------
::

    ?json__array__inarray=a

    objects.filter(json__array__contains=["a"])


int_inarray
-----------
::

    ?json__array__int_inarray=1

    objects.filter(json__array__contains=[1])
