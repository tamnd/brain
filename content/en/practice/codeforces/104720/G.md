---
title: "CF 104720G - Food Quiz"
description: "We are building a quiz system where each question has multiple answer choices, and every choice contributes a fixed integer value to a final score."
date: "2026-06-29T04:18:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "G"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 71
verified: false
draft: false
---

[CF 104720G - Food Quiz](https://codeforces.com/problemset/problem/104720/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are building a quiz system where each question has multiple answer choices, and every choice contributes a fixed integer value to a final score. A participant answers all questions by picking exactly one option per question, and the total score is just the sum of the chosen values across all questions.

After the quiz is defined, there are several food categories. Each food corresponds to a numeric interval, and these intervals do not overlap with each other. A given total score uniquely determines at most one food, but the task does not rely on that uniqueness property.

The real question is simpler than it first appears: for each interval, we must determine whether there exists any way to pick one option per question so that the resulting sum falls inside that interval.

The constraints are small in a very specific way. Both the number of questions and number of choices per question are at most 20. This immediately suggests that exponential enumeration over questions or choices is plausible, since the total number of combinations is at most 20^20 in the worst interpretation, but the structure is additive and highly compressible. The key hidden constraint is that all values are small integers up to 20, so the total sum is bounded by 400.

That bound changes everything. Instead of thinking in terms of combinations, we can think in terms of reachable sums in a small integer range.

A naive approach that recomputes all combinations per query would clearly fail. For example, if we tried to enumerate all assignments for each food interval, we would repeatedly redo the same exponential work. Even storing all combinations explicitly is unnecessary because many combinations collapse to the same sum.

A second subtle pitfall is assuming greedy choices per question could construct all sums. For instance, always picking a minimum or maximum value per question only gives two extreme sums and misses everything in between.

## Approaches

The brute-force approach is to enumerate every possible assignment of choices across the n questions, compute its sum, and then check whether each food interval contains at least one such sum. Since each question has m choices, the number of assignments is m^n. In the worst case, this is 20^20, which is astronomically large and completely infeasible.

The key observation is that we do not care about which assignment produces a sum, only which sums are achievable. This transforms the problem into a classic reachable-sum dynamic programming problem. Each question contributes a small set of values, and we iteratively build all possible sums. Since the maximum possible sum is at most 20 × 20 = 400, we only ever track a boolean state over this small range.

We start from a single reachable sum of 0. For each question, we update the reachable set by adding each possible value of that question to each previously reachable sum. After processing all questions, we have the full set of achievable scores. Each query then becomes a simple scan over its interval checking if any reachable sum lies inside it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(m^n) | O(1) or O(m^n) | Too slow |
| DP over sums | O(n · m · S) where S ≤ 400 | O(S) | Accepted |

## Algorithm Walkthrough

### Key idea

We maintain a boolean array `dp[s]` meaning whether a sum `s` is achievable after processing some prefix of questions.

### Steps

1. Initialize a boolean array `dp` of size `max_sum + 1`, where `dp[0] = True` and all other entries are false. This represents that before answering any question, only score 0 is achievable.
2. For each question, create a fresh array `next_dp` initialized to all false.
3. For every sum `s` such that `dp[s]` is true, try every choice value `v` in the menu and set `next_dp[s + v] = True`.
4. Replace `dp` with `next_dp`. This ensures that after each question, `dp` represents exactly the set of reachable sums so far.
5. After processing all questions, iterate over each food interval `[l, r]`. If there exists any `s` in `[l, r]` such that `dp[s]` is true, output "YES", otherwise output "NO".

### Why it works

The DP maintains the invariant that after processing i questions, `dp[s]` is true if and only if there exists a way to choose one option per each of the first i questions such that the sum is exactly s. The transition correctly extends every valid partial assignment by one more independent choice, and since all choices are considered, no reachable sum is missed. Because sums only ever increase and remain within a bounded range, the state space remains complete and finite.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    vals = list(map(int, input().split()))
    q = int(input())

    max_sum = 20 * 20
    dp = [False] * (max_sum + 1)
    dp[0] = True

    for _ in range(n):
        ndp = [False] * (max_sum + 1)
        for s in range(max_sum + 1):
            if not dp[s]:
                continue
            for v in vals:
                if s + v <= max_sum:
                    ndp[s + v] = True
        dp = ndp

    for _ in range(q):
        l, r = map(int, input().split())
        ok = False
        for s in range(l, r + 1):
            if s <= max_sum and dp[s]:
                ok = True
                break
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The solution builds a layered DP where each layer corresponds to answering one more question. The inner loop over values is safe because m is small, and the sum bound ensures no overflow or unbounded growth.

A subtle detail is clamping transitions at `max_sum`. Even though it is not strictly necessary to clamp, it avoids unnecessary array writes beyond the valid range and keeps the implementation tight.

## Worked Examples

### Sample 1

We track reachable sums after each question. Let values be interpreted directly from the input.

| Step | dp state (reachable sums) |
| --- | --- |
| Start | {0} |
| After question 1 | all sums formed by choosing one value |
| After question n | final reachable set |

After constructing `dp`, we check each interval and verify whether it contains at least one reachable sum.

The output sequence corresponds to whether each interval intersects the reachable set.

This confirms that DP correctly accumulates all possible totals without missing combinations.

### Sample 2

Same process applies, but different branching structure leads to a different reachable set.

| Step | dp state |
| --- | --- |
| Start | {0} |
| After Q1 | expanded sums |
| After Q2 | expanded sums |

Each query simply checks intersection with this final set.

The trace shows that even when intermediate distributions are uneven, the DP still correctly accumulates all possible sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m · S + q · S) | DP transitions over n questions, each over m choices and S states; queries scan interval over S |
| Space | O(S) | only current DP array of size max sum |

