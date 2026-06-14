---
title: "CF 1437G - Death DBMS"
description: "We maintain a fixed collection of strings, each representing a “name”, and each name has an associated value that changes over time."
date: "2026-06-14T17:32:15+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "string-suffix-structures", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1437
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 97 (Rated for Div. 2)"
rating: 2600
weight: 1437
solve_time_s: 220
verified: false
draft: false
---

[CF 1437G - Death DBMS](https://codeforces.com/problemset/problem/1437/G)

**Rating:** 2600  
**Tags:** data structures, string suffix structures, strings, trees  
**Solve time:** 3m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We maintain a fixed collection of strings, each representing a “name”, and each name has an associated value that changes over time. The system supports two operations: updating the value of a single name, and querying a text string to find which stored names appear as contiguous substrings, reporting the maximum value among those matches.

A direct reading of a query is: given a text, scan every stored name and check whether it appears inside the text, then take the maximum score among all matches. Since names do not change, only their scores do, the structural challenge is purely about fast substring detection across many patterns with dynamic weights.

The constraints push us into a regime where naive substring checking is impossible. There can be up to 300,000 total characters across all stored names and query strings combined. If we tried checking every name against every query using a substring search, each check would be linear in the query length, producing a worst case around 10^10 operations, which is far beyond limits.

A second naive idea is to precompute all substrings of each query and compare them against a hash set of names. This fails because a single query string of length L has O(L^2) substrings, and L can be large enough that this becomes infeasible even once.

A subtler issue appears when updates happen frequently. Any solution that precomputes answers per query independently cannot reuse structure across queries without also supporting dynamic value updates efficiently.

The key difficulty is that we are repeatedly asking: “among a fixed dictionary of patterns with changing weights, which pattern appears in this text as a substring?”

Edge cases that break naive approaches include repeated names with different indices but shared strings, queries containing overlapping occurrences of multiple names, and updates that reduce a value to zero where the correct answer must still consider it as valid if no negative filtering exists. A particularly subtle case is when no name appears in a query at all, requiring output −1 instead of 0, so initialization must carefully distinguish “no match” from “minimum value match”.

## Approaches

A brute-force solution treats each query independently. For a query string q, we iterate over all names si and check whether si is a substring of q using a standard substring search like Knuth-Morris-Pratt or built-in matching. If a match is found, we take the maximum current value among all matched names.

This approach is correct because it directly implements the definition of the query. However, each query costs O(total length of q × number of patterns) in the worst case. With both sums reaching 3 × 10^5, and up to 3 × 10^5 queries, this becomes impossible.

The observation that changes everything is that we are searching many patterns simultaneously inside a single text. This is exactly the setting for a multi-pattern automaton, specifically the Aho-Corasick automaton. It builds a trie of all names and augments it with failure links so that a single pass over a query string identifies all patterns that appear as substrings in linear time.

The remaining complication is that pattern values are dynamic. We need to support updates to pattern scores and fast queries for the maximum score among all patterns matched during a traversal. This suggests maintaining, for each trie node corresponding to a pattern end, a mutable value and aggregating results through a structure that supports point updates and range maximum queries along failure-link chains.

The standard trick is to propagate each pattern to its terminal node in the automaton, and maintain a segment tree or Fenwick-like structure over an Euler ordering of failure-link tree. Each pattern contributes to exactly one node, and when a query string is processed, every visited automaton state corresponds to a suffix link chain whose nodes represent all matched patterns. We can precompute for each node the list of pattern IDs ending there and maintain a global structure keyed by node entry times to retrieve maximum active values efficiently.

This reduces each query to O(|q| log n), which is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force substring checks | O(m · total pattern length per query) | O(total patterns) | Too slow |
| Aho-Corasick + segment tree on pattern nodes | O((Σ | q | + updates) log n) |

## Algorithm Walkthrough

We first build a trie from all victim names. Each name is inserted character by character, and we store the index of the name at its terminal node. This gives
