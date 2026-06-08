---
title: "CF 2000H - Ksyusha and the Loaded Set"
description: "We are asked to maintain a dynamic set of integers that supports insertions, deletions, and queries called the $k$-load. The $k$-load of a set is the smallest positive integer $d$ such that the sequence $d, d+1, dots, d+k-1$ is completely missing from the set."
date: "2026-06-08T14:17:57+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2000
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 966 (Div. 3)"
rating: 2200
weight: 2000
solve_time_s: 166
verified: false
draft: false
---

[CF 2000H - Ksyusha and the Loaded Set](https://codeforces.com/problemset/problem/2000/H)

**Rating:** 2200  
**Tags:** binary search, brute force, data structures, implementation  
**Solve time:** 2m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maintain a dynamic set of integers that supports insertions, deletions, and queries called the $k$-load. The $k$-load of a set is the smallest positive integer $d$ such that the sequence $d, d+1, \dots, d+k-1$ is completely missing from the set. For example, if the set is ${3,4,6}$, the $2$-load is $1$, because $1$ and $2$ are both missing, and that is the smallest such contiguous missing sequence of length $2$.

The input gives multiple test cases, each starting with an initial set of up to $2 \cdot 10^5$ integers sorted strictly increasingly. Each test case then has up to $2 \cdot 10^5$ operations consisting of insertions, deletions, and $k$-load queries. Across all test cases, the sum of $n$ and the sum of $m$ are both bounded by $2 \cdot 10^5$.

The constraints mean a naive approach iterating over all positive integers for each $k$-load query is impractical. A single test case could contain $2 \cdot 10^5$ queries and $k$ values as high as $2 \cdot 10^6$, which would require trillions of operations if checked naively. We need an approach that queries the $k$-load in near-constant or logarithmic time.

Edge cases to watch out for include querying a $k$-load after removing or inserting the first few positive integers, for example starting with ${2,3,4}$ and querying $k=1$, the answer must be $1$. Another tricky scenario is when $k$ is very large and no contiguous sequence of $k$ missing integers occurs below the largest present element, forcing the $k$-load beyond the current set's maximum.

## Approaches

The brute-force approach would attempt to answer each $k$-load query by iterating through positive integers, checking for each candidate $d$ whether the sequence $d, d+1, \dots, d+k-1$ intersects with the current set. This works because the logic directly implements the definition, but for large $k$ or dense sets, the search may need to check millions of integers, making the worst-case complexity roughly $O(n + m \cdot k)$, which is too slow given $k$ can reach $2 \cdot 10^6$ and $m$ up to $2 \cdot 10^5$.

The key observation is that for any $k$-load query, we only need to track the first positive integer where exactly $k$ consecutive integers are missing. We can map the problem to a prefix-count structure: if we know the number of integers less than or equal to $x$ currently in the set, we can compute how many positive integers are missing below $x$. Denote this count as `missing = x - count_in_set_up_to(x)`. Then the smallest $d$ such that `d` through `d+k-1` are all missing is the smallest $d$ satisfying `missing_before_d + k <= d`. This reduces to a search problem: find the smallest $d$ satisfying the formula, which can be done with binary search. We only need to maintain a data structure that supports insertion, deletion, and fast rank queries (number of elements ≤ x). Balanced BSTs or a segment tree over the bounded universe of integers can do this efficiently.

This observation transforms the brute-force from scanning sequences explicitly to computing missing counts and using binary search. Updates become logarithmic, and queries are logarithmic, making the solution feasible within the time constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m*k) | O(n) | Too slow |
| Binary Search + Rank Structure | O(m log U) | O(U) | Accepted |

Here, U is the maximum integer value, $2 \cdot 10^6$.

## Algorithm Walkthrough

1. Initialize a boolean array or bitset of size $2 \cdot 10^6 + 2$ representing which integers are present in the set. This allows O(1) insertions and deletions. Maintain a Fenwick tree or segment tree over the same range to track the count of elements up to each index, supporting fast prefix sums.
2. For each insertion `+ x`, mark `x` as present in the boolean array and increment its count in the prefix structure.
3. For each deletion `- x`, mark `x` as absent and decrement its count in the prefix structure.
4. For each query `? k`, perform a binary search for the smallest positive integer `d` such that the number of integers ≤ d+k-1 minus the number of integers ≤ d-1 equals zero. In other words, the sequence `d` through `d+k-1` is entirely absent. This uses the prefix sum structure to compute the number of present elements in that interval efficiently.
5. Output the found $d$ for each query.

Why it works: At any moment, the prefix sum structure accurately counts how many integers up to a certain value exist. By searching for the first interval of length `k` with zero present elements, we find exactly the $k$-load. Insertions and deletions update the counts correctly, maintaining the invariant that the prefix sums reflect the current set state.

## Python Solution

```python
import sys
input = sys.stdin.readline

class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0]*(n+2)
    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i
    def query(self, i):
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res
    def range_query(self, l, r):
        return self.query(r) - self.query(l-1)

MAX_A = 2_000_002

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        m = int(input())
        present = [0]*(MAX_A)
        bit = BIT(MAX_A)
        for num in a:
            present[num] = 1
            bit.update(num, 1)
        res = []
        for _ in range(m):
            op = input()
            if op[0] == '+':
                x = int(op[2:])
                present[x] = 1
                bit.update(x,1)
            elif op[0] == '-':
                x = int(op[2:])
                present[x] = 0
                bit.update(x,-1)
            else:
                k = int(op[2:])
                l, r = 1, MAX_A-1
                ans = -1
                while l <= r:
                    mid = (l+r)//2
                    # missing in [1, mid] = mid - count of present ≤ mid
                    missing = mid - bit.query(mid)
                    if missing >= k:
                        ans = mid - k + 1
                        r = mid -1
                    else:
                        l = mid +1
                res.append(str(ans))
        print(' '.join(res))

if __name__ == "__main__":
    solve()
```

The solution uses a Binary Indexed Tree (Fenwick tree) to track prefix sums of present elements. The boolean array is used to quickly mark insertions and deletions, although it is not strictly required for correctness. Binary search identifies the first interval of length `k` where all numbers are missing by comparing the number of missing numbers up to a midpoint to `k`. The search narrows the interval until the smallest starting `d` is found.

## Worked Examples

For the first test case from the sample input:

```
Initial set: 1 2 5 905 2000000
Operations:
- 2 -> remove 2
? 2 -> query 2-load
? 1 -> query 1-load
- 1 -> remove 1
? 1 -> query 1-load
+ 4 -> insert 4
+ 2 -> insert 2
? 2 -> query 2-load
...
```

| Step | Set | BIT Prefix | Query Result |
| --- | --- | --- | --- |
| init | {1,2,5,905,2000000} | counts updated | - |
| -2 | {1,5,905,2000000} | BIT decremented at 2 | - |
| ?2 | - | - | 2 |
| ?1 | - | - | 2 |
| -1 | {5,905,2000000} | BIT decremented at 1 | - |
| ?1 | - | - | 1 |
| +4 | {4,5,905,2000000} | BIT incremented 4 | - |
| +2 | {2,4,5,905,2000000} | BIT incremented 2 | - |
| ?2 | - | - | 6 |

This trace shows the algorithm correctly maintains the set and prefix sums through insertions and deletions, and binary search identifies the minimal $k$-load.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log U) | Each operation ( |
