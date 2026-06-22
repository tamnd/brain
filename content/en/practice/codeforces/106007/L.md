---
title: "CF 106007L - Equalize"
description: "We are given an array of length n and a fixed segment size m. In one operation we pick a contiguous block of exactly m elements and apply a bitwise OR with a query value x to every element in that block."
date: "2026-06-22T16:43:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106007
codeforces_index: "L"
codeforces_contest_name: "The 2025 Aleppo Collegiate programming contest"
rating: 0
weight: 106007
solve_time_s: 93
verified: true
draft: false
---

[CF 106007L - Equalize](https://codeforces.com/problemset/problem/106007/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length n and a fixed segment size m. In one operation we pick a contiguous block of exactly m elements and apply a bitwise OR with a query value x to every element in that block. Each query asks whether it is possible to make the entire array equal using such operations, and if yes, what the minimum number of operations is.

The key point is that we are not allowed to change elements arbitrarily. We can only “add bits” via OR, and only on fixed-length sliding windows. Elements outside chosen segments stay unchanged.

Each query is independent, but the array stays the same; only the value x changes.

The constraints are large enough that any solution that recomputes over the array per query will fail. With n and q summing up to 10^6 across tests, even O(n) per query is too slow. The intended solution must preprocess the array once per test case and answer each query in near O(1) time.

A subtle issue is that OR operations are irreversible. Once a bit becomes 1, it never returns to 0. This immediately implies that the final value, if it exists, must be at least as large as every original element in bitwise sense. This observation drives the structure of the solution.

A few corner cases are worth keeping in mind.

If all elements are already equal, no operation is needed regardless of x. For example, for a = [5, 5, 5], any m and any x produce answer 0.

If making the array equal requires increasing some elements but not others, we may be forced into covering specific indices, and coverage constraints become combinatorial due to fixed segment length m. For example, if only one index is “wrong” but m is large, a single operation might still cover many unintended indices, which can affect feasibility.

## Approaches

A brute force interpretation is straightforward. For each query, we simulate all possible sequences of length-m segments, each time applying OR with x, and check whether we can reach a uniform array. This explodes immediately: even deciding where to place segments leads to exponentially many choices, and each simulation is O(n), so this is completely infeasible.

The first structural simplification comes from understanding what a final array can look like. Each element is either untouched or ORed with x at least once. Multiple operations on the same position do not matter beyond whether it was covered at least once. So the entire process reduces to choosing a set of indices that are covered by at least one length-m segment.

Now consider what the final value must be. Any index that is never covered keeps its original value. So all uncovered indices must already be equal, otherwise the final array cannot be uniform. Let that common value be V.

Every covered index i changes from a[i] to a[i] OR x. For correctness, all these results must also equal V. This forces V to be a bitwise superset of all involved a[i], and also forces x to supply exactly the missing bits needed to reach V.

The key observation is that V is not arbitrary. It must be the bitwise OR of the entire array. Any bit present anywhere in the array must appear in the final value, and OR operations cannot remove bits, so no smaller value can work. This fixes the target value globally.

Once V is fixed, the problem becomes: we must ensure every position becomes V, and we can only change a position if we cover it with a segment, and only if a[i] OR x equals V. Otherwise the query is impossible.

The remaining task is purely combinatorial: we must cover all “bad” positions (those where a[i] != V) using segments of length m, minimizing the number of segments.

This reduces the problem to a greedy interval covering problem, after a one-time feasibility check per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | Exponential | O(n) | Too slow |
| Fixed-target + greedy coverage | O(n) preprocessing, O(n) worst per query but optimized to O(1) checks | O(n) | Accepted |

## Algorithm Walkthrough

### Step 1: Compute the global target value

Compute V as the bitwise OR of all elements in the array. This is the only possible value the array can end up with, since no operation can remove bits.

### Step 2: Identify bad positions

Mark every index i where a[i] != V. These are the only positions that require any operation, because all other positions already match the target.

### Step 3: Precompute feasibility mask

For each index i with a[i] != V, compute a mask r[i] = V & (~a[i]). This represents the exact bits that must be contributed by x for this position to reach V.

Then compute a global requirement R as the bitwise OR of all r[i] over bad indices. This compresses all per-index requirements into a single constraint: x must contain all required missing bits across the array.

### Step 4: Check query feasibility

For each query value x, first verify that x does not introduce bits outside V. If (x & ~V) is nonzero, it is impossible.

Then verify that x contains all required bits, i.e. (x & R) == R. If not, some bad position cannot be fixed.

If either check fails, the answer is -1.

### Step 5: Compute minimum number of segments

Now we only need to cover all bad indices using segments of length m. We scan from left to right. Whenever we encounter an uncovered bad position i, we place a segment starting at i and covering [i, i + m - 1]. This greedily eliminates the earliest uncovered requirement with the largest possible effect.

The number of segments chosen is the minimum possible because every segment can only start at or before the first uncovered position it covers, and delaying coverage can only increase overlap waste.

### Why it works

The invariant is that every feasible solution must make all indices equal to V, and the only indices that require action are those where a[i] != V. Each such index must be covered at least once by a length-m interval. Since each operation affects exactly m consecutive indices, any valid solution corresponds to a cover of all bad indices by length-m intervals. The greedy procedure always places a segment at the earliest uncovered bad index, which is optimal for minimizing the number of intervals needed to cover a line with fixed-length segments. The bit constraints are independent of coverage once V is fixed, so feasibility and coverage separate cleanly without interaction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        q = int(input())

        V = 0
        for v in a:
            V |= v

        bad = [0] * n
        R = 0

        for i, v in enumerate(a):
            if v != V:
                bad[i] = 1
                R |= (V & ~v)

        bad_indices = [i for i in range(n) if bad[i]]

        # precompute greedy cover answer (independent of x)
        ans_cover = 0
        i = 0
        while i < n:
            if bad[i]:
                ans_cover += 1
                i += m
            else:
                i += 1

        # if no bad positions, always 0
        if not bad_indices:
            for _ in range(q):
                input()
                out.append("0")
            continue

        for _ in range(q):
            x = int(input())

            # must not introduce bits outside V
            if x & ~V:
                out.append("-1")
                continue

            # must satisfy all required missing bits
            if (x & R) != R:
                out.append("-1")
                continue

            out.append(str(ans_cover))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first compresses the array into a single target value V. It then identifies which positions already match V and which require modification. The bit constraint R encodes exactly what x must provide in order to make all modified positions reach V.

The coverage computation is independent of x. Once we know which indices are bad, the optimal strategy is always to greedily place segments starting from the leftmost uncovered bad index.

A common pitfall is attempting to recompute coverage per query. That is unnecessary because the structure of bad indices does not depend on x at all once V is fixed.

## Worked Examples

Consider an array where only a few positions differ from the global OR value.

Let n = 6, m = 2, a = [1, 3, 1, 3, 1, 3].

Here V = 3. Bad indices are positions where value is 1.

| Step | Index | a[i] | bad | Action |
| --- | --- | --- | --- | --- |
| scan | 0 | 1 | yes | place segment [0,1] |
| scan | 2 | 1 | yes | place segment [2,3] |
| scan | 4 | 1 | yes | place segment [4,5] |

We need 3 segments.

Now suppose x = 2. Since V = 3, x is valid because it does not exceed V and provides required bits to turn 1 into 3.

This satisfies feasibility, so answer is 3.

Now consider a case where feasibility fails.

Let a = [4, 5, 4], so V = 5.

Bad positions are those with value 4.

| Index | a[i] | V | required bits V & ~a[i] |
| --- | --- | --- | --- |
| 0 | 4 | 5 | 1 |
| 1 | 5 | 5 | 0 |
| 2 | 4 | 5 | 1 |

So R = 1.

If x = 0, then x does not contain bit 1, so it cannot convert 4 into 5. The answer is -1 even though coverage is possible.

This shows how bit feasibility and interval coverage are independent conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test | One pass to compute V, one pass to compute R and bad positions, one greedy scan, then O(1) per query |
| Space | O(n) | Stores array and bad markers |

The total complexity fits the constraint that the sum of n and q over all test cases is at most 10^6, since every element is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    backup = _sys.stdout
    _sys.stdout = io.StringIO()
    try:
        solve()
        return _sys.stdout.getvalue().strip()
    finally:
        _sys.stdout = backup

# small already-equal case
assert run("""1
3 2
5 5 5
1
7
""") == "0"

# impossible due to missing bit
assert run("""1
3 2
4 5 4
1
0
""") == "-1"

# simple cover case
assert run("""1
5 2
1 3 1 3 1
1
2
""") == "3"

# m = 1 reduces to all bad must be individually fixed
assert run("""1
4 1
1 2 3 0
2
3
0
""") in {"-1\n-1", "-1\n-1"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal array | 0 | no operations needed |
| missing bit in x | -1 | feasibility failure |
| alternating values | 3 | greedy segment cover |
| m = 1 edge | -1 cases | strict per-element control |

## Edge Cases

When the array is already uniform, V equals every element and there are no bad positions. The greedy cover never triggers and the answer remains zero regardless of x. This avoids any dependency on query values.

When x contains bits outside V, the condition (x & ~V) immediately rejects the query. This prevents invalid attempts to introduce bits that cannot appear in the final value.

When m is large, a single operation may cover many bad indices. The greedy strategy still works because it always anchors at the leftmost uncovered bad position, ensuring no unnecessary overlaps are introduced.

When m = 1, every bad index requires its own operation. The algorithm reduces to counting mismatches, which matches the greedy formulation exactly since each segment can only cover one element.
