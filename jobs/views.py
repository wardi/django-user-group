from datetime import datetime

from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from models import Posting, default_expiration
from forms import PostingForm


def get_postings():
    """
    Return an ordered queryset of visible job postings.
    """
    return Posting.objects.filter(accepted__isnull=False,
        expires__gt=datetime.now).order_by('-accepted')


def list_postings(request, template_name="jobs/list_postings.html"):
    """
    Display a list of the job postings that have been accepted and have
    not yet expired.
    """
    return object_list(request, template_name=template_name,
        queryset=get_postings(),
        allow_empty=True,
        paginate_by=20)


def view_posting(request, posting_id, template_name="jobs/view_posting.html"):
    """
    View the details of an accepted job posting.  Will allow viewing an 
    expired posting, although there will be no links to those pages.
    """
    return object_detail(request, object_id=posting_id,
        template_name=template_name, 
        queryset=Posting.objects.filter(accepted__isnull=False))


def new_posting(request, template_name="jobs/new_posting.html"):
    """
    Interface to create a new job posting.  A GET request will present
    an empty form.  A POST request will allow previewing and submitting
    the job posting.
    """
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if 'submit' in request.POST and form.is_valid():
            posting = form.save()
            send_new_posting_notification(posting)
            return HttpResponseRedirect(posting.get_edit_url())

        if form.is_valid():
            preview = form.save(commit=False) # create a dummy posting instance
            return render_to_response(template_name, {'form': form,
                'preview': preview}) 
    else:
        form = PostingForm()

    return render_to_response(template_name, {'form': form})


def send_new_posting_notification(posting):
    """
    Send an email to everyone in settings.JOB_POSTING_EMAILS.
    """
    from django.conf import settings 
    from django.contrib.sites.models import Site
    
    try:
        email_to = settings.JOB_POSTING_EMAILS
        email_from = settings.JOB_POSTING_FROM
    except AttributeError:
        # fail silently if unconfigured
        return

    site = Site.objects.get(id=settings.SITE_ID)
    
    subject = "%s Job Posting: %s" % (site.domain, posting.title)
    body = "http://%s/admin/jobs/posting/%d/\n\n%s\n\nContact:\n\n%s" %(
        site.domain, posting.id, posting.description, posting.contact)
    send_mail(subject, body, email_from, email_to, fail_silently=True)


def edit_posting(request, posting_id, hash, 
    template_name="jobs/edit_posting.html"):
    """
    Interface to allow removal and extending expiration of a job posting.
    """
    posting = get_object_or_404(Posting, id=int(posting_id))
    if posting.hash() != hash:
        raise Http404()  # if hash doesn't match send 404

    if 'delete' in request.POST:
        posting.delete()
        return HttpResponseRedirect("/jobs/")
    if 'extend' in request.POST:
        posting.expires = default_expiration()
        posting.save()
        return HttpResponseRedirect(posting.get_edit_url())

    return render_to_response(template_name, {'posting': posting,
        'next_expiration': default_expiration()})

