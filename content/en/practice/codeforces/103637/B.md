---
title: "CF 103637B - BSUIR Open X"
description: "We are given a collection of strings, each representing the code name of a task set. From this collection we must choose exactly two distinct strings, and we are allowed to place them in either order, concatenating one after the other."
date: "2026-07-02T22:18:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103637
codeforces_index: "B"
codeforces_contest_name: "2019-2020 10th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 103637
solve_time_s: 52
verified: true
draft: false
---

[CF 103637B - BSUIR Open X](https://codeforces.com/problemset/problem/103637/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of strings, each representing the code name of a task set. From this collection we must choose exactly two distinct strings, and we are allowed to place them in either order, concatenating one after the other.

The goal is to count how many ordered pairs of distinct indices produce the target string “BSUIROPENX” after concatenation. Distinctness is defined by indices, not by string values, so if two identical strings appear at different positions, they are treated as different choices.

The key constraint is the size of the input: up to 100,000 strings with total length up to 1,000,000. This immediately rules out any solution that tries to test all pairs of strings directly, since that would be quadratic in the number of strings and far beyond feasible limits. Even an O(n²) check where each comparison is O(1) would already be around 10¹⁰ operations in the worst case.

A more subtle constraint comes from the target string length, which is fixed and small (10 characters). That hints that only strings that can contribute to forming this exact string are relevant, and everything else can be ignored.

A common failure case is assuming we need substring matching or overlap matching between arbitrary pairs. For example, if one tries to match suffixes and prefixes dynamically for every pair, it becomes easy to overcount or miss cases where the split point is constrained by exact equality rather than partial matching.

A concrete pitfall appears when multiple identical strings exist. For instance, if the list contains three copies of “BSU” and two copies of “IROPENX”, the answer is not 3 + 2 but 3 × 2 plus reversed possibilities if applicable. Many incorrect solutions forget that ordering doubles the contribution and that identical strings must still be treated as distinct indices.

## Approaches

A brute-force approach would iterate over all ordered pairs of strings and check whether their concatenation equals “BSUIROPENX”. Each check costs O(L) where L is at most 10, and there are O(n²) pairs. With n up to 10⁵, this leads to roughly 10¹⁰ comparisons, which is far too slow.

The key observation is that we do not actually need to consider arbitrary concatenations. Since the target string is fixed, any valid pair must correspond to a split point inside “BSUIROPENX”. That means we can split the target into two parts and look for one string equal to the prefix and another equal to the suffix.

Let the target be T = “BSUIROPENX”. For every split position i from 1 to 9, we consider T[0:i] and T[i:]. Any valid ordered pair must consist of one string equal to T[0:i] and another equal to T[i:]. This reduces the problem to frequency counting of strings.

We simply count how many times each string appears in the input, then sum over all valid split points the product of frequencies. We must also respect ordering automatically: prefix first and suffix second already defines direction, and we separately account for reversed ordering if the problem requires both concatenation orders, which it does. So for each split, we add both freq(prefix) × freq(suffix) and freq(suffix) × freq(prefix) when prefix and suffix differ, and only freq(prefix) × (freq(prefix) − 1) when they are equal.

This reduces the problem to linear scanning of strings and constant work over the fixed-length target.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² · L) | O(1) | Too slow |
| Frequency + split enumeration | O(n + | T | ) |

## Algorithm Walkthrough

Let the target string be T = “BSUIROPENX”.

1. Read all input strings and build a frequency map. Each distinct string stores how many times it appears. This allows constant-time lookup later instead of repeated scanning.
2. Iterate over all possible split positions i from 1 to len(T) − 1. Each split defines a prefix A = T[0:i] and suffix B = T[i:].
3. For each split, check whether both A and B exist in the frequency map. If either is missing, skip this split entirely because no valid pair can be formed.
4. If A and B are different strings, add freq[A] × freq[B] × 2 to the answer. The factor of 2 accounts for both possible orders: A followed by B and B followed by A.
5. If A and B are the same string, add freq[A] × (freq[A] − 1). This counts ordered pairs of distinct indices chosen from identical strings, since ordering still matters but we must avoid pairing an index with itself.
6. Accumulate results over all split points and output the final sum.

### Why it works

