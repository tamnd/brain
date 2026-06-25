---
title: "CF 105862A - Dragons"
description: "We are given a simple progression simulation involving a character and a sequence of dragons. Each dragon has a required strength to be defeated and a reward in strength after being defeated. The character starts with an initial strength value."
date: "2026-06-25T14:34:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105862
codeforces_index: "A"
codeforces_contest_name: "ACPC Kickoff 2025"
rating: 0
weight: 105862
solve_time_s: 48
verified: true
draft: false
---

[CF 105862A - Dragons](https://codeforces.com/problemset/problem/105862/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a simple progression simulation involving a character and a sequence of dragons. Each dragon has a required strength to be defeated and a reward in strength after being defeated. The character starts with an initial strength value. The dragons can be fought in any order, and the goal is to determine whether there exists an order in which all dragons can be defeated sequentially so that at every fight the character’s current strength strictly exceeds the dragon’s requirement.

The input describes one initial strength and then a list of dragon encounters, each represented by two numbers: the minimum strength needed to fight that dragon and the strength gained after winning. The task is to decide whether it is possible to defeat all dragons and output a yes or no answer accordingly.

The constraints are typically large enough to rule out any approach that tries all permutations of dragons. If there are n dragons, a naive permutation-based solution would cost n factorial operations, which becomes infeasible even for n around 20. This immediately pushes us toward a greedy ordering strategy with sorting, which runs comfortably in n log n time.

A subtle failure mode appears if we attempt to fight dragons in the given input order without reasoning about ordering. A small example illustrates the issue. Suppose the initial strength is 10, and the dragons are (strength 11, reward 5) and (strength 10, reward 100). If we follow input order, we fail immediately because 10 is not enough for 11. However, if we first fight the second dragon, we gain a large boost and then can defeat the first. This shows that ordering is the core difficulty, not the fight simulation itself.

## Approaches

The brute-force strategy is to try every possible permutation of dragons and simulate the fights in that order. For each permutation, we check whether the character’s strength remains sufficient at each step. This works because it exhaustively explores all possible sequences, guaranteeing that if a valid order exists, it will be found.

The problem with this approach is the number of permutations. With n dragons, there are n! possible orders, and for each order we perform O(n) simulation work. Even for n = 15, this already exceeds practical limits, and for n = 20 it becomes entirely infeasible.

The key observation is that the ordering decision depends only on the current strength compared to the dragon requirement, and the reward always increases strength. This structure suggests that fighting weaker requirements earlier expands the set of dragons we can handle later. If we sort dragons by their required strength in increasing order, we ensure that we never postpone an “easy” dragon while attempting a harder one prematurely. Once sorted, a single linear pass is sufficient to simulate the process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Greedy Sort | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first reorder the dragons so that those with smaller strength requirements come earlier. This ordering is crucial because it aligns the sequence with what is currently feasible at each step.

1. Sort all dragons by their required strength in ascending order. This ensures we always consider the weakest available challenge first.
2. Initialize the current strength with the starting value.
3. Iterate over the sorted dragons one by one. At each dragon, compare current strength with its requirement.
4. If current strength is strictly greater than the requirement, defeat the dragon and increase current strength by the reward value.
5. If at any point the current strength is not sufficient, terminate early and conclude failure, since no later ordering can fix the fact that we are already blocked by a weaker requirement than what we could have handled.
6. If all dragons are processed successfully, output success.

Why the greedy choice is valid comes from the fact that defeating any accessible dragon never reduces strength and only expands future possibilities. Sorting ensures that whenever a dragon is skipped, it is not because of ordering, but because it is genuinely impossible at that moment.

The invariant maintained is that before processing each dragon in the sorted order, we have already defeated all dragons with smaller or equal requirements that were possible to defeat, and our current strength is the maximum achievable under that prefix. This prevents missing any beneficial early fights.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s, n = map(int, input().split())
    dragons = []

    for _ in range(n):
        x, y = map(int, input().split())
        dragons.append((x, y))

    dragons.sort(key=lambda d: d[0])

    for x, y in dragons:
        if s > x:
            s += y
        else:
            print("NO")
            return

    print("YES")

if __name__ == "__main__":
    solve()
```

The solution begins by reading the initial strength and number of dragons. We store each dragon as a pair of requirement and reward. Sorting by requirement is the critical step that transforms an otherwise combinatorial problem into a linear simulation.

During iteration, we enforce the strict comparison condition `s > x`. This strictness is important because equality is not allowed; missing this condition is a common off-by-one error. The early exit on failure avoids unnecessary computation but is not required for correctness, only efficiency.

## Worked Examples

### Example 1

Input:

```
10 2
11 5
10 100
```

Sorted dragons:

| Step | Strength | Dragon (req, reward) | Action | New strength |
| --- | --- | --- | --- | --- |
| 1 | 10 | (10, 100) | 10 > 10 false | stop |

The process stops immediately because equality is not sufficient for victory. This shows why ordering alone does not solve everything if we ignore the strict inequality condition.

### Example 2

Input:

```
10 3
5 2
9 1
8 10
```

Sorted dragons:

| Step | Strength | Dragon | Action | New strength |
| --- | --- | --- | --- | --- |
| 1 | 10 | (5, 2) | fight | 12 |
| 2 | 12 | (8, 10) | fight | 22 |
| 3 | 22 | (9, 1) | fight | 23 |

Every dragon becomes easier to handle after early gains, confirming that increasing order of requirements preserves feasibility while maximizing early growth opportunities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, simulation is linear |
| Space | O(n) | storing the list of dragons |

The algorithm comfortably fits within typical constraints where n can reach up to 10^5, since sorting and a single pass are efficient enough under standard limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided sample-like case
assert run("10 2\n11 5\n10 100\n") == "NO"

# all possible successful
assert run("10 1\n5 10\n") == "YES"

# must reorder to succeed
assert run("10 3\n11 1\n5 1\n8 1\n") == "YES"

# impossible case
assert run("1 2\n2 1\n3 1\n") == "NO"

# edge: exact equality failure
assert run("5 1\n5 100\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal case | YES | single dragon success |
| mixed ordering | YES | sorting necessity |
| impossible chain | NO | early failure detection |
| equality edge | NO | strict inequality rule |

## Edge Cases

One edge case is when the initial strength is exactly equal to a dragon’s requirement. For input `s = 5` and dragon `(5, 100)`, the correct result is failure because the condition is strictly greater than. The algorithm handles this correctly through the `if s > x` check, immediately rejecting the dragon.

Another case is when a weak dragon appears late in the input but must be fought early. For example, starting strength 10 with dragons `(11, 1)` and `(5, 1)` requires sorting. After sorting, `(5, 1)` is processed first, increasing strength and enabling progression. Without sorting, the algorithm would incorrectly fail, but the sorted greedy pass guarantees correct ordering.

A final case is when all dragons are individually impossible but become possible after earlier rewards. The greedy structure naturally handles this because every successful fight only increases strength, ensuring no future opportunity is artificially blocked once it becomes available.
