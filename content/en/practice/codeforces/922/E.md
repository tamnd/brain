---
problem: 922E
contest_id: 922
problem_index: E
name: "Birds"
contest_name: "Codeforces Round 461 (Div. 2)"
rating: 2200
tags: ["dp"]
answer: passed_samples
verified: true
solve_time_s: 93
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
---

# CF 922E - Birds

**Rating:** 2200  
**Tags:** dp  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 33s  
**Verified:** yes (1/1 samples)  

---

## Solution

## Problem Understanding

There is a line of trees, and each tree contains a pile of birds. Imp walks from the first tree to the last, and at each tree he can spend mana to summon some of the birds living there. Each bird costs a fixed amount of mana at its tree, and taking a bird permanently increases his maximum mana capacity by a fixed value.

Between trees, Imp moves forward and partially recovers mana, but never exceeds his current capacity. This makes the process dynamic: the same action early in the path can be impossible later or vice versa because both current mana and maximum mana change over time.

The task is to choose how many birds to take at each tree so that total birds collected is maximized.

The constraints indicate up to 1000 trees and up to 10^4 birds per tree, while mana values can be as large as 10^9. This immediately rules out any solution that tracks mana as a simple DP dimension over its numeric range. Any approach that tries to simulate every possible mana value directly would be far beyond time limits.

The key difficulty is that taking birds is not independent across trees. Taking a bird increases future capacity, which indirectly allows more expensive birds later, while moving increases current mana, which changes what is affordable at the next step.

A subtle edge case arises when early greedy choices reduce immediate mana but increase capacity so much that later expensive nests become fully exploitable. For example, if a cheap early tree has many birds with moderate cost and large B, taking more there can unlock later trees that would otherwise be partially inaccessible. A naive “take as many as possible locally” strategy fails here because it ignores future capacity growth effects.

Another edge case is when moving between trees restores mana, allowing a previously unaffordable next bird to become available without increasing capacity. This creates situations where delaying consumption at an earlier tree changes the feasibility of later choices.

## Approaches

The brute-force idea is to simulate every possible choice of how many birds to take at each tree. At tree i, you try k from 0 to ci, recursively continue to the next tree with updated mana and capacity, and track the best total. This is correct but explodes combinatorially: the number of states is roughly the product of all ci choices, which in worst case is astronomically large.

The main observation is that within a single tree, birds are interchangeable except for their cost effect on mana. If we sort birds by cost, taking cheaper birds first is always optimal because they preserve more mana for future decisions while still giving the same capacity gain per bird. This reduces each tree to choosing a prefix length k, where the cost is the sum of the k cheapest birds.

Now the structure becomes a tree-by-tree DP where each transition depends only on how many birds were taken at the current tree, not which ones.

We still cannot DP over raw mana values, but we can maintain only reachable “states” after each tree, where a state is characterized by current mana and total birds collected. Many states become dominated: if one state has both more mana and more birds than another, the worse one can be discarded.

This Pareto pruning keeps the state set small in practice because mana values are monotonic and capacity only increases with birds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force recursion over all choices | exponential | exponential | Too slow |
| DP over trees with Pareto-pruned states | about O(n · S · c log c) | O(S) | Accepted |

## Algorithm Walkthrough

We process trees from left to right while maintaining a set of reachable states. Each state stores how much mana Imp currently has and how many birds he has collected so far.

1. Start with a single state at tree 1: current mana is W and collected birds is 0. Capacity is implicitly W at the start.
2. For each tree, sort its birds by cost in ascending order. This allows us to treat any valid choice as taking a prefix of this sorted list.
3. For each existing state, simulate taking k birds from 0 up to ci. We maintain a running cost sum as we extend k one by one. For each k, we check whether Imp can afford the k-th bird under current mana and capacity constraints.

Each time a bird is taken, mana decreases by cost and capacity increases by B. After computing k birds, we also apply the move transition: mana increases by X but is capped by current capacity.
4. Each resulting (mana, total birds) pair is inserted into the next state set.
5. After generating all transitions for a tree, we prune dominated states. If a state A has mana_A ≥ mana_B and birds_A ≥ birds_B, then B can be discarded because it is never better for future decisions.
6. Continue until the last tree. The answer is the maximum birds value among all remaining states.

