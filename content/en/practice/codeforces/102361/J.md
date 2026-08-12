---
title: "CF 102361J - MUV LUV EXTRA"
description: "Only the digits after the decimal point matter. Let that fractional part have length (n). A candidate repeating part must be a suffix of the observed fractional digits, because the repetition has to be continuing at the very end of what Sumika measured."
date: "2026-08-13T00:15:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "J"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 95
verified: true
draft: false
---

[CF 102361J - MUV LUV EXTRA](https://codeforces.com/problemset/problem/102361/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

Only the digits after the decimal point matter. Let that fractional part have length (n). A candidate repeating part must be a suffix of the observed fractional digits, because the repetition has to be continuing at the very end of what Sumika measured.

Suppose a candidate suffix has appeared for (p) digits in total, including a possibly incomplete final copy of the repeating block, and its shortest valid repeating block has length (l). Its reliability is

[
a p-b l.
]

For a fixed (p), the first term (ap) is already determined. Since (b>0), the best candidate ending at that position is always the one with the smallest possible period (l). The problem is thus to find, for every suffix length (p), the shortest period of that suffix.

The fractional part can contain up to (10^7) digits. An algorithm that examines all pairs of suffix length and period length is already too large at this scale. Even (O(n^2)) work would mean around (10^{14}) iterations at the maximum size, while an (O(n^3)) character-comparison implementation can reach roughly

[
\sum_{p=1}^{n}\frac{p(p-1)}2
=\frac{n(n+1)(n-1)}6
]

character comparisons, about (1.67\times10^{20}) when (n=10^7). We need a linear-time string algorithm, and we also need only linear memory.

There are several boundary cases that can make a seemingly correct implementation fail. The answer can be negative. For example, with

```
1 2
0.5
```

the only possible repeating part has (p=1,l=1), so the answer is (-1). Initializing the answer to zero would incorrectly produce zero.

The integer part must be ignored completely. For example,

```
5 3
123.1020
```

has exactly the same answer as the sample with `1.1020`, namely `9`. An implementation that processes the whole string would build the wrong periods.

The final repetition is allowed to be incomplete. For

```
2 1
0.102
```

the reversed fractional string is `201`. Its prefix of length three has shortest period two, so (p=3,l=2), giving (6-2=4). Restricting candidates to periods that divide the observed length would miss this kind of candidate.

A fractional part of length one is also valid. For

```
7 10
42.8
```

there is only (p=l=1), so the answer is (-3). This catches both the one-character boundary and negative answers.

## Approaches

A direct solution would enumerate every possible suffix length (p). For each suffix, it would try every possible repeating length (l), checking whether characters at distance (l) agree throughout the suffix. If the check succeeds, the candidate has reliability (ap-bl), and because (b) is positive we could keep the smallest valid (l) for that suffix.

This is correct because every legal repeating part is a period of some suffix, and checking all possible (l) examines every legal choice. The problem is the amount of repeated string comparison. For a suffix of length (p), testing all candidate lengths can require (\Theta(p^2)) character comparisons, giving (\Theta(n^3)) overall in the worst case. Even if substring comparisons were optimized enough to make each check constant time, simply examining every pair ((p,l)) would still be (O(n^2)), which is too large for (10^7) characters.

The useful observation is that every candidate is a suffix of the original fractional string. Reverse the fractional string. A suffix of length (p) in the original string becomes a prefix of length (p) in the reversed string. We have therefore transformed the problem into finding the shortest period of every prefix.

This is exactly the information provided by the KMP prefix function. For a prefix of length (p), let its prefix-function value be (k), the length of its longest proper prefix that is also a suffix. A border of length (k) means the first (k) characters and the last (k) characters coincide. The distance between those two equal regions is (p-k), and that distance is a period of the prefix. Since (k) is the longest possible border, (p-k) is the shortest possible period.

Thus, if the reversed fractional string is (t) and its prefix function is (\pi), then for every prefix length (p),

[
l=p-\pi[p-1].
]

The appeared length is simply (p), so its best reliability is

[
a p-b(p-\pi[p-1]).
]

We compute this for every prefix while constructing the KMP prefix function.

The brute-force approach works because it explicitly tests every possible period, but fails because the same characters are repeatedly compared for closely related suffixes. Reversing converts all relevant suffixes into prefixes, and KMP reuses the border information between consecutive prefixes, reducing the whole problem to linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) with direct period checks | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read (a), (b), and the decimal string, then discard everything through the decimal point. The integer part has no role in the reliability calculation, so retaining it would only waste memory and complicate the string processing.
2. Reverse the fractional digits. A candidate repeating part must reach the end of the original observed string, so every candidate corresponds to a suffix. After reversal, that suffix becomes a prefix, which is exactly the form handled by the prefix function.
3. Allocate the KMP prefix-function array for the reversed fractional string. For position (i), let (\pi[i]) be the longest proper prefix of `t[:i+1]` that is also its suffix.
4. Construct the prefix function using the standard KMP fallback rule. When the next character does not match the current border, repeatedly replace the border length (j) by (\pi[j-1]). These fallbacks skip entire groups of characters whose comparisons are already known to fail.
5. For every prefix ending at position (i), set (p=i+1). Its longest border has length (\pi[i]), so its shortest period is

