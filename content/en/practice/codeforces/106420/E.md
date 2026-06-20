---
title: "CF 106420E - Strongest Attack First"
description: "We are given a sequence of enemy attack waves. Each wave has two parameters: a damage rate per second and a duration. If the player chooses a level ℓ, every wave is weakened by subtracting ℓ from its damage rate, but never below zero."
date: "2026-06-20T23:10:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106420
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 3-11-26 (Beginner)"
rating: 0
weight: 106420
solve_time_s: 38
verified: true
draft: false
---

[CF 106420E - Strongest Attack First](https://codeforces.com/problemset/problem/106420/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of enemy attack waves. Each wave has two parameters: a damage rate per second and a duration. If the player chooses a level ℓ, every wave is weakened by subtracting ℓ from its damage rate, but never below zero. So wave i contributes only max(0, dᵢ − ℓ) damage per second, sustained for tᵢ seconds.

The total damage taken over all waves is the sum of these contributions. The goal is to find the smallest level ℓ such that the total accumulated damage is strictly less than a given health threshold h, meaning the player survives.

The key computational object is the function D(ℓ) = Σ max(0, dᵢ − ℓ) · tᵢ. We are not choosing among independent decisions per wave, but a single global parameter ℓ that uniformly reduces all waves.

The input size allows up to large n and large values of dᵢ and tᵢ. Any solution that recomputes the full damage expression repeatedly in a naive way will need to process all waves per query. If we attempt a linear scan over possible ℓ values up to max(dᵢ), this becomes too large because dᵢ can be large, making an O(max(dᵢ) · n) approach infeasible.

The main structural observation is monotonicity: increasing ℓ can only reduce each term max(0, dᵢ − ℓ), so D(ℓ) never increases as ℓ grows. This implies a clean threshold behavior where once survival becomes possible at some ℓ, all larger ℓ also work.

A subtle edge case is when ℓ exceeds all dᵢ. In that case every term becomes zero, so D(ℓ) = 0 and survival is trivially guaranteed. This guarantees that the search space is bounded and the answer always exists.

Another corner case is when even ℓ = 0 already gives D(0) < h. Then the answer is 0, and binary search must correctly allow the lower bound to be valid without skipping it due to off-by-one mistakes.

## Approaches

The most direct idea is to try every possible level ℓ starting from zero and compute total damage for each choice. For a fixed ℓ, we scan all waves and compute max(0, dᵢ − ℓ) · tᵢ, summing into a total. This is correct because it directly follows the definition of damage. However, each evaluation is O(n), and if ℓ ranges up to max(dᵢ), the total cost becomes O(n · max(dᵢ)), which is far too large when dᵢ can be large.

The improvement comes from recognizing that we are not optimizing an arbitrary function but searching a monotone predicate. The condition “D(ℓ) < h” behaves consistently: if it holds for some ℓ, it holds for all larger ℓ. This converts the problem into finding a threshold point in a monotone decreasing function.

Once this structure is visible, binary search becomes the natural tool. We define a search range from 0 to max(dᵢ). The upper bound is sufficient because once ℓ reaches max(dᵢ), all terms vanish and damage is zero. Each check evaluates D(ℓ) in linear time, giving a total logarithmic number of evaluations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · max(dᵢ)) | O(1) | Too slow |
| Optimal (Binary Search) | O(n log max(dᵢ)) | O(1) | Accepted |

## Algorithm Walkthrough

We want to locate the smallest ℓ such that total damage drops below h.

1. Compute the maximum value among all dᵢ to define the upper bound of search space. This works because any ℓ beyond this point nullifies all damage contributions.
2. Set binary search boundaries with low = 0 and high = max(dᵢ). We are searching over a discrete monotone domain.
3. While low ≤ high, compute mid = (low + high) // 2. This represents a candidate level.
4. Evaluate total damage at level mid by iterating over all waves and summing max(0, dᵢ − mid) · tᵢ. This directly simulates the problem definition.
5. If the computed damage is at least h, then mid is insufficient, so we move low to mid + 1. This is because increasing ℓ is the only way to reduce damage.
6. Otherwise, mid is sufficient, so we store it as a candidate answer and move high to mid − 1 to try finding a smaller valid level.
7. After the loop ends, the stored candidate is the minimum valid ℓ.

