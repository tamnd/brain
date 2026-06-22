---
title: "CF 105315J - Hamza's Birthday"
description: "Each test case describes a collection of dishes, where every dish belongs to a specific restaurant and has a numeric taste value. The key constraint is that you cannot mix restaurants. You must pick exactly one restaurant and take all dishes belonging to it."
date: "2026-06-23T06:15:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105315
codeforces_index: "J"
codeforces_contest_name: "JPC 4.0"
rating: 0
weight: 105315
solve_time_s: 62
verified: true
draft: false
---

[CF 105315J - Hamza's Birthday](https://codeforces.com/problemset/problem/105315/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a collection of dishes, where every dish belongs to a specific restaurant and has a numeric taste value. The key constraint is that you cannot mix restaurants. You must pick exactly one restaurant and take all dishes belonging to it. The value of a chosen restaurant is determined by the weakest dish in it, meaning the minimum taste value among all its dishes. Your task is to identify the restaurant whose weakest dish is as strong as possible.

In more concrete terms, for every restaurant label, you group all its associated taste values, compute the minimum inside that group, and then among all these minima you pick the maximum one.

The input size goes up to a total of 500,000 dishes across all test cases, which immediately rules out any approach that repeatedly scans lists per query or recomputes minima from scratch for each restaurant choice. A solution that is quadratic in the number of dishes would be far too slow because even 10^5 operations per test case repeated 10^3 times already leads to unacceptable runtime.

A subtle edge case appears when multiple dishes belong to the same restaurant but arrive in arbitrary order. For example, if a restaurant has dishes with values 10, 2, and 7, the answer contribution from this restaurant is 2, regardless of order. A naive approach that only tracks the last seen value per restaurant would incorrectly output 7 in this case if the smallest value appears earlier and gets overwritten.

Another edge case arises when every restaurant has exactly one dish. Then the answer is simply the maximum di, since each restaurant’s minimum is its only value. Any incorrect grouping logic that accidentally merges restaurants would fail here.

## Approaches

The brute-force approach is to treat each restaurant independently. For every restaurant label, we collect all its dishes and explicitly compute the minimum by scanning the full list of dishes assigned to it. If there are n dishes and potentially n distinct restaurants, then in the worst case we repeatedly rescan almost the entire array for each restaurant. This leads to a worst-case operation count on the order of n squared, which becomes roughly 10^10 operations at maximum constraints, far beyond what a 2-second limit can handle.

The key observation is that we never actually need to recompute anything. Each dish contributes exactly one value to exactly one restaurant group, and the only information that matters per group is its minimum. This suggests maintaining a running minimum per restaurant as we read the input once. Instead of revisiting data, we update a dictionary keyed by restaurant id, storing the smallest value seen so far.

This transforms the problem into a single pass aggregation problem. Each update is constant time, and after processing all dishes, we only need to scan the collected minima to find the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently, building a mapping from restaurant id to its current minimum dish value.

1. Initialize an empty dictionary that will store, for each restaurant, the smallest taste value seen so far. This structure is necessary because we need constant-time updates per dish.
2. Read each dish one by one. For a dish belonging to restaurant a with value d, check whether a has been seen before. If it has not, store d directly as its current minimum.
3. If the restaurant already exists in the dictionary, update its stored value only if the new dish has a smaller value. This ensures we never lose track of the weakest dish in that restaurant.
4. After processing all dishes, iterate over all stored minima and compute the maximum among them. This final step selects the best possible restaurant according to the required criterion.
5. Output this maximum value for the test case.

The reason this works is that every restaurant’s contribution is fully determined by its minimum value, and that minimum can be maintained incrementally without needing the full list of dishes again.

### Why it works

At any point during processing, the dictionary stores the exact minimum of all processed dishes for each restaurant. This is an invariant preserved by only replacing stored values when a smaller one appears. Since every dish is processed exactly once, by the end of input the stored value for each restaurant is exactly the global minimum of that restaurant’s full set. Taking the maximum over these correct minima yields the optimal restaurant choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        best = {}
        for _ in range(n):
            a, d = map(int, input().split())
            if a in best:
                if d < best[a]:
                    best[a] = d
            else:
                best[a] = d

        ans = 0
        for v in best.values():
            if v > ans:
                ans = v
        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core of the implementation is the dictionary `best`, which stores the current minimum value per restaurant. The update step is carefully written to avoid unnecessary function calls or merges. The final loop is separate because mixing aggregation with reading would complicate correctness reasoning and risk missing the final comparison across all restaurants.

One subtle point is initialization of `ans`. It is safe to start from 0 because all dish values are positive as given in the constraints. If values could be negative, initialization would need to be adjusted to negative infinity or the first dictionary value.

## Worked Examples

### Example 1

Input:

```
1
4
4 5
10 7
4 6
10 2
```

We track restaurant minima step by step.

| Step | Restaurant | Value | Stored state |
| --- | --- | --- | --- |
| 1 | 4 | 5 | {4: 5} |
| 2 | 10 | 7 | {4: 5, 10: 7} |
| 3 | 4 | 6 | {4: 5, 10: 7} |
| 4 | 10 | 2 | {4: 5, 10: 2} |

After processing, we take max over minima {5, 2}, giving 5.

This trace shows that repeated updates only refine the stored minimum, and order does not affect correctness.

### Example 2

Input:

```
1
3
1 10
2 3
3 7
```

| Step | Restaurant | Value | Stored state |
| --- | --- | --- | --- |
| 1 | 1 | 10 | {1: 10} |
| 2 | 2 | 3 | {1: 10, 2: 3} |
| 3 | 3 | 7 | {1: 10, 2: 3, 3: 7} |

Final minima are {10, 3, 7}, so answer is 10.

This case confirms that when each restaurant has a single dish, the solution reduces correctly to a simple maximum over values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | each dish is processed once and each dictionary operation is O(1) average |
| Space | O(k) | k is number of distinct restaurants stored in the dictionary |

The total n across test cases is at most 5 × 10^5, so a linear solution comfortably fits within time limits. Memory usage is bounded by storing at most one entry per restaurant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        best = {}
        for _ in range(n):
            a, d = map(int, input().split())
            if a in best:
                best[a] = min(best[a], d)
            else:
                best[a] = d

        ans = max(best.values())
        out.append(str(ans))

    return "\n".join(out)

# provided sample-style test
assert run("""1
4
4 5
10 7
4 6
10 2
""") == "5"

# minimum size
assert run("""1
1
1 100
""") == "100"

# all same restaurant
assert run("""1
3
5 10
5 3
5 7
""") == "3"

# multiple restaurants, mixed order
assert run("""1
6
1 8
2 6
1 4
3 9
2 1
3 7
""") == "7"

# all unique restaurants
assert run("""1
4
1 5
2 4
3 3
4 2
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single dish | 100 | minimum boundary case |
| same restaurant repeated | 3 | correct minimum tracking |
| mixed updates | 7 | order independence |
| all unique | 5 | max over single-element groups |

## Edge Cases

One important edge case is when a restaurant appears many times with decreasing values over time. For example, input:

```
1
4
1 10
1 5
1 7
1 3
```

The algorithm updates the stored value step by step:

first 10, then 5, then remains 5 after 7, then becomes 3. The invariant that the stored value is always the minimum seen so far guarantees correctness, and the final output is 3.

Another case is when multiple restaurants compete closely:

```
1
5
1 10
2 9
3 8
4 7
5 6
```

Each restaurant has a single value, so the dictionary stores all values unchanged. The final maximum correctly returns 10, showing that the algorithm reduces to a simple maximum selection when no grouping refinement is needed.
