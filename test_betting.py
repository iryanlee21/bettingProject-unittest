import unittest
from betting import score_to_state, available_actions, compute_reward, choose_action, Q_table
from unittest.mock import patch

class TestBetting(unittest.TestCase):
    def test_score_to_state(self):
        self.assertEqual(score_to_state(3.0), "low")
        self.assertEqual(score_to_state(10.0), "mid")
        self.assertEqual(score_to_state(20.0), "high")

    def test_available_actions(self):
        odds = [("1-0", 5.0), ("2-1", 7.0)]
        actions = available_actions(odds)
        self.assertIn("bet_1-0", actions)
        self.assertIn("no_bet", actions)

    def test_compute_reward_win(self):
        odds = [("2-1", 8.0)]
        result = compute_reward("bet_2-1", 1000, odds, "2-1")
        self.assertEqual(result, 1000 * (8.0 - 1))

    def test_compute_reward_loss(self):
        odds = [("2-1", 8.0)]
        result = compute_reward("bet_2-1", 1000, odds, "1-0")
        self.assertEqual(result, -1000 * 0.8)

    def test_compute_reward_no_bet(self):
        odds = [("2-1", 8.0)]
        result = compute_reward("no_bet", 1000, odds, "2-1")
        self.assertEqual(result, 1000 * 0.05)

    @patch("random.random", return_value=0.99)
    def test_choose_action_exploit(self, mock_random):
        Q_table["mid"]["bet_1-0"] = 1.0
        Q_table["mid"]["bet_2-1"] = 5.0
        actions = ["bet_1-0", "bet_2-1"]
        result = choose_action("mid", actions)
        self.assertEqual(result, "bet_2-1")

    @patch("random.random", return_value=0.01)
    @patch("random.choice", return_value="bet_1-0")
    def test_choose_action_explore(self, mock_choice, mock_random):
        actions = ["bet_1-0", "bet_2-1"]
        result = choose_action("mid", actions)
        self.assertEqual(result, "bet_1-0")

if __name__ == "__main__":
    unittest.main()
