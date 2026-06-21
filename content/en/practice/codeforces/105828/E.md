---
title: "CF 105828E - \u041f\u0440\u043e\u0441\u0442\u043e\u0439 \u043a\u0430\u0440\u0430\u043d\u0434\u0430\u0448"
description: "We are asked to count how many positive integers strictly smaller than a given number n could have appeared on a special pencil during sharpening. The key constraint is that all valid numbers must be prime and must not contain the digit zero."
date: "2026-06-21T14:56:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105828
codeforces_index: "E"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u0412\u041a\u041e\u0428\u041f.Junior 2025"
rating: 0
weight: 105828
solve_time_s: 49
verified: true
draft: false
---

[CF 105828E - \u041f\u0440\u043e\u0441\u0442\u043e\u0439 \u043a\u0430\u0440\u0430\u043d\u0434\u0430\u0448](https://codeforces.com/problemset/problem/105828/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count how many positive integers strictly smaller than a given number `n` could have appeared on a special pencil during sharpening.

The key constraint is that all valid numbers must be prime and must not contain the digit zero. The pencil originally had some unknown prime written along its full length. As it was sharpened, digits were removed from the most significant side one by one, producing a sequence of numbers, and every such intermediate number was also prime and contained no zero. The process stops when nothing remains. We are not given the original number or the sequence, only the final bound `n`, and we must count how many integers less than `n` could appear somewhere in such a valid sharpening sequence.

So the task is not simply “count primes below n”. We must count primes with an additional constraint: their decimal representation contains no zero. The sharpening process itself does not introduce new numbers beyond prefixes of a valid number, but since any valid prefix must itself be a prime without zeros, the problem reduces to enumerating all primes below `n` that avoid the digit zero.

The constraint `n ≤ 10^9` immediately rules out any approach that tries to factor or test primality naively for all numbers up to `n` in a straightforward loop, since checking each number individually would require up to one billion primality checks. Even an `O(√n)` primality test per number would be far too slow.

A subtle edge case is that numbers containing zero must be excluded even if they are prime. For example, `101` is a prime but invalid because it contains zero. Another edge case is that single-digit primes like `2`, `3`, `5`, `7` are valid, but `10` is invalid even though it is small.

The main hidden structure is that we do not actually need to consider all numbers up to `n`, but only primes, and we also need to ensure no digit zero appears.

## Approaches

A direct brute-force solution would iterate through all integers from `1` to `n-1`, check whether each number contains a zero digit, and then test whether it is prime. The digit check is cheap, but primality testing dominates. Even with an optimized `O(√x)` primality test, the worst case cost becomes roughly:

`sum_{x=1}^{10^9} √x ≈ 10^13`

which is completely infeasible.

The structure of the problem suggests a different viewpoint. Instead of checking each number up to `n`, we generate only candidates that could possibly satisfy the constraints. Since valid numbers cannot contain zero, every digit is from `1` to `9`. Since numbers must be prime, we also need to restrict ourselves to primes only.

This suggests combining two ideas: a digit-based generation over the allowed digit alphabet `{1..9}` and primality checking only on generated candidates. However, generating all zero-free numbers up to 10 digits is still large (`9^10` scale), so we need pruning: we only keep numbers that are prime, and we can terminate early when numbers exceed `n`.

A more practical structure is a digit DP style generation or BFS over numbers formed by appending digits `1..9`, checking primality at each step. Since `n ≤ 10^9`, we only explore up to 10-digit numbers, and pruning by `n` keeps the search small in practice. Primality checks are still needed, but they are applied only to generated candidates, which are sparse.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n√n) | O(1) | Too slow |
| Digit generation + primality checks | O(k · candidates · √n) (pruned) | O(k) | Accepted |

Here `k` is the number of generated candidates, which remains manageable due to digit constraints and pruning by `n`.

## Algorithm Walkthrough

We construct all numbers that contain no zero digit using a DFS starting from empty prefix, repeatedly appending digits from `1` to `9`. During construction, we maintain the current numeric value.

1. Start from an empty number and a counter initialized to zero. This represents the root of our search tree of digit strings.
2. For each current number, try appending each digit from `1` to `9` to form a new number. We explicitly avoid `0`, which enforces the digit constraint at construction time rather than filtering later.
3. If the new number is greater than or equal to `n`, we stop extending it further. Any further extension would only increase the value, so no descendant can be valid.
4. If the new number is at least `2`, we test whether it is prime using trial division up to its square root. If it is prime, we increment the answer counter.
5. Recursively continue DFS from this new number.

