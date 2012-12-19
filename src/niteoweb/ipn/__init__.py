# -*- coding: utf-8 -*-
"""Init and utils."""
import pdb; pdb.set_trace( )
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('niteoweb.ipn')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
