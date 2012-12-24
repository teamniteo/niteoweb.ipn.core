# -*- coding: utf-8 -*-
"""Tests for disable_member action."""

from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.testing import IntegrationTestCase
from plone import api
from zope.component import queryAdapter
from zope.testing.loggingsupport import InstalledHandler


class TestDisableMember(IntegrationTestCase):
    """Test runtime flow through the disable_member() action."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)
        self.log = InstalledHandler('niteoweb.ipn.core')

        # create a test member and a test product group
        api.user.create(email='enabled@email.com')
        api.group.create(groupname='1')
        api.group.add_user(username='enabled@email.com', groupname='1')

    def tearDown(self):
        """Clean up after yourself."""
        self.log.clear()
        self.log.uninstall()

    def test_disable_member(self):
        """Test default execution of the disable_member() action."""
        self.ipn.disable_member(
            email='enabled@email.com',
            product_id='1',
            transaction_type='CANCEL',
        )

        # test member is in Disabled group
        self.assertIn(
            'enabled@email.com',
            [user.id for user in api.user.get_users(groupname='disabled')]
        )

        # test member does not have the Member role
        self.assertNotIn(
            'Member',
            api.user.get_roles(username='enabled@email.com'),
        )

        # TODO: test member history

        # test log output
        self.assertEqual(len(self.log.records), 3)
        self.assert_log_record(
            'INFO',
            "Adding member 'enabled@email.com' to Disabled group.",
        )
        self.assert_log_record(
            'INFO',
            "Revoking member 'enabled@email.com' the Member role.",
        )
        self.assert_log_record(
            'INFO',
            "Disabled member 'enabled@email.com'.",
        )

    def test_nonexistent_member(self):
        """Test disabling a non-existing member."""
        self.ipn.disable_member(
            email='nonexistent@email.com',
            product_id='1',
            transaction_type='CANCEL',
        )

        # TODO: test member history

        # test log output
        self.assertEqual(len(self.log.records), 1)
        self.assert_log_record(
            'WARNING',
            "Cannot disable a nonexistent member: 'nonexistent@email.com'.",
        )
