from person.models import Client
from schedule.models import Session, Treatment, Package
from itertools import chain
from operator import attrgetter

# Create your views here.
def dashboard_callback(request, context):
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

    # scheduled_sessions = Session.get_scheduled_sessions()
    context.update(
        {
            # "sample": "example",  # this will be injected into templates/admin/index.html
            "sample": "templates/admin/index.html",
            "upcoming_birthdays_table": {
                "headers": ["Cliente", 	"Telefone", "Data do aniversário", "Idade atual"],
                "rows": [
                    [
                        client.name,
                        client.phone,
                        client.formt_birth_date,
                        client.age_at_next_birthday,
                    ] for client in upcoming_birthdays
                ]
            },
            "upcoming_appointments_table": {
                "headers": ["Agendada para o dia", "Tipo", "Cliente", "Serviço"],
                "rows": [
                    [
                        appointment.date,
                        appointment.type,
                        appointment.client.name,
                        appointment.service.name,
                    ] for appointment in upcoming_appointments
                ]
            },
            'count_clients_prof' : count_clients_prof,
            'count_finished_services' : count_finished_services,
            'count_unfinished_services' : count_unfinished_services,
        }
    )
    return context