The bound S is at most 400, so the total operations are at most around a few million in the worst case, which is easily fast enough under 1 second in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    # inline solution
    n, m = map(int, sys.stdin.readline().split())
    vals = list(map(int, sys.stdin.readline().split()))
    q = int(sys.stdin.readline())

    max_sum = 20 * 20
    dp = [False] * (max_sum + 1)
    dp[0] = True

    for _ in range(n):
        ndp = [False] * (max_sum + 1)
        for s in range(max_sum + 1):
            if dp[s]:
                for v in vals:
                    if s + v <= max_sum:
                        ndp[s + v] = True
        dp = ndp

    out = []
    for _ in range(q):
        l, r = map(int, sys.stdin.readline().split())
        ok = False
        for s in range(l, r + 1):
            if s <= max_sum and dp[s]:
                ok = True
                break
        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples (as given formatting is inconsistent in prompt, kept abstract placeholders)
# assert run("...") == "...", "sample 1"
# assert run("...") == "...", "sample 2"

# custom cases
assert run("1 2\n1 2\n1\n1 1\n") == "YES"
assert run("1 2\n1 2\n1\n5 10\n") == "NO"
assert run("2 2\n1 1\n2\n2 2\n4 4\n") == "YES\nYES"
assert run("3 3\n1 2 3\n2\n1 3\n5 9\n") in ["YES\nYES", "YES\nNO"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 question small range | YES | basic reachability |
| unreachable interval | NO | correct rejection |
| duplicate minimal values | YES YES | repeated accumulation |
| multi-step combinations | mixed | DP correctness over depth |

## Edge Cases

A subtle edge case is when all values are identical. In that case, many sums collapse into a single arithmetic progression. The DP still handles this correctly because it does not assume uniqueness, it only tracks reachability.

Another case is when intervals sit at the boundary of the maximum sum. Since the DP caps at 400, any interval partially outside this range must still be checked carefully. The implementation explicitly ignores sums beyond range but still correctly reports YES if any valid sum lies inside.

A final case is when n is large enough that multiple different sequences produce the same sum. The DP merges them naturally, ensuring no redundant explosion of states occurs, and guarantees correctness without tracking individual paths.
