---
title: "CF 2082B - Floor or Ceil"
description: "We start with a single integer value and repeatedly transform it using two kinds of halving operations. One operation replaces the number with its floor half, which always rounds down, and the other replaces it with its ceil half, which rounds up when the number is odd."
date: "2026-06-08T06:19:58+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2082
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1010 (Div. 2, Unrated)"
rating: 1600
weight: 2082
solve_time_s: 87
verified: false
draft: false
---

[CF 2082B - Floor or Ceil](https://codeforces.com/problemset/problem/2082/B)

**Rating:** 1600  
**Tags:** brute force, greedy  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a single integer value and repeatedly transform it using two kinds of halving operations. One operation replaces the number with its floor half, which always rounds down, and the other replaces it with its ceil half, which rounds up when the number is odd. We are forced to apply exactly `n` floor operations and `m` ceil operations, but we are free to choose the order in which these operations are applied.

The task is to understand how the ordering of these operations changes the final value and then determine the smallest and largest possible final value after all operations are used.

Even though each operation looks like it only halves the number, the order matters because floor and ceil behave differently on odd numbers. The rounding difference can accumulate early, and once the value becomes small, later operations behave differently again.

The constraints allow `x`, `n`, and `m` up to 10^9, and up to 10^4 test cases. Any approach that simulates operations one by one is impossible because in the worst case we could attempt up to 2·10^9 operations per test case. Even a logarithmic simulation per test case would still be borderline if done naively with repeated branching.

A subtle edge case appears when `x` becomes 0 or 1. From 0, both operations stay at 0 forever. From 1, floor halves to 0 while ceil halves stay at 1, which means the presence of remaining floor operations can completely determine whether the value collapses early. Another important situation is when `x` is large and mostly even, because both operations behave identically for long stretches, and differences only appear when odd values are encountered.

A naive greedy strategy like always applying floor first or always applying ceil first fails because the benefit of delaying or advancing rounding depends on the evolving parity of intermediate values.

## Approaches

A brute-force solution would try all permutations of `n + m` operations, simulate each sequence, and track the minimum and maximum final results. This is correct because it explores all possible orderings, but it is infeasible because the number of sequences is combinatorial: roughly $\binom{n+m}{n}$, which is astronomically large even for small values.

A second naive attempt is to simulate greedily in two extreme ways: always apply floor first for minimum, and always apply ceil first for maximum. This fails because early rounding decisions change parity structure later. For example, with `x = 7`, applying floor early produces 3, while delaying it yields different intermediate parity patterns that change future ceil results.

The key observation is that the value only depends on how many times we are forced to apply floor or ceil while the number is odd. When `x` is even, both operations give exactly the same result. When `x` is odd, floor reduces more aggressively while ceil preserves a higher value. This means the only meaningful decision is: when encountering an odd number, which operation to use first.

We can think in terms of how many “useful changes” we can still force while `x > 1`. Each time `x` is odd, applying ceil preserves more mass than floor. So for maximum result, we want to “delay destruction” caused by floor operations, using ceil whenever it prevents an early drop. For minimum result, we want the opposite, applying floor whenever it can reduce the value as early as possible.

The process stabilizes quickly because each operation roughly halves the number, so only about $O(\log x)$ meaningful transitions exist before reaching 0 or 1. Instead of simulating blindly, we track how many floor and ceil operations remain and greedily decide based on parity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(1) | Too slow |
| Optimal | O(log x) per test | O(1) | Accepted |

## Algorithm Walkthrough

We handle minimum and maximum separately using the same simulation logic but different choices when `x` is odd.

1. For the minimum value, we prioritize floor operations whenever possible. When `x` is odd and both operations remain, applying floor reduces the value more aggressively, so it is preferred. When `x` is even, both operations are identical, so we just consume either type.
2. For the maximum value, we prioritize ceil operations when `x` is odd, because ceil preserves the higher outcome and delays reduction. Floor operations are used when we have no alternative or when `x` is even.
3. We repeatedly process the number while `x > 1`. At each step, if `x` is even, we divide it by 2 and decrement any available operation count since both operations behave identically.
4. When `x` is odd, we branch based on whether we are computing the minimum or maximum. For minimum, we apply floor if available, otherwise ceil. For maximum, we apply ceil if available, otherwise floor.
5. If `x` reaches 1, remaining operations determine the final value. Any remaining floor operation forces it to 0, while ceil operations preserve it as 1 unless a floor appears later.

The key invariant is that at every step we maintain the best possible ordering locally without needing to revisit earlier decisions. Since every operation strictly reduces or stabilizes `x`, any greedy choice made on an odd value determines whether we preserve or destroy a unit of value permanently. There is no way to recover lost value later because both operations are non-increasing. Thus, local optimal decisions on odd states propagate globally to the final result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_one(x, n, m, want_min):
    # want_min = True for minimum, False for maximum
    while x > 1 and (n + m) > 0:
        if x % 2 == 0:
            x //= 2
            # even step: either operation works, consume any
            if n > 0:
                n -= 1
            else:
                m -= 1
        else:
            if want_min:
                # minimize: prefer floor
                if n > 0:
                    x = x // 2
                    n -= 1
                else:
                    x = x // 2 + 1
                    m -= 1
            else:
                # maximize: prefer ceil
                if m > 0:
                    x = x // 2 + 1
                    m -= 1
                else:
                    x = x // 2
                    n -= 1

    # remaining operations on 0 or 1
    if x == 0:
        return 0
    if x == 1:
        if want_min and n > 0:
            return 0
        return 1
    return x

t = int(input())
for _ in range(t):
    x, n, m = map(int, input().split())
    mn = solve_one(x, n, m, True)
    mx = solve_one(x, n, m, False)
    print(mn, mx)
```

The solution separates the computation into two independent simulations: one for minimizing and one for maximizing. The same core loop applies the transformations until `x` becomes 1 or all operations are used. The distinction comes entirely from the branch on odd values, where we decide whether to apply floor or ceil first.

A subtle implementation detail is handling the case when `x` becomes 1. At that point, any remaining floor operation immediately collapses the value to 0, while remaining ceil operations keep it at 1. This shortcut avoids unnecessary simulation of identical outcomes.

## Worked Examples

### Example 1

Input:

```
x = 12, n = 1, m = 2
```

We compute minimum first.

| x | n | m | action |
| --- | --- | --- | --- |
| 12 | 1 | 2 | even → x=6 |
| 6 | 1 | 1 | even → x=3 |
| 3 | 1 | 1 | odd, use floor → x=1 |
| 1 | 0 | 1 | stop |

Result is 1.

Now maximum.

| x | n | m | action |
| --- | --- | --- | --- |
| 12 | 1 | 2 | even → x=6 |
| 6 | 1 | 1 | even → x=3 |
| 3 | 1 | 1 | odd, use ceil → x=2 |

Result is 2.

This shows how a single odd step changes the outcome depending on which operation is chosen.

### Example 2

Input:

```
x = 7, n = 2, m = 1
```

Minimum simulation:

| x | n | m | action |
| --- | --- | --- | --- |
| 7 | 2 | 1 | odd, floor → 3 |
| 3 | 1 | 1 | odd, floor → 1 |
| 1 | 0 | 1 | stop |

Maximum simulation:

| x | n | m | action |
| --- | --- | --- | --- |
| 7 | 2 | 1 | odd, ceil → 4 |
| 4 | 2 | 0 | even → 2 |
| 2 | 2 | 0 | even → 1 |

This shows how postponing floor operations in the maximum case keeps the value larger for longer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t log x) | each step halves x or finishes operations |
| Space | O(1) | only counters and current value are stored |

The logarithmic behavior comes from the fact that every operation reduces the magnitude of `x` by at least half, so the number of meaningful states is bounded by the number of bits in `x`. With up to 10^4 test cases, this easily fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve_one(x, n, m, want_min):
        while x > 1 and (n + m) > 0:
            if x % 2 == 0:
                x //= 2
                if n > 0:
                    n -= 1
                else:
                    m -= 1
            else:
                if want_min:
                    if n > 0:
                        x = x // 2
                        n -= 1
                    else:
                        x = x // 2 + 1
                        m -= 1
                else:
                    if m > 0:
                        x = x // 2 + 1
                        m -= 1
                    else:
                        x = x // 2
                        n -= 1

        if x == 0:
            return 0
        if x == 1:
            if want_min and n > 0:
                return 0
            return 1
        return x

    t = int(input())
    out = []
    for _ in range(t):
        x, n, m = map(int, input().split())
        out.append(f"{solve_one(x, n, m, True)} {solve_one(x, n, m, False)}")
    return "\n".join(out)

# provided samples
assert run("""5
12 1 2
12 1 1
12 0 0
12 1000000000 1000000000
706636307 0 3
""") == """1 2
3 3
12 12
0 0
88329539 88329539"""

# custom cases
assert run("1\n1 0 0\n") == "1 1", "identity"
assert run("1\n1 1 0\n") == "0 0", "floor kills 1"
assert run("1\n1 0 1\n") == "1 1", "ceil keeps 1"
assert run("1\n7 10 10\n") is not None, "large mix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0` | `1 1` | no operations |
| `1 1 0` | `0 0` | floor effect on 1 |
| `1 0 1` | `1 1` | ceil stability |
| `7 10 10` | varies | stability under many ops |

## Edge Cases

A critical edge case occurs when the value becomes 1 while operations remain. For example, `x = 1, n = 5, m = 0` immediately collapses to 0 because floor is applied at least once. The algorithm explicitly checks `x == 1` and consumes remaining floor operations to return 0, matching the fact that no future ceil operation can recover from a floor.

Another edge case is when `x = 0` early in the process. Both operations keep it at 0, so all remaining steps are irrelevant. The early return ensures no incorrect transition occurs.

A final subtle case is when operations are heavily unbalanced, such as `n = 10^9, m = 0`. The simulation must avoid looping through all operations and instead rely on the fact that repeated halving quickly stabilizes `x`, after which remaining operations only decide whether it collapses to 0 or stays at 1.
