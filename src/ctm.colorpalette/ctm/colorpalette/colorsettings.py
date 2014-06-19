# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.autoform import directives as form
from plone.supermodel import model

from Products.CMFCore.utils import getToolByName

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import Invalid
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from collective.z3cform.colorpicker.colorpickeralpha import ColorpickerAlphaFieldWidget
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue

from colorops import RGBColor

from ctm.colorpalette import MessageFactory as _



### Validation functions ###################

def colorIsValid(value):
    value_c = value
    if value_c == None:
        raise Invalid(_(u"You cannot choose a transparent color."))
    if value_c[0] == '#':
        value_c = value_c[1:]
    if len(value) > 6:
        value_c = value_c[:6] 
    color = '0x'+value_c
    color = int(color, 16)
    color = RGBColor(color)
    if color.contrast_ratio(0xFFFFFF) < 2.0:
        raise Invalid(_(u"Color too light. Please choose a darker one."))
    return True

def logoIsValid(value):
    width, height = value.getImageSize()
    if 55 <= height <= 65:
        raise Invalid(_(u"Logo height must be in the 55px to 65px range."))
    if 45 <= widht <= 450:
        raise Invalid(_(u"Logo width must be in the 45px to 450px range."))
    return True

def faviconIsValid(value):
    width, height = value.getImageSize()
    if width > 16 or height > 16:
        raise Invalid(_(u"Favicon size must be 16x16 px."))
    return True

def backgroundIsValid(value):
    height = value.getImageSize()[1]
    if 110 <= height <= 120:
        raise Invalid(_(u"Background image height must be between 110px and 120px."))
    return True



### Vocabularies for schema.Choice ###################

FooterPortletsVocabulary = SimpleVocabulary([
        SimpleTerm(value=u'recommended', title=_(u'Automatically apply a color from the site palette (recommended)')),
        SimpleTerm(value=u'own', title=_(u'Apply the color defined below')),
        SimpleTerm(value=u'any', title=_(u'Leave it uncolored'))
        ])






class IColorSettings(model.Schema, IImageScaleTraversable):
    """
    Descriu una interficie pel paquet
    """

    # Imatges del portal
    model.fieldset('images',
                   label=_(u"Site images"),
                   fields=['logo', 'background','favicon']
                   )

    logo = NamedBlobImage(
        title=_(u"Logo of the project"),
        description=_(u'Width must be between 45 and 450 px. Height must be between 55 and 65 px. A transparent backgrounded image is recommended.'),
        required=False,
        constraint=logoIsValid,
        )

    background = NamedBlobImage(
        title=_(u"Header background image"),
        description=_(u'A height between 100 and 120 px is required.'),
        required=False,
        constraint=backgroundIsValid,
        )

    favicon = NamedBlobImage(
        title=_(u"Favicon image"),
        description=_(u'An image of 16x16 px is required.'),
        required=False,
        constraint=faviconIsValid,
        )

    # Color principal del portal
    model.fieldset('colorp',
                   label=_(u"Main color"),
                   fields=['color']
                   )

    form.widget(color=ColorpickerAlphaFieldWidget)
    color = schema.TextLine(
        title=_(u"Main color of the site"),
        description=_(u"The site will be globally themed with the selected color."),
        required=False,
        default=u'205c90',
        constraint=colorIsValid,
        )
    

    # Color de fons dels portlets
    model.fieldset('colorportlets',
                   label=_(u"Portlets background color"),
                   fields=['portlets_apply', 'portlets_bgcolor']
                   )
    
    portlets_apply = schema.Choice(
        title=_(u"Choose the portlets background coloring policy"),
        vocabulary=FooterPortletsVocabulary,
        required=True,
        default=u'any',
        )

    form.widget(portlets_bgcolor=ColorpickerAlphaFieldWidget)
    portlets_bgcolor = schema.TextLine(
        title=_(u"Portlets background color"),
        description=_(u"This color will be applied according to the policy selected before."),
        required=False,
        default=u'ffffff',
        )

    # Pagina footer
    model.fieldset('footerpage',
                   label=_(u"Footer content"),
                   fields=['pfooter']
                   )

    pfooter = RichText(
        title=_(u"Footer text"),
        description=_(u"Content of the site footer."),
        required=False,
        ) 


    # Color de fons del footer
    model.fieldset('colorfooter',
                   label=_(u"Footer background color"),
                   fields=['footer_apply', 'footer_bgcolor']
                   )

    footer_apply = schema.Choice(
        title=_(u"Choose the footer background coloring policy"),
        vocabulary=FooterPortletsVocabulary,
        required=True,
        default='recommended',
        )

    form.widget(footer_bgcolor=ColorpickerAlphaFieldWidget)
    footer_bgcolor = schema.TextLine(
        title=_(u"Footer background color"),
        description=_(u"This color will be applied according to the policy selected before."),
        required=False,
        default=u'ffffff',
        )


