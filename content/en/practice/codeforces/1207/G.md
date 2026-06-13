---
title: "CF 1207G - Indie Album"
description: "We are given a sequence of strings that evolve over time. The first string is a single character. Every later string is built by taking an earlier string and appending one new lowercase letter at the end."
date: "2026-06-13T16:21:51+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "hashing", "string-suffix-structures", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1207
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 71 (Rated for Div. 2)"
rating: 2700
weight: 1207
solve_time_s: 159
verified: false
draft: false
---

[CF 1207G - Indie Album](https://codeforces.com/problemset/problem/1207/G)

**Rating:** 2700  
**Tags:** data structures, dfs and similar, hashing, string suffix structures, strings, trees  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of strings that evolve over time. The first string is a single character. Every later string is built by taking an earlier string and appending one new lowercase letter at the end. So each string is literally a growing history of append operations, forming a rooted tree where each node has exactly one parent pointer and one extra character on the edge.

Alongside this construction, we receive queries. Each query asks: inside a particular string version, how many times does a given pattern appear as a contiguous substring.

The difficulty is that both the number of strings and the total length of all patterns are large, so we cannot afford to explicitly construct all strings or scan them for every query.

The constraints force us into roughly linear or near-linear behavior in the total size of input strings and patterns. Any approach that touches each character of a string per query will immediately fail, because in the worst case we would do about $O(n \cdot |t|)$ work per query, which becomes astronomically large when both reach $4 \cdot 10^5$.

A more subtle issue is that strings are not independent. Each string is a suffix-extended version of some earlier string. This creates a tree of strings where long common prefixes appear repeatedly across different nodes. A naive substring search per node would recompute the same prefixes many times.

A typical edge case that breaks naive thinking is when many queries ask for short patterns across very deep nodes. For example, if the tree is a chain of repeated appends of 'a', then every string is “aaaa...”. A naive per-query scan would repeatedly count overlaps without reusing structure.

## Approaches

The brute force idea is straightforward: explicitly build every string, then for each query run a substring counting algorithm like KMP or a rolling hash scan. This is correct because each string is fully materialized, and substring matching is well understood. The problem is that building all strings costs the sum of their lengths, which is already up to $4 \cdot 10^5$, and then each query may scan another string of comparable size. In the worst case, this leads to about $O(n^2)$ total behavior across queries and constructions.

The key observation is that the string construction forms a rooted tree where each node adds exactly one character. Any substring of a node corresponds to a path in this tree ending at that node. Instead of reasoning about strings directly, we can reason about positions in this implicit tree.

If we fix a pattern, we are essentially asking: how many nodes in a rooted tree have an ancestor path ending at that node that matches this pattern. That suggests reversing the perspective: instead of matching pattern inside each string, we match the pattern along suffix chains in the tree.

This becomes a classical use case for building an Aho-Corasick automaton over all query patterns, and then propagating counts through the string construction tree. Each node in the album tree corresponds to a single appended character transition. As we traverse nodes in order, we maintain the automaton state that represents all suffix matches ending at that node. Whenever we land in a state, we increment occurrences of patterns ending there. Then a reverse propagation over suffix links accumulates counts correctly.

The final missing piece is that queries are not just “how many times pattern appears anywhere”, but “how many times pattern appears in a specific prefix-string node”. That is handled by storing, for each
