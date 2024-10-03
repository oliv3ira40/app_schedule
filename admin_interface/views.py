from person.models import Client
from schedule.models import Session, Treatment

# Create your views here.
def dashboard_callback(request, context):
    upcoming_birthdays = Client.get_upcoming_birthdays(request)
    count_clients_prof = Client.get_count_clients_by_professional(request)
    # scheduled_sessions = Session.get_scheduled_sessions()

    context.update(
        {
            # "sample": "example",  # this will be injected into templates/admin/index.html
            "sample": "templates/admin/index.html",
            "upcoming_birthdays_table": {
                "headers": ["Cliente", 	"Email", "Data do aniversário", "Idade atual"],
                "rows": [
                    [
                        client.name,
                        client.email,
                        client.formt_birth_date,
                        client.age_at_next_birthday
                    ] for client in upcoming_birthdays
                ]
            },
            'count_clients_prof' : count_clients_prof
        }
    )
    return context
