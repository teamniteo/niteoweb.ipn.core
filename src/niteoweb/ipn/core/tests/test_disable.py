# -*- coding: utf-8 -*-
"""Tests for disable_member action."""

from DateTime import DateTime
from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.interfaces import IMemberDisabledEvent
from niteoweb.ipn.core.testing import IntegrationTestCase
from plone import api
from zope.component import eventtesting
from zope.component import queryAdapter
from zope.testing.loggingsupport import InstalledHandler

import mock


class TestDisableMember(IntegrationTestCase):
    """Test runtime flow through the disable_member() action."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)
        self.log = InstalledHandler('niteoweb.ipn.core')
        eventtesting.setUp()

        # create a test member and a test product group
        api.user.create(email='enabled@test.com')
        api.group.create(groupname='1')
        api.group.add_user(username='enabled@test.com', groupname='1')

    def tearDown(self):
        """Clean up after yourself."""
        self.log.clear()
        eventtesting.clearEvents()

    def test_required_parameters(self):
        """Test that parameters are required."""
        from niteoweb.ipn.core.interfaces import MissingParamError

        with self.assertRaises(MissingParamError) as cm:
            self.ipn.disable_member(
                email=None,
                product_id='1',
                trans_type='CANCEL',
            )
        self.assertEquals(
            cm.exception.message,
            "Parameter 'email' is missing.",
        )

        with self.assertRaises(MissingParamError) as cm:
            self.ipn.disable_member(
                email='enabled@test.com',
                product_id=None,
                trans_type='CANCEL',
            )
        self.assertEquals(
            cm.exception.message,
            "Parameter 'product_id' is missing.",
        )

        with self.assertRaises(MissingParamError) as cm:
            self.ipn.disable_member(
                email='enabled@test.com',
                product_id='1',
                trans_type=None,
            )
        self.assertEquals(
            cm.exception.message,
            "Parameter 'trans_type' is missing.",
        )

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_disable_member(self, DT):
        """Test default execution of the disable_member() action."""
        DT.return_value = DateTime('2012/01/01')

        self.ipn.disable_member(
            email='enabled@test.com',
            product_id='1',
            trans_type='CANCEL',
        )

        # test member is in Disabled group
        self.assertIn(
            'enabled@test.com',
            [user.id for user in api.user.get_users(groupname='disabled')]
        )

        # test member does not have the Member role
        self.assertNotIn(
            'Member',
            api.user.get_roles(username='enabled@test.com'),
        )

        # test event emitted
        events = list(set(eventtesting.getEvents(IMemberDisabledEvent)))
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0].username, 'enabled@test.com')

        # test member history
        self.assert_member_history(
            username='enabled@test.com',
            history=['2012/01/01 00:00:00|1|CANCEL|disable_member']
        )

        # test log output
        self.assertEqual(len(self.log.records), 3)
        self.assert_log_record(
            'INFO',
            "Adding member 'enabled@test.com' to Disabled group.",
        )
        self.assert_log_record(
            'INFO',
            "Revoking member 'enabled@test.com' the Member role.",
        )
        self.assert_log_record(
            'INFO',
            "Disabled member 'enabled@test.com'.",
        )

    def test_nonexistent_member(self):
        """Test disabling a non-existing member."""
        self.ipn.disable_member(
            email='nonexistent@test.com',
            product_id='1',
            trans_type='CANCEL',
        )

        # test log output
        self.assertEqual(len(self.log.records), 1)
        self.assert_log_record(
            'WARNING',
            "Cannot disable a nonexistent member: 'nonexistent@test.com'.",
        )

    def test_member_already_in_disabled_group(self):
        """Test that adding to disabled group is skipped if member is already
        in the group."""
        api.group.add_user(groupname='disabled', username='enabled@test.com')
        self.ipn.disable_member(
            email='enabled@test.com',
            product_id='1',
            trans_type='CANCEL',
        )

        # test log output
        for record in self.log.records:
            self.assertNotEquals(
                record.getMessage(),
                "Adding member 'enabled@test.com' to Disabled group.",
            )

    def test_member_already_without_member_role(self):
        """Test that revoking Member role is skipped if member is already
        without this role."""
        api.user.revoke_roles(username='enabled@test.com', roles=['Member', ])
        self.ipn.disable_member(
            email='enabled@test.com',
            product_id='1',
            trans_type='CANCEL',
        )

        # test log output
        for record in self.log.records:
            self.assertNotEquals(
                record.getMessage(),
                "Revoking member 'enabled@test.com' the Member role.",
            )
