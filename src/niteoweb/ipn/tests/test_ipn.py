"""Tests for Dummy Spinner."""

from niteoweb.ipn.testing import IntegrationTestCase
from niteoweb.ipn.interfaces import IIPN
from zope.component import queryAdapter


class TestIPN(IntegrationTestCase):
    """TODO."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        # prepare the request object
        # from niteoweb.plr.interfaces import IPLRSpecific
        # alsoProvides(self.layer['app'].REQUEST, IPLRSpecific)

        # shortcuts
        self.portal = self.layer['portal']

        # # set member annotations
        # from niteoweb.plr.extspinners.dummy import KEY
        # annotations = IAnnotations(self.member)
        # annotations.setdefault(KEY, {})
        # self.config = annotations[KEY]

        # # map test content to shorter variable names
        # self.article1 = self.portal.articles.article1
        # self.article2 = self.portal.articles.article2
        # self.article3 = self.portal.articles.article3
        # self.empty_article = self.portal.articles.article6

        # # request object needs to be marked with IPloneFormLayer
        # from plone.app.z3cform.interfaces import IPloneFormLayer
        # alsoProvides(self.layer['request'], IPloneFormLayer)

    def test_ipn_registered(self):
        """TODO
        """
        ipn = queryAdapter(self.portal, IIPN)
        self.assertIsNotNone(ipn)
        ipn.enable_member()
        ipn.disable_member()
