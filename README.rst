=====================
drf-querystringfilter
=====================

.. image:: https://badge.fury.io/py/drf-querystringfilter.png
    :target: https://badge.fury.io/py/drf-querystringfilter

Filter backend for DjangoRestFramework able to parse url parameters

Supports drf 3.5.x, 3.6.x, 3.7.x, 3.8.x Django 1.10.x, 1.11.x, 2.0.x, python 2.7, 3.6

Documentation
-------------

The full documentation is at https://drf-querystringfilter.readthedocs.org.


Basic Usage
-----------

.. code-block:: python

    class UserSerializer(ModelSerializer):
        class Meta:
            model = User
            exclude = ()


    class Users(ListAPIView):
        serializer_class = UserSerializer
        filter_fields = ['username', 'email', 'is_staff', 'date_joined']
        filter_blacklist = None
        filter_backends = (QueryStringFilterBackend,)
        queryset = User.objects.all()


now you can query using...


.. code-block:: sh

    - /users/?username=sax
    - /users/?username__startswith=sa&date_joined__year=2000
    - /users/?email__contains=@gmail.com
    - /users/?is_staff=true


Links
~~~~~

+--------------------+----------------+--------------+---------------------------+
| Stable             | |master-build| | |master-cov| |  |master-doc|             |
+--------------------+----------------+--------------+---------------------------+
| Development        | |dev-build|    | |dev-cov|    |  |dev-doc|                |
+--------------------+----------------+--------------+---------------------------+
| Project home page: |https://github.com/saxix/drf-querystringfilter             |
+--------------------+---------------+-------------------------------------------+
| Issue tracker:     |https://github.com/saxix/drf-querystringfilter/issues?sort |
+--------------------+---------------+-------------------------------------------+
| Download:          |http://pypi.python.org/pypi/drf-querystringfilter/         |
+--------------------+---------------+-------------------------------------------+
| Documentation:     |https://drf-querystringfilter.readthedocs.org/en/latest/   |
+--------------------+---------------+--------------+----------------------------+


.. |master-build| image:: https://secure.travis-ci.org/saxix/drf-querystringfilter.png?branch=master
                    :target: http://travis-ci.org/saxix/drf-querystringfilter/

.. |master-cov| image:: https://codecov.io/gh/saxix/drf-querystringfilter/branch/master/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/drf-querystringfilter

.. |master-doc| image:: https://readthedocs.org/projects/drf-querystringfilter/badge/?version=stable
                    :target: http://drf-querystringfilter.readthedocs.io/en/stable/

.. |dev-build| image:: https://secure.travis-ci.org/saxix/drf-querystringfilter.png?branch=develop
                  :target: http://travis-ci.org/saxix/drf-querystringfilter/

.. |dev-cov| image:: https://codecov.io/gh/saxix/drf-querystringfilter/branch/develop/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/drf-querystringfilter

.. |dev-doc| image:: https://readthedocs.org/projects/drf-querystringfilter/badge/?version=latest
                :target: http://drf-querystringfilter.readthedocs.io/en/latest/
