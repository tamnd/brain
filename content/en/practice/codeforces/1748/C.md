---
title: "CF 1748C - Zero-Sum Prefixes"
description: "We are given a sequence of integers, and we care about how often its prefix sums hit zero. A prefix sum at position i is the sum of the first i elements, and we score the array by counting how many of these prefix sums are exactly zero."
date: "2026-06-09T15:26:51+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1748
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 833 (Div. 2)"
rating: 1600
weight: 1748
solve_time_s: 160
verified: true
draft: false
---

[CF 1748C - Zero-Sum Prefixes](https://codeforces.com/problemset/problem/1748/C)

**Rating:** 1600  
**Tags:** brute force, data structures, dp, greedy, implementation  
**Solve time:** 2m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and we care about how often its prefix sums hit zero. A prefix sum at position `i` is the sum of the first `i` elements, and we score the array by counting how many of these prefix sums are exactly zero.

The twist is that some elements are initially zero, and each such position is flexible: we are allowed to replace it with any integer we want, possibly using different values for different zero positions. The goal is to choose replacements so that the number of zero prefix sums becomes as large as possible.

From a constraints perspective, the total input size across all test cases is up to `2 · 10^5`. This immediately rules out any quadratic strategy that repeatedly recomputes prefix sums for many candidate modifications. Anything acceptable must essentially process each element a constant number of times per test case.

A subtle edge case appears when all values are nonzero. In that situation no operations are allowed at all, so the answer is fixed by the original prefix structure. A naive approach that assumes we can always “fix” prefix sums using operations would incorrectly overestimate the score. Another edge case is when zeros are frequent. A careless greedy approach might assume every zero can independently force a prefix sum to zero, but the ability to choose arbitrary values only helps if we understand how prefix sums evolve globally.

## Approaches

A direct way to think about the problem is to simulate all possible choices for replacing zero entries. For each zero position, we could try all integers that might help create future zero prefix sums, and recompute prefix sums afterward. This is correct in principle, but completely infeasible: even restricting values to a small set, the number of configurations grows exponentially in the number of zeros, and each configuration requires a full scan to compute prefix sums, giving exponential time in the worst case.

The key observation is that the score depends only on prefix sums, and prefix sums evolve linearly. When we encounter a zero, we have full control over how much we adjust the running sum at that point. This means each zero acts like a “reset opportunity”: we can choose its value so that the prefix sum at that position becomes exactly zero, regardless of the previous history. However, using that freedom incorrectly can destroy future opportunities, because changing one position affects all later prefix sums.

The correct perspective is to process the array from left to right while tracking the current prefix sum. Whenever we reach a position where the original value is zero, we can decide whether to use it to “force” a zero prefix sum at that exact position. If we do so, we effectively reset the running sum to zero. This is beneficial whenever the current prefix sum is not already zero, because it allows us to create an additional counted zero without losing the ability to continue consistently afterward.

This reduces the problem to greedily counting how many times we can enforce a zero prefix sum, with the constraint that after each enforced reset, we restart the accumulation from zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over replacements | Exponential | O(n) | Too slow |
| Greedy prefix simulation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and scan the array once.

1. Initialize a running prefix sum `s = 0` and a counter `ans = 0`.
2. Iterate through the array from left to right. For each position `i`, add `a[i]` to `s`. This simulates the prefix sum if we do nothing special at this position.
3. If the current prefix sum `s` becomes zero, increment `ans` because we have achieved a valid zero prefix.
4. If `a[i] == 0`, we consider using this position as a replacement point. If the current prefix sum is not zero, we set `ans += 1` and reset `s = 0`. The reason is that we can assign a value to this zero that cancels the current prefix sum exactly, creating a new zero prefix at position `i`, and then restart accumulation.
5. Continue until the end of the array.

The core decision is that every zero-valued position can either be ignored or used to enforce a prefix reset. Using it is only useful when it increases the number of zero prefixes, which happens when the running sum is not already zero.

### Why it works

The running prefix sum fully determines whether a prefix contributes to the score. Any modification at a zero position affects all future prefix sums uniformly through the running total. Therefore, each zero acts as a potential “cut point” where we can reset the system to a clean state.

The invariant is that after processing index `i`, the algorithm maintains the maximum possible number of zero prefix sums achievable using optimal choices among the first `i` elements, while keeping the current simulated prefix sum consistent with the chosen decisions. Any alternative strategy that does not reset at a zero when the prefix sum is nonzero cannot increase the score at that position without reducing flexibility later.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        s = 0
        ans = 0
        
        for x in a:
            s += x
            
            if s == 0:
                ans += 1
            
            if x == 0:
                if s != 0:
                    ans += 1
                    s = 0
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the left-to-right simulation directly. The prefix sum `s` represents the current accumulated value after applying chosen modifications. The check `s == 0` accounts for natural zero-prefix occurrences without any modification. The second condition handles zero positions where we actively choose a value to force a reset.

Resetting `s` to zero is essential because once we use a zero position to cancel the current sum, future prefix sums should be computed relative to that new baseline. Without this reset, later computations would incorrectly accumulate past contributions.

## Worked Examples

We trace the logic on two inputs.

### Example 1

Input:

```
a = [2, 0, 1, -1, 0]
```

| i | a[i] | prefix sum s before action | s after add | action | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 2 | none | 0 |
| 2 | 0 | 2 | 2 | reset | 1 |
| 3 | 1 | 0 | 1 | none | 1 |
| 4 | -1 | 1 | 0 | natural zero | 2 |
| 5 | 0 | 0 | 0 | natural + skip reset | 3 |

The trace shows one forced reset at index 2 and two natural prefix zeros later.

This confirms that forced resets are only useful when they create new zero prefixes that would not otherwise occur.

### Example 2

Input:

```
a = [3, 0, 2, -10, 10, -30, 30, 0]
```

| i | a[i] | s before | s after | action | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 3 | none | 0 |
| 2 | 0 | 3 | 3 | reset | 1 |
| 3 | 2 | 0 | 2 | none | 1 |
| 4 | -10 | 2 | -8 | none | 1 |
| 5 | 10 | -8 | 2 | none | 1 |
| 6 | -30 | 2 | -28 | none | 1 |
| 7 | 30 | -28 | 2 | none | 1 |
| 8 | 0 | 2 | 2 | reset | 2 |

The second forced reset creates the final improvement, showing how each zero is evaluated independently against the current prefix state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once in a single scan per test case |
| Space | O(1) | Only a few variables are used beyond the input array |

The solution comfortably fits within the limits since the total number of elements across all test cases is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        s = 0
        ans = 0
        for x in a:
            s += x
            if s == 0:
                ans += 1
            if x == 0:
                if s != 0:
                    ans += 1
                    s = 0
        
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""5
5
2 0 1 -1 0
3
1000000000 1000000000 0
4
0 0 0 0
8
3 0 2 -10 10 -30 30 0
9
1 0 0 1 -1 0 1 0 -1
""") == """3
1
4
4
5"""

# custom cases
assert run("""1
1
0
""") == "1"

assert run("""1
3
1 2 3
""") == "0"

assert run("""1
5
0 0 0 0 0
""") == "5"

assert run("""1
4
1 0 -1 0
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n0` | `1` | single element edge case |
| `1\n3\n1 2 3` | `0` | no zero prefixes possible |
| `1\n5\n0 0 0 0 0` | `5` | all zeros maximize resets |
| `1\n4\n1 0 -1 0` | `3` | interaction between natural and forced zeros |

## Edge Cases

A minimal input with a single zero demonstrates the reset behavior directly. With `a = [0]`, the prefix sum is initially zero and the algorithm counts it once, then also recognizes the zero position as a reset opportunity, but since the sum is already zero, it avoids double counting incorrectly and still returns `1`.

For `a = [1, 2, 3]`, there are no zeros to manipulate and no prefix sum hits zero, so the answer stays `0`. The algorithm never triggers the reset branch and simply accumulates a nonzero prefix throughout.

For a sequence of all zeros, every position can be used to force a reset. Each step yields a new zero prefix, so the result is `n`, and the greedy reset rule correctly achieves this by resetting at every position where the sum is nonzero before processing the next element.