[
l=p-\pi[i].
]

The reason this gives the shortest valid repeating part is the border-period relationship. A border of length (k) makes the string repeat after (p-k) positions, and the longest border produces the smallest such distance.

1. Compute

[
a p-b l
]

for this prefix and update the maximum. Since (p) increases from one through the full fractional length, every possible appeared length is considered exactly once.

1. Output the maximum value. The answer must be initialized using the first candidate, (a-b), rather than zero, because all reliability values can be negative.

### Why it works

Consider any legal repeating part in the original fractional string. Because it is still repeating at the end, all digits involved in its appearance form some suffix of the fractional string. Let that suffix contain (p) digits. After reversing the fractional string, the same characters form a prefix of length (p).

For this prefix, every valid repeating block length is a period of the prefix. If its longest border has length (k), then (p-k) is a period. Since no border can be longer than (k), no period can be shorter than (p-k). Thus the KMP value gives exactly the smallest possible (l) for this fixed (p).

For fixed (p), reliability is (ap-bl), and (b) is positive. A smaller (l) always gives a larger reliability. Consequently, considering only (l=p-\pi[p-1]) loses no optimal candidate. Since every possible (p) is examined, the maximum found by the algorithm is the maximum reliability over all legal repeating parts.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    s = input().strip()

    # Only the fractional part matters.
    frac = s.split('.', 1)[1]
    n = len(frac)

    # A signed 32-bit integer is enough for every prefix-function value.
    # Using array instead of a Python list keeps memory close to O(n) bytes
    # rather than O(n) Python objects.
    pi = array('i', [0]) * n

    if n == 0:
        print(a - b)
        return

    # Prefix of length 1: p = 1, l = 1.
    ans = a - b

    # We need suffixes of frac, so process the reversed string.
    t = frac[::-1]

    j = 0
    for i in range(1, n):
        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]

        if t[i] == t[j]:
            j += 1

        pi[i] = j

        p = i + 1
        l = p - j
        value = a * p - b * l

        if value > ans:
            ans = value

    print(ans)

if __name__ == "__main__":
    solve()
```

The first input line supplies (a) and (b), while the second line contains the complete observed decimal. `split('.', 1)[1]` extracts exactly the fractional part, so digits before the decimal point never participate in KMP.

The reversed string `t` is created because the relevant candidates are suffixes of the original fractional digits. A prefix-function value at index `i` describes the prefix of length `i+1`, which corresponds to a suffix of exactly that length in the original orientation.

The `pi` array uses four-byte signed integers. Every prefix-function value is at most (n), and (n\le10^7), so a 32-bit signed integer is sufficient. This choice matters in Python because a normal list of ten million Python integers can consume several hundred megabytes, while the typed array stores the same values compactly.

The KMP loop starts at `i = 1` because the first character always has prefix-function value zero. The variable `j` is the current border length. On a mismatch, `j = pi[j - 1]` jumps to the next smaller border instead of restarting the comparison from scratch.

After computing `pi[i]`, the prefix length is `p = i + 1`. The shortest period is `p - pi[i]`, so the reliability is calculated directly from those two values. The subtraction order matters because (a p-b l) can be negative.

Python integers have arbitrary precision, so there is no overflow concern in the implementation. In a C++ solution, however, the products can reach roughly (10^{16}), so `long long` is required.

The KMP fallback loop looks nested inside the main loop, but its total work remains linear. Every successful character match increases `j`, while every fallback strictly decreases `j`. Across the entire computation, the number of fallback operations is bounded by the number of increases, giving (O(n)) total work.

## Worked Examples

### Sample 1

The fractional part is `1020`. Reversing it gives `0201`.

| Prefix length (p) | Prefix | (\pi[p-1]) | Period (l=p-\pi[p-1]) | Reliability (5p-3l) | Best so far |
| --- | --- | --- | --- | --- | --- |
| 1 | `0` | 0 | 1 | 2 | 2 |
| 2 | `02` | 0 | 2 | 4 | 4 |
| 3 | `020` | 1 | 2 | 9 | 9 |
| 4 | `0201` | 0 | 4 | 8 | 9 |

At prefix length three, `020` has border `0` of length one. Removing that border from the prefix length gives period (3-1=2). Reversing back corresponds to the original suffix `020`, whose repeating block is `02`, appearing for three digits. Its reliability is (5\cdot3-3\cdot2=9), which is the optimum.

The key point is that the best candidate is not necessarily a complete number of repetitions. The prefix `020` consists of `02` followed by the first character `0` of another copy. That partial final copy is allowed.

### Sample 2

The fractional part is `1212`, so the reversed string is `2121`.

| Prefix length (p) | Prefix | (\pi[p-1]) | Period (l=p-\pi[p-1]) | Reliability (2p-l) | Best so far |
| --- | --- | --- | --- | --- | --- |
| 1 | `2` | 0 | 1 | 1 | 1 |
| 2 | `21` | 0 | 2 | 2 | 2 |
| 3 | `212` | 1 | 2 | 4 | 4 |
| 4 | `2121` | 2 | 2 | 6 | 6 |

For the complete prefix `2121`, the longest border is `21`, of length two. Hence the shortest period is (4-2=2). In the original direction this corresponds to the repeating part `12`, which appears for all four observed digits. Its reliability is (2\cdot4-1\cdot2=6).

The trace also shows why checking only prefixes with no partial repetition would be insufficient. The prefix of length three has period two even though three is not divisible by two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Extracting, reversing, building KMP, and evaluating all prefixes are each linear |
| Space | (O(n)) | The fractional string and prefix-function array both have linear size |

Here (n) is the number of digits after the decimal point, with (n\le10^7). Linear processing is the necessary scale for the input size. The typed prefix-function array also keeps the memory proportional to the input rather than storing millions of separate Python integer objects.

## Test Cases

```python
import sys
import io
from array import array

