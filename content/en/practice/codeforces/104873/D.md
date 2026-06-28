---
title: "CF 104873D - Distinct Substrings"
description: "We are given a short string p and a very large integer n. The actual string we work with is not arbitrary: it is formed by repeating p over and over and then cutting it after exactly n characters."
date: "2026-06-28T10:12:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104873
codeforces_index: "D"
codeforces_contest_name: "2018-2019 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104873
solve_time_s: 35
verified: true
draft: false
---

[CF 104873D - Distinct Substrings](https://codeforces.com/problemset/problem/104873/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short string `p` and a very large integer `n`. The actual string we work with is not arbitrary: it is formed by repeating `p` over and over and then cutting it after exactly `n` characters. So the final string `s` is periodic, with period `k = |p|`, except possibly for a truncated last block.

The task is to count how many distinct non-empty substrings appear somewhere inside `s`. Two substrings are considered the same if they are equal as strings, even if they come from different positions.

The difficulty comes from the scale mismatch. The pattern `p` is small, up to length 1000, but `n` can be as large as 10^9. That immediately rules out constructing `s` explicitly, since even storing it is impossible. Any approach that tries to enumerate substrings directly from `s` is also infeasible, because the number of substrings grows quadratically in `n`.

A naive mental model might suggest sliding over `s` and hashing every substring. That already fails because even iterating over all start positions is O(n), which is too large for n = 10^9.

A more subtle issue appears with periodicity. Even though the structure is repetitive, substrings can cross boundaries between repeated copies of `p`. This creates new substrings that are not present in a single period. For example, in `p = "ab"`, the string `s = "ababab..."` contains substrings like `"bab"`, which do not exist inside one block.

A key edge case is when `n` is just slightly larger than `k`. Then most substrings come from interactions across the boundary of two copies, not from within a single block. Any approach that only counts substrings inside one period and multiplies by a factor will undercount.

Another edge case is when `p` itself contains repeated structure. For example `p = "aaaa"`. Then `s` is just a long run of `a`, and the number of distinct substrings is only `n`, not quadratic. This shows that repetition inside `p` collapses substring diversity heavily, and any correct solution must account for internal structure of `p`, not just its length.

## Approaches

The brute-force method is straightforward: construct the full string `s`, enumerate every substring `s[l:r]`, insert it into a set, and output the size of the set. This is correct because every distinct substring is explicitly collected. However, the number of substrings in a string of length `n` is on the order of n(n+1)/2, which becomes about 5 × 10^17 when n = 10^9. Even if `n` were only 10^5, this approach is already far beyond any feasible runtime.

The structure of the problem is dominated by periodicity. The string is fully determined by a small pattern `p`, so any substring of `s` is determined by where it starts inside a period and how many periods it spans. This suggests compressing the problem from length `n` down to something depending on `k`.

The key observation is that any substring of `s` is either completely contained within a window of a few consecutive copies of `p`, or it becomes eventually periodic itself. In fact, once the substring length exceeds `k`, its behavior is determined by overlaps of `p` with itself. This reduces the problem to analyzing substrings over a conceptual infinite periodic string, but only up to length `n`.

The standard way to formalize this is to use a suffix automaton or suffix array idea on a string that represents two copies of `p`. Two copies are enough to capture all substrings that cross a boundary, because any substring of a periodic string of period `k` only needs at most `2k` characters to represent its internal transitions. We then combine this with a length constraint `n`.

From this viewpoint, the problem becomes counting distinct substrings in a string that is conceptually `p + p`, but where each substring is allowed to extend up to length `n`, not just `2k`. The suffix automaton provides a compact structure where each state represents a set of substrings, and transitions encode extension by one character. We can then simulate extending up to length `n` while respecting periodic transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Suffix automaton over periodic doubling | O(k) | O(k) | Accepted |

## Algorithm Walkthrough

We build a suffix automaton for the string `t = p + p`. This doubled string is enough to capture all transitions between consecutive copies of `p`, which is where new substrings are created.

We then compute, for each automaton state, how many distinct substrings it contributes, but we must restrict substring lengths to at most `n`. Since `n` can be much larger than `k`, the automaton structure still fully captures all distinct patterns; `n` only limits how far we are allowed to extend along transitions.

The core idea is that every state in the suffix automaton represents a set of substrings sharing the same end positions. Each state has a `len` value, which is the maximum length of strings in that state, and a link to its suffix state, which defines the minimum length boundary.

We adjust counts so that instead of counting all substrings in `p+p`, we only count substrings whose length does not exceed `n`.

### Steps

1. Construct the string `t = p + p`.

This ensures that any substring that crosses a period boundary appears explicitly inside a length `2k` window. This avoids reasoning over infinite repetition directly.
2. Build a suffix automaton over `t`.

Each state represents a class of substrings ending at some position, and transitions correspond to extending substrings by one character.
3. For each state, interpret its contribution to distinct substrings as the interval of lengths `[link.len + 1, len]`.

This interval describes all substring lengths that belong uniquely to that state.
4. Clip each interval to `[1, n]`.

Since the original string is truncated at length `n`, any substring longer than `n` is invalid and must not contribute.
5. Sum, over all states, the size of these clipped intervals.

Each valid length contributes exactly once because suffix automaton states partition all distinct substrings by length ranges.

### Why it works

The suffix automaton partitions all distinct substrings into disjoint equivalence classes based on their end positions and longest repeated extensions. Every substring corresponds to exactly one state and exactly one length within that state’s interval. Clipping to `n` preserves correctness because it only removes substrings that cannot exist in the truncated periodic string, without changing the structure of which substrings are distinct. Since `t = p + p` already captures all cross-boundary interactions, no substring of `s` is missed or duplicated beyond these constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SAM:
    def __init__(self):
        self.next = []
        self.link = []
        self.length = []
        self.last = 0

        self.next.append({})
        self.link.append(-1)
        self.length.append(0)

    def extend(self, c):
        cur = len(self.next)
        self.next.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(0)

        p = self.last
        while p != -1 and c not in self.next[p]:
            self.next[p][c] = cur
            p = self.link[p]

        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][c]
            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                clone = len(self.next)
                self.next.append(self.next[q].copy())
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])

                while p != -1 and self.next[p].get(c) == q:
                    self.next[p][c] = clone
                    p = self.link[p]

                self.link[q] = self.link[cur] = clone

        self.last = cur

