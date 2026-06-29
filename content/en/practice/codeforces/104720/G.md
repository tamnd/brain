---
title: "CF 104720G - Food Quiz"
description: "We are given a quiz system where each question is answered by choosing exactly one option from a fixed set of choices. Every choice has a numeric value, and the total quiz result is just the sum of the values chosen across all questions."
date: "2026-06-29T07:11:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "G"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 69
verified: false
draft: false
---

[CF 104720G - Food Quiz](https://codeforces.com/problemset/problem/104720/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a quiz system where each question is answered by choosing exactly one option from a fixed set of choices. Every choice has a numeric value, and the total quiz result is just the sum of the values chosen across all questions. Importantly, every question shares the same list of possible values, so the structure is uniform: we repeat the same selection process independently for each of the n questions.

Once a total score is formed, it is matched against several disjoint numeric intervals, each interval corresponding to a particular food. For every food, we must determine whether there exists at least one way to answer the quiz such that the resulting sum falls inside that food’s interval.

The core computational task is therefore not to construct all answers explicitly, but to understand which total sums are achievable after n independent selections from the same multiset of values, and then to check membership of those sums inside given ranges.

The constraints are small enough to strongly suggest a state-space dynamic programming solution. With n and m both at most 20, the total number of selections is at most 20 steps, and each step offers up to 20 choices. Any exponential enumeration of all m^n possibilities would grow as 20^20, which is far beyond feasible limits. However, the maximum possible sum is tightly bounded: each value is at most 20, so the largest sum is 400. This makes it possible to track reachability over a small integer range.

A subtle issue that can cause incorrect solutions is forgetting that different sequences can lead to the same sum. Treating sequences as distinct is unnecessary and expensive; only the set of achievable sums matters. Another common mistake is assuming greedy construction works, for example always picking minimum or maximum values per question. That fails because intermediate combinations can unlock sums that pure extremes cannot reach. For instance, with values [1, 10] and n = 2, the sum 11 is achievable, but a greedy strategy might incorrectly miss such combinations if it reasons locally per question.

## Approaches

The naive approach is to enumerate every possible way to answer the quiz. Each of the n questions has m choices, so the total number of complete answer sheets is m^n. For each, we compute a sum and mark it as reachable. This is correct because it explicitly constructs every possibility, but its runtime grows exponentially. With m and n both up to 20, this becomes 20^20 combinations, which is far beyond any feasible computation.

The key observation is that the order of questions does not matter for the sum, and the same value set is reused at every step. This transforms the problem into a repeated sumset construction: starting from a set containing only 0, we repeatedly add one more layer where we add each value in v to all previously reachable sums. After n layers, we obtain all achievable totals. Since the maximum sum is only 400, we can safely maintain a boolean DP over sums and iterate n times.

This reduces the problem from exponential enumeration over sequences to polynomial-time propagation over a bounded state space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n · n) | O(1) | Too slow |
| Optimal DP | O(n · m · S) where S ≤ 400 | O(S) | Accepted |

## Algorithm Walkthrough

## Optimal DP Construction

1. Initialize a boolean array dp where dp[s] indicates whether a sum s is achievable after processing some number of questions. Set dp[0] = true because before answering any questions, the sum is zero.
2. Repeat the following process exactly n times, once per question. Each iteration represents adding one more chosen value to the total sum.
3. For each iteration, create a new array next_dp initialized to false. This array will store all sums reachable after answering one more question.
4. For every sum s such that dp[s] is true, try extending it with every possible value v_i. Mark next_dp[s + v_i] as true. This corresponds to choosing answer v_i for the current question.
5. After processing all sums and values, replace dp with next_dp. This ensures that each layer only uses results from the previous number of questions, avoiding accidental reuse within the same step.
6. After completing all n iterations, dp encodes all possible final scores.
7. For each food interval [l, r], check whether there exists any s in this range such that dp[s] is true. If such a sum exists, the answer is YES; otherwise NO.

The reason we can safely scan each interval independently is that each food decision depends only on existence of at least one valid sum, not on how many such sums exist or how they overlap with other intervals.

### Why it works

The DP maintains the invariant that after i iterations, dp exactly represents all sums achievable using i question selections. Each transition adds exactly one choice from the allowed set of values, preserving correctness because every valid sequence of length i + 1 can be decomposed into a valid sequence of length i plus one final choice. Conversely, every constructed transition corresponds to a real sequence of selections. This bijection between transitions and valid answer sequences guarantees completeness and soundness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    v = list(map(int, input().split()))
    q = int(input())
    intervals = [tuple(map(int, input().split())) for _ in range(q)]

    max_sum = n * max(v)
    dp = [False] * (max_sum + 1)
    dp[0] = True

    for _ in range(n):
        ndp = [False] * (max_sum + 1)
        for s in range(max_sum + 1):
            if not dp[s]:
                continue
            for val in v:
                if s + val <= max_sum:
                    ndp[s + val] = True
        dp = ndp

    for l, r in intervals:
        ok = False
        for s in range(l, r + 1):
            if 0 <= s <= max_sum and dp[s]:
                ok = True
                break
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the DP construction directly. The dp array is reallocated at each step to prevent mixing states from different question counts. The boundary check ensures we never index beyond the maximum possible sum n · max(v). Interval checking is done by a simple scan since the total range is small enough that even full traversal is trivial.

A common pitfall is attempting to update dp in place. That would incorrectly allow multiple uses of the same question
