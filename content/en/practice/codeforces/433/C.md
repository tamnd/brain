---
title: "CF 433C - Ryouko's Memory Note"
description: "The notebook pages are numbered from 1 to n. The sequence a describes the order in which Ryouko will read information. If two consecutive pieces of information are on pages a[i] and a[i+1], she must turn The total effort is the sum of these distances over all consecutive pairs."
date: "2026-06-07T02:41:06+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 433
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 248 (Div. 2)"
rating: 1800
weight: 433
solve_time_s: 265
verified: true
draft: false
---

[CF 433C - Ryouko's Memory Note](https://codeforces.com/problemset/problem/433/C)

**Rating:** 1800  
**Tags:** implementation, math, sortings  
**Solve time:** 4m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

The notebook pages are numbered from `1` to `n`. The sequence `a` describes the order in which Ryouko will read information. If two consecutive pieces of information are on pages `a[i]` and `a[i+1]`, she must turn `|a[i] - a[i+1]|` pages.

The total effort is the sum of these distances over all consecutive pairs.

Before reading, she may perform at most one operation. She chooses a page number `x` and a page number `y`, copies everything from `x` onto `y`, and every occurrence of `x` inside the sequence becomes `y`. The task is to find the minimum possible total page-turning cost after applying this operation once, or not changing anything.

The input size is large. Both `n` and `m` can reach `100000`. The sequence itself can contain `100000` elements, so any algorithm that tries all pairs `(x, y)` is immediately impossible. There are up to `10^10` such pairs. Even checking every possible target page for every page value would be far beyond the time limit.

The answer can also exceed 32-bit range. A sequence of length `100000` can contribute roughly `100000 × 100000`, so 64-bit arithmetic is required.

A few edge cases are easy to mishandle.

Consider:

```
3 4
2 2 2 2
```

The cost is already zero. There are no transitions between different pages. Any solution that assumes every value participates in at least one edge may accidentally access an empty structure.

Consider:

```
5 2
1 5
```

The initial cost is `4`. Merging page `5` into page `1` produces sequence `[1,1]` and cost `0`. A solution that only looks at frequencies of pages instead of their neighboring pages will miss this improvement.

Consider:

```
5 5
1 2 1 2 1
```

Page `1` interacts with page `2` four times. Those repetitions matter. Treating neighbors as a set instead of a multiset would underestimate the contribution of repeated transitions and produce the wrong gain.

## Approaches

Start with the most direct idea.

Suppose we choose a page `x` and replace every occurrence of it with some page `y`. We could rebuild the sequence and recompute the total cost. Doing this for every pair `(x, y)` requires `O(n^2 m)` work.

With `n = m = 100000`, this is roughly `10^15` operations, completely infeasible.

The key observation is that replacing page `x` only affects transitions touching `x`.

Take a transition between pages `u` and `v`.

If neither endpoint equals `x`, then after the merge the transition remains unchanged and contributes exactly the same amount. Only edges incident to `x` matter.

For a fixed page value `x`, collect every page that appears next to `x` in the sequence. If a transition occurs multiple times, keep multiple copies. Let this multiset of neighbors be:

```
v1, v2, ..., vk
```

Before any change, the part of the total cost involving `x` is

```
|x-v1| + |x-v2| + ... + |x-vk|
```

If we replace `x` by `y`, it becomes

```
|y-v1| + |y-v2| + ... + |y-vk|
```

Now the problem becomes:

For each page value `x`, find the value `y` minimizing

```
Σ |y-vi|
```

This is a classic property of absolute values. The minimum is achieved at any median of the multiset.

So for every page value `x`:

1. Gather all neighboring page values.
2. Compute its current contribution.
3. Sort the neighbor list.
4. Take its median.
5. Compute the contribution if `x` were replaced by that median.
6. The difference is the improvement obtained by optimally merging page `x`.

The best merge is simply the largest improvement among all page values.

The total size of all neighbor lists is only `2(m-1)` because every adjacent pair contributes once to each endpoint. Sorting all lists together costs `O(m log m)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m) | O(m) | Too slow |
| Optimal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Compute the original total cost by summing `|a[i] - a[i+1]|` over all adjacent pairs.
2. For every adjacent pair `(a[i], a[i+1])`, if the values differ, add each endpoint to the other's neighbor list.

This records exactly which transitions would be affected if one endpoint were changed.
3. For every page value `x` from `1` to `n`, process its neighbor list.
4. Compute

```
old = Σ |x - v|
```

over all neighbors `v` of `x`.

This is the current contribution of all transitions touching `x`.
5. Sort the neighbor list and take its median value.

The median minimizes the sum of absolute deviations.
6. Compute

```
new = Σ |median - v|
```

over the same neighbor list.
7. The gain from optimally replacing page `x` is

```
gain = old - new
```
8. Keep the maximum gain over all page values.
9. The answer is

```
original_cost - maximum_gain
```

### Why it works

Every transition contributes independently to the total cost. Replacing page `x` only changes transitions incident to `x`; all other transitions remain identical.

For a fixed page `x`, the affected part of the objective is exactly

```
Σ |y - v|
```

where `v` ranges over all neighbors of `x`, counted with multiplicity. The classical median property states that this expression is minimized by choosing `y` equal to a median of the multiset.

Since each page value can be optimized independently and we are allowed only one merge operation, the globally optimal move is the page whose best possible reduction is largest. Subtracting that reduction from the original cost gives the minimum achievable total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    neigh = [[] for _ in range(n + 1)]
    total = 0

    for i in range(m - 1):
        u = a[i]
        v = a[i + 1]

        total += abs(u - v)

        if u != v:
            neigh[u].append(v)
            neigh[v].append(u)

    best_gain = 0

    for x in range(1, n + 1):
        if not neigh[x]:
            continue

        vec = neigh[x]

        old = 0
        for v in vec:
            old += abs(x - v)

        vec.sort()
        med = vec[len(vec) // 2]

        new = 0
        for v in vec:
            new += abs(med - v)

        best_gain = max(best_gain, old - new)

    print(total - best_gain)

solve()
```

The first loop computes the original cost and simultaneously builds the neighbor lists. Every adjacent pair contributes to exactly two lists, one for each endpoint.

Transitions where both endpoints are equal are ignored when building neighbor lists. Such transitions already contribute zero and remain zero regardless of any merge, so they cannot affect the gain calculation.

For each page value, `old` measures the current cost contributed by all incident transitions. After sorting the neighbor list, the middle element is a median. Replacing the page by this median gives the smallest possible value of the affected cost, which is computed as `new`.

The improvement is `old - new`. The largest improvement corresponds to the best merge operation.

Python integers automatically handle values larger than 32 bits, so no special overflow handling is needed.

## Worked Examples

### Example 1

Input:

```
4 6
1 2 3 4 3 2
```

The adjacent transitions are:

```
1-2, 2-3, 3-4, 4-3, 3-2
```

Initial cost:

```
1 + 1 + 1 + 1 + 1 = 5
```

Neighbor lists:

| Page | Neighbors |
| --- | --- |
| 1 | [2] |
| 2 | [1, 3, 3] |
| 3 | [2, 4, 4, 2] |
| 4 | [3, 3] |

Processing:

| Page x | old | Median | new | Gain |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 0 | 1 |
| 2 | 3 | 3 | 2 | 1 |
| 3 | 4 | 4 | 4 | 0 |
| 4 | 2 | 3 | 0 | 2 |

Maximum gain is `2`.

Final answer:

```
5 - 2 = 3
```

This corresponds to replacing page `4` with page `3`.

### Example 2

Input:

```
5 5
1 5 1 5 1
```

Initial cost:

```
4 + 4 + 4 + 4 = 16
```

Neighbor lists:

| Page | Neighbors |
| --- | --- |
| 1 | [5, 5, 5, 5] |
| 5 | [1, 1, 1, 1] |

Processing:

| Page x | old | Median | new | Gain |
| --- | --- | --- | --- | --- |
| 1 | 16 | 5 | 0 | 16 |
| 5 | 16 | 1 | 0 | 16 |

Maximum gain is `16`.

Final answer:

```
16 - 16 = 0
```

The trace shows why repeated neighbors must be counted with multiplicity. Each occurrence contributes separately to the cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Total size of all neighbor lists is O(m), and sorting all of them costs O(m log m) |
| Space | O(m) | Neighbor lists store O(m) values in total |

With `m ≤ 100000`, an `O(m log m)` solution is comfortably within the limits. The memory usage is also linear in the input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    neigh = [[] for _ in range(n + 1)]
    total = 0

    for i in range(m - 1):
        u = a[i]
        v = a[i + 1]

        total += abs(u - v)

        if u != v:
            neigh[u].append(v)
            neigh[v].append(u)

    best = 0

    for x in range(1, n + 1):
        if not neigh[x]:
            continue

        vec = neigh[x]

        old = sum(abs(x - v) for v in vec)

        vec.sort()
        med = vec[len(vec) // 2]

        new = sum(abs(med - v) for v in vec)

        best = max(best, old - new)

    return str(total - best)

# provided sample
assert run("4 6\n1 2 3 4 3 2\n") == "3", "sample 1"

# minimum size
assert run("1 1\n1\n") == "0", "single element"

# all equal
assert run("3 4\n2 2 2 2\n") == "0", "all equal"

# simple merge to zero
assert run("5 2\n1 5\n") == "0", "single transition"

# repeated alternating values
assert run("5 5\n1 5 1 5 1\n") == "0", "multiplicity handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `0` | Minimum input size |
| `3 4 / 2 2 2 2` | `0` | Empty neighbor lists |
| `5 2 / 1 5` | `0` | Single transition |
| `5 5 / 1 5 1 5 1` | `0` | Repeated neighbors must be counted multiple times |

## Edge Cases

Consider:

```
1 1
1
```

There are no adjacent pairs, so the original cost is `0`. Every neighbor list is empty. The algorithm skips all pages, keeps `best_gain = 0`, and outputs `0`.

Consider:

```
3 4
2 2 2 2
```

Every adjacent difference is zero. No neighbors are recorded because all adjacent values are equal. The algorithm never attempts to compute a median of an empty list and correctly returns `0`.

Consider:

```
5 2
1 5
```

The original cost is `4`. Page `1` has neighbor list `[5]`, giving `old = 4`, `median = 5`, `new = 0`, gain `4`. The same gain appears for page `5`. The final answer is `4 - 4 = 0`.

Consider:

```
5 5
1 2 1 2 1
```

The neighbor list of page `1` is `[2,2,2,2]`, not just `{2}`. The algorithm stores all four copies. Its contribution is `4`, and replacing `1` by `2` removes all four units of cost. Treating neighbors as a set would incorrectly count only one occurrence and underestimate the gain.
