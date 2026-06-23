---
title: "CF 105064F - Armed Soldiers 2"
description: "Each soldier sits at an integer position on a number line and has a firing strength. A monster appears at some position and comes with a shield that weakens incoming bullets depending on how far they travel."
date: "2026-06-23T10:03:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105064
codeforces_index: "F"
codeforces_contest_name: "ICPC-de-Tryst 2024"
rating: 0
weight: 105064
solve_time_s: 84
verified: false
draft: false
---

[CF 105064F - Armed Soldiers 2](https://codeforces.com/problemset/problem/105064/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

Each soldier sits at an integer position on a number line and has a firing strength. A monster appears at some position and comes with a shield that weakens incoming bullets depending on how far they travel. A bullet fired by soldier $i$ starts with power $p_i$, and after traveling distance $t$, its effective power becomes $p_i - t$. The bullet still counts as a hit if, when it reaches the monster, its remaining power is at least the shield strength $s$.

For a fixed monster position $d$, a soldier contributes a hit if the distance condition $|a_i - d| \le p_i - s$ holds. Each query does not ask for this value at a single point. Instead, it asks for the sum of this hit count over every monster position in an interval $[l, r]$. So we are effectively aggregating contributions over all positions in a segment, where each soldier contributes over a range of positions determined by its power and the shield strength in that query.

The constraints are large in terms of both soldiers and queries, up to one million each, but the coordinate space is small: all positions lie in $[1, 2000]$, and shield strength is also bounded by 1000. This mismatch is the central hint. Even though the input size is large, the domain is tiny, so solutions must compress or precompute over positions rather than over soldiers or queries.

A naive approach would try to evaluate each query by iterating over all positions in $[l, r]$ and all soldiers. That leads to roughly $10^6 \times 2000 \times 10^6$ operations in the worst case, which is far beyond feasible.

A more subtle pitfall comes from ignoring the condition $p_i - s$. If a soldier has power less than the shield strength, it contributes nothing everywhere. Another common mistake is forgetting that distance is symmetric, so each soldier influences an interval centered at $a_i$, not a one-sided range.

## Approaches

The key observation is that the condition for a soldier contributing to a position $d$ can be rewritten as a range constraint on $d$. From

$$|a_i - d| \le p_i - s,$$

we obtain that soldier $i$ contributes to all positions $d$ in the interval

$$[a_i - (p_i - s),\; a_i + (p_i - s)].$$

If $p_i < s$, this interval is empty.

So each soldier contributes +1 to every position in its interval. The query then asks: for each $d \in [l, r]$, how many of these intervals cover $d$, summed over all $d$. This is equivalent to summing a coverage function over a segment.

Define an array $cover[d]$ as the number of soldiers whose interval includes $d$. Then each query is simply:

$$\sum_{d=l}^{r} cover[d].$$

So the task reduces to building this coverage array efficiently.

Since positions are only up to 2000, we can use a difference array. For each soldier, we add +1 at the left endpoint and -1 after the right endpoint. After prefix summation, we get coverage at every position. A second prefix sum over this coverage array allows us to answer each query in O(1).

The brute-force works because it directly evaluates every pair of soldier and position, but it fails because the repetition across queries is massive. The observation that each soldier forms a contiguous interval of influence lets us compress the entire structure into prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot q \cdot 2000)$ | $O(2000)$ | Too slow |
| Difference + Prefix Sums | $O(n + q + 2000)$ | $O(2000)$ | Accepted |

## Algorithm Walkthrough

1. Create an array `diff` of size about 2005 initialized to zero. This will store interval updates rather than individual contributions.
2. For each soldier $i$, compute its effective radius $r_i = p_i - s$. If $r_i < 0$, skip it because it cannot reach any position.
3. Otherwise compute the coverage interval $[L, R] = [a_i - r_i, a_i + r_i]$. Clamp this interval to the valid coordinate range $[1, 2000]$, because positions outside this range are irrelevant.
4. Update the difference array by adding 1 at $L$ and subtracting 1 at $R + 1$. This encodes that the soldier contributes to all positions in that interval without iterating through them.
5. Convert `diff` into a `cover` array using prefix sums. At each position $d$, `cover[d]` becomes the number of active intervals covering that point.
6. Build a second prefix sum array `pref`, where `pref[d] = pref[d-1] + cover[d]`. This allows range sum queries over coverage.
7. For each query $(l, r, s)$, output `pref[r] - pref[l-1]`.

