"""
Evaluation functions
"""


def dummy_evaluation_func(state):
    return 0.0


def distance_evaluation_func(state):
    player = state.get_current_player()
    info = state.get_info()
    score = 0.0
    for p, info_p in info.items():
        if p == player:
            score -= info_p["max_distance"]
        else:
            score += info_p["max_distance"]
    return score


live_four_score = 0.5
four_score = 0.05
live_three_score = 0.04
three_score = 0.025
live_two_score = 0.01
max_distance_score = 0.01

def detailed_evaluation_func(state):
    # TODO
    player = state.get_current_player()
    info = state.get_info()
    score = 0.0
    for p, info_p in info.items():
        if p == player:
            score += info_p["live_four"] * live_four_score + \
                     info_p["four"] * four_score + \
                     info_p["live_three"] * live_three_score + \
                     info_p["three"] * three_score + \
                     info_p["live_two"] * live_two_score - \
                     info_p["max_distance"] * max_distance_score
        else:
            score -= info_p["live_four"] * live_four_score + \
                     info_p["four"] * four_score + \
                     info_p["live_three"] * live_three_score + \
                     info_p["three"] * three_score + \
                     info_p["live_two"] * live_two_score -\
                     info_p["max_distance"] * max_distance_score
    return score


def get_evaluation_func(func_name):
    if func_name == "dummy_evaluation_func":
        return dummy_evaluation_func
    elif func_name == "distance_evaluation_func":
        return distance_evaluation_func
    elif func_name == "detailed_evaluation_func":
        return detailed_evaluation_func
    else:
        raise KeyError(func_name)
