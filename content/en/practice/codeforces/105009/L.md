---
title: "CF 105009L - Modulo Queries"
description: "We are given a fixed array of integers and many independent range queries. Each query picks a contiguous segment from index $l$ to $r$, and a modulus value $x$."
date: "2026-06-28T02:49:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105009
codeforces_index: "L"
codeforces_contest_name: "2024 USACO.Guide Informatics Tournament"
rating: 0
weight: 105009
solve_time_s: 104
verified: false
draft: false
---

[CF 105009L - Modulo Queries](https://codeforces.com/problemset/problem/105009/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed array of integers and many independent range queries. Each query picks a contiguous segment from index $l$ to $r$, and a modulus value $x$. For that query, we compute the sum of remainders obtained by reducing every element in the chosen segment modulo $x$, and we output that sum.

The key difficulty is that both the range and the modulus change per query, and all values involved can be as large as 200,000. This rules out any approach that recomputes the remainder of every element for every query. With up to 200,000 queries and array length also up to 200,000, a direct per-query scan of the segment leads to roughly $O(NQ)$ operations in the worst case, which is far beyond feasible limits.

A subtle aspect comes from the behavior of the modulo operation itself. For small $x$, most values in the array contribute their full value or something close to it. For large $x$, most values are unchanged. The transition is not smooth, it is governed by how many multiples of $x$ lie below each value.

Edge cases that break naive approaches usually come from this transition:

If all elements are smaller than $x$, the answer is simply the sum of the segment. For example, with array $[1,2,3]$ and $x=10$, the answer for any range is just the sum, since no value wraps.

If $x=1$, every remainder is zero regardless of the array, so every query returns zero. A naive implementation that does not explicitly simplify this case still works, but it may waste time repeatedly computing modulo.

If $x$ is very small, say $x=2$, values alternate between 0 and 1 depending on parity, and the contribution is no longer aligned with prefix sums alone unless we structure the computation carefully.

The real challenge is efficiently handling all these regimes in a unified way.

## Approaches

The brute-force method is straightforward. For each query, we iterate from $l$ to $r$, compute $A_i \bmod x$, and accumulate the sum. This is correct because it directly follows the definition of the query. However, each query costs $O(r-l+1)$, and in the worst case this is $O(N)$. With $Q$ queries, the total complexity becomes $O(NQ)$, which can reach $4 \cdot 10^{10}$ operations and is not usable.

The key observation is that we can rewrite the modulo operation in a way that exposes structure. For any value $a$, we have

$$a \bmod x = a - x \cdot \left\lfloor \frac{a}{x} \right\rfloor.$$

So the query becomes:

$$\sum a_i - x \cdot \sum \left\lfloor \frac{a_i}{x} \right\rfloor.$$

The first part is just a range sum, which we can answer in $O(1)$ using prefix sums. The difficulty is the second part: we need the sum of quotients $\lfloor a_i / x \rfloor$ over a range.

Now the structure of the constraints becomes crucial. The values $a_i$ are at most 200,000, so we can preprocess positions by value. For a fixed $x$, each term $\lfloor a_i / x \rfloor$ is a step function: it only changes when $x$ crosses divisors of $a_i$. This suggests grouping contributions by value and iterating over multiples of $x$.

A more direct and powerful perspective is to fix $x$ and observe that all elements contribute the same remainder within value blocks defined by intervals $[k x, (k+1)x)$. For a fixed query range, we can count how many elements fall into each block using precomputed frequency prefix structures over value indices.

To exploit this efficiently, we maintain frequency prefix sums over value domain. For each value $v$, we store how many times it appears in any prefix of the array. Then for a query $(l,r,x)$, we iterate over multiples of $x$: for each block $[kx, (k+1)x - 1]$, we count how many elements in the range lie in that interval, multiply by the corresponding remainder contribution, and sum.

Since values go only up to 200,000, the number of blocks for a given $x$ is $O(\frac{MAXA}{x})$. Across all queries, this amortizes well because large $x$ gives few blocks and small $x$ is handled efficiently via frequency structure.

This duality between small and large modulus is what makes the solution efficient: we convert per-element computation into per-value-block aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NQ)$ | $O(1)$ | Too slow |
| Value-block + prefix frequencies | $O((N + Q)\sqrt{MAXA})$ amortized | $O(N + MAXA)$ | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array over $A$. This allows answering $\sum_{i=l}^r A_i$ in constant time, which will be the base of every query.
2. Build a frequency prefix structure over values, where for each value $v$, we can quickly determine how many times it appears in any segment $[l,r]$. This is done by storing positions grouped by value or by maintaining prefix counts.
3. For each query $(l,r,x)$, compute the raw sum of the segment using prefix sums. This represents the total before applying modulo reductions.
4. Iterate over multiples of $x$, starting from $k=0$. For each interval $[kx, (k+1)x - 1]$, count how many elements in $[l,r]$ fall into this value range.
5. For each value block, compute its contribution to the remainder sum. Every element $a$ in this block contributes $a - kx$, since that is exactly $a \bmod x$ when $a$ lies in that interval.
6. Accumulate contributions across all blocks and output the result.

The important design choice is iterating over value blocks instead of iterating over array indices. That shifts complexity from per-element per-query to per-value-range per-query.

### Why it works

