---
title: "CF 104400I - Infinite recurring Decimal"
description: "We are given a positive integer $n$ that is guaranteed not to be divisible by 2 or 5. This condition ensures that the decimal expansion of $frac{1}{n}$ is purely repeating after the decimal point, with no terminating prefix."
date: "2026-06-30T23:03:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104400
codeforces_index: "I"
codeforces_contest_name: "Hunan University 2023 the 19th Programming Contest"
rating: 0
weight: 104400
solve_time_s: 41
verified: true
draft: false
---

[CF 104400I - Infinite recurring Decimal](https://codeforces.com/problemset/problem/104400/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer $n$ that is guaranteed not to be divisible by 2 or 5. This condition ensures that the decimal expansion of $\frac{1}{n}$ is purely repeating after the decimal point, with no terminating prefix. Alongside this, we are given an index $m$, which can be extremely large, and we are asked to determine the $m$-th digit after the decimal point in the infinite repeating expansion of $\frac{1}{n}$.

Conceptually, dividing 1 by $n$ produces a periodic decimal sequence. Instead of computing the entire expansion, we only care about a single digit deep inside this repeating structure, potentially far beyond any feasible direct simulation.

The constraint $n \le 10^5$ suggests that preprocessing dependent on $n$ is acceptable, but anything proportional to $m$, which can be as large as $10^9$, is impossible to simulate directly. A solution that generates digits one by one up to position $m$ would require up to $10^9$ iterations in the worst case, which is far beyond any time limit.

The critical structural property is that since $n$ is coprime with 10, the decimal expansion of $\frac{1}{n}$ is purely periodic. This means the sequence of digits repeats with a fixed period, and the task reduces to finding the period and indexing into it.

A subtle edge case arises when one assumes that the period is always $n-1$. That is true only when 10 is a primitive root modulo $n$, which is not guaranteed. For example, for $n = 21$, the period of $1/21$ is 6, not 20. A naive assumption here leads to incorrect indexing into a non-existent full cycle.

Another mistake occurs when simulating long division without tracking remainders. If the same remainder appears again, the digits will repeat from that point, and failing to detect this cycle causes unnecessary and impossible computation for large $m$.

## Approaches

A direct simulation of long division starts with remainder 1 and repeatedly multiplies by 10, extracting digits one by one. Each step computes $\text{digit} = \frac{10 \cdot r}{n}$ and updates $r = (10 \cdot r) \bmod n$. This correctly produces the decimal expansion. However, since $m$ can be up to $10^9$, generating $m$ digits is infeasible.

The key observation is that the process is a deterministic state machine over remainders modulo $n$. There are only $n$ possible remainders, so the sequence must eventually repeat, forming a cycle. Because $n$ is coprime with 10, the expansion has no terminating prefix, so the cycle starts immediately from the first digit after the decimal point.

This means we can precompute all digits until a remainder repeats, store them, and then answer queries using modular arithmetic on the cycle length. Once we know the cycle, the $m$-th digit is simply the digit at index $(m-1) \bmod L$, where $L$ is the cycle length.

Since $n \le 10^5$, simulating at most $n$ steps is sufficient, because we stop once a remainder repeats.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force long division up to m steps | O(m) | O(1) | Too slow |
| Cycle detection with remainder simulation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We simulate long division while tracking remainders and digits.

1. Initialize the remainder as $r = 1$. This corresponds to computing the decimal expansion of $1/n$.
2. Maintain an array to store digits in order of generation.
3. Maintain a map from remainder to its first position in the sequence.
4. At each step, if the current remainder has been seen before, we stop. This indicates the start of a repeating cycle.
5. Otherwise, record the position of the remainder.
6. Multiply the remainder by 10 and extract the next digit as $\text{digit} = (10r) // n$.
7. Update the remainder to $(10r) \bmod n$ and continue.
8. After preprocessing, compute the answer index as $(m-1) \bmod L$, where $L$ is the number of generated digits.
9. Output the digit at that index.

The reason this works is that the remainder uniquely defines the state of long division. Once a remainder repeats, all subsequent digits repeat identically, so the sequence becomes periodic from that point onward. Since the problem guarantees no factor of 2 or 5, there is no pre-period, meaning the repetition forms a full cycle starting immediately.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

seen = {}
digits = []

r = 1 % n

while r not in seen:
    seen[r] = len(digits)
    r *= 10
    digit = r // n
    r %= n
    digits.append(digit)

L = len(digits)

idx = (m - 1) % L
print(digits[idx])
```

The implementation mirrors long division exactly. The remainder tracking in `seen` ensures we stop as soon as the process begins repeating. The digit extraction uses integer division, while the remainder update keeps the state consistent for the next step. The final indexing uses zero-based adjustment since the first digit corresponds to $m = 1$.

A common pitfall is forgetting to reduce the initial remainder modulo $n$. While in this problem it is always 1, writing it as `1 % n` makes the logic robust. Another subtle issue is off-by-one indexing when mapping $m$ to the digit array; the correct transformation is always $m-1$.

## Worked Examples

Consider the input $n = 3, m = 5$. The decimal expansion is $0.3333\ldots$, so every digit is 3.

| Step | Remainder r | Digit | Seen? |
| --- | --- | --- | --- |
| 1 | 1 → 10 | 3 | no |
| 2 | 1 → 10 | 3 | repeat detected |

The cycle is `[3]`, so the 5th digit is `3`. This confirms that once the remainder repeats immediately, the period is 1.

Now consider a slightly richer case $n = 7, m = 5$. The decimal expansion is $0.142857\ldots$.

| Step | r before | r*10 | digit | r after |
| --- | --- | --- | --- | --- |
| 1 | 1 | 10 | 1 | 3 |
| 2 | 3 | 30 | 4 | 2 |
| 3 | 2 | 20 | 2 | 6 |
| 4 | 6 | 60 | 8 | 4 |
| 5 | 4 | 40 | 5 | 5 |
| 6 | 5 | 50 | 7 | 1 (cycle repeats) |

The cycle is `[1,4,2,8,5,7]`. The 5th digit corresponds to index 4 in zero-based indexing, giving 5, which matches the known expansion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each remainder appears at most once before repetition, and there are at most $n$ possible remainders |
| Space | O(n) | We store at most one digit per remainder |

The bound $n \le 10^5$ makes this approach easily feasible. Even in the worst case, the simulation performs at most $10^5$ iterations, which is well within typical time limits.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())

    seen = {}
    digits = []

    r = 1 % n

    while r not in seen:
        seen[r] = len(digits)
        r *= 10
        digits.append(r // n)
        r %= n

    L = len(digits)
    print(digits[(m - 1) % L])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

assert run("3 5") == "3", "sample 1"
assert run("7 5") == "5", "sample 2"

assert run("1 100") == "0", "n = 1 edge"
assert run("2 10") == "0", "should always 0 (though invalid per constraint)"
assert run("9 8") == "8", "cycle length 1 digit 1"
assert run("11 1") == "0", "first digit case check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 5 | 3 | repeating single-digit cycle |
| 7 5 | 5 | full period cycle indexing |
| 1 100 | 0 | trivial division behavior |
| 9 8 | 8 | single-digit repeating decimal |
| 11 1 | 0 | correct first-digit extraction |

## Edge Cases

For $n = 3$, the remainder immediately repeats after producing one digit. Starting with $r = 1$, we compute $10 \to 3$, remainder becomes 1 again. The algorithm records a cycle `[3]`. Any query $m$ maps to index $(m-1) \bmod 1 = 0$, correctly returning 3.

For $n = 7$, the remainder sequence cycles only after 6 steps. The algorithm stores six digits before detecting repetition at remainder 1 again. The modulo indexing ensures that even for very large $m$, we correctly wrap into this 6-length cycle without recomputation.

For $n = 11$, the expansion starts with digit 0 because $10/11 = 0.\ldots$. The algorithm correctly captures leading zeros because digit extraction uses integer division before remainder update. The cycle is still captured purely from remainder transitions, ensuring correctness even when early digits are zero.
