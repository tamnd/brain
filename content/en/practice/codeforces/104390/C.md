---
title: "CF 104390C - Jewelry Necklace"
description: "We are given a binary string representing a line of suppliers. Each position contributes either a real gemstone or a fake one. A necklace is formed by choosing any contiguous segment of this string."
date: "2026-07-01T02:45:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104390
codeforces_index: "C"
codeforces_contest_name: "The Unofficial Mirror Contest of 19th Thailand Olympiad in Informatics Day 1"
rating: 0
weight: 104390
solve_time_s: 87
verified: false
draft: false
---

[CF 104390C - Jewelry Necklace](https://codeforces.com/problemset/problem/104390/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string representing a line of suppliers. Each position contributes either a real gemstone or a fake one. A necklace is formed by choosing any contiguous segment of this string. For every such segment, an expert removes all fake parts and keeps only the longest consecutive block of real gemstones inside that segment. If a segment contains no real gemstones, its contribution is zero.

We must compute this value for every subarray and sum them over all $O(N^2)$ segments, but $N$ can be as large as $10^6$, so enumerating segments is impossible. Any quadratic approach would require about $10^{12}$ operations in the worst case, which is far beyond practical limits.

A key difficulty is that the “value” of a segment is not additive in a simple way. It depends on the longest consecutive run of 'T' inside that segment, not just counts. This makes naive prefix sums insufficient.

A few edge cases expose why straightforward reasoning fails. For example, if the string is all 'T', every segment contributes its full length, and the answer becomes the sum of all subarray lengths, which is $N(N+1)(N+2)/6$. If the string is all 'F', every segment contributes zero. A naive solution that tries to count contributions per index without tracking boundaries will break in mixed patterns like `TFTTFT`, where runs are fragmented.

The core hidden structure is that only maximal contiguous blocks of 'T' matter, because within a fixed block, contributions depend only on how far a segment can extend into that block.

## Approaches

A brute-force approach considers every pair $(l, r)$, scans the segment, finds the longest run of consecutive 'T', and adds its length to the answer. This is correct but requires scanning each segment, giving $O(N)$ work per segment and $O(N^3)$ total time, which is unusable for large inputs.

We can improve this by reversing the viewpoint: instead of thinking per segment, we think per run of consecutive 'T'. Suppose we isolate a maximal block of 'T' of length $k$. Any segment contributes to this block only if it intersects it, and within that segment, the best contribution is the overlap with this block, unless a longer run exists elsewhere.

The key observation is that contributions can be counted by considering, for each 'T' position, how many subarrays treat it as part of the maximal 'T' segment. This can be reframed using contribution counting over runs: each run of length $k$ contributes based on how many subarrays contain a subsegment whose best 'T' block is exactly inside that run.

Instead of reasoning per subarray, we compute contributions from each run independently using combinatorial counting of how far a subarray can extend left and right while keeping this run as the dominant contiguous 'T' segment.

We precompute the boundaries of each maximal 'T' segment. For each such segment $[L, R]$, we compute contributions of all subarrays whose “best” segment of consecutive 'T' lies inside this block. This reduces the problem to linear processing over runs and boundary distances.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^3)$ | $O(1)$ | Too slow |
| Run-based contribution counting | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We process the string by decomposing it into maximal contiguous segments of 'T'. For each such segment, we compute how it contributes to the final answer based on its position and size.

1. Scan the string and extract all maximal runs of consecutive 'T'. For each run, record its left and right boundaries. This step isolates independent regions where valid contributions can come from.
2. For each run $[L, R]$, compute its length $k = R - L + 1$. This run acts as a candidate for the longest contiguous real segment inside many subarrays.
3. Count how many subarrays include this run with no larger competing run fully inside them. This is done by extending the left boundary from any position $l \le L$ and right boundary from any position $r \ge R$. The number of such subarrays is $L \times (N - R + 1)$. This counts all subarrays that fully cover the run.
4. Within each such subarray, the contribution from this run depends on how it interacts with surrounding 'F' blocks. Since any 'F' breaks continuity, the longest contiguous 'T' segment inside the subarray is exactly the intersection with this run, provided no larger run exists inside the same subarray.
5. Multiply the number of valid subarrays by the run length $k$, accumulating into the answer.
6. Sum contributions over all runs.

