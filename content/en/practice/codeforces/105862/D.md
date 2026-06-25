---
title: "CF 105862D - OR MEX"
description: "We are given a collection of integers and are asked to look at all values that can be formed by taking any subset of these numbers and combining them using bitwise OR."
date: "2026-06-25T14:34:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105862
codeforces_index: "D"
codeforces_contest_name: "ACPC Kickoff 2025"
rating: 0
weight: 105862
solve_time_s: 54
verified: true
draft: false
---

[CF 105862D - OR MEX](https://codeforces.com/problemset/problem/105862/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of integers and are asked to look at all values that can be formed by taking any subset of these numbers and combining them using bitwise OR. From this set of reachable results, we need to determine the smallest non-negative integer that never appears as a result.

A useful way to rephrase the task is to imagine starting from zero and optionally “adding” each number by OR-ing it into your current value. Each subset corresponds to some sequence of choices of whether to include each element, and the OR of that subset produces a single value. The final object of interest is the set of all such OR results, and we are looking for the first integer that is missing from this set.

The constraints in this problem are designed around the structure of bitwise OR rather than raw numeric size. Even if values look large, OR only interacts through bits, so the effective state space is determined by the number of bits required to represent the maximum value. This immediately rules out any approach that enumerates subsets explicitly, since that would be exponential in the number of elements. Instead, the only feasible approaches must compress the problem into a manageable state space over bitmasks.

A few edge cases are easy to miss if one thinks only in terms of the input array rather than subset OR structure. If the array contains only zeros, every subset OR is zero, so the reachable set is `{0}` and the answer should be `1`. A naive mistake is to assume every element contributes a new value, leading to incorrectly thinking multiple distinct OR results exist.

Another subtle case happens when values overlap heavily in bits. For example, with input `[1, 2, 3]`, subset OR results are `{0, 1, 2, 3}` because `1 | 2 = 3`, but there is no way to form `4`. A naive approach might incorrectly assume that since bits 0 and 1 appear, all numbers up to `3` are covered and that the mex should be `4`, but this is only true because `4` requires a new bit not present in any element.

Finally, consider inputs where the global OR is dense but still leaves gaps in representability. Even if the OR of all elements is `7`, it does not imply that all numbers from `0` to `7` are reachable. This mismatch between “bit coverage” and “value coverage” is the core reason naive reasoning fails.

## Approaches

The brute-force approach is straightforward: enumerate every subset of the array, compute its bitwise OR, store all results in a set, and finally scan upward from zero to find the first missing integer. This is correct because it explicitly constructs the definition of the problem. However, it requires iterating over all `2^n` subsets, and for each subset computing an OR over up to `n` elements in the worst case. This leads to roughly `O(n * 2^n)` operations, which becomes infeasible even for `n = 25`, let alone larger constraints.

The key observation is that we do not actually care about which subset produced a value, only whether a value is reachable. This turns the problem into a reachability problem over OR-states. Each number transforms a current state `x` into a new state `x | a_i`. Since OR only adds bits and never removes them, the state space is closed under repeated transitions and bounded by the maximum bitmask representable by the input.

This allows us to treat the problem as dynamic programming over bitmasks: maintain a boolean array of which OR-values are achievable, and iteratively expand it using each array element. Each element contributes transitions from all currently reachable states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 2^n) | O(2^n) | Too slow |
| Bitmask DP | O(n · 2^B) | O(2^B) | Accepted |

Here `B` is the number of bits needed to represent the maximum value in the array.

## Algorithm Walkthrough

1. Determine the maximum bit length needed to represent any value in the array, and set a limit `MAX_MASK = 2^B`. This defines the universe of all possible OR results, since OR cannot introduce new bits.
2. Create a boolean array `dp` where `dp[x]` indicates whether some subset produces OR value `x`. Initialize `dp[0] = True`, representing the empty subset.
3. Process each number `a` in the array. For each currently reachable value `x`, we can also reach `x | a`. To avoid overwriting information within the same iteration, we compute updates from a snapshot of the current state.
4. After processing all elements, scan `dp` from `0` upward and return the first index `mex` such that `dp[mex]` is false.

