---
title: "CF 105002E - \u041c\u0435\u0433\u0430\u041f\u043e\u043a\u0435\u0440"
description: "We are given a sequence of cards arranged in a fixed order. Each card carries an integer value between 1 and m. We are allowed to delete any subset of cards, but we cannot reorder the remaining ones."
date: "2026-06-28T03:18:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105002
codeforces_index: "E"
codeforces_contest_name: "vkoshp.letovo 2022"
rating: 0
weight: 105002
solve_time_s: 66
verified: true
draft: false
---

[CF 105002E - \u041c\u0435\u0433\u0430\u041f\u043e\u043a\u0435\u0440](https://codeforces.com/problemset/problem/105002/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of cards arranged in a fixed order. Each card carries an integer value between 1 and m. We are allowed to delete any subset of cards, but we cannot reorder the remaining ones. After deletions, we want the remaining sequence to form a strictly increasing-by-one chain, meaning every adjacent pair differs exactly by one.

So the task is to pick a subsequence that looks like x, x+1, x+2, and so on, while preserving original order, and maximize how many cards remain.

The key point is that we are not choosing arbitrary cards, we are choosing a subsequence that behaves like a continuous integer run.

The constraint n ≤ 100000 rules out any solution that tries all subsequences or even tries every starting point and greedily extends it with nested scans. Anything quadratic or worse will time out. We need something close to linear or n log n.

A subtle edge case appears when values repeat or when there are multiple candidate chains overlapping. For example, if the array is 1 2 1 2 3, we might be tempted to think we can extend many chains, but only subsequences respecting order and exact +1 transitions matter, so we must carefully track feasibility rather than just frequency.

Another tricky case is when the best chain is not aligned with the first occurrence of its starting value. For instance, in 2 3 2 1 4, starting from the first 2 is worse than starting from the later 2 for building a longer consecutive run.

## Approaches

A brute-force interpretation is to try every starting position i, treat a[i] as the beginning of a chain, and greedily scan to the right collecting a[i], a[i]+1, a[i]+2, and so on. For each start, we would maintain a pointer and repeatedly scan forward to find the next required value. This works correctly because any valid subsequence must pick elements in order, and greedily taking the earliest possible occurrence preserves feasibility.

However, this approach repeatedly scans the array. In the worst case, for each of n starting positions we may scan up to n elements, giving O(n²). With n up to 100000, this is around 10¹⁰ operations, which is not viable.

The structural observation is that once we fix a starting value x, the problem reduces to repeatedly finding the next occurrence of x+1 after a chosen position. If we can answer “next occurrence of value v after index p” quickly, we can simulate each chain efficiently. This suggests preprocessing positions of each value and using binary search.

We store, for each value, a sorted list of indices where it appears. Then, for a given start position i with value x, we walk forward by repeatedly jumping to the first occurrence of x+1 that appears after our current index. Each jump costs O(log k) via binary search, and we perform at most m steps, but in practice only along existing consecutive values.

This reduces the problem to scanning only feasible chains rather than the whole array repeatedly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Position lists + binary search | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a mapping from each value v to the list of indices where v appears in the array.

This allows us to quickly locate occurrences of any value in sorted order.
2. Iterate over every index i in the array and treat it as a potential starting point.

We attempt to build the longest valid consecutive subsequence starting at a[i].
3. Let current value be a[i] and current position be i. Initialize length to 1.
4. Repeatedly try to extend the chain to value current value + 1.

We search in the list of positions for that value and find the smallest index strictly greater than the current position using binary search.
5. If such an index exists, move to it, increment the chain length, and continue.

If it does not exist, the chain stops.
6. Track the maximum chain length over all starting positions.

Each step ensures we are always respecting the original ordering while only selecting strictly consecutive values.

### Why it works

For any valid solution, the subsequence must be anchored at some starting occurrence of a value v. From that point onward, every next element must be the first available occurrence of v+1 after the previous pick; choosing anything later only reduces future options. Therefore, the greedy jump to the earliest valid next occurrence does not reduce optimality. Since every starting index is considered, we do not miss any possible chain.

## Python Solution

```python
import sys
input = sys.stdin.readline

from bisect import bisect_right

n, m = map(int, input().split())
a = list(map(int, input().split()))

pos = [[] for _ in range(m + 2)]
for i, v in enumerate(a):
    pos[v].append(i)

ans = 1

for i in range(n):
    v = a[i]
    cur_idx = i
    length = 1

    while v + 1 <= m:
        lst = pos[v + 1]
        if not lst:
            break
        j = bisect_right(lst, cur_idx)
        if j == len(lst):
            break
        cur_idx = lst[j]
        v += 1
        length += 1

    if length > ans:
        ans = length

print(ans)
```

The solution relies on preprocessing positions so that every “next step” query becomes a binary search. The outer loop tries every possible starting index, because the best chain might begin at any occurrence of any value. The inner loop walks forward through consecutive values, always jumping to the earliest feasible occurrence.

The use of bisect_right is essential because we must ensure strict forward movement in indices; equality is not allowed since we cannot reuse the same card.

## Worked Examples

### Sample 1

Input:

```
5 4
2 3 2 1 4
```

We build position lists:

| Value | Positions |
| --- | --- |
| 1 | [3] |
| 2 | [0, 2] |
| 3 | [1] |
| 4 | [4] |

Now we trace key starting points.

Starting at index 0 (value 2):

| Step | Value | Current Index | Next position found | Length |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | start | 1 |
| 2 | 3 | 0 | 1 | 2 |
| 3 | 4 | 1 | 4 | 3 |
| 4 | 5 | 4 | stop | 3 |

Best from this start is 3.

Starting at index 3 (value 1):

| Step | Value | Current Index | Next position found | Length |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | start | 1 |
| 2 | 2 | 3 | no occurrence after 3 | 1 |

So maximum remains 3.

This confirms that the optimal chain is 2 → 3 → 4.

### Sample 2

Input:

```
7 10
1 2 3 4 7 8 9
```

Position lists:

| Value | Positions |
| --- | --- |
| 1 | [0] |
| 2 | [1] |
| 3 | [2] |
| 4 | [3] |
| 7 | [4] |
| 8 | [5] |
| 9 | [6] |

Starting from 1:

| Step | Value | Index | Next | Length |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | start | 1 |
| 2 | 2 | 0 | 1 | 2 |
| 3 | 3 | 1 | 2 | 3 |
| 4 | 4 | 2 | 3 | 4 |
| 5 | 5 | 3 | stop | 4 |

Starting from 7 gives a shorter chain of length 3. So answer is 4.

This shows the algorithm correctly handles gaps in values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each index can be a starting point, and each step uses binary search over position lists |
| Space | O(n) | We store index lists for all values appearing in the array |

The constraints allow up to 100000 elements, so an n log n solution is comfortably within limits. Memory usage is linear in array size and value occurrences, which also fits easily.

## Test Cases

```python
import sys, io
from bisect import bisect_right

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    pos = [[] for _ in range(m + 2)]
    for i, v in enumerate(a):
        pos[v].append(i)

    ans = 1

    for i in range(n):
        v = a[i]
        cur = i
        length = 1
        while v + 1 <= m:
            lst = pos[v + 1]
            if not lst:
                break
            j = bisect_right(lst, cur)
            if j == len(lst):
                break
            cur = lst[j]
            v += 1
            length += 1
        ans = max(ans, length)

    return str(ans)

# provided samples
assert solve("5 4\n2 3 2 1 4\n") == "3"
assert solve("7 10\n1 2 3 4 7 8 9\n") == "4"
assert solve("3 8\n3 2 1\n") == "1"

# custom cases
assert solve("1 5\n3\n") == "1", "single element"
assert solve("5 5\n1 1 1 1 1\n") == "1", "all equal"
assert solve("6 6\n1 3 2 4 5 6\n") == "4", "interleaving but valid chain"
assert solve("8 8\n8 7 6 5 4 3 2 1\n") == "1", "strictly decreasing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimum size correctness |
| all equal | 1 | no consecutive transitions possible |
| interleaving but valid chain | 4 | order-sensitive construction |
| strictly decreasing | 1 | worst ordering for chaining |

## Edge Cases

A key edge case is when multiple occurrences of a needed value exist, but only later ones allow continuation. For example, in 1 2 1 2 3, starting from the first 2 might force a dead end, while starting from the second 2 enables reaching 3. The algorithm handles this because every occurrence is considered as a starting point, and the binary search always picks the first valid next occurrence after the current position.

Another case is when values are missing in the middle of the sequence. If 1 and 3 exist but 2 does not, no chain longer than 1 can form. In this situation, the position list for 2 is empty, and the algorithm immediately stops extension, correctly preventing false chaining through gaps.

A final subtle case is repeated values clustered in order, such as 1 1 1 2 2 3. The algorithm always jumps forward in index space, so it avoids reusing earlier duplicates and still finds the maximum achievable chain 1 → 2 → 3 with length 3.
