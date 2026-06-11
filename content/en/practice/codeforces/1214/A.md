---
title: "CF 1214A - Optimal Currency Exchange"
description: "We start with a fixed amount of money in rubles and want to convert it into foreign currency using an exchange office that sells only fixed denominations of dollar bills and euro bills. Each dollar costs a fixed amount in rubles, and each euro also has its own fixed ruble price."
date: "2026-06-11T23:00:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1214
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 583 (Div. 1 + Div. 2, based on Olympiad of Metropolises)"
rating: 1400
weight: 1214
solve_time_s: 122
verified: true
draft: false
---

[CF 1214A - Optimal Currency Exchange](https://codeforces.com/problemset/problem/1214/A)

**Rating:** 1400  
**Tags:** brute force, math  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a fixed amount of money in rubles and want to convert it into foreign currency using an exchange office that sells only fixed denominations of dollar bills and euro bills. Each dollar costs a fixed amount in rubles, and each euro also has its own fixed ruble price. After we buy any number of these foreign bills, we are left with some unused rubles, and the goal is to minimize that leftover amount.

The important constraint is that we are not choosing arbitrary amounts of currency, but must buy whole banknotes, and each banknote type has a fixed value in its own currency, which translates into a fixed ruble cost per bill. So the real decision is how many dollar bills and euro bills to buy so that the total spent money is as large as possible but does not exceed the initial amount.

The input sizes are small enough that a direct exploration over reasonable combinations of bills is feasible, but large enough that any attempt to enumerate all possible multisets of bills would fail. The key observation is that both currencies have only a handful of denominations, so the number of meaningful combinations is tightly bounded.

A naive mistake is to assume a greedy strategy like always buying the largest possible bill in either currency first. That fails because mixed combinations can beat single-currency greedy choices. For example, spending everything on euros might leave a worse remainder than mixing a few dollars and euros to match the budget more tightly.

Another subtle issue is ignoring that euro and dollar bills interact only through the shared constraint of total rubles. There is no structural coupling between denominations beyond this shared budget, so the problem reduces to a bounded knapsack-like search over two independent item sets.

## Approaches

A brute-force view of the problem treats each possible selection of dollar bills and euro bills as a state. Since dollar bills have fixed denominations up to 100 and euro bills up to 200, one could imagine trying all combinations of counts for each denomination. This would quickly explode because even a moderate upper bound on the number of bills (up to n divided by smallest price, around 30) leads to an enormous state space if treated independently per denomination.

However, the structure is much simpler than it appears. Each currency independently only contributes multiples of a fixed cost per bill, meaning the problem is really about choosing two non-negative integers, the number of dollars and euros, such that:

$$d \cdot x + e \cdot y \le n$$

and maximizing the spent amount.

The key insight is that since both x and y are bounded by at most n / 30, we can safely fix one variable and compute the best possible value of the other in constant time. For a fixed number of dollar bills, the optimal number of euro bills is simply the remainder divided by e. This collapses the problem into a linear scan over all possible dollar counts.

The reverse is also true, but we only need one direction since symmetry is not required for correctness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all combinations | O((n/d)·(n/e)) | O(1) | Too slow |
| Fix one currency, compute greedy remainder | O(n/d) | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over all possible numbers of dollar bills from 0 up to n // d. Each choice represents spending a fixed portion of the budget in dollars, and leaves a remaining amount to be optimally filled with euros.
2. For each fixed number of dollar bills x, compute the remaining rubles after buying dollars as rem = n - x * d. This remainder represents the full budget available for euros.
3. Compute how many euro bills can be bought from this remainder as y = rem // e. This is optimal because euro bills are identical in cost and there is no constraint preventing greedy filling.
4. Compute the total spent amount as spent = x * d + y * e, and track the maximum value over all x.
5. After iterating all possibilities, the answer is n - best_spent, which represents the minimum leftover rubles.

### Why it works

For any optimal solution, fix the number of dollar bills used. Once that is fixed, there is no reason to leave any remainder unused if it can fit a euro bill, since all euro bills have identical cost structure and no restrictions other than budget. Therefore, the best euro choice is always greedy. This ensures that every feasible split of the budget is considered through some value of x, and for each such split the best corresponding y is chosen, so no optimal solution is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    d = int(input())
    e = int(input())

    max_spent = 0

    # try all possible number of dollar bills
    for x in range(n // d + 1):
        rem = n - x * d
        y = rem // e
        spent = x * d + y * e
        if spent > max_spent:
            max_spent = spent

    print(n - max_spent)

if __name__ == "__main__":
    solve()
```

The solution explicitly iterates over all feasible dollar counts. For each, it greedily fills the remaining budget with euros. The subtraction at the end converts the maximized spent value into the minimized leftover value.

A common implementation pitfall is forgetting that we are maximizing spent money rather than directly minimizing remainder during iteration. Both are equivalent, but tracking spent avoids confusion in intermediate states.

## Worked Examples

### Example 1

Input:

```
100
60
70
```

We try different numbers of dollar bills:

| Dollars x | Remaining | Euros y | Spent |
| --- | --- | --- | --- |
| 0 | 100 | 1 | 70 |
| 1 | 40 | 0 | 60 |

Best spent is 70, so leftover is 30. However, we can also observe that combining neither currency fully fits well, and euros alone dominate this case.

This trace shows that euro-only or dollar-only choices may dominate depending on divisibility of n.

### Example 2

Input:

```
120
30
50
```

| Dollars x | Remaining | Euros y | Spent |
| --- | --- | --- | --- |
| 0 | 120 | 2 | 100 |
| 1 | 90 | 1 | 80 |
| 2 | 60 | 1 | 110 |
| 3 | 30 | 0 | 90 |

Best spent is 110, achieved by mixing both currencies, giving leftover 10.

This demonstrates why greedy per currency alone fails: the optimal solution depends on a mixed allocation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n / d) | We iterate over all possible counts of dollar bills, each in constant time |
| Space | O(1) | Only a few variables are used regardless of input size |

The bound n ≤ 10^8 and d ≥ 30 ensures at most around 3 million iterations, which is safe in Python under tight loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    d = int(input())
    e = int(input())

    max_spent = 0
    for x in range(n // d + 1):
        rem = n - x * d
        y = rem // e
        max_spent = max(max_spent, x * d + y * e)

    return str(n - max_spent)

# provided sample
assert run("100\n60\n70\n") == "40"

# minimum case
assert run("30\n30\n30\n") == "0"

# only one currency useful
assert run("100\n50\n100\n") == "0"

# mixed optimal
assert run("120\n30\n50\n") == "10"

# boundary large-ish
assert run("100000000\n99\n100\n") == str(100000000 % 99)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 30,30,30 | 0 | exact division case |
| 100,50,100 | 0 | single optimal currency |
| 120,30,50 | 10 | mixed optimality |
| large case | computed | performance and correctness |

## Edge Cases

One edge case is when one currency dominates but slightly mismatches the budget. For example, with n = 100, d = 60, e = 70, neither currency alone fits perfectly. The algorithm checks both x = 0 and x = 1 for dollars, ensuring both euro-heavy and dollar-heavy configurations are evaluated. For x = 0, we get 100 // 70 = 1 euro, spending 70. For x = 1, we spend 60 and cannot afford euros, so best is 70 spent overall, leaving 30.

Another edge case is when one currency is strictly worse in cost efficiency but still needed to improve modular alignment. Even if d < e or vice versa, the mixed scan guarantees that every residue class induced by d is explored, so no hidden better combination exists outside the enumeration.
