---
title: "CF 235C - Cyclical Quest"
description: "We are given one large text string s, then many query strings x. For every query, we must count how many substrings of s are rotations of x. If x = \"abcd\", then all of these strings are considered equivalent: abcd, bcda, cdab, dabc."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 235
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 146 (Div. 1)"
rating: 2700
weight: 235
solve_time_s: 175
verified: true
draft: false
---

[CF 235C - Cyclical Quest](https://codeforces.com/problemset/problem/235/C)

**Rating:** 2700  
**Tags:** data structures, string suffix structures, strings  
**Solve time:** 2m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one large text string `s`, then many query strings `x`. For every query, we must count how many substrings of `s` are rotations of `x`.

If `x = "abcd"`, then all of these strings are considered equivalent:

`abcd`, `bcda`, `cdab`, `dabc`.

For each query, we are not checking whether `x` itself appears in `s`. We are checking whether _any rotation_ of `x` appears as a substring of `s`.

The constraints completely determine the shape of the solution. The main string can have length up to `10^6`, and the total length of all queries is also up to `10^6`. A quadratic algorithm is impossible. Even an `O(|s| * |x|)` matcher per query would explode immediately.

Suppose we tried checking every substring of `s` against every rotation of a query. A single query of length `10^5` has `10^5` rotations, and each comparison costs another `10^5`. That is already around `10^10` operations for one query alone.

The problem is really asking for very fast substring frequency queries over all cyclic shifts of a pattern. That strongly suggests preprocessing the main string into a suffix structure.

There are several subtle edge cases that break naive implementations.

Consider:

```
s = aaaa
x = aa
```

The rotations of `"aa"` are not distinct. There is only one unique rotation. The correct answer is `3`, not `6`. A careless implementation that independently counts every rotation would double count the same substring.

Another dangerous case is:

```
s = abcabc
x = abc
```

The rotations are:

`abc`, `bca`, `cab`.

All three appear, but occurrences overlap heavily. We still count occurrences normally:

`abc` appears twice,

`bca` appears once,

`cab` appears once.

Total answer is `4`.

A naive deduplication strategy based only on hashing can also fail if rotations repeat periodically.

For example:

```
x = ababab
```

Rotating by 2 gives the same string again. There are only two distinct rotations, not six.

Finally, queries longer than `s` must immediately return `0`. Some suffix-array traversals accidentally walk past boundaries and count invalid matches if this condition is forgotten.

## Approaches

The brute-force idea is straightforward. For every query string `x`, generate all rotations of `x`. For every rotation, scan the entire string `s` and count occurrences.

This works logically because every valid answer is exactly one substring equal to one cyclic shift of `x`.

The problem is the running time. If `|s| = 10^6` and `|x| = 10^5`, then generating all rotations already costs `10^10` total character work. Matching each rotation against `s` makes it even worse.

We need to avoid two separate inefficiencies.

First, matching substrings repeatedly against `s`.

Second, generating and processing duplicate rotations.

The key observation is that every rotation of `x` appears as a substring of `x + x`.

For example:

```
x = abcd
x + x = abcdabcd
```

Every length-4 substring starting in the first four positions is one cyclic shift.

That transforms the problem into:

Count occurrences in `s` of every length-`m` substring of `x + x`, where `m = |x|`.

Now we need a structure that can answer substring frequency queries quickly.

A suffix automaton is perfect here.

A suffix automaton of `s` compactly stores all substrings of `s`. After building it once, we can walk any pattern through the automaton in linear time. Every state also stores how many times the represented substrings occur in `s`.

The remaining challenge is avoiding duplicate rotations.

Suppose `x = aaaa`. All rotations are identical. If we simply iterate all windows in `x + x`, we would count the same substring multiple times.

We solve this by inserting all rotations into a set using rolling hash or another uniqueness method. Only distinct rotations contribute to the answer.

The final complexity becomes linear in the total input size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(\|s\| · Σ\|x\|²) | O(\|x\|) | Too slow |
| Optimal | O(\|s\| + Σ\|x\|) | O(\|s\|) | Accepted |

## Algorithm Walkthrough

1. Build a suffix automaton for the main string `s`.

Every substring of `s` corresponds to some path in the automaton. Each state stores how many end positions belong to it, which lets us recover occurrence counts.
2. Propagate occurrence counts through suffix links.

During construction, every newly added character contributes one occurrence. After construction finishes, process states in decreasing order of length and push counts upward through suffix links.

This makes every state know how many times its substrings appear in `s`.
3. For a query string `x` of length `m`, create `t = x + x`.

Every cyclic shift of `x` appears as a length-`m` substring of `t`.
4. Traverse `t` through the suffix automaton using the standard online matching technique.

Maintain:

`v` = current automaton state

`l` = current matched length

As characters are processed, follow transitions when possible. Otherwise move through suffix links until a valid transition exists.
5. Whenever the current matched length becomes at least `m`, the current window represents one occurrence of some rotation.

The current automaton state may represent substrings longer than `m`. Move upward through suffix links until its parent length becomes smaller than `m`.

Then this state corresponds exactly to the current length-`m` substring.
6. Deduplicate rotations.

Different windows in `x + x` may represent identical rotations. Use rolling hash to store which rotations were already counted.
7. Add the occurrence count of each distinct rotation.

The occurrence count is simply the `cnt` value stored in the corresponding automaton state.

### Why it works

The suffix automaton guarantees that every substring of `s` corresponds to one state interval. After occurrence propagation, the state associated with a substring stores exactly how many times that substring appears in `s`.

Every cyclic shift of `x` appears exactly once as a length-`m` window inside the first `m` positions of `x + x`.

The online traversal over `x + x` maintains the longest suffix currently present in `s`. Restricting the active state to length exactly `m` identifies the automaton state representing the current rotation.

Deduplication guarantees that periodic strings such as `"aaaa"` or `"ababab"` contribute only once per distinct rotation.

Because every valid rotation is processed and every counted substring corresponds to a valid rotation, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

ALPHA = 26
BASE = 911382323
MOD = 10**18 + 3

class SuffixAutomaton:
    def __init__(self, n):
        size = 2 * n

        self.next = [[-1] * ALPHA for _ in range(size)]
        self.link = [-1] * size
        self.length = [0] * size
        self.cnt = [0] * size

        self.size = 1
        self.last = 0

    def extend(self, ch):
        c = ord(ch) - 97

        cur = self.size
        self.size += 1

        self.length[cur] = self.length[self.last] + 1
        self.cnt[cur] = 1

        p = self.last

        while p != -1 and self.next[p][c] == -1:
            self.next[p][c] = cur
            p = self.link[p]

        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][c]

            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                clone = self.size
                self.size += 1

                self.next[clone] = self.next[q][:]
                self.length[clone] = self.length[p] + 1
                self.link[clone] = self.link[q]

                while p != -1 and self.next[p][c] == q:
                    self.next[p][c] = clone
                    p = self.link[p]

                self.link[q] = clone
                self.link[cur] = clone

        self.last = cur

    def build_counts(self):
        max_len = max(self.length[:self.size])

        bucket = [0] * (max_len + 1)

        for i in range(self.size):
            buc
```
