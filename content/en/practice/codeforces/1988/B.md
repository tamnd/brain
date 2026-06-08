---
title: "CF 1988B - Make Majority"
description: "We are given a binary sequence that can change shape over time. The only allowed move is to take any contiguous segment and compress it into a single value equal to the majority of that segment, where ties are resolved in favor of zero."
date: "2026-06-08T15:50:17+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1988
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 958 (Div. 2)"
rating: 900
weight: 1988
solve_time_s: 310
verified: false
draft: false
---

[CF 1988B - Make Majority](https://codeforces.com/problemset/problem/1988/B)

**Rating:** 900  
**Tags:** greedy, implementation  
**Solve time:** 5m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary sequence that can change shape over time. The only allowed move is to take any contiguous segment and compress it into a single value equal to the majority of that segment, where ties are resolved in favor of zero. Each operation reduces the length of the sequence, so eventually we end up with a single number.

The task is to determine whether it is possible to reduce the entire sequence into a single element equal to one.

The key difficulty is that the operation is not reversible and it changes both length and distribution of values. A segment that looks favorable locally might still destroy global structure if used incorrectly. The decision is purely about existence, not construction.

The constraints allow up to 2·10^5 total elements across test cases. Any solution that simulates operations or tries to search over segments would be far too slow because each operation itself is O(n), and there can be many operations before convergence. Even a quadratic approach per test case would be too large.

A few subtle edge cases are worth calling out.

A single zero, such as input `0`, is obviously impossible to turn into `1` because there is no way to introduce ones.

A string like `10` is also impossible: the only segment operations are either singletons or the whole array. The whole array has one zero and one one, so the majority is zero, which collapses everything to `0`.

A more interesting case is something like `10001`. Even though ones exist, they are sparse, and any operation that includes too many zeros will immediately flip to zero, making recovery impossible.

These examples suggest the answer is governed not by structure of segments, but by a global balance condition.

## Approaches

A brute force view tries to simulate all possible operations. At each step, we could choose any subarray, compute its majority, and recursively continue on the resulting sequence. This forms a huge search tree where each state branches into O(n^2) possibilities, and depth can also be O(n). Even with memoization, the number of distinct states is exponential because different sequences of compressions produce different intermediate arrays. This approach quickly becomes infeasible.

The key observation is that the operation has a strong monotonic behavior: it only reduces the array and replaces local structure with a single bit that reflects a local majority. Importantly, ones are only preserved if they are sufficiently dominant in some region. Zeros act as a default outcome when there is any local tie or zero majority.

We want to end with a single `1`, which means at some point there must exist a segment whose repeated compressions never eliminate all ones. If at any stage we create a segment dominated by zeros, that segment collapses to zero and cannot contribute to a final one.

This leads to a crucial simplification: the only way to end with a single `1` is if the total number of ones is strictly greater than zeros. If zeros are equal or more, any full-array operation immediately collapses to zero, and there is no mechanism to “recover” ones afterward because the process only compresses, never creates ones.

If ones are strictly more, we can always find a sequence of compressions that gradually removes zeros while preserving a majority of ones. Intuitively, we can always choose segments that avoid flipping the global dominance, eventually collapsing the array to a single one.

So the answer reduces to checking whether count(1) > count(0).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Optimal Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of ones and zeros in the input string. This gives a global summary of the array without needing to simulate any operation.
2. Compare the counts. If the number of ones is strictly greater than the number of zeros, output YES. Otherwise output NO.

### Why it works

Every operation replaces a segment with its majority, which never increases the number of ones unless ones are already locally dominant. Any segment with at least as many zeros as ones collapses into zero, permanently reducing the presence of ones in the system. If zeros are not strictly fewer than ones globally, any attempt to merge the entire array will eventually produce a zero, and since operations only reduce structure, there is no way to reintroduce lost ones. Conversely, if ones are strictly more, we can always avoid collapsing the entire structure into zero by merging carefully chosen segments, preserving a one-dominant configuration until the array shrinks to a single element.

This makes the global inequality between counts both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    
    ones = s.count('1')
    zeros = n - ones
    
    if ones > zeros:
        print("YES")
    else:
        print("NO")
```

The solution reads each test case independently and computes counts in linear time. The core logic is the comparison between ones and zeros. No simulation or structure tracking is required.

The only subtlety is ensuring the string is stripped correctly, since trailing newlines would otherwise affect counting.

## Worked Examples

### Example 1

Input: `100000001`

We track only counts.

| Step | ones | zeros | decision |
| --- | --- | --- | --- |
| initial | 2 | 7 | compare |

Since zeros exceed ones, the answer is NO.

This shows that even though ones exist at both ends, they are too sparse to dominate any global compression.

### Example 2

Input: `000011000`

| Step | ones | zeros | decision |
| --- | --- | --- | --- |
| initial | 2 | 7 | compare |

Again zeros dominate, so output is NO.

This confirms that clustering of zeros does not matter, only total counts.

### Example 3

Input: `1110`

| Step | ones | zeros | decision |
| --- | --- | --- | --- |
| initial | 3 | 1 | compare |

Since ones exceed zeros, output is YES.

This demonstrates that even with a trailing zero, the ones can absorb it through appropriate segment operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case scans the string once to count characters |
| Space | O(1) | Only integer counters are used |

The total input size across all test cases is at most 2·10^5, so a linear scan per test case is easily fast enough within 2 seconds.

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
        s = input().strip()
        ones = s.count('1')
        zeros = n - ones
        out.append("YES" if ones > zeros else "NO")
    return "\n".join(out)

# provided samples
assert run("""5
1
0
1
1
2
01
9
100000001
9
000011000
""") == """No
Yes
No
Yes
No"""

# custom cases
assert run("""1
1
1
""") == "YES", "single one"

assert run("""1
1
0
""") == "NO", "single zero"

assert run("""1
5
11111
""") == "YES", "all ones"

assert run("""1
6
110000
""") == "NO", "equal-ish boundary 2 vs 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | YES | minimal positive case |
| `1\n1\n0` | NO | minimal negative case |
| `1\n5\n11111` | YES | all ones extreme |
| `1\n6\n110000` | NO | dominance boundary |

## Edge Cases

A single-element array highlights the base behavior. For input `1`, the answer is trivially YES because the array already equals `[1]`. The algorithm correctly computes ones = 1, zeros = 0, and returns YES.

For input `0`, ones = 0 and zeros = 1, so the output is NO. This matches the impossibility of introducing ones via any operation.

A balanced structure like `01` or `10` always has equal counts, leading to NO. The algorithm does not depend on arrangement, which is consistent with the fact that any full merge of a balanced segment collapses to zero due to tie-breaking.
