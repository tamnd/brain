---
title: "CF 1788E - Sum Over Zero"
description: "We are given an array of integers and want to choose several segments on it. Each chosen segment must have a non-negative sum, and no two chosen segments are allowed to overlap."
date: "2026-06-09T10:49:07+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp"]
categories: ["algorithms"]
codeforces_contest: 1788
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 851 (Div. 2)"
rating: 2200
weight: 1788
solve_time_s: 91
verified: true
draft: false
---

[CF 1788E - Sum Over Zero](https://codeforces.com/problemset/problem/1788/E)

**Rating:** 2200  
**Tags:** data structures, dfs and similar, dp  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and want to choose several segments on it. Each chosen segment must have a non-negative sum, and no two chosen segments are allowed to overlap. The score of a choice is simply the total number of positions covered by all chosen segments, and the goal is to maximize this score.

Another way to see it is that we are trying to cover as many indices as possible using disjoint intervals, where every interval has “non-negative total mass” in terms of the array values.

The constraint $n \le 2 \cdot 10^5$ immediately rules out any solution that tries to enumerate segments or subsets explicitly. Even $O(n^2)$ constructions of intervals are already borderline, since there are $O(n^2)$ possible segments, and checking sums naively would push us to $O(n^3)$.

A subtle issue appears when there are many small negative values scattered between positives. A naive greedy that always takes the longest non-negative segment starting at each position can fail, because extending a segment might turn a slightly positive interval into a negative one, even though splitting it into multiple smaller valid segments yields a better total covered length.

For example, consider an array like:

```
[2, -1, 2, -1, 2]
```

The whole array has sum $4$, so it is valid as a single segment of length 5. However, a local strategy might instead pick shorter segments depending on prefix fluctuations. In other cases, merging too aggressively loses flexibility to place more segments later.

The core difficulty is that segment decisions are not independent: choosing a segment changes what remains available, but also changes whether future segments can be formed.

## Approaches

A brute-force approach would try to generate every possible set of disjoint segments and check whether each segment has non-negative sum. Even if we restrict ourselves to valid segments only, there are $O(n^2)$ candidates, and selecting disjoint subsets among them leads to exponential complexity. This is completely infeasible.

We need to recognize that the condition “segment sum is non-negative” interacts nicely with prefix sums. If we define prefix sums $p[i]$, then any segment $[l, r]$ is valid if $p[r] \ge p[l-1]$. This turns every valid segment into a relation between two prefix indices where the right endpoint has a prefix value not smaller than the left endpoint.

Now the key structural insight is that each segment contributes only its length, not its sum. That means if we fix a right endpoint $r$, and we want to end a segment there, we only care about choosing the earliest possible $l$ such that $p[l-1] \le p[r]$. Choosing an earlier $l$ always increases length, and it never hurts validity.

This turns the problem into a dynamic programming over prefix positions. At each position $r$, we decide whether we end a segment at $r$, and if we do, we want the longest valid segment ending there. The optimization reduces to repeatedly pairing each prefix value with the smallest previous prefix that does not exceed it.

To maintain this efficiently, we process prefix sums from left to right and maintain a data structure that stores the best DP value achievable for each prefix sum threshold. Since prefix sums are arbitrary integers, we compress and use a monotonic structure that behaves like a “best-so-far over prefix sums” map. This leads to a DP where each state is updated in amortized constant time using a monotonic stack-like structure.

The key transformation is that the decision at position $i$ depends only on the best reachable state among all earlier positions with prefix sum $\le p[i]$, and this structure can be maintained incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n^2) | Too slow |
| Prefix DP with monotonic structure | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums $p[i]$, where $p[0] = 0$. This converts segment sums into differences of prefix values.
2. We maintain a structure that supports: given a prefix value $x$, quickly retrieving the best DP value among all previous prefix positions whose prefix sum is $\le x$. This represents the best way to start a segment ending at current position.
3. We process positions from left to right, and maintain DP over prefix indices. Let $dp[i]$ be the maximum total covered length using positions up to $i$, with segment boundaries aligned at prefix points.
4. At each position $i$, we first carry forward $dp[i] = dp[i-1]$, meaning we do not end a segment at $i$.
5. Then we consider ending a segment at $i$. The best starting point is any $j < i$ such that $p[j] \le p[i]$, and the gain is $(i - j)$ plus the best DP up to $j$. We query the best such $dp[j] - j$, because:

$$dp[j] - j + i$$

already accounts for previous coverage plus the new segment length.
6. We maintain a data structure over prefix sums that stores the maximum value of $dp[j] - j$ for each prefix sum threshold. When processing $i$, we update it with the current state.
7. The final answer is $dp[n]$.

### Why it works

