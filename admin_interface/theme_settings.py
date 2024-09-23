from django.templatetags.static import static
UNFOLD = {
    "SITE_TITLE": 'Agenda Online',
    "SITE_HEADER": 'Agenda Online',
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "DASHBOARD_CALLBACK": "admin_interface.views.dashboard_callback",
    "STYLES": [
    ],
    "SCRIPTS": [
        # lambda request: static("js/unfold-translates.js"),
    ],
}
