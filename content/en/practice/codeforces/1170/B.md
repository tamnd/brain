---
title: "CF 1170B - Bad Days"
description: "We are given a sequence of daily website visit counts. Each position represents one day, and the value at that position represents how many visits occurred on that day. We need to examine every day and decide whether it is “bad”."
date: "2026-06-12T02:01:58+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1170
codeforces_index: "B"
codeforces_contest_name: "Kotlin Heroes: Episode 1"
rating: 0
weight: 1170
solve_time_s: 192
verified: true
draft: false
---

[CF 1170B - Bad Days](https://codeforces.com/problemset/problem/1170/B)

**Rating:** -  
**Tags:** *special, implementation  
**Solve time:** 3m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of daily website visit counts. Each position represents one day, and the value at that position represents how many visits occurred on that day. We need to examine every day and decide whether it is “bad”.

A day becomes bad if, when looking only at the days before it, there are at least two earlier days whose visit counts are strictly larger than the value on that day. The earlier days do not need to be adjacent, only their values matter.

The task is to count how many indices satisfy this condition.

The constraint on the number of days is up to 200,000. That immediately rules out any solution that compares each day against all previous days in a nested loop, since that would require on the order of n² comparisons, which is far too large for a 3-second limit. A linear or near-linear scan is necessary, possibly with a small fixed amount of extra work per element.

A subtle failure case for naive reasoning comes from forgetting that we only care about how many previous values are larger, not their positions. For example, in a sequence like [10, 1, 9, 8], the second element sees two larger values before it, while later elements may have fewer even though the array is not monotone. Another edge case is repeated values. Since the condition is strictly greater, equal values must not be counted.

## Approaches

A direct approach checks each day independently. For a fixed index i, we scan all j < i and count how many a[j] > a[i]. If this count is at least two, we mark the day as bad. This is correct because it exactly follows the definition. However, each position may require scanning up to i-1 elements, and across all i this becomes about n(n-1)/2 comparisons. With n = 200,000, this is infeasible.

The key observation is that for each day we only care about whether it has at least two larger values before it. This is a threshold condition, not an exact count beyond two. That means we do not need full information about all previous elements, only whether we can identify the two largest values seen so far among previous days.

Once we realize this, the structure becomes simple. As we iterate from left to right, we maintain the largest and second largest values encountered so far. For each new day, we compare its value to these two tracked maxima. If both stored maxima are strictly greater than the current value, then there must be at least two earlier days exceeding it, so it is bad.

This works because any element larger than the current value must be among the global top values seen so far. If there are at least two such elements, they will necessarily occupy the first and second maximum positions in the prefix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Maintain two maxima | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two variables, `first` and `second`, to track the largest and second largest values seen so far. We set them to negative infinity so that any input value replaces them correctly.
2. Initialize a counter `bad = 0` to accumulate the number of bad days.
3. Iterate through the array from left to right.
4. For the current value `x`, check whether both `first > x` and `second > x` hold. If they do, then at least two previous days have strictly greater values, so we increment `bad`.
5. After processing the condition, update the tracked maxima with `x`. If `x >= first`, shift `first` into `second` and assign `first = x`. Otherwise, if `x >= second`, update `second = x`.

The ordering of the update matters because we must evaluate the condition using only previous elements. Updating after checking ensures the current day is not counted among its own history.

### Why it works

At every position, `first` and `second` store the largest and second largest values from all previous indices. Therefore, the condition `first > x and second > x` is equivalent to saying that at least two earlier elements exceed `x`. No other values can violate this equivalence because any value greater than `x` must be among the prefix maxima, and if there are at least two such values, they must occupy these two tracked slots.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    first = float("-inf")
    second = float("-inf")
    
    bad = 0
    
    for x in a:
        if first > x and second > x:
            bad += 1
        
        if x >= first:
            second = first
            first = x
        elif x >= second:
            second = x
    
    print(bad)

if __name__ == "__main__":
    solve()
```

The solution processes the array in a single pass. The condition check uses only the prefix information stored in `first` and `second`, ensuring correctness. The update step carefully maintains ordering so that ties are handled correctly: using `>=` ensures duplicates are tracked in a way that preserves the ability to count strictly greater comparisons correctly in later steps.

## Worked Examples

Consider the sample array [3, 1, 4, 1, 5, 9, 2, 6].

We track `first`, `second`, and whether the current day is bad.

| i | x | first | second | bad? |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | -inf | no |
| 2 | 1 | 3 | 1 | no |
| 3 | 4 | 4 | 3 | no |
| 4 | 1 | 4 | 3 | yes |
| 5 | 5 | 5 | 4 | no |
| 6 | 9 | 9 | 5 | no |
| 7 | 2 | 9 | 5 | yes |
| 8 | 6 | 9 | 6 | no |

The table shows that days 4 and 7 are counted as bad, matching the requirement that each has at least two earlier larger values.

Now consider a small edge example [10, 8, 7, 9, 6].

| i | x | first | second | bad? |
| --- | --- | --- | --- | --- |
| 1 | 10 | 10 | -inf | no |
| 2 | 8 | 10 | 8 | no |
| 3 | 7 | 10 | 8 | yes |
| 4 | 9 | 10 | 9 | yes |
| 5 | 6 | 10 | 9 | yes |

This demonstrates that once two large values exist in the prefix, many later small values can become bad, and the algorithm consistently detects that without scanning history.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time updates and checks |
| Space | O(1) | Only two variables and a counter are maintained |

The linear scan comfortably handles n up to 200,000 within time limits since each iteration performs only a few comparisons and assignments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import inf
    
    data = inp.strip().split()
    n = int(data[0])
    a = list(map(int, data[1:]))

    first = float("-inf")
    second = float("-inf")
    bad = 0

    for x in a:
        if first > x and second > x:
            bad += 1
        
        if x >= first:
            second = first
            first = x
        elif x >= second:
            second = x

    return str(bad)

# provided sample
assert run("8\n3 1 4 1 5 9 2 6") == "2"

# minimum size
assert run("1\n5") == "0"

# all equal
assert run("5\n7 7 7 7 7") == "0"

# strictly decreasing
assert run("5\n9 8 7 6 5") == "3"

# increasing sequence
assert run("5\n1 2 3 4 5") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | minimal boundary |
| all equal | 0 | strict greater condition |
| decreasing | 3 | many early large values accumulate |
| increasing | 0 | no element has two greater predecessors |

## Edge Cases

One edge case is when the array is strictly decreasing, for example [9, 7, 5, 3, 1]. The algorithm updates `first` and `second` so that after the first two elements, both are large. Starting from the third element, every new value is smaller than both stored maxima, so every subsequent position is counted as bad. This matches the definition since every such element has at least two earlier greater values.

Another edge case is repeated values such as [5, 5, 5, 5]. Here, although there are many earlier elements, none are strictly greater than any given element. The condition `first > x and second > x` never becomes true because `first` and `second` are never strictly greater than the current value once equality dominates. This correctly yields zero bad days.
