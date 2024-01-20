

# prepare data for UI
def prepareDataForDFA(dfa):
    state_name = {}
    i = 0
    for state in dfa["reachable_states"]:
        if state == "phi":
            state_name[state] = 'q'  # "\u03A6"
        else:
            state_name[state] = "q"+str(i)
            i += 1

    final_states = []
    for x in dfa["final_reachable_states"]:
        final_states.append(state_name[x])

    states = []
    for x in state_name:
        states.append(state_name[x])

    links = []
    for state in dfa["reachable_states"]:
        for character in dfa["transition_function"][state].keys():
            transition_state = dfa["transition_function"][state][character]
            path = {
                'source': state_name[state],
                'target': state_name[transition_state],
                'label': character
            }
            links.append(path)

    data = {
        'links': links,
        'states': states,
        'final_states': final_states
    }
    return data
