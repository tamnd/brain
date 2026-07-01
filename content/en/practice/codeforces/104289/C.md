---
title: "CF 104289C - Equal Digits"
description: "We are given a positive integer $n$, and we need to find the smallest integer $k$ such that $k ge n$ and every digit of $k$ is identical. Such numbers look like $1, 2, 3, dots, 9, 11, 22, 33, dots, 9999$, where a single digit is repeated some number of times."
date: "2026-07-01T20:36:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104289
codeforces_index: "C"
codeforces_contest_name: "Bangladesh CP Server - BCS Round 1 (Div. 3)"
rating: 0
weight: 104289
solve_time_s: 77
verified: false
draft: false
---

[CF 104289C - Equal Digits](https://codeforces.com/problemset/problem/104289/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a positive integer $n$, and we need to find the smallest integer $k$ such that $k \ge n$ and every digit of $k$ is identical. Such numbers look like $1, 2, 3, \dots, 9, 11, 22, 33, \dots, 9999$, where a single digit is repeated some number of times.

The task is essentially about finding the next “uniform digit number” that is not smaller than the given input. The input can be as large as $10^{18}$, so $n$ can have up to 18 digits. This immediately rules out any approach that tries to iterate upward from $n$ one by one, because even a single step per candidate could lead to up to $10^{18}$ operations in the worst case, which is far beyond any feasible time limit.

The structure of the output is also constrained: every valid candidate number is fully determined by two choices, the digit $d \in [1,9]$ and the length $L \ge 1$. This already suggests the search space is small and highly structured.

The main edge cases come from boundary transitions between digit lengths. For example, if $n = 9992$, the answer is $9999$, but if $n = 9999$, the answer jumps to $11111$. A naive approach that only tries same-length candidates would fail in the latter case. Another subtle case is when the smallest valid number of the same length is still too small, forcing us to move to the next length entirely.

## Approaches

A brute-force approach would start from $n$ and repeatedly increment by one, checking whether all digits are identical. Checking a number is cheap, only $O(\log n)$, but in the worst case we might scan through a huge range before hitting the next valid number. If $n$ is something like 1000000, the next valid number is 1111111, meaning about a million checks in the worst case, each with digit scanning. This becomes too slow for the upper bound of $10^{18}$.

The key observation is that valid numbers are extremely sparse and structured. For each length $L$, there are only nine candidates: $d \times 111...1$ with $L$ digits. So instead of searching number by number, we only need to consider a small set of candidates formed by repeating digits.

The strategy becomes: for each possible digit length $L$ around the length of $n$, generate all uniform-digit numbers and pick the smallest one that is at least $n$. Since $L$ is at most 18, and digits are 1 through 9, we are checking at most 162 candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer − n) · O(digits) | O(1) | Too slow |
| Optimal | O(9 · number of digits) | O(1) | Accepted |

## Algorithm Walkthrough

We rely on the fact that any valid answer must be one of a very small set of constructed numbers.

1. Compute the number of digits $L$ in $n$. This gives the natural scale of candidates we should first inspect.
2. Generate all numbers formed by repeating a digit $d \in [1,9]$, exactly $L$ times. Each such number can be constructed as $d \cdot (111...1)$. We compare each against $n$ and track the smallest valid one.
3. Also generate all such numbers for length $L + 1$, because if no valid $L$-digit number is large enough, the answer must be the smallest uniform number with one more digit. This captures transitions like 9999 → 11111.
4. Among all candidates from lengths $L$ and $L+1$, pick the minimum value that is at least $n$.

Each step is justified by the fact that uniform-digit numbers are strictly ordered first by length and then by digit value within the same length.

### Why it works

Every valid number belongs to a discrete set indexed by its length and digit value. For a fixed length, there are no gaps in this set beyond digit repetition, so any candidate answer must appear in the constructed list. Considering only lengths $L$ and $L+1$ is sufficient because any number with length smaller than $L$ is already below $n$, and any number with length greater than $L+1$ is strictly larger than any candidate we need to consider. This guarantees that the minimum over the generated candidates is exactly the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def make(d, length):
    return int(str(d) * length)

def solve():
    n = int(input().strip())
    s = str(n)
    L = len(s)

    candidates = []

    for length in (L, L + 1):
        for d in range(1, 10):
            candidates.append(make(d, length))

    ans = min(x for x in candidates if x >= n)
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation constructs candidate numbers by repeating digit characters, which is safe because Python handles arbitrary-length integers efficiently for these sizes. The loop over digits 1 through 9 ensures we cover all uniform-digit numbers of a given length.

The decision to include both lengths $L$ and $L+1$ is critical. Without $L+1$, cases like 999 or 9999 would fail because no same-length candidate can satisfy the condition.

## Worked Examples

### Example 1: n = 6528

We compute $L = 4$. We generate all 4-digit uniform numbers and all 5-digit ones.

| length | digit | value |
| --- | --- | --- |
| 4 | 6 | 6666 |
| 4 | 7 | 7777 |
| 4 | 8 | 8888 |
| 4 | 9 | 9999 |
| 5 | 1 | 11111 |
| 5 | 2 | 22222 |
| ... | ... | ... |

The smallest value ≥ 6528 is 6666.

This confirms that within the same digit length, the answer is simply the first uniform number that crosses the threshold.

### Example 2: n = 9952

Here $L = 4$. Among 4-digit candidates, only 9999 is large enough.

| length | digit | value |
| --- | --- | --- |
| 4 | 9 | 9999 |

No other 4-digit uniform number works. Since 9999 is valid, we do not need 5-digit numbers.

This demonstrates that we only move to longer lengths when all same-length candidates are insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(9 · 2 · L) | We generate at most 18 candidates per digit length range |
| Space | O(1) | Only a constant number of candidates are stored |

The constraints allow numbers up to 18 digits, and the algorithm performs only a few dozen integer constructions and comparisons, which is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def make(d, length):
        return int(str(d) * length)

    n = int(input().strip())
    s = str(n)
    L = len(s)

    candidates = []
    for length in (L, L + 1):
        for d in range(1, 10):
            candidates.append(make(d, length))

    ans = min(x for x in candidates if x >= n)
    return str(ans)

# provided samples
assert run("6528\n") == "6666"
assert run("9952\n") == "9999"

# custom cases
assert run("1\n") == "1", "minimum case"
assert run("9\n") == "9", "single digit max boundary"
assert run("10\n") == "11", "transition to repeated digits"
assert run("9999\n") == "11111", "length increase boundary"
assert run("777\n") == "777", "already uniform"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest possible input |
| 9 | 9 | boundary of single digit space |
| 10 | 11 | transition from non-uniform to uniform |
| 9999 | 11111 | length increase behavior |
| 777 | 777 | already valid number |

## Edge Cases

One important edge case is when the input is already a uniform digit number. For example, $n = 777$. The algorithm still generates candidates for length 3, and since 777 itself is in the candidate set, it will be selected correctly as the minimum valid value.

Another case is when the number is just below a uniform threshold, such as $n = 9999$. All 4-digit uniform numbers below 9999 except 9999 itself are valid but smaller than $n$, so none qualify. The algorithm correctly moves to 5-digit candidates and selects 11111, matching the required wrap-around behavior.

A third case is small inputs like $n = 1$. Here the candidate generation includes 1-digit uniform numbers, and the minimum valid candidate is 1 itself, so no unnecessary escalation occurs.
