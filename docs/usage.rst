=====
Usage
=====

To use drf-querystringfilter in a project::

    import drf_querystringfilter


Configure your view to use it::

    class DemoModelView(ListAPIView):
        filter_backends = (QueryStringFilterBackend,)

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

.. _gt:
.. _greater_than:


gt/gte
------
::

    ?int__gt=5


lt/lte
------
::

    ?int__lt=5

is
--
::

    ?flag__is=1
    ?flag__is=true

or ::

    ?flag__is=0
    ?flag__is=false


isnull
------
::

    ?flag__isnull=true
    ?flag__isnull=false

not
---
::

    ?name__not=abc

in
--
::

    ?id__in=1,2,4

not_in
------
::

    ?id__not_in=1,2,4

inarray
-------
::

    ?json__array__inarray=a

int_inarray
-----------
::

    ?json__array__int_inarray=1