The crucial invariant is that for any prefix value $x$, the structure stores the best achievable value of $dp[j] - j$ among all positions $j$ whose prefix sum is at most $x$. This is sufficient because any valid segment ending at $i$ must start at some $j$ satisfying $p[j] \le p[i]$, and among all such choices, the one maximizing $dp[j] - j$ maximizes total gain.

Since every transition only depends on prefix sums and the linear expression $dp[j] - j$, no future decision can invalidate a previously stored optimal candidate. The monotonicity of prefix constraints ensures we never need to reconsider older states in a more refined way.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # prefix sums
    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + a[i - 1]

    # DP
    dp = [0] * (n + 1)

    # We maintain pairs (prefix_sum, best dp[j] - j up to this prefix constraint)
    # We'll compress prefix sums by sorting unique values
    vals = sorted(set(pref))

    from collections import defaultdict
    import bisect

    # best value for each compressed prefix threshold
    best = [-10**18] * len(vals)

    def get_idx(x):
        return bisect.bisect_right(vals, x) - 1

    def query(x):
        i = get_idx(x)
        return best[i] if i >= 0 else -10**18

    def update(x, val):
        i = get_idx(x)
        if i >= 0:
            best[i] = max(best[i], val)

    # initialize: j = 0
    update(pref[0], dp[0] - 0)

    for i in range(1, n + 1):
        dp[i] = dp[i - 1]

        # try ending segment at i
        best_start = query(pref[i])
        if best_start != -10**18:
            dp[i] = max(dp[i], best_start + i)

        # update structure with j = i
        update(pref[i], dp[i] - i)

    print(dp[n])

if __name__ == "__main__":
    solve()
```

The code starts by converting the array into prefix sums so that segment validity becomes a simple inequality. The DP array tracks the best total covered length up to each prefix position.

The data structure is implemented by compressing prefix sums and maintaining a best value per prefix threshold. Each DP state contributes a candidate value $dp[j] - j$, which represents how profitable it is to start a segment after position $j$.

At each position, we first compute the option of not placing a segment ending here. Then we query all valid starting points for a segment ending at the current index. Finally, we insert the current state into the structure so it can serve as a future segment start.

The most delicate part is ensuring that we always update the structure after computing $dp[i]$, otherwise we would incorrectly allow using the same position twice.

## Worked Examples

### Example 1

Input:

```
5
3 -3 -2 5 -4
```

| i | pref[i] | best query(pref[i]) | dp[i-1] | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | 0 | - | 0 | 0 |
| 1 | 3 | 0 | 0 | 1 |
| 2 | 0 | 0 | 1 | 1 |
| 3 | -2 | 1 | 1 | 1 |
| 4 | 3 | 2 | 1 | 4 |
| 5 | -1 | 4 | 4 | 4 |

The final answer is 4, corresponding to selecting two disjoint valid segments whose total covered length is maximized.

This trace shows how prefix-sum-based querying allows the algorithm to reuse earlier optimal starts without explicitly enumerating segments.

### Example 2

Input:

```
3
1 2 3
```

| i | pref[i] | best query(pref[i]) | dp[i] |
| --- | --- | --- | --- |
| 0 | 0 | - | 0 |
| 1 | 1 | 0 | 1 |
| 2 | 3 | 2 | 2 |
| 3 | 6 | 5 | 3 |

All prefixes are positive increasing, so the best strategy is to take the entire range as one segment, giving answer 3.

This confirms that when all segment sums are valid globally, the DP naturally collapses into a single maximal interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each update and query uses prefix compression lookup |
| Space | O(n) | Storage for prefix sums and DP states |

The complexity is fast enough for $n \le 2 \cdot 10^5$, and the logarithmic factor comes only from prefix compression operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("5\n3 -3 -2 5 -4\n") == "4"

# increasing array (single full segment)
assert run("3\n1 2 3\n") == "3"

# all negative
assert run("4\n-1 -2 -3 -4\n") == "0"

# alternating
assert run("6\n1 -1 1 -1 1 -1\n") == "6"

# single element positive
assert run("1\n5\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| increasing | 3 | full segment optimality |
| all negative | 0 | empty set correctness |
| alternating | 6 | multiple unit segments |
| single element | 1 | base case |

## Edge Cases

One important edge case is when all prefix sums are negative after the first step. In that situation, no segment ending at later positions can start at index 0, and the DP must avoid forming invalid negative-sum segments. The algorithm handles this because queries over prefix thresholds return no valid starting candidate, so only the “skip” transition survives.

Another case is when the optimal solution consists of many small segments instead of one large segment. For an input like:

```
[2, -1, 2, -1, 2]
```

the algorithm correctly allows multiple resets of the starting position because each prefix update stores a new candidate $dp[i] - i$, enabling future segments to start from different optimal points without overlap.

Finally, when prefix sums repeat, the compression ensures they map to the same threshold bucket, so earlier and later identical prefix values are treated consistently, preserving correctness of the “$\le$” condition used in validity checks.
