# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

class FaviconView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('ctm-theme-favicon')

    def render(self):
        response = self.request.response
        report = self.context
                
        pc = getToolByName(self.context, 'portal_catalog')
        result = pc.searchResults(portal_type='ctm.ColorSettings', search_limit=1)[0]
        colorsettings = result.getObject()
        
        # Tractem la imatge de favicon
        if colorsettings.favicon:
            content_type = colorsettings.favicon.contentType
            response.setHeader('Content-Type', content_type)        
            return colorsettings.favicon.data 
        else:
            foto = report.restrictedTraverse('/++resource++ctm.colorpalette/favicon.ico')
            response.setHeader('Content-Type', 'image/x-icon')        
            return foto.GET()

    def update(self):
        self.request.set('disable_border', True)


