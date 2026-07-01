---
title: "CF 104095A - \u73ed\u59d4\u7ade\u9009"
description: "Each student either competes for exactly one position or none of them matter for a given position. For every position, we must look at all students who applied for that position and select the one with the highest vote count."
date: "2026-07-02T02:19:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104095
codeforces_index: "A"
codeforces_contest_name: "2020 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 104095
solve_time_s: 161
verified: true
draft: false
---

[CF 104095A - \u73ed\u59d4\u7ade\u9009](https://codeforces.com/problemset/problem/104095/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

Each student either competes for exactly one position or none of them matter for a given position. For every position, we must look at all students who applied for that position and select the one with the highest vote count. If multiple students achieve the same maximum number of votes, the tie is resolved by choosing the smallest student index.

The input gives a list of students, where each student declares one target position and a vote count. The task is to reconstruct, for every position from $1$ to $m$, which student wins that position after applying the “maximum votes, then smallest index” rule.

The bounds are very small: $n \le 51$ and $m \le 12$. This removes any concern about efficiency. Even an $O(nm)$ or $O(n^2)$ simulation is trivially fast. The only real requirement is correctness of grouping and tie-breaking.

The most common failure case comes from forgetting tie-breaking order or failing to correctly group students by position. For example, if two students target the same position with equal votes, picking the later input instead of the smaller index produces an incorrect answer even though all values are processed.

Another subtle issue is assuming that positions are independent but accidentally mixing indices across positions due to shared variables or not resetting per-position maxima.

## Approaches

The structure of the problem is already the optimal approach. Each position is independent, so the natural solution is to group all candidates by their chosen position and compute a simple maximum.

A brute-force interpretation would, for each position, scan all students and pick the best candidate. This works because each position decision is independent and requires only a linear scan. The cost is $O(nm)$ operations, since for each of the $m$ positions we check all $n$ students. With the given constraints, this is already minimal and efficient.

The key observation is that no interaction exists between positions. A student belongs to exactly one group, so we never need global sorting or matching. The entire problem reduces to repeated maximum selection with a lexicographic key of $(t_i, -i)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scanning per position | $O(nm)$ | $O(1)$ extra | Accepted |
| Group + single pass | $O(n + m)$ | $O(m)$ | Accepted |

Both are effectively the same in practice; the grouped version just makes the structure clearer.

## Algorithm Walkthrough

1. Create an array `best_id` of size $m$ initialized to $0$, representing the current winner for each position. Also maintain `best_score` initialized to $0$ for each position. This setup encodes the invariant that each position always stores its current best candidate.
2. Read each student $i$ from $1$ to $n$, with chosen position $c_i$ and votes $t_i$.
3. For the position $c_i$, compare $t_i$ with the current best score stored in `best_score[c_i]`.
4. If $t_i$ is larger than the current best score, replace both `best_score[c_i]` and `best_id[c_i]` with $t_i$ and $i$. This ensures that the position keeps the highest vote candidate seen so far.
5. If $t_i$ equals the current best score, compare student indices. If $i$ is smaller than the stored best index, replace the stored winner. This enforces the tie-breaking rule.
6. After processing all students, output `best_id[1]` through `best_id[m]`.

### Why it works

At any point during processing, each position stores the best candidate among all students seen so far for that position under lexicographic ordering by $(t_i, -i)$. Each new student is either strictly better, strictly worse, or tied in votes, and in the tied case only the smallest index survives. Since every student is processed exactly once and comparisons are monotone updates, the final stored values must be the global maxima for each position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    best_score = [0] * (m + 1)
    best_id = [0] * (m + 1)

    for i in range(1, n + 1):
        c, t = map(int, input().split())
        if t > best_score[c]:
            best_score[c] = t
            best_id[c] = i
        elif t == best_score[c] and i < best_id[c]:
            best_id[c] = i

    print(*best_id[1:])

if __name__ == "__main__":
    solve()
```

The solution maintains two arrays indexed by position. One stores the best vote count seen so far, and the other stores the corresponding student index. The update logic directly encodes the selection rule, and the final output simply lists winners per position in order.

A subtle point is initialization: setting `best_score` to $0$ is valid because vote counts are guaranteed to be at least $1$. Another detail is that `best_id` starts at $0$, which works because any real student index is at least $1$, so the first valid candidate always overwrites it.

## Worked Examples

### Example 1

Input:

```

```

We track state per position.

| Student | Position | Votes | best_score[1] | best_id[1] | best_score[2] | best_id[2] |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 5 | 1 | 0 | 0 |
| 2 | 1 | 3 | 5 | 1 | 0 | 0 |
| 3 | 2 | 4 | 5 | 1 | 4 | 3 |

Final output is `1 3`.

This confirms that later weaker candidates do not overwrite stronger ones.

### Example 2

Input:

```

```

| Student | Position | Votes | best_score[1] | best_id[1] | best_score[2] | best_id[2] |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 7 | 0 | 0 | 7 | 1 |
| 2 | 2 | 7 | 0 | 0 | 7 | 1 |
| 3 | 1 | 5 | 5 | 3 | 7 | 1 |
| 4 | 1 | 5 | 5 | 3 | 7 | 1 |

Final output is `3 1`.

This shows tie-breaking: for position 1, students 3 and 4 tie on votes, so the smaller index 3 remains. For position 2, student 1 remains because later equal entries do not replace earlier smaller index.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each student is processed once with constant-time updates |
| Space | $O(m)$ | Arrays store best candidate per position |

The constraints $n \le 51$ and $m \le 12$ are far below typical limits, so even less optimized solutions would pass easily. The chosen approach is optimal in structure and constant factors.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 1 5 | basic correctness and grouping |
| single position | 1 | aggregation and tie-breaking |
| tie case | 1 3 | smallest index rule |
| identity case | 1 2 3 | independent positions |

## Edge Cases

A critical edge case is when multiple students compete for the same position with identical votes. The algorithm handles this by comparing indices only when vote counts are equal, ensuring the smallest index is preserved.

Another edge case is when a position receives only one candidate. The initialization with zero ensures the first candidate always becomes the winner.

A final corner case is when candidates for different positions interleave in input order. Since each update only touches its own position index, no interference occurs across positions, preserving correctness automatically.
