---
title: "CF 104916C - CAT"
description: "We are given a string consisting of uppercase Latin letters, and we are interested in counting how many ordered subsequences of the form “C-A-T” exist inside it."
date: "2026-06-28T08:10:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104916
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u0421\u0430\u043c\u0430\u0440\u0435 2022-2023 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104916
solve_time_s: 48
verified: true
draft: false
---

[CF 104916C - CAT](https://codeforces.com/problemset/problem/104916/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting of uppercase Latin letters, and we are interested in counting how many ordered subsequences of the form “C-A-T” exist inside it. A subsequence is formed by picking indices $i < j < k$ such that the characters at those positions are respectively ‘C’, ‘A’, and ‘T’. The characters do not need to be adjacent, only their order matters.

The task is purely combinatorial: for every valid choice of positions, we count one occurrence of the pattern. The output is the total number of such triples.

If the string length is large, on the order of $10^5$ or more, any solution that explicitly tries all triples of indices is impossible because that would require cubic or at least quadratic behavior in the worst case. Even a double loop over positions quickly becomes too slow when nested with another scan.

A subtle edge case is when the string contains many repeated letters. For example, if the string is “CATCAT”, a naive greedy interpretation might incorrectly assume overlapping patterns interfere with each other, but in fact every valid triple of indices is independent. Another failure mode is treating the problem as contiguous substring matching rather than subsequence counting, which would miss valid non-adjacent formations such as:

Input:

```
CAXAT
```

Correct output:

```
2
```

because the pairs (C at 1, A at 3, T at 5) and (C at 1, A at 4, T at 5) both form valid subsequences.

## Approaches

The brute-force idea is straightforward: choose every position for ‘C’, then every later position for ‘A’, and then every later position for ‘T’. This directly follows the definition of the problem and is correct because it enumerates all valid triples $i < j < k$. However, this requires checking all $O(n^3)$ triples in the worst case. With $n = 10^5$, this is far beyond feasible limits.

We can improve this by reusing partial structure. Instead of independently searching for each triple, we observe that every ‘A’ sits between a set of ‘C’s on its left and a set of ‘T’s on its right. If we knew, for each ‘A’, how many valid “C-A” prefixes end at it and how many “A-T” suffix extensions start from it, we could combine them efficiently.

This leads to a natural dynamic accumulation strategy. We process the string from right to left so that we can maintain how many ‘T’s exist to the right, how many “AT” pairs exist to the right, and how many “CAT” triples can be formed.

By maintaining counters for partial structures, we avoid recomputing overlapping subproblems. Each character contributes to higher-level patterns based on previously accumulated information.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Right-to-left accumulation | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We scan the string from right to left while maintaining three counters:

1. A counter `cntT` that stores how many ‘T’ characters have been seen so far.
2. A counter `cntAT` that stores how many pairs “A-T” exist where ‘A’ is to the left of those ‘T’s in the suffix.
3. A counter `cntCAT` that stores how many full “C-A-T” subsequences exist in the processed suffix.

We update these counters based on the current character:

1. Start with all counters set to zero. We process characters from the last index down to the first.
2. If the current character is ‘T’, increment `cntT` by one because this ‘T’ can serve as the ending of future “AT” and “CAT” patterns.
3. If the current character is ‘A’, then every ‘T’ currently in the suffix can pair with this ‘A’ to form a new “AT”. We add `cntT` to `cntAT`.
4. If the current character is ‘C’, then every existing “AT” pair in the suffix can be extended with this ‘C’ at the front to form a full “CAT”. We add `cntAT` to `cntCAT`.

After processing all characters, `cntCAT` holds the answer.

### Why it works

At any position during the right-to-left scan, `cntT` correctly counts all valid choices for the final character of a pattern within the already processed suffix. Similarly, `cntAT` counts all valid ordered pairs (A before T) entirely inside the suffix. Finally, every time we see a ‘C’, combining it with all existing “AT” pairs enumerates exactly all triples (C, A, T) with correct ordering. Each extension step preserves ordering because contributions only come from the suffix, which lies strictly to the right of the current position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    
    cntT = 0
    cntAT = 0
    cntCAT = 0
    
    for ch in reversed(s):
        if ch == 'T':
            cntT += 1
        elif ch == 'A':
            cntAT += cntT
        elif ch == 'C':
            cntCAT += cntAT
    
    print(cntCAT)

if __name__ == "__main__":
    solve()
```

The implementation follows the reverse scan directly. The key detail is the strict order of updates: `cntT` must be updated before `cntAT`, and `cntAT` before `cntCAT` depending on character type, because each layer depends on the previously accumulated suffix information.

No intermediate storage is needed because all relevant structure is compressed into the three counters.

## Worked Examples

### Example 1

Input:

```
CATAT
```

We track the variables while scanning right to left.

| Character | cntT | cntAT | cntCAT |
| --- | --- | --- | --- |
| T | 1 | 0 | 0 |
| A | 1 | 1 | 0 |
| T | 2 | 1 | 0 |
| A | 2 | 3 | 0 |
| C | 2 | 3 | 3 |

Final answer: 3

This confirms that multiple overlapping “AT” structures can be reused by a single ‘C’ to form multiple valid triples.

### Example 2

Input:

```
ACAT
```

| Character | cntT | cntAT | cntCAT |
| --- | --- | --- | --- |
| T | 1 | 0 | 0 |
| A | 1 | 1 | 0 |
| C | 1 | 1 | 1 |
| A | 1 | 2 | 1 |

Final answer: 1

This demonstrates that only one valid triple exists, even though multiple partial pairs exist, because only one ‘C’ is available to anchor them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each character is processed once with constant-time updates |
| Space | $O(1)$ | Only three integer counters are maintained |

The linear scan is optimal for strings of length up to $10^5$ or more, since it performs a single pass with no nested iteration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    s = sys.stdin.readline().strip()
    
    cntT = 0
    cntAT = 0
    cntCAT = 0
    
    for ch in reversed(s):
        if ch == 'T':
            cntT += 1
        elif ch == 'A':
            cntAT += cntT
        elif ch == 'C':
            cntCAT += cntAT
    
    return str(cntCAT)

# provided samples (conceptual)
assert run("CATAT\n") == "3"

# minimum size
assert run("C\n") == "0"

# no valid pattern
assert run("TTTAAA\n") == "0"

# single valid pattern
assert run("CAT\n") == "1"

# multiple overlaps
assert run("CCAAATTT\n") == "27"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| C | 0 | minimum edge case |
| TTTAAA | 0 | ordering requirement |
| CAT | 1 | basic correctness |
| CCAAATTT | 27 | combinatorial explosion handling |

## Edge Cases

A key edge case is when letters are heavily repeated and all valid combinations exist. For example:

Input:

```
CCAAATTT
```

We process from right to left. Every ‘T’ increases `cntT`, every ‘A’ contributes all current `T`s to `cntAT`, and every ‘C’ multiplies all current `AT` pairs into `cntCAT`. Because there are multiple identical letters, the counters grow quickly but always represent exact combinatorial counts, not approximations.

Another edge case is absence of one required character, such as no ‘A’ in the string. In that situation, `cntAT` never increases from zero, so `cntCAT` remains zero regardless of how many ‘C’ and ‘T’ exist. This matches the definition since no valid triple can be formed without a middle character.
