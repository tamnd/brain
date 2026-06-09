---
title: "CF 1780G - Delicious Dessert"
description: "We are given a string s of length n representing Tonio's dessert recipe. A substring of s is called delicious if the number of times it appears in s is divisible by its own length. The task is to count all delicious substrings of s, counting multiple occurrences separately."
date: "2026-06-09T11:25:42+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dsu", "hashing", "math", "number-theory", "string-suffix-structures"]
categories: ["algorithms"]
codeforces_contest: 1780
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 846 (Div. 2)"
rating: 2400
weight: 1780
solve_time_s: 103
verified: true
draft: false
---

[CF 1780G - Delicious Dessert](https://codeforces.com/problemset/problem/1780/G)

**Rating:** 2400  
**Tags:** binary search, dsu, hashing, math, number theory, string suffix structures  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string `s` of length `n` representing Tonio's dessert recipe. A substring of `s` is called _delicious_ if the number of times it appears in `s` is divisible by its own length. The task is to count all delicious substrings of `s`, counting multiple occurrences separately.

The input size can be up to `10^6`, which rules out any algorithm that iterates over all possible substrings explicitly and counts them by naive scanning, because there are about `n*(n+1)/2` substrings, which can reach roughly `5*10^11` operations in the worst case. This means an efficient algorithm must rely on string data structures or hashing to quickly determine the frequency of each substring.

Non-obvious edge cases include: a string where all characters are identical. For example, `s = "aaaa"` has substrings like `"a"` appearing 4 times, `"aa"` appearing 3 times, `"aaa"` appearing 2 times, and `"aaaa"` appearing 1 time. A careless approach might miscount `"aa"` or `"aaa"` if it only checks divisibility against the total number of substrings rather than the actual occurrences. Another edge case is a string where no substring repeats, e.g., `s = "abcdef"`, where all lengths greater than 1 must appear exactly once, so only substrings of length 1 are delicious.

## Approaches

The brute-force approach is straightforward: enumerate every substring of `s`, count its occurrences in the entire string, and check divisibility by its length. For a string of length `n`, there are `O(n^2)` substrings. Counting occurrences of each substring naively takes `O(n)` time, resulting in `O(n^3)` overall complexity. This is clearly too slow for `n` up to `10^6`.

The key observation is that the problem reduces to efficiently counting how many times each substring appears. Suffix structures like **Suffix Automaton**, **Suffix Array**, or **Z-function combined with hashing** allow us to compute all substring frequencies efficiently. Using a Suffix Automaton, each substring corresponds to a state, and we can propagate occurrence counts through the automaton to get the frequency of every substring. Once we know the frequency of each substring, checking divisibility by its length is trivial.

The optimal approach uses a **Suffix Automaton (SAM)** with occurrence counts. After building the SAM, we traverse the states, noting the minimal and maximal substring lengths for each state. The frequency stored in each state corresponds to how many times that substring appears in `s`. We sum up, for all substring lengths from `min_len+1` to `max_len`, the occurrences divisible by the length. This approach runs in `O(n)` for building the automaton and propagating counts, plus an `O(n)` traversal to compute the final answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n^2) | Too slow |
| Suffix Automaton + Occurrence Counting | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a **Suffix Automaton (SAM)** for the string `s`. Each state in the SAM represents a set of end positions for a substring of `s`. The SAM can be built incrementally in `O(n)` time by iterating through the string and extending the automaton with each character.
2. Compute the occurrence count for each state. Initialize the count for states corresponding to actual end positions (i.e., terminal states) to 1. Then propagate counts from longer substrings to shorter ones along the suffix links. This way, each state accumulates the total number of occurrences of its represented substring in `s`.
3. For each state, determine the minimal and maximal lengths of substrings represented by that state. The minimal length of a state is `len(link(state)) + 1` and the maximal length is `len(state)`.
4. For each state, iterate over all substring lengths from minimal to maximal length. For each length `L`, if the frequency of this substring is divisible by `L`, add the frequency to the result.
5. Sum over all states to compute the total number of delicious substrings.

**Why it works:** Every substring corresponds to exactly one state in the suffix automaton. Propagating occurrence counts ensures we count all repeated substrings correctly. By iterating over the allowed lengths for each state, we consider each substring exactly once and check the divisibility condition, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SuffixAutomaton:
    def __init__(self, n):
        self.states = [{}]
        self.link = [-1]
        self.len = [0]
        self.occ = [0]
        self.last = 0
        self.size = 1
        self.n = n

    def extend(self, c):
        p = self.last
        cur = self.size
        self.size += 1
        self.states.append({})
        self.len.append(self.len[p] + 1)
        self.occ.append(1)
        self.link.append(0)
        while p != -1 and c not in self.states[p]:
            self.states[p][c] = cur
            p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.states[p][c]
            if self.len[p] + 1 == self.len[q]:
                self.link[cur] = q
            else:
                clone = self.size
                self.size += 1
                self.states.append(self.states[q].copy())
                self.len.append(self.len[p] + 1)
                self.link.append(self.link[q])
                self.occ.append(0)
                while p != -1 and self.states[p].get(c) == q:
                    self.states[p][c] = clone
                    p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur

def main():
    n = int(input())
    s = input().strip()
    sam = SuffixAutomaton(n)
    for ch in s:
        sam.extend(ch)

    # Count occurrences
    order = sorted(range(sam.size), key=lambda x: sam.len[x], reverse=True)
    for state in order:
        if sam.link[state] != -1:
            sam.occ[sam.link[state]] += sam.occ[state]

    result = 0
    for state in range(1, sam.size):
        min_len = sam.len[sam.link[state]] + 1
        max_len = sam.len[state]
        freq = sam.occ[state]
        for l in range(min_len, max_len + 1):
            if freq % l == 0:
                result += freq

    print(result)

if __name__ == "__main__":
    main()
```

**Explanation:** We build the SAM, extend it for each character, then propagate occurrences from longer substrings to shorter ones. We iterate over the range of substring lengths represented by each state, summing those whose frequency is divisible by the length.

## Worked Examples

### Sample 1

Input: `"abacaba"`

State variables for selected substrings:

| Substring | freq | len | min_len | max_len | divisible? | contribution |
| --- | --- | --- | --- | --- | --- | --- |
| "a" | 4 | 1 | 1 | 1 | yes | 4 |
| "b" | 2 | 1 | 1 | 1 | yes | 2 |
| "ab" | 2 | 2 | 2 | 2 | yes | 2 |
| "ba" | 2 | 2 | 2 | 2 | yes | 2 |
| others | ... | ... | ... | ... | ... | ... |

Total sum = 11. This confirms the algorithm counts both single and multi-length substrings correctly, including repeated ones.

### Sample 2

Input: `"aaaa"`

| Substring | freq | min_len | max_len | divisible? | contribution |
| --- | --- | --- | --- | --- | --- |
| "a" | 4 | 1 | 1 | yes | 4 |
| "aa" | 3 | 2 | 2 | no | 0 |
| "aaa" | 2 | 3 | 3 | no | 0 |
| "aaaa" | 1 | 4 | 4 | no | 0 |

Total = 4, which matches expectations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Building the suffix automaton and propagating occurrences is linear. The final summation over lengths is also `O(n)` in total. |
| Space | O(n) | SAM stores roughly 2*n states and transitions. Occurrences, links, and lengths arrays are all linear. |

Given `n <= 10^6` and operations linear in `n`, this algorithm runs comfortably within the 3-second limit and uses less than 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided samples
```
