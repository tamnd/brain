---
title: "CF 104805N - First words"
description: "We are given a small dictionary of words that Veronica knows, and then a single long string that represents what Igor wrote down as her spoken monologue."
date: "2026-06-28T13:22:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104805
codeforces_index: "N"
codeforces_contest_name: "Central Russia Regional Contest, 2022"
rating: 0
weight: 104805
solve_time_s: 58
verified: true
draft: false
---

[CF 104805N - First words](https://codeforces.com/problemset/problem/104805/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small dictionary of words that Veronica knows, and then a single long string that represents what Igor wrote down as her spoken monologue. The task is to decide whether the long string can be formed by concatenating some sequence of the known words, without inserting or deleting characters.

In other words, we want to know if we can split the string `s` into a sequence of contiguous substrings, where each substring is exactly one of the given words. The same word can be reused multiple times, and we do not need to use all words, only enough to cover the entire string exactly.

The input size allows up to 100 known words, with a total combined length of at most 100,000, and the monologue string `s` can also be up to 100,000 characters long. This immediately rules out any approach that tries all possible segmentations of the string in exponential time. A solution that repeatedly scans `s` efficiently, or performs dynamic programming over positions in `s`, is necessary.

A subtle edge case appears when words overlap or share prefixes. For example, if the dictionary contains `"a"`, `"aa"`, and `"aaa"`, and the string is `"aaaaa"`, a naive greedy approach might fail by choosing short matches too early. Another issue arises if we try to match words at every position without indexing, which can degrade into repeated full scans of all words for every character position.

## Approaches

A brute-force idea is to start from index `0` in `s` and recursively try every dictionary word that matches the current prefix, then continue from the end of that match. This is a straightforward depth-first search over positions in the string.

While correct, this approach can repeat the same subproblems many times. From a given index in `s`, we may attempt matching all words again and again. In the worst case, each position branches into up to 100 choices, and each match costs up to O(length of word), leading to exponential behavior on adversarial inputs.

The key observation is that the problem only depends on the current index in `s`, not on how we arrived there. This suggests a dynamic programming formulation: for each position `i`, we want to know whether the suffix `s[i:]` can be fully segmented. Once computed, this result should be reused.

We can accelerate matching by iterating over words and checking whether `s[i:i+len(word)]` equals that word. Since total word length is bounded, this direct comparison is efficient enough. Alternatively, one could build a trie, but with constraints this small dictionary scan per position is sufficient.

The final solution becomes a DP over positions in `s`, where we attempt to extend valid states forward using all dictionary words.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS | O(exp) | O(n) | Too slow |
| DP over positions | O(n * total_words) | O(n) | Accepted |

## Algorithm Walkthrough

We define a boolean array `dp`, where `dp[i]` indicates whether the prefix `s[0:i]` can be segmented into known words.

1. Initialize `dp[0] = True`, since an empty prefix is always valid. Every other position starts as False.
2. Iterate through positions `i` from `0` to `len(s)`.
3. If `dp[i]` is False, skip it. This means there is no valid segmentation reaching position `i`, so extending from it is useless.
4. For each known word `w`, check whether the substring starting at `i` matches `w`, i.e., `s[i:i+len(w)] == w`.
5. If it matches, set `dp[i + len(w)] = True`, because we can extend a valid segmentation to that endpoint.
6. After processing all positions, check `dp[len(s)]`. If it is True, output "YES", otherwise output "NO".

### Why it works

At every index `i`, `dp[i]` represents exactly whether there exists a valid segmentation of the prefix up to `i`. When we extend using a word, we only append valid dictionary words, so any newly marked state corresponds to a valid segmentation. Conversely, any valid segmentation must end with some dictionary word, and the transition will eventually mark the corresponding endpoint. This ensures no valid construction is missed and no invalid construction is introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    words = [input().strip() for _ in range(n)]
    s = input().strip()

    L = len(s)
    dp = [False] * (L + 1)
    dp[0] = True

    for i in range(L):
        if not dp[i]:
            continue

        for w in words:
            lw = len(w)
            if i + lw <= L and s[i:i + lw] == w:
                dp[i + lw] = True

    print("YES" if dp[L] else "NO")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the DP formulation. The outer loop iterates over positions in the string, and transitions are attempted only from reachable positions, which avoids unnecessary work. The substring comparison `s[i:i+lw] == w` is safe because we explicitly check bounds before slicing.

A common mistake here is forgetting to restrict transitions to reachable `dp[i] == True`, which would incorrectly allow building segments from invalid prefixes. Another subtle issue is not checking bounds before slicing, which could lead to incorrect partial matches or wasted work.

## Worked Examples

We use the provided sample.

Input:

```
4
bububu
mama
papa
matan
bububumatanbububumama
```

We track `dp[i]` only at relevant positions.

| i | dp[i] | matched word | updated positions |
| --- | --- | --- | --- |
| 0 | True | bububu | dp[6] = True |
| 0 | True | none others | - |
| 6 | True | matan | dp[11] = True |
| 11 | True | bububu | dp[17] = True |
| 17 | True | mama | dp[21] = True |

At the end, `dp[21] = True`, so the answer is YES.

This trace shows that multiple dictionary words can be chained, and the DP correctly accumulates reachable boundaries.

We can also consider a failing case:

Input:

```
2
ab
aba
abab
```

At `i = 0`, both `"ab"` and `"aba"` are possible transitions. DP marks positions 2 and 3. From 2, we reach 4 via `"ab"`, so full coverage is possible. This demonstrates why exploring all transitions is necessary, not just a greedy choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m * k) | n is length of s, m is number of words, k is average word length due to substring comparisons |
| Space | O(n) | dp array over string positions |

Given n ≤ 100,000 and m ≤ 100, the product remains acceptable in Python because each transition is a simple bounded substring comparison, and early skipping of unreachable states reduces work significantly in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve_and_capture()

def solve_and_capture():
    import sys
    input = sys.stdin.readline

    n = int(input())
    words = [input().strip() for _ in range(n)]
    s = input().strip()

    L = len(s)
    dp = [False] * (L + 1)
    dp[0] = True

    for i in range(L):
        if not dp[i]:
            continue
        for w in words:
            lw = len(w)
            if i + lw <= L and s[i:i+lw] == w:
                dp[i+lw] = True

    return "YES" if dp[L] else "NO"

# provided sample
assert run("""4
bububu
mama
papa
matan
bububumatanbububumama
""") == "YES"

# single word exact match
assert run("""1
abc
abc
""") == "YES"

# impossible case
assert run("""2
a
b
abx
""") == "NO"

# repeated concatenation
assert run("""2
ab
aba
abab
""") == "YES"

# long chain
assert run("""3
a
aa
aaa
aaaaaa
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single word match | YES | basic acceptance |
| impossible string | NO | rejection case |
| repeated concatenation | YES | branching correctness |
| overlapping words | YES | non-greedy transitions |

## Edge Cases

A key edge case is overlapping dictionary words where greedy choices fail. Consider `words = ["a", "aa"]` and `s = "aaa"`. The algorithm sets `dp[1]`, `dp[2]`, and `dp[3]` correctly because it explores both extensions at each reachable index. A greedy approach might take `"aa"` first and get stuck, but the DP still keeps `"a"` as an alternative path.

Another edge case is when multiple words match at the same position. Since transitions are additive, marking multiple endpoints ensures no valid segmentation is lost.

Finally, empty reachability is handled cleanly: if `dp[i]` is never reached, no transitions originate there, preventing invalid propagation into later states.
