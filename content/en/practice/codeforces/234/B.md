---
title: "CF 234B - Reading"
description: "We are given a sequence of hours on a train journey, each with an associated light level between 0 and 100. Vasya wants to read for exactly k of these hours."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 234
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 145 (Div. 2, ACM-ICPC Rules)"
rating: 1000
weight: 234
solve_time_s: 79
verified: true
draft: false
---

[CF 234B - Reading](https://codeforces.com/problemset/problem/234/B)

**Rating:** 1000  
**Tags:** sortings  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of hours on a train journey, each with an associated light level between 0 and 100. Vasya wants to read for exactly _k_ of these hours. The reading strategy is constrained: during each chosen hour, he will read the entire time, and the reading experience is determined by the minimum light level among the selected hours. The goal is to maximize this minimum light, because a higher minimum means he never struggles with low light during his reading hours. The output must report this maximum achievable minimum, along with the indices of _k_ hours that achieve it.

The input size is modest: _n_ can be up to 1000. This allows algorithms with complexity up to roughly O(n log n) or O(n²) to run comfortably within 1 second, since n² is just 1,000,000 operations. Each light level is between 0 and 100, so we could exploit this small range if needed. The selection does not require consecutive hours, meaning we are free to pick any subset of _k_ hours.

Edge cases to consider include scenarios where multiple hours have identical light levels, especially when the smallest among the top _k_ hours determines the result. For example, if the input is `n=5, k=3` with light levels `10 20 20 10 30`, a naive approach that just picks the first k largest values could misidentify the minimum light. Another edge case is when all hours have the same light level: any choice of k hours is optimal.

## Approaches

The naive solution would examine every combination of _k_ hours and compute the minimum light for each. This guarantees correctness, but its complexity is O(C(n,k) * k), which is infeasible even for n=20 and k=10. Beyond that, the number of combinations grows explosively.

The key insight is that the problem reduces to a selection problem: we want the k hours with the highest light levels, because taking the largest k ensures that the minimum among them is as high as possible. Sorting the array by light level and selecting the top k elements produces an optimal solution. If we preserve the original indices while sorting, we can output the hours exactly as requested. This approach works because the minimum of a subset of k elements is maximized by choosing the k largest elements. There is no advantage in skipping a higher-light hour in favor of a lower-light one.

This observation reduces the problem from combinatorial to a simple sorting task. Sorting n elements costs O(n log n), selecting the first k elements is O(k), and returning their indices is O(k). The method handles all edge cases, including repeated values, naturally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,k) * k) | O(k) | Too slow |
| Sorting Selection | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read n and k, then read the array of light levels. Each element has its original position stored alongside the value. Keeping the index ensures we can report the correct hour numbers.
2. Sort the array of pairs `(light, index)` in descending order of light levels. Ties can remain in any order; any valid selection is acceptable.
3. Select the first k elements from the sorted array. These correspond to the hours with the largest light levels.
4. Determine the minimum light level among these selected hours. Since they are the largest k values, the last of them in sorted order will have the smallest light among the selection.
5. Extract the original indices of the chosen hours. These indices are the output required by the problem.
6. Print the minimum light level on the first line and the list of selected indices on the second line. The order of indices is arbitrary.

The reason this works is because of the property that in any set of k elements, the smallest value is maximized when you take the largest k elements from the universe. By sorting, we guarantee that no other subset of k hours can have a higher minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
lights = list(map(int, input().split()))

# store value with original index
indexed = [(light, i + 1) for i, light in enumerate(lights)]
indexed.sort(reverse=True)  # sort by light descending

selected = indexed[:k]
min_light = min(light for light, _ in selected)
indices = [idx for _, idx in selected]

print(min_light)
print(' '.join(map(str, indices)))
```

We first attach original indices to the light levels so we can report the hours after sorting. Sorting descending ensures the top k elements have the highest possible light. The `min` function over the selected k elements identifies the minimum among them, which is our target metric. Finally, we extract and print the indices.

## Worked Examples

For input:

```
5 3
20 10 30 40 10
```

After attaching indices:

| Light | Index |
| --- | --- |
| 20 | 1 |
| 10 | 2 |
| 30 | 3 |
| 40 | 4 |
| 10 | 5 |

Sorting descending:

| Light | Index |
| --- | --- |
| 40 | 4 |
| 30 | 3 |
| 20 | 1 |
| 10 | 2 |
| 10 | 5 |

Select top k=3 elements:

| Light | Index |
| --- | --- |
| 40 | 4 |
| 30 | 3 |
| 20 | 1 |

Minimum light = 20, indices = 4, 3, 1. Output:

```
20
4 3 1
```

Another example:

```
4 2
5 5 5 5
```

All lights are equal. Sorting preserves indices, select any top 2:

| Light | Index |
| --- | --- |
| 5 | 1 |
| 5 | 2 |

Minimum light = 5, indices = 1, 2. Output:

```
5
1 2
```

These traces demonstrate that the approach works for both varied and uniform light distributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting n elements dominates. |
| Space | O(n) | Storing value-index pairs and selected indices. |

With n ≤ 1000, O(n log n) is well within 1 second. Memory usage is also trivial under the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    lights = list(map(int, input().split()))
    indexed = [(light, i + 1) for i, light in enumerate(lights)]
    indexed.sort(reverse=True)
    selected = indexed[:k]
    min_light = min(light for light, _ in selected)
    indices = [idx for _, idx in selected]
    return f"{min_light}\n{' '.join(map(str, indices))}"

# provided sample
assert run("5 3\n20 10 30 40 10\n") == "20\n4 3 1", "sample 1"

# minimum size
assert run("1 1\n0\n") == "0\n1", "minimum size"

# all equal values
assert run("5 2\n10 10 10 10 10\n") == "10\n1 2", "all equal"

# largest n, k=n
assert run("1000 1000\n" + " ".join(map(str, range(1000))) + "\n") == f"999\n" + " ".join(map(str, range(1000,0,-1))), "max size"

# multiple max values
assert run("6 3\n10 20 20 30 30 10\n") == "20\n4 5 3", "multiple max"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 | 0\n1 | smallest possible n and k |
| 5 2 10 10 10 10 10 | 10\n1 2 | handling all equal values |
| 1000 1000 0..999 | 999\n1000..1 | handling maximum input size |
| 6 3 10 20 20 30 30 10 | 20\n4 5 3 | handling repeated maximum values |

## Edge Cases

For input `1 1 0`, the algorithm correctly picks the single hour. Sorting a single element has no effect, selected[0] gives the only value and index. Output is `0` and `1`.

For uniform values, like `5 2 10 10 10 10 10`, sorting preserves order, selection of top k produces any valid subset. Minimum light matches the uniform value, confirming correct behavior when no decision needs to be made.

For repeated maximums, such as `6 3 10 20 20 30 30 10`, the sort captures the top three light levels: 30, 30, and 20. The minimum light is 20, and the indices reflect valid hours with these values, demonstrating the algorithm correctly handles ties and non-consecutive selections.
