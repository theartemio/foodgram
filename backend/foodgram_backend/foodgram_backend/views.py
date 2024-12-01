from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from recipes.models import ShortenedLinks


class ShortLinkRedirectView(RedirectView):
    """
    Перенаправление короткой ссылки на длинную ссылку.
    """

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short_code = kwargs["short_code"]
        link = get_object_or_404(ShortenedLinks, short_link_code=short_code)
        return link.original_url