def solve_text(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        a, b = map(int, sys.stdin.readline().split())
        s = sys.stdin.readline().strip()

        frac = s.split('.', 1)[1]
        n = len(frac)

        if n == 0:
            return str(a - b)

        t = frac[::-1]
        pi = array('i', [0]) * n

        ans = a - b
        j = 0

        for i in range(1, n):
            while j > 0 and t[i] != t[j]:
                j = pi[j - 1]

            if t[i] == t[j]:
                j += 1

            pi[i] = j

            p = i + 1
            l = p - j
            value = a * p - b * l

            if value > ans:
                ans = value

        return str(ans)
    finally:
        sys.stdin = old_stdin

def run(inp: str) -> str:
    return solve_text(inp)

# Provided samples
assert run("5 3\n1.1020\n") == "9", "sample 1"
assert run("2 1\n12.1212\n") == "6", "sample 2"

# Minimum-size fractional part
assert run("7 10\n42.8\n") == "-3", "single fractional digit"

# Negative answer
assert run("1 2\n0.5\n") == "-1", "answer may be negative"

# All equal digits
assert run("2 1\n0.1111\n") == "7", "shortest period remains 1"

# Partial final repetition and off-by-one boundary
assert run("2 1\n0.121\n") == "4", "partial final repetition"

# Integer part must be ignored
assert run("5 3\n987654321.1020\n") == "9", "integer part is irrelevant"

# Maximum-size stress case.
# Ten million equal fractional digits have period 1 for every prefix.
# The final prefix gives p = 10,000,000 and l = 1.
n = 10_000_000
maximum_case = "1 1\n0." + ("7" * n) + "\n"
assert run(maximum_case) == "9999999", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7 10 / 42.8` | `-3` | Minimum fractional length and negative result |
| `1 2 / 0.5` | `-1` | Prevents incorrect initialization of the answer to zero |
| `2 1 / 0.1111` | `7` | All-equal digits and a period of one |
| `2 1 / 0.121` | `4` | Partial final repetition and prefix-function boundary |
| `5 3 / 987654321.1020` | `9` | Confirms that the integer part is ignored |
| `1 1 / 0.` followed by (10^7) copies of `7` | `9999999` | Maximum input size and linear-memory processing |

The maximum-size test deliberately uses equal digits because it stresses the entire prefix-function construction while keeping the expected answer easy to derive. For (n=10^7), every prefix has shortest period one, so the final candidate has (p=10^7), (l=1), and reliability (10^7-1=9,999,999).

## Edge Cases

For a negative answer, consider

```
1 2
0.5
```

The fractional string has length one, so the reversed string is also `5`. Its prefix-function value is zero, giving (p=1) and (l=1). The only reliability is (1\cdot1-2\cdot1=-1). The algorithm starts with `ans = a - b`, so it preserves this negative result instead of accidentally replacing it with zero.

For a single fractional digit, consider

```
7 10
42.8
```

The algorithm extracts `8`, reverses it to `8`, and has no KMP iterations beyond the initial prefix. The period is one and the reliability is (7-10=-3). There is no special string-pattern case hidden here, so the ordinary initialization already handles the smallest valid input.

For an incomplete final repetition, consider

```
2 1
0.121
```

The fractional string is `121`, and reversing gives `121`. The prefix-function values are (0,0,1). At (p=3), the longest border has length one, so (l=3-1=2). The candidate is the original suffix `121`, interpreted as the period `12` followed by its first digit `1`. Its reliability is (2\cdot3-1\cdot2=4). A solution that requires (p) to be a multiple of (l) would incorrectly discard this candidate.

For the integer-part boundary, consider

```
5 3
987654321.1020
```

After the decimal point, the algorithm sees exactly `1020`, producing the same reversed string `0201` and the same four candidates as the first sample. The maximum remains `9`. This confirms that the integer part cannot affect either (p), (l), or the reliability.

For repeated digits, consider

```
2 1
0.1111
```

The reversed string is still `1111`. Its prefix-function values are (0,1,2,3), so for the full prefix (p=4), the shortest period is (4-3=1). The reliability is (2\cdot4-1=7), which beats all shorter prefixes. This case exercises the long chain of KMP borders and confirms that the fallback structure handles maximal repetition without degenerating into quadratic work.
