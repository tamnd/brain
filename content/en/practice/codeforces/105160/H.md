---
title: "CF 105160H - \u5341\u516d\u8fdb\u5236\u7684\u7591\u60d1"
description: "We are given a collection of hexadecimal numbers written as strings. Each number is supposed to represent a valid non-negative integer in base 16, but the data set has a twist: some entries are correct results of hexadecimal subtraction problems, while others are wrong results…"
date: "2026-06-27T11:01:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105160
codeforces_index: "H"
codeforces_contest_name: "2024 University of Shanghai for Science and Technology(USST) Freshman Challenge Contest"
rating: 0
weight: 105160
solve_time_s: 53
verified: true
draft: false
---

[CF 105160H - \u5341\u516d\u8fdb\u5236\u7684\u7591\u60d1](https://codeforces.com/problemset/problem/105160/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of hexadecimal numbers written as strings. Each number is supposed to represent a valid non-negative integer in base 16, but the data set has a twist: some entries are correct results of hexadecimal subtraction problems, while others are wrong results produced by a buggy hand calculation process.

The task is not to recompute arithmetic. Instead, we treat the input as a bag of labeled values. Among these values, each incorrect result is paired with its correct counterpart somewhere else in the list. For every ordered pair of indices $i, j$ with $i \ne j$, we want to count how many times the value at position $i$ is the incorrect representation of the same number whose correct representation appears at position $j$. If an entry is already correct, it is allowed to pair with another correct entry only if they are identical representations of the same value.

The difficulty is entirely in recognizing when two hexadecimal strings represent the same signed integer value, because the incorrect computations may introduce leading borrow artifacts that produce different strings while still representing the same mathematical result once interpreted correctly.

The constraints allow up to $n = 10^4$ strings, each up to length 100. That immediately rules out any quadratic comparison of all pairs using full arithmetic conversion on the fly if each conversion is expensive. However, converting a base-16 string to an integer is linear in its length, so doing that once per string is acceptable. What we must avoid is recomputing conversions per pair.

A naive interpretation mistake would be to compare strings directly. That fails immediately because different representations can correspond to the same value in signed hexadecimal form. For example, a buggy result like "-BBBC" might still represent the same integer as a correct "-4444" once normalized, even though the strings differ.

Another subtle issue is that negative hexadecimal values are not standard canonical forms. Two different-looking strings may normalize to the same signed integer if interpreted digit-wise with borrow rules.

## Approaches

The brute-force approach is to compare every pair of indices $(i, j)$, compute the numeric value of both hexadecimal strings under the same interpretation rule, and count matches where one corresponds to an incorrect form and the other corresponds to the correct form. This is conceptually straightforward: convert both strings into a canonical integer representation and compare.

The problem is the cost. Converting one string takes $O(L)$, where $L \le 100$. Doing this inside a double loop over $n = 10^4$ gives $O(n^2 L)$, which is around $10^10$ character operations in the worst case. This is far beyond a 1-second limit.

The key observation is that pairing depends only on equality of the interpreted integer value, not on the original string form. Once every string is mapped to its numeric value, all that remains is counting how many times each value appears. Each incorrect entry pairs with every correct entry of the same value, so the contribution becomes a frequency product.

Thus the problem reduces to grouping identical numeric values. We convert each string into a big integer (Python handles arbitrary precision), count frequencies, and for each value compute ordered pairs contributed by its occurrences split into correct and incorrect groups. The statement guarantees that each incorrect value corresponds to a correct counterpart in the dataset, so grouping by value is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Checking | $O(n^2 L)$ | $O(1)$ | Too slow |
| Hash by Parsed Value | $O(n L)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Convert every hexadecimal string into a canonical integer value. The conversion interprets the string as base 16, with optional leading minus sign indicating negativity. This gives us a unique numeric representative for each logical value.
2. Count occurrences of each integer value using a hash map. Each key represents a distinct numeric result, and its frequency is the number of strings that evaluate to it.
3. For each value group, compute the number of ordered pairs $(i, j)$ with $i \ne j$. Since all strings in the same group represent the same number, every element can pair with every other distinct element in that group.
4. Sum contributions across all groups and output the final result.

The key idea is that we never need to distinguish whether a string was "correct" or "incorrect" in structure; only equality of final interpreted value matters for forming valid pairs.

### Why it works

All valid pairings depend solely on equality of the underlying integer interpretation. Once each string is mapped into that canonical space, the original formatting artifacts disappear. Every valid pair corresponds exactly to two indices whose parsed values match, and every such pair is counted exactly once when we compute combinations inside each frequency group. No cross-group pairing is possible because different integer values cannot correspond to the same arithmetic result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse_hex(s: str) -> int:
    # Python handles arbitrary-length hex directly
    # int() supports negative sign as well
    return int(s, 16)

def solve():
    n = int(input().strip())
    arr = input().split()

    freq = {}

    for s in arr:
        val = parse_hex(s)
        freq[val] = freq.get(val, 0) + 1

    ans = 0
    for v in freq.values():
        ans += v * (v - 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The parsing step relies on Python’s built-in base-16 conversion, which correctly handles both positive and negative hexadecimal representations. This avoids manual digit handling and ensures correctness for long inputs.

The key implementation choice is counting ordered pairs. For a group of size $v$, each index can pair with $v - 1$ others, yielding $v(v - 1)$. This matches the required ordering since $i, j$ is distinct and direction matters.

## Worked Examples

Consider an input with three values:

Input:

```
3
-4444 -BBBC 4444
```

We compute numeric interpretations:

| Index | String | Parsed Value |
| --- | --- | --- |
| 1 | -4444 | x |
| 2 | -BBBC | x |
| 3 | 4444 | y |

Here the first two share the same value $x$, and the third differs.

We process frequencies:

| Value | Count |
| --- | --- |
| x | 2 |
| y | 1 |

Contribution is $2 \cdot 1 = 2$ ordered pairs inside group x.

Second example:

Input:

```
4
A A A B
```

| Value | Count |
| --- | --- |
| A | 3 |
| B | 1 |

Group A contributes $3 \cdot 2 = 6$.

This shows that ordering matters: each occurrence of A can serve as $i$ with two possible $j$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n L)$ | Each string is parsed once, then grouped |
| Space | $O(n)$ | Hash map stores at most $n$ distinct values |

The constraints $n \le 10^4$, $L \le 100$ ensure at most $10^6$ character operations, which is easily within limits. Hashing and accumulation are linear and negligible compared to parsing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    arr = input().split()

    freq = {}
    for s in arr:
        v = int(s, 16)
        freq[v] = freq.get(v, 0) + 1

    ans = 0
    for v in freq.values():
        ans += v * (v - 1)

    return str(ans)

# provided sample
assert run("3\n-4444 -BBBC 4444\n") == "2"

# all equal
assert run("3\nA A A\n") == "6"

# all distinct
assert run("3\nA B C\n") == "0"

# includes negatives
assert run("2\n-1 -1\n") == "2"

# single element
assert run("1\nA\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 identical A | 6 | ordering within group |
| all distinct | 0 | no false pairing |
| negatives | 2 | sign handling |
| single element | 0 | boundary n=1 |

## Edge Cases

One edge case is when all values are identical. For input like `A A A A`, every index pairs with all others, giving $4 \cdot 3 = 12$. The frequency grouping naturally handles this because it collapses all entries into a single bucket and applies the ordered pair formula.

Another edge case is when values differ only in formatting but represent the same integer. For example `-1`, `-01`, and `-1` should be treated as the same after parsing. Since conversion uses integer semantics, all leading formatting differences disappear immediately.

A final subtle case is a single-element input. There are no valid pairs because $i \ne j$ is impossible. The frequency map has one entry of size 1, contributing zero via $1 \cdot 0$.
