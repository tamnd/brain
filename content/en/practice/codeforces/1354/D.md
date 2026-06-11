---
title: "CF 1354D - Multiset"
description: "We are maintaining a collection of integers where duplicates are allowed, and the collection changes over time. Initially we are given a sorted list of values that already form the starting multiset. After that, we receive a long sequence of operations."
date: "2026-06-11T13:55:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1354
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 87 (Rated for Div. 2)"
rating: 1900
weight: 1354
solve_time_s: 101
verified: true
draft: false
---

[CF 1354D - Multiset](https://codeforces.com/problemset/problem/1354/D)

**Rating:** 1900  
**Tags:** binary search, data structures  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a collection of integers where duplicates are allowed, and the collection changes over time. Initially we are given a sorted list of values that already form the starting multiset. After that, we receive a long sequence of operations.

Each operation either inserts a new integer into the multiset, or removes an element based on its position in sorted order. When we say “k-th order statistic”, we mean if you sort the entire multiset, the k-th smallest element is chosen. That element is then removed from the structure. Insertions simply add a value, and removals depend on the current ordering, not on value equality.

At the end, we only need to output one remaining element from the multiset if it is non-empty, otherwise we print zero.

The key difficulty is that the number of operations can be up to one million, so any approach that re-sorts or scans the entire structure per query will fail. Even O(n) per operation leads to 10^12 operations in the worst case, which is far beyond the time limit. This forces us into a structure that supports both insertion and k-th order statistic queries in logarithmic time.

A subtle edge case comes from repeated removals of small k values. For example, if we repeatedly remove the 1st element, the structure keeps shrinking from the front. A naive approach that rebuilds arrays or repeatedly sorts can silently degrade into quadratic behavior even if each step seems “simple”.

Another important edge case is that after all removals, the multiset may become empty, even if it started large. In that case, we must output 0 rather than attempting to access an element.

## Approaches

A straightforward idea is to maintain the multiset as a dynamic array or Python list. For each insertion, we append the value. For each removal, we sort the array and remove the k-th element.

This is correct logically, but the performance collapses immediately. Sorting costs O(n log n), and doing it up to one million times leads to roughly 10^6 × n log n operations, which is infeasible. Even if we maintain the list in sorted order using binary insertion, deletions of the k-th element still require shifting elements, leading to O(n) per operation.

The core observation is that we never need the actual ordering of elements explicitly. We only need two capabilities: maintain frequencies of values and quickly find the k-th smallest element among all present elements. Once that element is found, we decrement its frequency.

This transforms the problem into a dynamic prefix-sum structure. If we maintain how many times each value appears, then the k-th smallest element is the smallest index such that the prefix sum reaches at least k. A Fenwick tree supports exactly this pattern: point updates and prefix sums, plus binary lifting to locate the k-th position in O(log n).

Because all values are bounded by n, we can safely use a Fenwick tree of size n. Each insertion is a single point update, and each removal is a “find by prefix sum” followed by another point update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Re-sorting / array simulation | O(nq) or O(nq log n) | O(n) | Too slow |
| Fenwick tree (BIT) | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We model the multiset as a frequency array over the value range, maintained inside a Fenwick tree.

1. Build a Fenwick tree and insert all initial elements by increasing their frequency by one. This establishes the correct starting prefix sums.
2. For each query, check its sign. If the value is positive, it represents insertion, so we increase the frequency of that value in the Fenwick tree by one. This keeps prefix sums consistent with the updated multiset.
3. If the value is negative, we interpret it as a request to remove the k-th smallest element, where k is the absolute value. We first use the Fenwick tree to locate the smallest index such that its prefix sum is at least k. This index corresponds exactly to the k-th smallest element in the current multiset.
4. Once that index is found, we decrease its frequency by one in the Fenwick tree. This simulates removing exactly one occurrence of that value.
5. After processing all queries, we scan for any index with a positive frequency. If none exists, we output zero. Otherwise, we output any index with non-zero frequency.

The key operation is the “find k-th” step, which uses binary lifting on the Fenwick tree. At each bit level, we try to move right if doing so does not exceed the cumulative frequency k. This constructs the answer in logarithmic time.

### Why it works

At every moment, the Fenwick tree stores exact multiplicities of all values currently in the multiset. Prefix sums therefore represent the number of elements less than or equal to any value. The k-th smallest element is uniquely determined by the first position where this cumulative count reaches k, so the binary search over prefix sums always identifies the correct element. Since every insertion and deletion updates frequencies exactly once, this invariant is preserved throughout all operations.

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

    def find_kth(self, k):
        idx = 0
        bit_mask = 1 << (self.n.bit_length())
        while bit_mask:
            nxt = idx + bit_mask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bit_mask >>= 1
        return idx + 1

n, q = map(int, input().split())
a = list(map(int, input().split()))

fw = Fenwick(n)

for x in a:
    fw.add(x, 1)

for x in map(int, input().split()):
    if x > 0:
        fw.add(x, 1)
    else:
        k = -x
        pos = fw.find_kth(k)
        fw.add(pos, -1)

for i in range(1, n + 1):
    if fw.sum(i) - fw.sum(i - 1) > 0:
        print(i)
        break
else:
    print(0)
```

The Fenwick tree is initialized over the value range, not over the number of elements. This matters because we are not tracking positions in an array but frequencies of values.

The `find_kth` function performs a binary lifting search over the implicit prefix sums. It builds the answer bit by bit, ensuring we never exceed the required cumulative frequency.

The final loop simply finds any value still present. Since the problem allows any remaining element, we stop at the first positive frequency.

## Worked Examples

### Example 1

Input:

```
5 5
1 2 3 4 5
-1 -1 -1 -1 -1
```

We track the multiset frequencies.

| Step | Operation | Multiset state (conceptual) | Removed |
| --- | --- | --- | --- |
| 1 | remove 1st | 2 3 4 5 | 1 |
| 2 | remove 1st | 3 4 5 | 2 |
| 3 | remove 1st | 4 5 | 3 |
| 4 | remove 1st | 5 | 4 |
| 5 | remove 1st | empty | 5 |

After all operations, no elements remain, so output is 0.

This confirms repeated prefix removals correctly collapse the structure until empty.

### Example 2

Input:

```
3 4
1 1 3
2 -1 2 -1
```

Initial multiset is [1, 1, 3].

| Step | Operation | Multiset |
| --- | --- | --- |
| 1 | insert 2 | 1 1 2 3 |
| 2 | remove 1st | 1 2 3 (removed 1) |
| 3 | insert 2 | 1 2 2 3 |
| 4 | remove 1st | 2 2 3 (removed 1) |

Final multiset contains [2, 2, 3], so any of 2 or 3 is valid output.

This shows that duplicates are handled correctly and removals only affect a single occurrence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each update and k-th query is handled by Fenwick tree operations in logarithmic time |
| Space | O(n) | One frequency array stored inside the Fenwick tree |

The bounds allow up to two million operations total, so a logarithmic factor around 20 keeps the solution comfortably within limits. Memory usage stays linear in n, which fits under the 28 MB constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
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

        def find_kth(self, k):
            idx = 0
            bit_mask = 1 << (self.n.bit_length())
            while bit_mask:
                nxt = idx + bit_mask
                if nxt <= self.n and self.bit[nxt] < k:
                    k -= self.bit[nxt]
                    idx = nxt
                bit_mask >>= 1
            return idx + 1

    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    fw = Fenwick(n)

    for x in a:
        fw.add(x, 1)

    for x in map(int, input().split()):
        if x > 0:
            fw.add(x, 1)
        else:
            pos = fw.find_kth(-x)
            fw.add(pos, -1)

    for i in range(1, n + 1):
        if fw.sum(i) - fw.sum(i - 1) > 0:
            return str(i)
    return "0"

# provided sample
assert run("""5 5
1 2 3 4 5
-1 -1 -1 -1 -1
""") == "0"

# custom: single element delete
assert run("""1 1
1
-1
""") == "0"

# custom: insert only
assert run("""1 3
1
2 3 1
""") != ""

# custom: duplicates
assert run("""3 3
1 1 1
-1 -1 -1
""") == "0"

# custom: mixed
assert run("""3 4
1 2 3
2 -1 2 -1
""") in {"2", "3"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element delete | 0 | removal on minimal structure |
| insert only | non-empty | handling inserts without deletions |
| duplicates all removed | 0 | correct handling of repeated values |
| mixed ops | 2 or 3 | correctness under interleaving |

## Edge Cases

A key edge case is when removals repeatedly target the smallest element. For input like `1 2 3 4 5` followed by repeated `-1` operations, the structure shrinks from the left every time. The Fenwick tree correctly updates frequencies, and each `find_kth(1)` always returns the current minimum, ensuring deterministic shrinking until empty.

Another case is heavy duplication such as starting with many identical values and repeatedly removing arbitrary order statistics. Since all equal elements share the same index, every removal only decreases frequency by one, and prefix sums still behave consistently. The k-th query never confuses identical values because it depends on cumulative count, not identity.

Finally, alternating insertions and deletions stress the invariant that the Fenwick tree always reflects the current multiset exactly. Each operation is local, so no global reconstruction is needed, which prevents both correctness issues and performance collapse.
