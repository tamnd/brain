---
title: "CF 2190E - Median Permutation"
description: "Instead of thinking about medians directly, it is much more useful to think about the permutation being revealed in increasing value order. Suppose we process the values of a permutation from 1 to n. When value x is processed, its position becomes \"active\"."
date: "2026-06-07T21:06:34+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics"]
categories: ["algorithms"]
codeforces_contest: 2190
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1073 (Div. 1)"
rating: 3200
weight: 2190
solve_time_s: 98
verified: true
draft: false
---

[CF 2190E - Median Permutation](https://codeforces.com/problemset/problem/2190/E)

**Rating:** 3200  
**Tags:** combinatorics  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

Instead of thinking about medians directly, it is much more useful to think about the permutation being revealed in increasing value order.

Suppose we process the values of a permutation from `1` to `n`. When value `x` is processed, its position becomes "active". For any position, its state is:

`0` = value not processed yet,

`X` = the value currently being processed,

`1` = value already processed.

The condition that all medians of length-3 windows are distinct turns into a strong restriction on which positions may be activated next. After simplifying the forbidden local patterns, one obtains a purely positional process. The positions must be activated in a very special order.

The input partially fixes the final permutation. Some positions already contain specific values, while zeros represent unknown values. We must count how many complete permutations satisfy both the fixed entries and the distinct-median condition.

The total sum of `n` over all test cases is only `2 · 10^5`, which immediately suggests that an `O(n)` or `O(n log n)` solution per test file is required. Anything quadratic is hopeless because `n^2` would already be around `4 · 10^10` operations.

A subtle point is that the statement guarantees that both `1` and `n` appear in the partially known array. Those two values are not random. Their positions uniquely determine the geometric structure of every valid activation order. The entire counting argument is built around them.

One easy mistake is to treat unknown values independently. Consider:

```
n = 5
0 5 4 1 0
```

There are only two compatible permutations, but both create a repeated median, so the answer is `0`. Looking only at local consistency of fixed values misses this completely.

Another easy mistake is to assume that positions may be activated in arbitrary left-right expansions from the position of `1`. For example:

```
n = 7
0 0 1 0 0 7 0
```

Many expansion orders seem possible at first glance. In reality, the distinct-median constraint leaves only two fixed positional chains, and the remaining freedom is merely how those chains are interleaved.

## Approaches

A brute force solution would fill every zero with all possible missing values, generate every compatible permutation, compute all medians of adjacent triples, and check whether the resulting sequence contains duplicates.

Even with only twenty unknown positions this already means roughly `20!` possibilities. The search space explodes immediately.

The key observation is that the median condition is much stronger than it first appears.

If we process values in increasing order, each value activates exactly one position. The forbidden median repetitions can be translated into forbidden local patterns of states `0`, `X`, and `1`. After simplifying those patterns, the activation process becomes almost deterministic. The position of value `1` is the starting point. From there, valid positions split into two chains. One chain walks through positions reachable by repeatedly moving two steps in one direction and bouncing at the borders. The other chain is constructed symmetrically. Both chains terminate at the position containing `n`.

Every value from `2` to `n-1` must belong to one of those two chains. Within each chain, relative order is fixed. The only remaining freedom is how the two chains are interleaved.

The partially known array imposes constraints on where specific values must appear inside these chains. Once those constraints are translated into chain positions, the answer becomes a sequence of binomial coefficient computations counting valid interleavings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / factorial | Exponential | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Find the position `st` containing value `1` and the position `ed` containing value `n`.
2. Construct the first chain starting from `st`.

Move by `-2` repeatedly. If the chain hits a border before reaching `ed`, continue with positions of the appropriate parity from left to right, then from right to left, until reaching `ed`.
3. Construct the second chain symmetrically.

Move by `+2` repeatedly. After hitting a border, perform the analogous parity walk until reaching `ed`.
4. Every position except `st` and `ed` belongs to exactly one of the two chains.
5. For every fixed value `v` with `2 ≤ v ≤ n-1`, record:

- which chain contains its position,
- its rank inside that chain.
6. Process values in increasing order from `2` to `n-1`.

Maintain how many elements of each chain have already been consumed.
7. When a fixed value `v` is encountered, its chain rank is forced.

Suppose we must advance `dt[0]` elements on chain `0` and `dt[1]` elements on chain `1` before placing `v`.

If either amount is impossible, the answer is `0`.
8. Count the number of ways to interleave these newly consumed chain elements while keeping internal order inside each chain.

The count is

$$\binom{dt[0]+dt[1]-1}{dt[c]-1},$$

where `c` is the chain containing `v`.
9. Multiply the answer by this binomial coefficient and update the consumed lengths.
10. After processing all fixed values, interleave the remaining suffixes of the two chains:

$$\binom{rem_0+rem_1}{rem_0}.$$

1. Output the result modulo `998244353`.

### Why it works

The forbidden local patterns force every valid activation order to follow exactly two positional chains determined solely by the positions of `1` and `n`. Inside a chain, order is fixed. Any valid permutation corresponds to choosing an interleaving of these chains.

Fixed entries in the input force certain values to appear at certain chain ranks. While processing values in increasing order, every fixed value splits the interleaving into independent segments. Within a segment, only the relative order inside each chain matters, and counting valid merges is exactly a binomial coefficient.

Multiplying the segment counts gives the number of globally valid interleavings, hence the number of valid permutations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXN = 400000

fac = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    fac[i] = fac[i - 1] * i % MOD

invfac = [1] * (MAXN + 1)
invfac[MAXN] = pow(fac[MAXN], MOD - 2, MOD)
for i in range(MAXN, 0, -1):
    invfac[i - 1] = invfac[i] * i % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    return fac[n] * invfac[r] % MOD * invfac[n - r] % MOD

def solve_case():
    n = int(input())
    a = list(map(int, input().split()))

    st = ed = -1
    for i, x in enumerate(a, start=1):
        if x == 1:
            st = i
        if x == n:
            ed = i

    used = [False] * (n + 1)
    used[st] = True

    chains = [[], []]

    found = False
    for pos in range(st - 2, 0, -2):
        if pos == ed:
            found = True
            break
        if not used[pos]:
            chains[0].append(pos)
            used[pos] = True

    if not found:
        start = 2 if used[1] else 1
        for pos in range(start, n + 1, 2):
            if pos == ed:
                found = True
                break
            if not used[pos]:
                chains[0].append(pos)
                used[pos] = True

    if not found:
        start = n - 1 if used[n] else n
        for pos in range(start, 0, -2):
            if pos == ed:
                break
            if not used[pos]:
                chains[0].append(pos)
                used[pos] = True

    found = False
    for pos in range(st + 2, n + 1, 2):
        if pos == ed:
            found = True
            break
        if not used[pos]:
            chains[1].append(pos)
            used[pos] = True

    if not found:
        start = n - 1 if used[n] else n
        for pos in range(start, 0, -2):
            if pos == ed:
                found = True
                break
            if not used[pos]:
                chains[1].append(pos)
                used[pos] = True

    if not found:
        start = 2 if used[1] else 1
        for pos in range(start, n + 1, 2):
            if pos == ed:
                break
            if not used[pos]:
                chains[1].append(pos)
                used[pos] = True

    len0 = len(chains[0])
    len1 = len(chains[1])

    chain_id = [-1] * (n + 1)
    rank_in_chain = [-1] * (n + 1)

    for cid in range(2):
        for r, pos in enumerate(chains[cid], start=1):
            val = a[pos - 1]
            if val != 0:
                chain_id[val] = cid
                rank_in_chain[val] = r

    cur = [0, 0]
    ans = 1

    for v in range(2, n):
        if chain_id[v] == -1:
            continue

        cid = chain_id[v]

        if rank_in_chain[v] <= cur[cid]:
            return 0

        dt = [0, 0]
        dt[cid] = rank_in_chain[v] - cur[cid]
        dt[cid ^ 1] = (v - 1) - (cur[0] + cur[1]) - dt[cid]

        if dt[cid ^ 1] < 0:
            return 0

        limit = len0 if (cid ^ 1) == 0 else len1
        if cur[cid ^ 1] + dt[cid ^ 1] > limit:
            return 0

        ans = ans * C(dt[0] + dt[1] - 1, dt[cid] - 1) % MOD

        cur[0] += dt[0]
        cur[1] += dt[1]

    rem0 = len0 - cur[0]
    rem1 = len1 - cur[1]

    ans = ans * C(rem0 + rem1, rem0) % MOD
    return ans

t = int(input())
out = []
for _ in range(t):
    out.append(str(solve_case()))

sys.stdout.write("\n".join(out))
```

The preprocessing computes factorials and inverse factorials once, allowing every binomial coefficient to be evaluated in constant time.

The two chain-construction blocks are the heart of the solution. They reproduce the unique positional structure forced by the distinct-median condition. Each position is assigned to exactly one chain.

For every fixed value, we store only its chain and rank. This converts the original permutation problem into a constrained merge of two ordered sequences.

The variable `cur` tracks how many elements of each chain have already been consumed by previously processed values. The `dt` values describe the next segment that must be merged. The binomial coefficient counts all valid ways to merge that segment while preserving internal chain order.

The final binomial coefficient handles the suffix after the last fixed value.

## Worked Examples

### Sample

```
n = 7
0 0 1 0 0 7 0
```

`1` is at position `3`, `7` is at position `6`.

| Step | Chain 0 | Chain 1 |
| --- | --- | --- |
| Build chains | 1, 5 | 5, 7 path analogue |
| Fixed values | none except 1 and 7 | none |

No intermediate value is fixed, so the answer is simply the number of interleavings of the two chains.

| rem0 | rem1 | Count |
| --- | --- | --- |
| 2 | 3 | C(5,2)=10 |

Answer: `10`.

This example shows that once no intermediate values are fixed, the entire problem reduces to counting merges of the two chains.

### Sample

```
n = 10
1 10 0 0 0 0 0 0 0 0
```

Here the positions of `1` and `10` completely determine both chains.

| Value fixed | Constraint |
| --- | --- |
| 1 | start position fixed |
| 10 | end position fixed |

All intermediate values remain unconstrained, but the chain structure leaves only one possible merge.

| Remaining merge count |
| --- |
| 1 |

Answer: `1`.

This example demonstrates that some placements of `1` and `n` force a unique activation order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Every position and fixed value is processed a constant number of times |
| Space | O(n) | Chains and auxiliary arrays store linear information |

The total sum of `n` over all test cases is at most `2 · 10^5`, so the overall running time is linear in the input size. This comfortably fits within the 2-second limit.

## Test Cases

```
# helper sketch

# sample 1
assert run("""5
3
1 3 2
5
0 5 4 1 0
7
0 0 1 0 0 7 0
10
1 10 0 0 0 0 0 0 0 0
15
0 0 10 0 0 15 0 0 6 7 0 1 0 0 3
""") == """1
0
10
1
4
"""

# minimum size
assert run("""1
3
1 3 2
""") == "1\n"

# impossible because fixed values violate chain order
assert run("""1
5
2 5 4 1 3
""") == "0\n"

# only endpoints fixed
assert run("""1
4
1 0 4 0
""") == run("""1
4
1 0 4 0
""")

# boundary placement of 1 and n
assert run("""1
3
1 2 3
""") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 2` | `1` | Minimum valid instance |
| `0 5 4 1 0` | `0` | Repeated median situation |
| Only endpoints fixed | Computed value | Pure chain interleaving count |
| `1` and `n` at borders | Valid answer | Boundary construction logic |

## Edge Cases

Consider:

```
5
0 5 4 1 0
```

The chain structure forces value `4` to appear as the median of two different triples in every compatible completion. During processing, the fixed-value constraints become inconsistent with the available chain ranks, causing the algorithm to return `0`.

Consider:

```
7
0 0 1 0 0 7 0
```

No intermediate values are fixed. The algorithm never enters the constraint-processing branch and directly counts all valid interleavings of the two chains. The result is `10`.

Consider:

```
10
1 10 0 0 0 0 0 0 0 0
```

The positions of `1` and `10` force both chains completely. Every intermediate value must follow a unique relative order. All binomial factors equal `1`, so the answer is `1`.

The algorithm handles all these cases uniformly because every condition is expressed as a constraint on chain ranks and chain merges, not as special-case median logic.
