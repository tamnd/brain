---
title: "CF 104566A - Live Love"
description: "We are given a binary-like sequence, but instead of bits it consists of two labels: PERFECT and NON-PERFECT. The sequence has fixed length n, and exactly m of its positions must be PERFECT while the remaining n - m are NON-PERFECT."
date: "2026-06-30T08:31:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104566
codeforces_index: "A"
codeforces_contest_name: "The 2018 ACM-ICPC Asia Qingdao Regional Contest, Online (The 2nd Universal Cup. Stage 1: Qingdao)"
rating: 0
weight: 104566
solve_time_s: 50
verified: true
draft: false
---

[CF 104566A - Live Love](https://codeforces.com/problemset/problem/104566/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary-like sequence, but instead of bits it consists of two labels: PERFECT and NON-PERFECT. The sequence has fixed length `n`, and exactly `m` of its positions must be PERFECT while the remaining `n - m` are NON-PERFECT.

For any valid arrangement of these labels, we define its score as the length of the longest contiguous block of PERFECTs. In other words, we look at every run of consecutive PERFECT entries and take the maximum length among them.

The task is not to construct one sequence, but to reason about all possible sequences that satisfy the constraints and determine two extremes: the maximum possible longest PERFECT run and the minimum possible longest PERFECT run.

The constraints are small: both `n` and `m` are at most 1000 and there are at most 100 test cases. This immediately suggests that any solution that builds or simulates sequences explicitly is unnecessary. The structure of the problem is purely combinatorial and depends only on how we partition `m` identical items (PERFECTs) into segments separated by NON-PERFECTs.

A naive approach might try to enumerate all placements of `m` PERFECTs among `n` positions, which is `C(n, m)` configurations. Even for `n = 1000`, this is astronomically large and impossible to explore. Another naive idea is to try to greedily place PERFECTs and simulate all distributions, but that still implicitly explores exponential arrangements.

Edge cases appear when `m = 0` or `m = n`. In those cases the sequence is fixed: all NON-PERFECT or all PERFECT respectively. Any solution must immediately recognize these degenerate configurations or risk unnecessary computation or incorrect reasoning about empty runs.

## Approaches

The brute-force viewpoint starts from generating every binary string of length `n` with exactly `m` ones (PERFECTs). For each configuration, we compute the longest consecutive run of ones in `O(n)` time. Since there are `C(n, m)` such configurations, the total complexity is on the order of `O(C(n, m) * n)`, which is far beyond feasible even for small inputs like `n = 1000, m = 500`.

The key observation is that the score depends only on how we split `m` identical items into contiguous groups. NON-PERFECTs act as separators that allow us to break PERFECT runs. So the problem becomes: given `m` identical objects, how large or small can the largest group be if we are allowed to distribute them across segments?

For the maximum score, we want to avoid splitting PERFECTs at all. If we place all `m` PERFECTs consecutively, we obtain a single block of length `m`. This is clearly optimal because any NON-PERFECT inserted inside would split the block and cannot increase the maximum run length.

For the minimum score, we want to spread PERFECTs as evenly as possible so that no contiguous block becomes too large. If we divide `m` items into `n - m + 1` possible slots (gaps between NON-PERFECTs, including ends), we want to distribute them as evenly as possible across these slots. The maximum load of any slot after optimal balancing determines the minimum possible longest consecutive run.

This reduces to a classic load-balancing interpretation: we place `m` indistinguishable balls into `k = n - m + 1` buckets, minimizing the maximum bucket size. The answer is the ceiling of `m / k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n, m) · n) | O(n) | Too slow |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read `n` and `m`. These define how many PERFECT and NON-PERFECT elements we must place.
2. Compute the maximum possible score. Since grouping all PERFECTs together is always valid, the largest contiguous block we can form is simply `m`.
3. Compute the number of available separation slots as `k = n - m + 1`. This corresponds to how many segments of PERFECTs can exist when we interleave NON-PERFECTs optimally. This step captures the idea that every NON-PERFECT can potentially split a block, increasing fragmentation.
4. If `m = 0`, both maximum and minimum scores are `0`, since there are no PERFECTs at all.
5. If `m > 0`, compute the minimum possible maximum block size by distributing `m` items as evenly as possible across `k` slots. The smallest achievable maximum load is `(m + k - 1) // k`.
6. Output the pair `(smax, smin)`.

The key reasoning step is the transformation from sequence arrangement to distribution across slots. Once this mapping is made, the answer becomes a simple arithmetic computation.

### Why it works

Any valid sequence can be seen as alternating blocks of PERFECTs separated by at least one NON-PERFECT, except possibly at the ends. This creates at most `n - m + 1` slots where PERFECT blocks can be placed. The longest contiguous PERFECT run is exactly the largest number of PERFECTs assigned to any single slot. Maximizing or minimizing that maximum reduces to either collapsing everything into one slot or distributing items as evenly as possible. No arrangement outside this model can change the fundamental bound imposed by splitting via NON-PERFECTs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())

        if m == 0:
            print(0, 0)
            continue

        smax = m

        k = n - m + 1
        smin = (m + k - 1) // k

        print(smax, smin)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the derived formulas. The only subtle case is `m = 0`, where the general formula would still work but makes the reasoning less transparent, so it is handled explicitly.

