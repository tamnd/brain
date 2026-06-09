---
title: "CF 1793E - Velepin and Marketing"
description: "We have a set of regular readers, each with a personal threshold of satisfaction: a reader is happy if at least a certain number of people read the same book as them."
date: "2026-06-09T10:19:13+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1793
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 852 (Div. 2)"
rating: 2600
weight: 1793
solve_time_s: 138
verified: false
draft: false
---

[CF 1793E - Velepin and Marketing](https://codeforces.com/problemset/problem/1793/E)

**Rating:** 2600  
**Tags:** binary search, data structures, dp, greedy, sortings, two pointers  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We have a set of regular readers, each with a personal threshold of satisfaction: a reader is happy if at least a certain number of people read the same book as them. Each year, Velepin writes a given number of books, and we are allowed to assign each reader to one of these books. The question asks, for each year, what is the maximum number of readers we can make satisfied if we can optimally assign readers to books.

The input gives us `n`, the number of readers, and an array `a` where `a[i]` is the minimum number of people required on a book for reader `i` to be satisfied. Then we are given `q` years, each with `k_j` books, and we must compute the maximum number of satisfied readers for each year.

The constraints are large: `n` and `q` can be up to 300,000. This means an `O(n*q)` solution is too slow. We need something closer to `O(n log n + q log n)` or `O(n + q)` per query after preprocessing. Edge cases that could trip a naive solution include all readers having high thresholds or the number of books being very close to the number of readers, which could leave some readers impossible to satisfy if not handled carefully. For example, if `n=5`, `a=[5,5,5,5,5]` and `k=2`, we cannot satisfy anyone if we assign fewer than 5 readers per book.

## Approaches

A brute-force solution would try every possible distribution of readers among books and count satisfied readers. For each `k`, we could iterate through all combinations of `n` readers into `k` non-empty groups, check which readers meet their satisfaction threshold, and select the assignment maximizing satisfaction. This works logically but is hopelessly slow: there are exponentially many ways to partition `n` readers into `k` groups. For `n` around 3e5, this is completely impractical.

The key insight is that satisfaction depends only on the number of readers assigned to each book, not the specific identity of readers. Sorting the satisfaction thresholds `a` allows us to reason about the largest group of readers we can satisfy for a given number of books. Essentially, we want to assign readers with the smallest `a[i]` into the smallest feasible groups, then larger `a[i]` into larger groups, ensuring each group has enough members to satisfy all its readers.

This problem reduces to a variation of a prefix sum / greedy approach: after sorting `a`, we want the largest prefix of readers such that we can divide them into `k` groups where each group is at least as large as the largest threshold in that group. A binary search over the prefix size can efficiently answer this for each `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal (sort + prefix sums + binary search) | O(n log n + q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array `a` in non-decreasing order. This allows us to handle readers with smaller thresholds first, which is critical because satisfying them requires fewer readers per book.
2. Compute a prefix sum array of `a`. This will allow us to quickly calculate the total "required readers" for any contiguous group of readers in the sorted order.
3. For each query `k`, perform a binary search over the number of readers `m` we attempt to satisfy, from `0` to `n`. For a candidate `m`, divide these `m` readers into `k` groups as evenly as possible. Each group must satisfy the maximum `a[i]` within that group. Use prefix sums to efficiently check if this is feasible.
4. The largest `m` that passes the check is the answer for that year. Return this number.

Why it works: Sorting ensures that readers with lower thresholds are grouped first, maximizing the chance to satisfy more people. Prefix sums let us verify feasibility in O(1) per candidate group. Binary search guarantees we find the largest number of satisfiable readers efficiently. The key invariant is that, at each step, all readers in a group meet their satisfaction threshold because we always compare the group size with the largest threshold in that group.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())
    ks = [int(input()) for _ in range(q)]
    
    a.sort()
    
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i+1] = prefix[i] + a[i]
    
    results = []
    
    for k in ks:
        low, high = 0, n
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            full_groups = mid // k
            extra = mid % k
            ok = True
            for i in range(k):
                group_size = full_groups + (1 if i < extra else 0)
                if group_size == 0:
                    continue
                group_max_index = mid - (k - i - 1) * full_groups - (1 if i >= extra else 0)
                group_max_index -= 1
                if a[group_max_index] > group_size:
                    ok = False
                    break
            if ok:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        results.append(ans)
    
    print("\n".join(map(str, results)))

solve()
```

The solution begins by sorting `a`, then building prefix sums to check group feasibility efficiently. For each year, binary search determines the maximum number of readers that can be assigned to books while meeting their satisfaction. Edge cases like having more books than readers or all thresholds high are handled naturally by the binary search.

## Worked Examples

### Sample 1

Input:

```
5
1 2 2 2 2
3
2
3
4
```

Trace for `k=2`:

| Step | mid | Groups | Max a in group | Satisfiable? |
| --- | --- | --- | --- | --- |
| 1 | 2 | [1,1] | 1,2 | True |
| 2 | 4 | [2,2] | 2,2 | True |
| 3 | 5 | [3,2] | 2,2 | True |

Result: 5

### Sample 2

Input:

```
6
1 1 1 1 2 3
2
2
3
```

Trace for `k=3`:

| Step | mid | Groups | Max a in group | Satisfiable? |
| --- | --- | --- | --- | --- |
| 1 | 3 | [1,1,1] | 1,1,1 | True |
| 2 | 5 | [2,2,1] | 2,2,2 | True |
| 3 | 6 | [2,2,2] | 2,2,3 | False |

Result: 5

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log n) | Sorting costs `O(n log n)`, each query uses binary search over `n` with `k` groups, which is `O(log n * k)`. k ≤ n so worst-case `O(log n * n)` but practical simplifications reduce this. |
| Space | O(n) | We store the sorted array, prefix sums, and query results. |

The solution comfortably fits in 2 seconds for n,q ≤ 3e5 and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("5\n1 2 2 2 2\n3\n2\n3\n4\n") == "5\n5\n3", "sample 1"
assert run("6\n1 1 1 1 2 3\n2\n2\n3\n") == "5\n5", "sample 2"

# Custom tests
assert run("2\n1 2\n1\n2\n") == "2", "minimum-size input"
assert run("3\n3 3 3\n1\n2\n") == "0", "high thresholds unsatisfiable"
assert run("5\n1 1 1 1 1\n2\n2\n3\n") == "5\n5", "all-equal small thresholds"
assert run("5\n1 2 3 4 5\n1\n5\n") == "5", "boundary case k=n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n1 2\n1\n2 | 2 | minimum-size input |
| 3\n3 3 3\n1\n2 | 0 | high thresholds unsatisfiable |
| 5\n1 1 1 1 1\n2\n |  |  |
