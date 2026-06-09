---
title: "CF 1791C - Prepend and Append"
description: "We are given a binary string that is the final result of repeatedly applying a very specific operation. Each operation takes the current string and expands it by adding one character to the left end and one character to the right end, with the constraint that the two added…"
date: "2026-06-09T10:28:47+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1791
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 849 (Div. 4)"
rating: 800
weight: 1791
solve_time_s: 75
verified: true
draft: false
---

[CF 1791C - Prepend and Append](https://codeforces.com/problemset/problem/1791/C)

**Rating:** 800  
**Tags:** implementation, two pointers  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string that is the final result of repeatedly applying a very specific operation. Each operation takes the current string and expands it by adding one character to the left end and one character to the right end, with the constraint that the two added characters are always different. One end receives a `0`, the other end receives a `1`, but we are free to choose which side gets which.

The task is to reverse this process in a compressed sense. Instead of reconstructing all possible histories, we only need to determine the minimum possible length of the string before any operations were applied.

The key observation is that every operation only adds symbols at the boundaries, so the middle part of the string is never modified internally. This immediately suggests that the original string corresponds to what remains after peeling off symmetric “outer pairs” that could have been added during the process.

The constraints are small: up to 100 test cases and total length up to 2000 per test. This rules out any exponential reconstruction of all possible histories, but still allows linear or near-linear scanning per test case. An $O(n^2)$ solution would still pass comfortably, but the intended solution is linear.

A naive but tempting idea is to simulate reversing operations by guessing which characters came from which operation. This quickly becomes ambiguous because each operation can be undone in two ways. That leads to exponential branching.

Edge cases that matter:

A string like `"1"` has no valid reduction, so the answer is 1 because no operation could have produced a single character without starting from length 1.

A string like `"10"` can be fully reduced to empty, because it could be the result of one operation starting from empty.

A string like `"10101"` cannot be reduced at all, because the outer structure never matches a removable pair pattern.

These examples hint that we are really looking for how much of the string can be “canceled” from both ends under a pairing rule.

## Approaches

The brute-force view tries to reconstruct the original string by simulating reverse operations. From a final string, we would try to guess whether the last operation removed a `0` from the left and a `1` from the right or vice versa. Each choice produces a smaller string, and we recurse.

This works in principle because every valid history corresponds to some sequence of such reversals. However, the branching factor is 2 at every step, and in the worst case the depth is $O(n)$, leading to $O(2^n)$ possibilities. Even with memoization, the number of distinct states is still exponential in worst cases because different removal patterns produce different substrings.

The key insight is that we do not need to reconstruct the process. Every operation effectively pairs one `0` with one `1`, one from each side, and removes them from the boundary. So the process continues as long as the leftmost remaining character and rightmost remaining character are different. Once they match, no further valid reverse operation can explain them as boundary additions simultaneously.

This reduces the problem to a two-pointer shrinking process: repeatedly remove matching-opposite boundary pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We simulate the idea of reversing the construction by shrinking the string from both ends.

1. Initialize two pointers, one at the start and one at the end of the string. These represent the current remaining segment that could still be the original string after undoing operations.
2. While the left pointer is strictly to the left of the right pointer, check the characters at both ends.
3. If the two characters are different, we can interpret them as the last operation that placed these two characters at opposite ends. We remove both by moving the left pointer rightward and the right pointer leftward.
4. If the two characters are the same, we cannot pair them in a valid operation reversal, so we stop immediately. Any inner structure cannot be resolved further into valid boundary operations.
5. When the loop stops, the remaining segment between the pointers is the shortest possible original string, so its length is the answer.

The subtle point is that only mismatched ends can be “explained away” by an operation. Matching ends are frozen because no operation ever produces two identical characters at both ends simultaneously.

### Why it works

Each operation adds two opposite bits at the boundaries. Reversing an operation is only possible when the current outermost characters could have been exactly those two added bits. That means they must differ. As long as the ends differ, we can safely peel them off in pairs, preserving the existence of some valid construction history. Once the ends match, no sequence of operations could have created that configuration by repeatedly adding opposite bits, so any remaining substring must be part of the original string.

This invariant ensures that every removal corresponds to a valid inverse operation and that stopping occurs exactly when no further inverse operation is possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    l, r = 0, n - 1

    while l < r and s[l] != s[r]:
        l += 1
        r -= 1

    print(r - l + 1)
```

The solution relies on a simple two-pointer scan. The loop condition ensures we only shrink when the ends differ, which corresponds exactly to a valid reverse operation. Once we hit equal endpoints or pointers cross, we stop and measure the remaining substring.

The key implementation detail is that we never actually modify the string. We only move indices, which keeps the solution linear and avoids unnecessary allocations.

## Worked Examples

### Example 1: `100`

We track how the pointers evolve.

| Step | l | r | s[l] | s[r] | Action |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 1 | 0 | shrink |
| 1 | 1 | 1 | - | - | stop |

At step 0, the ends differ, so we remove both ends. After that, only `"0"` remains, and we stop.

This confirms that only one character could have been originally present.

### Example 2: `1010110`

| Step | l | r | s[l] | s[r] | Action |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 6 | 1 | 0 | shrink |
| 1 | 1 | 5 | 0 | 1 | shrink |
| 2 | 2 | 4 | 1 | 1 | stop |

After two valid cancellations, we reach equal endpoints, so no further reverse operation is possible. The remaining substring is `"101"`, which has length 3.

This demonstrates how the process halts precisely when symmetry no longer matches the allowed operation structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each pointer moves at most $n$ steps total, shrinking from both ends |
| Space | $O(1)$ | Only two indices are stored, no extra data structures |

The total length across test cases is small enough that a single linear scan per test case fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        l, r = 0, n - 1
        while l < r and s[l] != s[r]:
            l += 1
            r -= 1
        out.append(str(r - l + 1))

    return "\n".join(out)

# provided samples
assert run("""9
3
100
4
0111
5
10101
6
101010
7
1010110
1
1
2
10
2
11
10
1011011010
""") == """1
2
5
0
3
1
0
2
4"""

# minimum size
assert run("""2
1
0
1
1
""") == """1
1"""

# empty-like reduction
assert run("""1
2
10
""") == """0"""

# already irreducible pattern
assert run("""1
5
10101
""") == """5"""

# fully reducible alternating
assert run("""1
6
101010
""") == """0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single chars | 1 | base case with no reduction |
| "10" | 0 | full cancellation to empty string |
| "10101" | 5 | no valid reductions possible |
| "101010" | 0 | maximal alternating cancellation |

## Edge Cases

A single-character string such as `"0"` or `"1"` never enters the shrinking loop because `l < r` is false immediately. The algorithm returns length 1, matching the fact that no operation sequence can reduce it further.

For `"10"`, the pointers start at opposite ends with differing characters, so both are removed, leaving an empty interval where `l > r`. The computed length becomes 0, which corresponds to the empty initial string.

For `"10101"`, the first and last characters match (`1` and `1`), so the loop stops immediately. The algorithm correctly concludes that no boundary removal is possible, and the full string must have been the original.
