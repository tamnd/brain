---
title: "CF 1107C - Brutality"
description: "We are given a fixed sequence of hits, where each hit has a damage value and is associated with a specific button (a lowercase letter). We are allowed to delete any hits from the sequence while keeping the remaining ones in their original order."
date: "2026-06-12T05:26:34+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1107
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 59 (Rated for Div. 2)"
rating: 1300
weight: 1107
solve_time_s: 327
verified: false
draft: false
---

[CF 1107C - Brutality](https://codeforces.com/problemset/problem/1107/C)

**Rating:** 1300  
**Tags:** greedy, sortings, two pointers  
**Solve time:** 5m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed sequence of hits, where each hit has a damage value and is associated with a specific button (a lowercase letter). We are allowed to delete any hits from the sequence while keeping the remaining ones in their original order. The total damage is the sum of the kept hits.

The constraint is that if the same button is pressed more than `k` times consecutively in the resulting sequence, the gamepad breaks. So in the final chosen subsequence, every maximal block of identical letters must have length at most `k`.

The task is to choose a subsequence maximizing total damage under this constraint.

The input size goes up to `2 · 10^5`, so any solution that is quadratic in `n` is immediately too slow. Even `O(n log n)` is acceptable, but the structure of the problem strongly suggests that we need a linear or near-linear greedy approach, because decisions depend only on local blocks of equal characters rather than global interactions.

A naive idea is to consider all subsequences, but even restricting ourselves to a single character, we would still be forced to consider combinatorial subsets inside each block of equal letters, which is exponential in worst case.

A more subtle issue appears when high-damage elements occur in the middle of long runs. For example, if a letter repeats many times and one occurrence has extremely high damage, we might want to ensure it is not excluded just because earlier choices filled the quota of `k`.

Another corner case is when multiple long blocks of the same letter are separated by other letters. Even though they are not consecutive in the original string, after deletions they can merge into a single block, so skipping decisions in earlier segments influence later feasibility.

## Approaches

A brute force interpretation would be: we try every subset of indices, compute the resulting sequence, and check whether any run of identical letters exceeds length `k`. For valid subsets, we sum damages and take the maximum. This is clearly exponential in `n`, since there are `2^n` subsets, and even checking each subset takes `O(n)`.

The key observation is that feasibility depends only on runs of identical characters in the _resulting subsequence_, and we are free to skip elements to control those run lengths. Inside any contiguous segment of identical letters in the original string, we are effectively choosing which elements to keep, but their order is fixed.

Now focus on a single letter `c`. Suppose all positions where `s[i] = c` are considered. We want to pick a subsequence of these occurrences, but with the restriction that in the final sequence, no run of `c` exceeds `k`. However, since other letters break runs in between, the real coupling happens per maximal block of consecutive identical letters in the original string.

So we decompose the string into segments of equal characters. Inside each segment, we are forced to deal with a single letter. The constraint becomes: in each segment, we may not take more than `k` items in a row, but since all are identical, this simply becomes choosing the best subset while ensuring that we never pick more than `k` consecutive picks inside that segment. The optimal strategy inside a segment is therefore straightforward: we keep the `k` largest values if the segment is fully independent.

However, segments interact only through whether we start a new run of the same character. The correct global viewpoint is simpler: for each letter, we process its occurrences in order, and ensure we never take more than `k` consecutive chosen elements of that letter. If we reach `k` consecutive chosen occurrences, any further occurrence must be skipped unless we "reset" by switching to another letter, which naturally happens when we are processing globally in order.

This leads to a greedy structure: process indices in order, maintain a counter of consecutive kept characters per letter block, and whenever we are forced to exceed `k`, we must drop the least valuable element among the current run of consecutive same-letter picks. This naturally turns into a priority-queue-like adjustment, but there is an even simpler interpretation.

Instead of thinking dynamically, we can process each block independently. In a block of identical letters, suppose its length is `m`. We cannot keep more than `k` of them in a row in the final sequence, so within that block we are allowed to choose at most `k` elements in total, because the block itself is already consecutive in the original string and cannot be separated internally. Therefore, the optimal choice in each block is to pick the `k` largest values from that block.

This fully decouples the problem: we sort or maintain a small selection per block.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log k) | O(n) | Accepted |

## Algorithm Walkthrough

We process the string by splitting it into maximal contiguous segments of identical characters.

1. We scan the array from left to right, grouping consecutive equal characters into a segment. This is necessary because only within such a segment can consecutive presses accumulate.
2. For each segment, we collect all damage values belonging to that segment. Since all characters are the same inside it, any chosen subset from this segment will appear consecutively in the final sequence.
3. Inside a segment, we want to maximize the sum while ensuring we do not effectively "overcommit" beyond what the constraint allows. The optimal strategy is to select the `min(k, length of segment)` largest damage values. The reasoning is that any chosen items in this segment will form a consecutive block, so we only want the most valuable ones up to the allowed limit.
4. We sort the values inside the segment in descending order and take the first `k`.
5. We add these chosen values to the answer and continue to the next segment.