The value `smax = m` comes from the observation that merging all PERFECTs into one contiguous segment never violates constraints. The computation of `k` reflects how many disjoint PERFECT segments can exist if we insert all NON-PERFECTs as separators. The ceiling division computes the tightest possible bound when distributing identical elements evenly.

## Worked Examples

We trace two representative cases.

### Example 1: `n = 5, m = 4`

We have 4 PERFECTs and 1 NON-PERFECT.

| Step | m | k = n-m+1 | smax | smin |
| --- | --- | --- | --- | --- |
| initial | 4 | 2 | - | - |
| compute max | - | - | 4 | - |
| compute min | - | - | 4 | (4+2-1)//2 = 2 |

The maximum arrangement is `PPPPN`, giving a run of 4. The minimum is achieved by splitting the single NON-PERFECT between PERFECTs, such as `PPNPP`, producing runs of length 2.

This confirms that the NON-PERFECT acts as a separator that forces splitting when possible.

### Example 2: `n = 10, m = 3`

| Step | m | k = n-m+1 | smax | smin |
| --- | --- | --- | --- | --- |
| initial | 3 | 8 | - | - |
| compute max | - | - | 3 | - |
| compute min | - | - | 3 | (3+8-1)//8 = 1 |

Here there are enough slots that we can isolate every PERFECT individually, so the minimum longest run becomes 1. The structure allows full separation, which is consistent with distributing sparse items across many gaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test | Only arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

With `T ≤ 100`, this runs instantly. The solution avoids any combinatorial enumeration and reduces the problem to constant-time reasoning per query.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())

        if m == 0:
            out.append("0 0")
            continue

        smax = m
        k = n - m + 1
        smin = (m + k - 1) // k
        out.append(f"{smax} {smin}")

    return "\n".join(out)

# provided samples
assert run("5\n5 4\n100 50\n252 52\n3 0\n10 10\n") == "4 2\n50 1\n52 1\n0 0\n10 10"

# custom cases
assert run("1\n1 0\n") == "0 0"
assert run("1\n1 1\n") == "1 1"
assert run("1\n6 1\n") == "1 1"
assert run("1\n6 5\n") == "5 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 0 0 | empty PERFECT set |
| 1 1 | 1 1 | fully filled sequence |
| 6 1 | 1 1 | single PERFECT behaves trivially |
| 6 5 | 5 3 | non-trivial split distribution |

## Edge Cases

When `m = 0`, there are no PERFECTs at all, so no contiguous segment can exist. The algorithm explicitly returns `0 0`, which matches the definition of an empty maximum.

When `m = n`, all elements are PERFECT. The formula gives `smax = n`, and `k = 1`, so `smin = n`. The algorithm correctly returns a single forced configuration.

When `m = 1`, regardless of `n`, there is only one PERFECT, so both maximum and minimum are 1. The formula produces `(1 + (n - 1 + 1) - 1) // (n - 1 + 1) = 1`, consistent with isolation of a single element.

These cases confirm that the slot-based interpretation remains valid at extreme densities, where either no separation is possible or separation is trivial.
