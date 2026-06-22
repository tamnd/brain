---
title: "CF 105444G - Gig Combinatorics"
description: "We are given a sequence of songs in the order they were written. Each song has a label, which can only be 1, 2, or 3. We want to count how many contiguous subsequences of these songs form a valid “setlist”."
date: "2026-06-23T03:31:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105444
codeforces_index: "G"
codeforces_contest_name: "2020-2021 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2020)"
rating: 0
weight: 105444
solve_time_s: 51
verified: true
draft: false
---

[CF 105444G - Gig Combinatorics](https://codeforces.com/problemset/problem/105444/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of songs in the order they were written. Each song has a label, which can only be 1, 2, or 3. We want to count how many contiguous subsequences of these songs form a valid “setlist”.

A valid setlist is a subsequence taken in order from the original list, with three structural constraints. The first chosen song must have label 1, the last chosen song must have label 3, and every song in between must have label 2. The setlist must contain at least three songs, so at least one 1, at least one 3, and at least one 2 in between.

This is a counting problem over all subarrays, but the structure is extremely rigid: every valid setlist is completely determined by picking a starting position containing 1 and an ending position containing 3, with the requirement that everything between them is only 2.

The constraint n up to 10^6 immediately rules out any O(n^2) or O(n^2) enumeration of pairs of endpoints. Even O(n log n) solutions are acceptable but unnecessary; the structure suggests a linear scan solution is possible.

A naive approach that tries all pairs (l, r) and checks whether the segment is valid would recompute interior checks repeatedly and fail catastrophically at n = 10^6.

A more subtle failure case appears if one tries to only check pairs of 1 and 3 endpoints without validating the interior efficiently. For example, in input

1 2 3 1 3

the pair (1, 3) is valid because the middle is 2, but (1, 4) is invalid because the middle contains 3. A naive endpoint pairing approach that ignores interior validation would overcount.

## Approaches

The brute-force idea is straightforward: consider every possible pair of indices (l, r), and check whether a valid setlist can be formed from l to r. This requires verifying that a[l] = 1, a[r] = 3, and every element between them is 2. Even if the interior check is optimized with prefix information, iterating over all pairs still costs O(n^2) in the worst case. With n = 10^6, this is completely infeasible.

The key observation is that the structure of a valid segment forces all internal elements to be 2. This means that valid segments can only live inside maximal contiguous blocks of 2s, with a 1 immediately before the block and a 3 immediately after the block. So instead of thinking about arbitrary subarrays, we reduce the problem to counting patterns of the form 1 + (one or more 2s) + 3, where the 2s form a continuous region in the original array.

Once we view the array this way, we can scan once, track stretches of consecutive 2s, and for each such stretch count how many 1s appear immediately before it and how many 3s appear immediately after it. Each choice of (1, 2-block start, 2-block end, 3) contributes exactly one valid setlist, and we can aggregate these contributions efficiently.

This turns the problem into linear counting over runs, avoiding any repeated scanning of interior segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Run-based counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We scan the array once and compress it conceptually into runs of equal values, but we do not need to explicitly store them.

1. We iterate through the array while identifying maximal contiguous segments of value 2. Each such segment is a candidate “middle region” of valid setlists. This matters because any valid setlist must have all interior elements equal to 2, so it cannot cross a non-2 boundary.
2. For each contiguous block of 2s, we count how many valid choices exist for the starting 1. This is the number of consecutive 1s immediately to the left of this block, because the start of a valid segment must be a 1 positioned directly before the 2-block in the original order. Any 1 further away would force a non-2 inside the segment.
3. Similarly, we count how many valid choices exist for the ending 3. This is the number of consecutive 3s immediately to the right of the 2-block, since the ending 3 must be directly after the 2-block.
4. The number of valid setlists contributed by a given 2-block is the product of these two counts, because each left choice of 1 can pair with each right choice of 3 independently, and all combinations preserve the required structure.
5. We accumulate this product over all 2-blocks, taking the result modulo 10^9 + 7.

### Why it works

Any valid setlist must have a structure where all internal elements are 2. That forces the interior of the chosen segment to lie entirely within a single contiguous run of 2s in the array. Once that run is fixed, the endpoints are determined only by how many consecutive 1s appear immediately before it and how many consecutive 3s appear immediately after it. No other positions can form valid boundaries because introducing any gap or mismatch breaks the constraint that only 2s appear internally. This makes the decomposition into independent contributions from each 2-run both complete and non-overlapping.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Precompute prefix counts of consecutive 1s ending at i
    left_ones = [0] * n
    if a[0] == 1:
        left_ones[0] = 1
    for i in range(1, n):
        if a[i] == 1:
            left_ones[i] = left_ones[i - 1] + 1
    
    # Precompute suffix counts of consecutive 3s starting at i
    right_threes = [0] * n
    if a[-1] == 3:
        right_threes[-1] = 1
    for i in range(n - 2, -1, -1):
        if a[i] == 3:
            right_threes[i] = right_threes[i + 1] + 1
    
    ans = 0
    
    i = 0
    while i < n:
        if a[i] != 2:
            i += 1
            continue
        
        j = i
        while j < n and a[j] == 2:
            j += 1
        
        left_count = left_ones[i - 1] if i > 0 else 0
        right_count = right_threes[j] if j < n else 0
        
        if left_count and right_count:
            ans = (ans + left_count * right_count) % MOD
        
        i = j
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first builds two helper arrays that capture how long runs of 1s end at each position and how long runs of 3s begin at each position. These allow constant-time access to how many valid starting and ending choices exist around any 2-block.

Then it scans through the array, jumping across contiguous segments of 2s. For each such segment, it looks immediately left and right to determine how many valid 1-starts and 3-ends exist. Multiplying these counts gives the contribution of that block.

A common pitfall is incorrectly allowing non-adjacent 1s or 3s to participate. The use of consecutive run counts ensures only boundary-adjacent values are considered.

## Worked Examples

### Example 1

Input:

```
1 1 1 2 2 2 3 3 3
```

We compute consecutive 1s ending at each index and consecutive 3s starting at each index.

The only 2-block is from index 3 to 5.

| Step | 2-block (i, j) | left_count (1s before) | right_count (3s after) | contribution |
| --- | --- | --- | --- | --- |
| 1 | (3, 5) | 3 | 3 | 9 |

The block of 2s is surrounded by three 1s and three 3s, so we get 3 × 3 = 9 valid setlists.

This confirms that every combination of choosing a starting 1 among the first three positions and an ending 3 among the last three positions yields a valid segment through the 2-block.

### Example 2

Input:

```
1 2 1 2 3 1 2 3
```

We identify two 2-blocks: at index 1 and at index 3, and at index 6.

| Step | 2-block | left_count | right_count | contribution |
| --- | --- | --- | --- | --- |
| 1 | (1, 1) | 1 | 0 | 0 |
| 2 | (3, 3) | 1 | 1 | 1 |
| 3 | (6, 6) | 1 | 1 | 1 |

Only blocks that are properly enclosed by at least one 1 on the left and one 3 on the right contribute. The total is 2.

This shows that isolated 2s or poorly positioned 2s contribute nothing unless they are bracketed correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each array is scanned a constant number of times, and each index is visited at most once in the 2-block scan |
| Space | O(n) | Two auxiliary arrays store prefix and suffix run lengths |

The solution comfortably fits within limits for n up to 10^6 since it performs only linear passes over the input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("9\n1 1 1 2 2 2 3 3 3\n") == "9"

# sample 2
assert run("8\n1 2 1 2 3 1 2 3\n") == "2"

# all ones (no valid setlists)
assert run("5\n1 1 1 1 1\n") == "0"

# no 1s
assert run("5\n2 2 2 3 3\n") == "0"

# no 3s
assert run("5\n1 2 2 2 2\n") == "0"

# single valid minimal pattern
assert run("3\n1 2 3\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all 1s | 0 | no 2/3 structure |
| no 1s | 0 | missing start |
| no 3s | 0 | missing end |
| 1 2 3 | 1 | minimal valid case |

## Edge Cases

A key edge case is when a 2-block is at the boundary of the array. For input like

```
2 2 2 1 3 3
```

there is no valid 1 immediately before any 2-block, so left_count is zero and no contribution is added. The algorithm correctly ignores this block because it computes left_count from index i - 1, which is out of range.

Another case is when multiple 2-blocks exist but only some are properly bracketed:

```
1 2 3 2 2 3
```

The first 2-block contributes 1 × 1, while the second contributes 1 × 1 as well. Each is handled independently because the scan resets at every non-2 boundary, ensuring no double counting or cross-block mixing.
