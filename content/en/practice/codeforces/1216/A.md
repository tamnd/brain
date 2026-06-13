---
title: "CF 1216A - Prefixes"
description: "We are given a binary string made only of characters a and b, and its length is even. The goal is to modify it using the minimum number of character flips so that every prefix whose length is even contains exactly the same number of a and b."
date: "2026-06-13T17:39:23+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 1216
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 587 (Div. 3)"
rating: 800
weight: 1216
solve_time_s: 155
verified: false
draft: false
---

[CF 1216A - Prefixes](https://codeforces.com/problemset/problem/1216/A)

**Rating:** 800  
**Tags:** strings  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string made only of characters `a` and `b`, and its length is even. The goal is to modify it using the minimum number of character flips so that every prefix whose length is even contains exactly the same number of `a` and `b`.

A useful way to rephrase the condition is to think in pairs of positions from the start. For every even index `i`, the prefix `s[1..i]` must have equal counts of both letters. That means in every prefix of length 2, 4, 6, and so on, the total balance between `a` and `b` must always be zero.

We are allowed to flip any character independently, changing `a` to `b` or `b` to `a`, and we want to minimize how many flips are needed while also constructing a valid final string.

The constraints allow `n` up to 200,000. This immediately rules out any solution that tries all possibilities or repeatedly recomputes prefix statistics in quadratic time. Anything like checking all substrings or simulating all modifications per position would be too slow. We need a linear pass solution with constant work per character.

A subtle edge case appears when early prefixes are heavily imbalanced. For example, if the string starts with many identical letters, a naive greedy fix that tries to “balance locally” might waste operations that would have been better delayed or paired differently. Another edge case is when corrections early in the string affect whether later positions even need to be flipped, so decisions cannot be made independently without tracking structure.

## Approaches

A brute-force strategy would try to fix the string incrementally while ensuring every even prefix is balanced. One way to imagine it is: after processing each even prefix, check if it contains equal `a` and `b`. If not, we would try all possible flips in that prefix to fix it, recompute counts, and proceed. This is correct in principle because it enforces the condition directly, but the cost is disastrous. For each of the `n/2` even prefixes, scanning the prefix costs O(n), and trying flips makes it even worse, leading to O(n²) or more.

The key observation is that constraints only exist at even prefix lengths, which naturally partitions the string into independent pairs `(1,2), (3,4), (5,6), ...`. Each pair must contribute exactly one `a` and one `b` in some order. Once we fix this interpretation, the global condition becomes local: every pair independently must be balanced, and there is no cross-pair dependency.

So the problem reduces to deciding, for each pair, whether it should become `"ab"` or `"ba"` in a way that minimizes total flips. For each pair, we simply compare the cost of making it `"ab"` versus `"ba"` and pick the cheaper option.

This transforms the problem from global prefix constraints into independent local decisions on pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split the string into consecutive pairs `(s[2i], s[2i+1])`. This is justified because every even prefix constraint ends exactly at pair boundaries.

2. For each pair, consider two possible target configurations: `"ab"` and `"ba"`. We compute how many flips each option requires.

3. If the pair is `(x, y)`, then making it `"ab"` costs 0 if `x='a'` and 0 if `y='b'`, otherwise each mismatch costs 1. Similarly compute cost for `"ba"`.

4. Choose the configuration with smaller cost. If both are equal, either choice is valid since the problem allows multiple answers.

5. Accumulate the total cost and build the resulting string by concatenating chosen pair results.

6. Output the total cost and the constructed string.

### Why it works

The crucial invariant is that after processing each pair, the prefix ending at that pair is balanced. Each pair contributes exactly one `a` and one `b`, so after `k` pairs, the prefix of length `2k` always has `k` `a`s and `k` `b`s. Since pairs are independent and do not interact, local optimality per pair implies global optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    res = []
    ops = 0

    for i in range(0, n, 2):
        a = s[i]
        b = s[i + 1]

        # cost to make "ab"
        cost_ab = (a != 'a') + (b != 'b')
        # cost to make "ba"
        cost_ba = (a != 'b') + (b != 'a')

        if cost_ab <= cost_ba:
            res.append("ab")
            ops += cost_ab
        else:
            res.append("ba")
            ops += cost_ba

    print(ops)
    print("".join(res))

if __name__ == "__main__":
    solve()
```

The code processes the string in steps of two characters. For each pair, it computes mismatch costs against both valid patterns. The comparison is constant time, and the final string is built incrementally in a list to avoid repeated string concatenation overhead.

A common pitfall is forgetting that both orientations must always be considered, even if one character already looks “correct”. Another is concatenating strings repeatedly, which would degrade performance to O(n²) in Python.

## Worked Examples

### Example 1
Input:
```
4
bbbb
```

We process pairs `(b,b)` and `(b,b)`.

| Pair | Cost "ab" | Cost "ba" | Chosen | Result | Ops |
|------|----------|----------|--------|--------|-----|
| bb   | 2        | 0        | ba     | ba     | 0   |
| bb   | 2        | 0        | ba     | baba   | 0   |

Final output string is `"baba"` with 0 operations? Actually correction shows both pairs are already optimal as `"ba"` each, so total operations is 2 if we measure flips from original `bbbb`.

This demonstrates that each pair is corrected independently.

### Example 2
Input:
```
6
abbaaa
```

Pairs: `(a,b)`, `(b,a)`, `(a,a)`.

| Pair | Cost "ab" | Cost "ba" | Chosen | Result | Ops |
|------|----------|----------|--------|--------|-----|
| ab   | 0        | 2        | ab     | ab     | 0   |
| ba   | 2        | 0        | ba     | abba   | 0   |
| aa   | 1        | 1        | ab     | abbaba | 1   |

This shows that even when both options are equal or close, local selection still yields a valid globally balanced result.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) | Each pair is processed once with constant-time cost computation |
| Space | O(n) | Output string storage |

The solution fits easily within constraints since `n = 2 * 10^5` only requires a single linear scan and simple arithmetic per pair.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("4\nbbbb\n") == "2\nbaba"

# minimum size
assert run("2\nab\n") == "0\nab"

# all same characters
assert run("6\naaaaaa\n") == "3\nababab"

# already balanced
assert run("4\nabba\n") == "0\nabba"

# alternating worst case
assert run("6\nababab\n") == "0\nababab"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 4 bbbb | 2 baba | basic correction |
| 2 ab | 0 ab | already valid |
| 6 aaaaaa | 3 ababab | heavy flipping |
| 4 abba | 0 abba | already valid |
| 6 ababab | 0 ababab | optimal no-op case |

## Edge Cases

A key edge case is when both characters in a pair are identical, such as `"aa"` or `"bb"`. In these cases, both target configurations require exactly one flip. For `"aa"`, making `"ab"` flips the second character, while making `"ba"` flips the first character, so both cost 1. The algorithm handles this by allowing either choice, ensuring correctness regardless of tie-breaking.

Another edge case is when the string is already alternating. In this case every pair already matches either `"ab"` or `"ba"`, so all computed costs are zero. The algorithm naturally produces zero operations and returns the original string unchanged.
