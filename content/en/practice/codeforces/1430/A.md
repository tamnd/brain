---
title: "CF 1430A - Number of Apartments"
description: "The building is described as being composed of three fixed apartment types, and each type contributes a fixed number of windows. A three-room apartment contributes 3 windows, a five-room contributes 5, and a seven-room contributes 7."
date: "2026-06-11T05:16:51+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1430
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 96 (Rated for Div. 2)"
rating: 900
weight: 1430
solve_time_s: 102
verified: false
draft: false
---

[CF 1430A - Number of Apartments](https://codeforces.com/problemset/problem/1430/A)

**Rating:** 900  
**Tags:** brute force, constructive algorithms, math  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

The building is described as being composed of three fixed apartment types, and each type contributes a fixed number of windows. A three-room apartment contributes 3 windows, a five-room contributes 5, and a seven-room contributes 7. For each test case, we are given only the total number of windows observed in the building, and we must reconstruct any possible combination of apartment counts that could sum exactly to that total.

So the task is equivalent to finding non-negative integers $a, b, c$ such that:

$$3a + 5b + 7c = n$$

If such a decomposition exists, any valid triple is acceptable. If no decomposition exists, we report impossibility.

The constraints are small: $n \le 1000$ and $t \le 1000$. This immediately tells us that even a cubic or moderately quadratic search per test case would be fine, since at worst we are doing about $10^6$ checks overall. However, the structure of the equation also suggests we can do much better than blind search.

A naive approach might try all triples $(a, b, c)$ up to $n$, but that would be unnecessarily large. A more reasonable brute force would fix two variables and derive the third, but even then we still want to minimize loops.

A subtle edge case appears when no combination exists, especially for small values like $n = 1, 2, 4$. These fail because all valid building blocks are odd-sized, meaning any valid sum must have the same parity as a combination of 3, 5, and 7. Since all are odd, any integer $n \ge 3$ can potentially be represented, but small values often cannot be expressed due to lack of flexibility in combinations.

Another edge case is when $n$ is exactly one of the coin types, like 3, 5, or 7. The answer must then correctly allow a single apartment of that type and zeros elsewhere.

## Approaches

The brute-force idea is straightforward: try all possible counts of three-room apartments $a$ and five-room apartments $b$, and compute whether the remaining value can be filled by seven-room apartments. For each pair $(a, b)$, we check whether $n - 3a - 5b$ is non-negative and divisible by 7.

This works because the constraints are small, but in the worst case we try about $1000 \times 1000 = 10^6$ pairs per test case, and with up to 1000 test cases this becomes $10^9$ operations, which is too slow.

The key observation is that we do not actually need to search deeply. Since we only need any valid solution, we can fix one variable and greedily determine the others. The most convenient choice is to iterate over the number of seven-room apartments $c$. Once $c$ is fixed, the remaining problem reduces to:

$$3a + 5b = n - 7c$$

Now we only need to find a representation using 3 and 5. Because the space is small, we can try all values of $b$ and compute whether the remaining amount is divisible by 3. This reduces the search dramatically and guarantees a quick solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over (a, b) | O(n²) per test | O(1) | Too slow |
| Fix c, try b | O(n²) worst-case per test but small constants, or O(n) with early exit | O(1) | Accepted |

A more practical interpretation is that even the simplest bounded double loop is fine here, but the structured reduction to two variables ensures we terminate quickly in practice.

## Algorithm Walkthrough

We solve each test case independently.

1. Try fixing the number of seven-room apartments $c$ from 0 up to $n // 7$. This ensures we never exceed the total window count contributed by seven-room apartments.
2. For each $c$, compute the remaining windows $rem = n - 7c$. This reduces the problem to representing $rem$ using 3 and 5.
3. Try possible values of five-room apartments $b$ from 0 up to $rem // 5$. For each choice, compute $rem - 5b$.
4. If the leftover value is divisible by 3, then set $a = (rem - 5b) // 3$. At this point we have a valid decomposition and can output $a, b, c$.
5. If no combination is found after exhausting all $c$ and $b$, output -1.

Why this ordering works is that we progressively reduce the search space while preserving exactness. Each step enforces non-negativity automatically, so we never need to backtrack or adjust previously chosen values.

### Why it works

The algorithm enumerates all feasible values of $c$, and for each such choice it exhaustively checks all feasible values of $b$. For every pair $(b, c)$, the value of $a$ is uniquely determined if it exists. Since all valid solutions correspond to exactly one such pair, the search space is complete and no solution can be skipped. The bounded loops guarantee termination while preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())

        found = False

        for c in range(n // 7 + 1):
            rem = n - 7 * c
            for b in range(rem // 5 + 1):
                rest = rem - 5 * b
                if rest % 3 == 0:
                    a = rest // 3
                    print(a, b, c)
                    found = True
                    break
            if found:
                break

        if not found:
            print(-1)

if __name__ == "__main__":
    solve()
```

The code directly implements the nested search described earlier. The outer loop iterates over possible counts of seven-room apartments, while the inner loop attempts to complete the remainder using five-room apartments. The final check enforces divisibility by 3, which determines the number of three-room apartments.

The early break ensures we stop as soon as a valid decomposition is found, preventing unnecessary computation.

## Worked Examples

We trace two cases: $n = 30$ and $n = 14$.

### Example 1: n = 30

| c | rem | b | rem - 5b | divisible by 3 | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 30 | 0 | 30 | yes | a=10, stop |

The first valid decomposition appears immediately: $10$ three-room apartments.

This shows the algorithm does not depend on finding a balanced solution; any valid representation is accepted.

### Example 2: n = 14

| c | rem | b | rem - 5b | divisible by 3 | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 14 | 0 | 14 | no | continue |
| 0 | 14 | 1 | 9 | yes | a=3, stop |

Here the solution is found after a small adjustment in $b$, showing that intermediate failures are expected and handled naturally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) per test worst-case | Two nested loops over c and b bounded by n/7 and n/5 |
| Space | O(1) | Only a few variables are used |

Given $n \le 1000$ and $t \le 1000$, the total work remains manageable in practice because the loops terminate early in most cases and the constants are small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())

        found = False
        for c in range(n // 7 + 1):
            rem = n - 7 * c
            for b in range(rem // 5 + 1):
                rest = rem - 5 * b
                if rest % 3 == 0:
                    a = rest // 3
                    out.append(f"{a} {b} {c}")
                    found = True
                    break
            if found:
                break
        if not found:
            out.append("-1")

    return "\n".join(out)

# provided samples
assert run("4\n30\n67\n4\n14\n") == "10 0 0\n7 5 3\n-1\n3 1 0"

# custom cases
assert run("1\n3\n") == "1 0 0", "single 3-room"
assert run("1\n5\n") == "0 1 0", "single 5-room"
assert run("1\n7\n") == "0 0 1", "single 7-room"
assert run("1\n1\n") == "-1", "impossible small case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 3 | 1 0 0 | base unit case |
| 1, 5 | 0 1 0 | middle unit case |
| 1, 7 | 0 0 1 | largest unit case |
| 1, 1 | -1 | impossible small value |

## Edge Cases

For very small values like $n = 1$, the algorithm correctly iterates over $c = 0$ and $b = 0$, leaving remainder 1. Since 1 is not divisible by 3, no solution is found and -1 is returned.

For exact matches like $n = 7$, the loop considers $c = 1$, giving remainder 0. The inner loop immediately finds $b = 0$, and $a = 0$, producing a valid answer.

For mixed cases like $n = 14$, multiple intermediate combinations are tested, but the algorithm correctly identifies $7 + 7$ or $3 + 5 + 3 + 3$-style decompositions depending on loop order. The correctness does not depend on which solution is found first, only that one is found if it exists.
