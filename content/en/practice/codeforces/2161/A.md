---
title: "CF 2161A - Round Trip"
description: "We are simulating a sequence of contest rounds where a participant can sometimes adjust their rating before each rated round."
date: "2026-06-07T23:58:20+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2161
codeforces_index: "A"
codeforces_contest_name: "Pinely Round 5 (Div. 1 + Div. 2)"
rating: 800
weight: 2161
solve_time_s: 91
verified: true
draft: false
---

[CF 2161A - Round Trip](https://codeforces.com/problemset/problem/2161/A)

**Rating:** 800  
**Tags:** games, greedy, implementation, math  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a sequence of contest rounds where a participant can sometimes adjust their rating before each rated round. The key complication is that whether a round is rated for the participant depends on their current rating compared to a fixed threshold, and in rated rounds they are allowed to shift their rating within a bounded range.

Each test case gives an initial rating, a threshold that separates two kinds of rounds, a maximum step size for how much the rating can be adjusted before a rated round, and a sequence of rounds labeled as type 1 or type 2. A type 1 round is always rated. A type 2 round is rated only if the current rating is strictly below the threshold; otherwise it becomes unrated and the rating does not change.

When a round is rated, the player can choose any final rating within a symmetric interval around the current rating. This makes the process feel like a controlled walk on the number line, except that some steps are “freezed” when the rating is too high.

The task is to maximize how many rounds end up being rated.

The constraints tell us that the number of rounds per test case is at most 1000, and the total over all tests is at most 30000. This immediately suggests that quadratic or near-quadratic dynamic programming over all states and all rounds is acceptable, but anything cubic over 1000 states per step is already borderline. A solution that maintains only a small set or interval of reachable ratings per step is necessary.

The main difficulty is that the rating is unbounded in principle, but only its relation to the threshold matters for type 2 rounds. This suggests that we never need exact tracking of all ratings, only ranges or extremal possibilities that influence whether we stay below or above the threshold.

A subtle failure case arises when greedy decisions are made locally. For example, immediately pushing rating as low as possible might help enable future type 2 rounds, but it could reduce flexibility for type 1 rounds where we might want to stay above threshold to avoid unwanted state changes. The interaction is long-term, so local decisions are unreliable.

## Approaches

A brute-force interpretation is to treat each round as branching over all possible rating values reachable after each rated round. After a rated round, the rating can become any integer in a segment of length 2D around the current rating. If we track all reachable ratings exactly, we quickly get a state explosion: each state expands into O(D) new states, and over n steps this becomes exponential in n in the worst case.

However, the structure of the problem makes this overkill. The only meaningful distinction between ratings is whether they are below X or not, because that determines whether type 2 rounds are active. Inside the below-X region and above-X region, we only care about how reachable we are and whether we can cross the threshold when needed.

The key insight is that instead of tracking all reachable ratings, we track the best possible “effective position” that maximizes future rated rounds. We observe that when we are in a rated round, we can always move the rating anywhere in an interval of size 2D. This means that after each rated round, the set of possible ratings is always a contiguous interval. This property collapses the state space from potentially many points into a single interval.

Thus, at every step we maintain the minimum and maximum possible rating achievable after maximizing rated rounds so far. For each round, we update this interval depending on whether the round is rated or not, and whether type 2 is active or skipped. When the round is rated, we expand the interval by D in both directions. When it is skipped, the interval remains unchanged. We also need to account for the fact that type 2 rounds become rated only when the current interval intersects below X, which determines whether we gain a point and whether we apply a transition.

This reduces the problem to a linear scan over the rounds with constant-time interval updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all ratings states) | Exponential | Exponential | Too slow |
| Interval DP | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process rounds from left to right while maintaining the range of possible ratings after achieving the maximum number of rated rounds so far.

1. Initialize the current reachable rating interval as a single point at the initial rating R₀. Also initialize the answer as 0.
2. Scan each round in order. For each round, determine whether it is type 1 or type 2.
3. If the round is type 1, it is always rated. We increment the answer by 1. We then update the interval by expanding it to [L - D, R + D], since after a rated round we can choose any rating within D of any previously reachable value, and combining all possibilities yields a full expanded interval. This step ensures we preserve all future possibilities.
4. If the round is type 2, we first check whether it is possible for this round to be rated, meaning there exists at least one rating in the current interval that is strictly less than X. This is equivalent to checking whether the interval’s minimum value is less than X.
5. If the type 2 round is rated under the current interval, we increment the answer by 1. We then update the interval in the same way as for type 1, expanding it by D on both sides.
6. If the type 2 round is not rated, we do not change the interval, since the rating remains frozen during unrated rounds.
7. Continue this process until all rounds are processed, and output the accumulated count of rated rounds.

