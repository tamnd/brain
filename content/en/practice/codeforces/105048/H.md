---
title: "CF 105048H - Stringliloquy"
description: "We are given a long string representing a “text” of length $N$. Alongside it, we are also given a set of $M$ distinct words. The total length of all words combined is bounded, so although there may be many words, their combined structure is still compact."
date: "2026-06-28T05:44:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 84
verified: false
draft: false
---

[CF 105048H - Stringliloquy](https://codeforces.com/problemset/problem/105048/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a long string representing a “text” of length $N$. Alongside it, we are also given a set of $M$ distinct words. The total length of all words combined is bounded, so although there may be many words, their combined structure is still compact.

Then we are asked $Q$ questions. Each question gives an interval $[l, r]$ inside the main string, and we must count how many substrings fully contained in that interval match any of the given words. Every occurrence is counted independently, so if a word appears multiple times in different positions, or if different words overlap, all valid matches contribute to the answer.

The core difficulty is that both the string and the number of queries are large, so recomputing matches inside each query interval from scratch is too slow. The hidden structure is that all we ever care about is whether a substring starting at some position matches one of the dictionary words, and then how many of those start positions lie inside each query range.

The constraints imply a solution must be close to linear or near-linear in the size of the text plus total dictionary length, with perhaps logarithmic overhead per query. Anything quadratic over $N$ or over $Q$ is immediately impossible.

A naive attempt would scan every query interval and try all substring matches. Even restricting to dictionary words, checking every position against all words gives a worst-case of $O(N \cdot M)$, which is far beyond limits.

A more subtle failure case comes from overlapping matches. For example, if the string is `"AAAAA"` and words include `"A"`, `"AA"`, and `"AAA"`, then at every position multiple matches start, and naive substring enumeration either double-counts incorrectly or spends too much time expanding all possibilities per query.

Another edge case is when many queries overlap heavily. If we recompute matches per query independently, repeated work explodes even if the underlying matches are identical.

## Approaches

The key observation is that every valid answer is determined by start positions of dictionary matches. If we knew, for every index $i$, how many words begin at $i$, then each query becomes a simple range sum over that array.

So the problem reduces to computing a frequency array over the text: for each position, count how many dictionary words match starting there.

A brute-force way is to try every word at every position. This leads to $O(N \cdot \text{word length})$ total comparisons per word, which is too large.

The structure of many patterns with shared prefixes suggests building a trie. Instead of checking each word independently at every position, we can scan the text once while walking the trie, which naturally merges repeated prefixes. This transforms repeated character comparisons into shared transitions.

We build a trie of all words, marking terminal nodes with how many words end there. Then we scan the text starting from each position, walking forward in the trie until we can no longer match. Whenever we reach a terminal node, we record that a word ends there, meaning a valid substring starts at the initial position.

Since total word length is bounded by $10^5$, the total number of trie transitions across all words is also bounded, and each scan from a position stops as soon as mismatch occurs. This makes the total work proportional to total matched transitions rather than $N \cdot M$.

Once we have an array `cnt[i]` = number of words starting at position $i$, we build a prefix sum. Each query $[l, r]$ becomes a single subtraction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot M \cdot L)$ | $O(1)$ | Too slow |
| Trie + Prefix Sum | (O(N + \sum | word | )) |

## Algorithm Walkthrough

1. Build a trie from all words. Each node stores transitions for letters A to Z and a counter indicating how many words end at that node. This allows multiple words sharing prefixes to reuse structure instead of duplicating work.
2. Initialize an array `cnt` of size $N$ with zeros. This array will store how many dictionary words start at each position in the main string.
3. For each starting position $i$ in the main string, traverse the trie character by character starting from $s[i]$. Each step moves down the trie if the character exists; otherwise, stop immediately because no longer match is possible.
4. Whenever we reach a trie node that marks the end of one or more words, add that node’s terminal count to `cnt[i]`. This captures all words that begin at position $i$ and match the prefix seen so far.
5. Repeat this process for all starting positions. The total number of trie transitions is bounded by the total length of all words, since each step either advances along a valid dictionary prefix or stops.
6. Build a prefix sum array over `cnt`. This allows answering any query $[l, r]$ in constant time by computing $\sum_{i=l}^{r} cnt[i]$.
7. For each query, output the difference of prefix sums.

