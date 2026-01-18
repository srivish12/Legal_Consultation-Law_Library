from .models import SiteSettings


def site_settings(request):
    settings = SiteSettings.objects.first()
    return {'settings': settings}
