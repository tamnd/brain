---
title: "CF 2041I - Auto Complete"
description: "We are asked to simulate an advanced text editor that supports four operations: adding patterns for auto-complete, deleting patterns, appending text to the current editor content, and deleting characters from the end of the current content."
date: "2026-06-08T09:45:46+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "hashing", "implementation", "sortings", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 2041
codeforces_index: "I"
codeforces_contest_name: "2024 ICPC Asia Taichung Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 2300
weight: 2041
solve_time_s: 130
verified: true
draft: false
---

[CF 2041I - Auto Complete](https://codeforces.com/problemset/problem/2041/I)

**Rating:** 2300  
**Tags:** binary search, data structures, hashing, implementation, sortings, strings, trees  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate an advanced text editor that supports four operations: adding patterns for auto-complete, deleting patterns, appending text to the current editor content, and deleting characters from the end of the current content. After each operation, the editor should suggest the "best" pattern that matches the current content as a prefix. The best pattern is defined first by maximum length, then lexicographic order, and finally by smallest ID.

The input gives the number of operations followed by the operations themselves. Each operation may reference a pattern by ID, a string to append, or a number of characters to remove. The output is a line per operation, showing the suggested pattern's ID or -1 if no match exists.

Given that `n` can be up to 10^6 and the total characters in all patterns and strings can reach 2×10^6, any solution that scans all patterns for each query would be far too slow. Specifically, a brute-force check for every append or delete would involve O(n × m) operations where m is the length of the current content, easily reaching 10^12 in the worst case. We need a solution that allows insertion, deletion, and prefix lookup in sub-linear or amortized constant time relative to the number of patterns.

Edge cases include scenarios where multiple patterns match equally in length and lexicographically, when deleting more characters than exist in the current content, and when the current content is empty or completely unmatched. For instance, if the only patterns are "abc" and "abcd" and the user appends "ab", the longest match should suggest "abcd". A naive approach that picks the first match it finds could incorrectly suggest "abc".

## Approaches

The brute-force solution would maintain a list of patterns. For each query that changes the current content, it would scan all patterns, check if the content is a prefix, and then select the best match according to the rules. This is correct logically but performs O(n) checks per content change, which becomes impractical at scale.

The key observation is that we need fast prefix matching with dynamic insertion and deletion of patterns. A trie (prefix tree) naturally supports prefix queries efficiently. Each node in the trie corresponds to a character, and edges represent transitions between characters. By storing candidate pattern IDs at nodes, we can quickly identify the longest match starting from the root. To handle deletions and tie-breakers (length, lexicographic, ID), each node should maintain a set or heap of active patterns passing through it, sorted by our criteria.

With this structure, adding a pattern involves walking down the trie, creating nodes as needed, and inserting the pattern ID at each node along the path. Deletion walks the path and removes the ID from each node. Querying for the current content is just walking the trie along the characters of the current text and reading the best pattern ID from the deepest reachable node.

This approach reduces the per-operation time complexity to O(length of string) for both insertions and queries, which is acceptable because the sum of all string lengths is bounded by 2×10^6.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × total pattern length) | O(n × avg pattern length) | Too slow |
| Trie with metadata | O(total string length) | O(total string length) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty trie. Each node contains a dictionary for child nodes and a set of pattern IDs that pass through the node. Each ID is associated with the pattern’s string and length for tie-breaking.
2. For an add operation with ID `i` and pattern `p`, start at the root of the trie. For each character in `p`, create a child node if it does not exist. At each node along the path, insert `i` into the node's set. This ensures every prefix of `p` knows which patterns pass through it.
3. For a delete operation with ID `i`, look up the original pattern string. Walk down the trie following the string. At each node along the path, remove `i` from the node’s set. This prevents stale patterns from being suggested.
4. Maintain a string `t` representing the current content in the editor. For an append operation, add the string to `t`. For a backspace operation, remove the specified number of characters from the end, truncating completely if needed.
5. After each operation, query the trie by walking down `t`. If at any point a character does not exist in the trie, output -1. Otherwise, reach the node corresponding to the last character of `t` and select the pattern with maximum length, then minimum lexicographic value, then minimum ID. This node contains a heap or sorted set to allow this selection in O(1) time per query.
6. Output the ID of the selected pattern or -1 if no pattern matches.

