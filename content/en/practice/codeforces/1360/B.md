---
problem: 1360B
contest_id: 1360
problem_index: B
name: "Honest Coach"
contest_name: "Codeforces Round 644 (Div. 3)"
rating: 800
tags: ["greedy", "sortings"]
answer: passed_samples
verified: true
solve_time_s: 218
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e3de0-0334-83ec-9ad2-5a24d5b4b9f9
---

# CF 1360B - Honest Coach

**Rating:** 800  
**Tags:** greedy, sortings  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 38s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e3de0-0334-83ec-9ad2-5a24d5b4b9f9  

---

## Solution

## Problem Understanding

We are given several independent test cases. In each case we receive a list of athlete strengths, and we must divide the athletes into two non-empty groups so that one group contributes its maximum value and the other contributes its minimum value, and the absolute difference between those two values is as small as possible.

A useful way to rephrase the goal is that we are trying to split the multiset of values into two parts such that the boundary between the two parts, in terms of value space, is as tight as possible. One group will contain some subset of strengths, and we care only about its maximum, while the other group contributes only its minimum. The actual membership of the remaining elements inside each group does not affect the score beyond preserving those two extremes.

The constraints are small. Each test case has at most 50 elements and there are at most 1000 test cases. This immediately rules out any exponential partitioning strategy per test case. Even a solution that is quadratic per test case is safe, since 50 squared is only 2500 operations.

The main subtlety is that the grouping is not constrained by positions or ordering, only by value selection. This means any reasoning based on adjacency in the input array is irrelevant, and only the sorted order of values matters.

A common mistake is to try to assign elements greedily without sorting. For example, one might try to build two sets by alternating assignment or splitting around the median of indices. That fails because optimality depends on numeric closeness, not original order.

Another failure mode appears when assuming the best split is around the median value. This is not always correct because duplicates or uneven gaps can make a different cut optimal. For instance, if values are `[1, 2, 100, 101]`, splitting between 2 and 100 is clearly optimal, but if values are `[1, 2, 3, 100]`, the best split is between 3 and 100, not around the median index.

## Approaches

The brute-force approach is to try every possible partition of the array into two non-empty sets. For each partition, compute the maximum of one set and the minimum of the other, then evaluate the absolute difference. There are `2^n` possible partitions, and for each we would need up to `O(n)` work to compute maxima and minima, leading to `O(n·2^n)` complexity per test case. With `n = 50`, this is far beyond feasible limits.

The key observation is that the value depends only on the boundary between two sets in the sorted order. Once we sort the array, we can think of choosing a split point that determines which values go to the left group and which go to the right group. Any optimal partition can be transformed into one where all elements in group A are less than or equal to all elements in group B. If this property were violated, swapping elements would only improve or preserve the objective.

After sorting, the candidate answer reduces to checking all adjacent pairs in the sorted array. If we split between positions `i` and `i+1`, then the best possible contribution is `|s[i] - s[i+1]|`, because group A can end at `s[i]` and group B can start at `s[i+1]`. Any other assignment that introduces a larger gap would only increase the difference.

Thus, the problem collapses into finding the minimum difference between consecutive elements in the sorted array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the list of strengths for the current test case. The goal is to prepare the data so that comparisons reflect value proximity rather than input order.
2. Sort the array in non-decreasing order. This step is essential because it aligns all potentially optimal splits next to each other in value space. Without sorting, adjacent differences have no meaning.
3. Initialize a variable `best` with a large value. This will store the smallest difference found between valid split boundaries.
4. Iterate through the sorted array from index 1 to n−1. At each position, compute the difference between the current element and the previous one. This represents the cost of splitting the array between these two values.
5. Update `best` whenever a smaller difference is found. This ensures we always track the tightest possible separation between two groups.
6. After processing all adjacent pairs, output `best` as the answer for the test case.

### Why it works

After sorting, any valid partition can be seen as choosing a threshold that separates the array into two non-empty parts. The value of the partition depends only on the largest element on the left side and the smallest element on the right side. The smallest possible gap between such a pair must occur between two consecutive elements in sorted order, because any larger jump would skip over a closer candidate pair. Therefore, scanning adjacent differences is sufficient to guarantee the optimal split.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = list(map(int, input().split()))
    
    s.sort()
    
    best = float('inf')
    for i in range(1, n):
        best = min(best, s[i] - s[i - 1])
    
    print(best)
```

The solution first sorts each test case, which is the structural transformation that makes the problem one-dimensional in value space. The loop over adjacent pairs directly encodes the only meaningful split points.

The subtraction `s[i] - s[i - 1]` is safe because the array is sorted, so the difference is always non-negative and represents the exact cost of splitting between those two elements.

The initialization of `best` with infinity avoids any special-case handling for the first comparison.

## Worked Examples

### Example 1

Input:

```
5
3 1 2 6 4
```

Sorted array:

`[1, 2, 3, 4, 6]`

| i | Pair | Difference | best |
| --- | --- | --- | --- |
| 1 | (1,2) | 1 | 1 |
| 2 | (2,3) | 1 | 1 |
| 3 | (3,4) | 1 | 1 |
| 4 | (4,6) | 2 | 1 |

The smallest gap is 1, corresponding to multiple valid splits. This confirms that the optimal partition depends only on the closest adjacent values.

### Example 2

Input:

```
4
7 9 3 1
```

Sorted array:

`[1, 3, 7, 9]`

| i | Pair | Difference | best |
| --- | --- | --- | --- |
| 1 | (1,3) | 2 | 2 |
| 2 | (3,7) | 4 | 2 |
| 3 | (7,9) | 2 | 2 |

The optimal answer is 2, achieved by either split between 1 and 3 or between 7 and 9. This shows that multiple optimal boundaries can exist, and the algorithm correctly captures the minimum among them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates, linear scan follows |
| Space | O(1) extra space | Only a few variables are used aside from input storage |

Given `n ≤ 50` and `t ≤ 1000`, the total work is trivial under constraints. Even the worst-case 1000 sorts of size 50 are negligible.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = list(map(int, input().split()))
        s.sort()
        best = float('inf')
        for i in range(1, n):
            best = min(best, s[i] - s[i - 1])
        out.append(str(best))
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("""5
5
3 1 2 6 4
6
2 1 3 2 4 3
4
7 9 3 1
2
1 1000
3
100 150 200
""") == """1
0
2
999
50"""

# custom cases
assert run("""1
2
10 20
""") == "10"

assert run("""1
5
5 5 5 5 5
""") == "0"

assert run("""1
6
1 100 101 102 200 300
""") == "1"

assert run("""1
4
1 2 100 101
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10 20` | `10` | minimal size and simple split |
| all equal values | `0` | zero-gap handling |
| mixed clusters | `1` | closest pair across boundary |
| separated clusters | `1` | ensures correct adjacent reasoning |

## Edge Cases

One edge case is when all values are identical. For input `[5, 5, 5, 5]`, sorting keeps it unchanged, and every adjacent difference is zero. The algorithm correctly returns zero because any split produces identical max and min across groups.

Another case is when the best split is not near the extremes but in the middle of a cluster structure, such as `[1, 100, 101, 102, 200]`. Sorting gives the same sequence, and the smallest adjacent gap is between `100` and `101`, which correctly represents the optimal partition boundary.

A final case is the smallest possible input size `n = 2`. The algorithm performs a single comparison and returns the difference between the only two elements, which is the only valid split.