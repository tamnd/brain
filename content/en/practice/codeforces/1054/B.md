---
title: "CF 1054B - Appending Mex"
description: "We are given a sequence that is claimed to be constructed step by step starting from an empty array. At each step, the builder is allowed to look at any subset of elements that already exist in the array, compute the mex of that subset, and append that mex as the next element."
date: "2026-06-15T10:22:07+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1054
codeforces_index: "B"
codeforces_contest_name: "Mail.Ru Cup 2018 Round 1"
rating: 1000
weight: 1054
solve_time_s: 152
verified: true
draft: false
---

[CF 1054B - Appending Mex](https://codeforces.com/problemset/problem/1054/B)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 2m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence that is claimed to be constructed step by step starting from an empty array. At each step, the builder is allowed to look at any subset of elements that already exist in the array, compute the mex of that subset, and append that mex as the next element.

The mex of a multiset is the smallest non-negative integer that does not appear in it. So the process is extremely flexible: at each step you can “query” any subset of the past and append the missing value.

The task is not to reconstruct the construction itself, but to detect consistency. We are given the final array, and we must decide whether there exists any sequence of subset choices that could produce it. If yes, we output -1. Otherwise, we must output the earliest prefix where some step must already be impossible in any valid construction.

The constraint n up to 100000 forces any solution to be linear or near-linear. Anything that tries to recompute mex over many subsets or simulate all choices is immediately infeasible, since the number of subsets grows exponentially. Even maintaining dynamic structures per step must be O(log n) or better.

A key subtlety is that the operation depends only on the set of values present in a chosen subset, not their order or multiplicity beyond presence. This means reasoning is fundamentally about which values are already available globally at each step.

A few failure cases that are easy to miss:

If the first element is not 0, the construction is immediately impossible. Since the initial array is empty, the only subset is empty, whose mex is 0, so the first element must always be 0.

Another tricky situation arises when a number appears that could not be generated given the current “available set” of values. For instance, if we see a value x but we have not yet ensured that all values 0 through x−1 have appeared somewhere earlier in the prefix, then x cannot be produced as a mex of any subset.

Finally, once we see a number, it affects future feasibility because it may become usable inside subsets. So we must maintain a growing set of “available numbers”.

## Approaches

A direct brute-force interpretation would try to simulate every step: for each position m, consider all subsets of previous elements, compute mex for each subset, and check if the current value is achievable. This is correct in principle because it exactly mirrors the definition. However, even for a single step there are 2^(m−1) subsets, making this exponential. At n = 100000, this is completely infeasible.

The key observation is that we never actually need to enumerate subsets. The mex of a subset depends only on which values from 0 upward are present in that subset. If a subset can produce mex x, then that subset must contain every integer from 0 to x−1 and must be missing x. So the real question becomes: at step i, is it possible that there exists some subset of previously seen elements whose contents allow mex = a[i]?

This reduces to a structural condition on the global prefix: we must be able to ensure that all numbers less than a[i] exist somewhere in earlier elements, otherwise no subset can include them simultaneously. Also, if a[i] is larger than what is currently “constructible”, it may force a contradiction.

A clean way to track feasibility is to maintain which values have already appeared in the prefix. Then we can check whether the current value is consistent with being a mex outcome. The construction fails exactly when we are asked to produce a value that is not the mex of any subset given the available set structure, which reduces to checking whether all smaller values exist in the prefix when needed and whether ordering constraints are violated.

The final solution becomes a single pass maintaining a frequency set and tracking the smallest missing value pattern implicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We scan the array from left to right while maintaining which values have appeared.

1. We initialize a boolean set or array `seen` to record which integers have appeared so far, and a pointer `mex` starting at 0.

The pointer represents the smallest non-negative integer not yet seen in the prefix.
2. For each position i from 1 to n, we read a[i].
3. If a[i] is greater than mex, we immediately conclude that the construction is impossible.

The reason is that mex of any subset of previous elements cannot exceed the global mex of the prefix, because any subset can only use values already present in the prefix.
4. If a[i] equals mex, this is always achievable: we can take a subset containing all values 0 through mex−1 (which must exist in the prefix), and omit mex itself, producing mex as the result. So we accept this step.
5. If a[i] is less than mex, then it is also achievable because we can choose a subset that contains all numbers 0 through a[i]−1 but excludes a[i], which is possible since mex is larger, meaning all those values exist.
6. After processing a[i], we mark it as seen and advance mex while seen[mex] is true.

We track the earliest position where step 3 triggers. That index is the first guaranteed mistake.

### Why it works

The invariant is that `mex` always represents the smallest number not present anywhere in the prefix. Any subset mex must lie in the range from 0 up to mex. If a value larger than mex appears in the output, it implies a subset produced a mex greater than what the prefix allows, which contradicts the definition of mex. Conversely, any value less than or equal to mex is achievable because the prefix already contains all required smaller numbers, allowing construction of a subset whose mex matches the target.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    seen = set()
    mex = 0

    for i, x in enumerate(a):
        if x > mex:
            print(i + 1)
            return

        seen.add(x)
        while mex in seen:
            mex += 1

    print(-1)

if __name__ == "__main__":
    solve()
```

The code maintains a running set of values already seen in the array and continuously updates the current global mex. The key check happens before inserting the current value: if the value exceeds the current mex, it violates the structural bound that no subset can generate a mex larger than what is globally missing.

The update step ensures mex always reflects the prefix state, and this is essential because future validity depends on which values have been introduced so far.

## Worked Examples

### Example 1

Input:

```
4
0 1 2 1
```

We track `seen` and `mex`:

| i | a[i] | seen before | mex before | action | mex after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | {} | 0 | add 0 | 1 |
| 2 | 1 | {0} | 1 | add 1 | 2 |
| 3 | 2 | {0,1} | 2 | add 2 | 3 |
| 4 | 1 | {0,1,2} | 3 | add 1 | 3 |

At no point does a value exceed mex, so the sequence is consistent. The algorithm outputs -1, matching the fact that the construction is feasible.

### Example 2

Input:

```
3
0 2 1
```

| i | a[i] | seen before | mex before | action |
| --- | --- | --- | --- | --- |
| 1 | 0 | {} | 0 | ok, mex becomes 1 |
| 2 | 2 | {0} | 1 | 2 > 1, fail |

At step 2 we encounter 2 while mex is 1. This is impossible because no subset of {0} can produce mex 2. The algorithm outputs 2.

This confirms that the first violation is detected immediately when the structural bound is broken.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each value is inserted once and mex advances at most n times overall |
| Space | O(n) | The set stores up to n distinct values |

The constraints allow up to 100000 elements, so a single linear pass with constant or amortized constant updates fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve()) if False else ""

# We redefine properly for testing
def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    seen = set()
    mex = 0

    for i, x in enumerate(a):
        if x > mex:
            return str(i + 1)
        seen.add(x)
        while mex in seen:
            mex += 1

    return "-1"

def run(inp: str) -> str:
    return solve_io(inp)

# provided samples
assert run("4\n0 1 2 1\n") == "-1", "sample 1"

# custom tests
assert run("1\n0\n") == "-1", "single valid"
assert run("1\n1\n") == "1", "must start with 0"
assert run("3\n0 2 1\n") == "2", "early violation"
assert run("5\n0 1 2 3 0\n") == "-1", "restarts allowed"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element valid | -1 | minimal valid construction |
| first element 1 | 1 | forced failure at step 1 |
| 0 2 1 | 2 | early mex violation |
| 0 1 2 3 0 | -1 | large increasing then reset |

## Edge Cases

A critical edge case is when the first element is non-zero. For input `1`, the only subset at step 1 is empty, whose mex is 0, so any value other than 0 immediately implies impossibility. The algorithm handles this because `x > mex` is true at the first step when mex is still 0.

Another case is when values jump above the current mex, such as `0 5 ...`. At step 2, mex is 1, so seeing 5 triggers an immediate failure. This correctly captures the fact that no subset of `{0}` can ever produce a mex beyond 1.

A subtle case is repeated small values like `0 0 0 0`. Here mex stays 1 after the first insertion, and all subsequent zeros are valid since subsets can always produce 0 by choosing an empty subset or one missing 0. The algorithm correctly never triggers a failure since no value exceeds mex.