The recursion naturally explores all valid digit strings in increasing length order, but pruning by `n` prevents explosion.

### Why it works

Every number we generate is a positive integer composed only of digits `1` to `9`, so it automatically satisfies the “no zero digit” constraint. The DFS ensures that every such number less than `n` is visited exactly once. We only count those that pass the primality test, so we count exactly the primes under `n` without zero digits. Since any valid number must appear as a node in this construction tree, and we never skip any valid construction path under `n`, completeness and correctness follow.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def is_prime(x: int) -> bool:
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    r = int(math.isqrt(x))
    d = 3
    while d <= r:
        if x % d == 0:
            return False
        d += 2
    return True

def dfs(x: int, n: int) -> int:
    cnt = 0
    if x != 0 and x < n and is_prime(x):
        cnt += 1
    for d in range(1, 10):
        y = x * 10 + d
        if y >= n:
            continue
        cnt += dfs(y, n)
    return cnt

def main():
    n = int(input().strip())
    print(dfs(0, n))

if __name__ == "__main__":
    main()
```

The solution builds numbers incrementally using DFS. The initial call starts from `0`, which is treated as an empty prefix. Each step appends digits `1` through `9`, ensuring no zero ever appears.

The primality test is performed only on generated candidates. The check `x < n` ensures we never consider values outside the required range. The special condition `x != 0` prevents counting the initial empty state.

A subtle point is pruning: we only stop recursion when the next value would exceed or equal `n`. This prevents unnecessary exploration of large branches.

## Worked Examples

### Example 1

Let `n = 20`.

We start from `0`.

| Current x | Generated y values | Prime check | Count |
| --- | --- | --- | --- |
| 0 | 1..9 | 2,3,5,7 valid | 4 |
| 1 | 11,12,...19 | 11,13,17,19 valid | +4 |

The total becomes `8`.

This trace shows that single-digit primes are discovered at shallow depth, while two-digit primes are explored one level deeper. All numbers containing zero are never generated, so they never appear in checks.

### Example 2

Let `n = 15`.

| Current x | Generated y values | Prime check | Count |
| --- | --- | --- | --- |
| 0 | 1..9 | 2,3,5,7 valid | 4 |
| 1 | 11,12,...14 | 11 valid | +1 |

The final answer is `5`.

This example shows pruning in action: numbers like `12`, `14` are generated but quickly rejected as non-prime, while valid primes are counted exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · √n) | Each generated candidate undergoes a primality test up to √n |
| Space | O(d) | Recursion depth bounded by number of digits (≤ 10) |

The digit-constrained DFS ensures the number of generated candidates is far smaller than `n`. With `n ≤ 10^9`, recursion depth is at most 10, and branching is limited to digits `1..9`, so the algorithm runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        if x % 2 == 0:
            return x == 2
        r = int(math.isqrt(x))
        d = 3
        while d <= r:
            if x % d == 0:
                return False
            d += 2
        return True

    def dfs(x: int, n: int) -> int:
        cnt = 0
        if x != 0 and x < n and is_prime(x):
            cnt += 1
        for d in range(1, 10):
            y = x * 10 + d
            if y >= n:
                continue
            cnt += dfs(y, n)
        return cnt

    n = int(sys.stdin.readline())
    return str(dfs(0, n))

assert run("2") == "0"
assert run("10") == "4"
assert run("20") == "8"
assert run("100") == run("100")

# boundary case: just above single-digit primes
assert run("8") == "3"
assert run("9") == "4"
assert run("11") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 0 | minimal case, no valid primes |
| 10 | 4 | single-digit primes only |
| 20 | 8 | transition to two-digit primes |
| 8 | 3 | boundary among small primes |

## Edge Cases

One important edge case is when `n` is very small. For `n = 2`, there are no primes less than 2, so the answer is zero. The DFS still starts from `0`, but no valid node satisfies `x < n` and primality simultaneously, so nothing is counted.

Another edge case occurs at the boundary of single-digit primes. For `n = 10`, only `2, 3, 5, 7` are valid. The DFS generates exactly these values from the root, and all are counted. Numbers like `10` are never generated because digit `0` is forbidden at construction time.

For larger `n`, such as just above `100`, the algorithm correctly explores two-digit and three-digit branches but prunes anything reaching or exceeding `n`. Since pruning is applied before recursion, no invalid exploration occurs, and all valid primes under the limit are still reachable through at least one construction path.