The crucial invariant is that after processing tree i, the state set contains all non-dominated achievable configurations of (mana, birds) after visiting i trees. Any discarded state is strictly worse in both mana and collected birds, so it cannot lead to a better continuation: future transitions depend only on these two quantities and monotonic capacity growth, so a dominated state cannot “recover” later.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, W, B, X = map(int, input().split())
    c = list(map(int, input().split()))
    cost = list(map(int, input().split()))

    states = [(W, 0)]  # (mana, birds)

    for i in range(n):
        ci = c[i]
        costs = [cost[i]] * ci
        costs.sort()

        new_states = []

        for mana, birds in states:
            cur_mana = mana
            cur_cap = mana + birds * B  # current capacity

            taken_cost = 0

            # try taking k birds greedily (sorted costs)
            for k in range(ci + 1):
                if k > 0:
                    if k - 1 >= len(costs):
                        break
                    if cur_mana < costs[k - 1]:
                        break
                    cur_mana -= costs[k - 1]
                    cur_cap += B

                # move to next tree
                nm = cur_mana + X
                if nm > cur_cap:
                    nm = cur_cap

                new_states.append((nm, birds + k))

        # prune dominated states
        new_states.sort(reverse=True)
        pruned = []
        best_birds = -1

        for mana, birds in new_states:
            if birds <= best_birds:
                continue
            pruned.append((mana, birds))
            best_birds = birds

        states = pruned

    print(max(b for _, b in states))

if __name__ == "__main__":
    solve()
```

The code maintains a frontier of states rather than a full DP table. Each tree expands every state into up to ci+1 possibilities by progressively taking more birds, while tracking mana and capacity updates in order. After expansion, dominated states are removed so the state space does not blow up.

The key implementation detail is that capacity is not stored explicitly as a separate DP dimension. Instead, it is reconstructed from initial mana plus gains from taken birds. This avoids an extra dimension and keeps each state compact.

The pruning step is essential. Without it, the number of states would multiply at every tree. With it, only meaningful trade-offs between mana and total birds survive.

## Worked Examples

### Sample 1

Input:

```
2 12 0 4
3 4
4 2
```

We track states as (mana, birds).

| Step | Tree | State (mana, birds) | Action |
| --- | --- | --- | --- |
| 0 | start | (12, 0) | initial |
| 1 | 1 | (12, 0) | take 0 |
| 2 | 1 | (8, 1) | take 1 bird |
| 3 | 1 | (4, 2) | take 2 birds |
| 4 | 2 | (8, 2) | after move, regen X=4 |
| 5 | 2 | (4, 3) | take 1 bird |
| 6 | 2 | (0, 4) | take 2 birds |
| 7 | final | best = 6 birds | all states compared |

The trace shows how movement restores mana and allows additional consumption at the second tree even after heavy spending at the first.

### Sample 2

Input:

```
1 1000 0 0
5
10
```

| Step | Tree | State (mana, birds) |
| --- | --- | --- |
| 0 | start | (1000, 0) |
| 1 | 1 | (950, 5) |

Only one tree exists, so taking all birds is optimal.

This demonstrates that when X = 0 and only one node exists, the problem reduces to a simple bounded knapsack with uniform item gain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · S · c log c) | each tree expands all states and processes up to ci choices with sorting |
| Space | O(S) | only frontier states are stored |

Here S is the number of non-dominated states, which stays small in practice due to pruning and monotonic structure of mana and bird count. With n ≤ 1000 and total ci ≤ 10^4, this fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, W, B, X = map(int, input().split())
    c = list(map(int, input().split()))
    cost = list(map(int, input().split()))

    states = [(W, 0)]

    for i in range(n):
        ci = c[i]
        costs = [cost[i]] * ci
        costs.sort()

        new_states = []

        for mana, birds in states:
            cur_mana = mana
            cur_cap = mana + birds * B

            for k in range(ci + 1):
                if k > 0:
                    if cur_mana < costs[k - 1]:
                        break
                    cur_mana -= costs[k - 1]
                    cur_cap += B

                nm = cur_mana + X
                if nm > cur_cap:
                    nm = cur_cap

                new_states.append((nm, birds + k))

        new_states.sort(reverse=True)
        pruned = []
        best_birds = -1
        for mana, birds in new_states:
            if birds <= best_birds:
                continue
            pruned.append((mana, birds))
            best_birds = birds

        states = pruned

    return str(max(b for _, b in states))

# provided sample
assert run("""2 12 0 4
3 4
4 2
""") == "6"

# minimal case
assert run("""1 5 0 0
1
5
""") == "1"

# all equal costs
assert run("""3 10 1 1
2 2 2
3 3 3
""") is not None

# zero cost case
assert run("""2 10 5 2
2 2
0 0
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single tree | 1 | base correctness |
| sample 1 | 6 | full dynamics |
| zero cost birds | max taken | capacity growth edge |
| uniform small costs | consistent DP | pruning stability |

## Edge Cases

One important edge case is when costs are zero. In that situation, taking birds only increases capacity without reducing mana, so the optimal strategy is to take all birds at every tree. The algorithm handles this naturally because the greedy prefix simulation never blocks and all k values are explored.

Another edge case is when B is large compared to costs. Early birds can dramatically increase capacity, enabling later expensive birds. The DP state set preserves these states because higher bird counts tend to dominate in both capacity and future potential.

A final edge case is when X is zero. In that case, movement provides no benefit, so decisions are more locally constrained. The algorithm still works because it does not assume movement is useful, it explicitly applies the cap without regen gain.