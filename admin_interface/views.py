from person.models import Client
from schedule.models import Session, Treatment, Package
from itertools import chain
from operator import attrgetter

# Create your views here.
def dashboard_callback(request, context):
    current_user = request.user
    if current_user.is_superuser:
        context.update(
            {"sample": "templates/admin/index.html", "current_user": current_user}
        )
        return context

    upcoming_birthdays = Client.get_upcoming_birthdays(request)
    next_treatments = Treatment.get_next_treatments_by_prof(request)
    next_sessions = Session.get_next_sessions_by_prof(request)
    upcoming_appointments = sorted(
        chain(next_treatments, next_sessions),
        key=attrgetter('date')
    )
    
    count_clients_prof = Client.get_count_clients_by_professional(request)

    count_fin_packages_prof = Package.get_count_fin_packages_by_prof(request)
    count_fin_treatments_prof = Treatment.get_count_fin_treatments_by_prof(request)
    count_finished_services = count_fin_packages_prof+count_fin_treatments_prof

    count_unfin_packages_prof = Package.get_count_unfin_packages_by_prof(request)
    count_unfin_treatments_prof = Treatment.get_count_unfin_treatments_by_prof(request)
    count_unfinished_services = count_unfin_packages_prof+count_unfin_treatments_prof
    
    context.update(
        {
            # "sample": "example",  # this will be injected into templates/admin/index.html
            "sample": "templates/admin/index.html",
            "upcoming_birthdays": upcoming_birthdays,
            "upcoming_appointments": upcoming_appointments,
            'count_clients_prof' : count_clients_prof,
            'count_finished_services' : count_finished_services,
            'count_unfinished_services' : count_unfinished_services,
        }
    )
    return context