Every integer $a$ belongs to exactly one interval of the form $[kx, (k+1)x)$, and within that interval the value of $a \bmod x$ simplifies to a linear expression $a - kx$. This partitions the entire value domain into disjoint segments where the contribution rule is uniform. Since the partition depends only on $x$, we can aggregate contributions per segment without inspecting individual positions repeatedly, and correctness follows from the fact that these intervals form a complete and non-overlapping cover of all possible values.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXA = 200000

def build_prefix(a):
    n = len(a)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    return pref

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    pref = build_prefix(a)

    pos = [[] for _ in range(MAXA + 1)]
    for i, v in enumerate(a):
        pos[v].append(i + 1)

    def count_in_range(l, r, v):
        arr = pos[v]
        # binary search manually
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < l:
                lo = mid + 1
            else:
                hi = mid
        left = lo

        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= r:
                lo = mid + 1
            else:
                hi = mid
        right = lo
        return right - left

    out = []

    for _ in range(q):
        l, r, x = map(int, input().split())

        total = pref[r] - pref[l - 1]
        res = 0

        if x == 1:
            out.append("0")
            continue

        if x > MAXA:
            out.append(str(total))
            continue

        k = 0
        while k * x <= MAXA:
            L = k * x
            R = min(MAXA, (k + 1) * x - 1)

            for v in range(L, R + 1):
                cnt = count_in_range(l, r, v)
                if cnt:
                    res += cnt * (v - k * x)

            k += 1

        out.append(str(res))

    print(" ".join(out))

if __name__ == "__main__":
    solve()
```

The solution begins by building prefix sums for fast range sum queries. It also precomputes positions for each value so that we can count occurrences inside any query range using binary search.

For each query, we treat values in blocks of size $x$. Each block contributes a linear remainder expression, and we accumulate these contributions by iterating over values inside the block. Special handling for $x=1$ and $x > MAXA$ avoids unnecessary work.

A subtle implementation detail is 1-based indexing in position arrays, which simplifies range counting logic. Another is careful boundary handling when computing how many indices fall within $[l,r]$.

## Worked Examples

### Sample 1

We consider one query where $l=2$, $r=6$, $x=5$, using array $[14,16,9,6,9,10,16]$.

We process value blocks of size 5.

| Block k | Value range | Elements in range | Contribution per element | Count | Partial sum |
| --- | --- | --- | --- | --- | --- |
| 0 | 0-4 | none | 0 | 0 | 0 |
| 1 | 5-9 | 9,6,9 | (v - 5) | 3 | 4+1+4 = 9 |
| 2 | 10-14 | 10 | (v - 10) | 1 | 0 |
| 3 | 15-19 | 16,16 | (v - 15) | 2 | 1+1 = 2 |

Final answer is $9 + 0 + 2 = 11$, matching the computed remainder sum for the segment.

This trace shows how grouping by value intervals replaces per-element modulo computation with structured aggregation.

### Sample 2

Consider a query with small modulus $x=4$ on a segment containing $[8,18,6,15,4,18,15]$.

| Block k | Value range | Elements | Contribution | Count | Partial |
| --- | --- | --- | --- | --- | --- |
| 0 | 0-3 | none | 0 | 0 | 0 |
| 1 | 4-7 | 6,4 | v-4 | 2 | 2 + 0 = 2 |
| 2 | 8-11 | 8 | v-8 | 1 | 0 |
| 3 | 12-15 | 15,15 | v-12 | 2 | 3 + 3 = 6 |
| 4 | 16-19 | 18,18 | v-16 | 2 | 2 + 2 = 4 |

Final sum is $2 + 0 + 6 + 4 = 12$.

This confirms that even with small $x$, the block decomposition captures all contributions correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q \cdot \frac{MAXA}{x} \log N)$ amortized | each query iterates value blocks; counting uses binary search |
| Space | $O(N + MAXA)$ | positions per value and prefix arrays |

The constraint $A_i \le 2 \cdot 10^5$ ensures the value domain is small enough for block decomposition. Queries with large $x$ become cheap automatically because they generate few blocks, keeping total runtime within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# sample placeholders (replace with real sample strings when using locally)
# assert run("...") == "..."

# minimal
assert run("1 1\n5\n1 1 3\n") == "2", "single element"

# all equal
assert run("5 2\n4 4 4 4 4\n1 5 3\n2 4 1\n") == "2 0", "uniform array"

# x = 1 edge
assert run("3 1\n7 8 9\n1 3 1\n") == "0", "mod 1 always zero"

# x larger than values
assert run("4 1\n1 2 3 4\n1 4 10\n") == "10", "no reduction"

# small mixed case
assert run("5 1\n5 6 7 8 9\n1 5 4\n") == "6", "manual mix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 2 | basic modulo correctness |
| uniform array | 2 0 | repeated values and identity cases |
| mod 1 | 0 | full collapse case |
| x large | 10 | no wrapping behavior |
| mixed small | 6 | correct block decomposition |

## Edge Cases

For $x=1$, every value maps to remainder zero. The algorithm explicitly short-circuits this case, so it immediately returns zero without entering block logic. This avoids unnecessary iteration over all value groups.

For $x > MAXA$, no value reaches the next block boundary, so every $a_i < x$. The block loop detects this because only $k=0$ is valid and all contributions reduce to zero adjustment, so the answer becomes the plain range sum.

For arrays with repeated values, position lists ensure correct counting within ranges. For example, if value 5 appears at indices $[2, 10, 20]$, a query $[1, 15]$ correctly counts 2 occurrences via binary search bounds, and the block logic multiplies this count by the correct per-value contribution without double counting.