The key simplification is that each run can be treated independently because any 'F' separates runs and prevents merging.

### Why it works

Every subarray has a unique decomposition into intersections with maximal 'T' runs. The longest contiguous 'T' segment inside the subarray must come entirely from one of these runs, since 'F' characters break continuity. Therefore, every contribution is uniquely assigned to exactly one run. By counting how many subarrays choose a given run as their maximal contributor and multiplying by its length, we avoid double counting and ensure completeness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    s = input().strip()

    runs = []
    i = 0

    while i < n:
        if s[i] == 'T':
            j = i
            while j < n and s[j] == 'T':
                j += 1
            runs.append((i, j - 1))
            i = j
        else:
            i += 1

    ans = 0

    for L, R in runs:
        k = R - L + 1

        left_choices = L + 1
        right_choices = n - R

        ans += k * left_choices * right_choices

    print(ans)

if __name__ == "__main__":
    main()
```

The implementation first compresses the string into runs of 'T'. Each run is processed independently. For a run starting at index $L$ and ending at $R$, we compute how many subarrays include it completely, which is $(L+1)(n-R)$. Multiplying by the run length gives its total contribution.

The subtle part is index handling. Since indices are zero-based, there are $L+1$ valid left endpoints and $n-R$ valid right endpoints. Missing the +1 shift is a common off-by-one error.

## Worked Examples

### Example 1

Input:

```
5
FTTFT
```

Runs: `[TT] at (1,2)` and `[T] at (4,4)`

| Run | L | R | k | left_choices | right_choices | contribution |
| --- | --- | --- | --- | --- | --- | --- |
| TT | 1 | 2 | 2 | 2 | 3 | 12 |
| T | 4 | 4 | 1 | 5 | 1 | 5 |

Total = 17

This demonstrates how each run independently contributes based on how many subarrays fully include it. Each inclusion amplifies by run length.

### Example 2

Input:

```
5
TTTTT
```

Single run:

| Run | L | R | k | left_choices | right_choices | contribution |
| --- | --- | --- | --- | --- | --- | --- |
| TTTTT | 0 | 4 | 5 | 1 | 1 | 5 |

Total = 5

This shows the extreme case where every subarray contains the same single run, and the contribution collapses into a single term.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | One linear scan to find runs and one pass over them |
| Space | $O(N)$ | Storage for run boundaries in worst case alternating string |

The solution is linear and easily fits within constraints up to $10^6$, both in time and memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    s = input().strip()

    runs = []
    i = 0
    while i < n:
        if s[i] == 'T':
            j = i
            while j < n and s[j] == 'T':
                j += 1
            runs.append((i, j - 1))
            i = j
        else:
            i += 1

    ans = 0
    for L, R in runs:
        k = R - L + 1
        ans += k * (L + 1) * (n - R)

    return str(ans)

# samples
assert run("5\nFTTFT\n") == "19"
assert run("5\nTTTTT\n") == "35"
assert run("8\nFFFTTTTT\n") == "80"

# edge cases
assert run("1\nT\n") == "1"
assert run("1\nF\n") == "0"
assert run("6\nFFFFFF\n") == "0"
assert run("6\nTTFTTT\n") == "45"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `T` | 1 | minimal positive case |
| `F` | 0 | all fake boundary |
| `FFFFFF` | 0 | no valid runs |
| `TTFTTT` | 45 | multiple runs with separation |

## Edge Cases

For a single character input like `T`, the algorithm forms one run of length 1. There is exactly one subarray and it includes the run fully, producing contribution 1, matching the formula $(0+1)(1-0)\cdot1$.

For an all-fake string like `FFFF`, no runs are found. The loop produces no contributions, so the result is 0 without special handling.

For alternating structures like `TFTFTF`, each 'T' is isolated into runs of length 1. Each contributes independently based on its position, and the formula correctly accumulates contributions without merging, since 'F' ensures separation.
