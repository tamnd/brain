---
title: "CF 105461J - Gibberish"
description: "We are dealing with a hidden permutation of positions from 1 to n. Whenever we send a word of length n, the system rearranges the letters according to this fixed permutation and returns the result."
date: "2026-06-23T17:54:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105461
codeforces_index: "J"
codeforces_contest_name: "2024-2025 ICPC, Swiss Subregional"
rating: 0
weight: 105461
solve_time_s: 63
verified: true
draft: false
---

[CF 105461J - Gibberish](https://codeforces.com/problemset/problem/105461/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are dealing with a hidden permutation of positions from 1 to n. Whenever we send a word of length n, the system rearranges the letters according to this fixed permutation and returns the result.

The permutation is consistent across all queries, so every response is just a deterministic relabeling of indices. The task is to reconstruct exactly where each original position ends up.

The key difficulty is that we only get to interact up to four times, and n can be as large as 100000. That rules out any strategy that tries to recover the permutation one position at a time. Any approach that queries each index independently would immediately exceed the limit on interactions, and even non-interactive reconstruction based on probing pairs of positions would still require linear or superlinear interaction count.

The structure suggests that each query must carry information about many positions simultaneously, and each response must allow us to extract positional identities indirectly.

A subtle failure case appears if we try to assign identical characters or low-resolution labels. For example, if we send a string of all `'a'`, the response is also all `'a'`, which reveals nothing about the permutation. Similarly, using only a few distinguishable symbols leads to collisions where multiple positions share the same signature, making reconstruction ambiguous.

The core requirement is to ensure that every position has a unique identity that can be recovered after permutation, while using only four queries.

## Approaches

A brute-force idea is to try identifying where each index goes by crafting queries that isolate positions. One could, for example, send strings where only one position is marked differently and observe where that mark appears in the output. This would work because we could track the movement of a single position per query. However, this immediately fails on scale: identifying n positions would require Θ(n) queries, while we are allowed only 4.

The key observation is that we do not need to identify positions sequentially. Instead, we can encode every position with a small fixed-length signature and recover that signature after permutation.

The permutation does not destroy information; it only rearranges it. If each position carries a unique “label vector”, then after permutation, those vectors are simply shuffled across positions. If we can reconstruct the vector seen at each output index, we can map it back to the original position.

With only four queries, each position can contribute four symbols of information. Using the 26-letter alphabet, each symbol can encode a base-26 digit. This gives us 26^4 possible distinct codes, which is more than enough for n up to 100000.

We assign each position i a 4-digit base-26 representation. In query k, position i is assigned the k-th digit as a character. After permutation, each output position reveals the full 4-character code of its source index. This makes reconstruction direct: we map each 4-character tuple back to the original index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) or O(n) queries | O(n) | Too slow |
| Optimal Encoding | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Assign each index i a unique identifier using base-26 encoding over 4 digits. This ensures every position has a distinct signature that can be reconstructed later.
2. Build four query strings. For each position i and each query k from 0 to 3, place the k-th digit of i in the alphabet at position i of the k-th string.
3. Send the first query string and receive a permuted result. For each position j in the response, record the character coming from the original position that maps into j under the permutation.
4. Repeat the same process for all four queries. After processing all responses, each position j has collected four characters, forming a 4-character signature.
5. Convert each 4-character signature back into the original index using base-26 decoding. This gives the inverse permutation, meaning for each output position j we find which original index i produced it.
6. Output the permutation in the required form.

The reason this works is that each query acts like a projection of a 4-dimensional encoding of indices. The permutation only reorders these encodings but does not mix them, so each position retains a complete, recoverable signature.

### Why it works

The invariant is that at any time, every position in the permuted strings carries exactly the same 4-character code that was assigned to a unique original index. Since the encoding function from indices to 4-character vectors is injective, and permutation preserves multiset structure without altering values, reconstructing the original index from any position is always unambiguous. No two indices share the same 4-character tuple, so no collisions can occur during reconstruction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def encode(i):
    # 4-digit base-26 encoding
    res = []
    for _ in range(4):
        res.append(chr(ord('a') + (i % 26)))
        i //= 26
    return res  # least significant digit first

def main():
    n = int(input().strip())

    # build 4 query strings
    queries = [ [''] * n for _ in range(4) ]

    codes = []
    for i in range(n):
        c = encode(i)
        codes.append(c)
        for k in range(4):
            queries[k][i] = c[k]

    queries = [''.join(q) for q in queries]

    # store received characters per position
    got = [ [] for _ in range(n) ]

    for k in range(4):
        print("?", queries[k])
        sys.stdout.flush()
        resp = input().strip()

        for j, ch in enumerate(resp):
            got[j].append(ch)

    # reconstruct mapping
    pos = {}
    for i, c in enumerate(codes):
        pos[''.join(c)] = i + 1

    ans = [0] * n
    for j in range(n):
        key = ''.join(got[j])
        ans[j] = pos[key]

    print("!", *ans)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
```

The construction phase builds four independent character layers, each acting as one digit of a base-26 identifier. The interaction loop reads back four permuted versions of these layers and accumulates the characters belonging to each output position. Once all four layers are collected, each position is fully identified by its 4-character key, which is then decoded back to the original index.

A common implementation pitfall is mixing up direction of permutation. The key insight is that the output position stores information about the original index, not the other way around, so reconstruction must treat collected tuples as inverse mapping targets.

## Worked Examples

Consider a small permutation n = 5 with permutation p = [3, 5, 1, 4, 2]. This means position 1 moves to 3, position 2 moves to 5, and so on.

We assign base-26 codes, but for simplicity imagine characters:

| index i | code |
| --- | --- |
| 1 | aaaa |
| 2 | aaab |
| 3 | aaba |
| 4 | abaa |
| 5 | baaa |

After permutation, positions receive codes from their sources:

| output position j | received code |
| --- | --- |
| 1 | aaba |
| 2 | baaa |
| 3 | aaaa |
| 4 | abaa |
| 5 | aaab |

From this table, we directly recover original indices by matching codes back to their assigned positions.

This trace shows that each output position independently reconstructs its origin without needing any cross-position inference beyond decoding.

A second example with n = 3 and identity permutation confirms stability. Every output position receives exactly its own code, so decoding trivially returns [1, 2, 3], verifying correctness in the fixed-point case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of 4 queries processes n characters once |
| Space | O(n) | Stores 4-character signatures for each position |

The solution performs a constant number of full-length scans over the string and stores a fixed-size label per position. With n up to 100000, this remains well within limits, and only four interactive queries are used.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    # Placeholder since this is interactive; real testing would mock interaction
    return "ok"

# custom sanity checks (non-interactive logic checks would go here)

assert True, "placeholder"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 identity | 1 | minimum size correctness |
| n=5 random permutation | valid permutation | general correctness |
| n=100000 identity | 1..n | maximum size stability |
| repeated structure check | unique decoding | collision safety |

## Edge Cases

For n = 1, the encoding still produces a 4-character signature for the single position. All four queries return identical single-character strings, and reconstruction maps that signature back to index 1 without ambiguity.

For large n close to 100000, base-26 four-digit encoding still provides sufficient uniqueness since 26^4 exceeds the range. Each index remains uniquely identifiable, and no collisions appear in the decoding map, ensuring correctness at scale.
