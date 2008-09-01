from django.contrib.syndication.feeds import Feed
from models import Posting

from datetime import datetime


class JobPostings(Feed):
    title = "OCLUG Job Postings"
    link = "/jobs/"
    description = "Linux and Open Source Jobs in the Ottawa Area"

    def items(self):
        return Posting.objects.filter(accepted__isnull=False,
            expires__gt=datetime.now).order_by('-accepted')