### Why it works

Every valid occurrence of a dictionary word corresponds to exactly one pair: a start position $i$ and a word that matches starting there. The trie traversal from $i$ enumerates exactly those words without duplication because each word corresponds to a unique terminal node path. The prefix sum step does not alter counts, it only aggregates contributions over intervals. Since each match is counted exactly once in `cnt[i]`, and each query sums exactly those positions inside $[l, r]$, the result is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("next", "end")
    def __init__(self):
        self.next = {}
        self.end = 0

def solve():
    N, M, Q = map(int, input().split())
    s = input().strip()

    root = Node()

    # build trie
    for _ in range(M):
        w = input().strip()
        cur = root
        for ch in w:
            if ch not in cur.next:
                cur.next[ch] = Node()
            cur = cur.next[ch]
        cur.end += 1

    cnt = [0] * N

    # scan from every position
    for i in range(N):
        cur = root
        j = i
        while j < N:
            ch = s[j]
            if ch not in cur.next:
                break
            cur = cur.next[ch]
            if cur.end:
                cnt[i] += cur.end
            j += 1

    # prefix sums
    pref = [0] * (N + 1)
    for i in range(N):
        pref[i + 1] = pref[i] + cnt[i]

    out = []
    for _ in range(Q):
        l, r = map(int, input().split())
        out.append(str(pref[r] - pref[l - 1]))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The trie construction ensures that shared prefixes are not recomputed repeatedly. Each node’s `end` value aggregates how many words finish at that point, so duplicates in the dictionary are naturally handled if they exist. The scanning loop stops immediately on mismatch, preventing unnecessary traversal.

The prefix sum array shifts indices by one so that range queries become clean subtractions without off-by-one complexity.

## Worked Examples

### Example 1

Input string: `"ABCDABCD"`

Words: `"AB", "BC", "CD", "A"`

We compute `cnt[i]`:

| i | suffix start | matches found | cnt[i] |
| --- | --- | --- | --- |
| 1 | A B C D... | A | 1 |
| 2 | B C D... | BC | 1 |
| 3 | C D... | CD | 1 |
| 4 | D A B... | none | 0 |
| 5 | A B C D... | A, AB | 2 |
| 6 | B C D... | BC | 1 |
| 7 | C D... | CD | 1 |
| 8 | D... | none | 0 |

Prefix sums then allow queries such as $[4,7]$ or $[1,8]$ to be answered directly. The table shows how overlapping matches at different starting positions are accumulated independently.

### Example 2

Input string: `"AAAAA"`

Words: `"A", "AA", "AAA"`

| i | matches | cnt[i] |
| --- | --- | --- |
| 1 | A, AA, AAA | 3 |
| 2 | A, AA, AAA | 3 |
| 3 | A, AA, AAA | 3 |
| 4 | A, AA | 2 |
| 5 | A | 1 |

This demonstrates why scanning all substrings would explode: every position generates multiple valid words, but trie traversal ensures we stop early once no further extension exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N + \sum | word |
| Space | (O(N + \sum | word |

The bounds $N, Q \le 5 \cdot 10^4$ and total word length $10^5$ fit comfortably within this complexity. The solution performs essentially linear work in input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()  # placeholder if integrated

# NOTE: real integration assumes solve() is available

# sample tests would be inserted when solve() is callable
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single char | 1 | base case correctness |
| overlapping words | high counts | overlap handling |
| no matches | 0s | empty trie matches |
| full string word | 1 full coverage | boundary full match |

## Edge Cases

One important edge case is when every word is a single character. In that situation, every position in the string potentially matches multiple words, and the trie degenerates into a single-level branching structure. The algorithm still behaves correctly because each position contributes independently to `cnt[i]`, and prefix sums accumulate these contributions without interaction.

Another case is when words share long prefixes but diverge late, such as `"ABCDE", "ABCDF", "ABCDG"`. The trie ensures the shared prefix `"ABCD"` is traversed once per start position, and branching happens only at the final step. Even though multiple words may match at the same depth, the `end` counter at terminal nodes ensures all are counted correctly without separate scans.
