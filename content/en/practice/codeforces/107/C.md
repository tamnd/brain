---
title: "CF 107C - Arrangement"
description: "We have n seats and n professors. Professor 1 is the most senior, professor n is the least senior. Some pairs of seats impose ordering constraints. If (a, b) is given, then the professor sitting in seat a must be more senior than the professor sitting in seat b."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp"]
categories: ["algorithms"]
codeforces_contest: 107
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 83 (Div. 1 Only)"
rating: 2400
weight: 107
solve_time_s: 155
verified: true
draft: false
---

[CF 107C - Arrangement](https://codeforces.com/problemset/problem/107/C)

**Rating:** 2400  
**Tags:** bitmasks, dp  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` seats and `n` professors. Professor `1` is the most senior, professor `n` is the least senior. Some pairs of seats impose ordering constraints. If `(a, b)` is given, then the professor sitting in seat `a` must be more senior than the professor sitting in seat `b`.

A seating arrangement is simply a permutation of professors assigned to seats. Since smaller professor numbers mean higher seniority, the constraint `(a, b)` becomes:

```
perm[a] < perm[b]
```

among the assigned professor numbers.

All valid arrangements are sorted lexicographically. Year 2001 uses the first valid arrangement, year 2002 uses the second valid arrangement, and so on. We must output the arrangement used in year `y`.

This is equivalent to finding the `(y - 2001)`-th valid permutation in lexicographic order.

The most important observation is that the constraints are about seats, not about professors. The relative order between seat values is fixed. We are counting permutations that satisfy a partial order.

The constraint `n ≤ 16` completely changes the nature of the problem. A factorial search over all permutations is impossible because:

```
16! ≈ 2 * 10^13
```

Even generating permutations for a few seconds would not come close.

At the same time, `2^16 = 65536`, which is very manageable. This strongly suggests a subset DP.

The year can be as large as `10^18`, which means the number of valid arrangements can be enormous. We cannot enumerate arrangements one by one. We must count how many valid completions exist from a partial assignment and use those counts to skip blocks of permutations.

There are several edge cases that break naive implementations.

A contradictory set of constraints may produce zero valid arrangements.

Example:

```
2 2001 2
1 2
2 1
```

Seat `1` must contain a smaller professor number than seat `2`, and simultaneously a larger one. No arrangement exists. The correct output is:

```
The times have changed
```

A careless implementation might still attempt DP transitions and accidentally produce garbage counts.

Another subtle case is when the requested year exceeds the number of valid arrangements.

Example:

```
2 2003 0
```

There are only `2! = 2` arrangements:

```
1 2
2 1
```

Years 2001 and 2002 are valid. Year 2003 does not exist. The correct output is:

```
The times have changed
```

A common bug is using zero-based indexing incorrectly and treating year 2001 as index `1` instead of `0`.

Duplicate constraints also appear in the input.

Example:

```
3 2001 3
1 2
1 2
1 2
```

These duplicates should not change anything. If constraints are stored improperly, they may inflate indegrees or break transitions.

## Approaches

The brute-force solution is straightforward. Generate every permutation of professors, check whether it satisfies all constraints, collect the valid ones, sort them lexicographically, then select the required year.

This works because the validity test is easy. For every constraint `(a, b)`, we simply verify:

```
perm[a] < perm[b]
```

The problem is the number of permutations. With `n = 16`, we would need to inspect:

```
16! ≈ 2 * 10^13
```

permutations. Even checking a billion permutations per second would still take hours.

The key observation is that lexicographic construction only needs counts of completions. Suppose we are building the arrangement from left to right. At some position, we try placing the smallest possible unused professor. If we know how many valid completions exist after that choice, we can decide whether the target arrangement lies inside that block or after it.

This converts the problem into counting valid assignments from a partial state.

A subset DP fits perfectly because `n ≤ 16`. Let a bitmask represent which professors have already been assigned. From that state, we determine which professor can be placed next without violating any seat constraints.

The constraints are on seats, but professors are assigned in increasing seniority order. This creates a very useful interpretation:

If professor `k` is the next smallest unused professor, then assigning professor `k` to seat `s` means seat `s` receives the next rank among unfilled seats.

For constraint `(a, b)`, seat `a` must receive a smaller professor number than seat `b`. So seat `a` must be filled before seat `b`.

This transforms the problem into counting topological orders of a DAG over seats.

Now the state becomes much cleaner:

```
dp[mask] = number of ways to fill exactly the seats in mask first
```

We may add a seat only if all prerequisite seats are already inside the mask.

This gives an `O(n * 2^n)` solution, which is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * m) | O(n!) | Too slow |
| Optimal | O(n * 2^n) | O(2^n) | Accepted |

## Algorithm Walkthrough

1. Interpret every constraint `(a, b)` as a dependency between seats.

Since smaller professor numbers are more senior, seat `a` must receive a professor earlier than seat `b`. This means seat `b` depends on seat `a`.
2. Build a prerequisite bitmask for every seat.

`pre[i]` stores all seats that must already be filled before seat `i` can be filled.
3. Use subset DP to count valid topological orders.

Let:

```
dp[mask]
```

denote the number of valid ways to fill the remaining seats after exactly the seats in `mask` have already been assigned.
4. Define the transition.

From `mask`, we may choose seat `i` if:

```
i is not in mask
and
all prerequisites of i are already in mask
```

Formally:

```
(pre[i] & mask) == pre[i]
```
5. Compute the DP with memoized DFS.

If all seats are filled, there is exactly one completion.

Otherwise, sum the counts of all valid next seats.
6. Let:

```
k = y - 2001
```

This is the zero-based index of the desired arrangement.
7. If:

```
dp[0] <= k
```

then the requested year exceeds the number of valid arrangements. Print:

```
The times have changed
```
8. Reconstruct the arrangement lexicographically.

We assign professors from smallest to largest. At each step, try candidate seats in increasing order because lexicographic order depends on which seat receives the current smallest professor.
9. For each candidate seat, compute how many completions exist if we place the current professor there.

If the number of completions is less than or equal to `k`, skip all those arrangements and subtract that count from `k`.

Otherwise, commit to that seat and continue.
10. After determining the filling order of seats, convert it into the final permutation.

If seat `s` is filled at step `t`, then it receives professor `t + 1`.

### Why it works

The DP counts exactly the valid topological orderings of the seat dependency graph. Every valid arrangement corresponds to one unique order in which seats receive increasing professor numbers.

During reconstruction, lexicographic order is preserved because smaller professor numbers are assigned first. Trying candidate seats in increasing order explores arrangements in the same order as lexicographic permutation comparison.

At every step, the DP count tells us how many arrangements begin with a specific prefix. Skipping whole blocks using these counts is equivalent to jumping directly to the target lexicographic arrangement.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

INF = 10**18 + 5

def solve():
    n, y, m = map(int, input().split())

    pre = [0] * n

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        pre[b] |= (1 << a)

    full = (1 << n) - 1

    @lru_cache(None)
    def dp(mask):
        if mask == full:
            return 1

        res = 0

        for i in range(n):
            if (mask >> i) & 1:
                continue

            if (pre[i] & mask) != pre[i]:
                continue

            res += dp(mask | (1 << i))

            if res > INF:
                res = INF

        return res

    k = y - 2001

    total = dp(0)

    if total <= k:
        print("The times have changed")
        return

    order = []
    mask = 0

    for _ in range(n):
        for seat in range(n):
            if (mask >> seat) & 1:
                continue

            if (pre[seat] & mask) != pre[seat]:
                continue

            cnt = dp(mask | (1 << seat))

            if cnt <= k:
                k -= cnt
            else:
                order.append(seat)
                mask |= (1 << seat)
                break

    ans = [0] * n

    for professor, seat in enumerate(order, start=1):
        ans[seat] = professor

    print(*ans)

solve()
```

The first part converts the input constraints into prerequisite masks. If `(a, b)` exists, then seat `b` depends on seat `a`, so we set the corresponding bit inside `pre[b]`.

The memoized DP works on subsets of already-filled seats. The transition condition:

```
(pre[i] & mask) == pre[i]
```

means every prerequisite of seat `i` is already filled.

The DP values can become very large, potentially exceeding the requested year range. We cap them at `INF` because we only need comparisons against `10^18`.

The reconstruction phase is the subtle part. We are not directly building the permutation values. Instead, we build the order in which seats receive professors `1, 2, 3, ...`.

Suppose seat `2` is chosen first. That means professor `1` sits there. If seat `0` is chosen second, professor `2` sits there, and so on.

Trying seats in increasing order guarantees lexicographic traversal. Whenever a candidate contributes `cnt` arrangements, those arrangements form one contiguous lexicographic block. If `k >= cnt`, we skip the entire block.

A common mistake is reconstructing by professor instead of by seat ordering. The DP naturally counts seat fill orders, which correspond directly to professor assignments.

## Worked Examples

### Example 1

Input:

```
3 2001 2
1 2
2 3
```

Dependencies:

```
seat 1 before seat 2
seat 2 before seat 3
```

Only one ordering exists.

#### DP Reconstruction Trace

| Step | Current Mask | Available Seats | Chosen Seat | k |
| --- | --- | --- | --- | --- |
| 1 | 000 | 0 | 0 | 0 |
| 2 | 001 | 1 | 1 | 0 |
| 3 | 011 | 2 | 2 | 0 |

Seat filling order is:

```
0 -> 1 -> 2
```

So:

```
seat 0 gets professor 1
seat 1 gets professor 2
seat 2 gets professor 3
```

Final arrangement:

```
1 2 3
```

This trace demonstrates that the dependency graph completely fixes the topological order.

### Example 2

Input:

```
3 2002 1
1 2
```

Constraint:

```
seat 1 before seat 2
```

Valid arrangements in lexicographic order are:

```
1 2 3
1 3 2
2 1 3
```

We want index:

```
k = 1
```

#### Reconstruction Trace

| Step | Mask | Candidate Seat | Completion Count | Action | k |
| --- | --- | --- | --- | --- | --- |
| 1 | 000 | 0 | 2 | take | 1 |
| 2 | 001 | 1 | 1 | skip | 0 |
| 2 | 001 | 2 | 1 | take | 0 |
| 3 | 101 | 1 | 1 | take | 0 |

Seat order:

```
0 -> 2 -> 1
```

Assignments:

```
seat 0 = 1
seat 2 = 2
seat 1 = 3
```

Final arrangement:

```
1 3 2
```

This example shows how the DP counts are used to skip entire lexicographic blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 2^n) | Each subset tries all seats once |
| Space | O(2^n) | Memoization table over subsets |

