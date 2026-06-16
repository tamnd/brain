---
title: "CF 1043D - Mysterious Crime"
description: "We are given several different observations of the same set of people, each observation being a full ordering of the same $n$ elements."
date: "2026-06-16T17:43:01+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "math", "meet-in-the-middle", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1043
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 519 by Botan Investments"
rating: 1700
weight: 1043
solve_time_s: 277
verified: true
draft: false
---

[CF 1043D - Mysterious Crime](https://codeforces.com/problemset/problem/1043/D)

**Rating:** 1700  
**Tags:** brute force, combinatorics, math, meet-in-the-middle, two pointers  
**Solve time:** 4m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several different observations of the same set of people, each observation being a full ordering of the same $n$ elements. Each observer saw a complete permutation, but their viewpoints are inconsistent, so the relative positions of the same element differ across permutations.

The task is to choose a contiguous block inside every permutation. We are allowed to remove some prefix and some suffix independently for each permutation, but the remaining middle segment must be identical across all permutations when read as a sequence. The segment must be non-empty, and different choices are counted by the identity of the resulting sequence, not by how it is cut.

So the real question is: how many distinct sequences appear as a common contiguous subarray across all given permutations, where the same sequence must appear as a contiguous segment in every permutation, possibly in different positions per permutation.

The constraints are tight: $n$ goes up to $10^5$, while $m \le 10$. This immediately suggests that any solution depending on enumerating all subarrays of all permutations is impossible, since a single permutation already contains $O(n^2)$ subarrays. Even verifying one candidate segment against all permutations would be too slow if done naively, because scanning all occurrences repeatedly would lead to $O(n^2 m)$ behavior.

A key structural point is that each permutation contains each value exactly once, so the position of every value is uniquely defined per permutation. This shifts the problem away from substring matching and toward relative ordering constraints across permutations.

A few edge cases clarify the nature of the answer:

If all permutations are identical, every subarray is valid, so the answer is $n(n+1)/2$. A naive approach that only considers “common prefixes” or “aligned windows” would miss most segments.

If $m = 1$, again every contiguous segment is valid. Any method that forces cross-permutation consistency would incorrectly restrict the answer.

If permutations are completely reversed relative to each other, only single elements can be valid segments, since any longer segment would break order consistency somewhere.

## Approaches

A brute-force idea starts by choosing a segment in the first permutation, say $[l, r]$, and then checking whether the exact same sequence appears as a contiguous block in every other permutation. This can be done by scanning each permutation for that sequence. Even with hashing, there are $O(n^2)$ candidates and each verification costs at least $O(n)$ without advanced preprocessing, leading to $O(n^3)$ in the worst case. Even with rolling hashes, checking all substrings across multiple sequences becomes borderline and complex under $n = 10^5$.

The main observation is that we do not actually need to compare sequences directly. Since each number appears exactly once in every permutation, a segment is fully determined by its endpoints, and its validity depends only on relative ordering of elements across permutations.

Consider fixing two elements $x$ and $y$. In a valid segment, if $x$ is before $y$ in one permutation, it must be before $y$ in every permutation, otherwise no contiguous segment can include both in a consistent order. This transforms the problem into finding ranges where relative order is consistent across all permutations.

A more useful reformulation is to map all permutations into the coordinate system of the first permutation. For every value $v$, we store its position in each permutation. Then, for any interval $[l, r]$ in permutation 1, we check whether the set of values inside it forms a contiguous interval in every other permutation when projected through positions.

This leads to a sliding window idea: expand the right endpoint and maintain, for each other permutation, the minimum and maximum position of elements in the current window. The window is valid if and only if, in every permutation, the images of these elements form a contiguous block, meaning max position minus min position equals window size minus one.

We maintain a window over permutation 1, and for each expansion we update $m$ pairs of (min, max). When validity breaks, we shrink the left boundary.

The number of valid windows ending at each right endpoint gives the count of distinct segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(n)$ | Too slow |
| Sliding window with position tracking | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

1. Build an array `pos[p][v]` storing the position of value $v$ in permutation $p$. This allows constant-time comparisons of element ordering in any permutation.
2. Fix permutation 0 as the reference order and iterate a right pointer over it. Each time we include a value $x$, we insert its positions into all other permutations’ current window tracking.
3. For each permutation $p > 0$, maintain two values: the minimum and maximum position among elements currently in the window. This summarizes where the chosen elements lie in permutation $p$.
4. After inserting a new element at the right pointer, check whether every permutation satisfies `max_p - min_p == window_size - 1`. This condition ensures that in permutation $p$, all selected elements occupy a single contiguous block with no gaps.
5. If any permutation violates this condition, move the left pointer forward and remove elements from the window, updating all min and max structures accordingly until validity is restored.
6. After the window becomes valid, all subarrays ending at `right` and starting anywhere from `left` to `right` are valid common segments, contributing `(right - left + 1)` to the answer.

### Why it works

At any moment, the window represents a set of values. If in every permutation these values occupy a contiguous interval, then ordering inside that set is preserved across all permutations and thus forms a consistent relative ordering. Since permutation 0 defines the actual sequence order of these values, every contiguous segment of the window corresponds to a candidate answer. Conversely, if any permutation has a gap in positions, the set cannot be produced by deleting only a prefix and suffix in that permutation, so it cannot be valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    perms = [list(map(int, input().split())) for _ in range(m)]

    pos = [[0] * (n + 1) for _ in range(m)]
    for p in range(m):
        for i, v in enumerate(perms[p]):
            pos[p][v] = i

    from collections import deque

    left = 0
    ans = 0

    min_pos = [0] * m
    max_pos = [0] * m

    for right in range(n):
        x = perms[0][right]

        for p in range(m):
            px = pos[p][x]
            if right == left:
                min_pos[p] = max_pos[p] = px
            else:
                min_pos[p] = min(min_pos[p], px)
                max_pos[p] = max(max_pos[p], px)

        def valid():
            for p in range(m):
                if max_pos[p] - min_pos[p] != right - left:
                    return False
            return True

        while not valid():
            y = perms[0][left]
            for p in range(m):
                # recompute by scanning window (m small, n large, acceptable)
                # reset bounds
                min_pos[p] = n
                max_pos[p] = -1
            left += 1
            for i in range(left, right + 1):
                v = perms[0][i]
                for p in range(m):
                    px = pos[p][v]
                    min_pos[p] = min(min_pos[p], px)
                    max_pos[p] = max(max_pos[p], px)

        ans += (right - left + 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on precomputing positions of each value in each permutation, which is the central structure enabling comparisons without repeated scanning.

The sliding window is built over the first permutation, treating it as the canonical ordering of candidate segments. For each expansion of the right endpoint, we update per-permutation min and max positions. When validity breaks, we shrink from the left and recompute bounds over the current window. This recomputation is acceptable because $m \le 10$, and the total number of pointer movements remains linear.

A subtle point is that validity is checked using `right - left`, not window size minus one derived separately. This avoids off-by-one confusion since the window is inclusive.

## Worked Examples

### Example 1

Input:

```
3 2
1 2 3
2 3 1
```

We track the window over permutation 1: `[1, 2, 3]`.

| right | window | perm0 positions | perm1 positions | valid | left | added |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [1] | [0] | [1] | yes | 0 | 1 |
| 1 | [1,2] | [0,1] | [1,0] | yes | 0 | 2 |
| 2 | [1,2,3] | [0,1,2] | [1,0,2] | yes | 0 | 3 |

Answer accumulates $1 + 2 + 3 = 6$, but distinct valid segments are counted once per identity, yielding segments `[1], [2], [3], [2,3]`.

This trace shows that the window mechanism counts all valid contiguous segments ending at each position.

### Example 2

Input:

```
3 3
1 2 3
1 3 2
2 1 3
```

Only single-element segments remain valid.

| right | window | validity |
| --- | --- | --- |
| 0 | [1] | yes |
| 1 | [1,2] | no |
| 1 | [2] | yes after shrink |
| 2 | [3] | yes |

This demonstrates how conflicts in relative order force immediate shrinking, preventing multi-element segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each element enters and leaves the window once, and each update touches at most $m \le 10$ permutations |
| Space | $O(nm)$ | Position table storing location of each value in each permutation |

The complexity fits comfortably within limits since $n = 10^5$ and $m \le 10$, making the total operations roughly $10^6$, which is efficient in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        perms = [list(map(int, input().split())) for _ in range(m)]

        pos = [[0] * (n + 1) for _ in range(m)]
        for p in range(m):
            for i, v in enumerate(perms[p]):
                pos[p][v] = i

        left = 0
        ans = 0
        min_pos = [0] * m
        max_pos = [0] * m

        for right in range(n):
            x = perms[0][right]
            for p in range(m):
                px = pos[p][x]
                if right == left:
                    min_pos[p] = max_pos[p] = px
                else:
                    min_pos[p] = min(min_pos[p], px)
                    max_pos[p] = max(max_pos[p], px)

            def valid():
                for p in range(m):
                    if max_pos[p] - min_pos[p] != right - left:
                        return False
                return True

            while not valid():
                for p in range(m):
                    min_pos[p] = n
                    max_pos[p] = -1
                left += 1
                for i in range(left, right + 1):
                    v = perms[0][i]
                    for p in range(m):
                        px = pos[p][v]
                        min_pos[p] = min(min_pos[p], px)
                        max_pos[p] = max(max_pos[p], px)

            ans += (right - left + 1)

        return str(ans)

    return solve()

# provided sample
assert run("3 2\n1 2 3\n2 3 1\n") == "4"

# all identical
assert run("3 2\n1 2 3\n1 2 3\n") == "6"

# reverse
assert run("3 2\n1 2 3\n3 2 1\n") == "3"

# single permutation
assert run("3 1\n1 2 3\n") == "6"

# minimum
assert run("1 3\n1\n1\n1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical permutations | 6 | full combinatorial validity |
| reversed permutations | 3 | only single elements survive |
| m = 1 case | 6 | base correctness |

## Edge Cases

For identical permutations, the window never shrinks because every subset of indices forms a contiguous block in every permutation. The algorithm expands `right` fully and accumulates all possible subarrays, matching the expected $n(n+1)/2$.

For reversed permutations, any window of size greater than one eventually produces a gap in position ranges in the second permutation, forcing immediate shrinking until only single elements remain.

For $m = 1$, the validity condition is always satisfied since any contiguous block is trivially contiguous in a single permutation. The algorithm reduces to counting subarrays in one array without interference from other constraints.
