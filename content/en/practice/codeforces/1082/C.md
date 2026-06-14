---
title: "CF 1082C - Multi-Subject Competition"
description: "Each candidate belongs to exactly one subject and brings a numeric contribution, which may be positive or negative."
date: "2026-06-15T05:57:55+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1082
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 55 (Rated for Div. 2)"
rating: 1600
weight: 1082
solve_time_s: 132
verified: true
draft: false
---

[CF 1082C - Multi-Subject Competition](https://codeforces.com/problemset/problem/1082/C)

**Rating:** 1600  
**Tags:** greedy, sortings  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

Each candidate belongs to exactly one subject and brings a numeric contribution, which may be positive or negative. We are asked to choose a group of candidates under a structural constraint: after selection, we also choose some set of subjects, and for every chosen subject the number of selected candidates in that subject must be identical.

This constraint forces the solution to balance counts across subjects. If we decide that each chosen subject must contribute exactly $k$ people, then every selected subject must contribute its top $k$ candidates from that subject, because adding a weaker candidate can only reduce the sum and does not help feasibility.

The output is the best possible total sum over all valid choices, or zero if every valid non-empty construction has negative total.

The constraints go up to $10^5$ candidates and subjects. A solution that tries all subsets of subjects or all possible $k$ values per subject independently would immediately fail. Anything quadratic in $n$ or even $n \log^2 n$ with large constants risks timing out.

The most delicate edge case is when all candidates are negative or when only some subjects have positive prefixes. For example, if every value is negative, any non-empty selection produces a negative sum, so the correct answer is zero. Another subtle case is when mixing subjects improves the result even though individual subjects have different optimal counts. A naive greedy that picks best per subject independently can fail because the shared $k$ requirement couples all subjects.

## Approaches

A brute-force idea is to decide a number $k$, and then for each subject independently pick the top $k$ candidates if it has at least $k$ people. After that, we sum contributions over all subjects and choose the best $k$. This is correct because within a fixed $k$, optimality per subject is independent.

However, the cost is in evaluating each $k$. If we try all $k$ from $1$ to $n$, and for each $k$ recompute prefix sums per subject, we would spend $O(n)$ per $k$, leading to $O(n^2)$ operations in the worst case. With $10^5$, this is impossible.

The key observation is that each subject can be preprocessed into a sorted list of skills, and its prefix sums computed once. Then for a fixed $k$, the total contribution is the sum over subjects of their prefix sum at index $k$, if it exists. Instead of recomputing per $k$, we flip the perspective: each prefix sum contributes to all $k$ up to its length, so we can accumulate contributions by iterating over subjects and distributing their prefix sums into a global array indexed by $k$.

This transforms the problem into aggregating contributions over all subjects in linear time after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k and subjects | $O(n^2)$ | $O(n)$ | Too slow |
| Sort + prefix + accumulation | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Group candidates by their subject. This is necessary because the constraint applies within each subject independently.
2. For each subject, sort its skill values in descending order. This ensures that taking the first $k$ elements is optimal for that subject.
3. Build prefix sums for each subject. The prefix at position $i$ represents the best possible sum if we take exactly $i+1$ candidates from that subject.
4. For each subject, iterate over its prefix sums. For the $i$-th prefix sum, add it to a global accumulator for group size $k = i+1$. This represents choosing this subject among those contributing to size $k$.
5. Maintain a global array `best[k]` representing the sum of contributions if every chosen subject contributes exactly $k$ participants.
6. After processing all subjects, scan all $k$ and take the maximum positive value.

The reason step 4 works is that each subject independently contributes to every possible uniform group size $k$, and we are summing compatible contributions across subjects.

### Why it works

Fix a valid solution with group size $k$. In that solution, each chosen subject contributes exactly its top $k$ candidates, otherwise swapping in a better candidate would improve the sum without violating constraints. Therefore every valid solution corresponds exactly to choosing some subset of subjects and summing their $k$-prefix values. The algorithm enumerates all such contributions implicitly and evaluates every possible $k$, so no valid configuration is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

n, m = map(int, input().split())

subjects = defaultdict(list)

for _ in range(n):
    s, r = map(int, input().split())
    subjects[s].append(r)

best = [0] * (n + 1)

for vals in subjects.values():
    vals.sort(reverse=True)
    pref = 0
    for i, v in enumerate(vals):
        pref += v
        k = i + 1
        if pref > 0:
            best[k] += pref

print(max(0, max(best)))
```

The code first groups candidates by subject, then sorts each group so that prefix sums represent optimal choices per fixed group size. The `best` array accumulates contributions indexed by how many people are taken from each subject.

The check `if pref > 0` ensures we only include prefixes that improve the result; negative prefixes would only worsen any configuration using that $k$. This aligns with the final maximization step where we also clamp at zero.

## Worked Examples

### Example 1

Input:

```
6 3
2 6
3 6
2 5
3 5
1 9
3 1
```

After grouping:

| Subject | Sorted values | Prefix sums |
| --- | --- | --- |
| 1 | [9] | [9] |
| 2 | [6, 5] | [6, 11] |
| 3 | [6, 5, 1] | [6, 11, 12] |

Now we distribute:

| k | contribution |
| --- | --- |
| 1 | 9 + 6 + 6 = 21 |
| 2 | 11 + 11 = 22 |
| 3 | 12 |

The maximum is 22.

This confirms that the optimal solution uses $k=2$, meaning two subjects contribute two top students each.

### Example 2

Input:

```
5 3
1 6
2 6
3 11
1 -5
2 0
```

Grouped and sorted:

| Subject | Sorted | Prefix sums |
| --- | --- | --- |
| 1 | [6, -5] | [6, 1] |
| 2 | [6, 0] | [6, 6] |
| 3 | [11] | [11] |

Accumulation:

| k | value |
| --- | --- |
| 1 | 6 + 6 + 11 = 23 |
| 2 | 1 + 6 = 7 |

Best is 23.

This shows how even negative elements can be included if they are compensated by other positives at the same $k$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting all subject lists dominates |
| Space | $O(n)$ | storing grouped values and prefix arrays |

The sorting step is acceptable for $10^5$ elements. All other operations are linear passes over the data, which keeps runtime comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    n, m = map(int, input().split())
    subjects = defaultdict(list)

    for _ in range(n):
        s, r = map(int, input().split())
        subjects[s].append(r)

    best = [0] * (n + 1)

    for vals in subjects.values():
        vals.sort(reverse=True)
        pref = 0
        for i, v in enumerate(vals):
            pref += v
            k = i + 1
            if pref > 0:
                best[k] += pref

    return str(max(0, max(best)))

# provided sample
assert run("""6 3
2 6
3 6
2 5
3 5
1 9
3 1
""") == "22"

# all negative
assert run("""3 2
1 -1
1 -2
2 -3
""") == "0"

# single subject
assert run("""4 2
1 5
1 4
1 -10
1 3
""") == "12"

# mixed subjects optimal k=1
assert run("""3 3
1 10
2 9
3 8
""") == "27"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all negative | 0 | correct handling of empty optimal set |
| single subject | 12 | prefix selection within one group |
| mixed k=1 | 27 | global aggregation across subjects |

## Edge Cases

A fully negative instance demonstrates the fallback behavior. For input like `[-1, -2, -3]` across subjects, every prefix sum is negative, so no $k$ accumulates positive value, and the algorithm correctly returns zero because `max(best)` is negative or zero.

A single-subject input tests that the algorithm does not require multiple subjects to form a valid solution. The subject’s best prefix sum directly becomes the answer, and the accumulation mechanism still works because only one subject contributes.

A sparse distribution where each subject has only one candidate ensures the algorithm correctly handles all possible $k=1$ contributions. Each subject contributes exactly once to `best[1]`, and no higher $k$ is populated, making the maximum correctly reflect the sum of all positive single entries.