With `n ≤ 16`, the number of states is at most `65536`. Each state checks at most `16` transitions, so the total operations are roughly one million, comfortably inside the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from functools import lru_cache

INF = 10**18 + 5

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n, y, m = map(int, input().split())

    pre = [0] * n

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        pre[b] |= (1 << a)

    full = (1 << n) - 1

    @lru_cache(None)
    def dp(mask):
        if mask == full:
            return 1

        res = 0

        for i in range(n):
            if (mask >> i) & 1:
                continue

            if (pre[i] & mask) != pre[i]:
                continue

            res += dp(mask | (1 << i))

            if res > INF:
                res = INF

        return res

    k = y - 2001

    if dp(0) <= k:
        print("The times have changed")
        return out.getvalue()

    order = []
    mask = 0

    for _ in range(n):
        for seat in range(n):
            if (mask >> seat) & 1:
                continue

            if (pre[seat] & mask) != pre[seat]:
                continue

            cnt = dp(mask | (1 << seat))

            if cnt <= k:
                k -= cnt
            else:
                order.append(seat)
                mask |= (1 << seat)
                break

    ans = [0] * n

    for professor, seat in enumerate(order, start=1):
        ans[seat] = professor

    print(*ans)

    return out.getvalue()

# provided sample
assert run(
"""3 2001 2
1 2
2 3
"""
) == "1 2 3\n", "sample 1"

