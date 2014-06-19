# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from css_pattern import CTM_CSS, obtainPalette
from Products.CMFCore.utils import getToolByName


def normalize_rgb(color, hash=False):
    """
    Returns a RGB color without alpha channel and with and optional
    hash prefix.

    >>> normalize_rgb('FAFAFA')
    FAFAFA
    >>> normalize_rgb('fafaFAFAFA')
    FAFAFA
    >>> normalize_rgb('FAFAFABB')
    FAFAFA
    >>> normalize_rgb('FAFAfa', True)
    #FAFAFA
    """
    if color[0] == '#': 
        color = color[1:] 
    if len(color) > 6: 
        color = color[:6]
    if hash:
        color = '#' + color
    return color

    

class CssView(grok.View):
    """
    Renders a css file that modifies the sunburst theme to become the
    ctm theme. It is dynamically build after fetching (the only) CTM
    setup object that configures it.
    """
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('ctm-theme-css')

    def render(self):
        response = self.request.response
        report = self.context
        response.setHeader('Content-Type', 'text/css; charset=utf-8')        
        
        pc = getToolByName(self.context, 'portal_catalog')
        result = pc.searchResults(portal_type='ctm.ColorSettings', sort_limit=1)[0]
        colorsettings = result.getObject()
        path          = result.getURL()

        # Compute the logo and its size
        if colorsettings.logo:
            width1 = colorsettings.logo.getImageSize()[0] 
            height1 = colorsettings.logo.getImageSize()[1]
            proportion = float(height1)/width1
            if height1 > 200:
                logo = path + "/@@images/logo/mini"
                width = "200"
                height = str(proportion*int(width))

            elif height1 < 100:
                logo = path + "/@@images/logo/mini"
                height = "100"
                width = str(int(height)/proportion)
                
            else:
                logo = path + "/@@images/logo"
                width = str(width1)
                height = str(height1)
        else:
            logo = path + "/++resource++ctm.colorpalette/ctm-logo.png"
            width = "373"
            height = "65"


        #Tractem la imatge de fons
        fondo = path + "url(/@@images/background)" if colorsettings.background else 'none'

        # Compute the color palette
        color = colorsettings.color
        (N1, N2, N3, L1, L2) = obtainPalette(normalize_rgb(color))
        
        # Compute portlets background color
        portlets_bg = "#FFFFFF"
        if colorsettings.portlets_apply == 'recommended':
            portlets_bg = N3
        elif colorsettings.portlets_apply == 'own':
            portlets_bg = normalize_rgb(colorsettings.portlets_bgcolor, True)
                
        # Compute footer background color
        footer_bg = "#FFFFFF"
        if colorsettings.footer_apply == 'recommended':
            footer_bg = N3
        elif colorsettings.footer_apply == 'own':
            footer_bg = normalize_rgb(colorsettings.footer_bgcolor, True)

        return CTM_CSS % {'nivell1': N1,
                          'nivell2': N2,
                          'nivell3': N3,
                          'links1': L1,
                          'links2': L2,
                          'logo': logo,
                          'portlets_bg': portlets_bg,
                          'footer_bg': footer_bg,
                          'logowidth': width,
                          'logoheight' : height,
                          'background_image': fondo,
                          } 

    def update(self):
        self.request.set('disable_border', True)


