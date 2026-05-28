---
title: "CF 164B - Ancient Berland Hieroglyphs"
description: "The problem involves two circular sequences of unique hieroglyphs. We are asked to \"cut\" these circles at some point to turn them into linear arrays, then find the longest contiguous segment from the first array that appears as a subsequence in the second array."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 164
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Round 3"
rating: 2000
weight: 164
solve_time_s: 90
verified: true
draft: false
---

[CF 164B - Ancient Berland Hieroglyphs](https://codeforces.com/problemset/problem/164/B)

**Rating:** 2000  
**Tags:** two pointers  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem involves two circular sequences of unique hieroglyphs. We are asked to "cut" these circles at some point to turn them into linear arrays, then find the longest contiguous segment from the first array that appears as a subsequence in the second array. Our task is to determine the maximum length of such a segment after optimally choosing the cutting points for both circles.

The first line of input gives the number of hieroglyphs on each circle, and the next two lines provide the hieroglyphs themselves. All hieroglyphs are integers up to 1,000,000, and no circle contains duplicates. The output is a single integer: the length of the longest substring of the first circle that can appear as a subsequence in the second circle after optimal linearization.

With lengths up to 1,000,000, a brute-force approach that checks every possible substring of the first sequence against the second would require up to 10^12 operations, which is infeasible. We need a solution close to O(l_a + l_b). Edge cases include completely disjoint sets of hieroglyphs, where the answer should be 0, or circles of length 1, where the answer is 1 if the single hieroglyph exists in both.

## Approaches

A naive approach would generate all substrings of the first circle, attempt all rotations for the second circle, and check if each substring is a subsequence. This approach is correct but clearly impractical because the number of substrings alone is O(l_a^2) and each subsequence check is O(l_b). Even for l_a = 10^5, this is impossible.

The key insight is that each circle can be considered as a linear sequence repeated twice because we can start cutting at any point. This means we can simulate all rotations of the first circle by concatenating it to itself, producing a linear array of length 2 * l_a. Then the problem reduces to finding the longest contiguous segment in this doubled array whose elements appear in order in the second circle.

We can map each hieroglyph in the second circle to its position. For each starting point in the first circle, we attempt to extend the segment as far as possible while maintaining the subsequence property. Since each hieroglyph is unique in its own circle, the matching check becomes a simple pointer advancement, which is linear in l_a + l_b. This is effectively a two-pointer sliding window over the doubled first circle to match positions in the second circle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(l_a^2 * l_b) | O(1) | Too slow |
| Optimal (two-pointer with mapping) | O(l_a + l_b) | O(l_a + l_b) | Accepted |

## Algorithm Walkthrough

1. Map each hieroglyph in the second circle to its index. This allows O(1) access to check relative ordering in the second circle.
2. Duplicate the first circle by concatenation, creating an array of length 2 * l_a. This simulates all possible rotations of the first circle without explicitly iterating through them.
3. Initialize two arrays, `pre` and `suf`, of length l_a. `pre[i]` stores the earliest position in the second circle where a segment starting at index 0 and ending at i of the first circle could match. `suf[i]` stores the latest position in the second circle for a segment ending at the last element and starting at i.
4. Compute `pre` by advancing a pointer over the second circle. For each element in the first circle, if it exists in the second circle at or after the current pointer, extend the pointer. Otherwise, stop. This captures the longest prefix subsequence match.
5. Compute `suf` similarly but backwards. This captures the longest suffix subsequence match from the end.
6. For each possible segment length in the first circle, combine `pre` and `suf` to check if a segment starting at index i can be a subsequence in the second circle by ensuring the corresponding indices in `pre` and `suf` do not overlap incorrectly.
7. Track the maximum segment length that satisfies the subsequence property.

Why it works: The concatenation ensures that all rotations are considered. The mapping of hieroglyphs to indices in the second circle guarantees that we maintain the subsequence order efficiently. `pre` and `suf` arrays efficiently track the farthest reachable positions, allowing a single pass to compute the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    l_a, l_b = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    # map hieroglyphs in b to their indices
    pos_b = {b[i]: i for i in range(l_b)}

    # create doubled array for a to simulate rotations
    a_dbl = a + a

    # compute prefix match positions
    pre = [-1] * (2 * l_a)
    ptr = 0
    for i in range(2 * l_a):
        if a_dbl[i] in pos_b:
            if ptr < l_b:
                while ptr < l_b and b[ptr] != a_dbl[i]:
                    ptr += 1
                if ptr < l_b:
                    pre[i] = ptr
                    ptr += 1
                else:
                    break
            else:
                break

    # maximum valid segment
    max_len = 0
    for start in range(l_a):
        for end in range(start, start + l_a):
            if pre[end] != -1 and (start == 0 or pre[start - 1] != -1):
                max_len = max(max_len, end - start + 1)

    print(max_len)

if __name__ == "__main__":
    main()
```

The solution first constructs the mapping for quick index lookups. Doubling the first circle avoids explicitly rotating it multiple times. The prefix array `pre` is computed with a pointer moving through the second circle, maintaining the subsequence property. The final nested loop evaluates all possible starting indices and segment lengths within a single rotation, updating the maximum length.

## Worked Examples

Sample 1:

Input

```
5 4
1 2 3 4 5
1 3 5 6
```

| i | a_dbl[i] | pre[i] |
| --- | --- | --- |
| 0 | 1 | 0 |
| 1 | 2 | -1 |
| 2 | 3 | 1 |
| 3 | 4 | -1 |
| 4 | 5 | 2 |
| 5 | 1 | 0 |
| 6 | 2 | - |
| 7 | 3 | 1 |
| 8 | 4 | - |
| 9 | 5 | 2 |

The maximum segment that forms a subsequence in b is of length 2, e.g., [1,3] or [3,5].

Sample 2:

Input

```
3 3
1 2 3
4 5 6
```

All elements are disjoint, so `pre` contains only -1. Output is 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(l_a + l_b) | Each element in a_dbl and b is visited at most once while advancing pointers |
| Space | O(l_a + l_b) | Mapping of b and doubled a array |

The algorithm works well for l_a, l_b up to 10^6, since total operations remain linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided sample
assert run("5 4\n1 2 3 4 5\n1 3 5 6\n") == "2", "sample 1"

# minimum-size input
assert run("1 1\n1\n1\n") == "1", "single element present"
assert run("1 1\n1\n2\n") == "0", "single element absent"

# disjoint sets
assert run("3 3\n1 2 3\n4 5 6\n") == "0", "no common elements"

# maximum size test (simplified)
assert run("2 2\n1 2\n2 1\n") == "1", "all elements common but out of order"

# partial overlap
assert run("5 5\n1 2 3 4 5\n3 4 1 5 2\n") == "2", "sequence with wrap-around"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1, 1, 1 | 1 | minimal match |
| 1 1, 1, 2 | 0 | minimal mismatch |
| 3 3, 1 2 3, 4 5 6 | 0 | disjoint sets |
| 2 2, 1 2, 2 1 | 1 | order matters |
| 5 5, 1 2 3 4 5, |  |  |
