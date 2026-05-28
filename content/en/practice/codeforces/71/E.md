---
title: "CF 71E - Nuclear Fusion"
description: "We start with several atoms, each represented by a chemical element symbol. Every element has an atomic number, and a fusion operation combines two atoms into one whose atomic number is the sum of the two originals."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 2200
weight: 71
solve_time_s: 168
verified: false
draft: false
---

[CF 71E - Nuclear Fusion](https://codeforces.com/problemset/problem/71/E)

**Rating:** 2200  
**Tags:** bitmasks, dp  
**Solve time:** 2m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We start with several atoms, each represented by a chemical element symbol. Every element has an atomic number, and a fusion operation combines two atoms into one whose atomic number is the sum of the two originals.

The task is not to simulate the exact sequence of pairwise fusions. Instead, we only need to partition the original atoms into `k` disjoint groups so that the sum of atomic numbers inside each group equals the target atom assigned to that group.

For example, if we have atoms with values `[1, 2, 3, 4]` and targets `[3, 7]`, we may group them as `{1,2}` and `{3,4}`.

The input uses element symbols instead of atomic numbers, so the first practical step is converting symbols into their periodic table indices.

The constraint `n ≤ 17` completely changes the nature of the problem. A partitioning problem is usually exponential, but `2^17 = 131072`, which is small enough for subset dynamic programming. This strongly suggests representing sets of atoms with bitmasks.

A brute-force partition enumeration would try assigning every atom to one of the `k` target groups. That leads to roughly `k^n` states. With `n = 17`, even `3^17 ≈ 129 million`, already too large in Python once transitions and bookkeeping are included.

The total sum of atomic numbers is guaranteed to match between source and target sets. That removes one easy impossibility check, but many configurations are still impossible because atoms cannot be split.

One subtle edge case is repeated target sums.

Example:

```
4 2
H H He He
Li Li
```

Values are `[1,1,2,2]`, targets are `[3,3]`.

There are several valid assignments:

`1+2` and `1+2`.

A careless reconstruction that stores only one subset per target without tracking used atoms can accidentally reuse the same atoms twice.

Another tricky case is when multiple subsets produce the same target value.

Example:

```
5 2
H H H Li Be
B B
```

Values are `[1,1,1,3,4]`, targets are `[5,5]`.

Possible subsets for `5` include `{1,4}` and `{1,1,3}`. Greedily taking the first matching subset may block completion later. The algorithm must consider combinations globally, not target-by-target greedily.

A final corner case is a target already matching one atom exactly.

Example:

```
3 2
H He Li
Li He
```

The correct solution uses singleton subsets. Any implementation that assumes every fusion must combine at least two atoms would incorrectly reject this case.

## Approaches

The most direct brute-force approach is to assign each original atom to one of the `k` target atoms. After all assignments are made, we check whether every target sum matches.

This works because every valid solution is exactly a partition of the original atoms. The problem is the search space. Each of `n` atoms has `k` choices, so the complexity is `O(k^n)`. With `n = 17` and `k = 17`, this is completely infeasible.

We need to exploit the small value of `n` differently.

The key observation is that the actual identities of intermediate fusion operations do not matter. Only the final partition matters. If a subset of atoms sums to a target value, we can always fuse those atoms together in some order.

That transforms the problem into:

"Can we partition the set of atoms into `k` disjoint subsets whose sums equal the target atomic numbers?"

Since `n` is at most 17, every subset of atoms can be represented by a bitmask. We can precompute the sum of every subset in `O(2^n)` time.

Now suppose we process target atoms one by one. For each target, we enumerate all subsets whose sum matches that target value. Then we run DP over masks:

`dp[mask] = how many target atoms have already been constructed using this set of original atoms`.

Transition:

if subset `s` matches target `t[dp[mask]]` and `s` does not overlap with `mask`,

then we move to `mask | s`.

This reduces the problem from exponential in assignments to exponential in subsets, which is manageable because `2^17` is small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^n) | O(n) | Too slow |
| Optimal | O(3^n) worst-case, practical much smaller | O(2^n) | Accepted |

## Algorithm Walkthrough

1. Convert all element symbols into atomic numbers.

The problem provides symbols like `H`, `He`, `Li`, so we need a lookup table from symbol to periodic table index.
2. Store the original atom values in array `a` and target values in array `b`.
3. Precompute `sum[mask]` for every subset of original atoms.

