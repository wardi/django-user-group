from django.db import models

from datetime import datetime, timedelta


def default_expiration():
    return datetime.now() + timedelta(60) # expire in 60 days by default 

class Posting(models.Model):
    title = models.CharField(max_length=100,
        help_text="Title for the job posting eg. "
            '"Full Time Perl/PHP Developer Position at Widget Packers Inc."')
    description = models.TextField(
        help_text="Detailed description of job posting "
            "including Linux or Open Source related responsibilities &mdash; "
            "Job postings not related to Linux or Open Source software "
            "will not be accepted")
    contact = models.TextField(
        verbose_name="Contact Information",
        help_text="Instructions for contacting the employer")
    created = models.DateTimeField(
        default=datetime.now,
        help_text="Date the posting was created")
    expires = models.DateTimeField(
        default=default_expiration,
        help_text="Date the posting will expire")
    accepted = models.DateTimeField(
        null=True, blank=True,
        help_text="Date the posting was displayed on the web site")

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/posting/%d/" % self.id

    def visible(self):
        return self.accepted is not None and datetime.now() < self.expires
    visible.boolean = True
    
    def hash(self):
        """
        generate a hash that will act as a password for editing.
        """
        from django.conf import settings
        from md5 import md5
        plaintext = "posting.%d.%s.%s" % (self.id, 
            self.created.strftime("%Y%m%d%H%M%S"), 
            settings.SECRET_KEY)
        return md5(plaintext).hexdigest()[:16]

    def get_edit_url(self):
        return "/posting/edit/%d/%s/" % (self.id, self.hash())

    class Meta:
        ordering = ['-accepted']
