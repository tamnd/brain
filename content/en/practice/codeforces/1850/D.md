---
title: "CF 1850D - Balanced Round"
description: "We are given a list of problem difficulties, and we are allowed to discard any subset of them and then reorder the remaining ones arbitrarily. After reordering, we want the sequence to be “smooth” in the sense that every adjacent pair differs by at most $k$."
date: "2026-06-09T05:32:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1850
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 886 (Div. 4)"
rating: 900
weight: 1850
solve_time_s: 190
verified: false
draft: false
---

[CF 1850D - Balanced Round](https://codeforces.com/problemset/problem/1850/D)

**Rating:** 900  
**Tags:** brute force, greedy, implementation, sortings  
**Solve time:** 3m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of problem difficulties, and we are allowed to discard any subset of them and then reorder the remaining ones arbitrarily. After reordering, we want the sequence to be “smooth” in the sense that every adjacent pair differs by at most $k$.

The goal is not to construct the sequence itself, but to keep as many problems as possible so that such an ordering exists. Equivalently, we want to find the maximum number of elements we can retain that can be arranged into a valid sequence, and then subtract that from $n$.

The key observation hidden in the freedom of reordering is that adjacency constraints depend only on whether we can connect values through steps of size at most $k$, not on their original positions.

From the constraints, $n$ can be up to $2 \cdot 10^5$ across test cases, so anything quadratic in a single test case is already too slow. Sorting-based or linear scanning solutions are expected. Since values go up to $10^9$, we cannot rely on frequency arrays or direct indexing.

A subtle failure case appears when values are “almost connected” but require skipping intermediate elements.

For example, if $k = 2$ and values are $[1, 10, 11, 12]$, a naive idea might try to greedily extend from 1, but 1 cannot connect to 10, even though 10, 11, 12 form a long valid block. The correct answer depends on identifying the largest structure where consecutive values stay within distance $k$, not on starting from an arbitrary point.

Another pitfall is assuming we need to preserve global ordering or simulate transitions. Since rearrangement is free, the problem reduces to selecting a multiset that can be arranged in a chain with bounded gaps.

## Approaches

The brute-force view is to try every subset of problems, and for each subset try to arrange them in some order and check if all adjacent differences are within $k$. Even if we assume checking a fixed subset is $O(n \log n)$ after sorting, the number of subsets is $2^n$, which is infeasible even for $n = 40$. This makes it clear we need a structural reduction rather than enumeration.

The key insight comes from sorting the array. Once sorted, any valid arrangement must come from selecting elements that can be chained in sorted order. If two chosen elements differ by more than $k$, they cannot be adjacent in any valid ordering without breaking monotonicity somewhere else, because inserting intermediate values would only worsen gaps.

So the problem becomes finding the largest subset such that after sorting, consecutive chosen elements differ by at most $k$. This is equivalent to finding the longest segment we can traverse while maintaining gaps ≤ $k$, but with a twist: we are allowed to skip elements, so we are really looking for the largest connected component under the relation “difference ≤ k between some chain neighbors”.

In sorted order, we can think of building a graph where edges connect indices $i, j$ if $a_j - a_i \le k$. The structure is monotone, so we can use a sliding window: as we move a right pointer, we ensure the left pointer stays within a range where connectivity is preserved. The best we can do is keep the largest window where the maximum gap between consecutive kept elements is ≤ $k$.

This reduces to grouping the sorted array into contiguous segments where adjacent differences are ≤ $k$. Inside each segment, we can keep all elements. Between segments, no element can bridge the gap, so they are independent.

Thus the answer is $n - \max(\text{size of a segment where consecutive differences} \le k)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n \log n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ per test | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Sort the array of difficulties in non-decreasing order.

Sorting is necessary because adjacency in an optimal arrangement will always respect increasing order; any reordering that mixes far apart values does not help bridge gaps.
2. Scan through the sorted array and track the longest contiguous block where each consecutive difference is at most $k$.

This block represents a group where we can place all elements in order without breaking the constraint.
3. Maintain a current segment length that resets whenever a gap greater than $k$ appears.

A large gap acts as a hard barrier: no valid adjacency can cross it.
4. Keep the maximum segment length seen during the scan.
5. The answer is $n - \text{maximum segment length}$, since we remove everything outside the best achievable block.

### Why it works

After sorting, any valid arrangement must respect the fact that large gaps cannot be bridged by intermediate values unless those intermediate values lie between them in sorted order. This forces any valid selection to lie entirely within a region where consecutive elements differ by at most $k$. Each time a gap exceeds $k$, the sequence splits into independent components that cannot be merged in any ordering. The optimal solution therefore keeps the largest such component, since within it all elements can be arranged consecutively without violating the constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort()
        
        best = 1
        cur = 1
        
        for i in range(1, n):
            if a[i] - a[i - 1] <= k:
                cur += 1
            else:
                best = max(best, cur)
                cur = 1
        
        best = max(best, cur)
        
        print(n - best)

if __name__ == "__main__":
    solve()
```

The solution first sorts the array so that all potential adjacency relations become local. It then performs a single linear scan, grouping elements into maximal segments where each adjacent difference is within the allowed threshold $k$. The variable `cur` tracks the current segment length, and `best` tracks the largest such segment encountered.

The only subtle detail is the final update after the loop ends, since the last segment may be the largest and would otherwise be missed.

## Worked Examples

### Example 1

Input:

```
n = 5, k = 1
a = [1, 2, 4, 5, 6]
```

After sorting (already sorted), we scan:

| i | a[i] | diff | cur | best |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | 1 | 1 |
| 1 | 2 | 1 | 2 | 1 |
| 2 | 4 | 2 | 1 | 2 |
| 3 | 5 | 1 | 2 | 2 |
| 4 | 6 | 1 | 3 | 2 |

Final best segment is 3, corresponding to $[4,5,6]$.

Answer is $5 - 3 = 2$.

This shows that isolated small values like 1 and 2 are not useful if they are separated by a forbidden gap.

### Example 2

Input:

```
n = 4, k = 2
a = [2, 4, 6, 8]
```

| i | a[i] | diff | cur | best |
| --- | --- | --- | --- | --- |
| 0 | 2 | - | 1 | 1 |
| 1 | 4 | 2 | 2 | 1 |
| 2 | 6 | 2 | 3 | 2 |
| 3 | 8 | 2 | 4 | 3 |

All elements form a single valid chain, so best = 4 and answer = 0.

This confirms that when all consecutive gaps are within $k$, no removals are needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates per test case, scan is linear |
| Space | $O(1)$ extra | Only counters used beyond input storage |

The total $n$ across test cases is bounded by $2 \cdot 10^5$, so sorting and scanning remains well within limits. The algorithm is efficient enough for worst-case inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import builtins
    
    input = sys.stdin.readline
    
    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, k = map(int, input().split())
            a = list(map(int, input().split()))
            a.sort()
            best = 1
            cur = 1
            for i in range(1, n):
                if a[i] - a[i - 1] <= k:
                    cur += 1
                else:
                    best = max(best, cur)
                    cur = 1
            best = max(best, cur)
            out.append(str(n - best))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""7
5 1
1 2 4 5 6
1 2
10
8 3
17 3 1 20 12 5 17 12
4 2
2 4 6 8
5 3
2 3 19 10 8
3 4
1 10 5
8 1
8 3 1 4 5 10 7 3
""") == """2
0
5
0
3
1
4"""

# all equal
assert run("""1
5 10
7 7 7 7 7
""") == "0"

# single element
assert run("""1
1 100
42
""") == "0"

# large gap splitting
assert run("""1
6 2
1 2 3 10 11 12
""") == "0"

# chain break
assert run("""1
5 1
1 3 5 7 9
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | no removals needed |
| single element | 0 | base case |
| split into two perfect blocks | 0 | only largest block matters |
| strict alternating gaps | 4 | maximum fragmentation case |

## Edge Cases

When all elements are identical, sorting produces zero differences everywhere, so the scan forms a single segment of length $n$. The algorithm keeps `best = n`, leading to output 0, which matches the fact that any ordering is already balanced.

When $n = 1$, the loop never runs, and `best` remains 1. The answer becomes 0, consistent with a trivial valid round.

When the array splits into two clusters separated by a large gap, such as $[1,2,3,100,101,102]$ with small $k$, the scan produces two segments. The algorithm correctly keeps only the larger one, since no adjacency is possible across the gap.

When values alternate with gaps always larger than $k$, every element becomes its own segment. The maximum segment size is 1, so the answer becomes $n-1$, reflecting that only one problem can be kept.
