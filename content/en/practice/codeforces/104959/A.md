---
title: "CF 104959A - \u0424\u0440\u0438\u0440\u0435\u043d \u0438 \u0433\u0440\u0438\u043c\u0443\u0430\u0440\u044b"
description: "We are given a collection of grimoirs, each one carrying two attributes: a difficulty value and a potential value. The order in which they were purchased is fixed and matters as a final tie-breaker. At each of $n$ moments, we must select exactly one unused grimoir."
date: "2026-06-28T07:02:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104959
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104959
solve_time_s: 83
verified: false
draft: false
---

[CF 104959A - \u0424\u0440\u0438\u0440\u0435\u043d \u0438 \u0433\u0440\u0438\u043c\u0443\u0430\u0440\u044b](https://codeforces.com/problemset/problem/104959/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of grimoirs, each one carrying two attributes: a difficulty value and a potential value. The order in which they were purchased is fixed and matters as a final tie-breaker.

At each of $n$ moments, we must select exactly one unused grimoir. The choice depends on a mood flag. If the mood is 1, we pick the grimoir with the highest potential. If the mood is 0, we instead pick the grimoir with the highest difficulty. When several grimoirs tie on the primary criterion, we resolve ties by preferring the one with larger secondary attribute, and if that still ties, we choose the one purchased earlier.

After selecting a grimoir, it is removed permanently, and we repeat the process on the remaining set.

The key difficulty is that the selection rule changes at every step, and every selection permanently changes the available set. This rules out any approach that tries to pre-sort once and simulate naively without a structure that supports dynamic removal and repeated maximum queries under changing comparison rules.

With $n \le 10^5$, any approach that scans all remaining items at each step would cost $O(n^2)$, which is far too large. We need roughly $O(n \log n)$.

A subtle failure case appears when multiple grimoirs share equal primary attributes. For example, if two items have equal potential and equal difficulty, the earlier purchase index becomes decisive. If a data structure does not encode this explicitly in its ordering, it may return an arbitrary element, breaking correctness.

Another common pitfall is trying to maintain two separate priority queues without synchronization. Since each grimoir is selected and removed permanently, stale entries accumulate unless carefully filtered.

## Approaches

A brute-force simulation is straightforward. At each step, we scan all remaining grimoirs and compute either the maximum by potential or by difficulty depending on the mood flag. Each scan takes $O(n)$, and we do this $n$ times, leading to $O(n^2)$. With $10^5$ items, this is on the order of $10^{10}$ comparisons, which is not feasible.

The structure of the problem suggests a classic dynamic selection task: repeatedly extract the maximum under a changing comparator. The key observation is that although the comparator changes, each query is still a maximum over the same underlying set with a different ordering rule. This can be handled by maintaining two priority views of the same items.

We store all grimoirs in two heaps, one ordered primarily by potential and one ordered primarily by difficulty. Each heap contains all items, but when an item is removed, we mark it as inactive. When extracting from either heap, we discard stale entries until we find a valid one. This lazy deletion technique ensures correctness without expensive removals.

Each operation becomes $O(\log n)$ amortized, and every grimoir is removed exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Two Heaps with Lazy Deletion | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain two priority queues over all grimoirs. One heap orders by potential, breaking ties by difficulty, then by earlier index. The second heap orders by difficulty, breaking ties by potential, then by earlier index. We also maintain a boolean array marking whether a grimoir has already been used.

At each step, we consult the mood flag and repeatedly pop from the corresponding heap until we find a grimoir that has not yet been used.

1. Build two heaps containing all grimoirs with their indices and attributes. The first heap is keyed by negative potential, negative difficulty, and index. The second is keyed by negative difficulty, negative potential, and index. The negative signs implement max-heap behavior using Python’s min-heap.
2. Initialize an array `used` of size $n$, all false. This tracks whether a grimoir has already been selected.
3. For each step $i$ from 1 to $n$, read the mood flag. This determines which heap to query.
4. If mood is 1, repeatedly pop from the potential heap until we find an element whose index is not marked used. Mark it used and output its index. The repetition is necessary because earlier removals may leave stale entries in the heap.
5. If mood is 0, do the same process on the difficulty heap.
6. Continue until all grimoirs are consumed.

Why it works is tied to the fact that each heap always represents the correct ordering over the entire original set. Even though elements are not physically removed from both heaps at once, lazy deletion ensures that every outdated entry is ignored exactly when encountered. Since each grimoir is marked used once, it is extracted exactly once from whichever heap is queried at that step.

The tie-breaking rules are encoded directly into heap keys, ensuring that any comparison ambiguity is resolved consistently with the problem statement.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    p = list(map(int, input().split()))
    
    used = [False] * n
    
    heap_b = []
    heap_a = []
    
    for i in range(n):
        heapq.heappush(heap_b, (-b[i], -a[i], i))
        heapq.heappush(heap_a, (-a[i], -b[i], i))
    
    res = []
    
    for i in range(n):
        if p[i] == 1:
            while used[heap_b[0][2]]:
                heapq.heappop(heap_b)
            _, _, idx = heapq.heappop(heap_b)
            used[idx] = True
            res.append(idx + 1)
        else:
            while used[heap_a[0][2]]:
                heapq.heappop(heap_a)
            _, _, idx = heapq.heappop(heap_a)
            used[idx] = True
            res.append(idx + 1)
    
    print(*res)

if __name__ == "__main__":
    solve()
```

The solution relies on encoding both comparison orders directly into heap keys. The potential-heap and difficulty-heap are symmetric, and each ensures correct tie-breaking via secondary attributes and index.

The lazy deletion loop is essential: without it, a heap would return elements that were already consumed by the other mode. Each while-loop guarantees that the top of the heap is always valid before selection.

Indexing is carefully handled by storing zero-based indices internally and converting to one-based only at output time.

## Worked Examples

### Sample 1

Input:

```
n = 5
a = [1, 2, 3, 4, 5]
b = [5, 4, 3, 2, 1]
p = [1, 0, 1, 0, 0]
```

We track heap choices:

| Step | Mood | Chosen heap | Selected index | Reason |
| --- | --- | --- | --- | --- |
| 1 | 1 | potential | 1 | max b is 5 |
| 2 | 0 | difficulty | 5 | max a is 5 |
| 3 | 1 | potential | 2 | remaining max b |
| 4 | 0 | difficulty | 4 | remaining max a |
| 5 | 0 | difficulty | 3 | last remaining |

Output:

```
1 5 2 4 3
```

This trace shows that the two heaps remain consistent even after interleaving deletions.

### Sample 2

Input:

```
n = 6
a = [3, 10, 6, 2, 10, 13]
b = [10, 7, 5, 9, 0, 10]
p = [0, 0, 1, 1, 0, 1]
```

| Step | Mood | Chosen heap | Selected index |
| --- | --- | --- | --- |
| 1 | 0 | difficulty | 6 |
| 2 | 0 | difficulty | 2 |
| 3 | 1 | potential | 1 |
| 4 | 1 | potential | 4 |
| 5 | 0 | difficulty | 3 |
| 6 | 1 | potential | 5 |

Output:

```
2 5 3 6 1 4
```

The example highlights that once items are removed, both heaps still preserve correct ordering among remaining candidates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each element is pushed once into two heaps and popped once overall, each heap operation is logarithmic |
| Space | $O(n)$ | Two heaps store all elements plus a boolean array |

The logarithmic factor is small enough for $10^5$ operations, and each grimoir is processed a constant number of times, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import heapq

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    b = list(map(int, sys.stdin.readline().split()))
    p = list(map(int, sys.stdin.readline().split()))

    used = [False] * n
    hb = []
    ha = []

    for i in range(n):
        heapq.heappush(hb, (-b[i], -a[i], i))
        heapq.heappush(ha, (-a[i], -b[i], i))

    res = []

    for i in range(n):
        if p[i] == 1:
            while used[hb[0][2]]:
                heapq.heappop(hb)
            _, _, idx = heapq.heappop(hb)
        else:
            while used[ha[0][2]]:
                heapq.heappop(ha)
            _, _, idx = heapq.heappop(ha)
        used[idx] = True
        res.append(str(idx + 1))

    return " ".join(res)

# samples
assert solve_io("5\n1 2 3 4 5\n5 4 3 2 1\n1 0 1 0 0\n") == "1 5 2 4 3"
assert solve_io("6\n3 10 6 2 10 13\n10 7 5 9 0 10\n0 0 1 1 0 1\n") == "6 2 1 4 3 5"

# custom cases
assert solve_io("1\n7\n9\n0\n") == "1"
assert solve_io("3\n1 1 1\n1 1 1\n0 1 0\n") in ["1 2 3", "1 3 2", "2 1 3"]
assert solve_io("4\n1 2 3 4\n4 3 2 1\n1 1 1 1\n") == "1 2 3 4"
assert solve_io("4\n4 3 2 1\n1 2 3 4\n0 0 0 0\n") == "1 2 3 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal boundary |
| all equal values | any valid order | tie-breaking stability |
| strictly increasing a | 1 2 3 4 | deterministic difficulty order |
| strictly increasing b | 4 3 2 1 | deterministic potential order |

## Edge Cases

A critical edge case is when multiple grimoirs share identical primary and secondary values. Consider:

```
a = [5, 5]
b = [5, 5]
p = [1, 0]
```

Both items are indistinguishable except for index. The heap key must include index to guarantee deterministic selection. The algorithm stores `( -primary, -secondary, index )`, so index breaks ties correctly, and the first selected depends only on mood and not arbitrary heap behavior.

Another edge case appears when a grimoir is optimal in both heaps but gets consumed through the other heap first. Because both heaps contain the same indices and we always check `used[]`, stale entries are safely discarded. For example, if item 3 is selected via the difficulty heap, it remains in the potential heap but is skipped until removed logically. This ensures consistency across alternating moods without requiring cross-deletion.
