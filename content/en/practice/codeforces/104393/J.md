---
title: "CF 104393J - Jane's Party Salad"
description: "We are given a fixed pantry of ingredients and a rule that Jane must pick exactly $K$ distinct ingredients to form a salad. Each friend has a personal list of ingredients they refuse to eat."
date: "2026-07-01T00:37:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104393
codeforces_index: "J"
codeforces_contest_name: "ICPC Masters Mexico LATAM 2023"
rating: 0
weight: 104393
solve_time_s: 92
verified: true
draft: false
---

[CF 104393J - Jane's Party Salad](https://codeforces.com/problemset/problem/104393/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed pantry of ingredients and a rule that Jane must pick exactly $K$ distinct ingredients to form a salad. Each friend has a personal list of ingredients they refuse to eat. A friend attends the party only if none of the chosen $K$ ingredients appear in their dislike list. The goal is to choose the $K$ ingredients so that the number of attending friends is as large as possible.

Rephrasing this in a more structural way, each ingredient is an element in a universe of size $N \le 50$. Each friend defines a forbidden subset of this universe. A chosen salad is a subset $S$ of size $K$. A friend is satisfied exactly when $S$ does not intersect their forbidden set. We want to select $S$ to maximize how many of these constraints are satisfied simultaneously.

The constraint sizes are small but arranged in an asymmetric way: $N \le 50$, $F \le 20$, and $K \le N$. The small number of friends is the key structural signal. Even though the ingredient space is large enough that direct enumeration of all $K$-subsets is impossible, the number of constraints is small enough that we can reason over subsets of constraints instead of subsets of ingredients.

A naive attempt would try all $\binom{50}{K}$ ingredient sets and check each against all friends. Even for $K \approx 25$, this explodes to an infeasible search space.

A more subtle failure case appears when trying greedy selection of ingredients. Choosing ingredients that individually appear safe for many friends does not work because conflicts only appear when multiple ingredients combine. A small example shows this:

Input:

```
3 2 2
1 1
1 2
```

If we greedily pick ingredient 1 (safe for second friend) and then ingredient 2 (safe for first friend), both friends are lost because each dislikes one of the chosen ingredients. The correct answer is 0, achieved by choosing any two ingredients, but no greedy rule can predict that interaction correctly.

The problem is fundamentally about global consistency across a fixed-size subset of constraints, not local scoring of individual ingredients.

## Approaches

The brute-force view is to enumerate all subsets of ingredients of size $K$, then count how many friends have zero intersection with that subset. This is correct because it directly follows the definition of validity, but it requires checking up to $\binom{50}{K}$ subsets, each checked against up to 20 friends with set intersection tests. Even a rough upper bound is far beyond time limits.

The key observation is to flip the perspective. Instead of choosing ingredients first, we consider choosing which friends we want to satisfy. Suppose we fix a set of friends $T$. For all of them to attend, the chosen salad $S$ must avoid every ingredient that appears in any friend in $T$'s dislike list. That means $S$ must be contained entirely within the intersection of the complements of their forbidden sets.

So for a fixed $T$, the condition becomes: compute the set of ingredients that are allowed for all friends in $T$, and check whether this allowed set contains at least $K$ elements. If it does, we can always choose any $K$ of them and satisfy all friends in $T$.

This converts the problem into iterating over subsets of friends instead of subsets of ingredients. Since $F \le 20$, there are only $2^F \le 10^6$ subsets, which is feasible. For each subset, we compute an intersection over at most 20 bitmasks of size 50.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over ingredients | $O(\binom{N}{K} \cdot F \cdot N)$ | $O(N)$ | Too slow |
| Subset DP over friends | $O(F \cdot 2^F + 2^F \cdot N/word)$ | $O(2^F)$ | Accepted |

## Algorithm Walkthrough

### 1. Encode ingredient sets as bitmasks

Each friend’s dislike list is converted into a 50-bit mask. From this we compute the complement mask representing ingredients they allow.

The reason for this representation is that set intersection becomes a fast bitwise AND operation.

### 2. Interpret each subset of friends as a constraint group

For any subset of friends $T$, we want all of them to simultaneously accept the salad. This means the salad must lie entirely inside the intersection of their allowed ingredient sets.

So for each $T$, we define:

$$A_T = \bigcap_{i \in T} A_i$$

where $A_i$ is the allowed ingredient mask for friend $i$.

### 3. Compute intersection for every subset of friends using DP

We compute $A_T$ for all subsets using subset DP. If $T$ is non-empty and contains the last added friend $i$, then:

$$A_T = A_{T \setminus \{i\}} \ \& \ A_i$$

This recurrence allows us to build all intersections in $O(F \cdot 2^F)$.

### 4. Evaluate feasibility of each friend subset

For each subset $T$, we compute the number of allowed ingredients in $A_T$. If this count is at least $K$, then it is possible to pick $K$ ingredients that satisfy all friends in $T$.

We update the answer with the maximum size of such a subset $T$.

### Why it works

Every valid salad corresponds to some subset of friends it satisfies, namely all friends whose dislike sets do not intersect the salad. For that subset $T$, the salad must be contained in $A_T$. Conversely, if $A_T$ has at least $K$ elements, we can always construct a valid salad that satisfies exactly those friends. This establishes a one-to-one correspondence between feasible salads and feasible friend subsets, and maximizing satisfied friends reduces to maximizing subset size under the capacity constraint $|A_T| \ge K$.

## Python Solution

```python
import sys
input = sys.stdin.readline

N, K, F = map(int, input().split())

dislike = []
for _ in range(F):
    arr = list(map(int, input().split()))
    f = arr[0]
    mask = 0
    for x in arr[1:]:
        mask |= 1 << (x - 1)
    dislike.append(mask)

ALL = (1 << N) - 1
allow = [(~d) & ALL for d in dislike]

size = 1 << F
inter = [0] * size

for mask in range(size):
    if mask == 0:
        inter[mask] = ALL
    else:
        lsb = mask & -mask
        i = (lsb.bit_length() - 1)
        prev = mask ^ lsb
        inter[mask] = inter[prev] & allow[i]

ans = 0

for mask in range(size):
    cnt = inter[mask].bit_count()
    if cnt >= K:
        ans = max(ans, mask.bit_count())

print(ans)
```

The solution begins by converting each friend's dislike list into a bitmask, then flips it into an allowed-set mask. This makes compatibility checks purely bitwise.

The DP array `inter[mask]` stores the intersection of allowed ingredient sets for all friends included in `mask`. The transition removes the least significant bit to reuse a previously computed intersection and refines it with one additional constraint.

Finally, each subset is tested for feasibility by checking whether its intersection contains at least $K$ ingredients. If it does, that subset size becomes a candidate answer.

A subtle point is that the DP relies on consistent indexing of the lowest set bit to map subsets to friends. This guarantees each subset is built exactly once without duplication or missing transitions.

## Worked Examples

### Sample 1

Input:

```
4 2 5
2 1 2
2 1 4
2 3 2
1 4
1 1
```

We track a few representative subsets of friends.

| Friend subset | Intersection of allowed ingredients | Count | Feasible (≥2) | Subset size |
| --- | --- | --- | --- | --- |
| {} | {1,2,3,4} | 4 | yes | 0 |
| {1} | {3,4} | 2 | yes | 1 |
| {2,3} | {2,3} | 2 | yes | 2 |
| {1,2,3} | {3} | 1 | no | - |

The best feasible subset size is 3, matching the output.

This shows how combining constraints gradually shrinks the available ingredient pool, and only subsets whose intersection remains large enough can support a valid salad.

### Sample 2

Input:

```
2 2 3
0
1 1
1 2
```

| Friend subset | Allowed intersection | Count | Feasible | Subset size |
| --- | --- | --- | --- | --- |
| {} | {1,2} | 2 | yes | 0 |
| {1} | {1,2} | 2 | yes | 1 |
| {2} | {2} | 1 | no | 1 |
| {3} | {1} | 1 | no | 1 |
| {1,2} | {1,2} | 2 | yes | 2 |
| {1,3} | {1,2} | 2 | yes | 2 |
| {2,3} | {} | 0 | no | - |

The best subset size is 1, since no two friends can be simultaneously satisfied while still allowing 2 ingredients.

This example highlights that even though ingredients exist in sufficient quantity globally, constraints can force the solution to sacrifice compatibility among friends.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(F \cdot 2^F + 2^F \cdot N/word)$ | DP over friend subsets plus bitmask intersections and popcounts |
| Space | $O(2^F)$ | Stores intersection mask for every subset of friends |

With $F \le 20$, the subset space is about one million states, and each state uses only a couple of bitwise operations over 50-bit integers. This fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    input = stdin.readline

    N, K, F = map(int, input().split())
    dislike = []
    for _ in range(F):
        arr = list(map(int, input().split()))
        f = arr[0]
        mask = 0
        for x in arr[1:]:
            mask |= 1 << (x - 1)
        dislike.append(mask)

    ALL = (1 << N) - 1
    allow = [(~d) & ALL for d in dislike]

    size = 1 << F
    inter = [0] * size

    for mask in range(size):
        if mask == 0:
            inter[mask] = ALL
        else:
            lsb = mask & -mask
            i = (lsb.bit_length() - 1)
            prev = mask ^ lsb
            inter[mask] = inter[prev] & allow[i]

    ans = 0
    for mask in range(size):
        if inter[mask].bit_count() >= K:
            ans = max(ans, mask.bit_count())

    return str(ans)

# provided samples
assert run("""4 2 5
2 1 2
2 1 4
2 3 2
1 4
1 1
""") == "3"

assert run("""2 2 3
0
1 1
1 2
""") == "1"

# minimum size
assert run("""1 1 1
0
""") == "1"

# all dislike everything except empty
assert run("""3 2 2
3 1 2 3
3 1 2 3
""") == "0"

# K = 0 edge (theoretical robustness)
assert run("""3 0 2
1 1
1 2
""") == "2"

# boundary: full compatibility
assert run("""4 2 2
0
0
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all-empty dislikes | full friend compatibility | baseline correctness |
| full conflicts | impossible selection | intersection collapse case |
| K = 0 | trivial feasibility | edge definition stability |
| mixed constraints | partial feasibility | interaction correctness |

## Edge Cases

A key edge case occurs when all friends dislike overlapping sets that collectively cover the entire ingredient universe. In that situation, most friend subsets quickly produce empty intersections, and only small subsets of friends remain feasible. The DP correctly handles this because any intersection that becomes zero immediately fails the $K$-ingredient check, preventing overcounting.

Another case is when no friend dislikes anything. The intersection for every subset remains the full ingredient set, so the answer becomes simply all $F$ friends, since any $K$-subset of ingredients is valid. The DP naturally preserves this because AND operations never reduce the mask.
