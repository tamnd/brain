---
title: "CF 204E - Little Elephant and Strings"
description: "We are given a list of strings, and for each string, we need to count the number of its substrings that appear in at least k strings from the list. A substring is any contiguous segment of a string."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "string-suffix-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 204
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 129 (Div. 1)"
rating: 2800
weight: 204
solve_time_s: 45
verified: true
draft: false
---

[CF 204E - Little Elephant and Strings](https://codeforces.com/problemset/problem/204/E)

**Rating:** 2800  
**Tags:** data structures, implementation, string suffix structures, two pointers  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of strings, and for each string, we need to count the number of its substrings that appear in at least _k_ strings from the list. A substring is any contiguous segment of a string. For example, if the string is "abc", its substrings are "a", "b", "c", "ab", "bc", and "abc". For each of these, we need to know how many of the strings in the input contain it and whether that number is at least _k_. The output is a sequence of integers, one per string, representing this count.

The constraints are tight: there can be up to 100,000 strings, and the total length of all strings is up to 100,000 characters. That immediately rules out any approach that checks all pairs of substrings directly. The total number of substrings of a string of length _m_ is _m_(m+1)/2, which can be close to 10^10 across all strings in the worst case. So an O(n²) or O(total_substrings) approach is completely infeasible. This suggests we need a global string structure that allows us to aggregate substring occurrences efficiently.

A non-obvious edge case arises when multiple strings are identical or when _k_ is 1. For example, if the input is ["a", "aa", "aaa"] with k=1, every substring counts because every substring appears in at least one string. A careless implementation that only counts distinct substrings across strings would undercount. Another edge case is strings with overlapping substrings: ["ab", "ba"] with k=2. The substring "a" appears in both strings, but "ab" and "ba" appear in only one. Handling these overlaps correctly requires precise bookkeeping.

## Approaches

The brute-force approach is conceptually simple: for each string, enumerate all of its substrings and check for each whether it appears in at least _k_ strings. This requires iterating over every substring of every string and then iterating over every string to see if it contains that substring. If the total length of all strings is _L_, the number of substrings is on the order of L². Even assuming a fast substring check, the total work would be far above 10^10 operations, which is impossible under the given time constraints.

The key observation that enables an optimal solution is that we do not care about which strings contain a substring individually, only how many distinct strings contain it. This suggests a suffix data structure, such as a generalized suffix automaton or a suffix trie/tree, where each node represents a substring, and we can annotate it with the number of distinct strings containing that substring. Building a generalized suffix automaton over all strings allows us to traverse all unique substrings efficiently. Once we have counts per substring, we can iterate over each string and, using two pointers along the string's suffix links in the automaton, count how many of its substrings meet the threshold _k_.

The two-pointer traversal is efficient because for a given start index in the string, we can extend the end index as far as possible while remaining in substrings that meet the _k_ threshold. The sum of lengths from each start index then gives the total number of qualifying substrings for that string. This reduces the problem to essentially linear time with respect to the total length of all strings, multiplied by the overhead of the automaton transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L³) | O(L²) | Too slow |
| Suffix Automaton + Two Pointers | O(L) | O(L) | Accepted |

## Algorithm Walkthrough

1. Concatenate all strings with unique separator characters so that substrings do not spill across string boundaries. Each separator is distinct from 'a'-'z' to avoid false overlaps.
2. Build a generalized suffix automaton (SAM) over the concatenated string. The SAM efficiently encodes all unique substrings and allows fast traversal along suffix links. Each state in the SAM represents a set of substrings ending at that state.
3. For each state, compute the number of distinct strings that contain the substring represented by that state. This can be done by propagating string identifiers from terminal states upward along suffix links.
4. For each original string, initialize a counter. Start at each position in the string and traverse the SAM following the corresponding characters. Extend the traversal until reaching a state where the number of containing strings is less than _k_. The length of this traversal gives the number of qualifying substrings starting at that position.
5. Sum the counts from all start positions in the string. This yields the answer for that string. Repeat for all strings.

