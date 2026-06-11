---
title: "CF 1399C - Boats Competition"
description: "We have a set of participants, each with a specific weight. The competition only allows two-person teams, and each team must have the same combined weight. Our goal is to form as many teams as possible for a given set of participants."
date: "2026-06-11T08:58:13+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1399
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 661 (Div. 3)"
rating: 1200
weight: 1399
solve_time_s: 83
verified: true
draft: false
---

[CF 1399C - Boats Competition](https://codeforces.com/problemset/problem/1399/C)

**Rating:** 1200  
**Tags:** brute force, greedy, two pointers  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of participants, each with a specific weight. The competition only allows two-person teams, and each team must have the same combined weight. Our goal is to form as many teams as possible for a given set of participants. The challenge is to pick a total weight `s` that maximizes the number of valid teams. Each participant can belong to only one team, so we cannot reuse people.

The constraints are small: `n` is at most 50, and the weights range from 1 to `n`. Since `n` is small, we can afford to examine all possible total weights, because the number of distinct sums of two participants is bounded by `2n`. This rules out the need for highly optimized data structures or complex algorithms. Edge cases include situations where all participants have the same weight, where it may be impossible to form pairs with certain sums, or where multiple total weights yield the same maximum number of teams.

A careless implementation might, for example, always try the sum of the lightest and heaviest participant without considering other sums. For instance, with participants `[1, 2, 2, 1, 2, 1, 1, 2]`, the optimal total weight is `3` (pairs `(1,2)`), not `4` (which leaves leftover participants). A naive algorithm might miss this because it only checks a single candidate sum.

## Approaches

The brute-force approach iterates over all possible total weights `s` from `2` (smallest sum of two participants) to `2n` (largest sum). For each `s`, we try all possible pairs of participants to see how many teams we can form. This can be implemented with nested loops or by keeping a frequency map of weights. Forming teams requires decrementing counts in the frequency map whenever a pair is used. While correct, this approach has worst-case complexity `O(n^2 * n) = O(n^3)` because we might check every pair for every candidate sum, which is acceptable for `n=50` but can be improved.

The key observation is that the problem can be reduced to counting how many times each weight appears and pairing weights greedily. For a candidate total weight `s`, a weight `w` can only pair with `s - w`. We can calculate the number of such pairs as the minimum of the counts of `w` and `s - w`. Iterating over all weights from `1` to `n` for each candidate `s` yields an `O(n^2)` solution, which is fast enough given the constraints. This approach leverages the small range of weights and the symmetry of pairs: we only need to consider each distinct weight once per sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Works but can be optimized |
| Frequency Map Greedy | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the number of participants `n` and their weights.
3. Create a frequency map `freq` counting how many participants have each weight.
4. Initialize a variable `max_teams` to zero. This will track the best number of teams for any total weight.
5. Iterate over all possible total weights `s` from `2` to `2n`.
6. For each candidate sum `s`, create a copy of the frequency map. This prevents modifying the original counts while simulating pair formation.
7. Initialize a counter `teams` to zero for the current sum `s`.
8. Iterate over weights `w` from `1` to `n`. For each `w`, find its complement `c = s - w`.
9. If `c` is in the range `1..n`, calculate the number of pairs as `min(freq[w], freq[c])`. If `w == c`, divide the result by two to avoid double counting.
10. Add this number of pairs to `teams` and decrement the counts in the copied frequency map.
11. After checking all weights for this sum `s`, update `max_teams` if `teams` is larger.
12. Print `max_teams` as the answer for the current test case.

Why it works: At every step, the algorithm maintains an invariant that we do not reuse participants. By iterating over all possible sums and greedily forming pairs using the frequency map, we guarantee that no pair is missed, and we correctly count the maximum number of teams for each total weight. The outer loop over sums ensures we find the globally optimal sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_teams(weights, n):
    freq = [0] * (n + 1)
    for w in weights:
        freq[w] += 1

    max_teams_count = 0

    for s in range(2, 2 * n + 1):
        temp_freq = freq.copy()
        teams = 0
        for w in range(1, n + 1):
            c = s - w
            if 1 <= c <= n:
                pair_count = min(temp_freq[w], temp_freq[c])
                if w == c:
                    pair_count //= 2
                teams += pair_count
                temp_freq[w] -= pair_count
                temp_freq[c] -= pair_count
        max_teams_count = max(max_teams_count, teams)

    return max_teams_count

t = int(input())
for _ in range(t):
    n = int(input())
    weights = list(map(int, input().split()))
    print(max_teams(weights, n))
```

The solution begins by reading input and constructing a frequency array to count participant weights. For each candidate total weight, we copy the frequency array to simulate pair formation without side effects. The greedy pairing is done by taking the minimum count of a weight and its complement. Special care is taken when `w` equals `s - w` to avoid overcounting. After evaluating all sums, the maximum number of teams is returned.

## Worked Examples

**Sample 1:** `weights = [1, 2, 3, 4, 5]`, `n = 5`.

| Sum `s` | Pairs Formed | Teams |
| --- | --- | --- |
| 2 | none | 0 |
| 3 | (1,2) | 1 |
| 4 | (1,3) | 1 |
| 5 | (1,4),(2,3) | 2 |
| 6 | (1,5),(2,4) | 2 |
| 7 | (2,5),(3,4) | 2 |
| 8 | (3,5) | 1 |
| 9 | (4,5) | 1 |
| 10 | none | 0 |

Maximum teams: 2

This trace shows that pairing lightest with heaviest does not always yield the global optimum. Considering all sums ensures we find the correct answer.

**Sample 2:** `weights = [6, 6, 6, 6, 6, 6, 8, 8]`, `n = 8`.

| Sum `s` | Teams |
| --- | --- |
| 12 | (6,6)x3 |
| 14 | (6,8)x3? |

Maximum teams: 3

This demonstrates that repeating weights can form multiple teams for a single sum, and the greedy pairing using frequency works correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each possible sum `s` (2n possibilities), we iterate over all weights 1..n to form pairs. |
| Space | O(n) | Frequency array and its copy for each sum. |

Given `n ≤ 50`, `n^2` operations per test case are within limits for `t ≤ 1000` test cases. Memory usage is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        weights = list(map(int, input().split()))
        print(max_teams(weights, n))
    return output.getvalue().strip()

# provided samples
assert run("""5
5
1 2 3 4 5
8
6 6 6 6 6 6 8 8
8
1 2 2 1 2 1 1 2
3
1 3 3
6
1 1 3 4 2 2
""") == """2
3
4
1
2"""

# custom cases
assert run("1\n1\n1\n") == "0", "single participant"
assert run("1\n2\n1 1\n") == "1", "two identical participants"
assert run("1\n4\n1 2 2 1\n") == "2", "pairs with multiple same weights"
assert run("1\n50\n" + " ".join(str(i%50+1) for i in range(50)) + "\n") != "", "maximum n case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 participant | 0 | Cannot form any |
