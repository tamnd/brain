---
title: "CF 276A - Lunch Rush"
description: "The problem describes a lunch scenario where three Rabbits have a fixed break of k time units and a list of n restaurants. Each restaurant is defined by two numbers: the joy fᵢ the Rabbits gain if they finish on time, and the time tᵢ it takes to eat there."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 276
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 169 (Div. 2)"
rating: 900
weight: 276
solve_time_s: 90
verified: false
draft: false
---

[CF 276A - Lunch Rush](https://codeforces.com/problemset/problem/276/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

The problem describes a lunch scenario where three Rabbits have a fixed break of _k_ time units and a list of _n_ restaurants. Each restaurant is defined by two numbers: the joy _fᵢ_ the Rabbits gain if they finish on time, and the time _tᵢ_ it takes to eat there. If _tᵢ_ exceeds the available time _k_, the joy is penalized by the overage: the Rabbits lose one unit of joy for each unit of extra time, resulting in joy equal to _fᵢ - (tᵢ - k)_. If _tᵢ ≤ k_, they enjoy the full joy _fᵢ_. The task is to determine the maximum possible joy across all restaurants.

Constraints indicate that _n_ can be up to 10,000 and _fᵢ_, _tᵢ_, _k_ can be as large as 10⁹. This excludes any solution that would rely on quadratic operations, but since each restaurant is considered independently, a linear scan suffices. A non-obvious edge case occurs when _tᵢ_ is exactly equal to _k_, in which case no penalty is applied. Another subtle scenario is when all _tᵢ_ exceed _k_, potentially resulting in negative joy values; the solution must still correctly identify the maximum among possibly negative results.

## Approaches

The naive approach is to consider each restaurant in turn, compute the effective joy, and track the maximum. This approach works correctly because each restaurant is independent: choosing one restaurant does not affect the others. The operation count is proportional to _n_, which is acceptable given the constraints.

The key insight is that the adjustment to joy, _fᵢ - max(tᵢ - k, 0)_, can be computed in a single conditional expression for each restaurant. There is no need for sorting or additional data structures since the maximum can be maintained on-the-fly. This transforms the problem into a simple linear scan, guaranteeing O(n) time and O(1) extra space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (linear scan) | O(n) | O(1) | Accepted |
| Sorting or advanced data structure | O(n log n) | O(n) | Unnecessary / slower |

## Algorithm Walkthrough

1. Initialize a variable `max_joy` to a very small value, such as negative infinity, to handle negative joy cases correctly.
2. Iterate over each restaurant _i_ from 1 to _n_. For each restaurant, read its joy value _fᵢ_ and time requirement _tᵢ_.
3. Compute the effective joy `current_joy`. If _tᵢ > k_, subtract the penalty _(tᵢ - k)_ from _fᵢ_. Otherwise, `current_joy = fᵢ`.
4. Update `max_joy` if `current_joy` exceeds the current `max_joy`.
5. After processing all restaurants, output `max_joy`.

Why it works: The algorithm maintains the invariant that `max_joy` is always equal to the maximum effective joy of all restaurants examined so far. Each restaurant is processed independently, and the maximum is correctly updated, so after the loop, `max_joy` contains the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
max_joy = -10**18  # sufficiently small initial value to handle negative joys

for _ in range(n):
    f, t = map(int, input().split())
    if t > k:
        current_joy = f - (t - k)
    else:
        current_joy = f
    if current_joy > max_joy:
        max_joy = current_joy

print(max_joy)
```

The solution reads input efficiently using `sys.stdin.readline`. Each restaurant's joy is computed with a conditional to handle the penalty, ensuring correctness for all edge cases, including when _tᵢ = k_ or all joys are negative. Using `-10**18` for `max_joy` avoids errors when all values are negative.

## Worked Examples

**Sample Input 1**

```
2 5
3 3
4 5
```

| Step | f | t | current_joy | max_joy |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 3 | 3 |
| 2 | 4 | 5 | 4 | 4 |

Output: `4`

This trace confirms the algorithm correctly applies no penalty when _t ≤ k_ and tracks the maximum.

**Sample Input 2**

```
3 4
5 6
7 4
6 5
```

| Step | f | t | current_joy | max_joy |
| --- | --- | --- | --- | --- |
| 1 | 5 | 6 | 3 | 3 |
| 2 | 7 | 4 | 7 | 7 |
| 3 | 6 | 5 | 5 | 7 |

Output: `7`

This demonstrates correct penalty computation when _t > k_ and proper maximum tracking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over all restaurants, performing constant work per restaurant |
| Space | O(1) | Only a few integer variables are maintained, independent of n |

The linear time complexity ensures that even for the maximum _n = 10^4_, the solution completes well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    max_joy = -10**18
    for _ in range(n):
        f, t = map(int, input().split())
        current_joy = f if t <= k else f - (t - k)
        if current_joy > max_joy:
            max_joy = current_joy
    return str(max_joy)

# Provided sample
assert run("2 5\n3 3\n4 5\n") == "4", "sample 1"

# Custom tests
assert run("3 4\n5 6\n7 4\n6 5\n") == "7", "penalty and on-time mix"
assert run("1 10\n10 15\n") == "5", "single restaurant, penalty applied"
assert run("2 3\n1 5\n2 6\n") == "0", "all negative or zero joy after penalty"
assert run("3 5\n6 5\n7 5\n8 5\n") == "8", "all on-time, maximum selection"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 4\n5 6\n7 4\n6 5 | 7 | correct penalty and maximum selection |
| 1 10\n10 15 | 5 | single restaurant with penalty |
| 2 3\n1 5\n2 6 | 0 | negative/zero joys correctly handled |
| 3 5\n6 5\n7 5\n8 5 | 8 | all on-time restaurants, selects maximum |

## Edge Cases

If a restaurant's time equals _k_, no penalty is applied. For example, input:

```
2 5
4 5
3 6
```

Processing:

| Step | f | t | current_joy | max_joy |
| --- | --- | --- | --- | --- |
| 1 | 4 | 5 | 4 | 4 |
| 2 | 3 | 6 | 2 | 4 |

Output: `4`

This confirms the algorithm handles the boundary case _t = k_ correctly. Negative or zero joys are also correctly compared because `max_joy` is initialized to a sufficiently small number.
