---
title: "CF 104069E - El Classificador"
description: "We are managing a collection of shoe sizes stored in a multiset-like structure where removals are permanent. Each time a customer arrives, they specify a minimum acceptable shoe size, and we must give them the smallest available shoe whose size is at least that threshold."
date: "2026-07-02T02:59:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104069
codeforces_index: "E"
codeforces_contest_name: "VII MaratonUSP Freshman Contest"
rating: 0
weight: 104069
solve_time_s: 43
verified: true
draft: false
---

[CF 104069E - El Classificador](https://codeforces.com/problemset/problem/104069/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are managing a collection of shoe sizes stored in a multiset-like structure where removals are permanent. Each time a customer arrives, they specify a minimum acceptable shoe size, and we must give them the smallest available shoe whose size is at least that threshold. Once a shoe is assigned, it disappears from the inventory and cannot be reused.

The input gives an initial array of shoe sizes and then a sequence of queries. Each query is independent in input, but not in execution, since earlier assignments change the available pool for later queries. For each query, we either output the size of the shoe assigned or −1 if no suitable shoe exists.

The constraints allow up to 200,000 shoes and 200,000 queries, with values up to 10^9. Any solution that tries to scan the entire array for every query will perform on the order of n·q operations, which is up to 4·10^10 comparisons in the worst case. That is far beyond what can run in a few seconds in Python or even in optimized C++.

A naive approach would fail in a simple scenario like an already sorted list with decreasing queries. For example, if the shoes are [1, 2, 3, 4, 5] and queries are all 5, each query would scan the full list to find the last remaining valid element. Even though the answer is obvious, the repeated linear scans dominate runtime.

A subtle edge case is repeated equal values. If the input is [4, 4, 4] and queries are [4, 4, 4, 4], the correct behavior is to consume one 4 per query until exhausted, then return −1. A naive solution that forgets to mark elements as removed or incorrectly handles duplicates will either reuse the same shoe multiple times or skip valid matches.

## Approaches

The brute-force strategy is straightforward: for each query, scan the entire array from left to right, find the first element that is at least x, output it, and remove it from the array. Removal can be done by physically deleting the element or marking it. The correctness is immediate because we directly simulate the rule given in the statement.

The failure point is performance. Each query costs O(n) in the worst case, and there are q queries, leading to O(nq). With n and q both up to 2·10^5, this becomes infeasible.

The key observation is that we repeatedly need two operations on a dynamic set of values: find the smallest element that is at least x, and remove it. This is exactly a predecessor-like query on a dynamic ordered set. Once we sort the initial array, the problem reduces to maintaining a structure that supports lower bound search plus deletion efficiently.

A balanced binary search tree or a multiset supports this directly, but in competitive programming we can simulate it efficiently using a sorted structure plus binary search. However, deletion in a Python list is linear, so we need a structure where removals do not shift large segments. A segment tree over frequency counts or a sorted container with bisect plus lazy deletion also works, but the cleanest approach is a segment tree over the compressed value domain or a Fenwick tree storing counts of occurrences, allowing us to locate the next available value via binary lifting.

We compress values because sizes go up to 10^9 but only 2·10^5 distinct values exist. After compression, we maintain frequencies. Each query becomes a “find first index with prefix sum ≥ target position in value order constrained by x”. We first locate the first compressed index whose value is ≥ x using binary search, then find the next available active index using a Fenwick tree “kth” style walk. That gives us the smallest valid available shoe, and we decrement its count.

This reduces each query to O(log n), giving a total O((n + q) log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal (Fenwick / multiset simulation) | O((n+q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first sort and compress the shoe sizes so that we can reason about them in increasing order while still mapping back to original values. Each distinct size gets an index in a sorted array.

We build a Fenwick tree over these indices, where each position stores how many shoes of that size are currently available.

For each query x, we translate x into the first index in the compressed array whose value is at least x. From that point onward, we only care about the suffix of the structure, since everything before x is invalid for this query.

We then use the Fenwick tree to find the first position at or after that index that still has a positive count. This is a standard “find first prefix where cumulative frequency reaches a target” operation, adapted to start from a lower bound index rather than from 1.

Once we locate that position, we output its value and decrement its frequency in the Fenwick tree.

If no such position exists, we output −1.

### Why it works

At every step, the Fenwick tree maintains the exact multiset of available shoes. The binary search step ensures we never consider values smaller than the query threshold. The “kth-like” traversal ensures we pick the smallest index that is still alive among valid candidates. Since each removal updates the structure immediately, future queries always reflect the correct remaining inventory, so the simulation matches the problem definition exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def kth(self, k):
        pos = 0
        bitmask = 1 << (self.n.bit_length())
        while bitmask:
            nxt = pos + bitmask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                pos = nxt
            bitmask >>= 1
        return pos + 1

def lower_bound(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] >= x:
            hi = mid
        else:
            lo = mid + 1
    return lo

def main():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    vals = sorted(set(a))
    idx = {v: i + 1 for i, v in enumerate(vals)}

    fw = Fenwick(len(vals))

    for v in a:
        fw.add(idx[v], 1)

    for _ in range(q):
        x = int(input())
        pos = lower_bound(vals, x)
        if pos == len(vals):
            print(-1)
            continue

        # convert to Fenwick index range [pos+1 ... end]
        # we need first active in suffix, so we compare counts
        total_before = fw.sum(pos)
        total_all = fw.sum(len(vals))
        if total_all - total_before <= 0:
            print(-1)
            continue

        # find (total_before + 1)-th alive element overall
        # but must ensure it's within suffix; this is guaranteed by construction
        k = total_before + 1
        i = fw.kth(k)

        if i < pos + 1:
            # fallback safety, should not happen
            i = fw.kth(total_before + 1)

        print(vals[i - 1])
        fw.add(i, -1)

if __name__ == "__main__":
    main()
```

The Fenwick tree maintains frequencies of each shoe size in compressed form. The `lower_bound` function locates the first eligible size index. We then compute how many valid shoes exist before that index and use a global kth query to pick the next available shoe. This works because all invalid candidates are effectively skipped by restricting the starting rank.

A common subtlety is ensuring we do not accidentally pick a shoe smaller than x. That is why we explicitly compare prefix counts and start selection from the first valid rank. Another subtle point is handling duplicates correctly: the Fenwick tree stores multiplicity, so identical sizes are naturally consumed one by one.

## Worked Examples

### Example 1

Input:

```
5 3
1 2 3 4 5
2
4
3
```

We compress values [1,2,3,4,5] directly.

| Query | x | lower_bound pos | prefix count | chosen index | output | remaining multiset |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 1 | 2 | 2 | [1,3,4,5] |
| 2 | 4 | 4 | 2 | 4 | 4 | [1,3,5] |
| 3 | 3 | 3 | 1 | 3 | 3 | [1,5] |

This trace shows how the structure always skips removed elements and respects the minimum constraint.

### Example 2

Input:

```
3 4
4 4 4
4
4
4
4
```

| Query | x | prefix count before x | chosen | output | remaining |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 0 | 1st | 4 | [4,4] |
| 2 | 4 | 0 | 1st | 4 | [4] |
| 3 | 4 | 0 | 1st | 4 | [] |
| 4 | 4 | 0 | none | -1 | [] |

This confirms correct handling of duplicates and exhaustion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | each insertion and query uses Fenwick operations |
| Space | O(n) | compressed values plus Fenwick tree |

The constraints allow up to 2·10^5 operations, and logarithmic factors around 18 are easily fast enough in Python when implemented with simple loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    import contextlib
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        main()
    return output.getvalue().strip()

# provided sample-style cases
assert run("5 3\n1 2 3 4 5\n2\n4\n3\n") == "2\n4\n3"
assert run("3 4\n4 4 4\n4\n4\n4\n4\n") == "4\n4\n4\n-1"

# custom edge cases
assert run("1 2\n10\n10\n10\n") == "10\n-1"
assert run("2 2\n1 100\n50\n50\n") == "100\n-1"
assert run("5 5\n5 4 3 2 1\n1\n1\n1\n1\n1\n") == "1\n2\n3\n4\n5"
assert run("4 3\n2 2 2 2\n3\n1\n2\n") == "-1\n2\n2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element exhaustion | 10, -1 | boundary removal |
| mixed values threshold | 100, -1 | lower bound correctness |
| reverse order full consumption | 1..5 | repeated kth logic |
| duplicates + threshold skip | -1,2,2 | duplicate handling |

## Edge Cases

For a single shoe in the system, the algorithm correctly handles immediate exhaustion. If the input is `10` followed by two queries `10, 10`, the Fenwick tree initially has one active element. The first query finds it, removes it, and the second query sees zero remaining elements, returning −1.

For duplicates, the structure treats each occurrence independently. In a case like `[4,4,4]` with queries `[4,4,4,4]`, each successful query reduces the frequency by exactly one. The final query observes that the total prefix sum is zero beyond the threshold and correctly outputs −1.

For threshold skipping, consider `[1,100]` with query `50`. The lower bound starts at 100, so the algorithm never considers 1. The Fenwick tree then directly returns 100 as the first valid element, preserving correctness even when invalid smaller elements exist earlier in the array.
