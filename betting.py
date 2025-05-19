# betting.py
import os, pickle, random
from collections import defaultdict
from typing import List, Tuple

EPSILON = 0.1
ALPHA, GAMMA = 0.1, 0.9
RISK_FACTOR = 0.8
QTABLE_PATH = "q_table.pkl"

score_frequencies = [("1-1", 11.92), ("1-0", 11.14), ("0-0", 8.74), ("2-1", 8.32), ("0-1", 8.19), ("2-0", 7.42)]

def default_action_dict():
    return defaultdict(float)

Q_table = defaultdict(default_action_dict)

def load_Q_table(path: str = QTABLE_PATH):
    global Q_table
    try:
        with open(path, "rb") as f:
            Q_table = pickle.load(f)
        print("[INFO] Q-table loaded.")
    except (FileNotFoundError, EOFError):
        print("[INFO] No valid Q-table found. Initializing new one.")
        Q_table = defaultdict(default_action_dict)

def save_Q_table(path: str = QTABLE_PATH):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(Q_table, f)
    print("[INFO] Q-table saved.")

def score_to_state(odds: float) -> str:
    if odds < 5: return "low"
    if odds < 15: return "mid"
    return "high"

def available_actions(odds_list: List[Tuple[str, float]]) -> List[str]:
    return [f"bet_{s}" for s, _ in odds_list] + ["no_bet"]

def choose_action(state: str, actions: List[str]) -> str:
    if random.random() < EPSILON:
        return random.choice(actions)
    return max(actions, key=lambda a: Q_table[state].get(a, 0.0))

def compute_reward(action: str, bet_amount: float, odds_list: List[Tuple[str,float]], actual_score: str) -> float:
    if action == "no_bet":
        return bet_amount * 0.05
    score = action.split("_", 1)[1]
    odds = dict(odds_list).get(score, 0.0)
    return bet_amount * (odds - 1) if score == actual_score else -bet_amount * RISK_FACTOR

def update_Q(state: str, action: str, reward: float, next_state: str = "terminal"):
    current = Q_table[state][action]
    future_max = max(Q_table[next_state].values() or [0.0])
    Q_table[state][action] = current + ALPHA * (reward + GAMMA * future_max - current)

def allocate_bets(odds_list: List[Tuple[str,float]], budget: float) -> List[Tuple[str,float,float]]:
    state = score_to_state(min(item[1] for item in odds_list))
    q_scores = {
        f"bet_{score}": max(Q_table[state].get(f"bet_{score}", 0.0), 0.0)
        for score, _ in odds_list
    }
    total_q = sum(q_scores.values())
    if total_q == 0:
        return []
    return [
        (score, odds, budget * (q_scores[f"bet_{score}"] / total_q))
        for score, odds in odds_list
    ]

def train_one_match(odds_list: List[Tuple[str, float]], budget: float):
    bets = allocate_bets(odds_list, budget)
    if not bets:
        print("> 아직 학습된 Q값이 없어 배팅을 건너뜁니다.")
        save_Q_table()
        return

    print("=== 추천 분할 배팅 ===")
    for score, odds, amt in bets:
        print(f"  • {score} (odds={odds:.1f}): {amt:,.0f}원")

    actual = input("실제 결과 스코어를 입력하세요 (예: '2-1'): ").strip()
    state = score_to_state(min(item[1] for item in odds_list))

    for score, odds, amt in bets:
        action = f"bet_{score}"
        reward = compute_reward(action, amt, odds_list, actual)
        print(f"  → [{score}] reward = {reward:,.0f}")
        update_Q(state, action, reward)

    save_Q_table()


if __name__ == "__main__":
    load_Q_table()

    # -------------------------------
    # ─── (추가) Q-table이 비어 있으면 score_frequencies로 초기화 ──────────
    all_q = sum(Q_table[s][a] for s in Q_table for a in Q_table[s])
    if all_q == 0:
        for state in ["low", "mid", "high"]:
            for score, freq in score_frequencies:
                Q_table[state][f"bet_{score}"] = freq
        save_Q_table()
        print("[INFO] Q-table initialized from score_frequencies.")
    # -------------------------------

    # ▶ 오늘 경기 배당률 리스트만 바꿔 넣으세요
    odds_list = [
      ('1-0', 9.7),  ('2-0', 11.7), ('2-1', 7.5),  ('3-0', 21.1),
      ('3-1', 13.6), ('3-2', 17.6), ('4-0', 50.9), ('4-1', 32.8),
      ('4-2', 42.4), ('4-3', 82.0), ('5-0',150.0), ('5-1', 98.9),
      ('5-2',130.0), ('5-3',250.0), ('기타홈승',79.7),('0-0',16.1),
      ('1-1', 6.3),  ('2-2', 9.7),  ('3-3',34.0),  ('4-4',210.0),
      ('기타무',999.0),('0-1',10.4), ('0-2',13.4), ('1-2',8.1),
      ('0-3',26.0),  ('1-3',15.6), ('2-3',18.8), ('0-4',67.0),
      ('1-4',40.3),  ('2-4',48.6), ('3-4',87.8), ('0-5',220.0),
      ('1-5',130.0), ('2-5',160.0),('3-5',280.0), ('기타홈패',110.0)
    ]

    budget = float(input("예산을 입력하세요 (예: 100000): "))
    train_one_match(odds_list, budget)