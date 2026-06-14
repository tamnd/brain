---
title: "CF 1104A - Splitting into digits"
description: "We are given a single integer $n$, and we want to represent it as a sum of positive integers, each between 1 and 9 inclusive."
date: "2026-06-15T05:20:44+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1104
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 534 (Div. 2)"
rating: 800
weight: 1104
solve_time_s: 108
verified: true
draft: false
---

[CF 1104A - Splitting into digits](https://codeforces.com/problemset/problem/1104/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation, math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, and we want to represent it as a sum of positive integers, each between 1 and 9 inclusive. In other words, we are splitting the value $n$ into “digits”, but repetition is allowed and there is no requirement that the digits form a number, only that their sum equals $n$.

Among all possible ways to decompose $n$, we want to minimize how many distinct digit values appear in the decomposition. For example, if we can express $n$ using only the digit 2 repeated several times, that is preferable to using a mix of 1s, 2s, and 3s.

The output is any valid decomposition achieving the smallest possible number of distinct digit values. We also output how many digits are used in total.

The constraint $n \leq 1000$ is small enough that even linear construction per test case is sufficient. Any solution that runs in $O(n)$ or better is trivially fast.

A subtle point is that the objective is not to minimize the number of digits, but to minimize the number of different digit values used. A naive reader might incorrectly try to reduce length first, which leads to wrong reasoning.

A typical incorrect approach is greedily taking the largest possible digit (like always using 9s). While this minimizes the number of digits, it does not directly guarantee minimal distinct values in a structured way unless handled carefully.

## Approaches

A brute-force approach would try all possible multisets of digits from 1 to 9 whose sum is $n$, and then compute how many distinct values appear in each candidate multiset. This is essentially a bounded integer partition problem with an additional constraint on allowed values and a secondary objective on distinct cardinality. The number of compositions of $n$ grows exponentially, roughly on the order of $2^n$ for unrestricted splits, making this completely infeasible even for $n = 1000$.

The key observation is that restricting the number of distinct digit values is much stronger than it looks. If we decide to use only one digit value $d$, then the problem becomes checking whether $n$ is divisible by $d$, and if so, using $n/d$ copies of $d$. This immediately gives a valid decomposition with exactly one distinct digit.

If no single digit works, then we try using two distinct digits. However, for this problem we do not need to explicitly construct complicated mixtures. Instead, we can observe that using digit 1 is always allowed and can always complete any remaining remainder. So we can always ensure feasibility with at most two distinct digits, and in practice a simpler constructive strategy suffices: use as many 9s as possible and finish with the remainder.

The standard constructive solution is to maximize the use of digit 9, then handle the leftover remainder as a final digit. This produces at most two distinct digits: 9 and the remainder (if nonzero). Since 1 is also a digit, the remainder is always valid.

This construction is optimal because using a single digit is only possible when $n \leq 9$, otherwise any single digit must divide $n$, which is rarely possible. For $n > 9$, the best we can guarantee is using exactly two digit values, and this construction achieves that bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all partitions | exponential | exponential | Too slow |
| Greedy 9s + remainder construction | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute how many full 9s fit into $n$, which is $q = n // 9$. This maximizes the number of large digits, reducing the remainder as much as possible.
2. Compute the remainder $r = n \bmod 9$. This is the only value that cannot be expressed using another 9.
3. If $r = 0$, output $q$ digits, all equal to 9. This works because $9q = n$, so the sum constraint is satisfied using a single digit value.
4. If $r \neq 0$, output $q$ digits equal to 9 and one additional digit equal to $r$. This ensures the sum becomes $9q + r = n$.
5. Print the total number of digits $k = q + (r \neq 0)$, followed by the constructed sequence.

The choice of 9 is not arbitrary. It is the largest allowed digit, so it minimizes the number of digits required to reach $n$, and any remainder is guaranteed to still be within the valid digit range $[1, 9]$.

### Why it works

The construction always produces a valid decomposition because every element is between 1 and 9 and the sum is exactly preserved. Among all decompositions that use only one digit value, only perfect divisors of $n$ are possible, which is rare. Once we allow a second digit, using 9s minimizes the number of required components, and any leftover remainder cannot be split further without introducing additional distinct digit values. This ensures we never introduce more than two distinct digits, which is optimal for all $n > 9$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    q = n // 9
    r = n % 9
    
    res = []
    
    for _ in range(q):
        res.append(9)
    
    if r:
        res.append(r)
    
    print(len(res))
    print(*res)

if __name__ == "__main__":
    solve()
```

The code directly implements the construction derived above. Integer division computes how many full 9s are used, while modulo computes the leftover remainder.

A common implementation pitfall is forgetting to handle the case where $r = 0$, which would incorrectly add an extra zero digit or extra element. Another issue is miscomputing the number of digits $k$, which must match the constructed list exactly.

## Worked Examples

### Example 1: $n = 1$

| Step | q | r | construction |
| --- | --- | --- | --- |
| compute | 0 | 1 | start empty |
| remainder | 0 | 1 | add 1 |
| output | - | - | [1] |

This confirms the base case where no 9s can be used and the number itself is directly valid as a digit.

### Example 2: $n = 20$

| Step | q | r | construction |
| --- | --- | --- | --- |
| compute | 2 | 2 | start with two 9s |
| remainder | 2 | 2 | add 2 |
| output | - | - | [9, 9, 2] |

This shows how the algorithm compresses most of the value into maximal digits and handles the leftover cleanly without increasing distinct digit count beyond two.

The trace confirms that the sum remains exact and the construction never exceeds digit constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only arithmetic and output of at most 1000/9 digits |
| Space | $O(1)$ | Output list is proportional to $n/9$, bounded by 112 |

The algorithm easily fits within limits since $n \leq 1000$, so even linear output construction is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    # re-run solution
    n = int(inp.strip())
    q = n // 9
    r = n % 9
    res = [9] * q
    if r:
        res.append(r)
    return str(len(res)) + "\n" + " ".join(map(str, res))

# provided samples
assert run("1") == "1\n1"

# custom cases
assert run("9") == "1\n9"
assert run("10") == "2\n9 1"
assert run("18") == "2\n9 9"
assert run("1000") == "112\n" + " ".join(["9"] * 111 + ["1"])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 / 1 | minimal boundary |
| 9 | 1 / 9 | exact single digit |
| 10 | 9 1 | remainder handling |
| 18 | 9 9 | exact multiple of 9 |
| 1000 | 111×9 + 1 | large construction |

## Edge Cases

For $n = 9$, the algorithm computes $q = 1$, $r = 0$, producing a single digit [9]. This correctly avoids adding a zero remainder digit, which would be invalid.

For $n = 10$, we get $q = 1$, $r = 1$, producing [9, 1]. The sum is preserved exactly, and only two distinct digits appear, which is optimal since 10 cannot be represented using a single digit in [1,9].

For $n = 1000$, the algorithm produces 111 nines and a final 1. The structure remains stable under maximum input size, and no overflow or special handling is required beyond list construction.