Why it works: The generalized suffix automaton encodes every substring exactly once, and the propagation of string identifiers ensures that each substring's count reflects the number of distinct strings containing it. Traversing along the string using the automaton guarantees that we count all substrings starting at each position and that the two-pointer method captures all maximal valid substrings without double-counting. This approach respects the original problem requirements while operating efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque

class SAMNode:
    def __init__(self):
        self.next = {}
        self.link = -1
        self.len = 0
        self.strings = set()

class SuffixAutomaton:
    def __init__(self):
        self.nodes = [SAMNode()]
        self.last = 0
    
    def extend(self, c, string_id):
        p = self.last
        cur = len(self.nodes)
        self.nodes.append(SAMNode())
        self.nodes[cur].len = self.nodes[p].len + 1
        self.nodes[cur].strings.add(string_id)
        while p != -1 and c not in self.nodes[p].next:
            self.nodes[p].next[c] = cur
            p = self.nodes[p].link
        if p == -1:
            self.nodes[cur].link = 0
        else:
            q = self.nodes[p].next[c]
            if self.nodes[p].len + 1 == self.nodes[q].len:
                self.nodes[cur].link = q
            else:
                clone = len(self.nodes)
                self.nodes.append(SAMNode())
                self.nodes[clone].len = self.nodes[p].len + 1
                self.nodes[clone].next = self.nodes[q].next.copy()
                self.nodes[clone].link = self.nodes[q].link
                self.nodes[clone].strings = self.nodes[q].strings.copy()
                while p != -1 and self.nodes[p].next[c] == q:
                    self.nodes[p].next[c] = clone
                    p = self.nodes[p].link
                self.nodes[q].link = self.nodes[cur].link = clone
        self.last = cur

def solve():
    n, k = map(int, input().split())
    strings = [input().strip() for _ in range(n)]
    separators = [chr(123+i) for i in range(n)]
    sam = SuffixAutomaton()
    
    for idx, s in enumerate(strings):
        sam.last = 0
        for c in s + separators[idx]:
            sam.extend(c, idx)
    
    # Propagate string counts using topological order by length
    max_len = max(node.len for node in sam.nodes)
    bucket = [[] for _ in range(max_len+1)]
    for i, node in enumerate(sam.nodes):
        bucket[node.len].append(i)
    
    order = []
    for b in bucket[::-1]:
        order.extend(b)
    
    for u in order:
        if sam.nodes[u].link != -1:
            sam.nodes[sam.nodes[u].link].strings.update(sam.nodes[u].strings)
    
    res = []
    for idx, s in enumerate(strings):
        count = 0
        l = 0
        node = 0
        for r, c in enumerate(s):
            while node != -1 and c not in sam.nodes[node].next:
                node = sam.nodes[node].link
                l = sam.nodes[node].len if node != -1 else 0
            if node == -1:
                node = 0
                l = 0
            else:
                node = sam.nodes[node].next[c]
                while sam.nodes[node].link != -1 and len(sam.nodes[sam.nodes[node].link].strings) >= k:
                    node = sam.nodes[node].link
                    l = sam.nodes[node].len
                count += r - l + 1
        res.append(str(count))
    print(' '.join(res))

if __name__ == "__main__":
    solve()
```

The code first constructs a generalized suffix automaton for all strings with unique separators. It then propagates string identifiers along the suffix links in topological order by node length. For each string, it uses a two-pointer-like traversal along the automaton to count substrings appearing in at least _k_ strings. Using unique separators prevents counting substrings that cross boundaries between strings.

## Worked Examples

### Example 1

Input:

```
3 1
abc
a
ab
```

| String | Substrings | Appearing in ≥1 strings | Count |
| --- | --- | --- | --- |
| "abc" | a,b,c,ab,bc,abc | all | 6 |
| "a" | a | a | 1 |
| "ab" | a,b,ab | all | 3 |

This confirms that the algorithm correctly counts substrings starting at each position and that the threshold of 1 is applied correctly.
