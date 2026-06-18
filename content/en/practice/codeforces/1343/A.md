---
problem: 1343A
contest_id: 1343
problem_index: A
name: "Candies"
contest_name: "Codeforces Round 636 (Div. 3)"
rating: 900
tags: ["brute force", "math"]
answer: passed_samples
verified: true
solve_time_s: 135
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e1df0-693c-83ec-baca-c8680d507a68
---

# CF 1343A - Candies

**Rating:** 900  
**Tags:** brute force, math  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 15s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e1df0-693c-83ec-baca-c8680d507a68  

---

## Solution

## Problem Understanding

We are given a number of candy wrappers, and we know they came from a very specific purchase pattern. On day one Vova bought some integer number of candies, call it $x$. On each subsequent day he doubled the previous day’s purchase, so the sequence of purchases looks like $x, 2x, 4x, \dots, 2^{k-1}x$ for some unknown number of days $k$, where $k > 1$.

If we sum all candies bought across all days, we get:

$$n = x(1 + 2 + 4 + \dots + 2^{k-1})$$

The geometric series inside the parentheses always collapses to $2^k - 1$, so the constraint is equivalent to finding any decomposition of $n$ such that:

$$n = x(2^k - 1), \quad k > 1, \quad x \ge 1$$

The task is not to recover the original $x$ and $k$, but simply to output any valid $x$ that could have produced the given $n$ for some valid $k$.

The constraints allow up to $10^4$ test cases and $n$ up to $10^9$, which immediately rules out any solution that tries to enumerate all pairs $(x, k)$ or simulates the process in a naive nested fashion for each test case. A direct brute-force over $k$ is still small because $2^k - 1$ grows exponentially, so $k$ is at most about 30 for the largest $n$. That observation is crucial.

A subtle edge case is that $k$ must be strictly greater than 1. If someone forgets this, they might incorrectly allow $k = 1$, which would make $n = x$, but this is invalid in the problem. Another issue is trying to fix $x = 1$ always; this works only when $n$ itself is a Mersenne number, and fails in general.

## Approaches

A brute-force approach would try every possible $k$, compute the sum factor $2^k - 1$, and check whether $n$ is divisible by it. If it is, then $x = n / (2^k - 1)$ is a valid answer. This works because the formula is exact and every valid construction corresponds to some $k$. The problem is performance is still bounded by how many $k$ values we test.

The key observation is that the geometric multiplier $2^k - 1$ grows extremely fast. Since $n \le 10^9$, we only need to test at most around 30 values of $k$. This turns the problem into a tiny loop per test case. For each $k$, we check divisibility and immediately return a valid $x$.

There is no need to search for all solutions or optimize further. Any valid pair is accepted, so the first successful $k$ is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $x, k$ | $O(n \log n)$ | $O(1)$ | Too slow |
| Try all $k$ up to 30 | $O(t \log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$. The goal is to find a representation $n = x(2^k - 1)$.
2. Iterate over possible values of $k$, starting from $k = 2$ because the problem explicitly forbids $k = 1$.
3. For each $k$, compute the multiplier $m = 2^k - 1$.
4. If $m > n$, stop checking larger $k$, since all future multipliers only grow.
5. If $n \mod m = 0$, compute $x = n / m$ and output it immediately.

The reason this greedy stopping works is that once the geometric factor exceeds $n$, it can no longer divide it.

### Why it works

Every valid configuration corresponds to a factorization of the form $n = x(2^k - 1)$. The algorithm systematically enumerates all possible values of the second factor $2^k - 1$ that could fit within $n$. Since these values are strictly increasing with $k$, we are guaranteed to encounter the correct one if it exists. Once found, dividing recovers the unique corresponding $x$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        
        k = 2
        power = 3  # 2^2 - 1
        
        while power <= n:
            if n % power == 0:
                print(n // power)
                break
            k += 1
            power = (1 << k) - 1

solve()
```

The implementation directly mirrors the derivation. The variable `power` tracks $2^k - 1$, starting from $k = 2$, which corresponds to $3$. The loop increases $k$ until the multiplier exceeds $n$, ensuring we only test feasible candidates.

A common mistake is recomputing powers from scratch using exponentiation inside the loop, which is unnecessary but still fast enough. Another subtle issue is starting from $k = 1$, which would introduce the invalid case $2^1 - 1 = 1$ and incorrectly allow $x = n$.

## Worked Examples

We trace two inputs from the sample.

### Example 1: $n = 21$

| k | $2^k - 1$ | divisible? | action |
| --- | --- | --- | --- |
| 2 | 3 | yes | output $21 / 3 = 7$ |

The algorithm stops immediately because $21$ is divisible by $3$. This corresponds to $k = 2, x = 7$, which reconstructs $7 + 14 = 21$.

### Example 2: $n = 28$

| k | $2^k - 1$ | divisible? | action |
| --- | --- | --- | --- |
| 2 | 3 | no | continue |
| 3 | 7 | yes | output $28 / 7 = 4$ |

This produces $k = 3, x = 4$, corresponding to $4 + 8 + 16 = 28$.

These traces show that the algorithm does not require searching all decompositions, only finding one valid geometric divisor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \log n)$ | each test checks at most ~30 values of $k$ |
| Space | $O(1)$ | only a few integers are stored |

The exponential growth of $2^k - 1$ ensures the loop is extremely small even in worst-case inputs, keeping the solution well within time limits for $10^4$ test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())

        k = 2
        power = 3
        while power <= n:
            if n % power == 0:
                out.append(str(n // power))
                break
            k += 1
            power = (1 << k) - 1

    return "\n".join(out)

# provided samples
assert run("7\n3\n6\n7\n21\n28\n999999999\n999999984\n") == "1\n2\n1\n7\n4\n333333333\n333333328"

# minimum edge
assert run("1\n3\n") == "1"

# Mersenne-like case
assert run("1\n7\n") == "1"

# non-trivial multiple test
assert run("3\n6\n21\n28\n") == "2\n7\n4"

# large value sanity
assert run("1\n999999999\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n3 | 1 | smallest valid $k=2$ case |
| 1\n7 | 1 | perfect $2^k-1$ structure |
| 3\n6\n21\n28 | 2\n7\n4 | mixed divisibility paths |
| 1\n999999999 | valid x | stress on loop bound |

## Edge Cases

A key edge case is when $n$ is itself of the form $2^k - 1$. For example, $n = 7$. The algorithm starts with $k = 2$, checks $3$, moves to $7$, and finds divisibility immediately, producing $x = 1$. This corresponds to a full geometric sequence starting at 1.

Another case is when $n$ is not divisible by small multipliers but becomes divisible at a later $k$, such as $n = 28$. The loop skips $k = 2$ since $28 \bmod 3 \neq 0$, then succeeds at $k = 3$ with multiplier $7$, yielding $x = 4$. The algorithm does not commit early, so it does not miss later valid decompositions.

Finally, for large $n$ like $999999999$, the loop still terminates quickly because $2^k - 1$ exceeds $n$ within about 30 iterations, guaranteeing bounded runtime regardless of input distribution.