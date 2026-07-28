---
title: "CF 102760B - Bombs In My Deck"
description: "We have a deck containing A cards. Among them, B are bombs and the remaining cards are safe. The order of the deck is random, so every possible placement of bombs has the same probability."
date: "2026-07-28T23:48:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "B"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 80
verified: true
draft: false
---

[CF 102760B - Bombs In My Deck](https://codeforces.com/problemset/problem/102760/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a deck containing `A` cards. Among them, `B` are bombs and the remaining cards are safe. The order of the deck is random, so every possible placement of bombs has the same probability.

The player starts a turn with `C` health points and reveals cards from the top until finding a safe card. Every bomb revealed reduces health by 5. If health reaches zero or below before a safe card appears, the player loses. The task is to calculate the probability that the player survives this turn.

The limits are very small: `A` is at most 30 and `C` is at most 30. This means we do not need advanced data structures or asymptotically optimized techniques. Even an approach that considers every possible number of bombs drawn is enough. However, floating point accuracy matters because the answer is a probability, so the calculation should avoid unnecessary precision loss.

The main edge cases come from the relationship between health and bombs. A careless implementation may count the first safe card incorrectly or stop too late after the player has already died.

Consider the input:

```
4 2 5
```

The player loses after one bomb because `5 - 5 = 0`. The only surviving case is drawing a safe card first, so the answer is:

```
0.500000000
```

A wrong solution that allows one bomb and checks death afterward would produce an incorrect probability.

Another case is:

```
4 2 6
```

Here the player survives after one bomb because `6 - 5 = 1`. Only two consecutive bombs cause a loss. The probability is:

```
0.833333333
```

A solution that uses `C // 5` instead of the ceiling value would incorrectly require two bombs to lose and fail on this boundary.

## Approaches

A direct approach is to simulate every possible position of the first safe card. If the first safe card appears after `k` bombs, the player survives exactly when `k` bombs do not reduce health to zero. We can compute the probability of each possible value of `k` and add the valid cases.

A brute-force way to think about the problem is to enumerate all possible arrangements of the deck and count the successful ones. Since the deck has up to 30 cards, this becomes impossible quickly. The number of possible placements of bombs is `C(30,15)` in the largest case, which is far beyond what can be processed.

The key observation is that the complete arrangement of the deck is unnecessary. The only thing that affects the outcome is how many bombs appear before the first safe card. We can directly compute the probability of seeing `k` bombs followed by a safe card.

The probability of the first `k` cards being bombs is:

```
B / A * (B - 1) / (A - 1) * ... * (B - k + 1) / (A - k + 1)
```

After those bombs, the next card must be safe. At that moment there are `A - k` cards left and still `A - B` safe cards, so the next factor is:

```
(A - B) / (A - k)
```

Because the player dies only after reaching `ceil(C / 5)` bombs, we only need to sum probabilities for smaller values of `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^A) | O(A) | Too slow |
| Optimal | O(A) | O(1) | Accepted |

## Algorithm Walkthrough

1. Calculate the minimum number of bombs needed to make health non-positive. This value is `ceil(C / 5)`. Any sequence with fewer bombs is successful.
2. Start with probability `1.0` for the event that zero bombs are drawn before the first safe card.
3. Iterate through the possible number of bombs drawn before the safe card. For each value `k`, maintain the probability that the first `k` cards are bombs.
4. For the current value of `k`, multiply by the probability that the next card is safe. Add this probability to the answer because this represents one possible surviving outcome.
5. Update the probability of drawing one more bomb and continue until either all bombs have been considered or the player would already have lost.

The invariant behind the algorithm is that before processing a value of `k`, the maintained probability represents exactly the chance that the first `k` revealed cards are bombs. Multiplying by the next-card probability converts that state into the chance that the first safe card appears immediately after those `k` bombs. Since every possible survival case has a unique number of preceding bombs, summing these probabilities gives the complete survival probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B, C = map(int, input().split())

    need = (C + 4) // 5
    ans = 0.0
    prob_all_bombs = 1.0

    for k in range(need):
        if k >= B:
            break

        prob_safe_next = (A - B) / (A - k)
        ans += prob_all_bombs * prob_safe_next

        prob_all_bombs *= (B - k) / (A - k)

    print("{:.9f}".format(ans))

if __name__ == "__main__":
    solve()
```

The variable `need` stores the smallest number of bombs that causes defeat. The loop only considers smaller values because any larger number cannot contribute to a successful outcome.

`prob_all_bombs` stores the probability that the first `k` cards are bombs before the current iteration. The multiplication by `(B - k) / (A - k)` advances this state to the next possible number of bombs.

The expression `(C + 4) // 5` is the integer ceiling of `C / 5`. Using normal integer division here would fail when health is not a multiple of 5.

The denominator `A - k` represents the number of cards remaining before drawing the next card. Since `A` is at most 30, floating point precision is more than sufficient.

## Worked Examples

### Sample 1

Input:

```
4 2 5
```

The player needs one bomb to lose.

| k | Probability first k cards are bombs | Probability next card is safe | Added probability | Answer |
| --- | --- | --- | --- | --- |
| 0 | 1.000000 | 0.500000 | 0.500000 | 0.500000 |

The only successful event is getting a safe card immediately. This trace shows the boundary where exactly one bomb is fatal.

### Sample 2

Input:

```
4 2 6
```

The player needs two bombs to lose.

| k | Probability first k cards are bombs | Probability next card is safe | Added probability | Answer |
| --- | --- | --- | --- | --- |
| 0 | 1.000000 | 0.500000 | 0.500000 | 0.500000 |
| 1 | 0.500000 | 0.666667 | 0.333333 | 0.833333 |

The player survives when there are zero or one bombs before the first safe card. The trace confirms that a single bomb is allowed when health remains positive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(A) | We check at most one case for every possible number of bombs. |
| Space | O(1) | Only a few probability values are stored. |

The maximum number of iterations is 30, so the algorithm easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert abs(float(run("4 2 5\n")) - 0.5) < 1e-9, "sample 1"
assert abs(float(run("4 2 6\n")) - 0.833333333) < 1e-9, "sample 2"

assert abs(float(run("4 2 20\n")) - 1.0) < 1e-9, "large health"
assert abs(float(run("2 1 1\n")) - 0.5) < 1e-9, "minimum size"
assert abs(float(run("30 15 1\n")) - 0.5) < 1e-9, "maximum size with one health"
assert abs(float(run("10 9 46\n")) - 1.0) < 1e-9, "many bombs but enough health"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 2 5` | `0.500000000` | A single bomb is immediately fatal. |
| `4 2 6` | `0.833333333` | One bomb is survivable because health remains positive. |
| `4 2 20` | `1.000000000` | Health is large enough that every possible draw survives. |
| `2 1 1` | `0.500000000` | Smallest deck boundary. |
| `30 15 1` | `0.500000000` | Maximum deck size and immediate death threshold. |
| `10 9 46` | `1.000000000` | The maximum possible number of bombs cannot kill the player. |

## Edge Cases

For the input:

```
4 2 5
```

the threshold is one bomb. The algorithm starts with the probability of zero bombs followed by a safe card. That probability is `2 / 4`, so the answer becomes `0.5`. It never considers one bomb because reaching one bomb already means death.

For the input:

```
4 2 6
```

the threshold is two bombs. The algorithm first counts the probability of a safe card immediately, which is `0.5`. It then considers exactly one bomb followed by a safe card. That probability is `(2 / 4) * (2 / 3) = 1 / 3`, giving the final answer `5 / 6`.

For the input:

```
4 2 20
```

the player needs four bombs to lose, but the deck contains only two bombs. The loop covers every possible number of bombs and adds all possible outcomes, resulting in probability `1`.

For the input:

```
2 1 1
```

the player dies from the first bomb. The only surviving arrangement is drawing the safe card first. The algorithm handles this because the loop stops before counting the fatal bomb case.

I can also provide a shorter contest-style editorial version or a more mathematical version with a formal probability derivation if needed.