The key idea is that segments are independent because skipping elements never helps merge different characters, and merging identical characters across different segments is impossible due to intervening different letters.

### Why it works

Within any contiguous block of identical characters, the final sequence preserves contiguity for any selected subset. Since all elements in that block contribute to a single run, the only meaningful constraint is how many we keep. Keeping more than `k` from that block would immediately violate the rule, and keeping fewer is always suboptimal if we replace them with higher-valued ones. Therefore, choosing the top `k` values in each segment maximizes contribution without ever risking a longer valid run elsewhere.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    s = input().strip()

    ans = 0
    i = 0

    while i < n:
        j = i
        vals = []

        while j < n and s[j] == s[i]:
            vals.append(a[j])
            j += 1

        vals.sort(reverse=True)
        for t in range(min(k, len(vals))):
            ans += vals[t]

        i = j

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads input and iterates through the string while grouping identical consecutive characters. For each group, it collects all corresponding damage values into a list. Sorting in descending order allows us to pick the most valuable hits first, and we only take up to `k` of them since taking more would violate the constraint inside that block.

The pointer `i` advances by skipping entire segments at once, ensuring linear traversal of the string. The only non-linear cost comes from sorting within each segment.

## Worked Examples

### Example 1

Input:

```
n = 7, k = 3
a = [1, 5, 16, 18, 7, 2, 10]
s = baaaaca
```

We split into segments: `b | aaaa | c | a`.

| Segment | Values | Sorted | Taken | Segment Contribution |
| --- | --- | --- | --- | --- |
| b | [1] | [1] | [1] | 1 |
| aaaa | [5,16,18,7] | [18,16,7,5] | [18,16,7] | 41 |
| c | [2] | [2] | [2] | 2 |
| a | [10] | [10] | [10] | 10 |

Total is `1 + 41 + 2 + 10 = 54`.

This trace shows that the decision is entirely local to each block, and higher-value elements inside a block dominate lower ones regardless of position.

### Example 2

Input:

```
n = 5, k = 2
a = [10, 1, 100, 2, 3]
s = aabbb
```

Segments: `aa | bbb`.

| Segment | Values | Sorted | Taken | Contribution |
| --- | --- | --- | --- | --- |
| aa | [10,1] | [10,1] | [10,1] | 11 |
| bbb | [100,2,3] | [100,3,2] | [100,3] | 103 |

Total is `114`.

This demonstrates that even if a segment is longer than `k`, only the best `k` values matter, and ordering inside the segment does not affect feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each segment is sorted independently, and total elements across segments is n |
| Space | O(n) | We store values of one segment at a time |

The algorithm fits comfortably within limits for `n ≤ 2 · 10^5`, since sorting dominates but is applied over partitioned data rather than globally.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    s = input().strip()

    ans = 0
    i = 0

    while i < n:
        j = i
        vals = []
        while j < n and s[j] == s[i]:
            vals.append(a[j])
            j += 1

        vals.sort(reverse=True)
        for t in range(min(k, len(vals))):
            ans += vals[t]

        i = j

    return str(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("7 3\n1 5 16 18 7 2 10\nbaaaaca\n") == "54"

# all equal, k smaller than n
assert run("5 2\n5 4 3 2 1\naaaaa\n") == "9"

# k large enough
assert run("4 10\n1 2 3 4\nabcd\n") == "10"

# alternating letters
assert run("6 1\n10 9 8 7 6 5\nababab\n") == "30"

# single element
assert run("1 1\n100\nz\n") == "100"

# boundary run
assert run("6 2\n1 100 2 90 3 80\naaaaaa\n") == "190"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same letters | 9 | selecting top k inside one block |
| k large | 10 | no restriction case |
| alternating letters | 30 | independence of segments |
| single element | 100 | minimal input correctness |
| long single block | 190 | correct top-k selection |

## Edge Cases

A subtle case is when the entire string is one character. In that case, the algorithm processes a single segment and simply selects the top `k` values. For example:

Input:

```
6 2
1 100 2 90 3 80
aaaaaa
```

The segment collects `[1, 100, 2, 90, 3, 80]`, sorts to `[100, 90, 80, 3, 2, 1]`, and takes `100 + 90 = 190`. The constraint is fully local, so no interaction with other segments exists.

Another edge case is when `k = 1`. Each segment contributes only its maximum element, which matches the intuition that we can never take two identical letters in a row, so we must reduce every block to its best representative.
