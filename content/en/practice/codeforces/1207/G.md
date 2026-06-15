---
title: "CF 1207G - Indie Album"
description: "We are given a growing collection of strings, where each new string is either a single character or an old string extended by exactly one character at the end."
date: "2026-06-15T17:48:26+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "hashing", "string-suffix-structures", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1207
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 71 (Rated for Div. 2)"
rating: 2700
weight: 1207
solve_time_s: 250
verified: false
draft: false
---

[CF 1207G - Indie Album](https://codeforces.com/problemset/problem/1207/G)

**Rating:** 2700  
**Tags:** data structures, dfs and similar, hashing, string suffix structures, strings, trees  
**Solve time:** 4m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a growing collection of strings, where each new string is either a single character or an old string extended by exactly one character at the end. This means the entire system forms a rooted tree: every string points to its parent (the string it was built from), and each edge appends one character.

For each query, we are asked to take one of these strings and count how many times another string appears as a contiguous substring inside it.

The key difficulty is that strings are not given explicitly in full. Some of them can be extremely long, and many queries can refer to the same or overlapping prefixes of this implicit tree. Since total input size is large, any approach that explicitly constructs all strings or scans them per query is immediately infeasible.

The constraints imply up to 400,000 nodes and 400,000 queries, with total query length also bounded by 400,000. A naive substring search per query would behave like $O(n \cdot |t|)$ in the worst case, which is far beyond limits.

A subtle issue arises from reuse of structure. Many strings share long prefixes because each is formed by appending one character. For example, if string 10 is built from string 5, then string 10 contains everything in 5 plus one extra character. Any solution must exploit this reuse rather than reconstructing or scanning from scratch.

Another pitfall is treating each string independently. If we store strings explicitly, memory and time blow up. Even hashing all substrings per node is too large because a string of length L has O(L²) substrings.

## Approaches

A brute force method would construct every string explicitly and then, for each query, scan the target string and count matches of the pattern using a sliding window. This is correct logically but fails because a single string can be very long, and there can be many queries. Even with KMP, each query costs $O(|s_i| + |t|)$, and since both can be large across many queries, the total worst case becomes quadratic in total length.

The key structural observation is that all strings form a tree where each node differs from its parent by one appended character. This means every string corresponds to a path from the root, and substrings correspond to paths in this tree that are not necessarily root-aligned but still continuous segments.

Instead of treating strings as flat sequences, we reinterpret the entire construction as a trie-like structure augmented with suffix links. The natural direction is to build an Aho-Corasick automaton over all query strings, because queries are fixed patterns, and then scan each generated string once through the automaton.

However, scanning each full string individually is still too expensive. The crucial improvement is to observe that the constructed strings form a tree with parent pointers, so we can traverse this tree while maintaining the automaton state, accumulating pattern occurrences as we go. This turns substring counting into a propagation problem over the tree of strings.

Each node carries a character transition from its parent. We maintain for every node the current automaton state reached after reading its string, and we propagate contributions using DFS over the construction tree. Each time we enter a node, we update how many query patterns end at that automaton state.

This reduces repeated scanning and ensures each node is processed once, while automaton transitions handle all pattern matching efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force scan per query | (O(n \cdot | t | )) |
| Tree + Aho-Corasick + DFS propagation | (O(n + \sum | t | )) |

## Algorithm Walkthrough

We separate the problem into two interacting structures: the tree of songs and the automaton built from all query patterns.

1. Build the Aho-Corasick automaton from all query strings. Each query string is inserted into the trie, and each terminal node stores which queries end there. We then compute suffix links so that every node knows where to fall back when a character transition fails.
2. For each automaton node, compute its output list by merging its own matches with those of its suffix link. This ensures that when we reach a state, we immediately know which query patterns end there.
3. Build the tree of songs. Each node i stores its parent j (if it is type 2) and its appended character.
4. Perform a DFS over the song tree while simultaneously maintaining the automaton state corresponding to the current string.
5. At the root, start with the automaton in the initial state (empty string). For each node, transition using its character from the parent state.
6. When entering a node, we are effectively at the end of its full string. We iterate over all patterns that end in the current automaton state and increment their answer counters.
7. Recurse into children, passing the updated automaton state.

The subtle point is that the automaton state always represents the suffix structure of the current string. This avoids recomputing matches for overlapping substrings because suffix links implicitly encode all possible fallback matches.

### Why it works

At every node in the DFS, the automaton state corresponds exactly to the set of all suffixes of the current string that match prefixes of any query pattern. Every occurrence of a pattern ending at that node must correspond to one of these automaton states. Because Aho-Corasick merges suffix contributions, every match is counted exactly once when the DFS visits the node where the pattern ends.

## Python Solution

```
PythonRun
```

The construction phase builds a standard Aho-Corasick automaton over all query strings. Each node in the automaton stores which patterns end there, and suffix links merge occurrences so that a single state already represents all matched patterns ending at that position.

The DFS walks through the song construction tree. The key implementation detail is that the automaton state is threaded through recursion rather than recomputed per node. Each node transition is a single character extension of its parent state, with fallback via suffix links when needed.

A common pitfall is forgetting to propagate output along suffix links. Without merging `out[link[u]]` into `out[u]`, many matches are missed because patterns ending in suffix states would not be counted at deeper nodes.

## Worked Examples

### Example 1 (simplified)

Consider a chain of strings: `a → ab → aba`, and a query asking for pattern `"aba"` in the last node.

At each DFS step, we track automaton state:

| Node | String | State transition | Matches found |
| --- | --- | --- | --- |
| 1 | a | goto 'a' | none |
| 2 | ab | 'a' → 'b' | none |
| 3 | aba | 'ab' → 'a' | pattern ends |

This shows that matches only appear when the automaton state reaches a terminal node, not necessarily at every step.

### Example 2 (overlapping patterns)

Strings: `a → aa → aaa`, pattern `"aa"`.

| Node | String | State | Matches |
| --- | --- | --- | --- |
| 1 | a | "a" | 0 |
| 2 | aa | "aa" | 1 |
| 3 | aaa | "aaa" | 2 |

This demonstrates that overlapping occurrences are naturally handled by automaton suffix propagation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n + \sum | t |
| Space | (O(n + \sum | t |

The solution fits comfortably because both total song construction and total query length are bounded by 400,000, making linear-time processing feasible.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single node | 0/1 cases | base correctness |
| chain repetition | multiple overlaps | suffix propagation |
| repeated pattern queries | accumulation | query grouping |

## Edge Cases

One important edge case is when multiple patterns share long suffixes. For example, patterns `"a"`, `"aa"`, `"aaa"` all end at overlapping automaton states. Without suffix merging in `out[]`, only the deepest pattern would be counted, while shorter ones would be missed even though they occur at every position.

Another edge case arises when a song is built by repeatedly appending the same character. In this case, automaton transitions repeatedly hit fallback links, and correctness depends on correctly chaining suffix transitions. If fallback is not handled, states become incorrect and substring counts collapse.

Both cases are handled because every automaton state inherits outputs from its suffix link, ensuring that every valid pattern occurrence is registered exactly at the node where its last character is processed.
