---
title: "CF 1041A - Heist"
description: "We are given a set of keyboard indices that survived a burglary. The key hidden structure is that before the theft, all keyboards formed one continuous block of integers, something like x, x+1, x+2, and so on up to some unknown length."
date: "2026-06-16T17:58:31+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1041
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 509 (Div. 2)"
rating: 800
weight: 1041
solve_time_s: 161
verified: true
draft: false
---

[CF 1041A - Heist](https://codeforces.com/problemset/problem/1041/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of keyboard indices that survived a burglary. The key hidden structure is that before the theft, all keyboards formed one continuous block of integers, something like x, x+1, x+2, and so on up to some unknown length. After the theft, some of those consecutive integers are missing, and we are left with an unordered subset of that original consecutive segment.

Our task is to determine the smallest possible number of keyboards that could have been stolen, assuming we are free to choose both the starting value x and the original length of the full consecutive segment.

What we are really doing is embedding the given numbers into a minimal-length integer interval of consecutive values. Once that interval is fixed, every integer inside it that is not in the given set must have been stolen. So minimizing stolen keyboards is equivalent to minimizing how many integers lie in the chosen interval but are absent from the input.

The constraint n ≤ 1000 means we can afford O(n^2) reasoning comfortably. Any solution that sorts and then inspects all gaps between elements is already well within limits. Anything cubic or worse is unnecessary.

A subtle edge case comes from the fact that the starting point x is not fixed. For example, if the smallest observed value is 8, the true sequence might have started at 1, 8, or even 10 depending on how we interpret missing values. A naive mistake is to assume the sequence must start at min(a), which ignores the possibility that the original consecutive block extended further left.

Another failure mode is ignoring internal gaps. For instance, if the remaining keyboards are 1, 10, 11, 12, it is not enough to look at extremes alone; the gap between 1 and 10 implies missing elements 2 through 9, which are part of the same original consecutive block in any consistent reconstruction.

## Approaches

The brute-force idea is to try every possible starting point x and every possible ending point y such that all given numbers lie in [x, y]. For each candidate interval, we check how many integers are missing from that interval. This is correct because it directly simulates the unknown original store configuration. However, the interval boundaries can range up to 10^9, and trying all possibilities would require iterating over an enormous range, making it infeasible.

The key observation is that the optimal interval must tightly wrap the existing numbers with no unnecessary slack at the ends. If we fix an order by sorting the remaining keyboards, then any valid original sequence must cover from the smallest observed value to the largest observed value, but it may also be optimal to extend the interval inward gaps only where needed to reduce inconsistencies. However, since extending the interval only increases the number of potential missing elements, the best strategy is to fix the interval as the minimal consecutive block containing all given values.

Within that interval, the number of missing keyboards is simply the difference between the length of the interval and the number of observed elements. The interval length is max(a) - min(a) + 1, and we subtract n.

So the problem reduces to sorting (or just scanning for min and max) and computing a simple arithmetic expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over intervals | O(range · n) or worse | O(1) | Too slow |
| Sort + compute span | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all remaining keyboard indices and store them in a list. These represent points inside an unknown consecutive interval.
2. Identify the smallest and largest values among them. These two values determine the minimal interval that can contain all remaining keyboards, since any valid original consecutive block must at least span from the minimum to the maximum observed index.
3. Compute the total number of integers in this interval using max_value - min_value + 1. This represents the full candidate original store inventory if no constraints from missing elements are considered.
4. Subtract the number of observed keyboards n from this interval length. What remains are the integers that must have existed in the original block but are not present in the final set, which corresponds exactly to stolen keyboards.

### Why it works

Any valid original configuration is a contiguous sequence of integers that must contain all observed values. Therefore, its endpoints must be at most min(a) and at least max(a), otherwise some observed value would lie outside the sequence. Expanding beyond these bounds only increases the number of implied missing elements without improving feasibility. Thus, the minimal possible original sequence is exactly the interval [min(a), max(a)], and every absent integer in that interval corresponds to a stolen keyboard.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    mn = min(a)
    mx = max(a)
    
    print((mx - mn + 1) - n)

if __name__ == "__main__":
    solve()
```

The solution reads the input in linear time and computes only two aggregate statistics: the minimum and maximum. The subtraction `(mx - mn + 1) - n` directly counts missing integers inside the smallest possible contiguous interval covering all remaining keyboards.

A common implementation mistake is sorting and then trying to count gaps individually, which is unnecessary here and increases risk of off-by-one errors. Another mistake is forgetting the `+1` when computing interval length, since both endpoints are inclusive.

## Worked Examples

### Example 1

Input:

```
4
10 13 12 8
```

Sorted array: [8, 10, 12, 13]

| Step | min | max | interval length | n | result |
| --- | --- | --- | --- | --- | --- |
| init | - | - | - | - | - |
| after scan | 8 | 13 | 6 | 4 | 2 |

The interval [8, 13] contains 6 integers. Since 4 are present, 2 are missing. This matches the intuition that 9 and 11 were stolen.

This trace confirms that only global bounds matter, not internal arrangement.

### Example 2

Input:

```
3
1 2 3
```

| Step | min | max | interval length | n | result |
| --- | --- | --- | --- | --- | --- |
| init | - | - | - | - | - |
| after scan | 1 | 3 | 3 | 3 | 0 |

The remaining keyboards already form a complete consecutive segment, so no missing elements exist. This demonstrates correctness when there are no gaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute min and max |
| Space | O(1) | Only a few variables are stored beyond input |

The constraints allow up to 1000 values, so a single linear scan is trivial in performance. Even a sorted O(n log n) approach would be safe, but unnecessary.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    return str(max(a) - min(a) + 1 - n)

# provided sample
assert run("4\n10 13 12 8\n") == "2"

# single element
assert run("1\n100\n") == "0"

# already consecutive
assert run("5\n1 2 3 4 5\n") == "0"

# large gap
assert run("3\n1 100 101\n") == "98"

# unordered input
assert run("4\n8 10 13 12\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | no theft when only one keyboard exists |
| consecutive block | 0 | handles perfect sequences |
| large gap | 98 | correctness over wide intervals |
| unordered input | 2 | order independence |

## Edge Cases

For a single keyboard, such as input `1 / 100`, the algorithm computes min = max = 100, interval length 1, result 0. This confirms that the model correctly handles degenerate intervals.

For a fully consecutive set like `1 2 3 4`, min is 1 and max is 4, giving interval length 4 and result 0. This ensures no false positives when there are no missing elements.

For large gaps like `1 100 101`, min = 1 and max = 101 gives interval length 101, and subtracting 3 yields 98 missing keyboards. This directly demonstrates how the method accounts for all unseen integers inside the bounding interval, regardless of distribution.
