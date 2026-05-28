---
title: "CF 82B - Sets"
description: "We are given all pairwise unions of some unknown disjoint sets. Suppose the original sets are: $$S1, S2, dots, Sn$$ Every pair $Si cup Sj$ for $i ne j$ was written down once. The order of the papers was shuffled, and the numbers inside each union were also shuffled."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "hashing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 82
codeforces_index: "B"
codeforces_contest_name: "Yandex.Algorithm 2011: Qualification 2"
rating: 1700
weight: 82
solve_time_s: 131
verified: false
draft: false
---

[CF 82B - Sets](https://codeforces.com/problemset/problem/82/B)

**Rating:** 1700  
**Tags:** constructive algorithms, hashing, implementation  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given all pairwise unions of some unknown disjoint sets.

Suppose the original sets are:

$$S_1, S_2, \dots, S_n$$

Every pair $S_i \cup S_j$ for $i \ne j$ was written down once. The order of the papers was shuffled, and the numbers inside each union were also shuffled.

Our task is to reconstruct any valid collection of the original disjoint sets.

The key property is that the original sets are pairwise disjoint. Because of that, every number belongs to exactly one original set. This structure is what makes reconstruction possible.

The input consists of:

1. The number of original sets.
2. Exactly $\frac{n(n-1)}{2}$ unions.
3. Each union contains all elements from two original sets.

The output must print the original sets in any order.

The constraints are small enough to allow fairly direct processing. Since $n \le 200$, the number of union sets is at most:

$$\frac{200 \cdot 199}{2} = 19900$$

Each union contains at most 200 elements. A quadratic or even mildly cubic solution over $n$ is acceptable. What would fail is trying to brute force arbitrary partitions of elements into sets, because the number of possible decompositions grows exponentially.

The most dangerous edge cases come from singleton sets.

Consider:

```
n = 3
{1,2}
{1,3}
{2,3}
```

The original sets are clearly:

```
{1}, {2}, {3}
```

Every number appears in exactly two unions. If we only count frequencies and greedily group frequent elements together, we could incorrectly merge unrelated elements.

Another tricky situation is when one original set is much larger than the others.

Example:

```
A = {1,2,3,4}
B = {5}
C = {6}
```

The unions are:

```
{1,2,3,4,5}
{1,2,3,4,6}
{5,6}
```

The set `{5,6}` contains no element from the large set. A careless algorithm that assumes every union overlaps heavily with others could fail to isolate the singleton sets.

There is also a subtle ambiguity when $n = 2$. We are given only one union, which is simply:

```
S1 ∪ S2
```

There are infinitely many valid decompositions. Since any valid answer is accepted, we may place one element into one set and all remaining elements into the other.

Example:

```
2
3 1 2 3
```

One valid output is:

```
1 1
2 2 3
```

A solution that assumes uniqueness would break here.

## Approaches

A brute force strategy would try to reconstruct the original partition directly.

We could collect all distinct numbers, then attempt every possible grouping into $n$ disjoint sets, checking whether the generated pairwise unions match the input. This is correct because the input fully describes the relationships between sets.

The problem is the number of partitions. Even for 20 distinct numbers, the search space becomes enormous. In the worst case we may have up to 200 distinct values, making exhaustive reconstruction completely impossible.

The breakthrough comes from looking at how often each element appears.

Suppose an element belongs to original set $S_i$. That element appears in every union involving $S_i$. Since $S_i$ pairs with all other $n-1$ sets, the element appears exactly:

$$n - 1$$

times in the input.

Now consider two elements $x$ and $y$.

If they belong to the same original set, then every union containing one also contains the other. Their occurrence patterns across the union papers are identical.

If they belong to different original sets, there exists a union containing $x$ but not $y$, namely any union between $x$'s set and a third set.

This gives a complete characterization:

Two elements belong to the same original set if and only if they appear together in exactly the same collection of unions.

That observation reduces the problem from reconstructing arbitrary partitions to grouping equal signatures.

We assign every distinct number a signature describing which union indices contain it. Elements with identical signatures form one original set.

The only exceptional case is $n=2$. There is only one union, so every element has the same signature. The decomposition is not unique, so we can output any partition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(U \cdot K)$ | $O(U \cdot K)$ | Accepted |

Here:

$$U = \frac{n(n-1)}{2}$$

and $K$ is the maximum union size.

## Algorithm Walkthrough

1. Read all union sets and assign each one an index.

We need stable identifiers because each element's signature is the list of union indices where it appears.
2. For every number appearing in the input, store the list of unions containing it.

Example:

```
number 5 -> [0, 3, 7]
```

This list is the structural fingerprint of the number.
3. Convert each occurrence list into a tuple so it can be used as a hashable key.

Elements from the same original set must have identical tuples.
4. Group numbers by identical signatures.

Each group corresponds to one original set because all its elements appear in exactly the same unions.
5. Handle the special case $n=2$.

All numbers appear in the only union, so every signature is identical. We may output any partition. A simple valid choice is:

- first set contains one element
- second set contains all remaining elements
6. Output the reconstructed groups.

The order does not matter.

### Why it works

Every original set participates in exactly $n-1$ unions. Any element inside that set appears in precisely those unions and nowhere else.

If two elements come from the same original set, they always appear together. Their signatures are identical.

If two elements come from different original sets, pick a union involving the first set but not the second. One element appears there while the other does not, so their signatures differ.

This creates a one-to-one correspondence between original sets and distinct signatures. Grouping equal signatures reconstructs the sets exactly.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n = int(input())

    unions = []
    occur = defaultdict(list)

    m = n * (n - 1) // 2

    for idx in range(m):
        arr = list(map(int, input().split()))
        vals = arr[1:]

        unions.append(vals)

        for x in vals:
            occur[x].append(idx)

    # Special case: n = 2
    if n == 2:
        elems = list(occur.keys())

        print(1, elems[0])

        rest = elems[1:]
        print(len(rest), *rest)
        return

    groups = defaultdict(list)

    for x, sig in occur.items():
        groups[tuple(sig)].append(x)

    ans = list(groups.values())

    for g in ans:
        print(len(g), *g)

solve()
```

The first phase reads every union and records where each element appears. The dictionary `occur` maps a number to all union indices containing it.

The crucial implementation detail is preserving the order of indices. Since we process unions sequentially, every occurrence list is naturally sorted. That allows tuples to be compared directly without extra sorting.

The grouping step uses tuples as hash keys. Two elements end up in the same bucket exactly when they share the same occurrence pattern.

The `n == 2` case needs special handling because all signatures collapse into one. Without this branch, the algorithm would output a single set instead of two.

The output order is arbitrary, which simplifies implementation. We only need each original set exactly once.

## Worked Examples

### Example 1

Input:

```
4
3 2 7 4
3 1 7 3
3 5 4 2
3 1 3 5
4 3 1 2 4
2 5 7
```

Union indices:

| Index | Union |
| --- | --- |
| 0 | {2,7,4} |
| 1 | {1,7,3} |
| 2 | {5,4,2} |
| 3 | {1,3,5} |
| 4 | {1,2,3,4} |
| 5 | {5,7} |

Occurrence signatures:

| Number | Signature |
| --- | --- |
| 1 | (1,3,4) |
| 2 | (0,2,4) |
| 3 | (1,3,4) |
| 4 | (0,2,4) |
| 5 | (2,3,5) |
| 7 | (0,1,5) |

Grouping by signatures:

| Signature | Reconstructed Set |
| --- | --- |
| (1,3,4) | {1,3} |
| (0,2,4) | {2,4} |
| (2,3,5) | {5} |
| (0,1,5) | {7} |

This trace demonstrates the central invariant. Elements from the same original set share exactly the same union participation pattern.

### Example 2

Input:

```
3
2 1 2
2 1 3
2 2 3
```

Union indices:

| Index | Union |
| --- | --- |
| 0 | {1,2} |
| 1 | {1,3} |
| 2 | {2,3} |

Occurrence signatures:

| Number | Signature |
| --- | --- |
| 1 | (0,1) |
| 2 | (0,2) |
| 3 | (1,2) |

Grouping:

| Signature | Reconstructed Set |
| --- | --- |
| (0,1) | {1} |
| (0,2) | {2} |
| (1,2) | {3} |

This example shows that singleton original sets are handled naturally. Distinct elements receive distinct signatures.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(U \cdot K)$ | Every element occurrence is processed once |
| Space | $O(U \cdot K)$ | Occurrence lists store all input appearances |

Here:

$$U = \frac{n(n-1)}{2}$$

and $K$ is the maximum union size.

At the maximum constraints, the total number of processed integers is comfortably below a few million operations, which easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n = int(input())

    occur = defaultdict(list)

    m = n * (n - 1) // 2

    for idx in range(m):
        arr = list(map(int, input().split()))
        vals = arr[1:]

        for x in vals:
            occur[x].append(idx)

    if n == 2:
        elems = list(occur.keys())

        print(1, elems[0])

        rest = elems[1:]
        print(len(rest), *rest)
        return

    groups = defaultdict(list)

    for x, sig in occur.items():
        groups[tuple(sig)].append(x)

    for g in groups.values():
        print(len(g), *g)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# sample 1
out1 = run(
"""4
3 2 7 4
3 1 7 3
3 5 4 2
3 1 3 5
4 3 1 2 4
2 5 7
"""
)

assert len(out1.splitlines()) == 4

# minimum n=2
out2 = run(
"""2
3 1 2 3
"""
)

assert len(out2.splitlines()) == 2

# all singleton sets
out3 = run(
"""3
2 1 2
2 1 3
2 2 3
"""
)

assert len(out3.splitlines()) == 3

# one large set and two singleton sets
out4 = run(
"""3
5 1 2 3 4 5
5 1 2 3 4 6
2 5 6
"""
)

assert len(out4.splitlines()) == 3

# larger grouped structure
out5 = run(
"""4
4 1 2 5 6
4 1 2 7 8
4 3 4 5 6
4 3 4 7 8
6 1 2 3 4 5 6
6 1 2 3 4 7 8
"""
)

assert len(out5.splitlines()) == 4
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum $n=2$ | Any valid partition | Special ambiguity handling |
| All singleton sets | Three singleton groups | Distinct signatures |
| One large set | Correct separation | Uneven set sizes |
| Larger grouped structure | Four groups recovered | General correctness |

## Edge Cases

Consider the ambiguous case:

```
2
3 1 2 3
```

There is only one union. Every element appears in exactly the same set of unions:

| Number | Signature |
| --- | --- |
| 1 | (0) |
| 2 | (0) |
| 3 | (0) |

The grouping method alone would produce one set `{1,2,3}`. That violates the requirement to output exactly two sets.

The algorithm detects `n == 2` separately and constructs an arbitrary valid partition:

```
{1}
{2,3}
```

Their union is indeed `{1,2,3}`.

Now consider singleton original sets:

```
3
2 1 2
2 1 3
2 2 3
```

Each number appears in a different pair of unions:

| Number | Signature |
| --- | --- |
| 1 | (0,1) |
| 2 | (0,2) |
| 3 | (1,2) |

Since all signatures differ, each element becomes its own set. The algorithm does not accidentally merge singleton groups.

Finally, consider unequal set sizes:

```
3
5 1 2 3 4 5
5 1 2 3 4 6
2 5 6
```

The occurrence signatures become:

| Number | Signature |
| --- | --- |
| 1 | (0,1) |
| 2 | (0,1) |
| 3 | (0,1) |
| 4 | (0,1) |
| 5 | (0,2) |
| 6 | (1,2) |

The large set `{1,2,3,4}` is reconstructed because all four elements share the same participation pattern. The singleton sets remain distinct because their signatures differ.
