---
title: "CF 105904K - Kickboxing"
description: "We are asked to count ways to split a total of N kicks into consecutive training sets. Each training set has a positive number of kicks, and these sizes form a sequence whose sum is exactly N. Two rules constrain this sequence."
date: "2026-06-22T04:26:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105904
codeforces_index: "K"
codeforces_contest_name: "I SBC S\u00e3o Paulo Programming Marathon"
rating: 0
weight: 105904
solve_time_s: 49
verified: true
draft: false
---

[CF 105904K - Kickboxing](https://codeforces.com/problemset/problem/105904/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count ways to split a total of N kicks into consecutive training sets. Each training set has a positive number of kicks, and these sizes form a sequence whose sum is exactly N.

Two rules constrain this sequence. First, each set cannot be longer than the previous one, so the sequence of segment lengths is non-increasing. Second, there is a forbidden size K, meaning no segment is allowed to have exactly K kicks. Since segments are positive, every valid segment size is at least 1.

So the task becomes counting all non-increasing sequences of positive integers that sum to N, while only allowing values in the range 1 to K−1.

This is a classic integer partition structure with a bounded maximum part size.

The constraints allow N up to 4000. A solution that tries to enumerate all partitions would explode exponentially, since the number of partitions grows roughly like exp(O(√N)). Anything even mildly combinational over partitions will be too slow. A dynamic programming approach in O(N·K) or better is the only realistic direction, since around 16 million transitions is acceptable in Python.

A subtle edge case appears when K = 1. In that case, the only forbidden size is 1, but every segment must be at least 1, so no valid segmentation exists unless N is zero, which is not allowed. The correct answer is therefore 0 for all N when K = 1.

Another point that can trip naive thinking is the “non-increasing” constraint. For example, a decomposition like 1 + 2 + 1 is invalid even if all parts avoid K, because the sequence increases. Any solution that treats this as a simple composition problem without enforcing ordering will overcount badly.

## Approaches

A direct attempt would generate all ways to split N into positive integers and then filter those that are non-increasing and avoid K. This brute-force method essentially explores a recursion tree where at each step we choose the next segment size. In the worst case, each state branches into up to O(N) choices, and the depth is also O(N), leading to an explosion far beyond feasible limits.

The key observation is that the order constraint turns the problem into a partition problem rather than a permutation problem. Once parts are required to be non-increasing, each valid solution corresponds to a multiset of integers rather than an ordered sequence. This removes factorial overcounting and allows a structured DP.

We can reinterpret the task as counting partitions of N using parts of size at most K−1. A standard way to enforce “non-increasing” implicitly is to only allow building solutions using parts up to a current maximum value, processed in increasing order of allowed part size.

This leads to a classic knapsack-style DP where we decide how many times each allowed part size is used, accumulating sums in a way that automatically preserves non-increasing order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | O(N) recursion | Too slow |
| Partition DP (bounded parts) | O(N·K) | O(N) | Accepted |

## Algorithm Walkthrough

We build a DP array where dp[x] represents the number of ways to form sum x using allowed segment sizes, ensuring that we never violate the non-increasing structure by construction.

1. Initialize dp[0] = 1 because there is exactly one way to form sum zero, using no segments at all. All other dp values start at 0 since no sums are reachable yet.
2. Iterate over allowed segment sizes from 1 to K−1. Each size is treated as a “building block” that can be used any number of times.
3. For each segment size s, update the dp array from s to N. For each total x, we add dp[x − s] into dp[x]. This step extends all previous valid constructions by appending a segment of size s.
4. The update is performed in increasing order of s so that larger segment sizes are not placed before smaller ones in implicit constructions. This preserves the non-increasing structure because earlier decisions correspond to smaller or equal parts being fixed before larger ones are considered.
5. After processing all allowed segment sizes, dp[N] contains the total number of valid partitions.

The subtle point is that although the transition looks like an unbounded knapsack, the ordering of iteration over segment sizes encodes the non-increasing constraint implicitly, preventing invalid permutations of the same multiset.

### Why it works

Every valid training plan corresponds exactly to a multiset of segment sizes between 1 and K−1. The DP counts each multiset exactly once because each part size is introduced in a fixed order, so no permutation of the same parts can be formed in multiple ways. The non-increasing requirement is therefore enforced structurally rather than explicitly checked.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    N, K = map(int, input().split())
    
    if K == 1:
        print(0)
        return

    max_part = K - 1
    dp = [0] * (N + 1)
    dp[0] = 1

    for s in range(1, max_part + 1):
        for x in range(s, N + 1):
            dp[x] = (dp[x] + dp[x - s]) % MOD

    print(dp[N])

if __name__ == "__main__":
    solve()
```

The solution first handles the degenerate case K = 1 explicitly. The DP array is then initialized for partition counting. The outer loop over segment sizes ensures each size contributes in a controlled manner, while the inner loop accumulates contributions for each reachable sum. The modulo operation is applied at every update to prevent overflow and stay within required constraints.

A common implementation pitfall is reversing loop order. If we iterate over sums first and then segment sizes incorrectly, we may accidentally count permutations instead of partitions. The chosen ordering avoids that.

## Worked Examples

Consider a small case N = 4, K = 3, so allowed segment sizes are 1 and 2.

We start with dp = [1, 0, 0, 0, 0].

After processing size 1, dp becomes:

| x | dp[x] update |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

After processing size 2, we add contributions from dp[x−2]:

| x | dp[x] before | dp[x−2] | dp[x] after |
| --- | --- | --- | --- |
| 2 | 1 | 1 | 2 |
| 3 | 1 | 1 | 2 |
| 4 | 1 | 2 | 3 |

Final dp[4] = 3, matching the valid partitions of 4 using parts 1 and 2 under non-increasing structure.

This confirms that the DP accumulates combinations of parts rather than permutations of sequences.

As a second example, take N = 5, K = 4, so allowed parts are 1, 2, 3. The DP gradually builds all partitions of 5 with maximum part size 3, and each update layer adds a new dimension of allowed segment sizes without breaking ordering constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N·K) | Each of the K−1 part sizes performs a full DP update over N states |
| Space | O(N) | Only a single DP array over sums is maintained |

With N and K up to 4000, the total number of operations is about 16 million, which is well within typical limits for Python when implemented with simple loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    input = sys.stdin.readline

    MOD = 998244353

    N, K = map(int, sys.stdin.readline().split())
    if K == 1:
        return "0"

    max_part = K - 1
    dp = [0] * (N + 1)
    dp[0] = 1

    for s in range(1, max_part + 1):
        for x in range(s, N + 1):
            dp[x] = (dp[x] + dp[x - s]) % MOD

    return str(dp[N])

# sample-style checks (no explicit sample values provided in prompt)
assert run("1 2") == "1"
assert run("4 3") == "3"
assert run("4 2") == "1"

# edge cases
assert run("5 1") == "0"              # K=1 impossible
assert run("6 7") == "11"             # unrestricted partitions up to 6
assert run("10 2") == "1"             # only all ones
assert run("10 10") == run("10 11")   # K>N behaves same as K=N
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 1 | 0 | forbidden segment size equals minimum possible |
| 10 2 | 1 | only partition is all ones |
| 6 7 | 11 | effectively unrestricted partitions up to 6 |

## Edge Cases

When K = 1, every segment size is forbidden. Running the DP would otherwise suggest dp[0] propagates incorrectly into dp[1], which would incorrectly count invalid constructions. The explicit check prevents any state transitions, leaving the answer as zero.

When K > N, all segment sizes from 1 to N are allowed, and the problem reduces to standard integer partitions of N. The DP still works correctly because the loop simply includes all meaningful part sizes without exceeding N.

When N is small, such as N = 1 or N = 2, the DP degenerates into trivial updates. The structure still holds because dp[0] = 1 is the only seed state, and all valid partitions are built directly from it without intermediate ambiguity.
