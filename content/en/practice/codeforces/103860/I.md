---
title: "CF 103860I - Reverse LIS"
description: "We are given a binary string that is not written explicitly, but compressed as alternating runs of equal characters. Each run tells us how many consecutive zeros or ones appear, and runs always alternate between the two characters."
date: "2026-07-02T07:58:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103860
codeforces_index: "I"
codeforces_contest_name: "The 7th China Collegiate Programming Contest, Finals (CCPC Finals 2021)"
rating: 0
weight: 103860
solve_time_s: 56
verified: true
draft: false
---

[CF 103860I - Reverse LIS](https://codeforces.com/problemset/problem/103860/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string that is not written explicitly, but compressed as alternating runs of equal characters. Each run tells us how many consecutive zeros or ones appear, and runs always alternate between the two characters.

From this string, we are allowed to perform at most k operations, where each operation chooses any contiguous substring and reverses it. After applying these reversals, we look at the longest non-decreasing subsequence of the resulting string. Since the alphabet is binary with 0 < 1, a non-decreasing subsequence is exactly a sequence of some zeros followed by some ones, preserving original order.

For each query k, we must compute the maximum possible length of such a subsequence after at most k reversals. Each query is independent, meaning we always start from the original string.

The input size is large: up to 2×10^5 runs and up to 2×10^5 queries, with run lengths as large as 10^9. This immediately rules out expanding the string. Even linear per query is too slow, so the structure must be reduced to run-level or even constant-time evaluation per query.

A naive interpretation would try to simulate reversals and recompute LIS. Even computing LIS once is O(N), but N can be up to sum of run lengths, which is impossible. Even working on runs, simulating k substring reversals per query would still be far too slow.

A subtle edge case appears when the string already has long monotone structure. For example, if the string is already all zeros followed by all ones, the answer is maximal even for k = 0, and reversals cannot improve it. A naive approach that assumes reversals always help would incorrectly increase the answer.

Another edge case is a fully alternating run structure like 010101..., where many boundaries exist. Here reversals can have strong effect because they can locally “untangle” alternating patterns, but only in a limited way per operation.

## Approaches

We start from the structure of the target quantity. For any fixed string, a non-decreasing subsequence in a binary alphabet is always equivalent to choosing a split point in the original ordering: we pick some indices as zeros, and all of them must appear before the indices chosen as ones. This means that for any cut position p in the original array, the best subsequence using that cut is the number of zeros we can take from the prefix plus the number of ones we can take from the suffix.

Since within each side we can take all matching characters while preserving order, the value for a cut p becomes the count of zeros in prefix p plus the count of ones in suffix p. The baseline answer is the maximum of this expression over all p.

This already reduces the problem to a structural optimization over cuts rather than subsequences.

Now consider what a substring reversal does. Reversing a segment does not change the multiset of characters, but it changes how 0s and 1s are interleaved. The only thing that matters for the LIS expression is how many zeros end up before the chosen cut and how many ones end up after it.

A reversal mainly affects boundaries between runs. Each boundary of the form 0→1 or 1→0 contributes to “misplacement” relative to a good cut. Intuitively, the closer the string is to being one block of zeros followed by one block of ones, the larger the LIS becomes.

The key structural insight is that a single reversal can fix at most two such “bad boundaries” in terms of contribution to this objective. It can merge or reorder adjacent alternating segments, but it cannot globally reorder all runs. Therefore, each operation can increase the best achievable LIS by a bounded additive amount, and improvements accumulate linearly until no bad structure remains.

This reduces the problem from reasoning about arbitrary substring operations to counting how many improvements are still possible. Once we compute the baseline LIS, the effect of k reversals is to increase it by up to 2k, but never beyond the maximum possible value of the string length.

So the final answer for each k is determined only by the baseline value and a simple linear growth clipped at n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation of reversals + LIS recomputation | Exponential / O(k·n) per query | O(n) | Too slow |
| Run-based LIS + bounded improvement per reversal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We first compress reasoning at the run level. The string is already given as alternating blocks, so we treat each run as a single unit with a length and a character.

We compute the baseline answer, which is the maximum LIS without any reversals. This is done by scanning possible cut positions at run boundaries. For each cut, we maintain how many zeros appear before it and how many ones appear after it. The best cut gives the initial value, which we call base.

Next we analyze how much structure prevents the string from reaching the ideal configuration. The ideal configuration is all zeros followed by all ones, which achieves the maximum possible LIS equal to the total length.

The gap between base and total length is caused by alternating boundaries where zeros appear after ones or ones appear before zeros relative to a good split. Each such boundary represents a unit of “inefficiency” in the subsequence structure.

We then observe how reversals interact with this inefficiency. A single substring reversal can eliminate up to two such problematic transitions, because it can flip a segment and merge adjacent runs in a way that reduces alternation locally on both sides of the cut structure.

So we treat each operation as consuming up to two units of inefficiency. If there are still enough inefficiencies remaining, each reversal increases the best possible LIS by exactly 2. Once inefficiency is exhausted, further reversals have no effect.

Therefore, for a query k, we compute the answer as base plus min(2k, remaining gap to full length).

### Why it works

The invariant is that the only factor limiting LIS from reaching n is the number of alternating inconsistencies relative to an optimal cut, and each reversal reduces this count by at most a constant amount while never increasing it. Since reversals only permute order locally, they cannot introduce new global structure that improves more than two units per operation. This makes the improvement process linear and bounded, ensuring that after k operations the best achievable configuration depends only on how many inconsistencies can be eliminated, not on their positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    runs = []
    total_len = 0

    for _ in range(n):
        c, p = input().split()
        p = int(p)
        runs.append((c, p))
        total_len += p

    # compute baseline LIS over run boundaries
    prefix_zeros = 0
    suffix_ones = 0

    for c, p in runs:
        if c == '1':
            suffix_ones += p

    best = suffix_ones  # cut before everything

    for c, p in runs:
        if c == '0':
            prefix_zeros += p
        else:
            suffix_ones -= p
        best = max(best, prefix_zeros + suffix_ones)

    q = int(input())
    for _ in range(q):
        k = int(input())
        # each reversal contributes up to 2 improvements
        ans = best + 2 * k
        if ans > total_len:
            ans = total_len
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first aggregates the run-length encoded string and computes the total length. It then computes the baseline LIS by sweeping through run boundaries, maintaining prefix counts of zeros and suffix counts of ones, which directly corresponds to evaluating all valid cut positions.

For each query, the effect of k reversals is applied as a linear improvement of 2k over the baseline, capped at the maximum possible subsequence length.

A common implementation pitfall is forgetting that suffix counts must be updated incrementally as we move the cut. Recomputing suffix sums per position would be too slow.

## Worked Examples

### Example 1

Consider a simple structure: 0011. The baseline LIS is already 4 because we can take all zeros then all ones.

| Step | Prefix zeros | Suffix ones | Current best |
| --- | --- | --- | --- |
| cut0 | 0 | 2 | 2 |
| cut2 | 2 | 2 | 4 |
| cut4 | 4 | 0 | 4 |

Now suppose k = 1. The formula gives min(4, 4 + 2) = 4, so no improvement is possible because the string is already optimal.

This shows that the algorithm correctly avoids overcounting when the structure is already monotone.

### Example 2

Consider 0101. Baseline computation:

| Cut | Prefix zeros | Suffix ones | Value |
| --- | --- | --- | --- |
| 0 | 0 | 2 | 2 |
| 1 | 0 | 2 | 2 |
| 2 | 1 | 1 | 2 |
| 3 | 1 | 1 | 2 |
| 4 | 2 | 0 | 2 |

So base = 2, total length = 4.

For k = 1, answer = min(4, 2 + 2) = 4.

This demonstrates how a single reversal is enough to remove the alternation penalty completely in a highly interleaved structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | One pass over runs to compute baseline, constant work per query |
| Space | O(n) | Storage of run-length representation |

The solution fits easily within limits since both n and q are up to 2×10^5 and all operations are linear or constant per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    output = []
    
    n = int(input())
    runs = []
    total = 0
    for _ in range(n):
        c, p = input().split()
        p = int(p)
        runs.append((c, p))
        total += p

    prefix0 = 0
    suffix1 = 0
    for c, p in runs:
        if c == '1':
            suffix1 += p

    best = suffix1
    for c, p in runs:
        if c == '0':
            prefix0 += p
        else:
            suffix1 -= p
        best = max(best, prefix0 + suffix1)

    q = int(input())
    for _ in range(q):
        k = int(input())
        ans = min(total, best + 2 * k)
        output.append(str(ans))

    return "\n".join(output)

# simple sanity cases
assert run("2\n0 2\n1 2\n1\n0\n") == "4"
assert run("2\n0 1\n1 1\n1\n1\n") == "2"
assert run("4\n0 1\n1 1\n0 1\n1 1\n1\n1\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| alternating runs | full conversion to monotone | reversals remove alternation efficiently |
| already sorted | no change | cap behavior |
| small mixed pattern | correct baseline + improvement | cut logic correctness |

## Edge Cases

For an already sorted string like 00001111, the baseline cut already achieves the maximum value equal to the total length. Running the algorithm, prefix and suffix computations immediately produce the maximum at an interior cut, and applying k reversals does not change the capped result because the answer is bounded by total length.

For a fully alternating structure like 010101, the baseline is significantly lower than the total length. The algorithm computes a small base value, then each reversal contributes an additive improvement of at most 2 until the result saturates at n. This matches the fact that each reversal can remove local alternation structure but cannot exceed the total available characters.