Every valid concatenation equals the target string. Therefore, the boundary between the two chosen strings must align exactly with one of the internal cut positions of the target. No other structure is possible because string concatenation preserves order without overlap or gaps. This reduces the entire problem space from arbitrary string pairing to a finite set of at most 9 candidate splits. The frequency-based counting ensures every valid index pair is counted exactly once according to whether it corresponds to a prefix-suffix split.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    freq = {}

    for _ in range(n):
        s = input().strip()
        freq[s] = freq.get(s, 0) + 1

    target = "BSUIROPENX"
    ans = 0

    m = len(target)

    for i in range(1, m):
        a = target[:i]
        b = target[i:]

        ca = freq.get(a, 0)
        cb = freq.get(b, 0)

        if ca == 0 or cb == 0:
            continue

        if a != b:
            ans += ca * cb * 2
        else:
            ans += ca * (ca - 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by compressing the input into a frequency table so that repeated strings do not require repeated scanning. Each split of the target string is then treated as a structural hypothesis about how the final concatenation is formed. The handling of equal and unequal halves is critical, since it determines whether ordered pairs come from two different groups or within a single group.

The multiplication by 2 for distinct parts is easy to miss, but it directly corresponds to the fact that both concatenation orders are valid and must be counted separately.

## Worked Examples

### Example 1

Input:

```
4
BSUIR
BSU
OPEN
IROPENX
```

Target is “BSUIROPENX”. We compute frequencies:

| string | freq |
| --- | --- |
| BSUIR | 1 |
| BSU | 1 |
| OPEN | 1 |
| IROPENX | 1 |

Now we check splits:

| split i | prefix | suffix | freq[prefix] | freq[suffix] | contribution |
| --- | --- | --- | --- | --- | --- |
| 3 | BSU | IROPENX | 1 | 1 | 2 |

Other splits do not match any strings in the input.

Final answer is 2, corresponding to both orderings of (BSU, IROPENX).

This confirms that ordering is counted correctly and that only exact prefix-suffix matches matter.

### Example 2

Input:

```
3
BSUIR
OPENX
BSUIROPENX
```

Target splits include BSUIR + OPENX, but OPENX is present and BSUIR is present.

| split i | prefix | suffix | freq[prefix] | freq[suffix] | contribution |
| --- | --- | --- | --- | --- | --- |
| 5 | BSUIR | OPENX | 1 | 1 | 2 |

Answer is 2, again reflecting both concatenation orders.

This demonstrates that even when strings are not adjacent in input, frequency counting correctly captures all valid pairings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + | T |
| Space | O(n) | Storage for frequency map of input strings |

The constraints allow up to 10⁵ strings and total length 10⁶, so a linear-time solution with hashing is well within limits. The target string is constant size, so the split enumeration is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    old = sys.stdout
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

def solve():
    n = int(input().strip())
    freq = {}
    for _ in range(n):
        s = input().strip()
        freq[s] = freq.get(s, 0) + 1

    target = "BSUIROPENX"
    ans = 0
    m = len(target)

    for i in range(1, m):
        a = target[:i]
        b = target[i:]
        ca = freq.get(a, 0)
        cb = freq.get(b, 0)

        if ca == 0 or cb == 0:
            continue

        if a != b:
            ans += ca * cb * 2
        else:
            ans += ca * (ca - 1)

    print(ans)

# provided sample
assert run("4\nBSUIR\nBSU\nOPEN\nIROPENX\n") == "2"

# single valid pair
assert run("2\nBSUIR\nOPENX\n") == "2"

# no solution
assert run("3\nA\nB\nC\n") == "0"

# duplicates
assert run("4\nBSU\nBSU\nIROPENX\nIROPENX\n") == "8"

# all equal strings irrelevant
assert run("3\nBSU\nBSU\nBSU\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 2 | basic correctness |
| 2 strings | 2 | both orderings counted |
| no match | 0 | safe rejection |
| duplicates | 8 | multiplicity handling |
| irrelevant repeats | 0 | filtering non-matching strings |

## Edge Cases

One important edge case is when prefix and suffix are identical. If the input contains multiple copies of such a string, we must count ordered pairs without pairing an index with itself. The formula freq × (freq − 1) correctly handles this.

For example, if target split produces A = B = "XX" and the input contains three occurrences of "XX", then valid ordered pairs are (i, j) with i ≠ j, giving 3 × 2 = 6.

Another edge case is when multiple splits of the target correspond to valid strings. Each split is independent, so contributions accumulate. The frequency map ensures that each valid pair is counted exactly once per split, and no overlap between splits creates double counting beyond intended ordering symmetry.
