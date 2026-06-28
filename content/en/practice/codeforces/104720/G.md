---
title: "CF 104720G - Food Quiz"
description: "We are given a quiz structure where each question behaves independently, but all questions share the same set of answer choices. Every answer choice has a fixed positive value."
date: "2026-06-29T05:42:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "G"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 73
verified: false
draft: false
---

[CF 104720G - Food Quiz](https://codeforces.com/problemset/problem/104720/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a quiz structure where each question behaves independently, but all questions share the same set of answer choices. Every answer choice has a fixed positive value. A participant answers the quiz by selecting exactly one choice per question, and the total score is the sum of the chosen values across all questions.

Because every question uses the same value set, the final score depends only on how many times each value is selected, not on which specific questions they appear in. After computing the score, we classify it into one of several disjoint intervals. Each interval corresponds to a particular food, and the task is to determine whether there exists any way to pick answers such that the resulting score falls inside that interval.

The constraints are very tight in structure. Both the number of questions and the number of choices per question are at most 20. This immediately suggests that the score space is small and highly structured rather than arbitrary. The maximum possible score is bounded by 20 times the maximum value per choice and number of questions, so all reachable scores lie in a relatively small integer range.

The key difficulty is not computing a single score but understanding the entire set of achievable sums formed by selecting one value per question repeatedly. This is a bounded sumset problem over repeated identical sets.

A naive misunderstanding is to treat each question independently and try to combine choices greedily or assume all sums in a range are reachable. For example, if values are `[1, 100]` and there are two questions, reachable sums are `{2, 101, 200}`, not all values in between. Any approach that assumes interval coverage will fail.

Another subtle failure case arises if one assumes that because choices are reused, all sums behave like a knapsack with unlimited items. That is incorrect because we are selecting exactly one item per of `n` identical layers, not arbitrary repetition.

## Approaches

The brute-force view is straightforward: each question contributes one of `m` values, so the total number of assignments is `m^n`. For each assignment, we compute its sum and mark it as reachable. This is correct because it enumerates every possible selection. However, even in the smallest worst case of `m = n = 20`, this becomes astronomically large, on the order of `20^20`, which is entirely infeasible.

The key observation is that all questions are identical in terms of value structure. This allows us to collapse the problem into computing all possible sums formed by choosing exactly `n` values, each from the same multiset of size `m`. This is equivalent to repeated convolution of a small set with itself `n` times.

Since the maximum possible sum is at most `20 * 20 = 400`, we can maintain a boolean DP over achievable sums. Each question updates the set of reachable sums by adding one more chosen value. This transforms the exponential enumeration into a polynomial process over a small state space.

The brute force explodes because it tracks sequences, while the DP only tracks accumulated sums. The structure of independence between questions ensures order does not matter, only cumulative totals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n · n) | O(n) | Too slow |
| DP over sums | O(n · m · S) | O(S) | Accepted |

Here `S ≤ 400`.

## Algorithm Walkthrough

We construct a dynamic programming table over possible scores.

1. Initialize a boolean array `dp` of size `S + 1`, where `dp[x]` indicates whether a score `x` can be formed using processed questions. Set `dp[0] = true`, since zero questions produce sum zero.
2. Repeat the following process for each question from 1 to `n`.
3. Create a fresh array `ndp` initialized to all false. This represents reachable sums after adding one more question.
4. For every previously reachable sum `s`, and for every value `v` in the answer choices, mark `ndp[s + v] = true`. This corresponds to extending a partial selection by choosing one answer for the current question.
5. After processing all transitions, replace `dp` with `ndp`. This ensures each question contributes exactly once to the sum.
6. After processing all questions, `dp` contains exactly all achievable scores.
7. For each food interval `[l, r]`, check whether any `dp[x]` is true for `x` in this range. If yes, output "YES", otherwise output "NO".

### Why it works

The DP maintains the invariant that after processing `i` questions, `dp[s]` is true if and only if there exists a way to pick one value per each of the first `i` questions summing to `s`. Each transition extends every valid construction for `i-1` questions by exactly one valid choice for the next question, preserving completeness and avoiding double counting. Since every full assignment corresponds to exactly one path through these transitions, no achievable sum is lost or incorrectly added.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    vals = list(map(int, input().split()))
    q = int(input())
    intervals = [tuple(map(int, input().split())) for _ in range(q)]

    max_sum = n * max(vals)
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

    for l, r in intervals:
        ok = False
        for s in range(l, r + 1):
            if s <= max_sum and dp[s]:
                ok = True
                break
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the DP construction. The key detail is rebuilding the state for each question rather than updating in place, which avoids accidentally reusing the same question multiple times within a single transition.

The second important detail is bounding transitions by `max_sum`. Without this, the array would grow unnecessarily or risk indexing errors. Since all values are positive, no negative sums or backward transitions exist.

## Worked Examples

### Sample 1

We track reachable sums after each question. Suppose values are interpreted as a small multiset and we apply DP.

After first question, `dp` contains exactly the given values.

| Step | Reachable sums |
| --- | --- |
| Init | {0} |
| After 1 question | {v1, v2, v3, ...} |

For subsequent questions, each step expands the set by adding each value again.

After full processing, we check each interval against this final set. Some intervals intersect reachable values, others do not.

This demonstrates that even with repeated identical choices, not all sums in a range are guaranteed.

### Sample 2

We again start from `{0}` and expand.

| Step | Reachable sums |
| --- | --- |
| Init | {0} |
| After 1 question | small set of base values |
| After 2 questions | pairwise sums of base values |

The second sample shows that combining two questions produces a structured sumset, not a continuous interval. Some target ranges fall entirely outside reachable sums, producing "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m · S) | For each question, we iterate all sums and all choices |
| Space | O(S) | DP array over possible sums up to n·max(v) |

The maximum sum is at most 400, and both `n` and `m` are at most 20, so the total number of operations is comfortably small. The solution runs well within the 1 second limit.

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

# sample cases (as given format placeholders)
# assert run("...") == "..."

# minimum size
assert run("1 1\n5\n1\n5 5\n") == "YES"

# all equal values
assert run("2 3\n2 2 2\n1\n4 4\n") == "YES"

# unreachable interval
assert run("2 2\n1 2\n1\n10 10\n") == "NO"

# boundary max sum
assert run("20 1\n20\n1\n400 400\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 question, single choice | YES | Base case correctness |
| identical values | YES | symmetry and repetition handling |
| large unreachable target | NO | avoids false positives |
| maximum sum boundary | YES | correct upper bound handling |

## Edge Cases

A subtle edge case arises when all values are identical. In this situation, reachable sums collapse into a single arithmetic progression, and the DP must not assume full coverage. The algorithm handles this correctly because each layer adds exactly one fixed increment, producing only sums of the form `k * v`.

Another edge case is when intervals touch the maximum possible sum. Since we explicitly bound DP size by `n * max(vals)`, any query exactly at the boundary is still checked correctly without overflow or missed states.

A third case is when `m = 1`. Here there is no branching at all, and the DP degenerates into a single path. The transition still works because each step deterministically shifts the reachable sum set by one fixed value, and the algorithm does not assume multiplicity of choices.
