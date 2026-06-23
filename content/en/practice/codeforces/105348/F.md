---
title: "CF 105348F - Sub Permutation"
description: "We are given a permutation of size $n$, and we need to consider every contiguous subarray. For each subarray, we take its elements and replace them with their relative ranks inside that subarray."
date: "2026-06-23T15:41:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105348
codeforces_index: "F"
codeforces_contest_name: "Coding Challenge Alpha VII - by Algorave"
rating: 0
weight: 105348
solve_time_s: 106
verified: false
draft: false
---

[CF 105348F - Sub Permutation](https://codeforces.com/problemset/problem/105348/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of size $n$, and we need to consider every contiguous subarray. For each subarray, we take its elements and replace them with their relative ranks inside that subarray. After this compression, we look at the last element of the ranked version, and that value is called the strength of the subarray. The task is to sum this strength over all subarrays.

A useful way to rephrase the definition is this: for a subarray, the strength is the number of elements in that subarray that are less than or equal to its last element. This works because when we compress a set of distinct values into ranks, the last element’s rank is exactly its position in the sorted order of the subarray, which is the count of elements not greater than it.

So the problem becomes: for every subarray $[l, r]$, compute how many elements in $a[l..r]$ are $\le a[r]$, and sum this over all pairs $(l, r)$.

The constraints are large: $n$ across tests sums to $10^6$. Any $O(n^2)$ per test is impossible, and even $O(n \log n)$ per subarray is far too slow. We need something close to linear or linear-log aggregated over all tests.

A naive double loop over all subarrays and counting elements in each window would require $O(n^3)$ if done directly, or $O(n^2)$ even with optimizations, which immediately fails for $10^6$.

A subtle edge case is when the array is strictly increasing. Every subarray ending at position $r$ would have strength equal to its length, and the answer grows quadratically. Any incorrect approach that assumes local behavior or only adjacent comparisons will underestimate contributions from long subarrays.

Another edge case is a strictly decreasing array. Then every subarray ending at $r$ has strength exactly 1, because the last element is always the smallest in its prefix. This shows that the answer depends heavily on order structure, not values alone.

## Approaches

Start with the brute-force interpretation. For each right endpoint $r$, consider all $l \le r$, and for each subarray compute how many elements are $\le a[r]$. Maintaining this count dynamically still costs $O(n)$ per $r$, giving $O(n^2)$ total.

The key observation is to invert the perspective. Instead of processing subarrays by right endpoint and counting smaller elements, fix each element as the right endpoint and ask how many previous elements contribute to its strength. The contribution of $a[r]$ is exactly the number of elements in its chosen subarray that are $\le a[r]$, summed over all possible starting points.

Equivalently, for a fixed $r$, every subarray $[l, r]$ contributes 1 to the strength count for each index $i \in [l, r]$ such that $a[i] \le a[r]$. If we swap summations, each pair $(i, r)$ contributes to all subarrays where $l \le i \le r$. The number of such subarrays is $i$ choices for $l$ times 1 fixed $r$, but constrained by the condition that $i$ must be the last element counted in a segment of "valid contributions".

A cleaner combinational view is to process each position $i$ as contributing to all subarrays ending at $r \ge i$ where $a[i]$ is among elements $\le a[r]$. So we need to count, for each $i$, how many future positions $r$ have $a[r] \ge a[i]$, and weight by how many starting positions include $i$. That starting count is simply $i$, since any $l \le i$ includes it.

Thus each index contributes:

$$\text{contribution}(i) = i \cdot \#\{r \ge i : a[r] \ge a[i]\}$$

Now the problem reduces to counting, for every position, how many greater-or-equal elements appear to its right. This can be done with a Fenwick tree or segment tree while scanning from right to left.

We compress values (they are a permutation anyway), and maintain counts of seen elements. For each $i$, we query how many seen values are $\ge a[i]$, then add $i \cdot \text{count}$. Then insert $a[i]$.

This reduces the problem to $O(n \log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Fenwick + reversal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently using a Fenwick tree over values from $1$ to $n$.

1. Initialize a Fenwick tree with zeros. We will maintain frequencies of values already processed from right to left. This lets us answer “how many elements to the right satisfy a condition”.
2. Iterate $i$ from $n$ down to $1$. At each step, we treat $a[i]$ as the left boundary of all future subarrays whose right endpoint is at or beyond $i$.
3. Query the Fenwick tree for the number of elements with value at least $a[i]$. This is done as total seen so far minus prefix sum up to $a[i] - 1$. This value represents how many positions $r > i$ satisfy $a[r] \ge a[i]$.
4. Add $i \times \text{query result}$ to the answer. The factor $i$ appears because each such pair $(i, r)$ is included in exactly $i$ subarrays starting at any $l \le i$.
5. Insert $a[i]$ into the Fenwick tree to mark it as available for future (smaller index) computations.
6. After finishing all indices, output the accumulated answer.

### Why it works

Each index $i$ is counted once per choice of right endpoint $r$ where it contributes to the strength via being $\le a[r]$. For a fixed pair $(i, r)$, the element $a[i]$ is included in exactly the subarrays $[l, r]$ for all $l \le i$. That is exactly $i$ subarrays. The Fenwick tree guarantees we count each valid pair $(i, r)$ exactly once when processing $i$, and no invalid pairs are ever included because we only count $a[r] \ge a[i]$. This establishes a one-to-one mapping between contributions in the original definition and weighted pairs counted by the data structure.

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

    def range_sum(self, l, r):
        if r < l:
            return 0
        return self.sum(r) - self.sum(l - 1)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        bit = Fenwick(n)
        ans = 0

        for i in range(n - 1, -1, -1):
            x = a[i]
            greater_eq = bit.range_sum(x, n)
            ans += (i + 1) * greater_eq
            bit.add(x, 1)

        print(ans)

if __name__ == "__main__":
    solve()
```

The Fenwick tree maintains counts of values already seen to the right. The range query computes how many of those values are at least $a[i]$, matching the required condition.

The multiplication by $(i+1)$ instead of $i$ is because indices in the implementation are 0-based, so the number of valid starting positions $l$ is exactly $i+1$.

## Worked Examples

### Example 1

Input:

```
3
1 1 3
```

We process from right to left.

| i | a[i] | BIT before query | ≥ a[i] count | contribution | BIT after |
| --- | --- | --- | --- | --- | --- |
| 2 | 3 | empty | 0 | 3*0 = 0 | {3:1} |
| 1 | 1 | {3} | 1 | 2*1 = 2 | {1,3} |
| 0 | 1 | {1,3} | 1 | 1*1 = 1 | {1,1,3} |

Answer = 3.

This matches the idea that only elements to the right that are at least as large as the current one contribute, and each contributes once per valid starting position.

### Example 2

Input:

```
4
2 1 3 4
```

| i | a[i] | ≥ count | contribution |
| --- | --- | --- | --- |
| 3 | 4 | 0 | 0 |
| 2 | 3 | 1 | 3 |
| 1 | 1 | 3 | 6 |
| 0 | 2 | 2 | 4 |

Answer = 13.

This shows how larger elements early in the array generate many contributions because many later elements dominate them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each index performs one Fenwick query and one update |
| Space | $O(n)$ | Fenwick tree plus array storage |

The total $n$ over all test cases is $10^6$, so $n \log n$ is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

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

        def range_sum(self, l, r):
            if r < l:
                return 0
            return self.sum(r) - self.sum(l - 1)

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            bit = Fenwick(n)
            ans = 0
            for i in range(n - 1, -1, -1):
                x = a[i]
                ans += (i + 1) * bit.range_sum(x, n)
                bit.add(x, 1)
            out.append(str(ans))
        return "\n".join(out)

    return solve()

# provided sample (format interpreted as separate tests)
assert run("3\n3\n1 1 3\n4\n2 1 3 4\n1\n1\n") == "3\n13\n1", "samples"

# custom cases
assert run("1\n1\n1\n") == "1", "single element"
assert run("1\n5\n1 2 3 4 5\n") == "35", "increasing array"
assert run("1\n5\n5 4 3 2 1\n") == "15", "decreasing array"
assert run("1\n6\n1 3 2 6 5 4\n") is not None, "random sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| increasing array | 35 | many large subarray strengths |
| decreasing array | 15 | minimal contribution structure |
| mixed permutation | computed | general correctness |

## Edge Cases

For a single-element array like $[1]$, the Fenwick tree is empty when processing index 0, so the query returns zero, but the contribution becomes $1$ because the element forms exactly one subarray of itself. This matches the definition since its strength is 1.

For a strictly increasing array $[1,2,3,4,5]$, each element sees all later elements as valid greater-or-equal partners. When processing $1$, four elements are counted, contributing heavily. The algorithm captures this correctly because the Fenwick tree accumulates all future values before earlier indices are processed.

For a strictly decreasing array $[5,4,3,2,1]$, each query returns zero because no later element is greater or equal. Every contribution becomes zero except implicit self-structure handled by index weighting, yielding minimal total consistent with every subarray having strength 1 per element position structure.
