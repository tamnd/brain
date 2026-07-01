---
title: "CF 104066E - \u0421\u0430\u043c\u0430\u044f \u0441\u0442\u0440\u0430\u0448\u043d\u0430\u044f \u0438\u0441\u0442\u043e\u0440\u0438\u044f"
description: "We are given a sequence of words forming a story, where words are separated by single spaces and each word consists only of lowercase Latin letters. The entire story can be viewed as one long string, but spaces are special characters that split it into word boundaries."
date: "2026-07-02T03:14:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104066
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 (\u0431\u0430\u0437\u043e\u0432\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f)"
rating: 0
weight: 104066
solve_time_s: 45
verified: true
draft: false
---

[CF 104066E - \u0421\u0430\u043c\u0430\u044f \u0441\u0442\u0440\u0430\u0448\u043d\u0430\u044f \u0438\u0441\u0442\u043e\u0440\u0438\u044f](https://codeforces.com/problemset/problem/104066/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of words forming a story, where words are separated by single spaces and each word consists only of lowercase Latin letters. The entire story can be viewed as one long string, but spaces are special characters that split it into word boundaries.

The task is to answer queries about positions inside this combined string. Each query gives a global character index in the full story string (including letters but typically ignoring spaces for indexing purposes in the query model described in the problem statement), and we must determine two things: which word contains that character and the position of that character inside that word.

So the core transformation is from a linear index in the concatenated representation into a pair of coordinates: word index and position within that word.

The constraints indicate up to 10^5 words and up to 5·10^5 queries, with total character length at most 10^6. This immediately implies that any per-query linear scan over words or characters is too slow. A solution must preprocess the structure once and answer each query in constant or logarithmic time. A linear scan per query would reach 5·10^11 operations in the worst case, which is not viable under a 1 second limit.

A naive but common mistake is to treat spaces as normal characters and forget that indexing jumps over them. Another subtle issue is off-by-one indexing when mapping prefix sums to segments, especially when a query hits exactly the boundary between words.

Edge cases appear when words have length 1, or when all words are very short, making boundaries frequent. For example, if the story is `"a b c"`, the global indices map tightly and boundary conditions matter. A query pointing exactly at the last character of a word must not spill into the next word.

## Approaches

The brute-force idea is straightforward: concatenate the entire story into a string, then for each query scan forward until we reach the k-th character. While correct, this requires O(n) work per query in the worst case, because locating a position requires traversing from the beginning or iterating through words until the correct segment is found. With up to 5·10^5 queries and up to 10^6 total length, this degenerates into repeated scanning of the same prefix structure, leading to repeated work.

The key observation is that word boundaries are static. Once we know prefix sums of word lengths, every query becomes a search for the first prefix that exceeds a given position. This converts the problem into repeated range location in a monotonic array, which can be solved either with binary search or more simply with a two-pointer sweep if queries are processed in order.

Because the total size is only 10^6, prefix sums plus binary search per query is sufficient and simple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan per Query | O(n·m) | O(n) | Too slow |
| Prefix Sum + Binary Search | O(n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first convert the sequence of words into a prefix structure that describes where each word begins and ends in the flattened story string without spaces.

We maintain an array `pref`, where `pref[i]` stores the total number of characters in the first `i` words.

Then each query becomes a search problem over this array.

1. Build an array of word lengths. Each word contributes its character count.
2. Construct prefix sums so that `pref[i]` is the total number of characters in words `[1..i]`. This gives a monotonic increasing sequence.
3. For a query position `x`, find the smallest index `i` such that `pref[i] >= x`. This identifies the word that contains the character.
4. Once the word is found, compute the position inside the word as `x - pref[i-1]`.

The correctness of step 3 relies on the fact that prefix sums partition the global string into contiguous disjoint segments corresponding exactly to words.

A direct binary search is sufficient because `pref` is strictly increasing.

### Why it works

Each word occupies a contiguous interval in the flattened story string, and these intervals do not overlap. The prefix array encodes the right endpoint of each interval. Locating the first prefix that exceeds or equals a query index is equivalent to finding the interval that contains that index. Since intervals are contiguous and ordered, this mapping is unique and deterministic.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    words = input().split()

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + len(words[i - 1])

    def find_word(x):
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if pref[mid] >= x:
                hi = mid
            else:
                lo = mid + 1
        return lo

    for _ in range(m):
        x = int(input())
        i = find_word(x)
        prev = pref[i - 1]
        print(i, x - prev)

if __name__ == "__main__":
    solve()
```

The implementation separates preprocessing and query handling cleanly. The prefix array is built once in O(n). Each query uses binary search over word boundaries.

The function `find_word` is carefully written to avoid off-by-one errors. The condition `pref[mid] >= x` ensures we land on the first word whose right boundary is not before the query index.

The subtraction `x - pref[i - 1]` converts the global position into a local offset inside the selected word.

## Worked Examples

Consider a small story with words:

Input:

```
3 3
hell spirits fear
1
7
10
```

Here prefix sums are:

| i | word | length | pref[i] |
| --- | --- | --- | --- |
| 0 | - | - | 0 |
| 1 | hell | 4 | 4 |
| 2 | spirits | 7 | 11 |
| 3 | fear | 4 | 15 |

Query traces:

| x | lo | hi | mid decisions | found word i | position |
| --- | --- | --- | --- | --- | --- |
| 1 | 1-3 | ... | converges to 1 | 1 | 1 |
| 7 | 1-3 | pref[2]=11 ≥7 → word 2 | 2 | 7 - 4 = 3 |  |
| 10 | ... | pref[2]=11 ≥10 → word 2 | 2 | 10 - 4 = 6 |  |

The table shows how binary search narrows down to the correct prefix segment. Each result confirms that indices are interpreted relative to word boundaries rather than the full concatenation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log n) | prefix construction is linear, each query uses binary search |
| Space | O(n) | prefix array stores one value per word |

The constraints allow up to 10^6 total characters and 5·10^5 queries, so logarithmic search per query is easily fast enough. Memory usage is dominated by storing word lengths and prefix sums.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()

    n, m = map(int, sys.stdin.readline().split())
    words = sys.stdin.readline().split()

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + len(words[i - 1])

    def find_word(x):
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if pref[mid] >= x:
                hi = mid
            else:
                lo = mid + 1
        return lo

    for _ in range(m):
        x = int(sys.stdin.readline())
        i = find_word(x)
        output.write(f"{i} {x - pref[i - 1]}\n")

    return output.getvalue()

# sample-like test
assert run("3 3\nhell spirits fear\n1\n7\n10\n") == "1 1\n2 3\n2 6\n"

# minimum size
assert run("1 3\na\n1\n1\n1\n") == "1 1\n1 1\n1 1\n"

# boundary test
assert run("2 2\naa b\n2\n3\n") == "1 2\n2 1\n"

# all equal lengths
assert run("4 4\na b c d\n1\n2\n3\n4\n") == "1 1\n2 1\n3 1\n4 1\n"

# long word
assert run("1 1\nabcde\n5\n") == "1 5\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single word repeats | 1 1 | minimal case correctness |
| boundary transitions | correct word switching | off-by-one at edges |
| equal-length words | sequential mapping | prefix correctness |
| long word query | last position | end boundary handling |

## Edge Cases

A critical edge case is when a query lands exactly on the last character of a word. In a story like `"abc def"`, the prefix sums are `[3, 6]`. A query `x = 3` must map to the first word, not the second. The condition `pref[mid] >= x` ensures that equality is resolved toward the left boundary word, preventing accidental overflow into the next word.

Another subtle case is when all words have length 1. Then prefix sums are strictly `1, 2, 3, ...`, and binary search must still correctly map each query to its exact word. The algorithm handles this because each index matches a unique prefix value.

Finally, when there is only one word, every query trivially maps to word 1, and position is identical to the query index. The implementation does not require special casing, as prefix array degenerates correctly to `[0, len(word)]`.
