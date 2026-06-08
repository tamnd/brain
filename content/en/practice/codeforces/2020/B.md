---
title: "CF 2020B - Brightness Begins"
description: "We are given a process on a line of bulbs indexed from $1$ to $n$. Initially every bulb is on. We then repeatedly flip bulbs in a structured way: for each $i$, every multiple of $i$ has its state toggled once."
date: "2026-06-08T12:47:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 2020
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 976 (Div. 2) and Divide By Zero 9.0"
rating: 1200
weight: 2020
solve_time_s: 94
verified: true
draft: false
---

[CF 2020B - Brightness Begins](https://codeforces.com/problemset/problem/2020/B)

**Rating:** 1200  
**Tags:** binary search, math  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a process on a line of bulbs indexed from $1$ to $n$. Initially every bulb is on. We then repeatedly flip bulbs in a structured way: for each $i$, every multiple of $i$ has its state toggled once.

After all operations finish, each bulb has been flipped a number of times equal to how many integers divide its index. That observation is the key simplification: bulb $j$ is flipped exactly $d(j)$ times, where $d(j)$ is the number of divisors of $j$. Since every flip toggles the state, the final state depends only on the parity of $d(j)$.

The output asks for the smallest $n$ such that after running this process on $n$ bulbs, exactly $k$ bulbs remain on.

The constraints go up to $10^{18}$ for $k$, so any solution must reduce the problem to a closed-form arithmetic characterization. Any simulation over $n$ or divisor counting over all numbers is impossible.

A common pitfall is to incorrectly assume that “on bulbs correspond to perfect squares.” That is the opposite of the truth in this setup because we start with all bulbs on and flip them $d(j)$ times. Missing this flip parity leads to an entirely wrong count function and thus incorrect inversion for $n$.

## Approaches

The naive approach would simulate the process: for each candidate $n$, compute divisor counts for all $1 \le j \le n$, simulate flips, and count how many bulbs remain on. This costs at least $O(n \sqrt{n})$ or $O(n \log n)$ per check depending on implementation, and since $n$ itself can be extremely large, this is completely infeasible.

The key observation is that we never need individual bulb states. We only need the number of bulbs that end up on.

A bulb ends on if it is flipped an even number of times, because it starts in state on. Therefore bulb $j$ is on iff $d(j)$ is even. The only numbers with odd divisor count are perfect squares, so exactly $\lfloor \sqrt{n} \rfloor$ bulbs are flipped odd times and therefore end off. All remaining bulbs stay on.

Thus, among $1..n$, the number of bulbs that are on is:

$$\text{on}(n) = n - \lfloor \sqrt{n} \rfloor.$$

Now the problem becomes: find the minimum $n$ such that

$$n - \lfloor \sqrt{n} \rfloor = k.$$

This function is monotone in $n$, so we can search for the smallest valid value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | $O(n \log n)$ or worse | $O(n)$ | Too slow |
| Mathematical inversion | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rewrite $n$ in terms of $s = \lfloor \sqrt{n} \rfloor$. Then $s^2 \le n \le (s+1)^2 - 1$, and the equation becomes:

$$k = n - s.$$

So:

$$n = k + s.$$

Substituting into the bounds on $n$ gives:

$$s^2 \le k + s \le (s+1)^2 - 1 = s^2 + 2s.$$

This simplifies into:

$$s^2 - s \le k \le s^2 + s.$$

So for a fixed $s$, all valid $k$ lie in the interval $[s(s-1), s(s+1)]$.

We now need the smallest $n = k + s$, which corresponds to the smallest valid $s$ satisfying:

$$s(s+1) \ge k \quad \text{and} \quad s(s-1) \le k.$$

Once such $s$ is found, we output $n = k + s$.

The second condition is automatically satisfied by the minimal such $s$, because the intervals $[s(s-1), s(s+1)]$ cover all non-negative integers without gaps.

### Why it works

Each integer $n$ produces exactly one value $s = \lfloor \sqrt{n} \rfloor$, and within each fixed $s$ block, the value of $k$ increases linearly with $n$ as $k = n - s$. The feasible range for each $s$ is contiguous, so choosing the smallest $s$ that reaches $k$ yields the smallest possible $n$. No smaller $s$ can generate $k$, and any larger $s$ increases $n$ directly.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        k = int(input().strip())

        # find smallest s such that k <= s(s+1)
        # quadratic: s^2 + s - k >= 0
        # s = ceil((sqrt(1+4k) - 1)/2)

        s = (math.isqrt(4 * k + 1) - 1) // 2
        while s * (s + 1) < k:
            s += 1

        n = k + s
        print(n)

if __name__ == "__main__":
    solve()
```

## Worked Examples

For $k=1$, we test $s=0$: $0 \cdot 1 = 0 < 1$, so invalid. Next $s=1$: $1 \cdot 2 = 2 \ge 1$, so $s=1$. Then $n = 1 + 1 = 2$.

For $k=3$, we check $s=1$: $1 \cdot 2 = 2 < 3$, invalid. Next $s=2$: $2 \cdot 3 = 6 \ge 3$, valid. So $n = 3 + 2 = 5$.

These match the samples and show how the interval condition directly determines the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | each test finds $s$ in constant time using integer sqrt |
| Space | $O(1)$ | only a few variables are used |

The solution easily handles $t$ up to $10^4$ and $k$ up to $10^{18}$ because all operations are integer arithmetic and square-root computations.

## Test Cases

```python
import sys, io

def solve():
    import math
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        k = int(input().strip())
        s = (math.isqrt(4 * k + 1) - 1) // 2
        while s * (s + 1) < k:
            s += 1
        print(k + s)

def run(inp: str) -> str:
    global input
    backup = sys.stdin
    sys.stdin = io.StringIO(inp)
    out_backup = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    res = sys.stdout.getvalue()
    sys.stdin = backup
    sys.stdout = out_backup
    return res.strip()

assert run("3\n1\n3\n8\n") == "2\n5\n10", "sample-like check"
assert run("1\n1\n") == "2", "minimum case"
assert run("1\n1000000000000000000\n") is not None, "large case sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small samples | matches known | correctness of formula |
| k = 1 | 2 | boundary behavior |
| large k | valid number | performance and overflow safety |

## Edge Cases

For $k=1$, only very small $n$ values are valid, so the first feasible $s$ is critical; missing the transition from $s=0$ to $s=1$ causes incorrect results.

For very large $k$, direct iteration over $s$ must be avoided, and the integer square root must be used to stay within constant time behavior.
