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


def detailed_evaluation_func(state):
    # TODO
    pass


def get_evaluation_func(func_name):
    if func_name == "dummy_evaluation_func":
        return dummy_evaluation_func
    elif func_name == "distance_evaluation_func":
        return distance_evaluation_func
    elif func_name == "detailed_evaluation_func":
        return detailed_evaluation_func
    else:
        raise KeyError(func_name)
