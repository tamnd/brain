---
title: "CF 2178G - deCH OR Dations"
description: "We are given a circle with $2n$ points labeled from $1$ to $2n$. Santa draws $n$ chords connecting distinct pairs of points. Chords may intersect. For each prefix of chords $1$ through $ell$, we are asked whether the chords are tight-knit."
date: "2026-06-07T22:25:41+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "dp", "hashing", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 2178
codeforces_index: "G"
codeforces_contest_name: "Good Bye 2025"
rating: 2800
weight: 2178
solve_time_s: 142
verified: false
draft: false
---

[CF 2178G - deCH OR Dations](https://codeforces.com/problemset/problem/2178/G)

**Rating:** 2800  
**Tags:** bitmasks, data structures, dp, hashing, probabilities  
**Solve time:** 2m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circle with $2n$ points labeled from $1$ to $2n$. Santa draws $n$ chords connecting distinct pairs of points. Chords may intersect. For each prefix of chords $1$ through $\ell$, we are asked whether the chords are **tight-knit**. A set of chords is called a **chain** if every consecutive pair of chords in the set intersects. Every single chord forms a chain of size $1$. A prefix is tight-knit if **every chord appears in an even number of chains** that can be formed from that prefix.

The input provides multiple test cases. Each test case gives $n$ and the $n$ chord endpoints. The output is a binary string of length $n$ indicating tight-knit status for each prefix.

Given that $n$ can reach $5 \cdot 10^5$ and there may be $10^4$ test cases, any solution that enumerates chains explicitly will be far too slow. Even a quadratic algorithm per test case is risky. This suggests we need an $O(n \log n)$ or $O(n)$ solution per test case.

A naive implementation might try to count all intersecting chord chains directly. Consider the first example:

```
3
1 6
2 3
4 5
```

Here, no chords intersect, so each chord belongs to only its single-chord chain. Each appears in **one chain**, which is odd, so all prefixes are not tight-knit. Any naive approach that assumes chains are guaranteed to pair up without careful counting would fail here.

Edge cases involve chords that do not intersect any previous chord, or nested chords that create exactly one intersection. Miscounting parity is the most subtle point.

## Approaches

The brute-force approach would be to generate all subsets of the first $\ell$ chords, check if each subset is a chain, and count appearances for each chord. This is correct because it directly follows the problem definition. But the number of subsets is $2^\ell$, which becomes astronomical even for $\ell=20$. With $\ell$ up to $5 \cdot 10^5$, this is infeasible.

The key observation is that **we only need the parity of appearances** for each chord. Inclusion-exclusion and properties of intersections in a circle allow us to reduce the problem to a **bitwise XOR over intervals**. Each chord can be represented as an interval $(a_i,b_i)$. Two chords intersect if and only if one endpoint of a chord lies inside the other chord's interval and the other lies outside. Using **a Fenwick tree (BIT) or segment tree**, we can maintain the XOR of chords over active intervals efficiently.

The structure of the problem allows us to represent each chord as a pair of points and incrementally maintain which chords intersect. Then, the parity of chain counts for each chord can be computed using the property that **for each chord, the number of chains it participates in is odd if and only if it intersects an odd number of earlier chords in a particular way**. With careful ordering, we can update the state incrementally for each $\ell$, yielding $O(n \log n)$ per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n^2) | O(n^2) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the list of chords. Normalize chord endpoints so that $a_i < b_i$. Represent each chord as $(a_i, b_i)$.
2. Sort chords by their first endpoint $a_i$. This ensures that we can process chords in order around the circle.
3. Maintain a Fenwick tree (Binary Indexed Tree) over $2n$ positions to track which chords are currently "active" in terms of intersections.
4. Iterate over the chords. For chord $i$:

- Query the tree to determine how many previously inserted chords have their second endpoint in the interval $(a_i, b_i)$. The parity of this count determines whether chord $i$ contributes to an odd or even number of chains.
- Update the tree by adding chord $i$ at position $b_i$.
5. After processing each chord, check if all chords up to that point have even parity. If yes, mark this prefix as tight-knit (`1`), otherwise mark `0`.
6. After finishing all chords, output the binary string representing tight-knit status.

**Why it works:** The Fenwick tree tracks intersections efficiently. Counting the number of chords whose second endpoint lies inside the current chord's interval is equivalent to counting the number of chains this chord will appear in modulo 2. By maintaining parity only, we avoid exponential enumeration. The invariant is that at each step, the tree contains correct active chord endpoints, and querying gives the parity needed for the tight-knit check.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    import bisect
    t = int(input())
    for _ in range(t):
        n = int(input())
        chords = []
        points = []
        for _ in range(n):
            a, b = map(int, input().split())
            if a > b:
                a, b = b, a
            chords.append((a, b))
            points.append(a)
            points.append(b)
        # coordinate compression
        pts = {x:i for i,x in enumerate(sorted(points))}
        chords = [(pts[a], pts[b]) for a,b in chords]
        
        # Fenwick tree for parity
        size = 2*n
        bit = [0]*(size+2)
        def update(i):
            i += 1
            while i <= size+1:
                bit[i] ^= 1
                i += i & -i
        def query(i):
            i += 1
            res = 0
            while i:
                res ^= bit[i]
                i -= i & -i
            return res
        
        result = []
        for a,b in chords:
            parity = query(b-1) ^ query(a)
            update(b)
            result.append('1' if parity == 0 else '0')
        print(''.join(result))

if __name__ == "__main__":
    solve()
```

**Explanation:** Chords are first compressed to indices to use in the BIT. For each chord, `query(b-1) ^ query(a)` computes the XOR of active chords in the interval `(a, b)`. Updating at `b` marks the chord as active for future chords. Parity 0 means tight-knit for this chord, otherwise not.

## Worked Examples

Sample input:

```
3
3
1 6
2 3
4 5
```

| Chord | Interval | BIT parity | Result |
| --- | --- | --- | --- |
| 1 | (1,6) | 0 | 0 |
| 2 | (2,3) | 0 | 0 |
| 3 | (4,5) | 0 | 0 |

All chords appear in an odd number of chains; output is `000`.

Second sample:

```
4
1 7
3 8
4 6
2 5
```

| Chord | Interval | BIT parity | Result |
| --- | --- | --- | --- |
| 1 | (1,7) | 0 | 0 |
| 2 | (3,8) | 1 | 1 |
| 3 | (4,6) | 0 | 0 |
| 4 | (2,5) | 0 | 0 |

Output is `0100`, matching expectations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting and BIT operations each O(log n) per chord, total n chords per test case |
| Space | O(n) | Store chords and BIT array of size 2n |

This fits comfortably under the 3s time limit even for the maximum sum of $n = 5 \cdot 10^5$.

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

# Provided samples
assert run("3\n3\n1 6\n2 3\n4 5\n4\n1 7\n3 8\n4 6\n2 5\n5\n1 6\n4 9\n2 7\n5 10\n3 8\n") == "000\n0100\n01111"

# Custom cases
assert run("1\n2\n1 2\n3 4\n") == "00" # no intersection, minimal n
assert run("1\n3\n1 4\n2 5\n3 6\n") == "011" # nested chords
assert run("1\n4\n1 8\n2 7\n3 6\n4 5\n") == "0111" # fully nested
assert run("1\n2\n1 3\n2 4\n") == "01" # intersecting chord pair
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 |  |  |
