from random import randint
transitions = {
    "OpenState":[
        {
            "transition":"answer",
            "weight":90
        },
        {
            "transition":"invalid",
            "weight":5
        }
    ],
    "WaitingOnCustomerState":[
        {
            "transition":"cancel",
            "weight":10
        },
        {
            "transition":"notsolved",
            "weight":120
        },
        {
            "transition":"solved",
            "weight":40
        }
    ],
    "PendingState":[
        {
            "transition":"customerinput",
            "weight":120
        },
        {
            "transition":"thirdpartyinput",
            "weight":40
        }
    ],
    "WaitingOnThirdPartyState":[
        {
            "transition":"thirdpartyrespond",
            "weight":1
        }
    ],
    "ClosedState":[],
    "ResolvedState":[]
}


# function to choose a random transition for a given state
def getRandomTransition(state):
    state_transitions = transitions[state]
    total_weight = 0
    for t in state_transitions:
        t['minval'] = total_weight + 1
        total_weight += t.get('weight')
        t['maxval'] = total_weight
    random_val = randint(1,total_weight)
    #return state where the random_val is between the min and max val
    for t in state_transitions:
        if random_val >= t.get('minval') and random_val <= t.get('maxval'):
            return(t.get('transition'))
