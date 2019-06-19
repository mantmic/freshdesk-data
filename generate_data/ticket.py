from ticket_states import OpenState

class Ticket(object):
    def __init__(self):
        """ Initialize the components. """
        # Start with a default state.
        self.state = OpenState()
        self.activity = []
        self.setState(self.state.initialize_activity())
        self.startTs = self.lastTs

    def setState(self,state):
        activity = state.get('activity')
        self.lastTs = activity.get('performed_at')
        activity['performed_at'] = activity.get('performed_at').isoformat()
        self.activity.append(activity)
        self.state = state.get('state')
        self.complete = state.get('complete')

    def on_event(self, event):
        self.setState(self.state.on_event(event,self.lastTs))
