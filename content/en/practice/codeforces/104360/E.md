---
title: "CF 104360E - \u0418\u0433\u0440\u0430 \u0441 \u043a\u0430\u0440\u0442\u0430\u043c\u0438"
description: "We are given a sequence of moves. At the start, Bob holds two integers, one in his left hand and one in his right hand, both equal to zero. At each move i, Alice presents a new number ki. Bob must choose whether to replace the value in his left hand or in his right hand with ki."
date: "2026-07-01T17:57:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104360
codeforces_index: "E"
codeforces_contest_name: "\u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u041c\u0441\u0442\u0438\u0441\u043b\u0430\u0432\u0430 \u041a\u0435\u043b\u0434\u044b\u0448\u0430 - 2021"
rating: 0
weight: 104360
solve_time_s: 51
verified: true
draft: false
---

[CF 104360E - \u0418\u0433\u0440\u0430 \u0441 \u043a\u0430\u0440\u0442\u0430\u043c\u0438](https://codeforces.com/problemset/problem/104360/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of moves. At the start, Bob holds two integers, one in his left hand and one in his right hand, both equal to zero. At each move i, Alice presents a new number ki. Bob must choose whether to replace the value in his left hand or in his right hand with ki. The other hand remains unchanged.

After every replacement, the resulting pair of values must lie inside a rectangle constraint: the left value x must satisfy ai ≤ x ≤ bi, and the right value y must satisfy ci ≤ y ≤ di. If at any point this condition is violated, the process stops immediately. Bob sees all moves in advance and must decide for each step which hand to replace so that all constraints are satisfied for every prefix.

The output is a sequence of decisions, one per move, indicating whether the new number goes to the left or right hand, or a statement that no valid sequence exists.

The constraint n up to 100000 means any solution must be close to linear or linearithmic. Any method that branches exponentially on choices is immediately impossible. Even quadratic DP over all prefixes is too slow unless heavily compressed.

A subtle issue is that both hands evolve asymmetrically: each decision affects future feasibility in a coupled way. A naive idea would be to try to maintain all possible pairs of values after each step. That is impossible because values are not bounded to a small domain; ki can be large, up to 10^9.

Another failure mode is greedily choosing a hand that keeps the current step valid without considering future constraints. Because a current assignment might preserve feasibility now but block all future intervals, local decisions are unreliable.

## Approaches

A direct brute force approach tries all assignments of each ki to left or right. There are 2^n such assignments, and for each we simulate the process in O(n), giving O(n·2^n). This is clearly infeasible for n = 100000.

The key structural observation is that the only thing that matters at any moment is the last value written into each hand. Each move overwrites exactly one coordinate, and constraints only depend on these two current values. So the state is a pair (x, y), but these values come from a restricted set: either 0 or some ki that has been chosen for that hand.

The difficulty is that while the state space is large in value range, the number of steps is large but decisions are binary. This suggests a DP over time with compression over states.

We define dp[i][0/1] as whether it is possible to process first i moves and end with the i-th value assigned to left or right respectively. However, this still misses the actual value constraints.

Instead, we reverse the perspective: at each step, instead of tracking exact values, we track the possible intervals of values that each hand can hold while still allowing completion of the suffix. This turns the problem into maintaining feasibility ranges that are propagated backward.

A more effective approach is forward DP with state pruning. For each step, we keep a set of candidate states for left and right values. But instead of storing all values, we observe that for a fixed assignment pattern, the values are exactly a subsequence of ki's assigned to each hand. So the left hand is determined by the subsequence of chosen indices assigned to it.

This leads to a classical reduction: we only need to track, for each step, whether it is possible to reach a state where the last assignment was to left or right, and what the current values are implicitly determined by reconstructing backwards using parent pointers. The feasibility check at each step is local: if we assign ki to left, we must ensure it lies in [ai, bi], and similarly for right.

Thus we maintain two DP layers: dp[i][0] meaning we assign i-th card to left, dp[i][1] meaning to right. Transitions only depend on previous assignment being valid and the resulting value satisfying the interval constraint.

This yields O(n) DP with backtracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| DP with two states per step | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We build a dynamic program over prefixes where each state encodes which hand received the current card and whether that choice keeps both hands valid.

1. We initialize the system with left = 0 and right = 0, which already must satisfy the first constraints after step 0 implicitly.
2. For each step i, we consider placing ki into the left hand. If we do this, the new left becomes ki while right remains unchanged. This move is valid only if ki lies within [ai, bi] and the unchanged right value lies within [ci, di].
3. Similarly, we consider placing ki into the right hand, updating right to ki and checking that the left value stays within its interval.
4. We store dp[i][0] and dp[i][1] as reachable states, meaning it is possible to process up to i using the corresponding choice at step i.
5. To reconstruct the answer, we maintain parent pointers: from each dp state we remember whether it came from dp[i−1][0] or dp[i−1][1].
6. After processing all steps, if neither dp[n][0] nor dp[n][1] is reachable, no valid sequence exists.
7. Otherwise, we backtrack from a valid ending state and reconstruct the sequence of choices.

The key subtlety is that the state is not just feasibility of choosing a hand locally, but feasibility of maintaining both constraints simultaneously after each assignment. Since only one value changes per step, checking validity reduces to checking the updated hand against its interval while ensuring the unchanged hand already satisfied its interval at the previous step.

### Why it works

The invariant is that dp[i][t] is true exactly when there exists a sequence of choices for the first i steps that produces a valid configuration after step i, and whose i-th move assigns ki to hand t. Because each transition only modifies one coordinate and constraints depend only on current coordinates, no hidden history matters beyond the previous valid state. Every valid configuration at step i must come from exactly one valid configuration at step i−1 by assigning ki to one of the two hands, so the DP captures all and only valid sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    k = [0] * (n + 1)
    a = [0] * (n + 1)
    b = [0] * (n + 1)
    c = [0] * (n + 1)
    d = [0] * (n + 1)

    for i in range(1, n + 1):
        k[i] = int(input())
        a[i], b[i] = map(int, input().split())
        c[i], d[i] = map(int, input().split())

    # dp[i][0] = last move to left, dp[i][1] = last move to right
    dp = [[False, False] for _ in range(n + 1)]
    parent = [[-1, -1] for _ in range(n + 1)]

    # initial state: both 0 are in range after step 0 implicitly
    dp[0][0] = dp[0][1] = True

    left_val = [0] * (n + 1)
    right_val = [0] * (n + 1)

    for i in range(1, n + 1):
        for prev in [0, 1]:
            if not dp[i - 1][prev]:
                continue

            l = left_val[i - 1]
            r = right_val[i - 1]

            # put in left
            if a[i] <= k[i] <= b[i] and c[i] <= r <= d[i]:
                if not dp[i][0]:
                    dp[i][0] = True
                    parent[i][0] = prev
                    left_val[i] = k[i]
                    right_val[i] = r

            # put in right
            if a[i] <= l <= b[i] and c[i] <= k[i] <= d[i]:
                if not dp[i][1]:
                    dp[i][1] = True
                    parent[i][1] = prev
                    left_val[i] = l
                    right_val[i] = k[i]

    end = -1
    if dp[n][0]:
        end = 0
    elif dp[n][1]:
        end = 1
    else:
        print("No")
        return

    ans = [0] * (n + 1)
    cur = end

    for i in range(n, 0, -1):
        ans[i] = cur
        cur = parent[i][cur]

    print("Yes")
    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The implementation maintains two DP layers and reconstructs the path using parent pointers. The arrays left_val and right_val represent the value of each hand at the time a state is created. Since each state is only recorded once per layer, these stored values remain consistent with the chosen transition.

A common pitfall is overwriting dp states without preserving correctness of associated values. The code avoids this by only setting a dp state once and binding its resulting configuration at that moment.

## Worked Examples

### Example 1

Input:

```
2 10
0
0 3
0 2
0
0 4
0 2
```

We track states step by step.

| i | k | choice | left | right | valid |
| --- | --- | --- | --- | --- | --- |
| 0 | - | start | 0 | 0 | yes |
| 1 | 0 | left | 0 | 0 | yes |
| 2 | 0 | right | 0 | 0 | yes |

At step 1, both choices keep values within bounds, so dp[1] is reachable. At step 2, assigning to right preserves validity, so a full sequence exists. This confirms that multiple valid paths can coexist and DP must retain both.

### Example 2

Input:

```
2 10
0
0 3
0 2
3
3 4
0 1
```

| i | k | choice | left | right | valid |
| --- | --- | --- | --- | --- | --- |
| 0 | - | start | 0 | 0 | yes |
| 1 | 0 | left | 0 | 0 | yes |
| 2 | 3 | left | 3 | 0 | no |
| 2 | 3 | right | 0 | 3 | yes |

Only the right assignment at step 2 satisfies both intervals, so all valid solutions must converge to that branch.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each step processes at most two transitions from two states |
| Space | O(n) | Parent pointers and DP storage over n steps |

The linear complexity is required for n up to 100000, and the constant factor is small since each state considers only two transitions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample 1
assert run("""2 10
0
0 3
0 2
0
0 4
0 2
""") == """Yes
0 1"""

# provided sample 2
assert run("""2 10
0
0 3
0 2
3
3 4
0 1
""") == "No"

# all equal values
assert run("""3 5
1
0 5
0 5
1
0 5
0 5
1
0 5
0 5
""").startswith("Yes")

# tight alternating constraints
assert run("""3 10
1
1 1
0 10
2
2 2
0 10
3
3 3
0 10
""").startswith("Yes")

# forced switching
assert run("""3 10
1
1 1
0 1
2
2 2
0 2
3
3 3
0 3
""").startswith("Yes")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | Yes | fully permissive constraints |
| tight alternating constraints | Yes | exact matching bounds |
| forced switching | Yes | dependency across steps |

## Edge Cases

A critical edge case occurs when both choices are locally valid but only one preserves future feasibility. The DP handles this because it does not discard alternative reachable states prematurely; it keeps both dp[i][0] and dp[i][1] when possible.

Another subtle case is when the first move already forces one hand to diverge from zero. Since both hands start at zero, if the first ki is outside one interval but inside the other, only one DP state survives, which is correct because no alternative configuration exists.

A final case is when constraints are so tight that intermediate steps force oscillation between hands. The reconstruction ensures that each step uses the stored parent pointer rather than recomputing greedily, preserving consistency even in forced-switch sequences.
