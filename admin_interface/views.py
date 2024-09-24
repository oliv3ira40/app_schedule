from django.shortcuts import render

# Create your views here.
def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            # "sample": "example",  # this will be injected into templates/admin/index.html
            "sample": "templates/admin/index.html",
        }
    )
    return context