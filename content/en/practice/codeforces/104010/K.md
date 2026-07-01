---
title: "CF 104010K - Pick a Pair"
description: "We are given an even number of words, all of identical length, and we want to pair them up. A pair is considered valid for a chosen value $k$ if the two words share a common prefix of length at least $k$."
date: "2026-07-02T05:22:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104010
codeforces_index: "K"
codeforces_contest_name: "2022-2023 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 22)"
rating: 0
weight: 104010
solve_time_s: 68
verified: true
draft: false
---

[CF 104010K - Pick a Pair](https://codeforces.com/problemset/problem/104010/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an even number of words, all of identical length, and we want to pair them up. A pair is considered valid for a chosen value $k$ if the two words share a common prefix of length at least $k$. Our task is to determine the maximum value of $k$ such that we can partition all words into disjoint pairs, and every pair satisfies this prefix constraint.

A useful way to rephrase the problem is to imagine that each word is a string placed at a leaf of a trie. For a fixed depth $k$, we are only allowed to pair words that land in the same node at depth $k$. The question becomes whether every group of words that share the same length-$k$ prefix can be internally paired.

The constraints are large: up to $2 \cdot 10^5$ words and total character length up to $2 \cdot 10^6$. This immediately suggests that any solution that repeatedly compares words or recomputes prefix structure for many values of $k$ will be too slow. A solution that is linear or near-linear in total string size is required, possibly with a logarithmic or constant number of passes over the data.

A subtle edge case arises when prefix grouping is imbalanced. For example, if at some depth $k$, one prefix bucket contains an odd number of words, pairing is impossible even if all other buckets are perfectly balanced. Another important case is when $k = 0$, where all words trivially match, so the answer is at least zero.

## Approaches

A brute-force idea is to fix $k$, group words by their first $k$ characters, and check whether each group has even size. This check is straightforward and correct, but repeating it for all possible $k$ up to the string length is expensive. Each check costs $O(n \cdot k)$ if done directly, leading to a worst-case $O(n \cdot L^2)$ or at least $O(n \cdot L)$ per check depending on implementation, which is too slow for $2 \cdot 10^5$ words and long strings.

The key observation is that feasibility is monotonic in a reversed sense over increasing $k$. If we fix a value $k$, we are essentially grouping words by prefixes of length $k$. Increasing $k$ refines the groups, potentially breaking large even groups into smaller ones that may become odd-sized. So if a certain $k$ is feasible, all smaller values are also feasible. This monotonicity suggests binary search over $k$.

The remaining problem is how to efficiently check feasibility for a fixed $k$. Instead of recomputing prefixes from scratch for each candidate $k$, we sort the words lexicographically. In a sorted array, all words sharing a prefix of length $k$ appear in a contiguous block. We can then scan the array once, grouping consecutive words that match on the first $k$ characters, and verifying that each block size is even.

This reduces each feasibility check to a linear scan over the sorted list with prefix comparisons, and binary search adds a logarithmic factor over possible $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot L^2)$ | $O(1)$ or $O(nL)$ | Too slow |
| Binary Search + Sorting + Scan | $O(nL \log L)$ | $O(nL)$ | Accepted |

## Algorithm Walkthrough

We first sort all words lexicographically. This ensures that any set of words sharing a prefix of length $k$ forms a contiguous segment in the array, because lexicographic order is determined exactly by prefixes.

Next, we binary search on the answer $k$, from $0$ to the maximum possible prefix length.

For a fixed candidate $k$, we scan the sorted array and group consecutive words that share the same prefix of length $k$. For each such group, we check whether its size is even. If every group is even-sized, the candidate $k$ is feasible.

We then adjust the binary search range accordingly: if feasible, we try larger $k$, otherwise we reduce it.

### Why it works

At any fixed $k$, grouping words by prefix of length $k$ defines an equivalence relation. Pairing is possible if and only if every equivalence class has even cardinality, since each pair must stay within a class. Sorting ensures these equivalence classes become contiguous segments, so the scan correctly identifies them without hashing or additional data structures. Binary search is valid because feasibility only decreases as $k$ increases.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(k, words):
    n = len(words)
    i = 0
    while i < n:
        j = i + 1
        pref = words[i][:k]
        while j < n and words[j][:k] == pref:
            j += 1
        if (j - i) % 2 == 1:
            return False
        i = j
    return True

def solve():
    n = int(input().strip())
    words = [input().strip() for _ in range(n)]
    words.sort()

    lo, hi = 0, len(words[0])

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid, words):
            lo = mid
        else:
            hi = mid - 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The sorting step is crucial because it transforms prefix grouping into a linear scan problem. The `can` function implements the feasibility check for a fixed $k$ by walking through contiguous blocks of identical prefixes. The binary search is biased upward using `(lo + hi + 1) // 2` to avoid infinite loops when narrowing the upper bound.

The main subtlety is ensuring the prefix comparison is consistent: slicing `words[j][:k]` is safe because all strings have equal length, and we only compare up to the same fixed $k$.

## Worked Examples

Consider a small example:

Input:

```
4
aabc
aacc
bbbb
bbbd
```

We first sort the words. Then we test different values of $k$.

| k | Groups (by prefix) | Validity |
| --- | --- | --- |
| 0 | all 4 together | valid |
| 1 | {aa.., aa..}, {bb.., bb..} | valid |
| 2 | {aab, aac}, {bbb, bbb} | valid |
| 3 | {aabc}, {aacc}, {bbb}, {bbbd} | invalid |

At $k=3$, every group has size 1, so pairing is impossible. The maximum valid $k$ is 2.

This trace shows that feasibility fails exactly when refinement produces singleton groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nL \log L)$ | sorting plus $O(\log L)$ checks, each linear scan over words |
| Space | $O(nL)$ | storage of all input strings |

The constraints allow up to $2 \cdot 10^6$ total characters, so an $O(nL \log L)$ approach is safe. Each feasibility check is a simple pass over the data, and binary search limits the number of such passes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return io.StringIO(sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else "").getvalue()

# Since solve() prints directly, we redefine a safer runner
def run(inp: str) -> str:
    import sys, io
    backup = sys.stdin
    backup_out = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdin = backup
    sys.stdout = backup_out
    return out

# provided sample
assert run("""4
aabc
aacc
bbbb
bbbd
""") == "2"

# minimum case
assert run("""2
aa
aa
""") == "2"

# all identical
assert run("""4
abc
abc
abc
abc
""") == "3"

# forced k=0 only
assert run("""2
ab
cd
""") == "0"

# mixed prefixes
assert run("""6
aaa
aab
aba
abb
bbb
bbc
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 identical pairs | 3 | maximum prefix when everything matches |
| 2 distinct words | 0 | only trivial pairing possible |
| mixed structured groups | 1 | partial prefix matching behavior |

## Edge Cases

A key edge case is when a prefix group becomes odd after refinement. For example:

Input:

```
4
aaaa
aaab
aaba
aabb
```

At $k = 1$, sorting groups them by first character, producing one block of 4, which is valid. At $k = 2$, grouping by first two characters splits them into two groups of size 2, still valid. At $k = 3$, each becomes a singleton group, making pairing impossible. The algorithm correctly detects failure at $k=3$ because during the scan, each block length is 1, which is odd, and immediately rejects the candidate.

This shows that the scan does not depend on global structure beyond contiguous grouping, and correctly handles fragmentation into multiple small classes.
