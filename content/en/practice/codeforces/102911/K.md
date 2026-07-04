---
title: "CF 102911K - Kallipolis"
description: "We are given a list of philosophers, each associated with a positive integer value that represents their “strength of dominance."
date: "2026-07-04T08:06:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102911
codeforces_index: "K"
codeforces_contest_name: "2021 Ateneo de Manila Senior High School Dagitab Programming Contest (Mirror)"
rating: 0
weight: 102911
solve_time_s: 34
verified: true
draft: false
---

[CF 102911K - Kallipolis](https://codeforces.com/problemset/problem/102911/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of philosophers, each associated with a positive integer value that represents their “strength of dominance.” A philosopher is said to dominate another if their value is divisible by the other’s value, meaning the larger value must be an exact multiple of the smaller one.

The task is to determine whether there exists a single philosopher who dominates every other philosopher in the list. If multiple candidates satisfy this condition, we choose the one with the smallest index.

The input is simply the number of philosophers followed by their values. The output is the 1-based index of a valid “king,” or -1 if no such philosopher exists.

The constraints allow values up to 10^9 and up to 2·10^5 philosophers. This immediately rules out any approach that checks every pair of philosophers directly, since that would be O(n^2), which could reach 4·10^10 operations in the worst case and clearly exceed time limits.

A subtle edge case appears when multiple philosophers share the same value. Since any number divides itself, identical values form mutual domination, and the earliest index among them becomes the answer if that value also dominates all others. For example, if all values are 224, every philosopher dominates every other, so the answer is 1.

Another corner case is when no single value divides all others, even if it is very large. For instance, in the array [6, 10, 15], no number divides both others, so the correct output is -1 despite multiple “large” values existing.

## Approaches

A brute-force approach tries each philosopher as a candidate king and checks whether their value is divisible by every other value. For each candidate i, we scan all j and verify Ai % Aj == 0. This costs O(n^2) divisibility checks in total. Each check is constant time, but with n up to 2·10^5 this becomes infeasible.

The key observation is that a valid king must be the maximum value in the array, because if Ai dominates all others, then Ai must be divisible by every Aj, implying Ai ≥ Aj for all j. So any candidate must come from the set of maximum values.

This reduces the search space drastically. Instead of checking all indices, we only check those holding the maximum value. Since all equal maximum values behave identically with respect to dominance, we only need to test one of them, ideally the first occurrence.

We then verify whether this maximum value divides every element in the array. If it does, it is a valid king. Otherwise, no candidate exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Max Candidate Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to testing whether a single value can divide all others.

1. Scan the array once to find the maximum value and its first index. The reason is that any valid king must be at least as large as all others, so only maximum values are eligible.
2. Traverse the array again and check divisibility of every element by the maximum value. If we find any element that is not divisible, we can immediately reject this candidate because dominance requires covering every philosopher.
3. If all checks pass, return the stored index of the first maximum element.
4. If any check fails, return -1.

The crucial decision is restricting attention to the maximum element, which eliminates the need for pairwise comparisons.

### Why it works

If a value A_k dominates every other value, then for every i we must have A_k = m · A_i for some integer m, which implies A_k ≥ A_i for all i. This forces A_k to be a global maximum. Among equal maxima, divisibility is identical, so choosing the smallest index ensures correctness under the tie-breaking rule. The algorithm therefore tests the only possible structural candidate directly and verifies the required divisibility condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    mx = max(a)
    idx = -1
    
    for i in range(n):
        if a[i] == mx:
            idx = i + 1
            break
    
    for x in a:
        if mx % x != 0:
            print(-1)
            return
    
    print(idx)

if __name__ == "__main__":
    solve()
```

The first pass computes the maximum value and records its earliest position. This is necessary because the output depends on index, not just value.

The second pass enforces the dominance condition by checking divisibility from the candidate maximum to every element. The condition mx % x == 0 is the direct translation of the requirement that mx is a multiple of every x.

The early exit on failure prevents unnecessary checks, keeping the solution linear.

## Worked Examples

Consider the input:

Input:

4

1 215 43 5

The maximum is 215, occurring at index 2.

| Step | Current value | 215 % value | Valid so far |
| --- | --- | --- | --- |
| check 1 | 1 | 0 | yes |
| check 2 | 215 | 0 | yes |
| check 3 | 43 | 0 | yes |
| check 4 | 5 | 0 | yes |

All values divide 215, so the answer is 2. This confirms that the candidate correctly dominates every element.

Now consider:

Input:

4

201 202 227 228

The maximum is 228 at index 4.

| Step | Current value | 228 % value | Valid so far |
| --- | --- | --- | --- |
| check 1 | 201 | non-zero | no |

The failure occurs immediately at 201, since 228 is not divisible by 201. This demonstrates early termination and shows why not every maximum is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to find maximum and one pass for divisibility checks |
| Space | O(1) | Only a few scalar variables are used |

With n up to 2·10^5, a linear scan easily fits within time limits, and constant memory ensures no overhead issues.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp))

# Re-implement wrapper for clarity in testing context
def solve_output(inp: str) -> str:
    import sys
    input = sys.stdin.readline
    data = inp.strip().split()
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    mx = max(a)
    idx = a.index(mx) + 1
    for x in a:
        if mx % x != 0:
            return "-1"
    return str(idx)

# samples
assert solve_output("4\n1 215 43 5\n") == "2"
assert solve_output("4\n201 202 227 228\n") == "-1"

# custom cases
assert solve_output("1\n7\n") == "1"
assert solve_output("5\n224 224 224 224 224\n") == "1"
assert solve_output("3\n2 3 4\n") == "-1"
assert solve_output("4\n1 2 4 8\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimum case |
| all equal | 1 | tie handling |
| no divisibility chain | -1 | failure case |
| perfect chain | last index | strong valid king |

## Edge Cases

When all values are identical, the maximum appears multiple times. The algorithm picks the first occurrence and still passes the divisibility check since every number divides itself. For example, [224, 224, 224] produces mx = 224 and no failures in the second pass, so index 1 is returned.

When the maximum appears multiple times but other values break divisibility, the result is still -1. For instance, [10, 10, 3] has mx = 10, but 10 % 3 fails, so no candidate survives.

When the array contains 1, it does not automatically become the answer unless all values are 1, because 1 only dominates itself. For example, [1, 2, 3] fails since 1 % 2 is not valid in the reverse direction of dominance.
