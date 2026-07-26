---
title: "CF 102803E - Everybody Lost Somebody"
description: "We are given a permutation describing the lexicographic order of all suffixes of an unknown string. We also receive some values of the LCP array between neighboring suffixes in that order. Some LCP values were deleted and replaced by -1."
date: "2026-07-26T16:22:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102803
codeforces_index: "E"
codeforces_contest_name: "The 15th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102803
solve_time_s: 48
verified: false
draft: false
---

[CF 102803E - Everybody Lost Somebody](https://codeforces.com/problemset/problem/102803/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation describing the lexicographic order of all suffixes of an unknown string. We also receive some values of the LCP array between neighboring suffixes in that order. Some LCP values were deleted and replaced by `-1`. The task is to rebuild the lexicographically smallest string that could have produced this suffix array and all the known LCP values.

The suffix array tells us much more than just an ordering. If two neighboring suffixes in the suffix array have a known LCP value `h`, their first `h` characters must be identical. If both suffixes continue after those `h` characters, then the next character of the smaller suffix must be strictly smaller than the next character of the larger suffix. These are the only direct restrictions we need to satisfy, because making every neighboring pair appear in the required order automatically fixes the whole suffix array.

The length is at most 5000 for a single test case, and the sum of all lengths is at most `4.1 * 10^4`. This rules out trying every possible string or repeatedly comparing many candidate strings. A solution around quadratic time per test case is acceptable, but a cubic approach is not. The alphabet is fixed to 26 lowercase letters, which allows us to use greedy character assignment instead of expensive search.

There are several traps that a direct implementation can miss. If a height value is zero, the two suffixes must start with different characters, not just fail to be merged. For example, if the suffix order is `[1,2]` for the string `"ab"`, the known height is `0` and the answer must be `"ab"`, not `"aa"`.

If a suffix is completely contained as a prefix of another suffix, the LCP value does not create a character inequality after it ends. For example, the string `"aa"` has suffixes `"a"` and `"aa"`. Their LCP is `1`, but there is no second character comparison to enforce.

Another common mistake is assigning letters according to suffix array order. The output string is ordered by original positions, so the earliest occurrence of an equivalence class in the original string determines the greedy choice. The suffix array is only used to create constraints.

## Approaches

A brute force solution could try to construct strings in lexicographic order and compute their suffix arrays until one matches the input. This is correct because the first matching string would be the smallest answer, but the search space is `26^n`, which is impossible even for very small strings.

A more reasonable attempt is to recover all equality relations first. Every known LCP value says that two ranges of the original string are equal. After applying those equalities, every position belongs to some equivalence class. The remaining task is to assign one character to each class.

The key observation is that the remaining restrictions are only comparisons between classes. If two classes have a relation `A < B`, the assigned character of `A` must be smaller than the assigned character of `B`.

Now process the original string from left to right. When the first occurrence of a class is reached, its character has to be chosen. Classes that appeared earlier are already fixed, so we only need to respect the lower and upper bounds created by already assigned neighbors. Choosing the smallest possible character is always optimal. Any future class depending on this class can adapt by choosing a larger character later.

The equality constraints are handled with a disjoint set union structure. The comparison constraints form a directed acyclic graph because they come from a valid suffix array, so the greedy character assignment cannot get stuck.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(26^n)` | `O(n)` | Too slow |
| Equality DSU + greedy assignment | `O(n^2)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Create a disjoint set union structure over the `n` positions. For every known height value between two neighboring suffixes, merge the corresponding characters inside the common prefix. If the height is `h`, positions `sa[i-1] + k` and `sa[i] + k` are equal for every `0 <= k < h`.

The DSU groups exactly those positions that must contain the same character.

1. Compress every position to its DSU representative. The representatives become the variables that need assigned characters.
2. For every known height value, check the first characters after the common prefix. If both suffixes still have characters remaining, add a directed edge from the smaller suffix character class to the larger suffix character class.

This creates the constraints of the form `classA < classB`.

1. Scan positions from left to right. When a class is seen for the first time, compute the smallest letter that is larger than every already assigned predecessor and smaller than every already assigned successor.

The first occurrence of a class matters because that is the earliest place where changing its letter affects the final string.

1. Replace every position by the character of its class and output the resulting string.

Why it works:

The DSU step never merges positions that are allowed to differ. Every merge comes from a required common prefix. The graph step records every forced character comparison between neighboring suffixes. Since neighboring suffixes determine the complete suffix array order, satisfying all these comparisons gives exactly the required order.

During greedy assignment, when a class receives a letter, all constraints involving already assigned classes are checked. Constraints involving future classes can always be satisfied by assigning them later because the algorithm chooses the smallest available letter, leaving as much room as possible above it. Therefore the produced string is the smallest possible one.

## Python Solution

The complete implementation and the remaining sections continue in the next message.
