# -*- coding: utf-8 -*-
from Products.CMFCore.WorkflowCore import WorkflowException
from plone import api
from ctm.theme import MessageFactory as _

def setupVarious(context):
    # GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file
    # as a flag to check that we actually meant for this import step
    # to be run.  The file is found in profiles/default.
    if context.readDataFile('ctm.theme_various.txt') is None:
        return
    # Add additional setup code here
    createContent(context)
    
##################################################################
#### Funcions
##################################################################


def createContent(context):
    
    portal = api.portal.get()
    existing = portal.objectIds()

    if 'ctm-theme-setup' not in existing:
        obj = api.content.create(portal, 
                                 type='ctm.ColorSettings', 
                                 id='ctm-theme-setup',
                                 title=_(u'CTM Theme Setup') )
        workflowTool = api.portal.get_tool(name='portal_workflow')
        workflowTool.doActionFor(obj, 'publish')
        obj.reindexObject()
        
