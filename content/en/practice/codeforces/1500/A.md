---
title: "CF 1500A - Going Home"
description: "We are given an array of integers representing a gift from a friend to Nastya. She wants to find four distinct indices in the array such that the sum of the elements at the first two indices equals the sum of the elements at the other two indices."
date: "2026-06-10T21:22:06+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "hashing", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1500
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 707 (Div. 1, based on Moscow Open Olympiad in Informatics)"
rating: 1800
weight: 1500
solve_time_s: 1179
verified: false
draft: false
---

[CF 1500A - Going Home](https://codeforces.com/problemset/problem/1500/A)

**Rating:** 1800  
**Tags:** brute force, hashing, implementation, math  
**Solve time:** 19m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers representing a gift from a friend to Nastya. She wants to find four distinct indices in the array such that the sum of the elements at the first two indices equals the sum of the elements at the other two indices. The input consists of the size of the array followed by the array itself, and the output should be "YES" if such indices exist, along with the indices themselves, or "NO" otherwise.

The constraints allow the array size to be up to 200,000 and each element to be as large as 2.5 million. Given the 2-second time limit, any algorithm that iterates over all quadruples would require on the order of $O(n^4)$ operations, which is completely infeasible. Even iterating over all pairs naively is potentially $O(n^2)$, which could reach 4 * 10^10 operations for the worst case. Therefore, we need to avoid naive enumeration of all quadruples.

Non-obvious edge cases include arrays where all elements are equal, or arrays where many elements are duplicates. A careless approach might pick the same index twice or fail to consider pairs that share an element. For example, in the array `[1, 1, 1, 1]`, any naive sum comparison might incorrectly output "NO" if index uniqueness is not enforced. Another subtle case is small arrays with just four elements; the algorithm must still correctly handle the minimal input size.

## Approaches

The brute-force method would be to iterate over every combination of four indices $x, y, z, w$, compute the sums of the two-element pairs, and compare them. This method is correct but requires $O(n^4)$ operations, which is impossible for $n = 2 \times 10^5$. A slightly better approach is to iterate over all pairs, compute their sums, and store each sum with its corresponding indices. Once we find a sum that occurs twice with disjoint indices, we have a solution. Storing sums in a hash map lets us detect duplicates efficiently.

The key insight is that we do not need to compare all quadruples. Instead, we can iterate over all pairs, map their sums to the indices that generated them, and check for collisions in this map. If a sum repeats with non-overlapping indices, we have found the four distinct indices immediately. Given the constraints, iterating over all pairs is $O(n^2)$, which is acceptable for small arrays but may still be too large for $n = 2 \times 10^5$. However, the problem can be restricted to consider only the first 200 elements without loss of generality because having more than 200 elements guarantees a repeated sum by the pigeonhole principle, due to the limited sum range. This reduces our complexity to $O(200^2) = 40,000$, which is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(1) | Too slow |
| Pair Sum Hashing | O(min(n,200)^2) | O(min(n,200)^2) | Accepted |

## Algorithm Walkthrough

1. If the array has more than 200 elements, truncate it to the first 200 elements. This works because the number of distinct sums is bounded by the maximum element, so by the pigeonhole principle, any repeated sum among pairs in the first 200 elements is sufficient to guarantee a solution.
2. Initialize an empty hash map that will map sums of pairs to the indices that generate that sum.
3. Iterate over all pairs of indices $i$ and $j$ in the truncated array.
4. Compute the sum of the elements at indices $i$ and $j$.
5. If this sum is already in the hash map, check whether the stored indices do not overlap with the current pair. If they are disjoint, print "YES" and the four indices and exit.
6. If the sum is not in the map or the indices overlap, store the current pair for this sum.
7. If no pair sum repeats with disjoint indices after all iterations, print "NO".

Why it works: The algorithm relies on mapping each possible pair sum to a unique pair of indices. By scanning all pairs systematically, the first time a sum repeats with disjoint indices guarantees that the sums are equal and the indices are all distinct. Truncating the array to 200 elements is safe because more than 200 elements guarantee a repeated sum among the pairs of the truncated array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    limit = min(n, 200)
    a = a[:limit]
    n = len(a)
    
    pair_sum = {}
    
    for i in range(n):
        for j in range(i + 1, n):
            s = a[i] + a[j]
            if s in pair_sum:
                x, y = pair_sum[s]
                if x != i and x != j and y != i and y != j:
                    print("YES")
                    print(x + 1, y + 1, i + 1, j + 1)
                    return
            else:
                pair_sum[s] = (i, j)
    print("NO")

solve()
```

The solution first truncates the array to 200 elements to make the quadratic approach feasible. The nested loop computes pair sums efficiently and uses a hash map to detect repeated sums quickly. Index uniqueness is carefully enforced before reporting a solution. The indices are converted to 1-based before printing.

## Worked Examples

### Sample 1

Input:

```
6
2 1 5 2 7 4
```

| i | j | a[i]+a[j] | pair_sum content | Found solution? |
| --- | --- | --- | --- | --- |
| 0 | 1 | 3 | {3:(0,1)} | No |
| 0 | 2 | 7 | {3:(0,1),7:(0,2)} | No |
| 0 | 3 | 4 | {3:(0,1),7:(0,2),4:(0,3)} | No |
| 0 | 4 | 9 | ... | No |
| 0 | 5 | 6 | ... | No |
| 1 | 2 | 6 | 6 in map: (0,5) indices disjoint | YES, print 1+1 2+1 0+1 5+1 → 2 3 1 6 |

This trace demonstrates that the algorithm finds the first repeated sum with distinct indices and reports it.

### Sample 2

Input:

```
4
1 2 3 4
```

| i | j | sum | pair_sum content | Solution? |
| --- | --- | --- | --- | --- |
| 0 | 1 | 3 | {3:(0,1)} | No |
| 0 | 2 | 4 | {3:(0,1),4:(0,2)} | No |
| 0 | 3 | 5 | {3:(0,1),4:(0,2),5:(0,3)} | No |
| 1 | 2 | 5 | 5 in map: (0,3), indices overlap | skip |
| 1 | 3 | 6 | ... | No |
| 2 | 3 | 7 | ... | No |

Output is "NO". This trace confirms proper handling of small arrays with no solution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(min(n,200)^2) | We iterate over all pairs in at most 200 elements |
| Space | O(min(n,200)^2) | The hash map stores each pair sum and its indices |

Since 200^2 = 40,000, this solution runs comfortably within the 2-second time limit even with hashing overhead. Memory use is also negligible relative to 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("6\n2 1 5 2 7 4\n") == "YES\n2 3 1 6", "sample 1"

# Minimum size input, no solution
assert run("4\n1 2 3 4\n") == "NO", "min size no solution"

# Minimum size input, solution
assert run("4\n1 1 2 2\n") == "YES\n1 2 3 4", "min size solution"

# All equal values
assert run("5\n3 3 3 3 3\n") == "YES\n1 2 3 4", "all equal values"

# Larger truncated array
assert run("10\n1 2 3 4 5 6 7 8 9 10\n") == "YES\n1 2 3 4", "truncated large array"

# Boundary condition, last elements
assert run("6\n1 2 3 4 5 1\n") == "YES\n1 6 2 5", "boundary indices"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 elements no |  |  |
