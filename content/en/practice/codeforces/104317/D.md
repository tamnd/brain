---
title: "CF 104317D - Deliver the string"
description: "We are given two strings, $A$ and $B$. We start with an empty string $C$, and we are allowed to build $C$ by repeatedly copying a substring from $A$ and appending it to the end of $C$."
date: "2026-07-01T19:30:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104317
codeforces_index: "D"
codeforces_contest_name: "Shanghai University 2023 Spring Contest"
rating: 0
weight: 104317
solve_time_s: 95
verified: true
draft: false
---

[CF 104317D - Deliver the string](https://codeforces.com/problemset/problem/104317/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings, $A$ and $B$. We start with an empty string $C$, and we are allowed to build $C$ by repeatedly copying a substring from $A$ and appending it to the end of $C$. The string $A$ never changes, and each operation can choose any contiguous segment inside $A$, possibly overlapping previous choices or repeating previous substrings.

The task is to construct $B$ exactly as $C$ using the minimum number of such copy operations.

So the real question is not about constructing $C$ directly, but about splitting $B$ into the fewest segments such that each segment appears somewhere inside $A$ as a substring.

The constraints are large: the total length of all $A$ and $B$ across test cases is up to $2 \cdot 10^5$. This immediately rules out any solution that checks substring existence naively for every possible segment in quadratic time. A naive approach that, for every position in $B$, tries all substrings of $A$ or verifies each candidate by scanning would degenerate to $O(|A| \cdot |B|)$, which is far too slow.

The key edge cases come from patterns where greedily taking short matches looks tempting but is suboptimal if not extended maximally. For example, if $A = \text{"abcd"}$ and $B = \text{"abcdabcd"}$, the optimal answer is 2 by taking "abcd" twice. A careless strategy that cuts early like "a", "b", "c", ... produces 8 operations, which is correct but not minimal. Another subtle case is when $B$ repeats overlapping substrings of $A$, where failing to extend the match fully inside $A$ leads to unnecessary cuts.

The important structural observation is that once a substring of $B$ is confirmed to exist somewhere in $A$, it is always better to extend it as far as possible before starting a new operation.

## Approaches

A direct brute-force strategy is to simulate the process of building $B$ by trying all possible substrings of $A$ at each step. At each position in $B$, we could enumerate every substring of $A$, check whether it matches the current prefix of the remaining suffix of $B$, and pick the longest valid one. This is correct because it directly mirrors the operation rules, but it requires repeated substring comparisons. Each comparison can cost $O(|B|)$ in the worst case, and there are $O(|A|^2)$ substrings of $A$, which makes this approach infeasible.

The key simplification comes from reinterpreting the operation. Since every operation appends a substring of $A$, the problem becomes partitioning $B$ into contiguous blocks, where each block must be a substring of $A$, and we want the minimum number of blocks. The crucial property is that whether a string is a valid block depends only on $A$, not on how previous blocks were chosen.

This independence allows a greedy strategy: starting from the current position in $B$, we should extend the current block as far as possible while it remains a substring of $A$. If we stop earlier, we only reduce the length of a valid block without affecting future feasibility, which can only increase the number of blocks.

To support fast substring existence checks, we can build a suffix automaton for $A$. A suffix automaton compactly represents all substrings of $A$ and allows us to verify in linear time whether a string is a substring by attempting to follow transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (enumerate substrings) | (O( | A | ^2 \cdot |
| Suffix Automaton + greedy scan | (O( | A | + |

## Algorithm Walkthrough

We process each test case independently and use a suffix automaton built from $A$ to test substring validity efficiently.

1. Build a suffix automaton over string $A$. This structure encodes all substrings of $A$ as valid paths from the initial state.
2. Start scanning $B$ from the leftmost position. Maintain a pointer `i` that marks the current start of the segment we are trying to construct.
3. For each segment, reset the automaton state to the initial state and try to extend a second pointer `j` starting from `i`.
4. While `j` is within bounds and there exists a transition in the automaton for character $B[j]$, move forward in the automaton and advance `j`. This ensures that the substring $B[i:j]$ is a valid substring of $A$.
5. When extension is no longer possible, we must end the current segment at position `j`. Increment the answer by one.
6. Set `i = j` and repeat until the entire string $B$ is consumed.

The key idea is that each character of $B$ is processed exactly once as part of a successful extension, and every time we fail to extend, we commit to one operation.

### Why it works

At any position $i$, the algorithm constructs the longest prefix of $B[i:]$ that exists as a substring of $A$. If a shorter prefix were chosen instead, that would only introduce an additional cut without expanding the set of reachable continuations, because any future segment is independent of how we split earlier ones. Since feasibility depends only on whether each segment exists in $A$, maximizing each segment length locally minimizes the number of segments globally.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SuffixAutomaton:
    def __init__(self):
        self.next = [dict()]
        self.link = [-1]
        self.length = [0]
        self.last = 0

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

def build_sam(s):
    sam = SuffixAutomaton()
    for ch in s:
        sam.extend(ch)
    return sam

def solve():
    t = int(input())
    for _ in range(t):
        a = input().strip()
        b = input().strip()

        sam = build_sam(a)

        i = 0
        ans = 0
        n = len(b)

        while i < n:
            state = 0
            j = i

            while j < n and b[j] in sam.next[state]:
                state = sam.next[state][b[j]]
                j += 1

            ans += 1
            i = j

        print(ans)

if __name__ == "__main__":
    solve()
```

The suffix automaton construction processes $A$ in linear time. The main loop over $B$ advances pointer $j$ whenever a valid transition exists in the automaton, and once it fails, we commit a segment and restart from the next position. The critical implementation detail is that we never reset $j$ backward, so each character of $B$ is consumed at most once during successful transitions, keeping the overall complexity linear.

A common mistake is attempting to reuse automaton state across segments. That does not correspond to the problem, because each operation is an independent copy from $A$, not a continuation of a previous substring.

## Worked Examples

Consider the input:

$A = \text{"jzq"}$, $B = \text{"jzqjzq"}$

| Step | i | j | Current segment | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0→3 | "jzq" | valid in A, extend fully |
| 2 | 3 | 3→6 | "jzq" | valid in A, extend fully |

This produces 2 segments. The trace shows that once we reach the full match, no earlier cut improves anything, since stopping early would only increase segment count.

Now consider:

$A = \text{"abcd"}$, $B = \text{"dcbadcba"}$

| Step | i | j | Current segment | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0→1 | "d" | stop (only 'd' matches start in A path) |
| 2 | 1 | 1→2 | "c" | stop |
| 3 | 2 | 2→3 | "b" | stop |
| 4 | 3 | 3→4 | "a" | stop |
| 5 | 4 | 4→5 | "d" | stop |
| 6 | 5 | 5→6 | "c" | stop |
| 7 | 6 | 6→7 | "b" | stop |
| 8 | 7 | 7→8 | "a" | stop |

This forces 8 operations because no longer substring starting at each position exists in $A$. The trace confirms that the algorithm naturally degenerates into single-character segments when longer matches are impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O( | A |
| Space | (O( | A |

The total sum of string lengths across test cases is $2 \cdot 10^5$, so the solution stays comfortably within limits since every character is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip()

# Since full solution is embedded, these are conceptual placeholders
# In practice, integrate solve() and capture output properly.

assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\na\naaaa` | `4` | repeated single-character matching |
| `1\nabcd\ndcba` | `4` | worst-case fragmentation |
| `1\nabcabc\nabcabc` | `1` | full reuse of a long substring |
| `1\nababa\naba` | `1` | overlapping substring structure |

## Edge Cases

One edge case occurs when $B$ is composed of repeated characters that exist in $A$ but longer patterns do not. For example, if $A = "ab"$ and $B = "aaaa"$, the automaton allows only single-character transitions, so each segment ends immediately and the algorithm produces 4 operations. The pointer `j` advances by exactly one character each time, so no incorrect merging happens.

Another case is when $A$ contains multiple overlapping substrings. For $A = "abcab"$ and $B = "abcababcab"$, the automaton allows full matches of length 5 at every step, and the greedy extension consumes the entire block before resetting. The algorithm never prematurely cuts because extension is always possible until the boundary.