The key idea is that we always preserve the full range of achievable ratings after maximizing decisions so far. We never need to choose a single trajectory because the interval already represents all optimal possibilities.

### Why it works

The correctness rests on the invariant that after processing each prefix of rounds, the interval [L, R] represents exactly the set of all ratings that can be achieved after maximizing the number of rated rounds up to that point.

When a round is rated, every point in the previous interval can be moved independently within ±D, and the union of all resulting intervals is again a single continuous interval. When a round is not rated, no transition occurs, so the reachable set remains unchanged. Since type 2 rounds are decided solely by whether any feasible rating lies below X, checking the interval minimum is sufficient to decide whether the round can be made rated in some optimal execution.

Because we never discard any reachable rating that could lead to more rated rounds later, the final count is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        R0, X, D, n = map(int, input().split())
        s = input().strip()

        L = R0
        R = R0
        ans = 0

        for c in s:
            if c == '1':
                ans += 1
                L -= D
                R += D
            else:
                if L < X:
                    ans += 1
                    L -= D
                    R += D
                else:
                    pass

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the interval interpretation. The variables L and R represent the full range of possible ratings after maximizing rated rounds. For every type 1 round, we always expand the interval and increment the answer.

For type 2 rounds, the condition `L < X` is sufficient because if the minimum possible rating is already above or equal to X, then no execution path can make the rating low enough to qualify, given that the interval contains all reachable states. Once the round is considered rated, we again apply the same expansion rule.

A subtle detail is that we never try to “force” the rating into a particular region; the interval automatically encodes all valid choices. This avoids any backtracking or case splitting.

## Worked Examples

### Example 1

Input:

```
R0=2098, X=2100, D=5
s = 111211
```

We track interval and answer:

| Step | Round | Interval [L, R] | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | [2098, 2098] | rated, expand | 1 |
| 2 | 1 | [2093, 2103] | rated, expand | 2 |
| 3 | 1 | [2088, 2108] | rated, expand | 3 |
| 4 | 2 | [2083, 2113] | rated (L < X) | 4 |
| 5 | 1 | [2078, 2118] | rated, expand | 5 |
| 6 | 1 | [2073, 2123] | rated, expand | 6 |

This shows how once the interval dips below X, type 2 rounds become fully usable.

### Example 2

Input:

```
R0=2100, X=2100, D=5
s = 222
```

| Step | Round | Interval [L, R] | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | [2100, 2100] | not rated (L ≥ X) | 0 |
| 2 | 2 | [2100, 2100] | not rated | 0 |
| 3 | 2 | [2100, 2100] | not rated | 0 |

Here the interval never reaches below X, so type 2 rounds never activate.

These examples show that the entire behavior reduces to whether the interval ever intersects the “eligible region” below X.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each round performs constant-time interval updates |
| Space | O(1) | Only two integers are maintained |

The total number of rounds across all test cases is at most 30000, so the solution runs easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        R0, X, D, n = map(int, input().split())
        s = input().strip()

        L = R0
        R = R0
        ans = 0

        for c in s:
            if c == '1':
                ans += 1
                L -= D
                R += D
            else:
                if L < X:
                    ans += 1
                    L -= D
                    R += D

        out.append(str(ans))
    return "\n".join(out) + "\n"

# provided samples
assert run("""4
2100 2100 5 3
222
2098 2100 5 6
111211
2115 2100 226 7
2211121
0 10 4 8
22111121
""") == """0
6
5
8
"""

# minimum case
assert run("""1
0 1 1 1
1
""") == """1
"""

# all type 2 impossible
assert run("""1
100 50 10 3
222
""") == """0
"""

# all type 1
assert run("""1
5 100 2 4
1111
""") == """4
"""

# alternating stress
assert run("""1
10 10 3 6
121212
""") == """6
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single type 1 | 1 | basic expansion |
| all type 2 blocked | 0 | threshold never reached |
| all type 1 | 4 | repeated growth correctness |
| alternating pattern | 6 | interaction of both rules |

## Edge Cases

One edge case is when the initial rating is already below the threshold. In this situation, the first type 2 round is immediately eligible, and the interval begins expanding from the start. The algorithm handles this naturally because the condition `L < X` is true at initialization, so no special casing is needed.

Another edge case is when the rating starts far above X and D is small. In such cases, it may take several rated rounds before the interval ever dips below X. The interval representation ensures this transition is captured implicitly as repeated expansions eventually shift the lower bound downward only when ratings can be chosen freely across the whole interval.

A final edge case is when X is extremely large compared to all reachable ratings. Then no type 2 round is ever counted. The algorithm correctly leaves the answer unchanged because the interval never intersects below X.
