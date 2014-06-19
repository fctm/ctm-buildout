# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

# your.app.package must match domain declaration in .po files
MessageFactory = MessageFactory('ctm.policy')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
