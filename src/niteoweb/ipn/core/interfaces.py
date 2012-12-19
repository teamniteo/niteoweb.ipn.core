# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface


class IIPN(Interface):
    """Definition of the IPN adapter."""

    def enable_member():
        """TODO"""

    def disable_member():
        """TODO"""
