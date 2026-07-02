---
title: "CF 103666F - \u041c\u0430\u0448\u0430 \u0438 \u043c\u0430\u0442\u0440\u0451\u0448\u043a\u0438"
description: "We are given a collection of matryoshka dolls, each with a numeric size. A doll can be placed inside another doll only if its size is strictly smaller. Each doll can contain at most one other doll directly, so the structure we build is a chain rather than a branching structure."
date: "2026-07-03T02:29:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103666
codeforces_index: "F"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2016"
rating: 0
weight: 103666
solve_time_s: 41
verified: true
draft: false
---

[CF 103666F - \u041c\u0430\u0448\u0430 \u0438 \u043c\u0430\u0442\u0440\u0451\u0448\u043a\u0438](https://codeforces.com/problemset/problem/103666/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of matryoshka dolls, each with a numeric size. A doll can be placed inside another doll only if its size is strictly smaller. Each doll can contain at most one other doll directly, so the structure we build is a chain rather than a branching structure.

The task is to discard some dolls so that the remaining ones can be arranged into a single nesting sequence, where each doll fits inside the next one. We want to maximize how many dolls remain in such a sequence.

Rephrased, this is asking for the longest strictly increasing sequence of numbers, where we are allowed to reorder the chosen elements arbitrarily because we can choose any nesting order as long as sizes strictly increase along the chain.

The input size is up to 1000 dolls, and sizes are up to 10000. This immediately suggests that an O(n^2) solution is acceptable, while anything cubic would also still pass but is unnecessary. An O(n log n) solution is also possible but not required.

A subtle point is that we are not restricted to preserving the original order. If someone mistakenly treats the input as a sequence and tries to find a longest increasing subsequence, they may undercount. Here we are free to reorder, so only the multiset of values matters.

A second edge case arises from equal sizes. Since nesting requires strict inequality, equal elements cannot be placed consecutively. For example, input `3 3 3 3` should produce `1`, not `4`, because only one of them can be chosen in any strictly increasing chain.

## Approaches

A naive interpretation is to think about building a chain by trying every possible ordering of selected dolls and checking whether it forms a valid strictly increasing sequence. This quickly becomes factorial in complexity because we would be permuting subsets and verifying constraints, which is impossible beyond very small n.

Another brute-force idea is to try every subset and then check whether it can be sorted into a strictly increasing sequence. That reduces the problem to checking whether all values in the subset are distinct, since sorting any subset gives a valid nesting if and only if no duplicates exist. This observation already simplifies the problem significantly.

The key insight is that order is irrelevant. Once we sort all sizes, any valid nesting corresponds to picking a subsequence of strictly increasing values. Since sorting removes permutation concerns, we only need to count how many distinct values we can chain, but we must also consider multiplicities correctly in a more general DP framing.

A clean way to see it is to sort the array and compute the longest strictly increasing subsequence. Because sorting destroys original structure, the LIS becomes trivial: equal values cannot extend sequences, and increasing values can always extend. In a sorted array, the best we can do is pick one representative from each distinct value, but this is not always sufficient if we interpret LIS incorrectly. The correct interpretation is still LIS on the original array, but since we are free to reorder, we can sort first and reduce the problem to grouping equal values.

Thus the solution reduces to counting how many times we can pick values such that each next value is strictly larger, which is equivalent to the number of distinct values in the multiset.

However, there is a more careful perspective: if we sort and compress duplicates, the longest chain is exactly the number of unique values.

The brute force works by exploring all subsets and permutations, but fails because it repeats the same feasibility checks exponentially. The observation that only ordering by value matters reduces the problem to deduplication after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets and permutations | O(n! · n) | O(n) | Too slow |
| Sort + count distinct values | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the list of doll sizes.
2. Sort the list in non-decreasing order. Sorting ensures that any valid nesting sequence must appear as a strictly increasing subsequence in this order.
3. Initialize a counter for the answer. Start by counting the first element if it exists.
4. Scan through the sorted array from left to right.
5. Each time we see a value strictly greater than the previous value, increase the counter. This step ensures we only extend the nesting chain when a strictly larger doll is available.
6. The final counter value is the maximum number of dolls that can be nested.

### Why it works

After sorting, any valid nesting chain must correspond to selecting a sequence of indices with strictly increasing values. Since equal values cannot be adjacent in such a chain, each distinct value can contribute at most one element. Conversely, picking one representative from each distinct value in increasing order always forms a valid nesting sequence. This establishes that the optimal solution is exactly the number of distinct values in the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()

if n == 0:
    print(0)
    sys.exit()

cnt = 1
for i in range(1, n):
    if a[i] > a[i - 1]:
        cnt += 1

print(cnt)
```

The solution starts by sorting the array so that all equal values become adjacent. We initialize the answer as 1 because a non-empty array always allows at least one doll in the chain. Then we scan linearly and only increment the answer when we encounter a strictly larger value than the previous one. This guarantees that duplicates are ignored, since they cannot extend a strictly increasing chain.

A common mistake here is to use `>=` instead of `>`, which would incorrectly allow equal sizes to extend the chain. Another subtle issue is forgetting the empty input case, though the constraints guarantee at least one element.

## Worked Examples

### Example 1

Input:

```
5
2 1 2 1 3
```

Sorted array:

```
1 1 2 2 3
```

| i | a[i] | previous | a[i] > previous | cnt |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | start | 1 |
| 1 | 1 | 1 | no | 1 |
| 2 | 2 | 1 | yes | 2 |
| 3 | 2 | 2 | no | 2 |
| 4 | 3 | 2 | yes | 3 |

This shows that only distinct transitions contribute, confirming that duplicates do not increase nesting length.

### Example 2

Input:

```
6
4 4 4 3 3 2
```

Sorted array:

```
2 3 3 4 4 4
```

| i | a[i] | previous | a[i] > previous | cnt |
| --- | --- | --- | --- | --- |
| 0 | 2 | - | start | 1 |
| 1 | 3 | 2 | yes | 2 |
| 2 | 3 | 3 | no | 2 |
| 3 | 4 | 3 | yes | 3 |
| 4 | 4 | 4 | no | 3 |
| 5 | 4 | 4 | no | 3 |

The trace confirms that repeated sizes contribute only once, and strictly increasing jumps define the chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | dominated by sorting |
| Space | O(1) auxiliary | only a few counters beyond input storage |

The constraints n ≤ 1000 make this comfortably fast. Even with multiple test cases, the solution remains well within limits due to the small input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    return _sys.stdout.getvalue()

def solve(inp: str) -> str:
    import sys
    from io import StringIO
    sys.stdin = StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    cnt = 1 if n > 0 else 0
    for i in range(1, n):
        if a[i] > a[i - 1]:
            cnt += 1
    return str(cnt)

# provided samples (illustrative; actual sample outputs not fully specified in statement text)
assert solve("5\n2 1 2 1 3\n") == "3"
assert solve("6\n4 4 4 3 3 2\n") == "3"

# custom cases
assert solve("1\n10\n") == "1", "single element"
assert solve("4\n1 1 1 1\n") == "1", "all equal"
assert solve("5\n5 4 3 2 1\n") == "5", "strictly decreasing becomes full chain after sort"
assert solve("6\n1 2 2 3 3 4\n") == "4", "mixed duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal case |
| all equal | 1 | strict inequality handling |
| decreasing sequence | 5 | sorting correctness |
| mixed duplicates | 4 | duplicate compression |

## Edge Cases

A key edge case is when all values are equal. For input:

```
4
7 7 7 7
```

Sorting yields the same sequence. The algorithm starts with cnt = 1, and no later element is strictly greater than the previous one, so the result stays 1. This matches the fact that only one doll can be chosen.

Another edge case is strictly decreasing input:

```
5
5 4 3 2 1
```

After sorting:

```
1 2 3 4 5
```

Every step increases cnt, producing 5. This confirms that reordering is fully allowed, and the original order is irrelevant.

A final subtle case is mixed duplicates:

```
6
1 2 2 3 3 4
```

Sorting does not change it. The algorithm counts transitions 1→2, 2→3, 3→4, yielding 4. This demonstrates that duplicates never contribute additional nesting depth, and only strict increases matter.
