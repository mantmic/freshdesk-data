# states of a ticket
from state import State
from activity import getActivity

class OpenState(State):
    def on_event(self, event):
        if event == 'answer':
            return {
                'state':WaitingOnCustomerState(),
                'activity':getActivity('Open'),
                'complete':False
            }
        elif event == 'invalid':
            return ClosedState()

        return self


class WaitingOnCustomerState(State):
    def _init_():
        print ('Processing current state:', str(self))
        #initialize activity stuff
        activity = getActivity('Waiting for Customer',self.lastTs)
        self.lastTs = activity.get('updated_ts')
        self.activity.append(activity)

    def on_event(self, event):
        if event == 'cancel':
            return ClosedState()
        elif event == 'solved':
            return ResolvedState()
        elif event == 'notsolved':
            return PendingState()

        return self

class PendingState(State):
    def _init_():
        print ('Processing current state:', str(self))
        #initialize activity stuff
        activity = getActivity('Pending',self.lastTs)
        self.lastTs = activity.get('updated_ts')
        self.activity.append(activity)
    def on_event(self, event):
        if event == 'customerinput':
            return WaitingOnCustomerState()
        elif event == 'thirdpartyinput':
            return WaitingOnThirdPartyState()

        return self

class WaitingOnThirdPartyState(State):
    def _init_():
        print ('Processing current state:', str(self))
        #initialize activity stuff
        activity = getActivity('Waiting for third party',self.lastTs)
        self.lastTs = activity.get('updated_ts')
        self.activity.append(activity)
    def on_event(self, event):
        if event == 'thirdpartyrespond':
            return PendingState()

        return self

class ClosedState(State):
    def _init_():
        print ('Processing current state:', str(self))
        #initialize activity stuff
        activity = getActivity('Closed',self.lastTs)
        self.lastTs = activity.get('updated_ts')
        self.activity.append(activity)
        self.complete = True

class ResolvedState(State):
    def _init_():
        print ('Processing current state:', str(self))
        #initialize activity stuff
        activity = getActivity('Resolved',self.lastTs)
        self.lastTs = activity.get('updated_ts')
        self.activity.append(activity)
        self.complete = True
