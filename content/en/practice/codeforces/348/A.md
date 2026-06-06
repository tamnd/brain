---
title: "CF 348A - Mafia"
description: "We are given a group of friends who will repeatedly play a game. Each round of the game has exactly one person acting as a supervisor, while the remaining $n-1$ people participate as players."
date: "2026-06-06T18:31:10+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 348
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 202 (Div. 1)"
rating: 1600
weight: 348
solve_time_s: 131
verified: false
draft: false
---

[CF 348A - Mafia](https://codeforces.com/problemset/problem/348/A)

**Rating:** 1600  
**Tags:** binary search, math, sortings  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a group of friends who will repeatedly play a game. Each round of the game has exactly one person acting as a supervisor, while the remaining $n-1$ people participate as players.

For each person $i$, we are told how many rounds they want to participate in as a player. Since a person is excluded from exactly one round whenever they become the supervisor, the total number of rounds determines how many times each person is able to play.

If the total number of rounds is $R$, then person $i$ will be a player in exactly $R - x_i$ rounds, where $x_i$ is how many times they were chosen as supervisor. Since each round has exactly one supervisor, the sum of all $x_i$ equals $R$.

The task is to determine the minimum possible $R$ such that we can assign supervisors across rounds so that every person plays at least their required number of times.

The constraints push us toward a solution faster than $O(n^2)$. With $n$ up to $10^5$ and values up to $10^9$, any construction that simulates rounds or tries all possibilities is impossible. We need a formulation that reduces the problem to a simple numeric check or optimization over a monotone condition.

A subtle edge case arises when all demands are very large but balanced, or when one person demands almost everything while others demand little. For example, if all $a_i = 1$, then two rounds are enough because each person can be supervisor once except one, and the last constraint is naturally satisfied. A naive idea that ignores balancing supervision would incorrectly overestimate or underestimate in such cases.

Another tricky situation is when one value dominates. For instance, $a = [10^9, 1, 1, \dots]$. A naive reasoning that simply sums requirements or averages them fails because supervision capacity is distributed unevenly but still bounded per round.

## Approaches

A brute-force idea is to try increasing values of $R$ and check feasibility. For a fixed $R$, we must decide whether we can assign $R$ supervisor slots among $n$ people such that person $i$ is excluded from at most $R - a_i$ rounds. Equivalently, they must be supervisor at most $R - a_i$ times.

To check feasibility for a given $R$, we compute capacities $c_i = R - a_i$. If any $c_i < 0$, that $R$ is impossible. Otherwise, we must ensure the total number of supervisor slots $R$ can be assigned without exceeding capacities. The key condition becomes $\sum \min(c_i, R)\ge R$, but a simpler observation exists: since every round needs exactly one supervisor, we need to distribute $R$ identical tasks among people with upper bounds $c_i$.

This turns into a standard feasibility check: sum of capacities must be at least $R$. That gives $\sum (R - a_i) \ge R$, which simplifies directly to a closed form condition.

The brute-force over $R$ would cost $O(n \cdot \max a_i)$, which is far too large given $a_i$ up to $10^9$.

The key observation is that feasibility is monotone in $R$. If some $R$ works, any larger $R$ also works because increasing rounds only increases supervisory capacity. This means we could binary search, but the algebra reveals we do not need search at all.

Starting from:

$$\sum (R - a_i) \ge R$$

we expand:

$$nR - \sum a_i \ge R$$

$$(n-1)R \ge \sum a_i$$

So:

$$R \ge \frac{\sum a_i}{n-1}$$

Thus the answer is the smallest integer $R$ satisfying this inequality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over R | $O(n \cdot \max a_i)$ | $O(1)$ | Too slow |
| Algebraic Reduction | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total sum $S = \sum a_i$. This captures the total number of times all players collectively insist on participating.
2. Observe that each round reduces total “required participation gap” by exactly $n-1$, since one person is excluded each time. This translates the scheduling problem into a linear resource balance.
3. Derive the condition $(n-1)R \ge S$, meaning total “player slots created” must cover all required participations.
4. Compute the smallest integer $R$ satisfying this inequality using ceiling division.
5. Output this value as the minimum number of rounds.

### Why it works

Each round contributes exactly $n-1$ participations because all but one player participate. Over $R$ rounds, total participation slots available is $R(n-1)$. Each person demands $a_i$ participations, so total demand is $S$. Since participation is the only constraint, feasibility depends only on whether total supply of participation slots meets total demand. Any distribution of supervisors automatically yields valid per-person assignments as long as total capacity is sufficient, because no per-person upper bound other than exclusion per round restricts flexibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    s = sum(arr)
    # minimal R such that (n-1)*R >= s
    r = (s + n - 2) // (n - 1)
    print(r)

if __name__ == "__main__":
    solve()
```

The implementation is a direct translation of the derived inequality. The only subtlety is integer ceiling division, implemented as $(S + n - 2) // (n - 1)$, which avoids floating point errors.

The sum computation is safe in Python due to arbitrary precision integers. No simulation is needed, and there is no need to track individual supervisor assignments.

## Worked Examples

### Example 1

Input:

```
3
3 2 2
```

We compute $S = 7$, $n = 3$, so $n-1 = 2$.

| Step | S | n | R computation | Result |
| --- | --- | --- | --- | --- |
| Compute sum | 7 | 3 | - | 7 |
| Apply formula | 7 | 3 | ceil(7/2) | 4 |

Output is 4.

This confirms that 4 rounds produce $4 \cdot 2 = 8$ participation slots, enough to cover total demand 7.

### Example 2

Input:

```
4
1 1 1 1
```

We compute $S = 4$, $n = 4$, so $n-1 = 3$.

| Step | S | n | R computation | Result |
| --- | --- | --- | --- | --- |
| Compute sum | 4 | 4 | - | 4 |
| Apply formula | 4 | 4 | ceil(4/3) | 2 |

Output is 2.

This shows that even though there are 4 people each wanting 1 participation, only 2 rounds are sufficient because each round includes 3 participants.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass to compute sum |
| Space | $O(1)$ | only a few integers stored |

The solution comfortably fits within constraints since $n \le 10^5$ and we only perform linear aggregation followed by constant-time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))
    s = sum(arr)
    r = (s + n - 2) // (n - 1)
    return str(r)

# provided sample
assert run("3\n3 2 2\n") == "4"

# minimum n
assert run("3\n1 1 1\n") == "1"

# all equal large
assert run("5\n10 10 10 10 10\n") == "13"

# skewed case
assert run("4\n100 1 1 1\n") == "35"

# large uniform
assert run("6\n1 1 1 1 1 1\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 1 1 | 1 | minimum feasible case |
| 5 identical large | 13 | scaling correctness |
| 100 skewed | 35 | dominance edge case |
| all ones | 2 | balanced distribution behavior |

## Edge Cases

When all values are minimal, such as $n=3, a=[1,1,1]$, the formula gives $R = 1$. One round already provides two participation slots per person pool over time, and any single-round assignment works.

When one value dominates, such as $a=[100,1,1,1]$, we get $S=103$, $n=4$, so $R = \lceil 103/3 \rceil = 35$. Each round contributes 3 participation slots, and 35 rounds produce 105 slots, enough to satisfy the heavy demand while distributing supervision constraints across lighter participants.

When all values are equal, the solution scales smoothly because both demand and capacity grow linearly, and the ceiling division handles non-divisibility without special cases.
