# Betting Strategy AI - Unit Test Report

이 프로젝트는 Q-learning 기반 축구 경기 스코어 배팅 프로그램입니다.  
Python으로 작성된 주요 로직에 대해 `unittest`와 `unittest.mock`을 활용하여 단위 테스트를 수행하였습니다.

---

## 테스트 환경

- Python 3.8 이상
- 실행 방법:
  ```bash
  python test_betting.py
  ```

---

## 테스트 대상 모듈: `betting.py`

`betting.py`는 다음과 같은 주요 함수들로 구성되어 있습니다:

- `score_to_state(odds)`: 배당률에 따라 상태 분류 (low / mid / high)
- `available_actions(odds_list)`: 가능한 배팅 액션 목록 생성
- `compute_reward(action, amount, odds_list, actual_score)`: 보상 계산 함수
- `choose_action(state, actions)`: ε-greedy 기반 액션 선택
- 기타 Q-table 관련 함수 등

---

## 테스트 항목 요약 (`test_betting.py`)

| 테스트 함수 | 설명 |
|-------------|------|
| `test_score_to_state()` | 배당률에 따라 상태가 정확히 분류되는지 확인 |
| `test_available_actions()` | 입력된 스코어 리스트에서 정확한 액션 목록 생성 여부 확인 |
| `test_compute_reward_*()` | 이긴 경우, 진 경우, no_bet 각각에 대한 보상 계산 결과 검증 |
| `test_choose_action_exploit()` | ε-greedy 정책에서 Q값 기반 선택 (탐욕적 선택) 확인 |
| `test_choose_action_explore()` | ε-greedy 정책에서 무작위 선택 (탐험적 선택) 확인<br>→ `unittest.mock.patch()` 사용하여 `random` 결과를 고정 |

---

## `mock` 활용

- `choose_action()`의 무작위 동작을 제어하기 위해 `random.random`과 `random.choice`를 mock 처리함
  ```python
  @patch("random.random", return_value=0.01)
  @patch("random.choice", return_value="bet_1-0")
  ```

---

## 파일 구성

```
my_betting_project/
├── betting.py          # 핵심 로직
├── test_betting.py     # 단위 테스트 코드
└── q_table.pkl         # Q-table 저장 파일 (실행 시 생성)
```

---

## 비고

- 학습된 Q값이 없는 경우에도 프로그램이 graceful하게 동작하는지 확인
- 실시간 사용자 입력 등은 테스트 범위에서 제외하고 로직 중심 테스트 진행
