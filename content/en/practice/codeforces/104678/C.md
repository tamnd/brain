---
title: "CF 104678C - Storybooks"
description: "We are given a collection of story lengths, where each story has a fixed number of pages. Alongside this, we are given several books, each with a page capacity."
date: "2026-06-29T09:05:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104678
codeforces_index: "C"
codeforces_contest_name: "October come back. Together training"
rating: 0
weight: 104678
solve_time_s: 70
verified: true
draft: false
---

[CF 104678C - Storybooks](https://codeforces.com/problemset/problem/104678/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of story lengths, where each story has a fixed number of pages. Alongside this, we are given several books, each with a page capacity. For every book, we want to know how many different stories we can place inside it if we are free to choose any subset of stories, but the total number of pages in that subset must not exceed the book’s capacity.

A key detail is that each story can be reused across books, but reuse does not create any coupling between queries. Every book is evaluated independently against the same pool of stories.

So the task reduces to, for each capacity value, finding the largest number of stories whose total page sum fits within that limit.

The constraints push us toward a near-linear or log-linear solution. With up to 200,000 stories and 200,000 queries, any approach that recomputes subsets per query would be far too slow. A naive per-query greedy selection over all stories would cost O(nk), which is on the order of 4e10 operations in the worst case and is not viable under a 2-second limit. Even sorting per query would be completely infeasible.

A subtle pitfall comes from misinterpreting the problem as needing arbitrary subsets. One might think different combinations could matter, but since all stories are independent and only contribute additively, the optimal choice is always to pick the smallest available stories first. Any attempt to include a larger story while excluding a smaller one can only reduce the number of stories achievable under the same sum constraint.

A second edge case appears when capacities are very small. If a book has capacity less than the smallest story, the answer must be zero. Another corner case is when capacities are extremely large, up to 10^18, where all stories can always be included if their total sum fits.

## Approaches

The brute-force idea is straightforward: for each book, try all subsets of stories, or at least simulate picking stories in some order and track how many can fit before exceeding capacity. Even if we optimize slightly by sorting stories once and greedily adding them, doing this separately for each query still leads to O(nk) behavior because each book may scan through all stories.

The key structural insight is that we only care about how many smallest stories can be packed before exceeding a limit, not which specific ones. Once the stories are sorted by size, the best strategy for maximizing count under a sum constraint is always to take them in increasing order. This transforms each query into a prefix problem over a sorted array.

If we precompute prefix sums over the sorted story lengths, then each query becomes: find the largest prefix whose sum does not exceed the book capacity. This is a classic monotonic condition that can be solved with binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(1) | Too slow |
| Sorting + Prefix + Binary Search | O(n log n + k log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all story lengths in non-decreasing order. This ensures that taking stories in sequence always gives the smallest possible cumulative sum for any fixed number of stories.
2. Build a prefix sum array over the sorted stories. Each position stores the total pages required to take all stories up to that index.
3. For each book capacity, we want to find the maximum prefix length such that the prefix sum is less than or equal to the capacity.
4. Use binary search over the prefix sum array to locate the rightmost position where the sum does not exceed the book’s limit. The index of that position is the answer for that book.
5. Output all answers in the same order as the input queries.

The reason binary search works here is that the prefix sum array is strictly increasing, since all story lengths are positive. This guarantees a monotonic predicate: once a prefix sum exceeds the capacity, all longer prefixes will also exceed it.

### Why it works

The optimal subset for maximizing count under a sum constraint must always consist of the smallest available elements. Any deviation that replaces a smaller story with a larger one reduces the number of elements you can fit without improving feasibility. This makes the sorted prefix structure not just sufficient but optimal, and the monotonicity of prefix sums guarantees that binary search finds the exact cutoff point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    a.sort()
    
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    
    import bisect
    
    res = []
    for cap in b:
        ans = bisect.bisect_right(pref, cap) - 1
        res.append(str(ans))
    
    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The solution starts by sorting the story lengths so that smaller stories are considered first. The prefix sum array converts the problem of “how many items fit under a sum constraint” into a range query over a single array. The use of `bisect_right` directly finds the first prefix sum strictly greater than the capacity, and subtracting one gives the last valid prefix length.

A subtle implementation detail is that the prefix array starts with a zero at index 0, representing selecting no stories. This ensures that even very small capacities correctly map to zero stories without special casing.

## Worked Examples

### Example 1

Input:

```
4 3
8 2 3 30
5 29 1
```

After sorting stories: `[2, 3, 8, 30]`

Prefix sums: `[0, 2, 5, 13, 43]`

| Book capacity | Binary search result (prefix index) | Answer |
| --- | --- | --- |
| 5 | 2 | 2 |
| 29 | 3 | 3 |
| 1 | 0 | 0 |

The first query fits stories 2 and 3 (sum 5). The second can fit three stories (2 + 3 + 8 = 13). The last capacity is too small to include even the smallest story.

This confirms that the prefix-based greedy choice aligns with optimal subset selection.

### Example 2

Input:

```
5 2
4 1 10 2 7
3 15
```

Sorted stories: `[1, 2, 4, 7, 10]`

Prefix sums: `[0, 1, 3, 7, 14, 24]`

| Book capacity | Prefix index | Answer |
| --- | --- | --- |
| 3 | 2 | 2 |
| 15 | 4 | 4 |

For capacity 3, we can take 1 and 2. For capacity 15, we can take 1, 2, 4, and 7, but not 10 since it would exceed the limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + k log n) | Sorting dominates, each query uses binary search |
| Space | O(n) | Prefix sum array and sorted list |

The constraints allow up to 200,000 elements, and this complexity comfortably fits within typical limits. Sorting once and answering each query in logarithmic time ensures the solution remains efficient even in the worst case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    pref = [0]
    for x in a:
        pref.append(pref[-1] + x)

    import bisect
    res = []
    for cap in b:
        res.append(str(bisect.bisect_right(pref, cap) - 1))
    return " ".join(res)

# provided sample
assert run("4 3\n8 2 3 30\n5 29 1\n") == "2 3 0"

# minimum size
assert run("1 1\n5\n5\n") == "1"

# cannot take anything
assert run("3 2\n10 20 30\n1 5\n") == "0 0"

# all equal
assert run("4 2\n3 3 3 3\n6 12\n") == "2 4"

# large increasing capacities
assert run("5 3\n1 2 3 4 5\n3 6 15\n") == "2 3 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal case correctness |
| large values too small | 0 0 | no selection edge case |
| all equal | 2 4 | duplicate handling and prefix sums |
| increasing capacities | 2 3 5 | progressive accumulation behavior |

## Edge Cases

When all stories are larger than a given book capacity, sorting ensures the smallest story is still too large. In that case, prefix sum for the first element already exceeds the capacity, and binary search returns index 0, correctly yielding zero stories.

For very large capacities, such as values close to 10^18, the prefix sum array still correctly handles them because the total sum is within 64-bit range. The binary search simply returns the full prefix length, meaning all stories can be included.

When there is only one story, the prefix array becomes `[0, a1]`. Any capacity greater than or equal to `a1` yields one story, otherwise zero, and the binary search naturally reproduces this behavior without special handling.
