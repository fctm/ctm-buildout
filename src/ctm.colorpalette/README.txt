================
CTM.COLORPALETTE
================

:Author: Ferran Llamas Arroniz
:Contact: llamas.arroniz@gmail.com
:organization: Universitat Politècnica de Catalunya
:date: 02/07/2013

Introduction
============
This product installs a new content type using Dexterity engine which
basically provides a panel for color and logo settings of the
site.

The values of these settings are stored in the catalog and read by
some custom views, which are also defined in this package, that
generates standalone views for the css stylesheet, the favicon image,
the logo image, and the footer page.

All those views are then treated by the ctm.theme package, which
includes them into theme.html as external content.

Configuration Panel
===================
The configuration panel is a simple schema that stores information
related to the desired aspect and feel of the site into the catalog.
It is also defined as a new content type using the plone.app.dexterity
package.

The settings which can be configured are:

 * The logo image of the site
 * The header background image
 * The favicon image
 * The main color of the site
 * The portlets background color
 * The footer page and its background color

So as to separate different parts of the configuration, the
plone.supermodel package has been used::

    model.fieldset('images',
                   label=_(u"Site images"),
                   fields=['logo', 'background','favicon']
                   )

Here we define a section of our panel, which contains three different
schema fields and will be displayed in a different window. There are
five different fieldsets in our panel:

 * Site images
 * Main color
 * Portlet background color
 * Footer page
 * Footer background color

In order to properly save the images, we have used the following packages::

   from plone.namedfile.interfaces import IImageScaleTraversable
   from plone.namedfile.field import NamedBlobImage

Which allow us to save the images as blob files and to be
scalable. Example given::

    class IColorSettings(model.Schema, IImageScaleTraversable):
           
          ... 
            
    	  logo = NamedBlobImage(
               title=_(u"Logo of the project"),
               description=_(u'Select the logo for the site.'),
               required=False,
               constraint=logoIsValid,
	       )

	  ...

Note tha constraint label, in which a name of a function is given so
as to validate the input of the schema field.

To select the colors, we have used the collective.colorpicker package,
which provides powerfull color picker widgets::

    from collective.z3cform.colorpicker.colorpickeralpha import ColorpickerAlphaFieldWidget

    ...
    
    form.widget(color=ColorpickerAlphaFieldWidget)
    color = schema.TextLine(
        title=_(u"Main color of the site"),
        description=_(u"The site will be globally themed with the selected color."),
        required=False,
        default=u'205c90',
        constraint=colorIsValid,
        )

In the case of the footer page, a RichText field is used so as to
provide a text editor field. The content of that field, as well as the
css or the favicon, will be rendered in a standalone view and then
externally included by the ctm.theme package::

    pfooter = RichText(
        title=_(u"Footer text"),
        description=_(u"Edit this page with the desired aspect and feel for the site footer"),
        allowed_mime_types=('text/plain','text/html','text/x-rst', 'text/structured',),
        default=RichTextValue(u"<html><head></head><body><br></body></html>", 'text/html', 'text/html'),
        required=False,
        )

The default value is set that way because the diazo rule needs
something in the view to extract and put into the footer.

Standalone Views
================
Three different standalone views are defined in the package:

 * Css view: it is defined in css_view.py and creates a text/css page named /@@css_view.
 * Favicon view: defined in favicon_view.py and creates a image/png page named /@@favicon_view.
 * Footer view: defined in footer_view.py and creates a text/html page named /@@footer_view.

Those three views are created using the five.grok engine.

Css View
--------
The main purpose of this view is to provide the desired stylesheet
calculated from the configuration panel catalog entries.

It includes a css pattern, defined in css_pattern.py, in which the
different color levels are placed strategically to configure an
harmonic look and feel derived from the main color.

The procedure is simple. We search into the catalog for the object
containing our configuration panel::

    pc = getToolByName(self.context, 'portal_catalog')
    result = pc.searchResults({'portal_type':'ctm.ColorSettings'})[0]
    path = result.getURL()
    colorsettings = result.getObject()

Once we got the object, we query for its properties (color, logo,
footer text, etc) and calculate the final css stylesheet.  A
supplementary library has been used to treat with color
transformations and property calculous. This library is named
colorops, and provides an implementation of a RGBColor or a HSVColor
class.

The logo image of the site is also included through the stylesheet
generated for this view::

    body #ctm-logo div {
        background-image: url("%(logo)s");
        width: %(logowidth)spx;
    	height: %(logoheight)spx;
    }

Where the url to the logo is previously calculated from the panel
field.


Favicon View
------------
This view is very similar to the css_view.py, and its only function is
to query the binary data of the foto from the catalog and show it
properly in the view.

Footer view
-----------
Exactly as the favicon view, this one just queries for the html data
into the panel field, which is stored into the catalog, and makes is
visible for the ctm.theme package.


