---
title: "CF 1167D - Bicolored RBS"
description: "We are given a valid parentheses string. Think of it as a walk that starts at height 0, where every opening bracket increases the height by 1 and every closing bracket decreases it by 1, and the walk never goes negative and ends at 0."
date: "2026-06-13T08:58:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1167
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 65 (Rated for Div. 2)"
rating: 1500
weight: 1167
solve_time_s: 159
verified: true
draft: false
---

[CF 1167D - Bicolored RBS](https://codeforces.com/problemset/problem/1167/D)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a valid parentheses string. Think of it as a walk that starts at height 0, where every opening bracket increases the height by 1 and every closing bracket decreases it by 1, and the walk never goes negative and ends at 0.

The task is to split this single balanced structure into two subsequences, one marked with 0 and the other with 1, without changing order. Each subsequence must itself remain a valid balanced parentheses sequence. So after filtering only characters with label 0 we must still have a correct bracket structure, and the same must hold for label 1.

Among all valid splits, we want to minimize the larger nesting depth of the two resulting sequences. Nesting depth corresponds to the maximum height reached in that subsequence’s own prefix sum view.

The constraint n up to 2×10^5 immediately rules out any approach that tries all partitions or performs nested validation per split. Any solution must be linear or near linear, since O(n log n) is acceptable but O(n^2) is not.

A subtle failure mode appears when one tries to greedily assign brackets based only on local decisions like “alternate colors” or “split by position parity”. For example, in the string “((()))”, alternating colors gives red “(()” and blue “(()”, both invalid because neither preserves balance. Another naive idea is to always assign by current depth parity, but without controlling consistency of push/pop structure, one color can become unbalanced even though total sequence is fine.

The key difficulty is that validity depends on matching opens and closes consistently within each color, not just global structure.

## Approaches

A brute-force idea is to assign each bracket one of two colors in all possible ways and check validity of both induced sequences. There are 2^n assignments, and for each we need linear validation of two bracket sequences, leading to O(n·2^n), which is far beyond limits.

We need to exploit structure of a regular bracket sequence. The key observation is that every opening bracket can be paired with exactly one closing bracket in a canonical matching, and these pairs form a tree-like nesting structure.

The crucial insight is to interpret the sequence as a depth walk. At each position, we know the current depth. The problem reduces to splitting all brackets into two stacks such that each stack independently forms a valid depth walk. The clean way to ensure validity is to guarantee that for each color, every prefix never goes negative, which is equivalent to ensuring that every opening assigned to a color is eventually matched by a closing of the same color in correct order.

This suggests controlling assignment using parity of depth. When we traverse the string, we track current depth before processing each character. If we alternate assignment based on whether depth is odd or even, all brackets at the same nesting level consistently go to the same color. Since nesting structure is perfectly aligned with depth parity, each color inherits a valid non-crossing structure.

This works because depth changes in a structured way: every “(” increases depth before its matching “)” decreases it, so both endpoints of a matched pair share the same parity of depth just before the closing bracket decision. Thus both ends get identical color, preserving balance.

We still have freedom to swap which parity maps to which color, so the maximum depth among both sequences is minimized by balancing assignment across even and odd layers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Depth parity greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We scan the string while maintaining current depth.

1. Initialize depth = 0 and an empty result array.

The depth represents how deeply nested we are before reading each character.
2. For each character in the string:

We decide its color based on current depth parity.
3. If the character is “(”, we assign color = depth % 2, then increase depth by 1.

This ensures all openings at the same structural level go to the same group.
4. If the character is “)”, we first decrease depth by 1, then assign color = depth % 2.

The key is that the closing bracket matches the depth of its corresponding opening structure, so both endpoints receive the same color.
5. Store the assigned color in the output string.
6. After processing all characters, output the constructed color string.

Why it works: each matched pair of parentheses corresponds to a segment of the depth walk that starts at some depth d and returns from d+1 back to d. Both endpoints are assigned using the same depth parity value d, so both ends go to the same color. This guarantees that every matched pair is entirely contained within one subsequence. Since nesting is preserved within parity layers, each color class forms a valid RBS. No invalid interleaving can occur because the depth-based assignment respects the natural stack structure of matching.

## Python Solution

```
PythonRun
```

The solution relies entirely on tracking depth as a structural fingerprint of the bracket tree. The only subtle point is the order of operations for closing brackets: depth must be decreased before computing the parity, otherwise the closing bracket would be assigned to the wrong layer and break pairing consistency.

## Worked Examples

Consider the input “()()”.

We track depth and assignment.

| i | char | depth before | action | depth after | color |
| --- | --- | --- | --- | --- | --- |
| 0 | ( | 0 | assign 0, inc | 1 | 0 |
| 1 | ) | 1 | dec, assign 0 | 0 | 0 |
| 2 | ( | 0 | assign 0, inc | 1 | 0 |
| 3 | ) | 1 | dec, assign 0 | 0 | 0 |

All characters go to one color, producing a valid single RBS and a second empty one.

Now consider “(())”.

| i | char | depth before | action | depth after | color |
| --- | --- | --- | --- | --- | --- |
| 0 | ( | 0 | assign 0, inc | 1 | 0 |
| 1 | ( | 1 | assign 1, inc | 2 | 1 |
| 2 | ) | 2 | dec, assign 1 | 1 | 1 |
| 3 | ) | 1 | dec, assign 0 | 0 | 0 |

We get two sequences: one containing outer layer brackets and one containing inner layer brackets. Each is balanced independently because matching pairs share the same assigned color.

This demonstrates how nesting levels are separated cleanly by parity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass through the string |
| Space | O(n) | storing output coloring string |

The algorithm processes each character once and performs constant work per step. With n up to 2×10^5, this fits comfortably within time limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `()` | `11` | smallest valid case |
| `(())` | balanced split | nesting separation |
| `()()` | uniform or stable assignment | sequential structure |
| `((()))` | alternating layers | deep nesting behavior |

## Edge Cases

One edge case is a completely flat structure like “()()()”. In this case depth parity never changes in a way that creates separation, so all brackets may end up in one group. The algorithm handles this correctly because a single valid RBS is allowed and yields nesting depth 1 for the other empty group.

Another edge case is maximal nesting like “((((...))))”. Here every level alternates color consistently, and each color forms a perfectly nested independent chain. The depth-based assignment ensures that no pair is split across colors, since both endpoints of each pair share identical parity assignment derived from their structural depth transition.
