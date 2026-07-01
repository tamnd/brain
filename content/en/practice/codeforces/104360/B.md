---
title: "CF 104360B - \u0412\u0430\u0441\u044f \u0438 \u041f\u0435\u0442\u044f"
description: "We are given a string of lowercase English letters. Each query selects a contiguous substring, and we transform that substring using a fixed rule: every character is expanded independently, where a letter at position x in the alphabet is repeated exactly x times."
date: "2026-07-01T17:56:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104360
codeforces_index: "B"
codeforces_contest_name: "\u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u041c\u0441\u0442\u0438\u0441\u043b\u0430\u0432\u0430 \u041a\u0435\u043b\u0434\u044b\u0448\u0430 - 2021"
rating: 0
weight: 104360
solve_time_s: 46
verified: true
draft: false
---

[CF 104360B - \u0412\u0430\u0441\u044f \u0438 \u041f\u0435\u0442\u044f](https://codeforces.com/problemset/problem/104360/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of lowercase English letters. Each query selects a contiguous substring, and we transform that substring using a fixed rule: every character is expanded independently, where a letter at position `x` in the alphabet is repeated exactly `x` times. For example, `a` becomes one copy, `b` becomes two copies, `c` becomes three copies, and so on. The task is not to construct the transformed string, only to compute its final length for each query.

So each query is fundamentally asking for a weighted sum over a substring, where the weight of a character depends only on its identity. If we map `a -> 1, b -> 2, ..., z -> 26`, each query asks for the sum of these weights over a range.

The input constraints allow up to 100,000 characters and 100,000 queries. Any solution that recomputes the sum from scratch per query would require scanning up to `O(n)` characters per query, leading to `O(nq)` in the worst case, which is on the order of `10^10` operations and will not run in time. This immediately forces a preprocessing-based solution with constant or logarithmic query time.

A subtle issue appears if one tries to be too literal with the transformation. Building the expanded string or simulating repetition per character will explode both time and memory. Even a single query can produce a string of length up to `26 * n`, which is far beyond feasible construction. The only meaningful quantity is the sum of contributions.

Another edge case is when the substring is a single character. The answer should be exactly its alphabet index. This helps validate correctness of prefix handling, since off-by-one mistakes in prefix sums often show up here.

## Approaches

The brute-force idea is straightforward: for each query, iterate through the substring, convert each character to its alphabet position, and accumulate the sum. This is correct because each character contributes independently to the final length. However, this approach repeats the same work for overlapping ranges. With `n = 100000` and `q = 100000`, the worst case repeatedly scans large segments of the string, leading to about `10^10` character operations.

The key observation is that each character contributes a fixed value independent of context. This means we can precompute prefix sums over these values. Once we build an array `pref`, where `pref[i]` stores the total contribution of the first `i` characters, any query `[l, r]` can be answered as `pref[r] - pref[l-1]`. This reduces each query to O(1) time after O(n) preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Prefix Sums | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the string into a numeric array where each character `c` is mapped to `ord(c) - ord('a') + 1`. This directly represents how many times that character would be repeated in the fictional expanded string, but we never construct that string.
2. Build a prefix sum array `pref` of size `n + 1`, where `pref[i]` equals the sum of values for the first `i` characters. This step compresses all repeated range computations into a single structure.
3. For each query `[l, r]`, compute the answer as `pref[r] - pref[l - 1]`. This works because prefix sums store cumulative contributions, and subtraction isolates the range.
4. Output each result immediately or store and print at the end.

The only real pitfall is indexing. The problem uses 1-based indices, while Python arrays are 0-based. Shifting consistently at both prefix construction and query time is essential.

### Why it works

Each character contributes independently to the final length, and the transformation rule does not introduce any interaction between positions. This makes the problem a linear additive function over intervals. Prefix sums preserve exact interval sums under subtraction, so every query reduces to evaluating a difference of two precomputed cumulative values. No approximation or state dependence is involved, so correctness follows directly from linearity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, q = map(int, input().split())
    s = input().strip()

    pref = [0] * (n + 1)

    for i in range(n):
        val = ord(s[i]) - ord('a') + 1
        pref[i + 1] = pref[i] + val

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        out.append(str(pref[r] - pref[l - 1]))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The code first constructs the prefix sum array over character weights. Each position contributes its alphabet index, and the prefix array accumulates these values.

Each query is answered using a subtraction of two prefix values. The subtraction `pref[r] - pref[l - 1]` correctly handles inclusive ranges because `pref` is defined with a leading zero entry.

A common implementation mistake is forgetting the `+1` shift in prefix indexing or mixing 0-based and 1-based indices in queries. Another is rebuilding the prefix array per query instead of once globally.

## Worked Examples

### Example 1

Input:

```
7 3
abacaba
1 3
2 5
1 7
```

We first compute character values:

`a=1, b=2, a=1, c=3, a=1, b=2, a=1`

Prefix sums:

| i | char | value | pref |
| --- | --- | --- | --- |
| 0 | - | - | 0 |
| 1 | a | 1 | 1 |
| 2 | b | 2 | 3 |
| 3 | a | 1 | 4 |
| 4 | c | 3 | 7 |
| 5 | a | 1 | 8 |
| 6 | b | 2 | 10 |
| 7 | a | 1 | 11 |

Queries:

`[1,3] = pref[3]-pref[0]=4`

`[2,5] = pref[5]-pref[1]=8-1=7`

`[1,7] = 11`

This trace confirms that the prefix array correctly aggregates weighted contributions and each query is a simple interval difference.

### Example 2

Input:

```
7 4
abbabaa
1 3
5 7
6 6
2 4
```

Character values:

`a=1, b=2, b=2, a=1, b=2, a=1, a=1`

Prefix:

| i | pref |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 3 |
| 3 | 5 |
| 4 | 6 |
| 5 | 8 |
| 6 | 9 |
| 7 | 10 |

Queries:

`[1,3]=5`

`[5,7]=10-6=4`

`[6,6]=1`

`[2,4]=6-1=5`

This case stresses single-element queries and overlapping ranges, both handled uniformly by the same prefix structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | One pass builds prefix sums, each query is O(1) |
| Space | O(n) | Prefix array of size n+1 |

The solution easily fits within constraints since both `n` and `q` are up to 100,000, keeping total operations around 200,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    s = input().strip()

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + (ord(s[i]) - ord('a') + 1)

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        out.append(str(pref[r] - pref[l - 1]))
    return "\n".join(out)

# provided samples
assert run("7 3\nabacaba\n1 3\n2 5\n1 7\n") == "4\n7\n11"
assert run("7 4\nabbabaa\n1 3\n5 7\n6 6\n2 4\n") == "5\n4\n1\n5"

# custom cases
assert run("1 1\na\n1 1\n") == "1"
assert run("5 2\nabcde\n1 5\n2 4\n") == "15\n9"
assert run("6 3\naaaaaa\n1 6\n2 5\n3 3\n") == "6\n5\n1"
assert run("4 2\nzzzz\n1 4\n2 3\n") == "104\n52"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char | 1 | minimum boundary |
| full alphabet | 15, 9 | general correctness |
| all a's | 6, 5, 1 | repeated uniform weights |
| all z's | 104, 52 | high-value character handling |

## Edge Cases

A single-character query such as `s = "c", l = r = 1` directly returns `3`. The prefix array becomes `[0, 3]`, so the answer is `pref[1] - pref[0] = 3`. This confirms that the base indexing works without needing special handling.

A full-range query tests whether the prefix array correctly aggregates the entire string. For example, `s = "abc"` gives prefix `[0,1,3,6]`, and querying `[1,3]` yields `6`, matching the direct sum.

Uniform strings like `"aaaaaa"` validate that repeated identical contributions accumulate correctly. Each prefix step increases by exactly 1, so range sums reduce to simple differences proportional to substring length.

These cases collectively ensure that both indexing and accumulation logic remain consistent across all query types.
