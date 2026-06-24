---
title: "CF 105228C - Suffixes"
description: "We are given a fixed set of dictionary words, each very short, and then a large number of queries. Each query provides a word and a rank. For a query word, we compare it against every dictionary word using suffix matching."
date: "2026-06-24T16:20:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105228
codeforces_index: "C"
codeforces_contest_name: "SanSi Cup 2023"
rating: 0
weight: 105228
solve_time_s: 312
verified: false
draft: false
---

[CF 105228C - Suffixes](https://codeforces.com/problemset/problem/105228/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed set of dictionary words, each very short, and then a large number of queries. Each query provides a word and a rank.

For a query word, we compare it against every dictionary word using suffix matching. A dictionary word is considered relevant if it shares at least one suffix with the query word. Among all such matches, we first identify the maximum possible suffix length that appears between the query word and any dictionary word. Only dictionary words achieving this maximum suffix length are kept. From these, we sort the words lexicographically and pick the k-th one. The answer is not the word itself but its original position in the input list. If there are not enough words in the selected group, the answer is -1.

The key structural detail is that words are extremely short, with length at most 5. That immediately limits the number of distinct suffixes that can appear, because every word contributes only a constant number of suffixes.

A naive interpretation would try to compare each query word against all dictionary words and compute suffix matches directly. With up to 10^5 dictionary words and 10^5 queries, that would be far too slow even if each comparison is short.

A second subtle issue is that the “best match” is defined globally per query, not per word independently. A dictionary word that matches a shorter suffix is irrelevant if another word matches a longer suffix.

A simple failure case appears when multiple suffix lengths exist.

For example, if dictionary words are `["aba", "caba"]` and query is `"xxcaba"`, both words match suffix `"aba"` but only `"caba"` matches suffix length 4. The correct answer must ignore all length-3 matches entirely.

Another pitfall is forgetting lexicographic ordering after filtering by suffix length. Two words may both match the best suffix length, but the answer depends on sorted order, not input order.

## Approaches

A direct brute force solution compares each query word with every dictionary word and computes their longest common suffix by scanning from the end up to 5 characters. Since each comparison costs O(5), a single query costs O(5n), and all queries cost O(5nq), which is on the order of 10^10 operations. This is far beyond the time limit.

The constraint that words have length at most 5 changes the structure completely. Each dictionary word contributes only a small set of suffixes: its last character, last two characters, and so on up to the full word. If we reverse our thinking, instead of comparing queries to all words, we can pre-group dictionary words by suffix.

For every dictionary word, we generate all its suffixes and store the word in a bucket keyed by that suffix string. Each bucket represents all dictionary words that share that suffix. If a query ends with the same suffix, we can immediately retrieve all matching words for that exact suffix length.

The crucial observation is that the answer only depends on the longest suffix that exists in this precomputed structure. So for each query, we check its suffixes from longest to shortest until we find a non-empty bucket. That bucket is exactly the set of words achieving the maximum possible suffix match length. We then sort that bucket lexicographically once during preprocessing so each query can directly index into it.

This reduces each query to checking at most 5 suffixes and then performing a simple k-th selection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq · 5) | O(1) | Too slow |
| Precomputed suffix buckets | O((n + q) · 5 + Σ sorting) | O(n · 5) | Accepted |

## Algorithm Walkthrough

1. For each dictionary word, generate all its suffixes by taking the last character, last two characters, and so on up to the full word. Store the word’s original index inside a map keyed by each suffix. This builds direct access from any suffix string to all words that contain it.
2. After processing all dictionary words, sort the list of words stored in each suffix bucket lexicographically by the word itself. We keep both the word and its original index so that we can output the required position later.
3. For each query word, consider its suffixes in decreasing order of length. Start from the full word and gradually remove the first character until only one character remains.
4. For each suffix, check whether it exists in the precomputed map. The first suffix found corresponds to the maximum possible suffix length shared with any dictionary word.
5. If no suffix is found in the map, output -1 because no dictionary word shares any suffix with the query.
6. Otherwise, take the corresponding bucket. If its size is less than k, output -1. If it is large enough, select the k-th element in lexicographic order and output its stored original index.