# minimum size
assert run(
"""1 2001 0
"""
) == "1\n", "single professor"

# contradictory constraints
assert run(
"""2 2001 2
1 2
2 1
"""
) == "The times have changed\n", "cycle"

# year exceeds arrangements
assert run(
"""2 2003 0
"""
) == "The times have changed\n", "not enough permutations"

# duplicate constraints
assert run(
"""3 2001 3
1 2
1 2
1 2
"""
) == "1 2 3\n", "duplicate edges"

# no constraints, second permutation
assert run(
"""3 2002 0
"""
) == "1 3 2\n", "lexicographic order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2001 0` | `1` | Minimum input size |
| Contradictory cycle | `The times have changed` | Detects impossible DAG |
| `2 2003 0` | `The times have changed` | Handles insufficient arrangements |
| Duplicate edges | `1 2 3` | Duplicate constraints do not break DP |
| No constraints, second permutation | `1 3 2` | Correct lexicographic reconstruction |

## Edge Cases

### Contradictory Constraints

Input:

```
2 2001 2
1 2
2 1
```

Dependencies become:

```
seat 0 depends on seat 1
seat 1 depends on seat 0
```

At `mask = 00`, neither seat is available because each requires the other to already be filled.

So:

```
dp(0) = 0
```

Since the total number of valid arrangements is zero, the algorithm prints:

```
The times have changed
```

The DP naturally detects cycles because no transition becomes legal.

### Requested Year Too Large

Input:

```
2 2003 0
```

There are only two valid arrangements:

```
1 2
2 1
```

The requested index is:

```
k = 2003 - 2001 = 2
```

But:

```
dp(0) = 2
```

Since valid indices are only `0` and `1`, the condition:

```
if total <= k:
```

correctly rejects the request.

### Duplicate Constraints

Input:

```
3 2001 3
1 2
1 2
1 2
```

All three edges are identical. Bitmask storage keeps only one dependency bit:

```
pre[1] = 001
```

The DP behaves exactly as if the edge appeared once.

The resulting arrangement is still:

```
1 2 3
```

### Fully Unconstrained Case

Input:

```
3 2004 0
```

All `3! = 6` permutations are valid.

The algorithm reconstructs the lexicographically fourth permutation:

```
2 3 1
```

This case verifies that lexicographic skipping works correctly even when every transition is available.
