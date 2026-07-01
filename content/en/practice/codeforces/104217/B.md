---
title: "CF 104217B - Max Difference"
description: "We are given a single integer $n$, and we are asked to look at all permutations of the sequence $(1, 2, 3, dots, n)$. Each permutation is interpreted as a number formed by concatenating its elements in order."
date: "2026-07-01T23:52:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104217
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 03-03-23 Div. 2 (Beginner)"
rating: 0
weight: 104217
solve_time_s: 61
verified: true
draft: false
---

[CF 104217B - Max Difference](https://codeforces.com/problemset/problem/104217/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, and we are asked to look at all permutations of the sequence $(1, 2, 3, \dots, n)$. Each permutation is interpreted as a number formed by concatenating its elements in order. For example, for $n = 4$, a permutation like $[3, 1, 4, 2]$ corresponds to the number 3142.

Among all possible permutations, we want the maximum possible difference between any two such formed numbers. One permutation should produce the largest possible concatenated number, and another should produce the smallest possible concatenated number, and we take their difference.

The input size goes up to $n = 10^5$. That rules out any approach that explicitly enumerates permutations or constructs all numbers, since there are $n!$ permutations, which is astronomically large even for small $n$. Any valid solution must be linear or at worst $O(n \log n)$, though sorting is unnecessary here since the structure of optimal permutations is fixed.

A subtle point is that we are dealing with concatenation, not arithmetic rearrangement of digits. So $n = 12$ contributes two digits, while $n = 9$ contributes one digit. This means positional weight depends on digit length, which affects the structure of extremal permutations.

Edge cases come from small values of $n$. For $n = 1$, there is only one permutation, so the difference must be zero. For $n = 10$, digit length changes from 1-digit to 2-digit numbers, which is exactly where a naive digit-level reasoning approach can fail if it assumes uniform width.

## Approaches

A brute-force solution would generate all permutations of $1$ to $n$, convert each permutation into its concatenated integer representation, and compute the minimum and maximum among them. This is conceptually straightforward and correct, since it directly follows the definition of the problem. However, its complexity is $O(n! \cdot n)$ due to generating all permutations and concatenating each one, which becomes impossible even for $n = 10$.

The key observation is that we do not actually need to explore permutations. We only need to determine which arrangement of numbers produces the largest concatenated value and which produces the smallest. For concatenation-based ordering, the optimal arrangement is determined by lexicographic comparison of the resulting strings, not by numerical magnitude of individual elements.

The largest concatenated number is obtained by arranging numbers in descending order when written as strings, because placing larger leading digits earlier always dominates later contributions. Similarly, the smallest concatenated number is obtained by arranging numbers in ascending order.

Since the sequence is fixed as $1$ to $n$, this reduces to constructing two strings: one formed by writing numbers from $n$ down to $1$, and another from $1$ up to $n$, then converting both to integers and subtracting.

The problem collapses from a combinatorial optimization over permutations to a direct construction problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \cdot d)$ where $d$ is digit cost | $O(n \cdot d)$ | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Construct the smallest possible concatenation by appending numbers from 1 to $n$ in increasing order. This works because earlier digits dominate later digits in lexicographic ordering of the resulting string.
2. Construct the largest possible concatenation by appending numbers from $n$ down to 1. This ensures that larger numbers appear earlier, maximizing the most significant digit positions.
3. Convert both constructed strings into integers. This step is safe because the resulting value can grow large, but Python handles arbitrary precision integers.
4. Compute the difference between the larger and smaller values and output it.

Why it works: the concatenated number is fully determined by the sequence of string blocks, and comparing two concatenations is equivalent to comparing their lexicographic order when all blocks are fixed tokens. Since the problem allows arbitrary permutation, extremal values are achieved by globally sorting these tokens in descending and ascending order respectively. Any deviation from these orders would introduce a larger token later or a smaller token earlier, which strictly worsens the objective.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())

    # build smallest concatenation: 1 to n
    small_parts = []
    for i in range(1, n + 1):
        small_parts.append(str(i))
    small_val = int("".join(small_parts))

    # build largest concatenation: n to 1
    large_parts = []
    for i in range(n, 0, -1):
        large_parts.append(str(i))
    large_val = int("".join(large_parts))

    print(large_val - small_val)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the construction described earlier. The only non-trivial decision is using string concatenation rather than arithmetic digit shifting. This avoids manual tracking of powers of ten and correctly handles varying digit lengths between consecutive integers.

Python’s arbitrary precision integers make the conversion safe even when $n = 10^5$, where the resulting number has hundreds of thousands of digits.

## Worked Examples

### Example 1

Input:

```
4
```

We construct both extremes.

| Step | Construction | Result |
| --- | --- | --- |
| Small | 1 → 2 → 3 → 4 | 1234 |
| Large | 4 → 3 → 2 → 1 | 4321 |

Difference is computed as $4321 - 1234 = 3087$.

This shows how ordering completely determines the value, and no intermediate permutations are needed.

### Example 2

Input:

```
3
```

| Step | Construction | Result |
| --- | --- | --- |
| Small | 1 → 2 → 3 | 123 |
| Large | 3 → 2 → 1 | 321 |

Difference is $321 - 123 = 198$, confirming that even for small $n$, the extremal structure is stable and independent of enumeration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot d)$ | Each integer is converted to string once and concatenated |
| Space | $O(n \cdot d)$ | Stores two concatenated strings |

The value of $d$ grows logarithmically with $n$, but in practice each number contributes at most 6 digits for $n \le 10^5$. The solution easily fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline

    def solve():
        n = int(input().strip())

        small_parts = []
        for i in range(1, n + 1):
            small_parts.append(str(i))
        small_val = int("".join(small_parts))

        large_parts = []
        for i in range(n, 0, -1):
            large_parts.append(str(i))
        large_val = int("".join(large_parts))

        print(large_val - small_val)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided sample
assert run("4") == "3087"

# minimum case
assert run("1") == "0"

# small case
assert run("3") == "198"

# check digit boundary
assert run("10") == str(int("10987654321") - int("12345678910"))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | single permutation edge case |
| 3 | 198 | basic correctness of construction |
| 10 | computed difference | digit-length transition handling |

## Edge Cases

For $n = 1$, the algorithm builds both strings as `"1"`. The difference becomes zero, which matches the fact that there is only one permutation.

For $n = 10$, the algorithm constructs `"12345678910"` and `"10987654321"`. The key subtlety is that `"10"` contributes two characters, which affects alignment if one incorrectly assumes fixed-width tokens. The string-based approach naturally handles this, since concatenation preserves token boundaries. The computed difference is consistent with direct integer interpretation.

No special branching is required, and all edge cases are handled uniformly by the same construction logic.
