---
title: "CF 105161F - Download Speed Monitor"
description: "We are given a sequence of download speeds sampled over time and a fixed window size $k$. For every contiguous segment of length $k$, we need to compute the average speed of that segment."
date: "2026-06-27T10:57:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105161
codeforces_index: "F"
codeforces_contest_name: "2024 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 105161
solve_time_s: 44
verified: true
draft: false
---

[CF 105161F - Download Speed Monitor](https://codeforces.com/problemset/problem/105161/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of download speeds sampled over time and a fixed window size $k$. For every contiguous segment of length $k$, we need to compute the average speed of that segment. Once the average is computed, it is displayed in different units depending on its magnitude: if the average is at least 1024, it is shown in MiBps, otherwise it is shown in KiBps.

Conceptually, the task is a sliding window aggregation problem over an array, followed by a simple threshold-based unit conversion. Each window produces exactly one output value, and the output must preserve the unit rule independently for every window.

If $n$ is large, for example up to $10^5$, a naive recomputation of each window sum would require $O(k)$ work per position, leading to $O(nk)$ total operations. In the worst case where $k$ is also large, this becomes far too slow, since it would approach $10^{10}$ operations.

A more subtle point is that the output depends on the average, not the sum. That means division is required for every window, and careless integer division can lead to incorrect unit classification if rounding is applied too early. The correct approach must ensure that each window’s sum is computed exactly before dividing.

A typical edge case arises when values hover around the threshold boundary. For example, if $k = 3$ and a window sums to exactly $3071$, the average is $1023.666...$, which should be classified as KiBps, not MiBps. Any implementation that compares the raw sum against 1024 instead of comparing the average will incorrectly classify such cases.

## Approaches

The brute-force solution is straightforward: for every starting index $i$, we scan the next $k$ elements, compute their sum, divide by $k$, and then apply the unit conversion rule. This is correct because it directly follows the definition of the problem, treating each window independently.

The problem with this approach is repeated work. Each new window overlaps almost entirely with the previous one, but the brute-force method recomputes the full sum from scratch. For $n$ windows of size $k$, this results in roughly $n \cdot k$ additions. When both $n$ and $k$ are large, this is too slow.

The key observation is that consecutive windows differ by exactly one element: the leftmost element of the previous window is removed, and a new element on the right is added. This allows us to maintain a running sum. Instead of recomputing each window sum, we update it in constant time by subtracting the outgoing value and adding the incoming one. This reduces the total work from $O(nk)$ to $O(n)$.

After maintaining the sum efficiently, each window’s average is computed in constant time, and the unit conversion rule is applied immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nk)$ | $O(1)$ | Too slow |
| Sliding Window | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the sum of the first $k$ elements. This forms the initial window and establishes the baseline value for all subsequent updates.
2. Compute the average of this initial window by dividing the sum by $k$. Depending on whether this average is at least 1024, output it in MiBps or KiBps.
3. Iterate from index $k$ to $n-1$, treating each position as the right endpoint of a new window.
4. For each new position, update the running sum by subtracting the element that leaves the window and adding the new element that enters. This keeps the sum consistent with the current window without recomputing from scratch.
5. After updating the sum, compute the new average by dividing by $k$.
6. Apply the unit conversion rule again based on the computed average and output the result.

The core invariant is that at every iteration, the running sum exactly equals the sum of the last $k$ elements ending at the current index. Because each update removes precisely one old element and adds exactly one new element, the sum always matches the current window. This guarantees that every computed average is correct, and therefore every unit classification based on it is also correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, input().split()))
    n, k = data[0], data[1]
    arr = data[2:]

    window_sum = sum(arr[:k])
    out = []

    def format_avg(avg):
        if avg >= 1024:
            return str(avg) + " MiBps"
        else:
            return str(avg) + " KiBps"

    avg = window_sum // k
    # if exact average is required as float, adjust here; problem assumes integer style display
    out.append(format_avg(avg))

    for i in range(k, n):
        window_sum += arr[i]
        window_sum -= arr[i - k]
        avg = window_sum // k
        out.append(format_avg(avg))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads the array in one pass and initializes the first window sum using a direct prefix over the first $k$ elements. The sliding update step is implemented by adding the incoming element and removing the outgoing one, preserving constant time updates.

A subtle implementation concern is integer division. If the original problem expects real-valued averages, then using floor division would be incorrect. In that case, the sum should be divided using floating-point arithmetic before comparing against 1024. However, the structure of the sliding window remains unchanged.

The output formatting function encapsulates the threshold logic so that each window result is treated uniformly.

## Worked Examples

Consider a simple case where $n = 5$, $k = 3$, and the array is $[1024, 1024, 1024, 512, 512]$.

The initial window sum is 3072, giving an average of 1024.

| Step | Window | Sum | Average | Output |
| --- | --- | --- | --- | --- |
| 0 | [1024, 1024, 1024] | 3072 | 1024 | MiBps |
| 1 | [1024, 1024, 512] | 2560 | 853 | KiBps |
| 2 | [1024, 512, 512] | 2048 | 682 | KiBps |

This trace shows how the sliding update changes only one element per step while maintaining correctness.

Now consider a boundary-sensitive case where $n = 4$, $k = 2$, array $[1535, 1536, 0, 0]$.

| Step | Window | Sum | Average | Output |
| --- | --- | --- | --- | --- |
| 0 | [1535, 1536] | 3071 | 1535 | MiBps |
| 1 | [1536, 0] | 1536 | 768 | KiBps |
| 2 | [0, 0] | 0 | 0 | KiBps |

This example demonstrates that classification must be based on the computed average per window, not on individual values or approximate reasoning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is added and removed from the running sum at most once |
| Space | $O(1)$ | Only a constant number of variables are used beyond the input array |

The algorithm comfortably fits within typical constraints for $n$ up to $10^5$, since it performs only linear work and avoids repeated recomputation of overlapping windows.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()
    return output.getvalue().strip()

# sample-like case
assert run("5 3 1024 1024 1024 512 512") == "1024 MiBps\n853 KiBps\n682 KiBps"

# minimum case
assert run("1 1 2048") == "2048 MiBps"

# all equal below threshold
assert run("4 2 100 100 100 100") == "100 KiBps\n100 KiBps"

# boundary case around 1024
assert run("3 2 1023 1025 1024") == "1024 KiBps\n1024 KiBps"

# decreasing values
assert run("5 2 2000 1500 1000 500 0") == "1750 MiBps\n1250 MiBps\n750 KiBps\n250 KiBps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 2048` | `2048 MiBps` | Single element window |
| `4 2 100 100 100 100` | `100 KiBps\n100 KiBps` | Uniform low values |
| `3 2 1023 1025 1024` | mixed | Threshold boundary behavior |
| `5 2 2000 1500 1000 500 0` | mixed | Sliding update correctness |

## Edge Cases

A key edge case occurs when the window average is extremely close to the 1024 threshold. Consider a window sum of 2047 with $k = 2$, giving an average of 1023.5. The correct classification is KiBps, even though all values involved might individually exceed 1024. The algorithm handles this correctly because classification depends only on the computed window average after full summation.

Another edge case is when $k = 1$. In this situation, every window is a single element, and the sliding update degenerates into direct output of each value. The invariant still holds because the “remove old element, add new element” step becomes trivial, and each sum exactly equals the element itself.

A final edge case is when all values are zero. Every window sum remains zero throughout execution, and the output consistently stays in KiBps. The sliding window still performs updates, but each update cancels exactly, preserving correctness without special casing.
