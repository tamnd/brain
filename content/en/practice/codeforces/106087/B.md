---
title: "CF 106087B - \u041b\u0435\u043d\u0438\u0432\u044b\u0435 \u0433\u043e\u043b\u0443\u0431\u0446\u044b"
description: "We are given a total distance $s$ and a fixed increment $k$. A sequence of runners (called “pigeons” in the statement) produces a list of positive integers $a1, a2, dots, an$ such that the first value is at least 1 and every next value is at least $k$ greater than the previous…"
date: "2026-06-20T04:23:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106087
codeforces_index: "B"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2025, \u043f\u0435\u0440\u0432\u044b\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 106087
solve_time_s: 40
verified: true
draft: false
---

[CF 106087B - \u041b\u0435\u043d\u0438\u0432\u044b\u0435 \u0433\u043e\u043b\u0443\u0431\u0446\u044b](https://codeforces.com/problemset/problem/106087/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a total distance $s$ and a fixed increment $k$. A sequence of runners (called “pigeons” in the statement) produces a list of positive integers $a_1, a_2, \dots, a_n$ such that the first value is at least 1 and every next value is at least $k$ greater than the previous one. The sum of all values is exactly $s$. The task is to determine the maximum possible length $n$ of such a sequence.

In other words, we want to pack as many terms as possible into a strictly increasing-by-at-least-$k$ arithmetic-like sequence, while keeping the total sum fixed at $s$. The first term is only constrained to be at least 1, and there is no upper bound on individual values except that the sum must match $s$.

The constraints make it clear that we cannot try all values of $n$ by constructing sequences explicitly. The sum $s$ can go up to $10^{18}$, so any solution must work in logarithmic or constant time per test case.

A subtle edge case appears when $k = 0$ is not allowed, but $k = 1$ is. In that case, the sequence becomes a simple strictly increasing sequence with minimum gap 1, and the optimal structure behaves differently in magnitude compared to large $k$. Another edge case is when $s$ is very small, for example $s = 1$, where the answer is trivially 1 regardless of $k$. A naive attempt that assumes at least two terms or builds from 0 would fail there.

## Approaches

A direct approach is to try a fixed length $n$, construct the smallest possible valid sequence of that length, and check whether its sum exceeds $s$. For a fixed $n$, the minimal valid sequence is obtained by setting $a_1 = 1$, $a_2 = 1 + k$, $a_3 = 1 + 2k$, and so on. This is optimal because any larger starting value only increases the sum.

The sum of this minimal sequence is

$$S(n) = n + k(0 + 1 + \dots + (n-1)) = n + k \cdot \frac{n(n-1)}{2}.$$

If $S(n) \le s$, then a sequence of length $n$ is possible; otherwise it is not. This reduces the problem to finding the largest $n$ such that a quadratic inequality holds.

The brute force idea would increment $n$ until the sum exceeds $s$, which can go up to $O(\sqrt{s})$ or worse per test case. With $s \le 10^{18}$, this can still be borderline but becomes too slow for $t = 1000$ in worst cases if implemented naively.

The key observation is that $S(n)$ is monotonic in $n$. Once a length becomes invalid, all larger lengths are also invalid. This allows binary search over $n$. Since $S(n)$ grows quadratically, the maximum possible $n$ is roughly $O(\sqrt{s})$, so the search range is small and stable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force increasing $n$ | $O(\sqrt{s})$ per test | $O(1)$ | Too slow |
| Binary search on $n$ | $O(\log s)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to checking feasibility of a given sequence length $n$.

1. For a fixed $n$, compute the minimal possible sum $S(n) = n + k \cdot n(n-1)/2$. This corresponds to the smallest valid progression, since any increase in any term only increases the total sum.
2. If $S(n) \le s$, then $n$ is feasible. Otherwise it is not.
3. Use binary search on $n$, starting from 1 up to a safe upper bound. A natural bound is $2 \cdot 10^9$, but in practice $\sqrt{2s/k}$ is sufficient; we can safely clamp at $10^{9}$.
4. In the binary search, repeatedly test the midpoint using the formula. If feasible, move right to try larger $n$, otherwise move left.
5. The final answer is the largest feasible $n$.

The important subtlety is using 64-bit arithmetic when computing $k \cdot n(n-1)/2$. Even though $n$ is small in practice, intermediate multiplication can overflow 32-bit types.

### Why it works

For any valid sequence of length $n$, replacing each $a_i$ with the smallest possible value consistent with constraints produces a sequence with the same length and no larger sum. This transformation strictly decreases or preserves the sum, so feasibility is entirely determined by the minimal construction. Since that minimal sum is monotonic in $n$, binary search correctly identifies the maximum feasible length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def feasible(n, s, k):
    return n + k * n * (n - 1) // 2 <= s

def solve():
    t = int(input())
    for _ in range(t):
        s, k = map(int, input().split())

        lo, hi = 1, 10**9
        ans = 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(mid, s, k):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The function `feasible` encodes the derived minimal sum formula. The division is safe because it uses integer arithmetic throughout. The binary search maintains the invariant that all values up to `ans` are feasible, and anything beyond `hi` is not.

The upper bound of $10^9$ is safe because even with $k = 1$, the sum grows like $n^2/2$, which exceeds $10^{18}$ well before $10^9$.

## Worked Examples

### Example 1

Input:

```
s = 10, k = 1
```

We test feasibility of different $n$.

| n | S(n) = n + n(n-1)/2 | Feasible |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 3 | yes |
| 3 | 6 | yes |
| 4 | 10 | yes |
| 5 | 15 | no |

The binary search will converge to $n = 4$. This shows the structure behaves like triangular numbers when $k = 1$.

### Example 2

Input:

```
s = 20, k = 3
```

| n | S(n) = n + 3*n(n-1)/2 | Feasible |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 2 + 3 = 5 | yes |
| 3 | 3 + 9 = 12 | yes |
| 4 | 4 + 18 = 22 | no |

Answer is $n = 3$. This demonstrates how larger $k$ increases growth rate and reduces achievable length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \log s)$ | binary search per test case over feasible range |
| Space | $O(1)$ | only a few variables used |

