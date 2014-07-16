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