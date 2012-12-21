# -*- coding: utf-8 -*-
"""Module providing IPN actions."""

from DateTime import DateTime
from five import grok
from niteoweb.ipn.core.interfaces import IIPN
from plone import api
from Products.CMFCore.interfaces import ISiteRoot

import logging

logger = logging.getLogger("niteoweb.ipn.core")

DISABLED = 'Disabled'


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

    def enable_member(self, data):
        """Enable an existing or create a new member."""
        self.data = data
        username = self.data['email']

        # Create a member object if this is a new user
        if not api.user.get(username=username):
            logger.info("Creating a new member: %s." % username)
            self._create_new_member(data)

        # If an existing member is in group Disabled, remove him from there
        if username in api.user.get(groupname=DISABLED):
            logger.info("Removing member '%s' from Disabled group." % username)
            api.group.remove_user(groupname=DISABLED, username=username)

        # Grant Member role if member does not have it yet
        if not 'Member' in api.user.roles():
            logger.info("Granting member '%s' the Member role." % username)
            api.user.grant_roles(username=username, roles=['Member'])

        # Add member to product's group
        product_group = self._get_product_settings()['product_group']
        api.group.add_user(username=username, groupname=product_group)
        logger.info(
            "Added member '%s' to product group '%s'."
            % (username, product_group)
        )

        # Set member's validity based on his product_id
        product_validity = self._get_product_settings()['product_validity']
        valid_to = DateTime().now() + product_validity
        self.member = api.user.get(username=username)
        self.member.setMemberProperties(mapping={
            'valid_to': DateTime() + product_validity
        })
        logger.info("Member's (%s) valid_to set to %s." % (username, valid_to))

        # Write to member log
        self._write_member_log('enable_member')

        # Done!
        logger.info("Enabled member '%s'." % username)

    def disable_member(self, data):
        """Disable an existing member."""
        self.data = data
        username = self.data['email']

        self.member = api.user.get(username=username)
        if not self.member:
            raise Exception

        # Move to Disabled group if not already there
        if not username in api.user.get_users(groupname=DISABLED):
            logger.info("Adding member '%s' to Disabled group." % username)
            api.group.add_user(groupname=DISABLED, username=username)

        # Revoke 'Member' role which "disables" the user
        # TODO: get_roles dobi role od current memberja, sweet!
        if 'Member' in api.user.get_roles():
            logger.info("Revoking member '%s' the Member role." % username)
            api.user.revoke_roles(username=username, roles=['Member'])

        # Write to member log
        self._write_member_log('disable_member')

        # Done!
        logger.info("Disabled member '%s'." % username)

    def _write_member_log(self, action):
        """Add a record to member's log."""
        log = list(self.member.getProperty('log'))
        log.append('{timestamp};{product_id};{ttype};{action}'.format(
            timestamp=DateTime(),
            product_id=self.data['product_id'],
            ttype=self.data['transaction_type'],
            action=action,
        ))
        self.member.setMemberProperties(mapping={'log': log})
