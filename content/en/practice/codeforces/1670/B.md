---
title: "CF 1670B - Dorms War"
description: "We are given a string that represents a password and a set of special characters. A transformation program can be applied repeatedly to the string."
date: "2026-06-10T01:41:38+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1670
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 788 (Div. 2)"
rating: 1100
weight: 1670
solve_time_s: 45
verified: false
draft: false
---

[CF 1670B - Dorms War](https://codeforces.com/problemset/problem/1670/B)

**Rating:** 1100  
**Tags:** brute force, implementation, strings  
**Solve time:** 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string that represents a password and a set of special characters. A transformation program can be applied repeatedly to the string. Each run looks at every position and marks those positions whose immediate right neighbor is a special character, then deletes all marked positions simultaneously.

The deletion rule is purely local: a character disappears if the character directly after it belongs to the special set. After deletion, the string shrinks and the same rule can be applied again to the new string. The process stops when an application of the rule would delete nothing, because that triggers an error.

The task is to compute how many successful deletions can be performed before reaching a state where no deletion is possible.

The constraints allow up to 100,000 characters per test case and up to 200,000 characters total. This immediately rules out any simulation that scans and rebuilds the string in each round, since in the worst case a single test case could degrade into quadratic behavior by repeatedly shrinking one character at a time.

A key subtlety is that deletions are simultaneous. A naive approach that removes characters one by one or that tries to mutate the string while iterating can easily mis-handle shifting indices. For example, in a string like `"ababa"` with `'b'` as special, the first round removes both `'a'` positions before `'b'`, and after recomputation the structure changes in a way that depends on all removals happening at once.

Another pitfall is assuming a single pass or greedy removal is enough. Each round depends on the updated adjacency structure, so the effect is iterative, but the number of iterations is what we must compute efficiently.

## Approaches

A direct simulation would repeatedly scan the string, mark deletable positions, build a new string, and repeat. Each scan is O(n), and in the worst case we remove only one character per iteration, leading to O(n²) time. With 2×10⁵ total characters, this is too slow.

The key observation is that we do not actually need to simulate every intermediate string. Each character effectively “waits” until a special character appears to its right in the current surviving structure. Once a character is removed, it can expose new adjacency relationships, but we can think in reverse: every character survives until it is blocked by a special character that is still to its right at that stage.

A more useful perspective is to process from right to left while tracking how “far” a deletion wave can propagate. The process behaves like repeated removal of characters that lie immediately before any special character in the current active suffix. Each round pushes the boundary of influence leftwards by skipping over blocks until it reaches a position where no special character remains to the right.

This reduces the problem to repeatedly counting how many characters can be removed before reaching a stable prefix where no special characters exist to the right of any remaining deletable position. The number of iterations is exactly how many ti
