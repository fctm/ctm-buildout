# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from css_pattern import CTM_CSS, obtainPalette
from Products.CMFCore.utils import getToolByName


class FooterView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('ctm-theme-footer')

    def render(self):
        response = self.request.response
        report = self.context
        response.setHeader('Content-Type', 'text/html; charset=utf-8')        
        
        pc = getToolByName(self.context, 'portal_catalog')
        result = pc.searchResults(portal_type='ctm.ColorSettings', search_limit=1)[0]
        colorsettings = result.getObject()
        if colorsettings.pfooter:
            return colorsettings.pfooter.output
        else:
            return "<span/>"

    def update(self):
        self.request.set('disable_border', True)


