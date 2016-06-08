from bottle_utils.i18n import lazy_gettext as _

from librarian.presentation.menu.menu import MenuItem


class TwitterMenuItem(MenuItem):
    name = 'twitter'
    label = _("Twitter")
    icon_class = 'twitter'
    route = 'twitter:list'
