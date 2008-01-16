from django.utils.html import escape
from django.template import Library

from datetime import datetime

register = Library()

def serving_time():
    """
    Return the approximate number of years since OCLUG's inception.
    """
    
    n = datetime.now()
    nm = (n.year * 12 + n.month) - (1997 * 12 + 3)
    m = nm % 12
    if m > 6:
        return "%d&frac12; years" % (nm / 12)
    else:
        return "%d years" % (nm / 12)
serving_time = register.simple_tag(serving_time)
     
