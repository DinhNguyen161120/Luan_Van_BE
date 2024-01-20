
from flask import Blueprint, jsonify, request
from automata_toolkit.regex_to_nfa import regex_to_nfa
from automata_toolkit.nfa_to_dfa import nfa_to_dfa
from automata_toolkit.visual_utils import draw_dfa
from automata_toolkit.dfa_to_regex import dfa_to_regex, dfa_to_efficient_dfa
from utils.draw_util import prepareDataForDFA

automataRoutes = Blueprint("automataRoutes", __name__)

@automataRoutes.route('/regex-to-nfa', methods=['POST'])
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

@automataRoutes.route('/nfa-to-dfa', methods=['POST'])
def nfa2dfa():
    try:
        data = request.json
        nfa = data.get('nfa')
        dfa = nfa_to_dfa(nfa)

        dataShowDfa = prepareDataForDFA(dfa)
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

@automataRoutes.route('/dfa-to-regex', methods=['POST'])
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


@automataRoutes.route('/test', methods=['GET'])
def testFunc ():
    data = {
        'regex': 'test'
    }
    return jsonify(data)