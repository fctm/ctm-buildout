## -*- coding: utf-8 -*-
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName
from plone.app.contenttypes.migration.utils import ATCT_LIST
from plone.app.contenttypes.migration.utils import isSchemaExtended

from plone.app.contenttypes.migration import vocabularies
from plone.app.contenttypes import _


def get_terms(context, counter, ext_dict, show_extended):
    results = []
    for k, v in counter.iteritems():
        if not show_extended:
            if k not in ext_dict:
                display = u"{0} ({1})".format(context.translate(_(k)), v)
                term = SimpleVocabulary.createTerm(k, k, display)
                results.append(term)
        else:
            if k in ext_dict:
                ext = str(ext_dict[k]['fields']).\
                    replace("[", "").replace("]", "")
                display = u"{0} ({1}) - extended fields: {2}".\
                    format(context.translate(_(k)), v, ext)
                term = SimpleVocabulary.createTerm(k, k, display)
                results.append(term)
    results.sort(key=lambda x: x.title)
    return results

def count(brains):
    counter = {}
    for i in brains:
        pt = i.portal_type
        if "Blob" in i.meta_type:
            if pt == "File":
                pt = "BlobFile"
            else:
                pt = "BlobImage"
        if not counter.get(pt):
            counter[pt] = 0
        counter[pt] += 1
    return counter

def results(context, show_extended=False):
    """Helper method to create the vocabularies used below.
    """
    ext_dict = {}
    ifaces = []
    for k, v in ATCT_LIST.items():
        iface = v['iface'].__identifier__
        extendend_fields = isSchemaExtended(v['iface'])
        expected = v['extended_fields']
        is_extended = len(extendend_fields) > len(expected)
        if is_extended and show_extended:
            ifaces.append(iface)
            ext_dict[k] = {}
            if expected and expected[0] in extendend_fields:
                extendend_fields.remove(expected[0])
            ext_dict[k]['fields'] = extendend_fields

        elif not show_extended and not is_extended:
            ifaces.append(iface)
    catalog = getToolByName(context, "portal_catalog")
    brains = catalog.search({'object_provides': ifaces})

    counter = count(brains)

    return SimpleVocabulary(get_terms(context,
                                      counter,
                                      ext_dict,
                                      show_extended))

vocabularies.results = results


from collective.hootsuite.interfaces import IHootsuiteRegistry
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
import datetime, time, urllib2, json, pytz, urllib
from Products.ATContentTypes.utils import DT2dt
import logging

logger = logging.getLogger("collective.hootsuite")


def update_on_modify(obj, event):
    """ We change the workflow. We check if the type is enabled and the state is published
    """
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IHootsuiteRegistry)
    if settings.portal_types and (obj.portal_type in settings.portal_types) and (event.new_state.id == 'published'):
        # Send the title to hootsuite
        dataDT = obj.getEffectiveDate()
        data = DT2dt(dataDT)
        # We send now !
        services = []
        for socialId in settings.active_services:
            services.append(int(socialId.split(" ")[-1]))
        title = obj.Title() + " " + obj.absolute_url() + " " + settings.hashtag
        if (datetime.datetime.now().replace(tzinfo=pytz.utc) > data.replace(tzinfo=pytz.utc)):
            tosend = {'message': title, 'socialNetworks': services}
        else:
            tosend = {'message': title, 'socialNetworks': services, 'sendLater': 1, 'sendAlert': 1, 'timestamp': time.mktime(data.timetuple())}

        tosend = json.dumps(tosend)
        #tosend = urllib.urlencode(tosend)
        authorization_header = "Bearer %s" % settings.token
        req = urllib2.Request(settings.urlapi + 'messages', tosend)
        req.add_header("Authorization", authorization_header)

        try:
            response = urllib2.urlopen(req)
            resultat_json = response.read()
            resultat = json.loads(resultat_json)
            logger.info("Added to HootSuite a event " + title + " " + json.dumps(resultat))
        except urllib2.HTTPError, error:
            contents = error.read()
            resultat = json.loads(contents)
            logger.error("Error on added a Hootsuite event " + title + " " + json.dumps(resultat))


from collective.hootsuite import subscriber

subscriber.update_on_modify = update_on_modify

from Acquisition import aq_inner, aq_parent
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from datetime import datetime
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import providedBy
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory
from z3c.form.interfaces import IAddForm
from Products.CMFCore.interfaces._content import IFolderish
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getMultiAdapter
import json


def get_portal():
    closest_site = getSite()
    if closest_site is not None:
        for potential_portal in closest_site.aq_chain:
            if ISiteRoot in providedBy(potential_portal):
                return potential_portal


def get_portal_url(context):
    portal = get_portal()
    if portal:
        root = getNavigationRootObject(context, portal)
        if root:
            try:
                return root.absolute_url()
            except AttributeError:
                return portal.absolute_url()
        else:
            return portal.absolute_url()
    return ''


def get_context_url(context):
    if IAddForm.providedBy(context):
        # Use the request URL if we are looking at an addform
        url = context.request.get('URL')
    elif hasattr(context, 'absolute_url'):
        url = context.absolute_url
        if callable(url):
            url = url()
    else:
        url = get_portal_url(context)
    return url

def get_tinymce_options(context, field, request):
    args = {'pattern_options': {}}
    folder = context
    if not IFolderish.providedBy(context):
        folder = aq_parent(context)
    if IPloneSiteRoot.providedBy(folder):
        initial = None
    else:
        initial = IUUID(folder, None)
    portal_url = get_portal_url(context)
    current_path = folder.absolute_url()[len(portal_url):]

    utility = getToolByName(aq_inner(context), 'portal_tinymce', None)
    if utility:
        # Plone 4.3
        config = utility.getConfiguration(context=context,
                                          field=field,
                                          request=request)

        config['content_css'] = config['portal_url'] + '/base.css'
        del config['customplugins']
        del config['plugins']
        del config['theme']

        config['content_css'] = '++resource++plone.app.widgets-tinymce-content.css'
        args['pattern_options'] = {
            'relatedItems': {
                'vocabularyUrl': config['portal_url'] +
                '/@@getVocabulary?name=plone.app.vocabularies.Catalog'
            },
            'upload': {
                'initialFolder': initial,
                'currentPath': current_path,
                'baseUrl': config['document_base_url'],
                'relativePath': '@@fileUpload',
                'uploadMultiple': False,
                'maxFiles': 1,
                'showTitle': False
            },
            'tiny': config,
            # This is for loading the languages on tinymce
            'loadingBaseUrl': '++plone++static/components/tinymce-builded/js/tinymce',
            'prependToUrl': 'resolveuid/',
            'linkAttribute': 'UID',
            'prependToScalePart': '/@@images/image',
            'folderTypes': utility.containsobjects.replace('\n', ','),
            'imageTypes': utility.imageobjects.replace('\n', ','),
            'anchorSelector': utility.anchor_selector,
            'linkableTypes': utility.linkable.replace('\n', ',')
        }
    else:
        # Plone 5
        # They are setted on the body
        pattern_options = getMultiAdapter(
            (context, request, field),
            name="tinymce_settings")()['data-pat-tinymce']
        args['pattern_options'] = json.loads(pattern_options)
    return args

from plone.app.widgets import utils

utils.get_tinymce_options = get_tinymce_options