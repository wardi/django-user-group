from django.utils.html import escape
from django.template import Library
from django.core.cache import cache

from urllib import urlopen
from xml.dom.minidom import parseString
from time import strptime, localtime, strftime
from calendar import timegm

FEED_URL = "http://devel.oclug.on.ca/timeline?ticket=on&wiki=on&max=10&daysback=90&format=rss"
CACHE_TIMEOUT = 10 * 60 # in seconds
DATE_IN_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
DATE_OUT_FORMAT = "%d %b %H:%M"

register = Library()

def devel_feed(url_only=False):
    """
    Generate HTML for recent entries from development timeline.
    Use the cache module to avoid fetching on every request.

    url_only -- if True then only return the url to the rss feed
    """

    if url_only:
        return FEED_URL

    out = cache.get('devel_feed')
    if out:
        return out

    # nothing in the cache, so we have to generate the feed now
    out = []
    try:
        doc = parseString(urlopen(FEED_URL).read())
        items = doc.getElementsByTagName("item")
        for i in items:
            out.append('<div class="develitem">')

            # parse and convert date to local time
            tm = i.getElementsByTagName("pubDate")[0].firstChild.data
            tm = localtime(timegm(strptime(tm, DATE_IN_FORMAT)))
            out.append(strftime(DATE_OUT_FORMAT, tm))

            # Here we are trusting the HTML returned from the rss feed
            # and displaying it mostly as-is:
            out.append(' <a href="%s">%s</a>' % (
                i.getElementsByTagName("link")[0].firstChild.data,
                i.getElementsByTagName("title")[0].firstChild.data))
            out.append('</div>')
    except:
        out = ["Error encountered updating devel feed."]

    out = "".join(out)
    # store the result for next time
    cache.set('devel_feed', out, CACHE_TIMEOUT)
    return out
devel_feed = register.simple_tag(devel_feed)

        