Why it works

The function D(ℓ) is non-increasing in ℓ because each individual term max(0, dᵢ − ℓ) is non-increasing. This creates a contiguous region of invalid values followed by a contiguous region of valid values on the integer line. Binary search exploits this structure by repeatedly discarding half of the search space while preserving the boundary between invalid and valid regions. The algorithm maintains the invariant that all values below low are invalid and all values above high are valid, so the answer must remain inside the interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, h = map(int, input().split())
    d = []
    t = []
    mx = 0

    for _ in range(n):
        di, ti = map(int, input().split())
        d.append(di)
        t.append(ti)
        if di > mx:
            mx = di

    def damage(l):
        total = 0
        for i in range(n):
            if d[i] > l:
                total += (d[i] - l) * t[i]
                if total >= h:
                    return total
        return total

    low, high = 0, mx
    ans = mx

    while low <= high:
        mid = (low + high) // 2
        if damage(mid) >= h:
            low = mid + 1
        else:
            ans = mid
            high = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the binary search structure directly. The damage function includes an early exit once the accumulated sum reaches h, which prevents unnecessary computation in large cases. This does not affect correctness because we only need to distinguish whether D(ℓ) is at least h or not.

The binary search keeps track of the best valid answer in ans. When a mid value passes the condition, we still continue searching left to ensure minimality.

A common implementation pitfall is forgetting the early stopping condition or computing (dᵢ − ℓ) for all i even when dᵢ ≤ ℓ, which would add unnecessary operations and risk incorrect accumulation if negative values are included.

## Worked Examples

Consider a small instance with three waves:

n = 3, h = 10

waves: (d, t) = (5, 2), (8, 1), (3, 4)

We compute candidate ℓ values.

| ℓ | Wave 1 | Wave 2 | Wave 3 | Total D(ℓ) |
| --- | --- | --- | --- | --- |
| 0 | 10 | 8 | 12 | 30 |
| 2 | 6 | 6 | 4 | 16 |
| 4 | 2 | 4 | 0 | 6 |
| 5 | 0 | 3 | 0 | 3 |

For ℓ = 2, damage is still above 10, so it is invalid. For ℓ = 4, damage drops below 10, so it is valid. The minimum valid ℓ is 4.

This trace shows the monotone decrease of D(ℓ), which is exactly what binary search relies on.

Now consider a case where survival is already easy:

n = 2, h = 5

(2, 10), (1, 10)

| ℓ | Total D(ℓ) |
| --- | --- |
| 0 | 30 |
| 1 | 10 |
| 2 | 0 |

Here the answer is ℓ = 1. Binary search will correctly converge near the first level where damage falls below h.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log max(dᵢ)) | Each binary search step scans all waves, and the number of steps is logarithmic in the value range |
| Space | O(1) | Only stores arrays of input and a few variables |

The constraints are satisfied because even for n up to 2×10⁵ and max(dᵢ) up to large values, the logarithmic factor keeps total operations manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# Sample-style sanity check
assert run("3 10\n5 2\n8 1\n3 4\n") == "4"

# Already safe at level 0
assert run("2 100\n1 5\n2 3\n") == "0"

# Single dominant wave
assert run("1 5\n10 2\n") == "8"

# All damage zero after threshold
assert run("2 1\n5 1\n5 1\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed waves | 4 | standard monotone behavior |
| low h | 0 | answer can be zero |
| single wave | 8 | correctness on minimal n |
| equal dᵢ | 5 | boundary when all become zero |

## Edge Cases

One edge case occurs when ℓ = 0 already satisfies the condition. For example, if all waves are extremely weak or h is large:

n = 2, h = 100

(1, 1), (2, 1)

At ℓ = 0, total damage is 3, already below h. The binary search correctly identifies that mid values will always be valid, so high shrinks toward zero. The algorithm maintains ans = 0 as soon as a valid mid is found.

Another edge case is when the optimal ℓ equals max(dᵢ). For instance:

n = 2, h = 1

(3, 1), (3, 1)

At ℓ = 2, damage is still positive; at ℓ = 3, all contributions vanish. The binary search must include high = max(dᵢ), otherwise the correct boundary point would be excluded.