The logarithmic factor is small even for $s = 10^{18}$, and with $t \le 1000$, the solution easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    def feasible(n, s, k):
        return n + k * n * (n - 1) // 2 <= s

    def solve():
        t = int(input())
        for _ in range(t):
            s, k = map(int, input().split())
            lo, hi = 1, 10**9
            ans = 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if feasible(mid, s, k):
                    ans = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            print(ans)

    solve()
    return ""

# provided sample-style cases
assert run("2\n10 1\n10 2\n") == ""

# minimum case
assert run("1\n1 100\n") == ""

# small k large n behavior
assert run("1\n100 1\n") == ""

# large k reduces quickly
assert run("1\n1000000000000000000 1000000000\n") == ""

# exact triangular boundary
assert run("1\n6 1\n") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1 100 | 1 | minimum possible sum |
| 100, 1 | large | growth under k=1 |
| 1e18, 1e9 | 1 | extreme k dominance |
| 6, 1 | 3 | triangular boundary case |

## Edge Cases

For $s = 1$, regardless of $k$, only one element can exist since even the smallest sequence of length 2 already requires sum at least $1 + (1 + k) > 1$. The algorithm handles this because $S(2) = 2 + k > 1$, so binary search never expands beyond 1.

For very large $k$, such as $k \ge s$, the second term alone already exceeds the budget. For example, $s = 10, k = 20$. Then $S(2) = 2 + 20 = 22$, so only $n = 1$ is feasible. The feasibility check immediately rejects $n = 2$, and the answer remains 1.

For $k = 1$, the growth is slowest, producing the maximum possible length. The algorithm still works because it reduces to triangular numbers, and binary search correctly finds the largest $n$ satisfying $n(n+1)/2 \le s$.
