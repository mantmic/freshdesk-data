# states of a ticket
from state import State
from activity import getActivity, getActivityStartTime

class OpenState(State):
    def initialize_activity(self):
        return {
            'state':self,
            'activity':getActivity('Open',getActivityStartTime()),
            'complete':False
        }

    def on_event(self, event, baseTs):
        if event == 'answer':
            return {
                'state':WaitingOnCustomerState(),
                'activity':getActivity('Waiting On Customer',baseTs),
                'complete':False
            }
        elif event == 'invalid':
            return {
                'state':ClosedState(),
                'activity':getActivity('Closed',baseTs),
                'complete':True
            }

        return {'state':self, 'complete':False}

class WaitingOnCustomerState(State):
    def on_event(self, event, baseTs):
        if event == 'cancel':
            return {
                'state':ClosedState(),
                'activity':getActivity('Closed',baseTs),
                'complete':True
            }
        elif event == 'solved':
            return {
                'state':ResolvedState(),
                'activity':getActivity('Resolved',baseTs),
                'complete':True
            }
        elif event == 'notsolved':
            return {
                'state':PendingState(),
                'activity':getActivity('Pending',baseTs),
                'complete':False
            }

        return {'state':self, 'complete':False}

class PendingState(State):
    def on_event(self, event, baseTs):
        if event == 'customerinput':
            return {
                'state':WaitingOnCustomerState(),
                'activity':getActivity('Waiting On Customer',baseTs),
                'complete':False
            }
        elif event == 'thirdpartyinput':
            return {
                'state':WaitingOnThirdPartyState(),
                'activity':getActivity('Waiting On Third Party',baseTs),
                'complete':False
            }
        return {'state':self, 'complete':False}

class WaitingOnThirdPartyState(State):
    def on_event(self, event, baseTs):
        if event == 'thirdpartyrespond':
            return {
                'state':PendingState(),
                'activity':getActivity('Pending',baseTs),
                'complete':False
            }

        return {'state':self, 'complete':False}

class ClosedState(State):
    def on_event(self, event, baseTs):
        return {'state':self, 'complete':True}

class ResolvedState(State):
    def on_event(self, event, baseTs):
        return {'state':self, 'complete':True}
