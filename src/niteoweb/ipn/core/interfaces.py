# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements


class IIPN(Interface):
    """Definition of the IPN adapter."""

    def enable_member():
        """TODO"""

    def disable_member():
        """TODO"""


# Exceptions
class NiteowebIpnCoreError(Exception):
    """Exception class for the niteoweb.ipn.core package."""


class ProductGroupNotFoundError(NiteowebIpnCoreError):
    """Exception for when the product group is not found."""


class MissingParamError(NiteowebIpnCoreError):
    """Exception raised when a required parameter is not found."""


class InvalidParamValueError(NiteowebIpnCoreError):
    """Exception raised when a parameter has an invalid value."""


# Events
class INiteowebIpnCoreEvent(Interface):
    """Base class for niteoweb.ipn.core events."""


class IMemberEnabledEvent(INiteowebIpnCoreEvent):
    """Interface for MemberEnabledEvent."""
    username = Attribute("Username of enabled member.")


class MemberEnabledEvent(object):
    """Emmited when a member is enabled."""
    implements(IMemberEnabledEvent)

    def __init__(self, context, username):
        self.context = context
        self.username = username


class IMemberDisabledEvent(INiteowebIpnCoreEvent):
    """Interface for MemberDisabledEvent."""
    username = Attribute("Username of disabled member.")


class MemberDisabledEvent(object):
    """Emmited when a member is disabled."""
    implements(IMemberDisabledEvent)

    def __init__(self, context, username):
        self.context = context
        self.username = username