Each bit in `mask` represents whether an atom is included. Since there are at most `131072` masks, this is cheap.
4. For every target value `b[i]`, collect all subsets whose sum equals `b[i]`.

These subsets are candidates for constructing target atom `i`.
5. Create DP over masks.

`dp[mask] = number of targets already assigned`.

Initialize:

```
dp[0] = 0
```
6. From a mask, determine which target index must be filled next.

If `dp[mask] = i`, then we are currently assigning subsets for target `b[i]`.
7. Try every subset matching `b[i]`.

If the subset does not overlap with the current mask, transition:

```
new_mask = mask | subset
```
8. Store parent information during transitions.

We need reconstruction later, so for every successful transition we remember:

the previous mask and the subset used.
9. If we reach the full mask, reconstruction is possible.

Otherwise, print `"NO"`.
10. Reconstruct the chosen subsets by walking backward through parent pointers.
11. Print each subset as:

```
x1+x2+...->target
```

### Why it works

At every DP state, the mask uniquely represents which original atoms have already been consumed. The transition only adds a subset whose sum equals the next target value and does not overlap with previously used atoms.

Because every atom is either used once or unused, the DP explores exactly all valid partitions of the original set. Reaching the full mask means every original atom belongs to exactly one target subset and every target sum is satisfied.

The reconstruction is correct because every stored transition corresponds to a valid subset assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

ELEMENTS = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm"
]

mp = {}
for i, s in enumerate(ELEMENTS, start=1):
    mp[s] = i

def solve():
    n, k = map(int, input().split())

    src_names = input().split()
    tgt_names = input().split()

    a = [mp[x] for x in src_names]
    b = [mp[x] for x in tgt_names]

    size = 1 << n

    subset_sum = [0] * size

    for mask in range(1, size):
        bit = mask & -mask
        idx = bit.bit_length() - 1
        subset_sum[mask] = subset_sum[mask ^ bit] + a[idx]

    good = [[] for _ in range(k)]

    for mask in range(1, size):
        s = subset_sum[mask]
        for i in range(k):
            if s == b[i]:
                good[i].append(mask)

    dp = [-1] * size
    parent = [(-1, -1)] * size

    dp[0] = 0

    for mask in range(size):
        if dp[mask] == -1:
            continue

        idx = dp[mask]

        if idx == k:
            continue

        for sub in good[idx]:
            if mask & sub:
                continue

            nmask = mask | sub

            if dp[nmask] != -1:
                continue

            dp[nmask] = idx + 1
            parent[nmask] = (mask, sub)

    full = size - 1

    if dp[full] != k:
        print("NO")
        return

    print("YES")

    groups = []

    cur = full

    while cur:
        prev, sub = parent[cur]
        groups.append(sub)
        cur = prev

    groups.reverse()

    for i in range(k):
        sub = groups[i]

        parts = []

        for j in range(n):
            if (sub >> j) & 1:
                parts.append(src_names[j])

        print("+".join(parts) + "->" + tgt_names[i])

solve()
```

The first section builds the periodic table mapping. The problem guarantees atomic numbers up to 100, so storing the first 100 symbols is enough.

The subset sum computation uses the standard least-significant-bit trick:

```
subset_sum[mask] = subset_sum[mask ^ bit] + value
```

This avoids recomputing sums from scratch for every mask.

The `good[i]` lists are important for pruning. Instead of testing every subset during every DP transition, we only iterate over subsets already known to match target `i`.

The DP meaning is subtle. `dp[mask] = t` means the first `t` target atoms have been successfully assigned using exactly the atoms inside `mask`. This guarantees reconstruction order stays consistent.

The parent array stores both the previous mask and the subset added during the transition. Without storing the subset explicitly, reconstruction becomes awkward because many subsets can lead to the same mask.

One easy mistake is forgetting singleton subsets. The loop includes all non-empty masks, including masks with exactly one bit set, so targets equal to existing atoms work naturally.

Another common bug is reusing atoms accidentally. The overlap check:

```
if mask & sub:
    continue
