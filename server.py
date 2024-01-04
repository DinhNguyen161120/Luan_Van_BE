import json
from flask import Flask, jsonify, request
from automata_toolkit.regex_to_nfa import regex_to_nfa
from automata_toolkit.nfa_to_dfa import nfa_to_dfa
from automata_toolkit.visual_utils import draw_dfa
from automata_toolkit.dfa_to_regex import dfa_to_regex, dfa_to_efficient_dfa

from flask_cors import CORS, cross_origin


def draw_dfa(dfa):
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


app = Flask(__name__)
cors = CORS(app)

@app.route('/', )
@cross_origin()
def index():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})

@app.route('/regex-to-nfa', methods=['POST'])
@cross_origin()
def regex2nfa():
    try:
        data = request.json
        regex = data.get('regex')
        nfa = regex_to_nfa(regex)
        return jsonify(nfa)
    except:
        print("An exception occurred")
        return jsonify({
            'err': 'true',
        })

@app.route('/nfa-to-dfa', methods=['POST'])
@cross_origin()
def nfa2dfa():
    try:
        data = request.json
        nfa = data.get('nfa')
        dfa = nfa_to_dfa(nfa)

        dataShowDfa = draw_dfa(dfa)
        data = {
            'dfa': str(dfa),
            'dataShowDfa': dataShowDfa
        }
        return jsonify(data)
    except:
        print("An exception occurred")
        return jsonify({
            'err': 'true',
        })

@app.route('/dfa-to-regex', methods=['POST'])
@cross_origin()
def dfa2regex():
    try:
        data = request.json
        dfa = data.get('dfa')
        newDfa = dfa_to_efficient_dfa(dfa)
        regex = dfa_to_regex(newDfa)
        data = {
            'regex': str(regex)
        }
        return jsonify(data)
    except:
        print("An exception occurred")
        return jsonify({
            'err': 'true',
        })
    
app.run(debug=True)
