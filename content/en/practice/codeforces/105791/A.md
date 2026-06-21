---
title: "CF 105791A - Autocomplete"
description: "We are given a fixed dictionary of words and then a sequence of query strings. For each query, we want to know how many words in the dictionary start with that query as a prefix."
date: "2026-06-21T14:54:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105791
codeforces_index: "A"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2025"
rating: 0
weight: 105791
solve_time_s: 54
verified: true
draft: false
---

[CF 105791A - Autocomplete](https://codeforces.com/problemset/problem/105791/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed dictionary of words and then a sequence of query strings. For each query, we want to know how many words in the dictionary start with that query as a prefix. A word counts if it has the query string as its beginning segment, even if it is exactly equal to the query or longer than it.

The input size makes it clear that both the dictionary and the query list can contain up to one hundred thousand strings, and the total number of characters across all strings is bounded by one million. This rules out any approach that repeatedly scans the full dictionary per query. A naive check that compares every query against every word character by character would require up to roughly $10^{10}$ comparisons in the worst case, which is far beyond what can run in one second in Python.

A more subtle constraint comes from string length distribution. Even if individual strings are short, the number of comparisons still scales with $N \cdot Q$, which is the dominant bottleneck. Any acceptable solution must reduce each query to at most logarithmic or constant-time work after preprocessing.

A few edge situations matter for correctness. If the query string is longer than all dictionary words, the answer must be zero. For example, if the dictionary contains "a", "ab", "abc" and the query is "abcd", the answer is zero because no word can match that prefix. Another case is when multiple identical words exist in the dictionary. Each occurrence should be counted separately since the problem asks for the number of words, not distinct words. Finally, empty prefixes are not present in the input, so we do not need to handle that case explicitly.

## Approaches

The most direct idea is to process each query by scanning every dictionary word and checking whether it starts with the query. This is correct because it directly tests the definition of a prefix. The issue is cost. Each check may require comparing up to the full length of the query, so one query costs $O(N \cdot L)$, and across all queries this becomes too slow.

The key observation is that prefix queries become easy if the dictionary is sorted lexicographically. In sorted order, all words sharing a prefix form a contiguous block. This happens because lexicographic order groups strings by their earliest differing character. Once sorted, answering a query reduces to finding the first position where a word with that prefix could appear and the first position where words stop matching that prefix.

This reduces the problem to two binary searches. One search finds the left boundary, the first word not smaller than the prefix. The second search finds the right boundary, which can be simulated by searching for the smallest string strictly greater than any string that starts with the prefix. A standard trick is to append a character larger than 'z' to the prefix, such as '{', because ASCII ordering guarantees all lowercase strings come before it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot Q \cdot L)$ | $O(1)$ extra | Too slow |
| Sorted + Binary Search | $O((N+Q)\log N)$ | $O(1)$ extra beyond storage | Accepted |

## Algorithm Walkthrough

We rely on sorting and binary search boundaries over lexicographically ordered strings.

1. Read all dictionary words and sort them lexicographically. This groups all words with the same prefix into contiguous segments, which is what makes range counting possible.
2. For each query string, compute the left boundary using binary search. This finds the first index in the sorted array where a word is not smaller than the query string.
3. Construct a helper string by appending a character strictly larger than any lowercase letter, for example '{', to the query. This defines an upper bound for all words that share the prefix.
4. Compute the right boundary using binary search on this modified string. This finds the first index where a word is not smaller than the next lexicographic bucket after all words starting with the prefix.
5. The answer for the query is the difference between the right boundary and left boundary. This difference counts exactly the number of dictionary words whose prefix matches the query.

### Why it works

Sorting guarantees that all strings with a common prefix occupy a continuous interval in lexicographic order. The left boundary isolates the first candidate that could match the prefix. The artificial upper-bound string ensures that every string starting with the prefix is strictly less than it, so the right boundary stops immediately after the last matching string. The subtraction therefore counts exactly the size of that contiguous block.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    words = [input().strip() for _ in range(n)]
    words.sort()

    import bisect

    out = []
    for _ in range(q):
        s = input().strip()
        left = bisect.bisect_left(words, s)
        right = bisect.bisect_left(words, s + '{')
        out.append(str(right - left))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core implementation hinges on Python’s lexicographic string comparison. Sorting the list once ensures that binary search behaves consistently over string order. The function `bisect_left(words, s)` finds the first position where `s` could be inserted without breaking order, which corresponds exactly to the first word not smaller than `s`.

The second boundary uses `s + '{'`, which is strictly greater than any lowercase string beginning with `s`. This avoids having to compute a complex next-prefix function. A common mistake is to try `s + 'z'`, which fails when the prefix already ends in 'z'. Using '{' avoids all such edge cases cleanly.

## Worked Examples

Consider the input:

```
4 4
a
ab
abc
abcd
a
ab
abc
b
```

After sorting, the dictionary remains the same.

For query "a", the left boundary is index 0 and the right boundary for "a{" is index 4, so the result is 4.

| Query | Left | Right | Result |
| --- | --- | --- | --- |
| a | 0 | 4 | 4 |
| ab | 1 | 4 | 3 |
| abc | 2 | 4 | 2 |
| b | 4 | 4 | 0 |

This trace shows how each prefix defines a shrinking segment of the same contiguous block.

Now consider:

```
5 3
dog
deer
deal
cat
car
de
ca
z
```

After sorting:

```
car, cat, deal, deer, dog
```

For "de", left is 2 and right is 4, giving 2. For "ca", left is 0 and right is 2, giving 2. For "z", both boundaries are 5, giving 0.

This confirms that non-existent prefixes correctly map to empty ranges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((N+Q)\log N)$ | Sorting dominates with $N \log N$, each query uses two binary searches |
| Space | $O(1)$ extra | Only storing input array beyond input storage |

The constraints allow up to $10^5$ strings and queries, and sorting plus binary search comfortably fits within time limits. The total character limit of one million ensures that string handling overhead remains manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys
    old = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# sample-like test
assert run("""4 4
a
ab
abc
abcd
a
ab
abc
b
""") == "4\n3\n2\n0"

# single element exact match
assert run("""1 2
aaaa
a
aaaa
""") == "1\n1"

# no matches
assert run("""3 2
dog
cat
mouse
z
doz
""") == "0\n0"

# identical words
assert run("""4 1
a
a
a
a
a
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single word repeated | 1/1 | duplicate counting |
| no prefix match | 0 | empty ranges |
| multiple identical strings | correct accumulation | frequency handling |
| mixed prefixes | correct segmentation | boundary correctness |

## Edge Cases

One edge case is when all dictionary words are identical. For input where all words are "a" and the query is "a", both boundaries collapse to the full array range, so the result correctly equals the number of occurrences.

Another edge case is when the query is lexicographically larger than any dictionary word. For example, dictionary ["a", "b"] and query "z". Both binary search boundaries return the end of the array, producing zero without special handling.

A final case is when the query itself is a full word present in the dictionary. Because the left boundary includes equality, the matching word is counted correctly, and the right boundary excludes only non-matching extensions, ensuring exact matches are included in the result.
