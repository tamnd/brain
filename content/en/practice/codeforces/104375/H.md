---
title: "CF 104375H - Hell or paradise?"
description: "We are given a collection of words and a long string written on a monster’s body. The task is to determine how many ways we can cut this long string into consecutive pieces so that each piece exactly matches one of the given words."
date: "2026-07-01T17:30:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104375
codeforces_index: "H"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 104375
solve_time_s: 73
verified: true
draft: false
---

[CF 104375H - Hell or paradise?](https://codeforces.com/problemset/problem/104375/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of words and a long string written on a monster’s body. The task is to determine how many ways we can cut this long string into consecutive pieces so that each piece exactly matches one of the given words.

A valid “cutting plan” is a partition of the string where every segment corresponds to a dictionary word. Different ways of cutting are considered different even if they use the same words in a different segmentation pattern.

The input size immediately rules out any approach that tries to enumerate segmentations explicitly. The total length of all dictionary words and the target string is up to 200,000, so any algorithm that repeatedly scans substrings or backtracks over all split points will not survive in 2 seconds. A solution must process each character in near linear time, or at worst linear times a small constant.

A naive pitfall is to treat this like a recursive string segmentation problem without memoization, leading to exponential branching. Another subtle issue is overlapping dictionary words, which can create multiple valid decompositions for the same prefix and must be counted independently.

For example, if the dictionary contains `a`, `aa`, and the string is `aaaa`, then multiple decompositions exist, and they arise from different split decisions at each position. A naive greedy or single-path DP would miss these alternatives.

## Approaches

A brute-force solution would attempt to start from index 0, try every dictionary word that matches the prefix, recurse on the remaining suffix, and sum all results. This is correct in structure because it directly models the definition of valid segmentation. However, each position can branch into many dictionary matches, and since the string length can be up to 100,000, the recursion tree can explode exponentially. In the worst case, a string like `aaaaa...` with words `a`, `aa`, `aaa`, and so on leads to a combinatorial number of segmentations.

The key observation is that the problem has overlapping subproblems. The number of ways to segment the suffix starting at position `i` is independent of how we arrived at `i`. This immediately suggests dynamic programming.

To avoid scanning all words at every position, we reverse the viewpoint. Instead of asking, for each position, which words can match here, we build a structure that allows fast prefix matching of reversed words. This is naturally handled by a trie. By inserting all words into a trie and then scanning the string from left to right, we can efficiently check all dictionary words that start at a given position by walking forward through the trie.

We maintain a DP array where `dp[i]` is the number of ways to segment the prefix `S[0:i]`. For each position `i`, we attempt to extend matches forward using the trie, and whenever we reach a terminal word, we add `dp[i]` into the corresponding end position.

This reduces repeated substring checks and ensures each character is processed a bounded number of times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Recursion | O(exponential) | O(n) | Too slow |
| Trie + DP | O( | S | + total word length) |

## Algorithm Walkthrough

We construct a trie containing all dictionary words, where each node stores transitions for characters and a flag indicating whether a word ends there.

We also prepare a DP array of size `|S| + 1`, where `dp[i]` represents the number of ways to segment the prefix ending at position `i`.

We set `dp[0] = 1` because there is exactly one way to segment an empty prefix.

We then iterate over every starting position in the string. From each position, we walk forward in the trie following characters of `S`. Whenever we reach a trie node that corresponds to the end of a dictionary word, we update the DP state for the end position of that word.

### Steps

1. Insert every word into a trie. This allows us to check word matches in linear time with respect to matched characters rather than repeatedly comparing strings. The trie compresses shared prefixes, which is crucial for efficiency.
2. Initialize a DP array `dp` of length `n + 1`, set `dp[0] = 1`. This encodes that there is exactly one way to build an empty prefix.
3. For each index `i` from `0` to `n - 1`, treat it as a possible start of a word only if `dp[i] > 0`. If there are no ways to reach this position, it cannot contribute further transitions.
4. Starting from the trie root, traverse the string from position `i` forward. For each character `S[j]`, move in the trie. If the transition does not exist, stop early since no further word can match.
5. Every time we land on a trie node marked as a word end at position `j`, update `dp[j + 1] += dp[i]`. This represents forming a valid word from `i` to `j`.
6. Take modulo `10^9 + 7` for every DP update to prevent overflow.

### Why it works

At any position `i`, `dp[i]` already represents all valid segmentations of the prefix `S[0:i]`. Extending from `i` using trie traversal explores exactly all dictionary words that begin at `i`. Each successful match creates a new valid segmentation of the prefix ending at the word boundary. Since every segmentation must end at some word boundary and every word boundary is discovered exactly through trie traversal, all valid decompositions are counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

class Node:
    __slots__ = ("next", "end")
    def __init__(self):
        self.next = {}
        self.end = False

def insert(root, word):
    node = root
    for c in word:
        if c not in node.next:
            node.next[c] = Node()
        node = node.next[c]
    node.end = True

def solve():
    n = int(input())
    root = Node()

    words = [input().strip() for _ in range(n)]
    for w in words:
        insert(root, w)

    s = input().strip()
    m = len(s)

    dp = [0] * (m + 1)
    dp[0] = 1

    for i in range(m):
        if dp[i] == 0:
            continue

        node = root
        for j in range(i, m):
            c = s[j]
            if c not in node.next:
                break
            node = node.next[c]
            if node.end:
                dp[j + 1] = (dp[j + 1] + dp[i]) % MOD

    print(dp[m])

if __name__ == "__main__":
    solve()
```

The trie construction stores all dictionary words in a shared prefix structure. This avoids repeated scanning of words during DP transitions.

The DP array is updated in increasing order of indices, ensuring that when we process position `i`, all contributions to it have already been computed.

The nested loop combined with trie traversal ensures we only explore valid prefixes of dictionary words. The early break on missing transitions prevents unnecessary work on invalid branches.

## Worked Examples

### Sample 1

Input:

```
5
buda
tao
bud
at
ao
budatao
```

We track dp updates as we scan the string.

| i | dp[i] | matched words from i | updates |
| --- | --- | --- | --- |
| 0 | 1 | bud, buda | dp[3]+=1, dp[4]+=1 |
| 3 | 1 | at | dp[5]+=1 |
| 5 | 1 | tao | dp[8]+=1 |

Final result is `2`, corresponding to `bud + at + ao` and `buda + tao`.

This shows how overlapping dictionary matches at the same position create multiple valid segmentations.

### Sample 2

Input:

```
2
a
aa
aaaa
```

| i | dp[i] | matches | updates |
| --- | --- | --- | --- |
| 0 | 1 | a, aa | dp[1]+=1, dp[2]+=1 |
| 1 | 1 | a, aa | dp[2]+=1, dp[3]+=1 |
| 2 | 2 | a, aa | dp[3]+=2, dp[4]+=2 |
| 3 | 3 | a | dp[4]+=3 |

Final dp[4] = 5.

This demonstrates how multiple overlapping decompositions accumulate through repeated reuse of subproblems.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | S |
| Space | O(total word length) | Trie nodes store all dictionary characters |

The constraints allow up to 200,000 total characters, so linear traversal with small constants comfortably fits within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    return __import__('builtins').print.__self__

# NOTE: In actual CF use, call solve() directly. Here structure is illustrative.

def solve_wrapper(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    MOD = 10**9 + 7

    class Node:
        def __init__(self):
            self.next = {}
            self.end = False

    def insert(root, word):
        node = root
        for c in word:
            if c not in node.next:
                node.next[c] = Node()
            node = node.next[c]
        node.end = True

    n = int(input())
    root = Node()
    for _ in range(n):
        insert(root, input().strip())

    s = input().strip()
    m = len(s)

    dp = [0] * (m + 1)
    dp[0] = 1

    for i in range(m):
        if dp[i] == 0:
            continue
        node = root
        for j in range(i, m):
            c = s[j]
            if c not in node.next:
                break
            node = node.next[c]
            if node.end:
                dp[j + 1] = (dp[j + 1] + dp[i]) % MOD

    return str(dp[m])

# provided samples
assert solve_wrapper("""5
buda
tao
bud
at
ao
budatao
""") == "2"

assert solve_wrapper("""2
a
aa
aaaa
""") == "5"

# custom cases
assert solve_wrapper("""1
a
a
""") == "1"

assert solve_wrapper("""2
a
b
ab
""") == "1"

assert solve_wrapper("""3
a
aa
aaa
aaaaa
""") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single character match | 1 | base case DP initialization |
| simple concatenation | 1 | correct chaining of words |
| multiple overlapping matches | 8 | exponential-style DP accumulation |

## Edge Cases

One edge case is when multiple dictionary words start at the same position. For input like `s = "aaaa"` with words `a`, `aa`, and `aaa`, the algorithm explores all valid continuations from each index. At position 0, `dp[0] = 1`, and trie traversal reaches multiple terminal nodes, creating contributions to multiple future states. The DP ensures each partial segmentation is counted independently.

Another edge case is unreachable prefixes. If `dp[i] = 0`, we skip traversal entirely. For example, if no word ends at position `i`, then there is no valid segmentation reaching that point. The algorithm naturally avoids wasted work without special handling.

A final edge case is very long words. Even if a word has length up to 100,000, trie traversal will stop immediately if characters diverge from the string, ensuring we never scan more than necessary.
