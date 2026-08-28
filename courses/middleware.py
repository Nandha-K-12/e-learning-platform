from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Course


class SubdomainCourseMiddleware:
    """
    Middleware to handle course subdomains.
    E.g., accessing http://python.educaproject.com/ will redirect/route
    to the specific course detail page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host_parts = request.get_host().split('.')
        if len(host_parts) > 2 and host_parts[0] != 'www':
            # Course slug from subdomain
            course_slug = host_parts[0]
            try:
                course = Course.objects.get(slug=course_slug)
                course_url = reverse('course_detail', args=[course.slug])
                # Redirect to main domain course detail
                main_host = '.'.join(host_parts[1:])
                url = f"{request.scheme}://{main_host}{course_url}"
                return redirect(url)
            except Course.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
