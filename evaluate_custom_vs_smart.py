import sys
import os
import random
import tracemalloc

sys.path.append(os.path.abspath("src/bazaar-ai"))
from agents.goldcrusher import GoldcrusherAgent
from agents.simple_agent import SmartAgent
from backend.bazaar import BasicBazaar
from backend.goods import GoodType
from backend.coins import BonusType


def compute_final_score(game, player):
    """
    Final score = all goods coins + all bonus coins + camel bonus if applicable
    """
    state = game.state

    goods_value = 0
    for good in GoodType:
        goods_value += sum(state.player_coins[player].goods_coins[good])

    bonus_value = 0
    for bonus in BonusType:
        bonus_value += sum(state.player_coins[player].bonus_coins[bonus])

    camel_bonus = 0
    other_player = None
    for p in game.players:
        if p != player:
            other_player = p
            break
    my_camels = state.player_goods[player][GoodType.CAMEL]
    opp_camels = state.player_goods[other_player][GoodType.CAMEL]

    if my_camels > opp_camels:
        camel_bonus = state.camel_bonus

    return goods_value + bonus_value + camel_bonus


def play_one_game(seed):
    """
    Runs one full game of CustomAgent vs SmartAgent.
    Returns:
        winner_name, custom_score, smart_score, total_move_time, move_count, max_move_time
    """
    custom = GoldcrusherAgent(seed=seed, name="Custom")
    smart = SmartAgent(seed=seed + 1, name="Smart")

    players = [custom, smart]
    game = BasicBazaar(seed=seed, players=players)
    if not hasattr(game, "round"):
        game.round = 0

    while not game.terminal(game.state):
        actor = game.state.actor
        legal_actions = game.all_actions(actor, game.state)

        if not legal_actions:
            break

        observation = game.observe(actor, game.state)

        def simulate_action_fnc(action):
            future_state = game.apply_action(game.state, action)
            return game.observe(actor, future_state)

        try:
            chosen_action = actor.select_action(
                legal_actions,
                observation,
                simulate_action_fnc
            )
        except Exception as e:
            print(f"Bot {actor.name} crashed with error: {e}")
            if actor == custom:
                return "Smart", 0, 1, custom.total_move_time, custom.move_count, custom.max_move_time
            else:
                return "Custom", 1, 0, custom.total_move_time, custom.move_count, custom.max_move_time

        if chosen_action not in legal_actions:
            chosen_action = legal_actions[0]

        game.state = game.apply_action(game.state, chosen_action)
        game.round += 1

    custom_score = compute_final_score(game, custom)
    smart_score = compute_final_score(game, smart)

    if custom_score > smart_score:
        winner_name = "Custom"
    elif smart_score > custom_score:
        winner_name = "Smart"
    else:
        winner_name = "Draw"

    return (
        winner_name,
        custom_score,
        smart_score,
        custom.total_move_time,
        custom.move_count,
        custom.max_move_time,
    )


def evaluate_matchup(num_games=60, start_seed=0):
    custom_wins = 0
    smart_wins = 0
    draws = 0

    custom_scores = []
    smart_scores = []

    total_custom_move_time = 0.0
    total_custom_moves = 0
    max_custom_move_time = 0.0

    for i in range(num_games):
        seed = start_seed + i
        (
            winner_name,
            custom_score,
            smart_score,
            custom_total_time,
            custom_move_count,
            custom_max_time,
        ) = play_one_game(seed)

        custom_scores.append(custom_score)
        smart_scores.append(smart_score)

        total_custom_move_time += custom_total_time
        total_custom_moves += custom_move_count
        if custom_max_time > max_custom_move_time:
            max_custom_move_time = custom_max_time

        if winner_name == "Custom":
            custom_wins += 1
        elif winner_name == "Smart":
            smart_wins += 1
        else:
            draws += 1

        if (i + 1) % 20 == 0:
            print(f"Finished {i + 1}/{num_games} games...")

    avg_custom_score = sum(custom_scores) / num_games
    avg_smart_score = sum(smart_scores) / num_games
    avg_margin = avg_custom_score - avg_smart_score
    pass_rate = custom_wins / num_games

    avg_custom_move_time = 0.0
    if total_custom_moves > 0:
        avg_custom_move_time = total_custom_move_time / total_custom_moves

    print("\n===== CUSTOM VS SMART =====")
    print(f"Games played: {num_games}")
    print(f"Custom wins: {custom_wins}")
    print(f"Smart wins: {smart_wins}")
    print(f"Draws: {draws}")
    print(f"Passes (Custom beat Smart): {custom_wins}/{num_games}")
    print(f"Pass rate: {100 * pass_rate:.2f}%")
    print(f"Average Custom score: {avg_custom_score:.2f}")
    print(f"Average Smart score: {avg_smart_score:.2f}")
    print(f"Average margin (Custom - Smart): {avg_margin:.2f}")
    print(f"Average Custom move time: {avg_custom_move_time:.6f} s")
    print(f"Max Custom move time: {max_custom_move_time:.6f} s")


if __name__ == "__main__":
    tracemalloc.start()

    for _ in range(3):
        seed = random.randint(0, 10_000_000)
        print("\nBATCH SEED:", seed)
        evaluate_matchup(num_games=60, start_seed=seed)

    current, peak = tracemalloc.get_traced_memory()
    print(f"\nCurrent memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

    tracemalloc.stop()