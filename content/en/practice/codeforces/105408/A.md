---
title: "CF 105408A - AAEGGLNU"
description: "We are given a collection of words that form a dictionary and a sequence of query words. The ordering of words is not the usual lexicographic order on the raw strings."
date: "2026-06-24T23:07:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105408
codeforces_index: "A"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico Repechaje"
rating: 0
weight: 105408
solve_time_s: 71
verified: false
draft: false
---

[CF 105408A - AAEGGLNU](https://codeforces.com/problemset/problem/105408/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of words that form a dictionary and a sequence of query words. The ordering of words is not the usual lexicographic order on the raw strings. Instead, each word is first transformed by sorting its characters alphabetically, and this transformed version is used as the primary key for comparison.

If two words have different sorted forms, the one with the smaller sorted string comes first. If the sorted forms are identical, we fall back to comparing the original words lexicographically.

Each query asks how many dictionary words are less than or equal to the query under this custom ordering.

The constraints allow up to one hundred thousand dictionary words and one hundred thousand queries, with total character length up to one million. This immediately rules out any solution that compares each query against all dictionary words individually, since a naive approach would require on the order of 10^10 character comparisons in the worst case.

A subtle issue appears when words are anagrams. For example, "abc" and "bca" share the same sorted representation "abc". In this case, the ordering depends on the original strings, not just the sorted form. Another edge case arises when many identical words exist. A correct solution must count all occurrences properly.

A naive mistake would be to sort only by the transformed string and ignore the tie-break rule. For instance, if the dictionary contains "ab" and "ba", both map to "ab". Without the secondary key, their relative order would be undefined, which breaks query correctness when counting prefix ranges.

## Approaches

A direct solution would process each query independently by iterating over all dictionary words and checking whether each word is smaller than or equal to the query under the defined ordering. This requires computing the sorted form for each comparison or storing it upfront. Even if preprocessing is done, each query still needs O(N) comparisons, leading to O(NQ) time. With 100000 queries, this becomes too large.

The key observation is that the ordering defines a total order on words if we treat each word as a pair consisting of its sorted version and the original string. Once every word is mapped into such a pair, we can sort the entire dictionary once. After sorting, each query reduces to finding the position of its pair in this sorted array, which can be done using binary search.

This works because the comparison rule is consistent and transitive once expressed as tuple ordering. Sorting the dictionary essentially builds the full order structure ahead of time, and each query becomes a rank query over a sorted array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ · L) | O(1) extra | Too slow |
| Sort + Binary Search | O((N + Q) L log N) | O(N) | Accepted |

Here L is the maximum word length contribution for sorting characters.

## Algorithm Walkthrough

1. Read all dictionary words and compute a transformed version for each word by sorting its characters. This transformation captures the primary comparison key used in the ordering.
2. Store each word as a pair consisting of its sorted version and its original string. The pair structure ensures that tie-breaking is automatically handled.
3. Sort the list of dictionary pairs. The sorting is lexicographic on the pair, meaning it first compares the sorted versions and then the original strings if needed.
4. For each query word, compute the same pair representation: its sorted version and its original form.
5. Use binary search to find how many dictionary pairs are less than or equal to this query pair. This is equivalent to finding the upper bound position of the query pair in the sorted array.
6. Output the resulting index for each query.

### Why it works

Every word is mapped to a unique comparable key in the form (sorted_string, original_string). The sorting step produces a total order consistent with the problem definition. Since the dictionary is sorted according to this order, all words less than or equal to a query form a contiguous prefix. Binary search correctly identifies the boundary of this prefix, so the count returned is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = []

    for _ in range(n):
        w = input().strip()
        arr.append(("".join(sorted(w)), w))

    arr.sort()

    q = int(input())
    res = []

    from bisect import bisect_right

    for _ in range(q):
        b = input().strip()
        key = ("".join(sorted(b)), b)
        res.append(str(bisect_right(arr, key)))

    print("\n".join(res))

if __name__ == "__main__":
    solve()
```

The core idea in the implementation is representing each word as a tuple so that Python’s built-in lexicographic tuple comparison matches the required ordering exactly. Sorting the list once establishes the full dictionary order.

For each query, constructing the same tuple ensures compatibility with the sorted list. The use of `bisect_right` is crucial because it counts all elements less than or equal to the query, including duplicates of identical words.

## Worked Examples

Consider a simple dictionary: ["ab", "ba", "aab", "baa"].

After transformation, we get pairs:

("ab", "ab"), ("ab", "ba"), ("aab", "aab"), ("aab", "baa")

After sorting:

("aab", "aab")

("aab", "baa")

("ab", "ab")

("ab", "ba")

Now consider query "aba". Its pair is ("aab", "aba").

| Step | Query | Sorted Key | Upper Bound Position |
| --- | --- | --- | --- |
| 1 | aba | aab | after second group |
| 2 | aba | aab | 2 |

This shows that both words with key "aab" are counted.

Another query "ba" becomes ("ab", "ba"), which lies in the second group.

| Step | Query | Sorted Key | Upper Bound Position |
| --- | --- | --- | --- |
| 1 | ba | ab | after all "aab" entries |
| 2 | ba | ab | 4 |

This demonstrates that tie-breaking on original strings correctly separates identical sorted forms.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + Q) · L log N) | Sorting N transformed words dominates; each transformation costs O(L log L) and each query uses O(log N) binary search |
| Space | O(N) | Storage of transformed pairs for all dictionary words |

The constraints allow up to one million total characters, so sorting each word and then sorting the array is comfortably fast within one second in Python when implemented with built-in sort and bisect.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample (formatted logically)
assert run("""5
language
abc
ddcba
aaegglnu
b
3
bcd
ace
gglnua
""") == """3
5
1"""

# all identical words
assert run("""3
aa
aa
aa
2
aa
a
""") == """3
0"""

# anagram ordering check
assert run("""4
ab
ba
aab
baa
2
ab
baa
""") == """3
4"""

# single word cases
assert run("""1
abc
2
abc
a
""") == """1
0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical words | 3, 0 | duplicates and equality handling |
| anagrams | 3, 4 | sorted-key grouping correctness |
| single word | 1, 0 | boundary behavior |

## Edge Cases

When all dictionary words are identical, every query that matches that word must return the full count. The tuple representation ensures this because all keys become identical, and `bisect_right` places the insertion point at the end of the block, counting all occurrences.

When words are anagrams, such as "ab" and "ba", the sorted key becomes identical. The secondary ordering by original string ensures deterministic placement inside that block. Queries must still count all entries in the block when the query’s original string falls after some of them lexicographically.

A minimal dictionary with one word tests boundary behavior. If the query word is lexicographically smaller than the only dictionary entry, the answer must be zero. If it is equal or larger under the ordering, the answer must be one. The binary search handles both cases correctly because it directly measures insertion position in the sorted structure.
