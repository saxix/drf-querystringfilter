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

substring
---------
::

    ?email__contains=@gmail

.. _gt:
.. _greater_than:


gt/gte
------
::

    ?int__lt=5


list/set
--------
::

    ?id__in=1,2,4

list/set
--------
::

    ?id__in=1,2,4