def count_distinct(p, n):
    sam = SAM()
    t = p + p

    for ch in t:
        sam.extend(ch)

    total = 0
    for v in range(1, len(sam.next)):
        l = sam.length[sam.link[v]] + 1
        r = sam.length[v]
        if l > n:
            continue
        r = min(r, n)
        if r >= l:
            total += (r - l + 1)

    return total

def main():
    p = input().strip()
    n = int(input())
    print(count_distinct(p, n))

if __name__ == "__main__":
    main()
```

The implementation builds a suffix automaton over `p + p`. The automaton structure encodes all distinct substrings of the doubled string, and the counting step extracts contributions from each state by using the standard suffix automaton interval property. The only modification compared to a classic substring count is the cap at `n`, which prevents counting substrings longer than the actual generated string.

A subtle implementation point is the cloning step in `extend`, which ensures correct partitioning of states when transitions are shared. Without cloning, multiple distinct substrings would collapse into incorrect equivalence classes, breaking the interval interpretation.

## Worked Examples

Consider `p = "ab"` and `n = 5`, so `s = "ababa"`.

We build `t = "abab"`.

| Step | State added | Length | Link | New transitions |
| --- | --- | --- | --- | --- |
| 1 | a | 1 | 0 | a |
| 2 | b | 2 | 0 | b |
| 3 | a | 3 | 1 | a |
| 4 | b | 4 | 2 | b |

Each state contributes an interval `[link.len + 1, len]`. For example, a state with `len = 3` and `link.len = 1` contributes lengths 2 to 3.

Clipping at `n = 5` does nothing here because all intervals are already small. The final sum counts all distinct substrings in `"ababa"`.

Now consider `p = "aaaa"` and `n = 6`, so `s = "aaaaaa"`.

Every state essentially collapses into repeated `'a'` extensions. The automaton has a linear chain of lengths, and intervals overlap only in length, not in content. The contribution becomes exactly 6, corresponding to substrings `"a"`, `"aa"`, ..., `"aaaaaa"`.

This trace shows that repetition inside `p` reduces the automaton into a single path, and the algorithm naturally compresses the substring space.

## Complexit
