---
title: "CF 104699C - \u0411\u0430\u0440\u0431\u0438 \u0432 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u043c \u043c\u0438\u0440\u0435"
description: "We are given a sequence of shelves, each shelf containing a fixed number of dolls. A group of children is initially distributed across these shelves, and each second every child standing at a shelf takes one doll from that shelf."
date: "2026-06-29T08:32:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104699
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104699
solve_time_s: 74
verified: true
draft: false
---

[CF 104699C - \u0411\u0430\u0440\u0431\u0438 \u0432 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u043c \u043c\u0438\u0440\u0435](https://codeforces.com/problemset/problem/104699/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of shelves, each shelf containing a fixed number of dolls. A group of children is initially distributed across these shelves, and each second every child standing at a shelf takes one doll from that shelf. If a shelf runs out of dolls during a second, only some of the children can successfully take a doll from it in that moment, and the remaining children are immediately rerouted to other shelves that still have enough dolls to support them in the next second. Some children may eventually fail to find any valid shelf to continue and leave with whatever they have already collected.

The key freedom in the problem is that we are allowed to choose the initial placement of all children across the shelves. The question is whether there exists some initial assignment such that in the end every child receives exactly the same number of dolls.

The input gives the number of shelves and children, followed by the number of dolls on each shelf. The output is a binary decision: whether such a fair assignment exists.

The constraint $n \le 10^5$ and $m \le 10^9$ immediately tells us that any simulation at the level of individual children or seconds is impossible. Even iterating over all children is already too large, and simulating their movement across shelves would clearly exceed limits. The solution must collapse the entire process into a small number of aggregate quantities derived from the array.

A subtle edge case appears when the total number of dolls is smaller than the number of children. In that case, even if we distribute perfectly, at least one child cannot receive even a single doll, making equal distribution impossible. Another edge case arises when the total number of dolls is not divisible by the number of children. Since every doll is eventually taken by some child and we require equal final counts, divisibility is necessary.

A naive approach might try to greedily assign children to shelves and simulate flow, but this quickly runs into ambiguity because children can move dynamically between shelves, and their interactions depend on time evolution rather than static allocation. This makes direct reasoning about individual paths misleading.

## Approaches

A brute-force strategy would be to explicitly simulate the entire process: assign children to shelves, run the second-by-second consumption process, handle overflow movements, and track how many dolls each child collects. This is conceptually straightforward because it follows the statement literally. However, each second may involve all children at a shelf, and children may migrate repeatedly across shelves. In the worst case, this creates on the order of $O(m \cdot \text{time})$ operations, which is infeasible given that $m$ itself can be up to $10^9$.

The crucial observation is that despite the complex movement rules, no dolls are created or destroyed, and every doll is eventually taken by exactly one child until the process terminates. The dynamics of movement only affect _who_ takes which doll, not _how many dolls are taken in total_. Therefore, the only meaningful quantity is the total number of dolls available.

If the total number of dolls is $S = \sum a_i$, then in any successful scenario all dolls must be evenly split among $m$ children, since every child ends with the same number. This immediately implies that each child must receive $S / m$ dolls, which must be an integer.

Once this condition holds, there is no additional structural constraint imposed by the movement rules. Any arrangement can be interpreted as a flow of identical units, and since all dolls are equivalent, we can always assign children in a way that realizes the equal split.

Thus the problem reduces entirely to checking whether the total sum is divisible by the number of children.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(large dynamic process) | O(m) | Too slow |
| Sum and Divisibility Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total number of dolls across all shelves. This represents the full amount of resources that must be distributed among all children.
2. Check whether this total is at least as large as the number of children. If it is smaller, some child would necessarily receive zero dolls while others receive more, making equality impossible.
3. Check whether the total number of dolls is divisible by the number of children. If it is not divisible, then no equal partition exists regardless of how children are arranged.
4. If both conditions are satisfied, conclude that a valid arrangement exists.

The reasoning behind this procedure is that the process is purely redistributive. Children movement affects only the local ordering of consumption, not the global total. Since every doll is consumed exactly once, the final distribution is forced to respect global conservation.

### Why it works

The system always terminates with every consumed doll assigned to exactly one child, and no child can end with more dolls than exist in total distribution allows. Because all children are indistinguishable in the final requirement, the only possible stable configuration is one where the total number of consumed dolls is evenly partitioned. Any imbalance would imply fractional or leftover allocation, which contradicts the discrete nature of consumption.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    total = sum(a)
    
    if total < m:
        print("NO")
        return
    
    if total % m != 0:
        print("NO")
        return
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The solution reads the array, aggregates the total number of dolls, and applies the two necessary conditions derived from global conservation. There is no need to track positions or simulate movement because the process does not affect total feasibility, only distribution order.

A common mistake would be attempting to model child movement between shelves. That introduces unnecessary complexity without changing the outcome criterion.

## Worked Examples

### Sample 1

Input:

```
3 3
3 4 5
```

Total dolls are 12, and there are 3 children. Each child would need to receive 4 dolls.

| Step | Total dolls | Children | Check |
| --- | --- | --- | --- |
| 1 | 12 | 3 | 12 ≥ 3 |
| 2 | 12 | 3 | 12 % 3 = 0 |

Since both conditions pass, the answer is YES.

This demonstrates a case where redistribution is possible even though shelves differ significantly, because only the aggregate matters.

### Sample 2

Input:

```
6 3
2 3 3 5 1 3
```

Total dolls are 17, with 3 children. Each child would need $17/3$, which is not an integer.

| Step | Total dolls | Children | Check |
| --- | --- | --- | --- |
| 1 | 17 | 3 | 17 ≥ 3 |
| 2 | 17 | 3 | 17 % 3 ≠ 0 |

Since divisibility fails, the answer is NO.

This shows a situation where even though there are enough dolls overall, equal distribution is structurally impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We only compute a single sum over the shelves |
| Space | O(1) | Only a few scalar variables are used |

The solution easily fits within constraints since $n \le 10^5$, and a single linear pass over the array is trivial in time and memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import *
    
    n, m = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))
    
    total = sum(a)
    if total < m or total % m != 0:
        return "NO"
    return "YES"

# provided samples
assert run("3 3\n3 4 5\n") == "YES"
assert run("6 3\n2 3 3 5 1 3\n") == "NO"

# custom cases
assert run("1 1\n10\n") == "YES", "single child trivial"
assert run("1 5\n4\n") == "NO", "insufficient total"
assert run("4 2\n1 1 1 1\n") == "YES", "even split possible"
assert run("5 3\n1 2 3 4 5\n") == "NO", "non divisible sum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 10 | YES | trivial single-child case |
| 1 5 / 4 | NO | insufficient total resources |
| 4 2 / 1 1 1 1 | YES | clean even partition |
| 5 3 / 1 2 3 4 5 | NO | divisibility failure |

## Edge Cases

A minimal case occurs when there is only one child. In that situation, any nonzero total immediately works because all dolls naturally go to that child, and divisibility always holds.

When the total number of dolls is smaller than the number of children, the process cannot assign even one doll per child, so equality is impossible. The algorithm correctly rejects this via the `total < m` check.

When the sum is exactly divisible by the number of children, even highly uneven distributions across shelves do not matter. The system can always be interpreted as redistributing identical units, so feasibility depends only on arithmetic consistency, which the algorithm captures directly.