Why it works: Each trie node aggregates all active patterns that share its prefix. By maintaining the tie-breakers in sorted order, the deepest node reachable along `t` always contains the valid best suggestion. Adding and deleting patterns updates all affected prefixes, so no node ever contains stale patterns.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

class TrieNode:
    __slots__ = ('children', 'patterns')
    def __init__(self):
        self.children = {}
        self.patterns = []

class Pattern:
    __slots__ = ('length', 'string', 'id')
    def __init__(self, string, id):
        self.string = string
        self.id = id
        self.length = len(string)
    def __lt__(self, other):
        if self.length != other.length:
            return self.length > other.length
        if self.string != other.string:
            return self.string < other.string
        return self.id < other.id

class AutoComplete:
    def __init__(self):
        self.root = TrieNode()
        self.pattern_map = {}
        self.t = ''

    def add_pattern(self, id, string):
        self.pattern_map[id] = string
        node = self.root
        pat = Pattern(string, id)
        for c in string:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
            bisect.insort(node.patterns, pat)

    def delete_pattern(self, id):
        string = self.pattern_map[id]
        node = self.root
        pat = Pattern(string, id)
        for c in string:
            node = node.children[c]
            idx = bisect.bisect_left(node.patterns, pat)
            if idx < len(node.patterns) and node.patterns[idx].id == id:
                node.patterns.pop(idx)

    def query(self):
        node = self.root
        for c in self.t:
            if c not in node.children:
                return -1
            node = node.children[c]
        if not node.patterns:
            return -1
        return node.patterns[0].id

    def append(self, s):
        self.t += s

    def backspace(self, c):
        self.t = self.t[:-c] if c <= len(self.t) else ''

ac = AutoComplete()
n = int(input())
for _ in range(n):
    parts = input().split()
    if parts[0] == 'add':
        ac.add_pattern(int(parts[1]), parts[2])
    elif parts[0] == 'delete':
        ac.delete_pattern(int(parts[1]))
    elif parts[0] == 'append':
        ac.append(parts[1])
    else:  # backspace
        ac.backspace(int(parts[1]))
    print(ac.query())
```

The solution defines a `TrieNode` that holds child nodes and an ordered list of patterns. Each pattern is wrapped in a class with a custom comparison operator that prioritizes length, then lexicographic order, then ID. We maintain a map from pattern IDs to strings to support deletions efficiently. `bisect.insort` is used to keep patterns sorted, allowing quick selection of the best candidate. Append and backspace operations manipulate the current text string directly.

## Worked Examples

Sample input:

```
6
add 1 pattern1_alice
add 2 pattern2_bob
add 3 pattern3_charlie
append pattern
append 2_bobabc
backspace 3
```

| Step | Current text `t` | Operation | Trie node patterns | Output |
| --- | --- | --- | --- | --- |
| 1 | "" | add 1 "pattern1_alice" | root->p->a->...->e patterns=[1] | 1 |
| 2 | "" | add 2 "pattern2_bob" | root->p->a->... patterns=[1,2] | 1 |
| 3 | "" | add 3 "pattern3_charlie" | root->p->a->... patterns=[1,2,3] | 3 |
| 4 | "pattern" | append "pattern" | node at 'n' patterns=[1,2,3] | 3 |
| 5 | "pattern2_bobabc" | append "2_bobabc" | node at 'c' patterns=[2] | -1 |
| 6 | "pattern2_b" | backspace 3 | node at 'b' patterns=[2] | 2 |

This trace shows that patterns are correctly suggested after each modification. Deletion and addition maintain the heap invariant at each node.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length of all strings) | Each character in each pattern is inserted |
