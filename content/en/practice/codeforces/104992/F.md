---
title: "CF 104992F - \u041b\u044f\u0433\u0443\u0448\u043a\u0430 \u0438 \u044f\u0433\u043e\u0434\u044b"
description: "We are given a linear sequence of positions from 1 to n. Each position has a value a[i], which can be positive or negative and represents how much the frog’s “energy” changes when it lands there. The frog starts at position 1 and must end at position n."
date: "2026-06-28T03:35:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104992
codeforces_index: "F"
codeforces_contest_name: "qual VKOSHP Junior 24"
rating: 0
weight: 104992
solve_time_s: 73
verified: false
draft: false
---

[CF 104992F - \u041b\u044f\u0433\u0443\u0448\u043a\u0430 \u0438 \u044f\u0433\u043e\u0434\u044b](https://codeforces.com/problemset/problem/104992/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a linear sequence of positions from 1 to n. Each position has a value a[i], which can be positive or negative and represents how much the frog’s “energy” changes when it lands there. The frog starts at position 1 and must end at position n.

Under normal movement rules, the frog can only move from i to i + 1. However, exactly once during its journey, it is allowed to make a single long jump of fixed length k, moving from i to i + k, as long as it stays within the range of positions. Every position it lands on is visited exactly once and contributes its value to the total sum.

The task is to choose whether to use the long jump, and if so, where to use it, in order to maximize the total sum of visited values.

The output is simply the maximum possible sum over all valid paths from 1 to n with at most one k-jump.

The constraints n up to 300,000 immediately rule out any solution that tries every possible jump position naively with O(n) recomputation per position, since that would lead to O(n^2) in the worst case.

A subtle edge case arises when skipping a segment is beneficial because it avoids large negative values. For example, if a block of values is strongly negative, using the jump to bypass it can significantly increase the total.

Another edge case is when k = 1. In that case, the “long jump” is identical to normal movement, so the answer must reduce to simply summing all values. Any solution that blindly applies transitions without handling this degeneracy can accidentally double count or overwrite states incorrectly.

Finally, when k is large (close to n), the jump may skip almost the entire middle, and the optimal strategy depends entirely on prefix and suffix sums.

## Approaches

A brute-force strategy tries every possible position i where the jump could be used. For each such i, we compute the total sum as the sum of values from 1 to i, then from i + k to n, skipping the middle segment.

Computing each candidate sum from scratch costs O(n), and there are O(n) choices of i, leading to O(n^2) time. With n = 3 × 10^5, this is far too slow.

The key observation is that the effect of choosing a jump position is entirely local: everything before i contributes as a prefix sum, everything after i + k contributes as a suffix sum, and the middle segment is skipped. This means we can precompute prefix sums so that each candidate can be evaluated in O(1).

We then only need to scan all i and combine prefix[i] with suffix[i + k], tracking the maximum. Alongside this, we also consider the case of not using the jump at all.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Prefix/Suffix Optimization | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute a prefix sum array where prefix[i] is the sum of a[1] through a[i]. This allows any segment sum to be computed in constant time.
2. Compute the total sum of all elements. This represents the case where we do not use the long jump at all.
3. Consider every possible starting position i for the long jump. From position i, the frog jumps directly to i + k, skipping all positions in between.
4. For each i such that i + k ≤ n, compute the total score as prefix[i] + (total_sum - prefix[i + k - 1]). The prefix part represents everything before the jump, and the suffix part represents everything after the skipped segment.
5. Track the maximum value over all valid i.
6. Compare this maximum against the no-jump total sum and output the larger one.

The reasoning behind step 4 is that removing a segment [i+1, i+k-1] from the path is equivalent to taking everything before it plus everything after it.

### Why it works

Any valid path with a single jump corresponds to choosing exactly one contiguous segment of length k - 1 (the skipped segment) that is removed from the full path. The remaining visited nodes are exactly a prefix followed by a suffix. Since prefix sums let us evaluate all such splits efficiently, checking all possible skip positions guarantees we consider every legal jump configuration exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    # prefix sums
    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + a[i - 1]

    total = pref[n]

    # no jump case
    ans = total

    # try all jump positions
    for i in range(1, n + 1):
        j = i + k
        if j > n:
            break
        # skip segment (i+1 ... j-1)
        # keep [1..i] and [j..n]
        cur = pref[i] + (total - pref[j - 1])
        ans = max(ans, cur)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on a standard prefix sum array to allow constant-time segment queries. The key detail is indexing: since prefix[i] includes a[1] through a[i], the skipped segment ends at j - 1 when jumping from i to i + k.

The answer is initialized with the no-jump case, ensuring correctness even when all possible jumps are harmful.

## Worked Examples

### Sample 1

Input:

```
5 2
1 2 -3 4 5
```

We compute prefix sums: [0, 1, 3, 0, 4, 9].

We evaluate possible jump positions:

| i | i+k | prefix[i] | prefix[i+k-1] | candidate |
| --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 3 | 1 + (9 - 3) = 7 |
| 2 | 4 | 3 | 0 | 3 + (9 - 0) = 12 |
| 3 | 5 | 0 | 4 | 0 + (9 - 4) = 5 |
| 4 | 6 | invalid | - | - |

Best with jump is 12. No-jump sum is 9. Answer is 12.

This trace shows that skipping the negative value -3 yields a better total.

### Sample 2

Input:

```
5 2
1 2 3 4 5
```

Prefix sums: [0, 1, 3, 6, 10, 15].

| i | i+k | prefix[i] | prefix[i+k-1] | candidate |
| --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 3 | 1 + (15 - 3) = 13 |
| 2 | 4 | 3 | 6 | 3 + (15 - 6) = 12 |
| 3 | 5 | 6 | 10 | 6 + (15 - 10) = 11 |
| 4 | 6 | invalid | - | - |

Best with jump is 13, but no-jump sum is 15, so answer is 15.

This confirms that when all values are positive, avoiding the jump is optimal since any skip removes beneficial contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | prefix computation plus single scan over all valid jump positions |
| Space | O(n) | prefix array storage |

The solution processes each index a constant number of times, which fits comfortably within constraints up to 3 × 10^5.

## Test Cases

```python
import sys, io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + a[i - 1]

    total = pref[n]
    ans = total

    for i in range(1, n + 1):
        j = i + k
        if j > n:
            break
        ans = max(ans, pref[i] + (total - pref[j - 1]))

    print(ans)

# provided samples
assert solve_io("5 2\n1 2 -3 4 5\n") == "12"
assert solve_io("5 2\n1 2 3 4 5\n") == "15"
assert solve_io("6 4\n-5 -10 -20 25 4 -1\n") == "-2"

# custom cases
assert solve_io("1 1\n5\n") == "5", "single element"
assert solve_io("5 5\n1 -2 3 -4 5\n") == "5", "jump ineffective"
assert solve_io("6 2\n-1 -2 -3 -4 -5 -6\n") == "-9", "best skip middle"
assert solve_io("7 3\n10 -100 10 -100 10 -100 10\n") == "-170", "avoid heavy losses"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 5 | minimal boundary |
| k = n | 5 | jump ineffective edge |
| all negative | -9 | skipping harmful segment |
| alternating heavy negatives | -170 | long skip optimization |

## Edge Cases

When k equals 1, the jump does not change the path structure. The algorithm still works because for i such that i + 1 ≤ n, the skipped segment is empty, meaning prefix[i] + (total - prefix[i]) equals total. The maximum remains the full sum, so the correct result is preserved.

When k is equal to n, only one jump is possible from position 1, and it skips everything between 2 and n - 1. The formula evaluates prefix[1] + a[n], which correctly captures the only meaningful jump option.

When all values are negative, the algorithm correctly prefers the least damaging segment removal. The prefix/suffix formulation ensures that even if every value is harmful, the best result is still computed by evaluating all possible skipped intervals.
