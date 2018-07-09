1.0
===
* First stable release

0.7.0
=====
* abstract query_params habdling
* handle multple values in query string
* BACKWARD INCOMPATIBLE: `__in` now accept raw values and can appear multiple times
* new operators `__inlist` and `__not_inlist` to be used for backward compatibility with `__in` and `__not_in`


0.6.0
=====
* Add handling of format query param


0.5.0 18/06/2018
================
* add support for django 2.0
* add `query_params` property to allow handling POST request


0.4.0 29/05/2017
================
* add '__inarray' and  '__int_inarray' lookup to handle json/arrays lookup both str/int


0.3.0 10/10/16
==============
* add '_distinct' parameter to enable '.distinct()' queries


0.2.0 19/09/16
==============
* add 'ignore_filter' to ignore querystring arguments


0.1.0 11/09/16
==============
* First release on PyPI.
