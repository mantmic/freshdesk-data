from ticket import Ticket
from ticket_transitions import getRandomTransition


def makeTicket(ticket_id):
    t = Ticket()
    while t.complete == False:
        t.on_event(getRandomTransition(str(t.state)))
    activities = t.activity
    for a in activities:
        a['ticket_id'] = ticket_id
    return(activities)

#make n number of tickets
def makeTicketActivies(n):
    activities = []
    for i in range(n):
        activities.extend(makeTicket(i+1))
    return({
        "metadata":{
            "activities_count":len(activities)
        },
        "activities_data":activities
    })