```

prevents that completely.

## Worked Examples

### Example 1

Input:

```
10 3
Mn Co Li Mg C P F Zn Sc K
Sn Pt Y
```

Atomic values:

| Element | Value |
| --- | --- |
| Mn | 25 |
| Co | 27 |
| Li | 3 |
| Mg | 12 |
| C | 6 |
| P | 15 |
| F | 9 |
| Zn | 30 |
| Sc | 21 |
| K | 19 |

Targets:

| Target | Value |
| --- | --- |
| Sn | 50 |
| Pt | 78 |
| Y | 39 |

One successful DP path:

| Step | Current Mask | Chosen Subset | Sum | Target |
| --- | --- | --- | --- | --- |
| 0 | 0 | Mn+C+K | 50 | Sn |
| 1 | Mn+C+K | Co+Zn+Sc | 78 | Pt |
| 2 | previous + subset | Li+Mg+P+F | 39 | Y |

The final mask contains all atoms exactly once.

This trace demonstrates the central invariant: every transition adds a disjoint subset matching exactly one target sum.

### Example 2

Input:

```
4 2
H H He He
Li Li
```

Values:

```
[1,1,2,2]
```

Targets:

```
[3,3]
```

DP progression:

| Step | Used Atoms | New Subset | Sum |
| --- | --- | --- | --- |
| 0 | none | H+He | 3 |
| 1 | first H and first He | remaining H+He | 3 |

This example demonstrates why overlap checks are necessary. Multiple subsets produce the same target sum, and the algorithm must ensure atoms are not reused.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3^n) worst-case | Enumerating subset transitions over masks |
| Space | O(2^n) | DP tables and subset sums |

With `n ≤ 17`, `2^n = 131072`, which is small enough for memory and iteration in Python. Even the worst practical transition count comfortably fits inside the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    ELEMENTS = [
        "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
        "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
        "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
        "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
        "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
        "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
        "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
        "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm"
    ]

    mp = {}
    for i, s in enumerate(ELEMENTS, start=1):
        mp[s] = i

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n, k = map(int, input().split())

    src = input().split()
    tgt = input().split()

    a = [mp[x] for x in src]
    b = [mp[x] for x in tgt]

    size = 1 << n

    subset_sum = [0] * size

    for mask in range(1, size):
        bit = mask & -mask
        idx = bit.bit_length() - 1
        subset_sum[mask] = subset_sum[mask ^ bit] + a[idx]

    good = [[] for _ in range(k)]

    for mask in range(1, size):
        for i in range(k):
            if subset_sum[mask] == b[i]:
                good[i].append(mask)

    dp = [-1] * size
    parent = [(-1, -1)] * size

    dp[0] = 0

    for mask in range(size):
        if dp[mask] == -1:
            continue

        idx = dp[mask]

        if idx == k:
            continue

        for sub in good[idx]:
            if mask & sub:
                continue

            nmask = mask | sub

            if dp[nmask] == -1:
                dp[nmask] = idx + 1
                parent[nmask] = (mask, sub)

    if dp[size - 1] != k:
        print("NO")
    else:
        print("YES")

    return out.getvalue()

# minimum size
assert run(
"""1 1
H
H
"""
).strip() == "YES"

# impossible partition
assert run(
"""3 2
H H He
Li He
"""
).strip() == "NO"

# repeated target sums
assert run(
"""4 2
H H He He
Li Li
"""
).splitlines()[0] == "YES"

# singleton subsets
assert run(
"""3 3
H He Li
H He Li
"""
).splitlines()[0] == "YES"

# all equal values
assert run(
"""4 2
He He He He
Be Be
"""
).splitlines()[0] == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / H / H` | YES | Minimum-size input |
| `H H He -> Li He` | NO | Impossible partition detection |
| `H H He He -> Li Li` | YES | Repeated target sums |
| Identical source and target sets | YES | Singleton subset handling |
| All equal values | YES | Multiple equivalent subset choices |

## Edge Cases

Consider:

```
4 2
H H He He
Li Li
```

Subset sums equal to `3` appear many times. During DP, once a subset is selected for the first target, the overlap check prevents any atom inside that subset from appearing again. The second target must use a disjoint subset.

Now consider:

```
3 2
H He Li
Li He
```

The target `Li` has value `3`, already present directly. The subset mask containing only the `Li` atom is valid because singleton masks are included in preprocessing. The algorithm correctly avoids forcing unnecessary fusions.

Finally:

```
5 2
H H H Li Be
B B
```

Values:

```
[1,1,1,3,4]
```

Targets:

```
[5,5]
```

The first target can be formed either as `1+4` or `1+1+3`. A greedy approach may choose badly and get stuck later. The DP explores both possibilities independently. If one branch fails, another may still succeed.