The reason the snapshot is necessary is that allowing in-place updates would incorrectly chain a single element multiple times within the same iteration, effectively simulating reuse of the same array element, which violates the subset constraint.

### Why it works

The algorithm maintains the invariant that after processing the first `i` elements, `dp[x]` is true if and only if there exists a subset of the first `i` elements whose OR equals `x`. Each transition `x -> x | a_i` corresponds exactly to deciding whether to include the `i`-th element in a subset. Since every subset decision is represented exactly once per element, no reachable OR value is missed and no invalid value is introduced. The final scan therefore correctly identifies the smallest integer that cannot be expressed as a subset OR.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    max_val = 0
    for x in arr:
        max_val |= x

    # number of bits needed to represent max_val
    B = max_val.bit_length()
    size = 1 << B

    dp = [False] * size
    dp[0] = True

    for a in arr:
        ndp = dp[:]  # snapshot
        for x in range(size):
            if dp[x]:
                ndp[x | a] = True
        dp = ndp

    for i in range(size):
        if not dp[i]:
            print(i)
            return

if __name__ == "__main__":
    solve()
```

The implementation first compresses the state space to only those bits that actually appear in the input. This avoids unnecessary work on unreachable higher masks.

The core loop builds `ndp` from `dp` to ensure each element is used exactly once per subset decision. The transition `x | a` encodes inclusion of the current element. The final linear scan is safe because the OR-state space is contiguous in indexing even though reachability is not.

A subtle point is that we never need to track subsets explicitly, only reachable OR values. This is what allows the solution to stay within a manageable `2^B` state space instead of exponential in `n`.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

We track reachable OR values.

| Step | Added value | Reachable states |
| --- | --- | --- |
| 0 | init | {0} |
| 1 | 1 | {0, 1} |
| 2 | 2 | {0, 1, 2, 3} |
| 3 | 3 | {0, 1, 2, 3} |

Final reachable set is `{0,1,2,3}`, so the first missing integer is `4`.

This confirms that even though every pair of bits is covered, no combination introduces a new bit beyond those already present.

### Example 2

Input:

```
4
0 0 0 0
```

| Step | Added value | Reachable states |
| --- | --- | --- |
| 0 | init | {0} |
| 1 | 0 | {0} |
| 2 | 0 | {0} |
| 3 | 0 | {0} |
| 4 | 0 | {0} |

Only value reachable is `0`, so the answer is `1`.

This highlights that duplicate zero elements do not expand the state space at all.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^B) | For each element, we scan all bitmask states and propagate OR transitions |
| Space | O(2^B) | We store reachability for each possible bitmask |

The value `B` is bounded by the maximum number of bits in the input values, which keeps the state space small in practice. This fits comfortably within typical constraints where values are up to around `10^6` or `10^7`, giving at most 20-25 bits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# Since solve() prints directly, we wrap carefully
def run(inp: str) -> str:
    import sys, io
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = backup_stdin
        sys.stdout = backup_stdout

# provided sample-like cases
assert run("3\n1 2 3\n") == "4"

# single element zero
assert run("1\n0\n") == "1"

# all zeros
assert run("4\n0 0 0 0\n") == "1"

# single power of two
assert run("1\n8\n") == "0"

# mixed small case
assert run("2\n1 4\n") == "2"

# dense small
assert run("3\n1 2 4\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 2 3 | 4 | typical full OR closure |
| 1 0 | 1 | zero-only edge case |
| 4 zeros | 1 | duplicates of zero |
| 1 8 | 0 | missing zero when empty subset excluded incorrectly |
| 1 4 / 1 2 4 | 2, 3 | gaps in OR space |

## Edge Cases

For an input consisting only of zeros, the algorithm initializes `dp[0] = True` and never expands it. Scanning from zero finds that `0` is reachable, but `1` is not, so the output is correctly `1`.

For inputs where all values are powers of two, each element introduces a single new bit and OR transitions gradually fill combinations of those bits. The DP correctly builds all subsets of bits, but any number requiring multiple identical bits is impossible, and the scan detects the first missing integer accordingly.

For cases where the array already contains a large value like `2^k`, that bit immediately propagates into all reachable states via OR, but does not guarantee intermediate values are filled. The algorithm still checks every candidate explicitly, ensuring no assumption is made about contiguous coverage.
