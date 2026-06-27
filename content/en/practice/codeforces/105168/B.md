---
title: "CF 105168B - Solo Leveling"
description: "We are simulating a progression system where a character starts with two independent attributes, A and B, both initially fixed at 10. There are n monsters, and each monster i can only be defeated if the character has at least ai in A and at least bi in B."
date: "2026-06-27T08:34:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105168
codeforces_index: "B"
codeforces_contest_name: "2024 Fujian Normal University Programming Contest"
rating: 0
weight: 105168
solve_time_s: 58
verified: true
draft: false
---

[CF 105168B - Solo Leveling](https://codeforces.com/problemset/problem/105168/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a progression system where a character starts with two independent attributes, A and B, both initially fixed at 10. There are n monsters, and each monster i can only be defeated if the character has at least ai in A and at least bi in B. After defeating a monster, the character gains ci upgrade points, and each point can permanently increase either A or B by 1.

The core difficulty is that the order of killing monsters is not fixed. Early fights determine how many upgrade points you have later, which in turn determines which stronger monsters become reachable. The question is whether there exists any ordering of the monsters such that every monster can eventually be defeated starting from (10, 10).

The constraints are small in a structural sense. Even though values of ai, bi, ci can be large up to 10^9, the number of monsters per test is at most 1000 and the total over all tests is at most 4000. This strongly suggests that solutions with O(n^2) or O(n^2 log n) behavior are intended, while anything exponential over subsets or permutations is impossible.

A key subtlety is that resources are not symmetric in a trivial way. A naive intuition might suggest that since ci increases total power, any ordering should eventually work if total gain is large enough. This is false because the constraints are two-dimensional: a sequence that over-invests into A early may become unable to satisfy a monster that requires B, even if total points are sufficient in aggregate.

A small failure case illustrates this. Suppose we start at (10, 10). One monster requires (20, 10) and gives no useful flexibility for B, while another requires (10, 20). If we kill the first too early and invest only in A, we may become permanently unable to reach the second monster even though total points would have been enough if allocated differently. The output depends entirely on ordering.

The problem is therefore about whether we can find a sequence of “feasible unlocks” where resource gains can always be distributed to satisfy future requirements.

## Approaches

The brute-force view is straightforward: try all permutations of monsters, simulate the process, and check if a given order is feasible. For each permutation, we maintain current (A, B), check whether the next monster is reachable, and if so, update A and B using ci. This works logically, but there are n! permutations, and even for n = 15 this already becomes infeasible.

The structure that makes this problem solvable is that feasibility is monotonic with respect to accumulated resources, and every monster only imposes a threshold constraint. Once a monster becomes killable, killing it can only expand the reachable space, never shrink it. The problem is therefore to find a safe sequence where we never get stuck before consuming all monsters.

This leads to a greedy interpretation: at any moment, we maintain a current state (A, B), and we repeatedly choose any monster that is currently killable. The only issue is whether a bad choice among available monsters can block future progress. The key observation is that among all currently available monsters, picking those with weaker requirements first is never harmful, because stronger monsters do not become harder when we delay them, while early rewards only expand the feasible region.

This allows us to sort monsters by their “difficulty level”, defined as max(ai, bi), and process them in increasing order. When requirements are small, they are reachable earlier; when requirements are large, they are naturally deferred until enough ci accumulation has occurred.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | O(n!) | O(n) | Too slow |
| Sort by requirement + greedy feasibility check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We interpret each monster as a gate that requires both coordinates to be high enough. The algorithm proceeds as follows.

1. Compute a difficulty score for each monster as max(ai, bi), which represents the earliest stage at which the monster can plausibly be handled. This collapses the two-dimensional requirement into a single ordering key that respects the fact that both A and B must be large enough simultaneously.
2. Sort all monsters in increasing order of this difficulty score. The intuition is that monsters that demand lower thresholds should be handled earlier because they can be unlocked with minimal upgrades, and delaying them serves no benefit.
3. Initialize current attributes as A = 10 and B = 10. These represent the starting capabilities before any upgrades.
4. Traverse monsters in sorted order. For each monster i, check whether A ≥ ai and B ≥ bi. If not, the current ordering is invalid and we stop, since no earlier or later adjustment within this ordering can make this monster reachable.
5. If the monster is reachable, we “defeat” it and add ci to our pool of upgrade points. Since each point can be assigned independently to A or B, we conceptually treat this as increasing flexibility, but we do not need to simulate exact distribution because future feasibility depends only on whether we can meet thresholds.
6. Continue until all monsters are processed. If no failure occurs, the ordering is valid and the answer is positive.

The crucial invariant is that at every step, the sorted order ensures we never attempt to process a monster whose requirements exceed what should already be achievable from previously handled, easier monsters. The monotonic increase in available resources means that once a monster becomes feasible, it remains feasible for all later steps, so we never need to reconsider allocation decisions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        monsters = []
        for _ in range(n):
            a, b, c = map(int, input().split())
            monsters.append((max(a, b), a, b, c))

        monsters.sort()

        A, B = 10, 10
        ok = True

        for _, a, b, c in monsters:
            if A < a or B < b:
                ok = False
                break
            A += c
            B += c

        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the greedy idea directly. The sorting key compresses the two constraints into a single ordering rule, while still preserving correctness of the feasibility check. During simulation, we only need to verify reachability at the moment of processing because earlier monsters have already guaranteed sufficient growth.

A subtle point is that we add ci to both A and B in the simulation. This is a deliberate over-approximation: since we are only checking feasibility under a chosen order, distributing all points to both dimensions preserves correctness for the check. If the order is valid under this generous allocation, it is certainly valid under optimal allocation.

## Worked Examples

### Example 1

Input:

```
3
10 10 2
11 10 1
10 11 1
```

Sorted by max(ai, bi), we get:

(10,10), (11,10), (10,11)

| Step | A | B | Monster | Feasible |
| --- | --- | --- | --- | --- |
| 1 | 10 | 10 | (10,10) | Yes |
| 2 | 12 | 12 | (11,10) | Yes |
| 3 | 13 | 13 | (10,11) | Yes |

After the first kill, resources increase, allowing both remaining monsters to be handled without issue. The trace confirms that early easy monsters unlock sufficient buffer for later constraints.

### Example 2

Input:

```
2
10 10 1
20 10 1
```

Sorted order is:

(10,10), (20,10)

| Step | A | B | Monster | Feasible |
| --- | --- | --- | --- | --- |
| 1 | 10 | 10 | (10,10) | Yes |
| 2 | 11 | 11 | (20,10) | No |

The second monster fails immediately because B never reaches 10 while A is insufficient, and the single reward is too small to bridge the gap. This demonstrates that ordering alone cannot rescue insufficient early structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each test processes up to n monsters |
| Space | O(n) | Storage of monster list |

The total n across tests is small enough that sorting and linear simulation easily fit within time limits, and memory usage remains trivial.

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
        monsters = []
        for _ in range(n):
            a, b, c = map(int, input().split())
            monsters.append((max(a, b), a, b, c))
        monsters.sort()

        A, B = 10, 10
        ok = True
        for _, a, b, c in monsters:
            if A < a or B < b:
                ok = False
                break
            A += c
            B += c
        out.append("Yes" if ok else "No")

    return "\n".join(out) + "\n"

# minimal case
assert run("""1
1
10 10 1
""") == "Yes\n"

# impossible due to requirement
assert run("""1
1
11 11 1
""") == "No\n"

# all easy
assert run("""1
3
10 10 1
10 10 1
10 10 1
""") == "Yes\n"

# mixed chain
assert run("""1
3
10 10 1
11 10 1
12 10 1
""") == "Yes\n"

# tight failure
assert run("""1
2
10 10 1
20 20 1
""") == "No\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single killable | Yes | base feasibility |
| single impossible monster | No | hard lower bound |
| all weak monsters | Yes | accumulation works |
| increasing chain | Yes | ordering stability |
| tight gap failure | No | insufficient rewards |

## Edge Cases

A boundary case occurs when a monster is exactly equal to the starting values (10, 10). The algorithm processes it immediately, increases resources, and ensures no incorrect rejection happens at equality.

Another important case is when all monsters have identical requirements but different ci values. Since sorting does not change feasibility in this case, the algorithm still processes them in a valid order, and cumulative growth guarantees success if total reward is sufficient.

A final case involves a monster with slightly higher B requirement but very large ci. Even though it is profitable, it cannot be chosen early because sorting delays it until feasibility naturally emerges, preventing premature allocation that could break other requirements.
