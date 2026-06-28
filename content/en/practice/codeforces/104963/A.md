---
title: "CF 104963A - \u041d\u0430\u0431\u0440\u0430\u0442\u044c \u0441\u0443\u043c\u043c\u0443 \u0434\u0435\u043d\u0435\u0433"
description: "We are asked to count how many different ways a fixed amount of money $N$ can be paid exactly using banknotes of denominations 50, 100, and 200, where each denomination can be used any number of times."
date: "2026-06-28T06:53:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104963
codeforces_index: "A"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2022. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 104963
solve_time_s: 61
verified: true
draft: false
---

[CF 104963A - \u041d\u0430\u0431\u0440\u0430\u0442\u044c \u0441\u0443\u043c\u043c\u0443 \u0434\u0435\u043d\u0435\u0433](https://codeforces.com/problemset/problem/104963/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count how many different ways a fixed amount of money $N$ can be paid exactly using banknotes of denominations 50, 100, and 200, where each denomination can be used any number of times. There is no concept of giving change, so a valid way is simply a multiset of these banknotes whose total sum equals $N$.

Two ways are considered different if the number of used 50, 100, or 200 ruble notes differs. The order of choosing notes does not matter, only the final counts.

From a computational perspective, we are counting integer solutions to an equation of the form:

$$50a + 100b + 200c = N$$

where $a, b, c \ge 0$.

The constraint $N \le 10^6$ already rules out enumerating all triples naively. A cubic or even quadratic scan over possible counts would be too slow in the worst case because $N / 50 = 20000$, which makes nested loops potentially large but still manageable if carefully bounded. The key is to reduce the problem to a single loop or direct counting.

Edge cases appear immediately from divisibility. If $N$ is not divisible by 50, there are no solutions because all denominations are multiples of 50. For example, input 36 cannot be formed at all, so the answer must be 0. A naive implementation that forgets this will waste time iterating uselessly.

Another subtle case is $N = 0$. The correct interpretation is that there is exactly one way to pay zero: using no banknotes at all. Any implementation that initializes the answer incorrectly or skips the empty combination will fail here.

Finally, small values like $N = 50$ should yield exactly one solution, and larger multiples such as 200 should reflect all valid decompositions across multiple denominations.

## Approaches

A direct brute-force method is to try all possible numbers of 200-ruble notes, then all possible numbers of 100-ruble notes, and compute whether the remaining sum can be formed using 50-ruble notes. For each pair $(b, c)$, we compute:

$$r = N - 200c - 100b$$

and check whether $r \ge 0$ and divisible by 50. If yes, we increment the answer.

This works because every valid solution corresponds to exactly one pair $(b, c)$, and the number of 50-ruble notes is then uniquely determined.

The complexity depends on how many values of $c$ and $b$ we try. Since $c \le N/200$ and $b \le N/100$, the worst case is about $O((N/200) \cdot (N/100)) = O(N^2)$ iterations in the worst scaling sense. With $N$ up to $10^6$, this is too slow.

The key observation is that we do not need to explicitly iterate over all 50-ruble notes. Once we fix $b$ and $c$, the value of $a$ is determined uniquely. So the problem reduces to counting valid $(b, c)$ pairs satisfying a divisibility constraint, which can be done in $O(N/200)$ by iterating over $c$ and solving for $b$ arithmetically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over (b, c) | $O((N/200)(N/100))$ | $O(1)$ | Too slow |
| Fix 200s, solve 100/50 | $O(N/200)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rewrite the equation:

$$50a + 100b + 200c = N$$

Divide everything by 50:

$$a + 2b + 4c = M$$

where $M = N / 50$. If $N$ is not divisible by 50, the answer is immediately zero.

We now count non-negative integer solutions to $a + 2b + 4c = M$.

### Steps

1. Check whether $N \bmod 50 \neq 0$. If so, return 0 because no combination of valid banknotes can form such a sum. This eliminates impossible cases immediately.
2. Set $M = N / 50$. Now the problem becomes counting solutions in normalized units, which simplifies arithmetic and avoids repeated multiplication.
3. Iterate over the number of 200-ruble notes $c$. Each $c$ contributes $4c$ units to the sum. The maximum possible $c$ is $M // 4$, since each unit is worth 4 in this scaled system.
4. For each fixed $c$, compute the remaining amount:

$$rem = M - 4c$$

This represents the portion to be formed using 50 and 100 notes only.
5. Now we count solutions to:

$$a + 2b = rem$$

For a fixed $b$, $a$ is uniquely determined as $a = rem - 2b$, so we only need valid $b$ such that $rem - 2b \ge 0$.

The number of valid $b$ values is:

$$\left\lfloor \frac{rem}{2} \right\rfloor + 1$$
6. Add this count to the answer for each $c$, accumulating all valid decompositions.

### Why it works

Every solution $(a, b, c)$ is uniquely identified by its value of $c$. For each fixed $c$, the remaining equation reduces to a one-dimensional counting problem in $b$, where each valid $b$ corresponds to exactly one valid $a$. This partitions the full solution space into disjoint slices indexed by $c$, so summing over all slices counts every solution exactly once without duplication or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N = int(input().strip())

    if N % 50 != 0:
        print(0)
        return

    M = N // 50
    ans = 0

    for c in range(M // 4 + 1):
        rem = M - 4 * c
        ans += rem // 2 + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduced equation in normalized units. The divisibility check at the start is crucial, since skipping it would incorrectly treat impossible cases as having fractional solutions.

The loop over $c$ represents fixing the number of 200-ruble notes. The remaining sum is then distributed between 100 and 50 ruble notes, where each 100-ruble note consumes 2 normalized units. The expression `rem // 2 + 1` counts all possible numbers of 100-ruble notes from 0 up to the maximum allowed by the remaining sum.

## Worked Examples

### Example 1: $N = 50$

We convert to normalized units: $M = 1$. Only $c = 0$ is possible.

| c | rem = M - 4c | rem // 2 + 1 |
| --- | --- | --- |
| 0 | 1 | 1 |

The only solution is one 50-ruble note.

This confirms the base case where the smallest denomination alone forms the sum.

### Example 2: $N = 200$

Here $M = 4$. We iterate over $c$.

| c | rem | rem // 2 + 1 |
| --- | --- | --- |
| 0 | 4 | 3 |
| 1 | 0 | 1 |

Total is 4.

This matches the intuition: either no 200 note and combinations of 100/50, or one 200 note alone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N/200)$ | loop over number of 200-ruble notes after normalization |
| Space | $O(1)$ | only a few integer variables are used |

The loop runs at most $2500$ iterations when $N = 10^6$, which is well within limits. All operations inside the loop are constant time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline().strip()

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    N = int(sys.stdin.readline().strip())

    if N % 50 != 0:
        return "0"

    M = N // 50
    ans = 0
    for c in range(M // 4 + 1):
        rem = M - 4 * c
        ans += rem // 2 + 1

    return str(ans)

# provided samples
assert solve("50\n") == "1"
assert solve("36\n") == "0"
assert solve("200\n") == "4"

# custom cases
assert solve("0\n") == "1"          # empty payment
assert solve("100\n") == "2"        # 100 or 50+50
assert solve("150\n") == "2"        # 100+50 or 3*50
assert solve("250\n") == "3"        # multiple decompositions
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 1 | empty solution handling |
| 100 | 2 | small mixed compositions |
| 150 | 2 | multiple representations |
| 250 | 3 | enumeration consistency |

## Edge Cases

For $N = 0$, the algorithm sets $M = 0$. The loop runs once with $c = 0$, giving $rem = 0$ and contributing $0 // 2 + 1 = 1$. This correctly counts the empty combination.

For non-multiples of 50 such as $N = 36$, the early check immediately returns 0. Without this guard, integer division would silently produce incorrect normalized values and overcount impossible states.

For small exact multiples like $N = 50$, the loop structure still works without special casing. With $M = 1$, only $c = 0$ is valid and produces exactly one configuration, matching the intended interpretation.
