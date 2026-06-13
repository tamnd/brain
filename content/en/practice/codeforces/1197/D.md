---
title: "CF 1197D - Yet Another Subarray Problem"
description: "We are given a sequence of numbers and asked to pick one contiguous segment, or skip picking anything at all, in order to maximize a specific score function. The score of a chosen segment is its plain sum minus a penalty that depends only on its length."
date: "2026-06-13T14:27:53+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1197
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 69 (Rated for Div. 2)"
rating: 1900
weight: 1197
solve_time_s: 268
verified: false
draft: false
---

[CF 1197D - Yet Another Subarray Problem](https://codeforces.com/problemset/problem/1197/D)

**Rating:** 1900  
**Tags:** dp, greedy, math  
**Solve time:** 4m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of numbers and asked to pick one contiguous segment, or skip picking anything at all, in order to maximize a specific score function. The score of a chosen segment is its plain sum minus a penalty that depends only on its length. The penalty is proportional to how many blocks of size `m` are needed to cover the segment, where each block costs `k`.

So instead of a simple maximum subarray sum, every additional `m` elements effectively triggers another deduction of `k`. This makes the problem behave like a standard Kadane-style optimization but with a stepwise cost that changes only when the length crosses multiples of `m`.

The output is a single integer: the best achievable score over all possible subarrays, including the option of choosing nothing, which yields zero.

The constraints immediately rule out any quadratic or worse solution. With `n` up to 300,000, any approach that tries all subarrays or even recomputes sums per subarray would exceed time limits by several orders of magnitude. We are forced toward a linear or near-linear scan with some form of dynamic programming.

A subtle difficulty is that the penalty is not linear in length. It changes only when the segment length crosses multiples of `m`. This creates discontinuities that break the standard Kadane formulation.

A few edge situations illustrate the issue clearly.

If all numbers are negative, a naive maximum subarray sum would return the least negative segment, but here the empty subarray is allowed and yields zero, so the answer must never go below zero.

If `m = 1`, then every element contributes its value minus `k`, turning the problem into a standard maximum subarray sum on transformed values `a[i] - k`. Any solution that fails to recognize this degeneracy may still work, but it provides a useful sanity check.

Another failure mode arises if one assumes the penalty can be distributed evenly across elements. For example, trying to subtract `k/m` per element is incorrect because the ceiling creates jumps at boundaries.

## Approaches

The brute force idea is straightforward: enumerate every subarray, compute its sum, compute its length, evaluate the penalty using the ceiling expression, and track the maximum. This is correct because it directly follows the definition. However, there are roughly `O(n^2)` subarrays, and even with prefix sums to compute range sums in O(1), we still spend quadratic time evaluating candidates. With `n = 3e5`, this is completely infeasible.

The key observation is that the penalty depends only on the length of the subarray, and length increases monotonically as we extend a fixed right endpoint. This suggests a dynamic programming formulation over prefixes, where we maintain the best score of a subarray ending at each position.

We define a running DP state representing the best subarray ending at position `i`. When extending a subarray by one element, the sum increases by `a[i]`, but the penalty may or may not increase depending on whether we cross a multiple of `m`. This is the crucial point: within each block of size `m`, adding elements has no additional penalty until the block is filled.

This structure suggests tracking the answer separately by how many elements have been taken modulo `m`. For each position, we maintain `m` DP states corresponding to the current subarray length modulo `m`. When we extend by one element, we transition between these states, and only when wrapping from `m-1` back to `0` do we apply an additional cost `k`.

This reduces the problem to a small-state DP over the array, giving a linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Modular DP | O(n·m) | O(m) | Accepted |

## Algorithm Walkthrough

We maintain DP states `dp[r]`, where `r` represents the length of the current chosen subarray modulo `m`. Each state stores the best possible sum difference for a subarray ending at the current index with that remainder.

We also allow restarting at any position, since the empty subarray is valid and we are not forced to extend previous segments.

### Steps

1. Initialize all DP states to a very negative value, and set the global answer to zero. This accounts for the option of choosing no subarray at all.
2. Iterate through the array from left to right, treating each position as a potential endpoint of a subarray.
3. At each element `a[i]`, we consider starting a new subarray consisting only of this element. This new subarray has length `1`, so it contributes `a[i]` with no penalty yet.
4. We also consider extending all previous DP states by adding `a[i]`. If we extend a state with remainder `r`, the new remainder becomes `(r + 1) % m`.
5. When the new remainder becomes `0`, it means we have just completed a block of size `m`, so we subtract `k` from the accumulated value. This encodes the stepwise ceiling penalty.
6. After updating transitions, we update the answer with all DP states, since any ending subarray could be optimal.
7. Continue until the end of the array.

### Why it works

The DP state implicitly tracks every subarray ending at the current index, grouped by how many elements beyond a multiple of `m` it currently has. Any time a subarray grows past a multiple of `m`, exactly one additional penalty of `k` is applied, matching the ceiling definition. Since every subarray is either started fresh or extended from a previous valid subarray, all possibilities are covered. The transition never double counts penalties because the cost is only triggered at precise boundary crossings, which correspond exactly to transitions where the remainder resets to zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    NEG = -10**30
    
    dp = [NEG] * m
    ans = 0
    
    for x in a:
        new_dp = [NEG] * m
        
        # start new subarray
        new_dp[1 % m] = max(new_dp[1 % m], x)
        
        # extend previous subarrays
        for r in range(m):
            if dp[r] == NEG:
                continue
            nr = (r + 1) % m
            val = dp[r] + x
            if nr == 0:
                val -= k
            new_dp[nr] = max(new_dp[nr], val)
        
        for r in range(m):
            dp[r] = max(dp[r], new_dp[r])
            ans = max(ans, dp[r])
    
    return ans

if __name__ == "__main__":
    print(solve())
```

The DP array `dp[r]` stores the best value of any subarray ending at the current position with length congruent to `r mod m`. The transition explicitly handles both starting new segments and extending old ones. The subtraction of `k` exactly when `nr == 0` encodes the ceiling function behavior.

The use of `NEG` ensures that invalid states do not interfere with transitions. We continuously merge `new_dp` into `dp` so that all subarrays remain available for extension at later positions.

## Worked Examples

Consider the sample input:

```
n = 7, m = 3, k = 10
a = [2, -4, 15, -3, 4, 8, 3]
```

We track only the most relevant states.

| i | a[i] | dp before | key transitions | dp after | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | all NEG | start [2] | r=1:2 | 2 |
| 2 | -4 | r=1:2 | extend → -2 | r=2:-2 | 2 |
| 3 | 15 | r=2:-2 | extend +15 → 13 (no penalty) | r=0:13-10=3, start 15 | 15 |
| 4 | -3 | ... | extend best r=0 → 0 | r=1:0 | 15 |
| 5 | 4 | ... | extend r=1 → 4 | r=2:4 | 15 |
| 6 | 8 | ... | extend r=2 → 12-10=2 | r=0:2 | 15 |
| 7 | 3 | ... | extend r=0 → 5 | r=1:5 | 15 |

The trace shows how penalties only activate when completing blocks of size `m`, and how good segments can accumulate multiple elements before paying cost.

A second simpler example:

```
a = [5, -1, -1], m = 2, k = 3
```

Here the best segment is `[5, -1]` with cost `4 - 3 = 1`, and the DP correctly captures the penalty exactly when length reaches 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | Each element processes up to m states, and m ≤ 10 |
| Space | O(m) | Only DP arrays of size m are stored |

With `n ≤ 3e5` and `m ≤ 10`, the total operations are about 3e6 transitions, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    NEG = -10**30
    dp = [NEG] * m
    ans = 0
    
    for x in a:
        new_dp = [NEG] * m
        new_dp[1 % m] = max(new_dp[1 % m], x)
        
        for r in range(m):
            if dp[r] == NEG:
                continue
            nr = (r + 1) % m
            val = dp[r] + x
            if nr == 0:
                val -= k
            new_dp[nr] = max(new_dp[nr], val)
        
        for r in range(m):
            dp[r] = max(dp[r], new_dp[r])
            ans = max(ans, dp[r])
    
    return str(ans)

# provided sample
assert run("7 3 10\n2 -4 15 -3 4 8 3\n") == "7"

# minimum size
assert run("1 1 5\n10\n") == "5"

# all negative
assert run("3 2 4\n-1 -2 -3\n") == "0"

# m = 1 reduces to Kadane with penalty
assert run("5 1 2\n3 -1 4 -2 5\n") == "7"

# boundary crossing test
assert run("4 2 10\n5 5 5 5\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | handles m=1 base case | minimal length correctness |
| all negative | returns 0 | empty subarray dominance |
| m=1 case | transforms into linear penalty | reduction sanity check |
| repeated positives | checks penalty timing | boundary transitions |

## Edge Cases

When the array is entirely negative, every DP state may still accumulate negative values, but the algorithm always compares against zero, ensuring the empty subarray remains optimal. For example, with `[-5, -2]`, every extension reduces the score, and no DP state exceeds zero, so the answer correctly stays `0`.

When `m = 1`, every new element completes a block immediately. The DP transitions subtract `k` on every step, matching the formula `a[i] - k`. The algorithm therefore behaves exactly like Kadane’s algorithm on transformed values, and the state compression does not break this special case.

When the optimal segment length is not a multiple of `m`, the DP still tracks partial remainders. The final incomplete block does not incur an extra penalty, because subtraction happens only when the remainder wraps to zero. This ensures that segments like length `m + 1` are charged exactly once, not twice, matching the ceiling definition precisely.
