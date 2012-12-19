=================
niteoweb.ipn.core
=================

A Plone add-on package that acts as a base for supporting different Instant
Payment Notification providers (such as PayPal, JVZoo, Click2Sell, etc.)

* `Source code @ GitHub <https://github.com/niteoweb/niteoweb.ipn.core>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/niteoweb.ipn.core>`_
* `Documentation @ ReadTheDocs <http://niteowebipncore.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/niteoweb/niteoweb.ipn.core>`_

Subpackages
===========

You probably do not want to use this package on it's own, but rather use one
of its sub-packages:

 * `niteoweb.ipn.jvz <http://pypi.python.org/pypi/niteoweb.ipn.jvz>`_
 * `niteoweb.ipn.c2s <http://pypi.python.org/pypi/niteoweb.ipn.c2s>`_

How it works
============

This package acts as a base layer for ``niteoweb.ipn.*`` packages. It provides
the code that these sub-packages would have to otherwise duplicate:

 * Creating a new member.
 * Updating an existing member.
 * Disabling an existing member.
 * Firing off events that your project code can catch and perform custom tasks
   on.

Installation
============

You probably do not want to install `niteoweb.ipn.core` directly, but rather
use one of ``niteoweb.ipn.*`` sub-packages.

