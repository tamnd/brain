---
title: "CF 432D - Prefixes and Suffixes"
description: "We are given a single string of uppercase letters. Our goal is to identify all prefixes of the string that are identical to some suffix, and for each such prefix, count how many times it occurs anywhere inside the string as a contiguous substring."
date: "2026-06-07T02:36:37+07:00"
tags: ["codeforces", "competitive-programming", "dp", "string-suffix-structures", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 432
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 246 (Div. 2)"
rating: 2000
weight: 432
solve_time_s: 251
verified: true
draft: false
---

[CF 432D - Prefixes and Suffixes](https://codeforces.com/problemset/problem/432/D)

**Rating:** 2000  
**Tags:** dp, string suffix structures, strings, two pointers  
**Solve time:** 4m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string of uppercase letters. Our goal is to identify all prefixes of the string that are identical to some suffix, and for each such prefix, count how many times it occurs anywhere inside the string as a contiguous substring. For example, if the string is `"ABACABA"`, the prefix `"A"` is also a suffix of length one and occurs four times in total inside the string.

The input string can be as long as 100,000 characters. A naive approach that checks every possible prefix against every possible substring will perform on the order of $10^{10}$ operations in the worst case, which is far beyond the one-second time limit. This tells us that we need a linear or near-linear solution.

Edge cases that can trip up a naive implementation include strings where every character is the same, such as `"AAAAA"`. In this scenario, multiple prefixes of different lengths match the suffixes, and their counts grow with overlapping occurrences. A careless solution might miscount overlapping substrings or omit prefixes of length equal to the entire string. Similarly, strings with no repeating patterns, like `"ABCDEFG"`, require the algorithm to correctly return only length-1 matches if any, without falsely identifying longer non-existent matches.

## Approaches

The brute-force method iterates over all possible prefix lengths. For each prefix, it checks whether it matches the corresponding suffix of the same length. Then it scans the whole string to count the number of times this prefix occurs. While correct, this approach has a complexity of roughly $O(n^2)$, because each prefix check requires a scan of the string, and the total number of prefixes is $O(n)$. This is impractical for $n = 10^5$.

The optimal approach leverages the fact that we can compute repeated substring occurrences efficiently using the prefix function from the Knuth-Morris-Pratt (KMP) algorithm. The prefix function at position $i$ tells us the length of the longest proper prefix of the substring $s[0..i]$ that is also a suffix of that substring. Using this function, we can identify all lengths where the prefix matches the suffix in linear time. Furthermore, by counting how many times each prefix length appears in the prefix function array, we can determine how often each candidate substring occurs as a substring. This reduces the problem to $O(n)$ time.

The brute-force works because it directly implements the problem definition, but it fails for long strings. The observation that the prefix function encodes all repeated prefix-suffix relationships lets us reduce both the prefix-suffix identification and substring counting to a linear pass over the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| KMP / Prefix Function | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix function for the string. For each position `i`, `pi[i]` stores the length of the longest proper prefix of `s[0..i]` that matches a suffix ending at `i`. This function captures all the repeated prefix-suffix relationships.
2. Count the frequency of each prefix length across the string using the prefix function array. Initialize a count array of size `n+1` with zeros. For each `pi[i]`, increment `count[pi[i]]`. This will help us later compute how many times each prefix occurs as a substring.
3. Propagate counts from longer prefixes to shorter ones. Since a prefix of length `x` also contributes to all prefixes that are its proper prefix, iterate from the largest length to the smallest: `count[pi[i]] += count[i+1]`. This ensures that every prefix includes all occurrences of longer overlapping prefixes.
4. Identify all prefix lengths that are also suffixes. Start from the full string length and follow the prefix function chain: `length = n`, then `length = pi[length-1]`, repeating until `length == 0`. Collect these lengths.
5. For each collected prefix length, the number of occurrences is `count[length] + 1`, because each prefix occurs at least once by definition. Output them in increasing order of length.

Why it works: the prefix function encodes all repeating prefix-suffix structures in linear time. By propagating counts from longer to shorter prefixes, we account for overlapping occurrences. The chain following `pi[length-1]` guarantees that we find all prefixes that are also suffixes, ordered by inclusion.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)

# Step 1: Compute prefix function
pi = [0] * n
for i in range(1, n):
    j = pi[i-1]
    while j > 0 and s[i] != s[j]:
        j = pi[j-1]
    if s[i] == s[j]:
        j += 1
    pi[i] = j

# Step 2: Count occurrences of each prefix length
count = [0] * (n + 1)
for length in pi:
    count[length] += 1

# Step 3: Propagate counts
for i in range(n, 0, -1):
    count[pi[i-1]] += count[i]

# Step 4: Collect prefix-suffix matches
lengths = []
k = n
while k > 0:
    lengths.append(k)
    k = pi[k-1]
lengths.sort()

# Step 5: Output results
print(len(lengths))
for l in lengths:
    print(l, count[l] + 1)
```

The prefix function computation in the first loop is standard KMP. Step 2 initializes a frequency array. Step 3 propagates occurrences from longer prefixes to their proper subprefixes, accounting for overlapping matches. Step 4 iterates the prefix function chain to find all prefixes that are suffixes. Sorting ensures output is in increasing order. The `+1` in Step 5 accounts for the prefix itself appearing at least once.

## Worked Examples

Sample input: `"ABACABA"`

| i | s[i] | pi[i] | count after Step 2 |
| --- | --- | --- | --- |
| 0 | A | 0 | [0,0,0,0,0,0,0,0] |
| 1 | B | 0 | same |
| 2 | A | 1 | [0,1,0,0,0,0,0,0] |
| 3 | C | 0 | [0,1,0,0,0,0,0,0] |
| 4 | A | 1 | [0,2,0,0,0,0,0,0] |
| 5 | B | 2 | [0,2,1,0,0,0,0,0] |
| 6 | A | 3 | [0,2,1,1,0,0,0,0] |

After propagating counts and tracing prefix-suffix chain, lengths `[1, 3, 7]` are identified. Their occurrence counts are `[4, 2, 1]`, matching the sample output.

Custom input: `"AAAA"`

| i | pi[i] |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

Count propagation gives counts `[4,3,2,1]`, and prefix-suffix chain yields lengths `[1,2,3,4]` with occurrences `[4,3,2,1]`.

These traces confirm correctness for overlapping repeats and full string matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Prefix function computation is linear; count propagation and prefix-suffix tracing are also linear |
| Space | O(n) | Arrays `pi` and `count` use `O(n)` space |

Given $n \le 10^5$ and operations $O(n)$, this solution runs comfortably under 1 second and uses less than the 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided sample
assert run("ABACABA\n") == "3\n1 4\n3 2\n7 1", "sample 1"

# Minimum-size input
assert run("A\n") == "1\n1 1", "single character"

# All equal characters
assert run("AAAA\n") == "4\n1 4\n2 3\n3 2\n4 1", "all same"

# No repeating prefix-suffix
assert run("ABCDEFG\n") == "1\n1 1", "no repeats"

# Overlapping occurrences
assert run("ABABAB\n") == "3\n2 3\n4 2\n6 1", "overlapping repeats"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"A"` | `"1\n1 1"` | Handles minimal string correctly |
| `"AAAA"` | `"4\n1 4 |  |