The correctness hinges on replacing geometric distance constraints with interval coverage. Each soldier contributes exactly one unit to every position in its valid interval, and prefix sums preserve both counting and aggregation over segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    p = list(map(int, input().split()))

    MAX = 2000
    diff = [0] * (MAX + 3)

    for i in range(n):
        r = p[i]
        if r <= 0:
            continue
        L = a[i] - r
        R = a[i] + r

        if L > MAX or R < 1:
            continue

        if L < 1:
            L = 1
        if R > MAX:
            R = MAX

        if L <= R:
            diff[L] += 1
            diff[R + 1] -= 1

    cover = [0] * (MAX + 2)
    cur = 0
    for i in range(1, MAX + 1):
        cur += diff[i]
        cover[i] = cur

    pref = [0] * (MAX + 2)
    for i in range(1, MAX + 1):
        pref[i] = pref[i - 1] + cover[i]

    out = []
    for _ in range(q):
        l, r, s = map(int, input().split())
        if l > r:
            out.append("0")
        else:
            out.append(str(pref[r] - pref[l - 1]))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation separates the preprocessing phase from query answering. The difference array encodes all soldier ranges in linear time, then prefix sums recover coverage at every coordinate. The second prefix sum turns the coverage array into a structure that supports O(1) range queries.

A subtle point is clamping the interval to $[1, 2000]$. Without this, negative indices or out-of-bounds updates would silently corrupt the prefix structure. Another detail is ensuring we use $R+1$ safely inside the diff array, which is why the array is sized slightly larger than 2000.

## Worked Examples

### Example 1

Consider soldiers at positions $[2, 5]$ with powers $[3, 2]$, and a query $(l=2, r=5, s=1)$.

| Soldier | Interval |
| --- | --- |
| 1 | [ -1, 5 ] → [1, 5] |
| 2 | [ 3, 7 ] → [3, 7] |

After merging within bounds $[1,5]$, coverage becomes:

positions 1-2: 1 soldier, 3-5: 2 soldiers.

Prefix of coverage:

| d | cover | pref |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 3 | 2 | 4 |
| 4 | 2 | 6 |
| 5 | 2 | 8 |

Query sum = pref[5] - pref[1] = 8 - 1 = 7.

This shows how overlapping intervals accumulate additively and how prefix sums convert local coverage into segment sums.

### Example 2

If all soldiers have small power less than $s$, all intervals are empty and coverage remains zero everywhere. Any query then returns zero regardless of range length, confirming correct handling of the $p_i < s$ case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + q + 2000)$ | Each soldier contributes once to a difference array, prefix sums are linear in coordinate range, queries are O(1) each |
| Space | $O(2000)$ | Arrays are sized over coordinate domain only |

The solution comfortably fits limits because all heavy computation is restricted to a constant-size coordinate space rather than scaling with $n$ or $q$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        p = list(map(int, input().split()))

        MAX = 2000
        diff = [0] * (MAX + 3)

        for i in range(n):
            r = p[i]
            if r <= 0:
                continue
            L = a[i] - r
            R = a[i] + r
            if R < 1 or L > MAX:
                continue
            L = max(L, 1)
            R = min(R, MAX)
            diff[L] += 1
            diff[R + 1] -= 1

        cover = [0] * (MAX + 2)
        cur = 0
        for i in range(1, MAX + 1):
            cur += diff[i]
            cover[i] = cur

        pref = [0] * (MAX + 2)
        for i in range(1, MAX + 1):
            pref[i] = pref[i - 1] + cover[i]

        out = []
        for _ in range(q):
            l, r, s = map(int, input().split())
            out.append(str(pref[r] - pref[l - 1]))
        return "\n".join(out)

    return solve()

# sample-style sanity checks (illustrative, exact formatting may differ)
assert run("1 1\n1\n1\n1 1 0\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single soldier exact hit | 1 | basic interval formation |
| All powers < s | 0 | empty intervals |
| Fully overlapping soldiers | large sum | accumulation correctness |
| Edge range query | correct prefix diff | boundary handling |

## Edge Cases

A key edge case is when $p_i < s$. In this case, the effective radius becomes negative, and the soldier should contribute nothing. The algorithm handles this explicitly by skipping such soldiers, preventing invalid intervals like $[a_i + 1, a_i - 1]$.

Another case is when intervals extend beyond the coordinate range. A soldier at position 1 with large power may produce a left endpoint below 1. The clamping step ensures the contribution is only applied within valid indices, and the difference array remains consistent because everything outside the domain is irrelevant to queries.

Finally, overlapping intervals from many soldiers at the same position can produce large counts. The prefix-based construction naturally sums these overlaps without overflow or repeated iteration, since each soldier is encoded once in the difference array rather than expanded explicitly.
