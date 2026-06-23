---
title: "CF 105272E - Excavating Mercury"
description: "The horizon of Mercury is described as a line of mountains, each position having a given height. We are allowed to perform only one type of operation: reduce the height of any mountain by removing material."
date: "2026-06-23T14:02:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105272
codeforces_index: "E"
codeforces_contest_name: "IX MaratonUSP Freshman Contest"
rating: 0
weight: 105272
solve_time_s: 45
verified: true
draft: false
---

[CF 105272E - Excavating Mercury](https://codeforces.com/problemset/problem/105272/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The horizon of Mercury is described as a line of mountains, each position having a given height. We are allowed to perform only one type of operation: reduce the height of any mountain by removing material. Increasing any height or transferring material between mountains is forbidden.

The goal is to modify the landscape so that all mountains end up with exactly the same height, while minimizing the total amount of material removed.

In more concrete terms, we start with an array of heights. We want to choose a final uniform height and reduce every element that is above this level down to it. Any element below that level would need to be increased, which is impossible, so such a choice of target height is invalid.

The constraint n ≤ 100000 with heights up to 10000 immediately suggests that an O(n) or O(n log n) solution is sufficient. Anything involving checking all possible target heights naively in a nested way would still be fine if done carefully because the value range is small, but it turns out unnecessary.

A subtle edge case appears when the array is not constant. For example, if all values are equal, no removal is needed and the answer is zero. If there is a single very small value, that value restricts everything else.

Input like:

```
5
10 10 10 10 10
```

should return 0.

Input like:

```
3
5 1 5
```

forces the final height to be 1, since we cannot raise the 1, and thus everything else must be reduced.

A naive misunderstanding would be to pick an average or median height, which might minimize distance in other problems, but here any target above the minimum is invalid.

## Approaches

A direct brute-force approach tries every possible target height H from 1 to max(ai). For each candidate H, we check feasibility: every element must be at least H, otherwise we discard it. If feasible, we compute the cost as the sum of reductions ai − H over all i. We take the minimum.

This works because the condition is simple, but its inefficiency comes from recomputing the cost for every possible H. With max(ai) up to 10000 and n up to 100000, this becomes about 10^9 operations in the worst case, which is unnecessary overhead.

The key observation is that feasibility forces H to be at most the minimum element of the array. Any higher choice immediately makes the solution impossible because at least one element would need to be increased.

Once we restrict H to valid choices, there is only one candidate that maximizes H: the minimum value in the array. Since the cost decreases as H increases, we want the largest possible valid H, which is exactly the minimum element.

This reduces the problem to computing the sum of all elements and subtracting n times the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over H | O(n * maxA) | O(1) | Too slow |
| Optimal (min + sum) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We want to express the final uniform height as a single value H, then compute how much needs to be removed.

1. Scan the array once to compute both the total sum of all heights and the minimum height. The sum captures total available material, and the minimum determines the highest feasible uniform level.
2. Set the target height H to the minimum value in the array. This is the largest possible height that does not require increasing any element.
3. Compute the total removed material as sum of all elements minus n multiplied by H. This represents reducing every element down to H.
4. Output this value.

### Why it works

Any valid final configuration must choose a height H that is no greater than every ai, otherwise some mountain would require an increase. This forces H ≤ min(ai). For any such H, the cost is sum(ai − H), which simplifies to a linear expression in H. Since the sum is fixed, maximizing H minimizes the removal cost. The maximum feasible H is exactly the minimum array element, so no other candidate can do better.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    mn = min(a)
    
    print(total - n * mn)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the derived formula. The only care needed is using a single pass aggregation of sum and minimum. There is no risk of overflow in Python, but in other languages one must ensure 64-bit integers because the sum can reach 10^9.

## Worked Examples

### Example 1

Input:

```
3
5 1 5
```

We track sum and minimum:

| Step | Array | Sum | Min | H | Cost |
| --- | --- | --- | --- | --- | --- |
| After scan | 5 1 5 | 11 | 1 | 1 | 11 - 3 = 8 |

The final height is 1. Each 5 becomes 1, contributing 4 units of removal each, totaling 8.

This confirms that any attempt to choose H = 2 or more is invalid since the middle element would need to increase.

### Example 2

Input:

```
4
10 10 10 10
```

| Step | Array | Sum | Min | H | Cost |
| --- | --- | --- | --- | --- | --- |
| After scan | 10 10 10 10 | 40 | 10 | 10 | 40 - 40 = 0 |

All elements already match the optimal height. No removal is needed.

This shows the algorithm correctly handles uniform arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute sum and minimum |
| Space | O(1) | Only a few accumulator variables are used |

The solution comfortably fits within limits since n is up to 100000 and only linear work is performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    n = int(input())
    a = list(map(int, input().split()))
    return str(sum(a) - n * min(a))

# provided samples
assert run("3\n5 1 5\n") == "8"
assert run("4\n10 10 10 10\n") == "0"

# minimum size
assert run("1\n7\n") == "0"

# already uniform large
assert run("5\n3 3 3 3 3\n") == "0"

# mixed values
assert run("6\n1 2 3 4 5 6\n") == str(21 - 6*1)

# single minimum in middle
assert run("5\n10 3 10 10 10\n") == str(43 - 5*3)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | single mountain needs no change |
| all equal | 0 | no removals required |
| increasing sequence | computed | correct identification of min constraint |
| scattered minimum | computed | min drives solution |

## Edge Cases

The most important edge case is when the minimum value appears multiple times or only once. The algorithm does not depend on frequency, only on the smallest element. For input:

```
5
10 3 10 10 10
```

The scan produces sum = 43 and min = 3. The computed result is 43 − 5 × 3 = 28. Every element above 3 is reduced, while the element equal to 3 remains unchanged, confirming correctness.

Another case is when the minimum is at the boundary:

```
3
1 100 100
```

Here H must be 1. The algorithm reduces both 100s down to 1, producing cost 198. Any higher H would force increasing the 1, which is illegal, so the constraint is enforced implicitly by choosing the minimum.
