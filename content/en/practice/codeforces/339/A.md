---
title: "CF 339A - Helpful Maths"
description: "We are given a single string that represents a sum of small integers. The expression is written using digits and plus signs, where every number is guaranteed to be either 1, 2, or 3."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 339
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 197 (Div. 2)"
rating: 800
weight: 339
solve_time_s: 243
verified: true
draft: false
---

[CF 339A - Helpful Maths](https://codeforces.com/problemset/problem/339/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings, strings  
**Solve time:** 4m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string that represents a sum of small integers. The expression is written using digits and plus signs, where every number is guaranteed to be either 1, 2, or 3. The task is to rearrange the numbers so that the resulting expression is sorted in non-decreasing order of the numbers, while preserving the same multiset of summands.

In more concrete terms, the input is a sequence of tokens separated by `+`. Each token is one digit in `{1,2,3}`. We are allowed to permute these tokens freely, and we must output them joined again by `+`, but sorted so that all `1`s come first, then `2`s, then `3`s.

The constraints are extremely small: the string length is at most 100 characters. That means we are never dealing with performance pressure from algorithmic complexity. Even a solution that scans or rearranges the string multiple times will run instantly. This pushes the problem away from anything involving sophisticated data structures and toward direct counting and reconstruction.

A subtle edge case comes from input structure rather than values. The string always contains valid formatting like `1+2+3`, but a careless split or reconstruction can easily introduce incorrect placement of plus signs. For example, reconstructing by sorting characters directly would fail because `'+'` must not be treated as a number.

Another edge case is minimal input such as a single number like `3`. The output must remain unchanged without adding any extra plus signs.

## Approaches

A brute-force interpretation would treat the string as a list of tokens, generate all permutations of these tokens, reconstruct each candidate expression, and then select one that is sorted. This is correct in principle because it explores all valid rearrangements. However, if there are `n` numbers, the number of permutations is `n!`, and even for `n = 10` this becomes already too large to enumerate.

The key observation is that we do not actually care about relative ordering decisions between individual elements beyond their values. Every valid answer depends only on how many `1`s, `2`s, and `3`s exist. Once those counts are known, the sorted answer is uniquely determined. This reduces the problem from permutation generation to frequency counting.

So instead of rearranging explicitly, we scan the string once, count occurrences of `1`, `2`, and `3`, and then reconstruct the output in sorted order by repeating each digit according to its frequency. This removes all combinatorial complexity and replaces it with linear processing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (permute all) | O(n!) | O(n) | Too slow |
| Counting and reconstruction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the input string character by character and ignore any `'+'` symbols. Every digit encountered is one of `1`, `2`, or `3`. We maintain three counters for these values. This step extracts the essential information from the formatting.
2. When a digit is encountered, increment the corresponding counter. This builds a frequency table of the multiset of numbers present in the expression.
3. After the scan completes, construct the output string by first writing all `1`s, then all `2`s, then all `3`s. Insert `'+'` between consecutive numbers but not at the beginning or end.
4. Join the constructed sequence into a single string and print it.

### Why it works

The correctness rests on the fact that sorting a multiset depends only on the frequency of each element. Since all elements are independent and comparable only by their numeric value, any valid non-decreasing arrangement must place all identical values contiguously and in increasing order of value. The counting step fully captures the multiset, and the reconstruction step produces the unique sorted arrangement consistent with that multiset.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    
    c1 = c2 = c3 = 0
    
    for ch in s:
        if ch == '1':
            c1 += 1
        elif ch == '2':
            c2 += 1
        elif ch == '3':
            c3 += 1
    
    parts = []
    parts.extend(['1'] * c1)
    parts.extend(['2'] * c2)
    parts.extend(['3'] * c3)
    
    print('+'.join(parts))

if __name__ == "__main__":
    solve()
```

The solution separates parsing from reconstruction. The scan phase ignores formatting characters entirely and only tracks meaningful symbols. The reconstruction phase builds an explicit list of tokens and then joins them with `'+'`, which avoids any risk of incorrect delimiter placement.

A common implementation mistake is attempting to sort the raw string directly, which would incorrectly place `'+'` among digits. Another is rebuilding the string manually with concatenation in a loop, which is unnecessary but still safe given the constraints.

## Worked Examples

### Example 1

Input: `3+2+1`

| Step | c1 | c2 | c3 | Output parts |
| --- | --- | --- | --- | --- |
| start | 0 | 0 | 0 | [] |
| read 3 | 0 | 0 | 1 | [3] |
| read 2 | 0 | 1 | 1 | [3,2] |
| read 1 | 1 | 1 | 1 | [3,2,1] |
| build | 1 | 1 | 1 | [1,2,3] |

The final reconstruction sorts by frequency, producing `1+2+3`. This confirms that the algorithm ignores input order entirely and relies only on counts.

### Example 2

Input: `1+1+3+2+2+1`

| Step | c1 | c2 | c3 | Output parts |
| --- | --- | --- | --- | --- |
| start | 0 | 0 | 0 | [] |
| after scan | 3 | 2 | 1 | [1,1,1,2,2,3] |

The output becomes `1+1+1+2+2+3`, demonstrating correct handling of repeated values and multiple groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the input string plus linear reconstruction |
| Space | O(1) | Only three counters and a small list of bounded size |

The input size is at most 100 characters, so even constant-factor overhead is negligible. The algorithm easily satisfies both time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    s = sys.stdin.readline().strip()
    c1 = c2 = c3 = 0
    
    for ch in s:
        if ch == '1':
            c1 += 1
        elif ch == '2':
            c2 += 1
        elif ch == '3':
            c3 += 1
    
    parts = []
    parts.extend(['1'] * c1)
    parts.extend(['2'] * c2)
    parts.extend(['3'] * c3)
    
    return '+'.join(parts)

# provided sample
assert run("3+2+1\n") == "1+2+3"

# custom cases
assert run("1\n") == "1", "single element"
assert run("2+2+2\n") == "2+2+2", "all same"
assert run("1+3+2+3+1+2\n") == "1+1+2+2+3+3", "balanced mix"
assert run("3+3+1+1+2\n") == "1+1+2+3+3", "random order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | single element handling |
| `2+2+2` | `2+2+2` | repeated identical values |
| `1+3+2+3+1+2` | `1+1+2+2+3+3` | balanced distribution |
| `3+3+1+1+2` | `1+1+2+3+3` | general reordering correctness |

## Edge Cases

For a single-number input like `2`, the scan produces `c2 = 1` and all other counters zero. Reconstruction yields a single-element list, and joining produces `"2"` without any plus signs. The algorithm naturally avoids inserting separators when only one token exists.

For highly unbalanced inputs such as `3+3+3+3+1`, counters accumulate as `c1 = 1, c3 = 4`. Reconstruction still places all `1`s before `3`s, producing `1+3+3+3+3`. This shows that the algorithm does not depend on input ordering at all, only on frequency aggregation, which remains correct even under extreme skew.
