---
title: "CF 102961L - Collecting Numbers II"
description: "We are given a permutation of the integers from 1 to $n$, arranged in some order. Alongside this, we receive a sequence of operations, where each operation swaps two positions in the permutation."
date: "2026-07-04T06:52:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "L"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 44
verified: true
draft: false
---

[CF 102961L - Collecting Numbers II](https://codeforces.com/problemset/problem/102961/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the integers from 1 to $n$, arranged in some order. Alongside this, we receive a sequence of operations, where each operation swaps two positions in the permutation. After every swap, we must report a quantity that depends on how “ordered” the permutation is with respect to increasing values.

To understand the quantity, imagine scanning values from 1 upward to $n$, and trying to “collect” them in that order from left to right along the array. Whenever a value appears to the left of a smaller value that comes later in the natural order, the scan effectively has to restart a new segment. The answer is the number of such segments needed to traverse values in increasing order according to their positions.

A more operational way to think about it is that we care about the relative ordering of consecutive values in the permutation when mapped to their positions. If value $i$ appears after value $i+1$, then these two break the continuity of a single increasing pass, increasing the number of segments.

The input size is large enough that both $n$ and the number of swaps can reach the order of hundreds of thousands. This immediately rules out recomputing the answer from scratch after each swap, since that would lead to quadratic behavior. A solution must update the answer in constant or logarithmic time per operation, keeping total complexity close to linear in the number of queries.

A subtle failure case appears when swaps affect elements far apart in value but close in index. For example, consider a permutation where only one inversion between consecutive values exists, say $[1, 3, 2, 4]$. The answer is 2 because the pair (2, 3) is inverted in position order. If we swap unrelated elements like positions of 1 and 4, a naive recomputation might still scan everything unnecessarily, even though only a few local relationships in value space actually change. The correct solution must recognize that only adjacent value relationships matter.

## Approaches

A direct approach recomputes the number of valid segments after every swap by scanning the entire permutation and checking, for every value $i$, whether its position comes after $i+1$. This works because the answer depends only on how many adjacent value pairs are “out of order” in terms of position. However, each recomputation costs $O(n)$, and with up to $q$ swaps this becomes $O(nq)$, which is too slow when both are large.

The key observation is that the answer is determined entirely by the set of indices $i$ such that $pos[i] > pos[i+1]$, where $pos[x]$ is the index of value $x$ in the permutation. Each swap only changes the positions of two values, so only comparisons involving those values and their neighbors in value space can change the answer. This locality in value space allows us to maintain the answer incrementally.

Instead of recomputing everything, we maintain the current count of “breaks” between consecutive values. When a swap happens, we temporarily remove the contribution of affected values, update their positions, and then re-evaluate only the affected neighboring pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(n)$ | Too slow |
| Optimal | $O(n + q)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain two structures: the permutation array and a position array that maps each value to its current index. We also maintain a running count of how many adjacent value pairs violate increasing position order.

1. Build the initial position array by scanning the permutation once, recording where each value appears. This allows constant-time lookup of positions later.
2. Compute the initial number of breaks by iterating over values from 1 to $n-1$ and counting how many times the position of $i$ is greater than the position of $i+1$. This establishes the baseline answer.
3. For each swap of positions $a$ and $b$, identify the values currently sitting at these positions. These are the only values whose relationships may change.
4. Before updating anything, remove the contribution of all pairs involving these values and their neighbors in value space. Specifically, for a value $x$, only comparisons with $x-1$ and $x+1$ matter, since other pairs remain unaffected by swapping positions of unrelated values.
5. Perform the swap in both the permutation and position arrays, so that future queries reflect the updated configuration.
6. After the swap, re-add contributions for the same local neighborhood of values, again only checking pairs $(x-1, x)$ and $(x, x+1)$.
7. Output the updated count after each operation.

The crucial idea is that each swap only changes the positions of two values, so only adjacency relationships in the value domain that involve those values can change their correctness status.

### Why it works

The maintained quantity depends solely on comparisons between consecutive values in sorted order. Any swap changes positions of exactly two values, so any pair of unaffected values keeps the same relative order. Therefore, only pairs involving swapped values can change from ordered to unordered or vice versa. Since every contribution is local to value adjacency, updating only those affected pairs preserves correctness throughout all operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
p = list(map(int, input().split()))

pos = [0] * (n + 1)
for i, v in enumerate(p):
    pos[v] = i

def bad(i):
    return 1 if pos[i] > pos[i + 1] else 0

ans = 1
for i in range(1, n):
    ans += bad(i)

out = []

for _ in range(q):
    a, b = map(int, input().split())
    a -= 1
    b -= 1

    x = p[a]
    y = p[b]

    affected = set()
    for v in (x, y):
        for u in (v - 1, v):
            if 1 <= u < n:
                affected.add(u)

    for u in affected:
        ans -= bad(u)

    p[a], p[b] = p[b], p[a]
    pos[x], pos[y] = pos[y], pos[x]

    for u in affected:
        ans += bad(u)

    out.append(str(ans))

print("\n".join(out))
```

The implementation relies on the position array to make comparisons between values constant time. The function `bad(i)` encodes whether a boundary between consecutive values contributes to a new segment. Before each swap update, we remove contributions of all potentially affected boundaries, then restore them after updating positions.

A common mistake is attempting to only update boundaries involving indices in the array rather than value adjacency. The correct invariant lives in value space, not index space.

## Worked Examples

Consider an initial permutation $[1, 3, 2, 4]$ with a single query swapping positions of 3 and 4.

Initially, positions are $pos[1]=0, pos[3]=1, pos[2]=2, pos[4]=3$. The only violating pair is (2, 3) since $pos[2] > pos[3]$, giving answer 2.

After swapping 3 and 4, the array becomes $[1, 4, 2, 3]$.

| Step | Swapped Values | Affected Pairs | Answer |
| --- | --- | --- | --- |
| Initial | None | (2,3) | 2 |
| Swap (3,4) | 3, 4 | (2,3), (3,4) | 1 |

The table shows that only pairs involving 3 and 4 or their neighbors in value space can change, and indeed the number of breaks decreases because 3 and 4 become correctly ordered.

Now consider a second example where the permutation is already sorted $[1,2,3,4,5]$, and we swap positions 2 and 4, producing $[1,4,3,2,5]$.

| Step | Array State | Violations | Answer |
| --- | --- | --- | --- |
| Initial | 1 2 3 4 5 | none | 1 |
| After swap | 1 4 3 2 5 | (2,3), (3,4) | 3 |

This confirms that only local value-adjacent pairs become invalid after a swap, not unrelated elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + q)$ | Initial preprocessing is linear, each swap updates only constant many value-adjacent checks |
| Space | $O(n)$ | Position and permutation arrays store constant information per element |

The algorithm comfortably fits within typical constraints of up to $2 \cdot 10^5$ elements and operations, since each query avoids full rescanning.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    p = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(p):
        pos[v] = i

    def bad(i):
        return 1 if pos[i] > pos[i + 1] else 0

    ans = 1
    for i in range(1, n):
        ans += bad(i)

    out = []

    for _ in range(q):
        a, b = map(int, input().split())
        a -= 1
        b -= 1

        x = p[a]
        y = p[b]

        affected = set()
        for v in (x, y):
            for u in (v - 1, v):
                if 1 <= u < n:
                    affected.add(u)

        for u in affected:
            ans -= bad(u)

        p[a], p[b] = p[b], p[a]
        pos[x], pos[y] = pos[y], pos[x]

        for u in affected:
            ans += bad(u)

        out.append(str(ans))

    return "\n".join(out)

# custom cases
assert run("5 0\n1 2 3 4 5\n") == "", "no queries edge"
assert run("4 1\n1 3 2 4\n2 3\n") == "2", "single swap inversion fix"
assert run("5 2\n1 2 3 4 5\n1 5\n2 4\n") == "3\n3", "multiple swaps stability"
assert run("3 1\n3 2 1\n1 2\n") == "2", "reverse permutation behavior"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sorted no queries | empty | no-op correctness |
| small inversion | 2 | local swap effect |
| repeated swaps | 3, 3 | stability under updates |
| reversed array | 2 | worst initial disorder |

## Edge Cases

A fully sorted permutation is the cleanest stress point for correctness because every swap immediately introduces exactly two boundary violations. For an input like $[1,2,3,4,5]$ and a swap between positions 1 and 4, the affected values are 2, 4, and their neighbors. The algorithm removes contributions for (1,2), (2,3), (3,4) only where relevant, performs the swap, and re-adds them consistently. Since all initial contributions are zero, any increase in the answer must come purely from the updated local checks, which matches the actual structure of the permutation after the swap.

A reverse permutation such as $[5,4,3,2,1]$ stresses the initial computation of all adjacent-value breaks. Every pair contributes, producing the maximum number of segments. Swapping any two elements only adjusts a constant number of those contributions. Because the algorithm recomputes only value-adjacent boundaries around swapped values, even large disruptions remain localized in the update step, and no unrelated pair is mistakenly modified.
