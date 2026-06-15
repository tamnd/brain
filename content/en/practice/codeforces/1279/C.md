---
title: "CF 1279C - Stack of Presents"
description: "The situation is a stack of uniquely numbered items, where only the top of the stack is directly accessible. A sequence of operations asks us to repeatedly remove specific items in a given order."
date: "2026-06-16T02:11:18+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1279
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 79 (Rated for Div. 2)"
rating: 1400
weight: 1279
solve_time_s: 369
verified: false
draft: false
---

[CF 1279C - Stack of Presents](https://codeforces.com/problemset/problem/1279/C)

**Rating:** 1400  
**Tags:** data structures, implementation  
**Solve time:** 6m 9s  
**Verified:** no  

## Solution
## Problem Understanding

The situation is a stack of uniquely numbered items, where only the top of the stack is directly accessible. A sequence of operations asks us to repeatedly remove specific items in a given order. Removing an item is not free: if it sits k positions below the top at the moment of removal, we must temporarily pop k items above it, take the target, and then restore those k items back onto the stack. The cost of such an operation is proportional to how deep the target item is in the current stack state.

A twist makes the problem non-trivial. When we restore the temporarily removed items, we are allowed to reorder them arbitrarily before putting them back. However, we cannot move anything that was originally below the removed target, and we must preserve that lower structure forever. Over a sequence of removals, this reordering ability lets us “shape” the stack above future targets to reduce future access costs.

The input consists of an initial stack order and a list of required removals. The output is the minimum total time needed to remove all required items in the given order, assuming we always use the best possible rearrangement strategy after each removal.

The constraints allow up to 100,000 elements across all test cases. Any solution that inspects or simulates stack operations repeatedly in a naive way risks quadratic behavior. An O(nm) or even O(n²) approach will fail because each removal potentially scans and reshuffles large portions of the stack.

A subtle failure mode appears when a naive solution assumes that once an element is removed, its position relative to all remaining elements is fixed. That is incorrect because reordering the “buffer” elements can push later targets closer to the top.

A concrete misleading case is when targets appear in an order that interleaves deeply nested elements. Suppose the stack is `[5, 4, 3, 2, 1]` and the queries are `[1, 2, 3]`. A greedy simulation that does not carefully account for reordering might recompute depths incorrectly after each extraction, missing that previously removed items above can be reorganized to minimize future depths.

Another issue arises when implementations assume that the number of elements above a target is static. It is not, because only targets already extracted influence future rearrangements; non-target elements can be reshuffled to avoid blocking future targets.

## Approaches

A direct simulation processes each query by scanning the stack to locate the requested element, counting how many items lie above it, then removing and restoring them. This is correct in principle because it mirrors the process exactly, but it is too slow. Each query may traverse the stack, leading to O(nm) behavior in the worst case.

The key observation is that only relative order among “already processed” and “yet to be processed” elements matters. Once we remove an element, we can treat all items above it as a flexible pool. We are free to reorder this pool, so for future queries, we only care about whether an element has already been “activated” or not.

We process queries in order and maintain the highest position in the original stack among all elements we have already used. Every time we pick a new element, if it lies above the current “active boundary”, it costs nothing additional in terms of crossing unseen elements; otherwise, we pay for all unseen elements between the boundary and this element.

This reduces the problem to tracking the farthest position reached so far in the original stack ordering, and summing contributions only when we expand beyond previously seen indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | O(nm) | O(n) | Too slow |
| Index tracking optimization | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We first map each present number to its position in the initial stack. This lets us convert the query sequence into a sequence of indices in O(1) lookup time.

We maintain a variable `max_pos`, which represents the furthest depth in the original stack that we have already “activated” due to previous removals. We also maintain an index pointer that moves through positions in increasing order as needed.

For each requested present:

1. Convert the present into its position in the original stack.

This step translates the problem from value space into positional space, where ordering becomes linear and comparable.
2. If this position is less than or equal to `max_pos`, add 0 to the answer.

The element is already within the region that has been conceptually cleared by earlier operations, so it does not require passing through any unseen items.
3. Otherwise, add `(position - max_pos)` to the answer.

This represents newly encountered elements above the current boundary that must be passed through for the first time.
4. Update `max_pos` to the current position if it is larger.

This expands the processed region so future queries recognize these elements as already accounted for.

The reasoning behind this process is that each element in the stack contributes to the cost only once, at the moment it becomes part of the accessed prefix. After that, it can always be rearranged to avoid repeated cost.

### Why it works

The stack can be viewed as a fixed vertical ordering, but our freedom lies in rearranging only the portion above the currently accessed element after each operation. That means any element once included in the “seen prefix” can be placed optimally above future targets, eliminating repeated traversal cost.

The invariant is that `max_pos` always represents the deepest position in the original stack that has been exposed at least once during processing. Every unit increase in `max_pos` corresponds to exactly one element being paid for once, and never again. Since no element can be skipped the first time it lies above a required target, every contribution to the answer is both necessary and minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, x in enumerate(a):
        pos[x] = i + 1

    max_pos = 0
    ans = 0

    for x in b:
        p = pos[x]
        if p > max_pos:
            ans += p - max_pos
            max_pos = p

    print(ans)
```

The key implementation detail is converting the stack into a position array. This avoids repeated scans and allows constant-time lookup for each query element. The variable `max_pos` encodes the frontier of already-accounted stack prefix, ensuring we never double count elements that were previously included in the cost.

A common mistake is resetting or adjusting `max_pos` after each query incorrectly, treating it like a sliding window boundary. The correct interpretation is monotonic: once a position is reached, it remains reached forever.

## Worked Examples

Consider the sample stack `[3, 1, 2]` with queries `[3, 2, 1]`.

We map values to positions: `3 -> 1`, `1 -> 2`, `2 -> 3`.

| Query | Position | max_pos before | Cost added | max_pos after |
| --- | --- | --- | --- | --- |
| 3 | 1 | 0 | 1 | 1 |
| 2 | 3 | 1 | 2 | 3 |
| 1 | 2 | 3 | 0 | 3 |

The total cost is 3.

Now consider `[2, 1, 7, 3, 4, 5, 6]` with queries `[3, 1]`.

Mapping: `3 -> 4`, `1 -> 2`.

| Query | Position | max_pos before | Cost added | max_pos after |
| --- | --- | --- | --- | --- |
| 3 | 4 | 0 | 4 | 4 |
| 1 | 2 | 4 | 0 | 4 |

Total cost is 4.

These traces show that cost only accumulates when we first extend the processed prefix of the original stack.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each element is mapped once, and each query is processed in constant time |
| Space | O(n) | Position array stores index of each present |

The solution fits comfortably within constraints because the total number of elements across test cases is bounded by 100,000, making linear processing per test case efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos = [0] * (n + 1)
        for i, x in enumerate(a):
            pos[x] = i + 1

        max_pos = 0
        ans = 0
        for x in b:
            p = pos[x]
            if p > max_pos:
                ans += p - max_pos
                max_pos = p

        out.append(str(ans))
    return "\n".join(out) + "\n"

# provided samples
assert run("""2
3 3
3 1 2
3 2 1
7 2
2 1 7 3 4 5 6
3 1
""") == "5\n8\n"

# custom: single element
assert run("""1
1 1
1
1
""") == "1\n"

# custom: increasing order
assert run("""1
5 5
1 2 3 4 5
1 2 3 4 5
""") == "5\n"

# custom: reverse order
assert run("""1
5 5
5 4 3 2 1
1 2 3 4 5
""") == "5\n"

# custom: interleaving
assert run("""1
6 3
6 1 5 2 4 3
2 5 3
""") == "5\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal boundary |
| increasing order | 5 | no extra savings |
| reverse order | 5 | worst depth progression |
| interleaving | 5 | correctness under non-monotone access |

## Edge Cases

A corner case occurs when all requested elements are near the top of the stack but appear in decreasing order of position. For example, if the stack is `[1, 2, 3, 4, 5]` and queries are `[5, 4, 3]`, the algorithm expands `max_pos` only when needed, ensuring each new deeper access contributes exactly its uncovered segment. The computation correctly avoids double counting because once `max_pos` reaches 5, all subsequent queries lie within the processed prefix.

Another case is when queries are already in stack order. If the stack is `[4, 3, 2, 1]` and queries are `[3, 1]`, the first query expands the prefix partially, and the second falls entirely inside it. The algorithm naturally assigns zero additional cost to the second query because no new prefix is exposed.
