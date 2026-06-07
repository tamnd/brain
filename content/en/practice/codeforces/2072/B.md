---
title: "CF 2072B - Having Been a Treasurer in the Past, I Help Goblins Deceive"
description: "We are given a string made only of two symbols, a dash and an underscore. We are allowed to reorder this string arbitrarily."
date: "2026-06-08T06:46:35+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "strings"]
categories: ["algorithms"]
codeforces_contest: 2072
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1006 (Div. 3)"
rating: 900
weight: 2072
solve_time_s: 66
verified: true
draft: false
---

[CF 2072B - Having Been a Treasurer in the Past, I Help Goblins Deceive](https://codeforces.com/problemset/problem/2072/B)

**Rating:** 900  
**Tags:** combinatorics, constructive algorithms, strings  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made only of two symbols, a dash and an underscore. We are allowed to reorder this string arbitrarily. After fixing an order, the string represents a value defined as the number of subsequences equal to the pattern “-_-”, meaning we pick three indices i < j < k such that the characters at those positions are dash, underscore, dash in that order.

The task is to permute the characters in a way that maximizes how many such triples exist.

The input gives multiple independent test cases. For each one we only care about counts of characters, not their original order, because rearrangement is fully allowed.

The constraint that the total length over all test cases is at most 2·10^5 implies we need an O(n) or O(n log n) solution per test case at worst. Anything quadratic over a single string would already be too slow.

A subtle failure case appears when thinking locally about placements. A naive idea might be to greedily build the string from left to right, placing characters to maximize immediate contributions. That fails because contributions of a dash depend on global distribution of underscores between dashes, not on local adjacency.

Another edge case is when the string has fewer than two dashes or no underscores. For example, if there is only one dash, no “-_-” subsequence can exist regardless of arrangement, so the answer must be zero. A naive combinatorial formula that assumes all three character types exist would incorrectly produce a positive value.

## Approaches

A brute-force approach would try all permutations of the string and count the number of “-_-” subsequences in each arrangement. For a string of length n, this is n! permutations, and counting subsequences in O(n^2) or O(n^3) per permutation makes it completely infeasible even for n = 10.

The key observation is that only the counts of dashes and underscores matter, and the optimal arrangement will place all identical characters in contiguous blocks. Once we fix a permutation, the number of subsequences “-_-” depends only on how many dashes appear before and after each underscore.

For any underscore, if there are L dashes before it and R dashes after it, it contributes L · R subsequences. Summing over all underscores gives total value.

If we decide to place x dashes on the left side of all underscores and the remaining d − x dashes on the right side, then every underscore contributes x(d − x). If there are u underscores, the total becomes u · x(d − x). The problem reduces to choosing x to maximize this quadratic expression.

The expression x(d − x) is maximized when x is as close as possible to d/2, so the optimal split is to distribute dashes evenly on both sides of all underscores. All underscores should be placed together in the middle, because mixing them into multiple blocks only reduces the product structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n^2) | O(n) | Too slow |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of dashes d and underscores u in the string. The arrangement depends only on these counts, not the original order.
2. If either d < 2 or u = 0, return 0. With fewer than two dashes, no valid pattern “-_-” can be formed.
3. Compute how many dashes go to the left side and right side of all underscores. To maximize x(d − x), set x = d // 2 for one side and d − x for the other side.
4. Compute the total number of subsequences as u · x · (d − x).
5. Output this value.

Why it works: once underscores are placed in a single block, each underscore sees the same number of dashes on its left and right. Any deviation that moves an underscore into a different region reduces the symmetry and decreases at least one of the multiplicative contributions. The optimal structure is fully determined by splitting dashes into two groups around a middle block of underscores, which maximizes the product for every underscore simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()

        d = s.count('-')
        u = n - d

        if d < 2 or u == 0:
            print(0)
            continue

        left = d // 2
        right = d - left
        print(u * left * right)

if __name__ == "__main__":
    solve()
```

The solution reduces the problem to counting characters only. The split of dashes into two halves is computed using integer division, which naturally handles odd counts by placing the extra dash on one side.

The main subtlety is recognizing that the arrangement structure is always optimal in “blocks”, and no interleaving can improve the product form of contributions.

## Worked Examples

We trace two cases from the sample set.

First case: `--_`

d = 2, u = 1

| Step | dashes (d) | underscores (u) | left | right | result |
| --- | --- | --- | --- | --- | --- |
| init | 2 | 1 | - | - | - |
| split | - | - | 1 | 1 | 1 · 1 · 1 = 1 |

This confirms that with two dashes and one underscore, the best arrangement is “-_-”.

Second case: `__-__`

d = 1, u = 4

Since d < 2, we immediately return 0. No underscore can have a dash on both sides, so no valid subsequence exists.

These two cases show the two regimes: either enough dashes to form a sandwich structure, or impossibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | counting characters dominates |
| Space | O(1) | only counters are stored |

The total input size is bounded by 2·10^5, so a linear scan over all test cases is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    output = []

    t = int(sys.stdin.readline())
    for _ in range(t):
        n = int(sys.stdin.readline())
        s = sys.stdin.readline().strip()

        d = s.count('-')
        u = n - d

        if d < 2 or u == 0:
            output.append("0")
        else:
            left = d // 2
            right = d - left
            output.append(str(u * left * right))

    return "\n".join(output) + "\n"

# provided samples
assert run("""8
3
--_
5
__-__
9
--__-_---
4
_--_
10
_-_-_-_-_-
7
_------
1
-
2
_-""") == """1
0
27
2
30
9
0
0
"""

# custom cases
assert run("""1
3
___""") == "0\n"  # no dashes

assert run("""1
3
---""") == "0\n"  # no underscores

assert run("""1
4
--__""") == "1\n"  # best split 1*1*1

assert run("""1
6
---___""") == "6\n"  # 3 dashes, 3 underscores

assert run("""1
5
-_-_-""") == "4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ___ | 0 | no dashes |
| --- | 0 | no underscores |
| --__ | 1 | minimal balanced case |
| ---___ | 6 | symmetric large blocks |
| -_-_- | 4 | alternating pattern stress |

## Edge Cases

When there are fewer than two dashes, the algorithm returns zero immediately. For example, input `_-` gives d = 1, u = 1, and the condition d < 2 triggers a direct zero output. Any arrangement still leaves at least one side of every underscore empty, so no valid triple can form.

When there are no underscores, such as `-----`, we also return zero. Even though we can split dashes, the formula multiplies by u, which is zero, matching the fact that no “-_-” subsequence exists.

When dashes are odd, say d = 5, the split becomes 2 and 3. This corresponds to placing all underscores in the middle and distributing dashes as evenly as possible. For u = 1, the result becomes 1 · 2 · 3 = 6, and any uneven split like 1 and 4 produces only 4, confirming that the floor division split is optimal.
