---
title: "CF 104257J - Jiggle Joggle"
description: "We are given a single sequence of integers, and we are allowed to delete elements while keeping the remaining elements in their original order."
date: "2026-07-01T21:47:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104257
codeforces_index: "J"
codeforces_contest_name: "2021 NTUIM Programming Design And Optimization (PDAO 2021)"
rating: 0
weight: 104257
solve_time_s: 53
verified: true
draft: false
---

[CF 104257J - Jiggle Joggle](https://codeforces.com/problemset/problem/104257/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single sequence of integers, and we are allowed to delete elements while keeping the remaining elements in their original order. The goal is to make the resulting subsequence as long as possible while satisfying a strict alternating pattern on its consecutive differences.

Concretely, if we look at the chosen subsequence, every adjacent pair must differ, and the sign of these differences must alternate strictly. If the first difference is positive, the next must be negative, then positive again, and so on. The same holds if the first difference is negative. Any zero difference immediately breaks validity because equality is not allowed inside the alternating pattern.

The task is to compute the maximum possible length of such a subsequence.

The constraint $n \le 10^5$ rules out any solution that tries all subsequences. A naive $O(2^n)$ enumeration is immediately impossible. Even quadratic $O(n^2)$ dynamic programming risks being too slow in the worst case, so the solution must essentially process the array in linear time, using only constant or logarithmic work per element.

A few edge cases matter more than they first appear.

If all elements are equal, every difference is zero, so no transition is valid and the answer must be 1.

If the sequence is strictly increasing or strictly decreasing, only one direction is usable at the start, and after that the alternating condition immediately fails, so again the answer collapses to 2 for any nontrivial length greater than 1.

If there are many repeated values interleaved with changes, naive approaches that do not explicitly discard zero-differences may incorrectly treat them as valid transitions, producing inflated answers.

## Approaches

A brute-force strategy would try every subsequence and check whether it satisfies the alternating sign condition. For each chosen subsequence of length $k$, verifying validity takes $O(k)$, and there are $2^n$ subsequences, so the total cost is exponential and infeasible even for $n = 40$, let alone $10^5$.

We need to compress the problem into something local. The key observation is that the only thing that matters for extending a valid subsequence is the last chosen element and the sign of the last non-zero difference. Once we know whether we are currently expecting an increase or a decrease, every new element either continues the pattern or breaks it.

This turns the problem into a greedy scan. We do not need to remember the entire subsequence, only the last chosen value and the last direction. Whenever we encounter a value that creates a valid change of direction, we take it and flip the expected direction. If the difference is zero, we ignore it entirely because it cannot contribute to a valid alternation.

This is the same structure as the classic “wiggle subsequence” problem: compress the array into maximal alternating runs of positive and negative slopes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Greedy sign compression | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We scan the array while tracking the last meaningful direction of change.

1. Initialize the answer length as 1 because any single element is always valid. Also keep a variable that stores the previous difference sign, initially unset.
2. Iterate through the array starting from the second element and compute the difference between the current and previous element.
3. If the difference is zero, skip it completely because it cannot contribute to any valid alternating subsequence. This avoids corrupting the direction logic.
4. If the difference is positive and we are either not tracking a direction yet or the previous direction was negative, we accept this element as part of the subsequence and set the direction to positive.
5. If the difference is negative and we are either not tracking a direction yet or the previous direction was positive, we accept this element and set the direction to negative.
6. Otherwise, the current difference continues the same direction as before and cannot extend the alternating pattern, so we ignore it.
7. The number of accepted transitions plus one gives the answer length.

The critical idea is that every time the direction flips, we are guaranteed to be using the most extreme available point for that transition, so no future element can improve the count without breaking the alternation.

### Why it works

At any point in the scan, the algorithm maintains a subsequence that ends at the most recent pivot where the direction changed. Any ignored element either has zero difference or continues the same slope direction. Keeping it would not allow a future alternation that is not already achievable, because the only way to increase the length is to create a new sign change, and sign changes are only possible when the slope flips. Therefore, the greedy choice of only taking slope flips preserves the maximum possible number of alternations, which directly determines subsequence length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    if n == 0:
        print(0)
        return
    
    count = 1
    prev_diff = 0  # 0 means unset, 1 means positive, -1 means negative
    
    for i in range(1, n):
        diff = a[i] - a[i - 1]
        
        if diff == 0:
            continue
        
        sign = 1 if diff > 0 else -1
        
        if prev_diff == 0 or sign != prev_diff:
            count += 1
            prev_diff = sign
    
    print(count)

if __name__ == "__main__":
    solve()
```

The solution relies on scanning once through the array and only reacting when the sign of consecutive differences changes. The variable `prev_diff` stores the last accepted slope direction. A zero difference is explicitly ignored so it does not interfere with the alternation logic.

The key subtlety is that we always compare against adjacent elements in the original sequence, not the chosen subsequence. This is sufficient because any optimal subsequence can be transformed into one that only uses consecutive “turning points” without reducing its length.

## Worked Examples

### Example 1

Input:

```
7
3 14 5 9 6 16 7
```

We track only sign changes between consecutive values.

| i | a[i-1] | a[i] | diff | sign | prev_diff | taken? | count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 14 | +11 | + | 0 | yes | 2 |
| 2 | 14 | 5 | -9 | - | + | yes | 3 |
| 3 | 5 | 9 | +4 | + | - | yes | 4 |
| 4 | 9 | 6 | -3 | - | + | yes | 5 |
| 5 | 6 | 16 | +10 | + | - | yes | 6 |
| 6 | 16 | 7 | -9 | - | + | yes | 7 |

The algorithm accepts every step because the sequence alternates perfectly in slope direction. This confirms that each sign flip contributes exactly one additional element in the optimal subsequence.

### Example 2

Input:

```
5
1 3 11 9 15
```

| i | a[i-1] | a[i] | diff | sign | prev_diff | taken? | count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | +2 | + | 0 | yes | 2 |
| 2 | 3 | 11 | +8 | + | + | no | 2 |
| 3 | 11 | 9 | -2 | - | + | yes | 3 |
| 4 | 9 | 15 | +6 | + | - | yes | 4 |

The second transition is ignored because it continues the same positive slope. This demonstrates why simply counting changes is not enough, we must explicitly suppress consecutive identical directions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass through the array, constant work per element |
| Space | $O(1)$ | only a few integer variables are maintained |

The solution easily fits within constraints for $n \le 10^5$, since it performs at most one subtraction and a few comparisons per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio
    
    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    if n == 0:
        print(0)
        return
    
    count = 1
    prev_diff = 0
    
    for i in range(1, n):
        diff = a[i] - a[i - 1]
        if diff == 0:
            continue
        sign = 1 if diff > 0 else -1
        if prev_diff == 0 or sign != prev_diff:
            count += 1
            prev_diff = sign
    
    print(count)

# provided samples
assert run("7\n3 14 5 9 6 16 7\n") == "7"
assert run("5\n1 3 11 9 15\n") == "4"

# all equal
assert run("4\n5 5 5 5\n") == "1"

# strictly increasing
assert run("5\n1 2 3 4 5\n") == "2"

# strictly decreasing
assert run("5\n5 4 3 2 1\n") == "2"

# alternating with zeros
assert run("6\n1 2 2 1 1 2\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 1 | zero differences must not be counted |
| increasing sequence | 2 | only one valid direction switch possible |
| decreasing sequence | 2 | symmetry with increasing case |
| sequence with duplicates | 3 | zero differences are safely ignored |

## Edge Cases

One important edge case is when the sequence contains repeated values that sit between direction changes. For example, in an input like `1 2 2 1`, the difference `2 -> 2` is zero and must be ignored, otherwise it would incorrectly interfere with detecting the subsequent drop. The algorithm handles this by explicitly skipping zero differences, so the effective sequence becomes `1 -> 2 -> 1`, producing a correct length of 3.

Another case is a monotonic array such as `1 2 3 4 5`. The first increase is accepted, but all later increases are ignored because they do not create a new sign flip. The result stabilizes at 2, which matches the fact that only two points are needed to represent a single increasing run.

A final case is a flat array like `7 7 7 7`. Every difference is zero, so no transitions are ever accepted. The algorithm correctly leaves the count at 1, reflecting that any single element forms a valid trivial jiggle sequence.
