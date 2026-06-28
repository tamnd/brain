---
title: "CF 104854F - Factorial Prime"
description: "We are given a single integer $x$. Our task is to find the largest number $y$ that does not exceed $x$, with two properties at the same time. First, $y$ must be a prime number."
date: "2026-06-28T11:04:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104854
codeforces_index: "F"
codeforces_contest_name: "2023-2024 ICPC, Swiss Subregional"
rating: 0
weight: 104854
solve_time_s: 46
verified: true
draft: false
---

[CF 104854F - Factorial Prime](https://codeforces.com/problemset/problem/104854/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $x$. Our task is to find the largest number $y$ that does not exceed $x$, with two properties at the same time. First, $y$ must be a prime number. Second, $y$ must also be representable as a factorial of some integer, meaning there exists a positive integer $z$ such that $y = z!$.

So we are looking for numbers of the form $1!, 2!, 3!, \dots$ that are also prime, and among those we want the maximum one that is at most $x$. If no such number exists, we output $-1$.

The constraint $x \le 10^5$ is extremely small for competitive programming standards, which immediately suggests that we do not need any advanced data structures or asymptotically optimized number theory machinery. Even a constant-sized precomputation would be enough if the set of candidates is small.

A key subtlety lies in understanding factorial growth. Factorials grow extremely quickly, so only very small values of $z$ will produce results within the input range. This drastically limits the search space.

One potential mistake is to interpret the problem as searching over primes up to $x$ that have some hidden factorial representation. That would be incorrect, since factorial values themselves are very sparse, and we are not filtering primes in general, only factorial numbers.

To ground this with examples, if $x = 10$, then factorials are $1, 2, 6, 24, \dots$. Among these, the primes are $2$ only. So the answer is $2$. If $x = 1$, no factorial is both prime and valid in a meaningful sense, so the answer is $-1$.

## Approaches

A direct brute-force approach would generate factorials sequentially: start from $1! = 1$, then compute $2!, 3!, \dots$ until the value exceeds $x$. For each factorial value, we check whether it is prime. The largest valid one not exceeding $x$ becomes the answer.

This works because factorials grow fast enough that we only evaluate a handful of values even at the upper bound $10^5$. In fact, $5! = 120$ already exceeds the limit, so only $1!$ through $5!$ are ever relevant.

The bottleneck of a naive mindset would be thinking we need to test primality for all numbers up to $x$, which would be $O(x \sqrt{x})$ or worse. That is unnecessary because factorial values are not dense; we only check at most five candidates.

The crucial observation is that factorials beyond $5!$ are irrelevant due to size, and among the small factorials, primality is easy to verify by inspection or a direct check.

Now we explicitly list factorial values and their primality:

$1! = 1$, not prime

$2! = 2$, prime

$3! = 6$, not prime

$4! = 24$, not prime

$5! = 120$, not prime

Beyond this, all factorials are even and larger than 2, so they cannot be prime. This completely collapses the problem to checking a constant set of candidates.

So the only possible valid value is $2$, provided $x \ge 2$. Otherwise, no solution exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Factorial + Prime Check | O(1) (effectively constant) | O(1) | Accepted |
| Optimal Precomputed Observation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Identify all factorial values that are within or potentially near the constraint range. We compute factorials starting from 1 until the value exceeds $x$, but we quickly notice the sequence becomes irrelevant after a few steps. This step ensures we do not assume too much about the structure without verification.
2. Check which of these factorial values are prime. This is the central filtering step, where we enforce both conditions of the problem simultaneously.
3. Track the largest factorial value that is both prime and $\le x$. Since factorials are increasing, this is naturally the last valid one encountered.
4. Output that value if it exists, otherwise output $-1$. This handles the case where no factorial satisfies primality.

A more direct refinement of these steps is recognizing that only $2! = 2$ survives the filtering process.

### Why it works

Factorials grow monotonically, and primality imposes a very strict constraint: except for 2, every factorial $n!$ for $n \ge 3$ is divisible by 2 and another integer, making it composite. This means the intersection of the set of factorials and the set of primes contains at most one element. Once we identify that element, no further search is necessary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def solve():
    x = int(input().strip())

    fact = 1
    best = -1
    z = 1

    while fact <= x:
        if is_prime(fact):
            best = fact
        z += 1
        fact *= z

    print(best)

if __name__ == "__main__":
    solve()
```

The solution constructs factorials incrementally using a running product. The loop condition ensures we never consider values exceeding $x$, which keeps the computation bounded. Each factorial is tested for primality, although in practice only $2$ passes.

The primality check is written in a standard $O(\sqrt{n})$ form. Even though it is overkill for such small values, it keeps the reasoning general and avoids hardcoding assumptions.

A subtle implementation detail is the order of updates: we multiply after incrementing $z$, ensuring we correctly generate $2!, 3!, 4!$, and so on without skipping values.

## Worked Examples

### Example 1

Input: $x = 10$

We generate factorials sequentially:

| z | factorial | is prime | best |
| --- | --- | --- | --- |
| 1 | 1 | False | -1 |
| 2 | 2 | True | 2 |
| 3 | 6 | False | 2 |
| 4 | 24 | False | 2 |

At $z=4$, factorial already exceeds 10, so we stop. The best valid value encountered is 2.

This trace shows that even though we compute multiple factorials, only one candidate matters.

### Example 2

Input: $x = 1$

| z | factorial | is prime | best |
| --- | --- | --- | --- |
| 1 | 1 | False | -1 |

The loop stops immediately since $1! = 1 \le x$, but no valid prime factorial is found.

This demonstrates the edge case where no solution exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | At most a few factorial iterations and constant-time primality checks |
| Space | O(1) | Only a handful of integer variables are stored |

The factorial sequence terminates almost immediately because values exceed $10^5$ very quickly, and primality checks are applied to extremely small numbers. This guarantees the solution comfortably fits within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# re-define solution for testing context
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def solve():
    x = int(sys.stdin.readline().strip())
    fact = 1
    best = -1
    z = 1
    while fact <= x:
        if is_prime(fact):
            best = fact
        z += 1
        fact *= z
    print(best)

# provided sample (x=1 style case)
assert run("1\n") == "-1", "sample-like case x=1"

# custom cases
assert run("2\n") == "2", "minimum valid answer"
assert run("10\n") == "2", "small range includes 2 only"
assert run("100000\n") == "2", "upper bound still only 2"
assert run("3\n") == "2", "boundary just above 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | -1 | no valid factorial prime |
| 2 | 2 | smallest valid case |
| 10 | 2 | intermediate range correctness |
| 100000 | 2 | upper bound stability |

## Edge Cases

### Case: x = 1

For $x = 1$, we start with $1! = 1$. The algorithm evaluates it, sees it is not prime, and immediately terminates the loop after confirming no valid candidate. The output remains $-1$, matching the requirement that no factorial prime exists below or equal to 1.

### Case: x ≥ 2

For any $x \ge 2$, the algorithm generates $1! = 1$, then $2! = 2$. At $2$, primality is confirmed, and best is updated to 2. Even though later factorials are generated, they exceed 2 quickly and are not prime. The algorithm preserves 2 as the final answer, demonstrating that the only surviving candidate is consistently selected regardless of input size.
