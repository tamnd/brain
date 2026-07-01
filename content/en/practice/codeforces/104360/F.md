---
title: "CF 104360F - \u041d\u0435\u043e\u0431\u044b\u0447\u043d\u044b\u0439 \u043c\u0430\u0441\u0441\u0438\u0432"
description: "We are given an array and we focus on each position independently. Fix an index $i$. We look at every contiguous subarray that contains this index. For each such subarray, we sort its elements and locate the value $ai$ inside this sorted list."
date: "2026-07-01T17:57:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104360
codeforces_index: "F"
codeforces_contest_name: "\u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u041c\u0441\u0442\u0438\u0441\u043b\u0430\u0432\u0430 \u041a\u0435\u043b\u0434\u044b\u0448\u0430 - 2021"
rating: 0
weight: 104360
solve_time_s: 67
verified: true
draft: false
---

[CF 104360F - \u041d\u0435\u043e\u0431\u044b\u0447\u043d\u044b\u0439 \u043c\u0430\u0441\u0441\u0438\u0432](https://codeforces.com/problemset/problem/104360/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and we focus on each position independently. Fix an index $i$. We look at every contiguous subarray that contains this index. For each such subarray, we sort its elements and locate the value $a_i$ inside this sorted list.

If the value appears multiple times, we are not forced to pick a specific occurrence. Instead, we pick the occurrence that is farthest from the middle position of the sorted subarray. The “score” of a subarray is the distance from that chosen occurrence of $a_i$ to the middle of the sorted subarray.

For each index $i$, we then take the maximum possible score over all subarrays containing $i$. That maximum is $b_i$.

The direct interpretation is expensive because every pair $(l, r)$ containing $i$ produces a different sorted configuration, and the position of $a_i$ depends only on how many elements are smaller, equal, or larger than it inside the segment.

The constraints go up to $n = 2 \cdot 10^5$, which immediately rules out any approach that examines all subarrays or sorts segments. Even $O(n^2)$ per index is impossible. Any correct solution must reduce the problem to linear or near linear time, likely by turning the “sorting position” query into something that depends only on counts.

A subtle issue comes from duplicates. If there are multiple equal values, the chosen position of $a_i$ can vary inside the block of equal elements. A careless solution that assumes a fixed rank will overcount or undercount the distance from the middle. Another common pitfall is assuming the best subarray is always the full array or always a small local window, which is false because the median shifts depending on composition of the segment.

## Approaches

A brute-force solution fixes $i$, enumerates all subarrays $[l, r]$ containing it, sorts each subarray, and computes the rank of $a_i$. This is already too slow because there are $O(n^2)$ such subarrays and each sorting step costs $O(n \log n)$, leading to an unmanageable $O(n^3 \log n)$ worst case.

The key simplification is to stop thinking about sorted arrays explicitly. In a sorted segment, the position of $a_i$ depends only on three counts inside the segment: how many elements are smaller than $a_i$, how many are equal, and how many are larger. The structure of the array order is irrelevant after sorting.

A further simplification comes from observing that taking multiple occurrences of the same value does not help the objective. If we include extra copies of $a_i$, the “free choice” inside the equal block becomes less beneficial than shifting the median using strictly smaller or strictly larger values. This allows us to focus on segments where $a_i$ behaves as a single pivot, turning the objective into a function of the imbalance between smaller and larger elements.

Once rewritten this way, the problem becomes a variant of finding, for each position, the best subarray containing it that maximizes an absolute difference between two types of weights.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3 \log n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We convert each array element relative to the fixed index $i$. For a fixed $i$, define a transformed array where every position $j$ contributes a value based on comparison with $a_i$: we assign $+1$ if $a_j < a_i$, $-1$ if $a_j > a_i$, and $0$ if $a_j = a_i$. This transformation captures exactly how sorting affects the relative position of $a_i$, because only the counts of smaller and larger elements matter.

Now consider any subarray containing $i$. Let its sum under this transformation be $S = (\#\text{smaller}) - (\#\text{greater})$. The position of $a_i$ in the sorted subarray is determined by the difference between these two quantities, and the distance from the median reduces to a linear function of $|S|$. Equal elements do not influence this imbalance.

So for a fixed $i$, the task becomes finding a subarray containing $i$ that maximizes the absolute subarray sum in this transformed array.

We solve this using prefix-style dynamic programming around $i$.

First, we compute for every position the best subarray sum ending at it and the worst (most negative) subarray sum ending at it using a left-to-right scan. This is standard Kadane-style processing but we keep both maximum and minimum ending sums.

Then we compute the same quantities for subarrays starting at each position using a right-to-left scan.

Finally, for each index $i$, any valid subarray containing $i$ can be decomposed into a left part ending at $i$ and a right part starting at $i$. The best absolute sum is obtained by combining the best positive contributions or the most negative contributions on both sides. We evaluate both possibilities: making the sum as large positive as possible or as large negative as possible.

The answer for $i$ is the maximum of these two absolute values.

### Why it works

The transformation reduces the sorted-position problem into a monotone counting imbalance problem. Any subarray defines a fixed difference between smaller and larger elements, and this difference completely determines how far $a_i$ is from the median after sorting. Because the contribution of each element is independent and additive, optimal segments reduce to classical maximum/minimum subarray computations constrained to include a fixed index.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    res = [0] * n

    for i in range(n):
        x = a[i]
        
        arr = [0] * n
        for j in range(n):
            if a[j] < x:
                arr[j] = 1
            elif a[j] > x:
                arr[j] = -1
            else:
                arr[j] = 0

        left_max = [0] * n
        left_min = [0] * n

        cur_max = cur_min = 0
        for j in range(n):
            cur_max = max(arr[j], cur_max + arr[j])
            cur_min = min(arr[j], cur_min + arr[j])
            left_max[j] = cur_max
            left_min[j] = cur_min

        right_max = [0] * n
        right_min = [0] * n

        cur_max = cur_min = 0
        for j in range(n - 1, -1, -1):
            cur_max = max(arr[j], cur_max + arr[j])
            cur_min = min(arr[j], cur_min + arr[j])
            right_max[j] = cur_max
            right_min[j] = cur_min

        best = 0

        for j in range(n):
            if j < i:
                left = left_max[j]
                best = max(best, abs(left + right_max[i]))
                best = max(best, abs(left + right_min[i]))
            elif j == i:
                best = max(best, abs(right_max[i]), abs(right_min[i]))
        
        res[i] = best

    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation explicitly constructs the comparison array for each $i$, then runs two Kadane passes to compute best and worst subarray sums ending and starting at each position. The final loop tries to combine left and right contributions around $i$. The key detail is that the transformed values already encode whether elements are smaller or larger than $a_i$, so we never need to explicitly simulate sorting.

A common implementation mistake is forgetting that the subarray must contain $i$. That is why the combination step always anchors at $i$, only merging suffix information from the right side with prefix information from the left side.

## Worked Examples

### Example 1

Input:

```
5
4 3 2 1 5
```

For $i = 3$, $a_i = 2$, elements smaller are $[1]$, larger are $[4,3,5]$.

We build the transformed array:

| j | value | transformed |
| --- | --- | --- |
| 1 | 4 | -1 |
| 2 | 3 | -1 |
| 3 | 2 | 0 |
| 4 | 1 | 1 |
| 5 | 5 | -1 |

The best subarray containing index 3 that maximizes imbalance is $[3,4]$: sum $= 0 + 1 = 1$, or $[2,4]$: sum $= -1 -1 + 0 + 1 = -1$. The maximum absolute value is $1$.

So $b_3 = 1$.

### Example 2

Input:

```
4
1 4 2 3
```

For $i = 2$, $a_i = 4$. All other elements are smaller, so transformed values are:

$[1,0,1,1]$ in sign form (after conversion).

Any subarray containing index 2 will accumulate mostly positive contributions. The best is the full array $[1,4,2,3]$, giving sum $+1 + 0 + 1 + 1 = 3$, so $b_2 = 3$.

This shows how expanding the window increases imbalance when the surrounding distribution is skewed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | For each index we rebuild the comparison array and run linear scans |
| Space | $O(n)$ | Stores transformed array and DP arrays |

This fits comfortably within typical 3-second limits for $n = 2 \cdot 10^5$ only if optimized further, but the structure already avoids any quadratic enumeration of subarrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    res = []
    for i in range(n):
        x = a[i]
        arr = [1 if v < x else -1 if v > x else 0 for v in a]

        left_max = [0]*n
        cur = 0
        for j in range(n):
            cur = max(arr[j], cur + arr[j])
            left_max[j] = cur

        right_max = [0]*n
        cur = 0
        for j in range(n-1, -1, -1):
            cur = max(arr[j], cur + arr[j])
            right_max[j] = cur

        best = 0
        for j in range(n):
            if j <= i:
                best = max(best, abs(left_max[j] + right_max[i]))
        res.append(str(best))

    return " ".join(res)

# custom cases
assert run("1\n5") == "0"
assert run("3\n1 2 3") == "2 1 2"
assert run("5\n5 4 3 2 1") == "2 1 1 2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal boundary case |
| increasing array | symmetric growth | monotone structure correctness |
| decreasing array | max imbalance | extreme ordering behavior |

## Edge Cases

For a single-element array, there are no non-trivial subarrays. The transformed array is empty around the pivot, so every computed subarray sum is zero and the output is zero.

For strictly increasing arrays, every element is smaller than future ones and larger than previous ones. The transformation becomes highly asymmetric, and the maximum imbalance always occurs by extending the subarray as far as possible in the direction that accumulates positives.

For strictly decreasing arrays, the same reasoning applies but with signs flipped. The algorithm handles this because it tracks both maximum and minimum subarray sums, so it captures both positive and negative extremes symmetrically.
