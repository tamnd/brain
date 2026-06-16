---
title: "CF 977B - Two-gram"
description: "We are given a string of uppercase English letters, and we are asked to look at every adjacent pair of characters in it. Each such adjacent pair forms a “two-letter pattern”, for example the string “ABAC” contains “AB”, “BA”, and “AC”."
date: "2026-06-17T01:26:27+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 977
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 479 (Div. 3)"
rating: 900
weight: 977
solve_time_s: 75
verified: false
draft: false
---

[CF 977B - Two-gram](https://codeforces.com/problemset/problem/977/B)

**Rating:** 900  
**Tags:** implementation, strings  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of uppercase English letters, and we are asked to look at every adjacent pair of characters in it. Each such adjacent pair forms a “two-letter pattern”, for example the string “ABAC” contains “AB”, “BA”, and “AC”.

The task is to find which of these two-letter patterns appears most frequently as a contiguous substring. Since substrings are defined by consecutive positions, overlaps are naturally allowed, so a pattern like “AAA” contains “AA” twice.

The output is not the count itself, but any pattern that achieves the maximum frequency. If multiple patterns tie, any one of them is acceptable.

The input size is small, with at most 100 characters. That immediately suggests that even quadratic reasoning is sufficient, since the total number of adjacent pairs is only n−1, at most 99.

A subtle point is that we are not searching over all possible 26×26 patterns independently. We only care about those that actually appear in the string as adjacent substrings. This removes any ambiguity about patterns like “ZZ” that might not exist in the input at all.

Edge cases are mostly about short strings. When n = 2, there is exactly one two-gram, and it must be returned. When all characters are identical, for example “AAAAA”, the correct answer is “AA”, and it appears multiple times due to overlap. A careless implementation might try to deduplicate occurrences or treat them as non-overlapping, which would be incorrect.

## Approaches

A brute-force idea would be to take every possible pair of positions (i, j) and check whether s[i:i+2] matches every other substring occurrence. That would lead to O(n²) candidates, and for each candidate another O(n) scan, resulting in O(n³). Even though n is small, this is unnecessary and conceptually clumsy for such a direct counting task.

A more natural brute-force is to generate all substrings of length two and count them using a dictionary. This reduces the problem to a frequency count over n−1 elements. Each substring extraction is O(1), so the total complexity becomes linear in n.

The key observation is that we are not constructing anything global or dependent on long-range structure. Every valid answer is fully determined by local adjacency, so a single pass is sufficient. This reduces the problem to counting frequencies in a fixed-size stream of pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration + recomparison | O(n³) | O(1) | Too slow |
| Sliding count of adjacent pairs | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the string from left to right, considering each index i from 0 to n−2, and extract the two-letter substring s[i]s[i+1]. This step converts the problem into a stream of overlapping observations.
2. Maintain a frequency map that records how many times each two-letter pattern has been seen so far. Each new substring increments its counter.
3. Track the currently best pattern and its frequency while scanning. When a pattern’s frequency exceeds the best so far, update both the best pattern and the best count.
4. After processing all adjacent pairs, output the stored best pattern.

The reason we can safely update the answer greedily during scanning is that future updates only depend on future pairs, and counts only ever increase. There is no scenario where a previously optimal pair becomes invalid or decreases in frequency.

### Why it works

Each two-gram occurrence is independent and determined solely by a fixed window of size two. The algorithm counts each such window exactly once. Since the frequency map stores exact counts, and we always maintain the maximum over all seen values, the final stored pair must be one of the global maxima.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    freq = {}
    best = ""
    best_cnt = 0

    for i in range(n - 1):
        pair = s[i:i+2]
        freq[pair] = freq.get(pair, 0) + 1

        if freq[pair] > best_cnt:
            best_cnt = freq[pair]
            best = pair

    print(best)

if __name__ == "__main__":
    solve()
```

The solution uses a single pass over the string. The substring extraction `s[i:i+2]` is constant time since the slice length is fixed. The dictionary maintains exact frequencies, and the best pair is updated only when a strictly larger count is observed, ensuring deterministic behavior without needing a second pass.

A common mistake is iterating up to n instead of n−1, which would attempt to access an out-of-range substring. Another is forgetting that overlapping pairs are valid, which is naturally handled here because every index contributes exactly one pair starting at it.

## Worked Examples

### Example 1

Input:

```
7
ABACABA
```

We track pairs step by step.

| i | pair | freq after update | best |
| --- | --- | --- | --- |
| 0 | AB | AB:1 | AB |
| 1 | BA | BA:1, AB:1 | AB |
| 2 | AC | AC:1, AB:1, BA:1 | AB |
| 3 | CA | CA:1, ... | AB |
| 4 | AB | AB:2 | AB |
| 5 | BA | BA:2 | AB or BA (tie) |

The final answer is “AB”, though “BA” would also be valid depending on tie handling.

This trace shows how overlapping occurrences naturally accumulate counts and how the maximum emerges incrementally.

### Example 2

Input:

```
5
AAAAA
```

| i | pair | freq after update | best |
| --- | --- | --- | --- |
| 0 | AA | AA:1 | AA |
| 1 | AA | AA:2 | AA |
| 2 | AA | AA:3 | AA |
| 3 | AA | AA:4 | AA |

The algorithm correctly captures overlap, since each adjacent position contributes a new valid occurrence.

This demonstrates that repeated identical letters do not require special handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over n−1 adjacent pairs, constant work per step |
| Space | O(1) | At most 26×26 possible pairs, effectively bounded constant |

The constraints cap n at 100, but the linear solution already operates comfortably within limits even for much larger inputs. Memory usage is constant because the alphabet is fixed and the number of possible two-grams is bounded.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys

    # capture output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout

# provided sample
assert run("7\nABACABA\n") in ["AB", "BA"]

# minimum length
assert run("2\nAB\n") == "AB"

# all same characters
assert run("5\nAAAAA\n") == "AA"

# clear dominant pattern
assert run("6\nABCABC\n") in ["AB", "BC", "CA"]

# tie case
assert run("4\nAABB\n") in ["AA", "AB", "BB"]

# alternating pattern
assert run("6\nABABAB\n") in ["AB", "BA"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 AB | AB | minimum edge case |
| AAAAA | AA | overlapping counting |
| ABCABC | AB/BC/CA | cyclic distribution |
| ABABAB | AB/BA | alternating tie behavior |

## Edge Cases

For a string of length two such as “XY”, the loop runs exactly once. The only pair is “XY”, so it becomes the answer immediately with frequency 1.

For repeated characters like “AAAAA”, each index contributes “AA”, so counts accumulate to 4. The algorithm never tries to deduplicate occurrences; it simply increments each observed window.

For alternating strings like “ABABAB”, both “AB” and “BA” occur multiple times. The algorithm updates the best value whenever a strict increase occurs, so the first pair to reach the maximum remains a valid output.
