---
title: "CF 105346C - Spooky Hallway"
description: "We are given a binary string representing a line of lanterns, where each position is either lit or unlit. In one move, we are allowed to pick any contiguous segment and flip every bit inside it, turning zeros into ones and ones into zeros."
date: "2026-06-23T05:43:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105346
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 09-13-24 Div. 2 (Beginner)"
rating: 0
weight: 105346
solve_time_s: 88
verified: false
draft: false
---

[CF 105346C - Spooky Hallway](https://codeforces.com/problemset/problem/105346/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string representing a line of lanterns, where each position is either lit or unlit. In one move, we are allowed to pick any contiguous segment and flip every bit inside it, turning zeros into ones and ones into zeros. The goal is to reach a configuration where the entire string becomes uniform, either all zeros or all ones, using as few such segment flips as possible.

The input size can go up to one hundred thousand characters. This immediately rules out any approach that tries all possible segments or simulates sequences of flips explicitly. Anything worse than linear or near-linear time will struggle, since the number of substrings alone is quadratic.

A naive idea is to try choosing every possible final target state, either all zeros or all ones, and then greedily or naively simulate flipping segments until the string matches. Another common incorrect attempt is to flip every maximal block of mismatched characters independently without considering merging opportunities, which can overcount operations.

For example, consider `010`. If we aim for all zeros, flipping the middle segment gives `000` in one move. A greedy that flips each mismatched character individually would incorrectly suggest two operations. Conversely, on `01010`, careless local decisions can easily overcount or undercount because flipping one segment changes multiple future boundaries.

The subtle issue is that a flip does not act locally in isolation, it changes adjacency structure, so the real cost depends on transitions between consecutive characters rather than individual characters themselves.

## Approaches

A brute-force approach would consider every possible sequence of segment flips. Even if we restrict ourselves to only flipping segments that help move toward a target, the number of ways to choose segments is exponential because after each flip the string changes and creates new possible segments. This quickly becomes infeasible beyond very small n.

A more structured brute force would try fixing a target string, either all zeros or all ones, and then simulate a greedy correction. If we sweep left to right, whenever we encounter a mismatch with the target, we flip from that position forward until the mismatch is resolved. This is correct for a fixed target, but still requires reasoning about how many flips are forced.

The key observation is that once we fix a target, the optimal strategy is completely determined by transitions in the string. Suppose we target all zeros. Every time we see a transition `0 → 1`, it means we are entering a segment that must eventually be flipped to fix those ones. Similarly, every transition `1 → 0` marks the end of such a segment. Each continuous block of ones must be flipped exactly once, and each flip can cover an entire block optimally.

Thus, the number of flips needed to convert the string into all zeros is equal to the number of contiguous blocks of ones. Symmetrically, the number of flips needed to convert to all ones equals the number of contiguous blocks of zeros. The answer is simply the minimum of these two values.

The problem reduces from choosing segments dynamically to counting runs in a binary string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the string once and count how many contiguous segments of `'1'` exist. A new segment starts whenever a `'1'` appears and the previous character is not `'1'`. This counts how many isolated groups of ones must be handled if we aim to turn everything into zeros.
2. Scan the string once and count how many contiguous segments of `'0'` exist using the same logic. This represents the number of flips needed if we aim to turn everything into ones.
3. Compare the two counts and output the smaller value. This corresponds to choosing the cheaper of the two possible final uniform states.

Why this works: every flip in an optimal solution can be assumed to cover an entire maximal contiguous segment of identical characters that differ from the target. Splitting a segment into multiple flips never helps, since flipping a larger contiguous region does not increase cost but reduces fragmentation. Therefore each maximal block contributes exactly one necessary operation, and no interactions between separated blocks can reduce this count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_blocks(s, ch):
    cnt = 0
    n = len(s)
    i = 0
    while i < n:
        if s[i] == ch:
            cnt += 1
            while i < n and s[i] == ch:
                i += 1
        else:
            i += 1
    return cnt

def solve():
    n = int(input().strip())
    s = input().strip()

    ones = count_blocks(s, '1')
    zeros = count_blocks(s, '0')

    print(min(ones, zeros))

if __name__ == "__main__":
    solve()
```

The function `count_blocks` computes the number of contiguous runs of a given character. It advances through the string and only increments the counter when it encounters the start of a new block, skipping the rest of that block immediately. This ensures linear traversal.

We compute both the number of one-blocks and zero-blocks because they correspond to the two possible target configurations. The final answer is the minimum, since we are free to choose which uniform state we want to achieve.

A common mistake is attempting to simulate flips explicitly. That is unnecessary because flips never need to overlap in an optimal solution, and the structure of the problem guarantees that block boundaries fully determine the cost.

## Worked Examples

Consider the sample input:

`101001011001`

We compute blocks of ones and zeros.

| index | char | new '1' block? | ones blocks | zeros blocks |
| --- | --- | --- | --- | --- |
| 0 | 1 | yes | 1 | 0 |
| 1 | 0 | - | 1 | 1 |
| 2 | 1 | yes | 2 | 1 |
| 3 | 0 | - | 2 | 2 |
| 4 | 0 | - | 2 | 2 |
| 5 | 1 | yes | 3 | 2 |
| 6 | 0 | - | 3 | 3 |
| 7 | 1 | yes | 4 | 3 |
| 8 | 1 | - | 4 | 3 |
| 9 | 0 | - | 4 | 4 |
| 10 | 0 | - | 4 | 4 |
| 11 | 1 | yes | 5 | 4 |

Final counts are ones = 5 and zeros = 4, so the answer is 4.

This trace shows that the solution is purely tracking transitions and does not depend on actual flip simulation. Each time we re-enter a run of identical characters, we only increment once.

A second example:

Input: `000111000`

| index | char | ones blocks | zeros blocks |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 0 | 1 |
| 3 | 1 | 1 | 1 |
| 4 | 1 | 1 | 1 |
| 5 | 1 | 1 | 1 |
| 6 | 0 | 1 | 2 |
| 7 | 0 | 1 | 2 |
| 8 | 0 | 1 | 2 |

Answer is min(1, 2) = 1.

This confirms that a single flip can fix a single contiguous middle block when choosing the appropriate target.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited at most once in each scan |
| Space | O(1) | Only counters and indices are stored |

The solution easily fits within limits since it performs a constant number of linear passes over the string, requiring no additional memory proportional to input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def count_blocks(s, ch):
        cnt = 0
        i = 0
        n = len(s)
        while i < n:
            if s[i] == ch:
                cnt += 1
                while i < n and s[i] == ch:
                    i += 1
            else:
                i += 1
        return cnt

    n = int(input().strip())
    s = input().strip()
    return str(min(count_blocks(s, '1'), count_blocks(s, '0')))

# provided sample
assert run("12\n101001011001\n") == "4"

# all equal ones
assert run("5\n11111\n") == "0"

# all equal zeros
assert run("5\n00000\n") == "0"

# alternating
assert run("4\n0101\n") == "2"

# single character
assert run("1\n0\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | 0 | already uniform requires no flips |
| all zeros | 0 | symmetric base case |
| alternating | 2 | worst-case fragmentation |
| single char | 0 | minimum boundary handling |

## Edge Cases

A string like `11111` has no internal transitions. The algorithm counts one block of ones and zero blocks of zeros as zero. The minimum is zero, matching the fact that no flips are needed.

For `010101`, every character alternates, producing three one-blocks and three zero-blocks. The algorithm correctly returns three, reflecting that each isolated character requires its own correction under any target choice.

For a pattern like `000111000`, the middle segment is the only one that differs from a chosen target of all zeros. The algorithm counts a single one-block, correctly capturing that one flip can cover the entire middle region in one operation.