The correctness comes from the fact that suffixes are checked in strictly decreasing order of length. The first match guarantees maximality, so no longer suffix match can exist for any dictionary word outside that bucket. All words in that bucket share exactly that suffix length, and any word matching a shorter suffix is irrelevant by definition of the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    words = []
    buckets = {}

    for i in range(n):
        w = input().strip()
        words.append(w)
        L = len(w)
        for j in range(L):
            suf = w[j:]
            if suf not in buckets:
                buckets[suf] = []
            buckets[suf].append((w, i + 1))

    for suf in buckets:
        buckets[suf].sort(key=lambda x: x[0])

    q = int(input())
    for _ in range(q):
        s, k = input().split()
        k = int(k)

        found = None

        for i in range(len(s)):
            suf = s[i:]
            if suf in buckets:
                found = buckets[suf]
                break

        if not found or len(found) < k:
            print(-1)
        else:
            print(found[k - 1][1])

if __name__ == "__main__":
    solve()
```

The preprocessing stage builds a dictionary from suffix strings to all dictionary words sharing that suffix. Each stored entry keeps both the word and its original position, since sorting is done by word but output requires the original index.

Each bucket is sorted once so that every query can directly access the k-th lexicographic element without recomputation.

During querying, suffixes of the query word are tested from longest to shortest. The first successful lookup guarantees the maximum suffix match length. The corresponding bucket is then used to answer the ranking request.

A subtle point is that we never recompute suffix matches dynamically. All comparisons are reduced to dictionary lookups on precomputed keys, which keeps query time constant.

## Worked Examples

Consider a small dictionary and a query set.

Dictionary: `["aba", "caba", "baba"]`

Query: `"xxcaba", k = 2`

| Step | Suffix Checked | Exists in Map | Selected Bucket |
| --- | --- | --- | --- |
| 1 | "xxcaba" | No | None |
| 2 | "xcaba" | No | None |
| 3 | "caba" | Yes | ["caba"] |

At this point the search stops because `"caba"` is the longest valid suffix. The bucket contains only one word, so k = 2 is invalid and the output is -1. This demonstrates that shorter suffix matches are never considered once a longer one is found.

Now consider:

Dictionary: `["abc", "xbc", "c", "bc"]`

Query: `"zzbc", k = 2`

| Step | Suffix Checked | Exists in Map | Selected Bucket |
| --- | --- | --- | --- |
| 1 | "zzbc" | No | None |
| 2 | "zbc" | No | None |
| 3 | "bc" | Yes | ["abc", "xbc", "bc"] |

After sorting lexicographically, the bucket becomes `["abc", "bc", "xbc"]`. The second element is `"bc"`, so the output is its original index.

The trace shows how suffix selection reduces the problem to a single precomputed group, and how ordering within that group determines the final answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L + q · L + total sorting) | Each word contributes up to 5 suffixes, each query checks up to 5 suffixes, and each bucket is sorted once |
| Space | O(n · L) | Every suffix stores references to dictionary words |

The value of L is at most 5, so all factors involving L behave as constant overhead. This keeps both time and memory comfortably within limits even for 10^5 words and queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# sample
assert run("""4
a
b
c
d
1
a 1
""") == "1"

# identical suffix competition
assert run("""3
aba
caba
baba
1
xxcaba 1
""") == "2"

# k too large
assert run("""3
abc
xbc
c
1
zzbc 5
""") == "-1"

# smallest inputs
assert run("""1
a
1
a 1
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single word | 1 | minimal case correctness |
| multiple same-suffix candidates | correct index | lexicographic sorting |
| k exceeds bucket | -1 | boundary handling |
| longest suffix selection | correct filtering | suffix-max rule |

## Edge Cases

A case where a query matches multiple suffix lengths is handled by scanning suffixes from longest to shortest. The first successful lookup always corresponds to the maximum possible match length because every shorter suffix is considered only after longer ones are exhausted.

For a query like `"abcd"` with dictionary words `"bcd"` and `"cd"`, the algorithm first checks `"abcd"`, then `"bcd"`, and immediately stops at `"bcd"`. The shorter suffix `"cd"` is never considered, which preserves correctness of the “maximum suffix length” requirement.

Another edge case is when multiple words share the same best suffix but appear in arbitrary input order. Since each bucket is explicitly sorted lexicographically after construction, the selection of the k-th element is independent of input order, preventing incorrect answers caused by insertion order.
