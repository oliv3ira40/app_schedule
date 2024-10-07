from django.templatetags.static import static

UNFOLD = {
    "SITE_TITLE": 'Agenda Online',
    "SITE_HEADER": 'Agenda Online',
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "DASHBOARD_CALLBACK": "admin_interface.views.dashboard_callback",
    "STYLES": [
        lambda request: static("css/admin_interface.min.css"),
    ],
    "SCRIPTS": [
        lambda request: static("../static/libs/jquery/jquery.min.js"),
        lambda request: static("../static/libs/masks/jquery.mask.min.js"),
        lambda request: static("js/admin_interface.min.js"),
    ],
}
