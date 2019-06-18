from ticket_states import OpenState

class Ticket(object):
    """
    A simple state machine that mimics the functionality of a device from a
    high level.
    """

    def __init__(self):
        """ Initialize the components. """
        self.activity = []
        # Start with a default state.
        self.state = OpenState()

    def setState(state):
        activity = state.get('activity')
        self.activity.append(activity)
        self.lastTs = activity.get('update_ts')
        self.state = state.get('state')
        self.complete = state.get('complete')

    def on_event(self, event):
        self.setState(self.state.on_event(event))
