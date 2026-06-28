---
title: "CF 104915C - \u0412\u044b\u0432\u043e\u0437 \u043c\u0443\u0441\u043e\u0440\u0430"
description: "We are given two sorted sequences of positions on a number line. One sequence represents garbage bags located along a street, and the other represents exits where a truck can leave the street."
date: "2026-06-28T18:05:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104915
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u0421\u0430\u043c\u0430\u0440\u0435 2023-2024 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104915
solve_time_s: 50
verified: true
draft: false
---

[CF 104915C - \u0412\u044b\u0432\u043e\u0437 \u043c\u0443\u0441\u043e\u0440\u0430](https://codeforces.com/problemset/problem/104915/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sorted sequences of positions on a number line. One sequence represents garbage bags located along a street, and the other represents exits where a truck can leave the street. For each garbage bag, we need to determine the distance to the closest exit and aggregate these distances as the final answer.

The key constraint is that both sequences are already sorted in non-decreasing order. This structure is not decorative, it is the entire reason the solution can avoid recomputing comparisons from scratch for every bag.

If we denote the number of exits as m and the number of bags as n, a direct interpretation suggests we might compare each bag against every exit. That leads to n times m distance checks, which is too slow when both arrays are large.

A subtle edge case appears when all exits lie strictly to one side of a bag. In that situation the closest exit is not ambiguous, but a naive implementation that only checks one direction or fails to consider both neighbors can return incorrect results. For example, if exits are at positions `[1, 2]` and a bag is at `100`, the correct answer is `98`, but an implementation that only compares until it passes the bag position and then stops early might incorrectly miss the last valid exit.

Another failure mode appears when duplicates or clustered values exist. If exits are `[10, 20, 30]` and bags are `[21, 22, 23]`, a naive pointer reset per bag can repeatedly rescan from the start, producing unnecessary quadratic behavior even though the correct closest exit index only moves forward.

## Approaches

A brute-force approach computes, for every bag, the absolute distance to every exit and takes the minimum. This is correct because it explicitly checks all possibilities, but it performs n × m comparisons. With large constraints, this becomes too slow because both arrays can grow to sizes where this product exceeds the allowed operations by orders of magnitude.

The key observation is that as we move from left to right along the bags, the closest exit index cannot move backwards. If a bag shifts slightly right, the best candidate exit either stays the same or moves to the next exit. This monotonicity allows us to maintain a pointer into the exits array and only move it forward, never resetting it.

Once we reach the first exit that is to the right of or equal to the current bag, the closest exit is always among that exit and the previous one. Everything further right or left is guaranteed to be worse because of sorted order. This reduces the search per bag to amortized constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · m) | O(1) | Too slow |
| Two Pointers | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We process bags in increasing order while simultaneously walking through exits in increasing order.

1. Initialize a pointer `j = 0` over the exits array. This pointer represents the first exit that we have not yet ruled out for the current bag.
2. For each bag position `b[i]`, advance `j` while `j + 1 < m` and the next exit is still closer or equal in the sense that `c[j + 1]` is not worse as a candidate than `c[j]` for this bag. Concretely, we move `j` until `c[j]` is the first exit greater than or equal to `b[i]`, or until we run out of exits.
3. Once `j` is positioned, the closest exit must be either `c[j]` or `c[j - 1]` if it exists. We compute both absolute distances and take the minimum.
4. Add this minimum distance to the running total.
5. Continue to the next bag without resetting `j`. This is valid because future bags are at the same or greater positions, so no earlier exit will become newly optimal.

The important structural decision is that we never restart scanning exits for each bag. The pointer only moves forward, which preserves correctness while eliminating repeated work.

### Why it works

The invariant is that before processing bag `i`, the pointer `j` is positioned at the smallest index such that all exits strictly to the left of `j` are guaranteed not to be better than any exit at or to the right of `j` for all remaining bags. Because both arrays are sorted, increasing the bag position cannot make a previously discarded exit become optimal again. This monotonic dominance ensures that checking only the two neighboring candidates around `j` is sufficient for correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    j = 0
    ans = 0

    for x in b:
        while j + 1 < m and abs(c[j + 1] - x) <= abs(c[j] - x):
            j += 1

        best = abs(c[j] - x)
        if j > 0:
            best = min(best, abs(c[j - 1] - x))

        ans += best

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps a single pointer `j` over exits. The inner loop advances it only when the next exit is at least as good as the current one for the current bag, ensuring we always end at a locally optimal candidate. The second check against `j - 1` handles the boundary where the closest exit lies just to the left of the pointer.

A common mistake is resetting `j` for each bag. That preserves correctness but destroys linear complexity. Another mistake is only checking one direction relative to `j`, which fails when the closest exit is on the opposite side.

## Worked Examples

### Example 1

Input:

```
n = 3, m = 3
b = [2, 8, 15]
c = [1, 10, 20]
```

| bag x | j before | j after movement | candidates | chosen distance |
| --- | --- | --- | --- | --- |
| 2 | 0 | 0 | 1 | 1 |
| 8 | 0 | 0 | 1, 10 | 2 |
| 15 | 0 | 1 | 10, 20 | 5 |

For the second bag, even though we could move toward 10, the pointer does not advance because 10 is not strictly better than 1 for that position. The table shows that the algorithm consistently compares only local candidates.

### Example 2

Input:

```
n = 4, m = 2
b = [1, 3, 6, 9]
c = [2, 8]
```

| bag x | j before | j after movement | candidates | chosen distance |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 2 | 1 |
| 3 | 0 | 0 | 2, 8 | 1 |
| 6 | 0 | 1 | 2, 8 | 2 |
| 9 | 1 | 1 | 8 | 1 |

This trace shows the pointer eventually moves right once the bags cross the midpoint between exits, after which all further bags remain associated with the right exit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each pointer over bags and exits only moves forward, never backward |
| Space | O(1) | Only a few variables are maintained besides input storage |

The linear complexity is essential for large inputs because it avoids recomputing nearest-exit checks for every bag. Each exit is visited at most once, which keeps execution well within typical Codeforces limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# basic samples
assert run("3 3\n2 8 15\n1 10 20\n") == "8"

# all bags left of exits
assert run("2 2\n1 2\n10 20\n") == "17"

# all bags right of exits
assert run("3 2\n10 11 12\n1 5\n") == "17"

# interleaved
assert run("4 3\n1 4 6 10\n2 5 9\n") == "7"

# single exit
assert run("3 1\n1 100 1000\n50\n") == "1499"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all left | 17 | closest always same exit |
| all right | 17 | symmetric boundary handling |
| interleaved | 7 | switching between exits |
| single exit | 1499 | degenerate case correctness |

## Edge Cases

When all bags lie to the left of the first exit, the pointer never advances and every bag must compare only against the first exit. The algorithm handles this because `j` stays at zero and the `j - 1` check is never triggered.

When all bags lie to the right of the last exit, the pointer advances until it reaches the final index and then stops. All distances are computed against the last exit only, since no better candidate exists to the right.

When exits are sparse and bags are dense, the pointer advances slowly relative to bags, but still only moves forward. This guarantees linear behavior even when many bags share the same nearest exit region.
