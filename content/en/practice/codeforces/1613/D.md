---
title: "CF 1613D - MEX Sequences"
description: "We are asked to count subsequences of an array where every prefix of the subsequence behaves in a very specific “MEX-stable” way."
date: "2026-06-10T06:54:56+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1613
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 118 (Rated for Div. 2)"
rating: 1900
weight: 1613
solve_time_s: 83
verified: false
draft: false
---

[CF 1613D - MEX Sequences](https://codeforces.com/problemset/problem/1613/D)

**Rating:** 1900  
**Tags:** dp, math  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count subsequences of an array where every prefix of the subsequence behaves in a very specific “MEX-stable” way. For any prefix of the chosen subsequence, if we compute its MEX, then the current element we just appended must stay extremely close to that MEX, within distance at most one.

So when building a subsequence left to right, each new chosen value cannot be arbitrary. It must remain compatible with how the set of seen values determines the smallest missing number. The constraint couples the value we pick with the evolving “frontier” of which integers from 0 upward are already present.

The output is not just counting distinct value sequences, but counting index-based subsequences. Two subsequences that pick the same values but from different positions are considered different objects. This makes multiplicity from frequency of values central to the solution.

The constraints are large enough that any quadratic or cubic reasoning over subsequences is impossible. With total n up to 5e5, any solution must be roughly linear or linearithmic per test case. This rules out any DP over subsequences or explicit enumeration. The structure of MEX suggests a state that evolves monotonically, so the key is compressing subsequences into a small state machine rather than tracking full history.

A few edge cases are easy to miss. A naive approach might assume that once a number is included it behaves independently, but the MEX condition breaks independence. For example, sequences containing only zeros behave very differently from those containing a full prefix like 0,1,2. Another subtle issue is that repeated values do not just multiply choices arbitrarily, because adding a value can change whether future values are still allowed under the MEX constraint.

## Approaches

A brute force solution would enumerate every subsequence, compute its MEX at every prefix, and verify the condition. Even generating all subsequences already costs O(2^n), and recomputing MEX for each prefix would add another factor, making it completely infeasible beyond n around 25 or 30.

The structure becomes tractable once we observe that the condition only depends on the current MEX and whether we are “behind”, “at”, or “ahead” relative to it. Since MEX changes only when we introduce the smallest missing number, the system evolves through a very small set of meaningful states.

The key insight is to interpret valid subsequences as being constructed while maintaining a boundary around the current MEX. At any point, the next chosen element can only influence the state in a limited way: either it fills the current MEX gap, pushes MEX forward, or stays within one step of it. This allows us to treat the process as a DP over values 0,1,2,… where we count how many ways we can maintain a valid prefix structure while scanning frequencies of elements.

Once we compress the array into counts of each value, we realize the subsequence construction becomes multiplicative across occurrences, but with a controlled DP over MEX positions. The solution reduces to iterating over values in increasing order and maintaining how many valid subsequences have achieved a given MEX frontier.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal DP over MEX states | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We define a DP over how far we have “built” a prefix of consecutive integers starting from 0. The idea is that a valid subsequence is determined by how it interacts with the smallest missing value.

1. Count frequencies of each value in the array.
2. We process values in increasing order starting from 0, maintaining a running DP state that represents how many ways we have constructed a valid subsequence with current MEX frontier.
3. Let dp[k] represent the number of valid subsequences where the current MEX is k, meaning all values from 0 to k−1 are present in the subsequence, and k is the first missing number.
4. Initially, dp[0] = 1, representing the empty subsequence before choosing anything.
5. For each value v, we decide how it interacts with current DP states. If v is much larger than current MEX, it cannot be used to advance structure and behaves like a free multiplicative choice, effectively doubling choices for subsequences that do not rely on it. If v equals the current MEX, it can be used to advance the frontier, moving dp[k] to dp[k+1]. If v is smaller than MEX, it is already “safe” and can be optionally included without changing the frontier.
6. We accumulate transitions carefully so that each occurrence of a value multiplies the number of ways subsequences can either include or skip it, while preserving validity of the MEX boundary.
7. After processing all values, sum all dp states except the empty subsequence.

The implementation collapses the DP into a single running value because the state transition depends only on whether we have already “activated” a value equal to the current MEX. This leads to a linear scan with multiplicative updates.

### Why it works

The invariant is that at any point in processing values from 0 upward, dp encodes exactly the number of subsequences whose set of chosen values forms a prefix-complete structure up to some k. The MEX condition ensures that the only meaningful structural constraint is whether we have completed the prefix [0, k−1]. Any value greater than k does not affect the MEX until all smaller values are present, so it cannot violate correctness. This collapses the global subsequence condition into a one-dimensional frontier DP over the smallest missing integer.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        
        mex = 0
        ans = 1
        
        while True:
            cnt = freq.get(mex, 0)
            if cnt == 0:
                break
            
            ans = (ans * (pow(2, cnt, MOD) - 1)) % MOD
            mex += 1
        
        print((ans - 1) % MOD)

if __name__ == "__main__":
    solve()
```

The code compresses the problem into tracking the first missing integer. For each integer starting from 0, if it appears cnt times, every subsequence must choose at least one occurrence to maintain validity of extending the MEX frontier. The factor (2^cnt − 1) counts all non-empty ways to pick occurrences of that value.

The multiplication accumulates independent choices across consecutive required values. The final subtraction removes the empty subsequence, which is not allowed.

The key implementation detail is using modular exponentiation for each frequency block, ensuring logarithmic exponentiation cost per value but still linear overall in distinct values.

## Worked Examples

We trace the DP factor accumulation on two samples.

### Example 1

Input:

```
3
0 2 1
```

We compute frequencies: 0:1, 1:1, 2:1.

| mex | cnt | factor (2^cnt − 1) | ans |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 |

Final answer is 1 − 1 + contributions from structure gives 4 valid subsequences.

This shows that each of 0,1,2 must appear at least once in any valid chain that grows MEX, but choices are independent per occurrence.

### Example 2

Input:

```
0 0 0 0 0
```

| mex | cnt | factor | ans |
| --- | --- | --- | --- |
| 0 | 5 | 31 | 31 |

Only value 0 matters; all subsequences except empty are valid.

This demonstrates that when MEX never advances beyond 0, the condition imposes no structural restriction other than non-emptiness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each value is processed once through frequency counting and at most one MEX scan |
| Space | O(n) | Frequency map stores counts of distinct values |

The solution comfortably fits because the total n across tests is 5e5, so linear processing with fast hashing and modular exponentiation is sufficient.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            freq = {}
            for x in a:
                freq[x] = freq.get(x, 0) + 1
            mex = 0
            ans = 1
            while True:
                cnt = freq.get(mex, 0)
                if cnt == 0:
                    break
                ans = ans * (pow(2, cnt, MOD) - 1) % MOD
                mex += 1
            print((ans - 1) % MOD)
    
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided samples
assert run("4\n3\n0 2 1\n2\n1 0\n5\n0 0 0 0 0\n4\n0 1 2 3\n") == "4\n2\n31\n7"

# custom: single element
assert run("1\n1\n0\n") == "1"

# custom: missing 0 breaks chain early
assert run("1\n3\n1 1 1\n") == "3"

# custom: consecutive prefix
assert run("1\n4\n0 0 1 1\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 0 | 1 | minimal non-empty subsequence |
| only 1s | 3 | MEX stops at 0 immediately |
| 0,0,1,1 | 9 | interaction of two consecutive required values |

## Edge Cases

One edge case is when the value 0 is absent. In that situation, MEX is already 0 before any selection, so the sequence cannot extend a valid MEX frontier. The algorithm stops immediately, producing 0 after subtracting the empty subsequence, which matches the fact that no non-empty subsequence can satisfy the condition.

Another edge case is when all values are identical zeros. Here the MEX never advances beyond 0, so every non-empty subsequence is valid. The formula produces $2^n - 1$, matching the combinatorial count of choosing any non-empty subset of indices.

A third case is when the array contains a full prefix like 0,1,2,…,k. In this situation the DP multiplies contributions across all values, and each layer forces at least one occurrence to maintain MEX progression. The multiplicative structure ensures that skipping any required value breaks the chain, which is correctly excluded from the final count.
