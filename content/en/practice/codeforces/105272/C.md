---
title: "CF 105272C - Cosmic candidates"
description: "We are given a group of $n$ people, where $n$ is divisible by 3, and these people are already partitioned into teams of exactly 3 members each. Each team will only agree to participate in a competition if at least two of its three members are convinced to go."
date: "2026-06-23T14:02:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105272
codeforces_index: "C"
codeforces_contest_name: "IX MaratonUSP Freshman Contest"
rating: 0
weight: 105272
solve_time_s: 42
verified: true
draft: false
---

[CF 105272C - Cosmic candidates](https://codeforces.com/problemset/problem/105272/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of $n$ people, where $n$ is divisible by 3, and these people are already partitioned into teams of exactly 3 members each. Each team will only agree to participate in a competition if at least two of its three members are convinced to go.

The coach can directly convince individual people. Once at least two members of a team agree, the third member automatically agrees as well. The goal is to minimize how many people must be directly convinced so that every team ends up participating.

Reframed, each group of three behaves like a threshold gadget: convincing one person is not enough to activate the team, but convincing any two forces the third to follow. The task is to pick a minimum number of initial “seeds” so that every triple has at least two seeds chosen or becomes forced through propagation.

The constraint $n \le 100$ means brute-force over subsets is not viable. Even $2^{100}$ is completely infeasible. Any solution must reason directly about the structure of each triple rather than exploring combinations.

A subtle pitfall appears when thinking greedily without structure. For example, one might try to pick exactly two people per team, yielding $2n/3$, but it is not obvious whether cross-team effects can reduce this further. Another naive thought is that picking one person per team might somehow cascade, but since teams are independent, no cascade crosses boundaries.

## Approaches

The brute-force perspective is to consider selecting a subset of people and simulating the process: for each team, check whether at least two members are selected, and if not, whether the third becomes convinced through repeated propagation. This quickly becomes complex because propagation across teams does not exist, and within a team the rule collapses to a simple threshold condition. Enumerating subsets gives correctness but costs $O(2^n \cdot n)$, which is far beyond limits.

The key simplification is recognizing that teams are completely independent. No decision in one team affects another. This means we can optimize each group of three in isolation and sum the answers.

Within a single team, we need the smallest number of initially convinced members such that eventually all three agree. If we convince 0 or 1 member, the team never reaches the threshold of two convinced members, so the process cannot complete. If we convince 2 members, the rule immediately activates and the third follows. Therefore the optimal per-team cost is exactly 2.

Since there are $n/3$ teams, the total answer is fixed as $2 \cdot (n/3)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Per-team reasoning | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the number of teams as $n // 3$. This works because the input guarantees divisibility by 3, so no remainder handling is needed.
2. For each team, determine the minimum number of people that must be directly convinced to ensure the team participates. A team activates only when at least two of its members are initially chosen, since the third follows automatically once the threshold is met.
3. Assign a cost of 2 per team, since selecting fewer than two cannot trigger activation, and selecting two is sufficient.
4. Multiply the number of teams by 2 to obtain the final answer.

### Why it works

Each team behaves independently and has a strict activation threshold of 2 out of 3 members. No cross-team interaction exists, so any global strategy decomposes into identical per-team decisions. Within a single triple, any solution must select at least two members; otherwise the activation rule is never satisfied. Selecting exactly two is sufficient because it immediately triggers full acceptance. This establishes that the per-team minimum is fixed and additive across all teams.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    print(2 * (n // 3))

if __name__ == "__main__":
    solve()
```

The solution reads a single integer and computes how many disjoint groups of three exist. Each group contributes exactly two required direct selections, so the computation is a direct multiplication.

The implementation avoids loops entirely because no interaction exists between teams. The only subtlety is ensuring integer division is used.

## Worked Examples

### Example 1

Input:

```
3
```

We have one team of three members.

| Step | Teams remaining | Cost so far | Action |
| --- | --- | --- | --- |
| 1 | 1 | 0 | Start |
| 2 | 1 | 2 | Pick any two members in the team |
| 3 | 0 | 2 | Team becomes fully active |

This confirms that a single triple always costs 2.

### Example 2

Input:

```
6
```

There are two independent teams.

| Step | Teams remaining | Cost so far | Action |
| --- | --- | --- | --- |
| 1 | 2 | 0 | Start |
| 2 | 2 | 2 | Activate first team with two picks |
| 3 | 1 | 4 | Activate second team with two picks |
| 4 | 0 | 4 | Done |

This shows additivity across independent groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations |
| Space | $O(1)$ | No auxiliary data structures |

The computation does not depend on the magnitude of $n$, only on dividing it by 3 and multiplying by 2. With $n \le 100$, this is trivially within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n = int(input().strip())
    return str(2 * (n // 3))

# provided samples (conceptual since original samples are empty in prompt)
assert run("3\n") == "2", "sample 1"
assert run("6\n") == "4", "sample 2"

# custom cases
assert run("0\n") == "0", "minimum case"
assert run("9\n") == "6", "three teams"
assert run("99\n") == "66", "near upper bound"
assert run("3\n") == "2", "single team sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | empty structure behavior |
| 9 | 6 | multiple independent teams |
| 99 | 66 | larger input scaling linearly |
| 3 | 2 | base case correctness |

## Edge Cases

The smallest meaningful case is $n = 3$, where exactly one team exists. The algorithm assigns cost 2, which matches the requirement that at least two members must be convinced to activate the only team.

At $n = 0$, although not explicitly stated in constraints, the formula still produces 0, consistent with having no teams.

At larger values such as $n = 99$, the algorithm scales linearly by counting 33 teams and assigning 66 convinced members. Each team remains independent, so no interaction effects can reduce this number further, and the computed value remains optimal.
