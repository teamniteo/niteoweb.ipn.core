# -*- coding: utf-8 -*-
"""Module providing IPN actions."""

from five import grok
from niteoweb.ipn.core.interfaces import IIPN
from Products.CMFCore.interfaces import ISiteRoot


class IPN(grok.MultiAdapter):
    """IPN actions."""
    grok.adapts(ISiteRoot)
    grok.implements(IIPN)

    def __init__(self, context):
        """TODO.

        :param context: Portal object.
        :type context: TODO
        """
        self.context = context

    def enable_member(self):
        """TODO
        """
        print 'enabling member'

    def disable_member(self):
        """TODO
        """
        print 'disabling member'
