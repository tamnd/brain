---
title: "CF 327A - Flipping Game"
description: "We are given a short binary array, where each position is either 0 or 1. We are allowed to choose exactly one contiguous segment and invert every value inside it, turning 0 into 1 and 1 into 0."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 327
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 191 (Div. 2)"
rating: 1200
weight: 327
solve_time_s: 243
verified: true
draft: false
---

[CF 327A - Flipping Game](https://codeforces.com/problemset/problem/327/A)

**Rating:** 1200  
**Tags:** brute force, dp, implementation  
**Solve time:** 4m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short binary array, where each position is either 0 or 1. We are allowed to choose exactly one contiguous segment and invert every value inside it, turning 0 into 1 and 1 into 0. After performing this single operation, we want the resulting array to contain as many 1s as possible.

The key difficulty is that flipping a segment has two effects at the same time. Every 0 inside the chosen segment becomes beneficial because it turns into a 1, while every 1 inside the segment becomes a loss because it turns into 0. So the quality of a segment is determined not by its raw content, but by how many more zeros than ones it contains.

The input size is very small, with at most 100 elements. This immediately allows quadratic enumeration strategies, but also leaves room for a clean reduction to a classical optimization problem.

A subtle edge case appears when the array is all ones. Any flip will necessarily destroy some ones, so the best possible answer is not “no change”, but the result of flipping a segment that minimizes damage. For example, if the array is `[1, 1, 1]`, flipping a single element produces `[1, 0, 1]`, giving two ones, which is the maximum possible under the constraint that we must flip exactly one segment.

Another important case is when zeros are scattered. For example, `[0, 1, 0]`. A naive strategy that flips all zeros independently is impossible because we must choose a single contiguous segment, so we must reason about grouping.

## Approaches

A brute-force approach is straightforward: try every possible pair of indices `(i, j)` and simulate flipping that segment. For each choice, we compute the resulting number of ones by scanning the entire array again. There are O(n²) possible segments, and each simulation costs O(n), which leads to O(n³) total work. With n up to 100, this is borderline but still acceptable, though it is unnecessary.

The key observation is that we do not actually need to simulate the final array. We only care about how the number of ones changes. Suppose the original number of ones is fixed. When we flip a segment, every 0 contributes +1 to the score, and every 1 contributes −1. This transforms the problem into finding a subarray with maximum sum, where we map 0 → +1 and 1 → −1.

So instead of brute-forcing segments, we reduce the task to finding the maximum subarray sum, which can be solved in linear time using Kadane’s algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Accepted but unnecessary |
| Kadane Transformation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the array into gains. Each element becomes +1 if it is 0, and −1 if it is 1.

1. Compute the initial number of ones in the array. This is the baseline result before any flip.
2. Convert the array into a gain array where flipping a segment corresponds to summing those gains.
3. Run a maximum subarray sum computation over this gain array.
4. The best gain represents the best improvement we can achieve by choosing an optimal segment.
5. Add this gain to the initial number of ones to obtain the final answer.

During the maximum subarray computation, we maintain a running best ending at the current position. If extending the previous segment decreases the sum below starting fresh, we reset. This ensures we always track the most beneficial contiguous segment.

### Why it works

Each flip affects the total number of ones in an additive way. A 0 flipped inside the segment increases the count by 1, while a 1 decreases it by 1. This makes the contribution of each index independent and additive over a segment. Any valid segment corresponds exactly to a subarray sum in this transformed representation, and maximizing ones is equivalent to maximizing that sum. Since every possible segment is representable, and every representation corresponds to a valid segment, the optimal subarray directly gives the optimal flip.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

base = sum(a)

# transform: 0 -> +1, 1 -> -1
best = float('-inf')
cur = 0

for x in a:
    val = 1 if x == 0 else -1
    cur = max(val, cur + val)
    best = max(best, cur)

print(base + best)
```

The solution first computes how many ones already exist, since that forms the baseline. It then converts each element into its contribution to improvement if included in the flipped segment. The Kadane update step either extends the current segment or restarts it at the current position, depending on which yields a better sum.

The final answer is the baseline plus the best achievable improvement.

A common mistake is forgetting that we must perform exactly one flip. This is why we do not allow skipping the operation; even in the all-ones case, the best subarray will be negative, correctly reflecting that any flip reduces the number of ones.

## Worked Examples

### Example 1

Input:

```
5
1 0 0 1 0
```

We compute:

Base ones = 2

Gain array = [-1, +1, +1, -1, +1]

| i | a[i] | gain | cur | best |
| --- | --- | --- | --- | --- |
| 1 | 1 | -1 | -1 | -1 |
| 2 | 0 | +1 | 1 | 1 |
| 3 | 0 | +1 | 2 | 2 |
| 4 | 1 | -1 | 1 | 2 |
| 5 | 0 | +1 | 2 | 2 |

Best gain = 2

Final answer = 2 + 2 = 4

This confirms that the optimal segment is `[2,5]`, producing a strong cluster of flipped zeros outweighing the loss from ones inside the interval.

### Example 2

Input:

```
3
1 1 1
```

Base ones = 3

Gain array = [-1, -1, -1]

| i | gain | cur | best |
| --- | --- | --- | --- |
| 1 | -1 | -1 | -1 |
| 2 | -1 | -1 | -1 |
| 3 | -1 | -1 | -1 |

Best gain = -1

Final answer = 3 + (-1) = 2

This shows why forcing a flip matters. Even though all elements are already optimal, we must still choose a segment, and the least damaging segment is a single element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass Kadane computation |
| Space | O(1) | only a few variables are maintained |

The linear scan fits easily within the constraints, and the memory usage is constant, making it optimal for n up to 100.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    base = sum(a)
    best = float('-inf')
    cur = 0

    for x in a:
        val = 1 if x == 0 else -1
        cur = max(val, cur + val)
        best = max(best, cur)

    return str(base + best)

# provided sample
assert run("5\n1 0 0 1 0\n") == "4"

# all ones
assert run("3\n1 1 1\n") == "2"

# all zeros
assert run("4\n0 0 0 0\n") == "4"

# single element 1
assert run("1\n1\n") == "0"

# single element 0
assert run("1\n0\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | 2 | mandatory flip reduces optimal segment choice |
| all zeros | 4 | best flip is whole array |
| single 1 | 0 | edge case minimal size |
| single 0 | 1 | best possible gain |

## Edge Cases

For an array like `[1, 1, 1]`, the gain array becomes `[-1, -1, -1]`. Kadane never allows an empty segment, so it selects the least negative single element, producing a best gain of −1. Adding this to the baseline correctly yields 2.

For `[0]`, the gain is `[+1]`, and Kadane picks it directly, giving a gain of +1 and final answer 1, which matches flipping the only element.

For `[1, 0]`, gains are `[-1, +1]`. Kadane resets at index 2, selecting only the +1 segment, giving correct improvement and showing why starting fresh is essential when a negative prefix dominates.
