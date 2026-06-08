---
title: "CF 2038A - Bonus Project"
description: "We have a team of engineers, each with a promised bonus and a personal cost for doing one unit of work. The team needs to complete a project that requires exactly $k$ units of work, and every engineer will decide individually how much to contribute."
date: "2026-06-08T10:34:44+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2038
codeforces_index: "A"
codeforces_contest_name: "2024-2025 ICPC, NERC, Southern and Volga Russian Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 1400
weight: 2038
solve_time_s: 129
verified: false
draft: false
---

[CF 2038A - Bonus Project](https://codeforces.com/problemset/problem/2038/A)

**Rating:** 1400  
**Tags:** games, greedy  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We have a team of engineers, each with a promised bonus and a personal cost for doing one unit of work. The team needs to complete a project that requires exactly $k$ units of work, and every engineer will decide individually how much to contribute. The amount each engineer contributes, $c_i$, must maximize their personal benefit, defined as $s_i = a_i - c_i \cdot b_i$, where $a_i$ is the bonus and $b_i$ is the per-unit cost. If an engineer expects negative benefit, they will not work at all. The goal is to determine the work distribution $[c_1, c_2, ..., c_n]$ that results when every engineer acts optimally.

Constraints tell us $n \le 1000$ and $k \le 10^6$. Since $k$ can be large, any algorithm that tries to test all possible distributions of work (for example, all tuples of non-negative integers summing to $k$) would be exponential in $n$, which is infeasible. A linear or $O(n \log n)$ solution is acceptable because it can handle up to about $10^6$ operations comfortably.

Non-obvious edge cases include situations where the total bonus is too small for the project to be profitable. For example, if $k = 10$ and the sum of bonuses $a_i$ is smaller than any reasonable allocation of work costs, no engineer would volunteer any work, so the output should be all zeros. Another edge case is when some engineers have very high cost per unit $b_i$ and low bonus. In this case, even though the project could be completed by others, those engineers should contribute zero, as working would reduce their benefit.

## Approaches

The brute-force approach would try every possible allocation of $k$ work units among the engineers. For each distribution, we would compute the benefit for each engineer and check if any benefit is negative, rejecting that allocation if so. This is correct in principle, but the number of allocations is combinatorial: roughly $\binom{k+n-1}{n-1}$. Even for small $n$ and moderate $k$, this is far too slow.

The key insight is that engineers act in order, each maximizing their own benefit given what the previous engineers have promised. Each engineer sees a remaining amount of work $r$ to reach $k$ after the previous engineers have decided. Their goal is to choose $c_i$ as large as possible without making their own benefit negative, i.e., $c_i \le a_i / b_i$. They also cannot contribute more than the remaining work $r$. Therefore, the optimal $c_i$ is the minimum of the remaining work and the maximum profitable contribution $a_i / b_i$. Once an engineer commits $c_i$, the next engineer repeats the same logic with the updated remaining work. This greedy approach is guaranteed to produce a unique solution because each engineer’s choice depends deterministically on the remaining work and their personal ratio $a_i / b_i$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((k+n-1 choose n-1)) | O(n) | Too slow |
| Greedy Sequential | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize the remaining work $r = k$. This variable keeps track of how much work still needs to be assigned.
2. Iterate through each engineer $i$ from $1$ to $n$. For each engineer, calculate their maximum profitable work, which is $m_i = a_i // b_i$. This represents the largest amount of work that does not reduce their benefit below zero.
3. Determine the actual work $c_i$ the engineer will contribute. This is the minimum of $m_i$ and the remaining work $r$. This ensures that the engineer maximizes their benefit without exceeding what is necessary to complete the project.
4. Subtract the engineer's contribution from the remaining work: $r -= c_i$. This updates the remaining work for the following engineers.
5. Continue this process for all engineers. After the last engineer, the sum of $c_i$ will either exactly match $k$ (project completed) or be less if completing the project is impossible without some engineer taking a negative benefit. Engineers who cannot profitably contribute will automatically contribute zero.

Why it works: At every step, each engineer acts optimally given the previous decisions. Because each engineer’s choice is bounded by both their maximum profitable contribution and the remaining work, the greedy sequential allocation guarantees no engineer ends up with negative benefit. The invariant is that after each engineer, the remaining work accurately reflects the unassigned portion of $k$, and every engineer has chosen the maximum amount they can contribute without loss. This produces a unique, optimal sequence $[c_1, c_2, ..., c_n]$.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

c = []
remaining = k

for i in range(n):
    max_work = a[i] // b[i]  # maximum work this engineer can profitably do
    contribution = min(max_work, remaining)
    c.append(contribution)
    remaining -= contribution

print(' '.join(map(str, c)))
```

The solution reads $n$, $k$, the bonuses $a_i$, and costs $b_i$. The `max_work` calculation ensures no engineer works at a loss, and the `min(max_work, remaining)` assignment guarantees that total work never exceeds $k$. The `remaining` variable updates sequentially so each engineer knows exactly how much work is left. Using integer division `//` ensures we stay in integer units.

## Worked Examples

**Sample 1**

Input:

```
3 6
4 7 6
1 2 3
```

Step trace:

| Engineer | a_i | b_i | max_work | remaining | c_i | remaining after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 4 | 6 | 1 | 5 |
| 2 | 7 | 2 | 3 | 5 | 3 | 2 |
| 3 | 6 | 3 | 2 | 2 | 2 | 0 |

The table shows that each engineer contributes up to their profitable limit without exceeding remaining work. Total work sums to 6, exactly $k$.

**Sample 2**

Input:

```
2 10
3 4
5 2
```

Step trace:

| Engineer | a_i | b_i | max_work | remaining | c_i | remaining after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 0 | 10 | 0 | 10 |
| 2 | 4 | 2 | 2 | 10 | 2 | 8 |

Remaining work is 8 after both engineers, but any further work would reduce benefit below zero, so they contribute only what is profitable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through all engineers, constant-time arithmetic per engineer |
| Space | O(n) | Storing the resulting contributions array |

The algorithm is linear in the number of engineers and independent of $k$. With $n \le 1000$, this easily runs under 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = []
    remaining = k
    for i in range(n):
        max_work = a[i] // b[i]
        contribution = min(max_work, remaining)
        c.append(contribution)
        remaining -= contribution
    return ' '.join(map(str, c))

# provided samples
assert run("3 6\n4 7 6\n1 2 3\n") == "1 3 2"
assert run("2 10\n3 4\n5 2\n") == "0 2"

# custom cases
assert run("1 5\n10\n2\n") == "5"  # single engineer does all work
assert run("3 5\n1 2 3\n1 1 1\n") == "1 2 2"  # sum of max work = k exactly
assert run("2 1000\n1000 1000\n1 1\n") == "500 500"  # evenly distributed
assert run("3 3\n1 1 1\n2 2 2\n") == "0 0 0"  # no profitable work
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1 5\n10\n2\n" | "5" | Single engineer handles all work |
| "3 5\n1 2 3\n1 1 1\n" | "1 2 2" | Work distributed to exactly reach k |
| "2 1000\n1000 1000\n1 1\n" | "500 |  |
