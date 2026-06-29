---
title: "CF 104673D - Journals"
description: "We are given a stack of journals represented by a string of + and -, where each symbol describes the orientation of a journal cover. The stack is read from top to bottom as the string is given."
date: "2026-06-29T09:19:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104673
codeforces_index: "D"
codeforces_contest_name: "2022-2023 CTU Open Contest"
rating: 0
weight: 104673
solve_time_s: 52
verified: true
draft: false
---

[CF 104673D - Journals](https://codeforces.com/problemset/problem/104673/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stack of journals represented by a string of `+` and `-`, where each symbol describes the orientation of a journal cover. The stack is read from top to bottom as the string is given. The goal is to rearrange the stack so that no two adjacent journals have the same sign, meaning the final string must alternate strictly between `+` and `-`.

The allowed operation is structured but effectively gives a powerful transformation. We can remove some prefix from the top of the stack, then take a contiguous block from what remains, reverse that block, and finally put the removed prefix back on top. The key observation is that this allows reversing any contiguous substring of the stack in a single operation.

Since reversing is the only real change, the problem becomes a transformation task: convert the initial binary string into an alternating target string using the minimum number of substring reversals.

The input length is up to $2 \cdot 10^5$, which immediately rules out any solution that tries all substrings or simulates each operation greedily in quadratic time. We need a linear or near-linear strategy.

A subtle point is that there are exactly two valid target configurations: one starting with `+` and one starting with `-`. Both are valid alternating patterns, and we must choose the one requiring fewer operations.

Edge cases that matter are small strings and already-correct strings. For example, input `"+-"` already satisfies the condition, so the answer is zero. For a string like `"++--"`, a naive approach might try to fix local conflicts greedily and overcount operations, even though a single reversal of the middle segment produces `"+-+-"`.

## Approaches

The brute-force view is to treat each state as a string and try all possible substring reversals, performing a BFS over configurations. Each state has $O(n^2)$ neighbors, and even a small depth of exploration becomes infeasible because the number of reachable strings grows explosively. Even if we restrict ourselves to optimal paths, the state space is $2^{2K}$, which is completely unmanageable.

The key insight is that we are not trying to reach an arbitrary configuration but one of two fixed alternating patterns. This removes the need to reason about global structure. Instead, we compare the current string against the target and focus on mismatched positions.

A reversal can correct two boundary mismatches in a single move if we choose its endpoints carefully. Intuitively, whenever two positions are wrong relative to the target, we can pair them and fix both in one reversal. This reduces the problem to counting mismatches and pairing them optimally. Each operation can eliminate at most two mismatches, and a carefully chosen reversal can always achieve this pairing without breaking previously fixed structure.

This leads to a simple reduction: compute mismatches with respect to each of the two alternating targets, and take the better result. The answer becomes the number of mismatches divided by two, rounded up.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| BFS over states | exponential | exponential | Too slow |
| Mismatch pairing | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We solve the problem by evaluating both possible alternating targets and counting how many positions disagree with each.

1. Construct a hypothetical target string starting with `+`, alternating for the full length.

This represents one valid final configuration.
2. Compare the input string with this target and count how many indices differ.

Each differing position represents a journal that is currently in the wrong orientation relative to the goal.
3. Compute the number of operations needed for this target as `(mismatch_count + 1) // 2`.

This comes from the fact that one reversal can fix two mismatched positions when paired correctly.
4. Repeat the same process for the target starting with `-`.
5. Return the minimum value between the two computed results.

### Why it works

The crucial property is that mismatched positions are independent except for pairing through reversals. A single reversal can only meaningfully "pair up" corrections at its endpoints while leaving internal structure consistent with the target pattern. Since every operation can fix at most two mismatches and any single mismatch requires at least one operation, the optimal strategy is equivalent to pairing mismatches as efficiently as possible. Trying both target patterns ensures we do not bias toward the wrong starting parity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    def cost(start_char):
        mismatches = 0
        cur = start_char
        for i in range(n):
            if s[i] != cur:
                mismatches += 1
            cur = '+' if cur == '-' else '-'
        return (mismatches + 1) // 2

    ans1 = cost('+')
    ans2 = cost('-')
    print(min(ans1, ans2))

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the two candidate alternating patterns. The helper function walks through the string once, maintaining what the expected character should be at each position. The mismatch count is accumulated in a single pass, keeping the solution linear.

The expression `(mismatches + 1) // 2` captures the pairing argument: every operation can resolve two incorrect positions, and if one remains unpaired, it requires an additional operation.

## Worked Examples

Consider a simple input like `"+-+-"`. The mismatch count against the same pattern is zero, so no operations are needed.

For a more illustrative case, take `"++--"`.

### Target starting with `+`

| i | s[i] | target | mismatch |
| --- | --- | --- | --- |
| 0 | + | + | 0 |
| 1 | + | - | 1 |
| 2 | - | + | 1 |
| 3 | - | - | 0 |

Mismatch count is 2, so operations needed is 1.

### Target starting with `-`

| i | s[i] | target | mismatch |
| --- | --- | --- | --- |
| 0 | + | - | 1 |
| 1 | + | + | 0 |
| 2 | - | - | 0 |
| 3 | - | + | 1 |

Mismatch count is again 2, giving 1 operation.

This shows the symmetry: both target orientations are equally valid, and the algorithm correctly selects either.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the two target checks scans the string once |
| Space | O(1) | Only counters and a few variables are used |

The solution comfortably handles strings of length up to $2 \cdot 10^5$ because it performs only a constant number of linear passes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    s = input().strip()
    n = len(s)

    def cost(start):
        mismatches = 0
        cur = start
        for i in range(n):
            if s[i] != cur:
                mismatches += 1
            cur = '+' if cur == '-' else '-'
        return (mismatches + 1) // 2

    return str(min(cost('+'), cost('-')))

# provided-style samples
assert run("+-+-\n") == "0"
assert run("++--\n") == "1"

# custom cases
assert run("+\n") == "0"
assert run("++\n") == "1"
assert run("-+-+\n") == "0"
assert run("++++----\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"+"` | `0` | Single element already valid |
| `"++"` | `1` | Minimal non-trivial correction |
| `"-+-+"` | `0` | Already alternating starting with `-` |
| `"++++----"` | `2` | Larger block structure |

## Edge Cases

For a single-character string like `"+"`, both target patterns are valid up to alternating rule truncation, and the mismatch count is zero, so the algorithm returns zero immediately.

For a string already alternating such as `"+-+-+-"`, the mismatch count is zero against one of the targets, so no operations are needed and the algorithm naturally selects that target.

For a uniform string like `"++++"`, both targets produce two mismatches per two characters, leading to two total mismatches and thus one operation, which corresponds to reversing the middle segment to create alternation.
