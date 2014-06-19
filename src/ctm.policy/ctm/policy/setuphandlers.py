# -*- coding: utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from ctm.policy import MessageFactory as _


logger = logging.getLogger('ctm.policy')



def setupDefault(context):
    """
    Setup handler for `default` profile
    """
    if context.readDataFile('ctm.policy-default.txt') is None:
        return
    # Add additional setup code here
    configure_portal_transforms(context)


def setupInitial(context):
    """
    Setup handler for `ctm-setup` profile
    """
    if context.readDataFile('ctm.policy-ctm-setup.txt') is None:
        return
    # Add additional setup code here
        

def configure_portal_transforms(context):
    """
    Following a hack in
    http://developer.plone.org/misc/portal_transforms.html and (more definitive)
    https://github.com/plone/plone.app.controlpanel/blob/master/plone/app/controlpanel/filter.py
    
    PortalTransforms no té api publica i cal fer hacks fastigosos per modificar-lo.
    """ 

    logger.info('Configure portal_transform safe_html settings')

    trans = getattr(getToolByName(context, 'portal_transforms'), 'safe_html')

    tconfig = trans._config

    # import pdb; pdb.set_trace()

    if 'embed' in tconfig['nasty_tags']:
        del tconfig['nasty_tags']['embed']
    if 'object' in tconfig['nasty_tags']:
        del tconfig['nasty_tags']['object']

    # valid_tags = XHTML_TAGS - stripped_tags + custom_tags

    tconfig['valid_tags']['iframe']=1
    tconfig['valid_tags']['embed']=1
    tconfig['valid_tags']['param']=0
    tconfig['valid_tags']['object']=1
    

    make_config_persistent(tconfig)

    trans._p_changed = True
    trans.reload()

        
