########################### support.py #############################
"""
STUDENT INFO: You may want to add new elif statements to support new bots

This file just contains a few support functions used by the other
files

"""
import bots
import ta_bots


def determine_bot_functions(bot_names):
    bot_list = []
    for name in bot_names:
        if name == "student":
            bot_list.append(bots.StudentBot())
        elif name == "random":
            bot_list.append(bots.RandBot())
        elif name == "wall":
            bot_list.append(bots.WallBot())
        elif name == "ta1":
            bot_list.append(ta_bots.TABot1())
        elif name == "ta2":
            bot_list.append(ta_bots.TABot2())
        elif name == "survivor":
            bot_list.append(bots.Survivor())
        elif name == "mocker":
            bot_list.append(bots.Mocker())
        elif name == "attacker":
            bot_list.append(bots.Attacker())
        elif name == "bad":
            bot_list.append(bots.BadSurvivor())
        elif name == "thinker":
            bot_list.append(bots.Thinker())
        else:
            raise ValueError(
                """Bot name %s is not supported. Value names include "student",
"random", "wall", "ta1", "ta2" "survivor", "attacker", """
                % name
            )
    return bot_list


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Player action timed out.")
