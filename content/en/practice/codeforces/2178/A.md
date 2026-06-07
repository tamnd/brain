---
title: "CF 2178A - Yes or Yes"
description: "We are given a string consisting only of two symbols, where one behaves like a neutral value and the other behaves like an absorbing “true” value under an OR-like merge operation."
date: "2026-06-07T22:21:37+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 2178
codeforces_index: "A"
codeforces_contest_name: "Good Bye 2025"
rating: 800
weight: 2178
solve_time_s: 79
verified: true
draft: false
---

[CF 2178A - Yes or Yes](https://codeforces.com/problemset/problem/2178/A)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting only of two symbols, where one behaves like a neutral value and the other behaves like an absorbing “true” value under an OR-like merge operation. The operation allows us to pick two adjacent characters, delete them, and replace them with their logical OR: if either character is Y, the result is Y, otherwise it is N. Each operation shortens the string by exactly one character, and we keep repeating this until only one character remains.

The restriction is that at no point are we allowed to directly merge two Y characters. That move is forbidden even though it would normally still produce Y. The task is to decide whether there exists some sequence of merges that reduces the string to a single character without ever selecting a YY pair.

The constraints are small: each string has length at most 100 and there are up to 500 test cases. This immediately rules out any need for complex dynamic programming over large states or search over all merge orders. Even exponential exploration of all merge sequences might be conceivable at n = 100 in theory, but the additional constraint forbidding YY merges prunes the structure heavily enough that a direct combinational characterization is expected.

A key subtlety is that merging changes adjacency relationships. A naive interpretation might assume we can just count Y and N, but adjacency matters because Y’s can become neighbors after deletions. Another subtle pitfall is thinking that avoiding YY merges means Y’s must remain separated forever, which is not true because Y can move “through” N merges indirectly.

For example, in `YNY`, it is possible to merge `NY -> Y` giving `YY`, which is already invalid if we had to merge them directly later. But in some configurations, careful ordering prevents ever having to merge two Y’s directly even if multiple Y’s exist.

So the real question is whether we can schedule merges so that no step ever produces a YY adjacency at the moment of a merge.

## Approaches

The brute force idea is to simulate all possible ways of reducing the string by repeatedly choosing adjacent pairs to merge, while tracking whether a YY merge was ever used. This forms a state space where each state is a string, and transitions correspond to merging any adjacent pair. The number of possible merge sequences is enormous, since a string of length n has roughly n choices initially, then n−1, and so on, leading to factorial growth. Even though n is only 100, this is far too large to explore.

The key observation is that we do not actually care about intermediate strings in full detail. The only dangerous event is when two Y’s become adjacent at the moment we decide to merge them. This suggests that Y’s behave like obstacles that must be separated by at least one N at every stage where they might become neighbors.

Now look at what an N does. Merging anything involving an N tends to either remove N or “absorb” it into Y. This means N’s are not stable barriers. However, a crucial structural simplification appears: if there are at least two Y’s in the string, then at some point during any reduction, those Y’s will inevitably become adjacent in any final single-character reduction unless there is at least one N to separate them throughout the process. But N’s are consumed, so they cannot permanently separate multiple Y’s.

This leads to a strong dichotomy: if there are two or more Y’s, the answer is generally NO, except in cases where the structure allows us to collapse everything without ever needing a YY merge. That turns out to be impossible when there are at least two Y’s because any contraction process that reduces length to one must eventually merge across a boundary that forces Y adjacency.

The only surviving safe cases are:

when there are no Y’s, or exactly one Y with surrounding N’s arranged so that Y never meets another Y during contraction. In fact, this simplifies further to a clean condition: the string is valid iff it contains at most one Y.

We can justify this by checking that:

if there are zero Y’s, every merge is NN → N, so the string always remains all N and is trivially reducible.

if there is exactly one Y, every merge involving it with N yields Y, and since no second Y exists, no forbidden YY merge can ever occur.

if there are two or more Y’s, any reduction to a single character requires eventually combining regions containing Y’s, which forces a YY adjacency at some step in any sequence of merges.

So the problem reduces to a simple counting condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of all merge orders | O(n!) | O(n) | Too slow |
| Count Y’s and check if ≤ 1 | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. For each test case, scan the string and count how many characters are equal to Y. This captures all information relevant to whether a forbidden merge can ever be forced.
2. If the count of Y is zero, immediately output YES. No operation can ever create a Y, so the string behaves as a purely collapsing sequence of N values.
3. If the count of Y is exactly one, output YES. Any merge involving that single Y can never involve another Y, so the forbidden operation is never triggered.
4. If the count of Y is two or more, output NO. With multiple Y’s present, any full reduction to a single character necessarily brings Y’s into adjacency at some intermediate stage, making a forbidden merge unavoidable.

### Why it works

The only way to produce a Y during operations is through merging with at least one Y. Once multiple Y’s exist, every reduction step preserves or reduces their number, but cannot separate them into permanently isolated components because merges eliminate boundaries. Since the process must reduce the string to a single character, all regions eventually interact. That guarantees a stage where two Y-origin regions become adjacent and would need to be merged directly, violating the constraint. With at most one Y, no such interaction between Y-origin regions exists, so the process can always proceed safely.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    y_count = s.count('Y')
    if y_count <= 1:
        print("YES")
    else:
        print("NO")
```

The implementation directly applies the observation that only the number of Y characters matters. The `.count()` operation scans the string once per test case, which is sufficient given the constraints.

The only subtle point is ensuring we treat all cases uniformly: both empty-N-dominant strings and single-Y strings are accepted, while any larger number of Y’s is rejected.

## Worked Examples

We trace two representative cases.

### Example 1: `NNNY`

| Step | String | Y count | Decision |
| --- | --- | --- | --- |
| 0 | NNNY | 1 | continue |
| final | single Y exists | 1 | YES |

This shows that a single Y never forces interaction with another Y, and all merges can always involve at most one Y per operation.

### Example 2: `YYNY`

| Step | String | Y count | Observation |
| --- | --- | --- | --- |
| 0 | YYNY | 3 | multiple Y’s present |
| final | - | - | impossible to avoid Y-Y interaction |

This case demonstrates that multiple Y regions inevitably collapse into adjacency during any full reduction, forcing a forbidden merge.

The invariant illustrated here is that the number of Y-origin components cannot be kept isolated through a full reduction to length one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | single pass counting Y characters |
| Space | O(1) | only a counter is stored |

The constraints allow up to 500 strings of length 100, so this solution runs in well under a millisecond per test case and easily fits within limits.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        s = input().strip()
        print("YES" if s.count('Y') <= 1 else "NO")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old_stdin
    return out.getvalue().strip()

# provided samples
assert run("""7
YY
NN
NNY
YYYNY
NNNNN
YYYYYY
YNNNNN
""") == """NO
YES
YES
NO
YES
NO
YES"""

# custom cases
assert run("""3
Y
N
YN
""") == """YES
YES
YES"""

assert run("""2
YY
YYY
""") == """NO
NO"""

assert run("""1
NNNNNNNNNN
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Y / N / YN | YES YES YES | single-character and minimal cases |
| YY / YYY | NO NO | multiple Y rejection |
| all N string | YES | all-neutral stability |

## Edge Cases

A single Y in any position always behaves the same because merges with N do not create new Y interactions. For example, in `NYNN`, every valid merge sequence keeps at most one Y active, so the process can always proceed safely down to a single character without ever forming YY adjacency.

A string like `YNNY` exposes the failure mode of naive reasoning based on adjacency only. Even though the Y’s are separated initially, any sequence of merges that reduces length will eventually force interaction between their regions. At that point, two Y-derived components must meet, which would require a forbidden YY merge. This is exactly why counting Y’s is sufficient: separation is not preserved under contraction.
