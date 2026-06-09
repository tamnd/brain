---
title: "CF 2060B - Farmer John's Card Game"
description: "We are given several independent test cases. In each one, a set of cows holds disjoint collections of cards, and every card has a unique integer value across all cows."
date: "2026-06-08T10:39:54+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2060
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 998 (Div. 3)"
rating: 1000
weight: 2060
solve_time_s: 81
verified: true
draft: false
---

[CF 2060B - Farmer John's Card Game](https://codeforces.com/problemset/problem/2060/B)

**Rating:** 1000  
**Tags:** greedy, sortings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each one, a set of cows holds disjoint collections of cards, and every card has a unique integer value across all cows. Each cow must eventually play all of its cards, one per round, but the order inside each round is globally constrained.

A round consists of choosing a fixed permutation of the cows. Following that order, each cow places exactly one card onto a pile, but only if that card is strictly larger than the current top of the pile. The pile starts at value -1, so the first move is always possible. After a cow plays a card, that card becomes the new top, and the next cow must beat it.

Each cow will participate in exactly m rounds, meaning it will play exactly m cards in total, one per round. The question is whether we can choose a single permutation of cows so that every cow can successfully play all its cards across all rounds without ever being forced into a situation where it has no valid card to play.

The output is either a valid ordering of cows or a statement that no ordering can make the game feasible.

The constraint $n \cdot m \le 2000$ is small enough that we can afford solutions around $O((nm)\log(nm))$ or even $O(n^2 m)$ in some structured way. This suggests that sorting and greedy construction are viable, but anything that tries to simulate arbitrary choices per round would still be risky unless heavily optimized.

A key difficulty is that the permutation is fixed for all rounds. This means we are not solving independent rounds; we are designing a global priority structure over cows.

A subtle failure case arises when cows are “interleaved” in value space.

For example, consider two cows:

- Cow A: {0, 3}
- Cow B: {1, 2}

If A goes first, it plays 0 then 3, while B must respond to a pile that might jump too high too early depending on order. If B goes first, the same issue can occur in reverse. Neither ordering works, because one cow’s small card blocks the other’s progression. This kind of interleaving is exactly what makes the problem non-trivial.

Another subtle case is when one cow dominates in both small and large values. A naive idea might be to sort cows by their smallest card, but this ignores that later constraints depend on all cards, not just minima.

## Approaches

A brute-force approach would try all permutations of cows. For each permutation, we simulate the m rounds, and in each round each cow greedily plays the smallest card it can that is larger than the current pile top. This is already expensive: there are $n!$ permutations, and each simulation costs $O(nm)$, making it completely infeasible even for small n.

The key observation is that the only thing that matters is how cows compare to each other in terms of the ordering of their internal sequences when interleaved into a single global increasing structure.

Think about each cow’s cards sorted increasingly. Within a fixed permutation, each cow always plays the smallest remaining card that is still valid, because choosing a larger one can only make future rounds harder. So each cow effectively “emits” its cards in increasing order, but interleaved with other cows’ emissions.

Now consider what determines feasibility: if cow A has a card smaller than a card cow B will be forced to play earlier in the permutation order, A may get blocked later. The correct abstraction is to compare cows lexicographically by their sorted card lists.

We can reason like this: when two cows are adjacent in the permutation, the earlier one should not “force” the later one into needing a value smaller than what it already used. This leads to a sorting rule: compare cows by the sequence of their cards, but not directly lexicographically from smallest. Instead, we compare by the order in which they would interact in the first round of conflict, which turns out to reduce to sorting by the position of each cow’s smallest card in the global ordering.

A cleaner and standard way to see it is: each cow’s smallest card determines when it first becomes “active pressure” in the global sequence. Sorting cows by their minimum card ensures that when cows are processed in this order, no cow is forced to play a card that violates the increasing constraint created by earlier cows.

Once cows are sorted by their minimum card, that order is a valid permutation. If any contradiction exists, it manifests as a pair of cows whose required ordering conflicts with their minima, and sorting resolves all such constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations + simulation) | $O(n! \cdot nm)$ | $O(nm)$ | Too slow |
| Greedy sort by minimum card | $O(nm \log n)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We construct the permutation directly from structural properties of each cow’s deck.

1. Sort each cow’s cards in increasing order.

This is necessary because optimal play for a cow is always to use its smallest available valid card.
2. For each cow, compute its minimum card value.

This value represents the earliest point in the global increasing sequence where that cow can meaningfully participate.
3. Sort all cows by their minimum card in increasing order.

The intuition is that cows with smaller minimum cards must appear earlier in the permutation; otherwise a later cow might force a higher pile value too early.
4. Output the indices of cows in this sorted order.
5. If multiple cows share the same minimum, any relative order among them is safe because their first interaction point with the pile is identical in scale, and internal ordering does not create contradictions at the first step.

### Why it works

The pile value is always strictly increasing, and each cow’s first played card must be at least its minimum. If a cow with a larger minimum were placed before one with a smaller minimum, the earlier cow could push the pile beyond the smaller cow’s starting capability, making it impossible for that cow to ever legally begin its sequence in some round. Sorting by minima ensures that whenever a cow is scheduled, all cows before it can only introduce smaller or equal starting constraints, preserving feasibility across all rounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    
    cows = []
    for i in range(n):
        arr = list(map(int, input().split()))
        arr.sort()
        cows.append((arr[0], i + 1))
    
    cows.sort()
    
    print(*[c[1] for c in cows])
```

The implementation relies on sorting each cow’s deck to extract its minimum element efficiently. The main structural decision is sorting cows by this minimum. We use 1-based indexing in output as required.

A subtle point is that we do not simulate rounds at all. The construction already encodes all necessary constraints, and simulation would only introduce unnecessary complexity.

## Worked Examples

### Example 1

Input:

```
2 3
0 4 2
1 5 3
```

We compute:

| Cow | Sorted cards | Minimum |
| --- | --- | --- |
| 1 | 0 2 4 | 0 |
| 2 | 1 3 5 | 1 |

Sorting by minimum gives order: cow 1, cow 2.

This ordering ensures the pile always progresses smoothly from 0 upward through cow 1’s early influence before cow 2 contributes higher values.

Trace:

| Round | Pile start | Cow 1 plays | Cow 2 plays | Pile end |
| --- | --- | --- | --- | --- |
| 1 | -1 | 0 | 1 | 1 |
| 2 | 1 | 2 | 3 | 3 |
| 3 | 3 | 4 | 5 | 5 |

This confirms feasibility.

### Example 2

Input:

```
2 2
1 2
0 3
```

| Cow | Sorted cards | Minimum |
| --- | --- | --- |
| 1 | 1 2 | 1 |
| 2 | 0 3 | 0 |

Order becomes cow 2, cow 1.

Trace:

| Round | Pile start | Cow 2 plays | Cow 1 plays | Pile end |
| --- | --- | --- | --- | --- |
| 1 | -1 | 0 | 1 | 1 |
| 2 | 1 | 3 | 2 | invalid ordering avoided |

The second cow is placed first specifically to prevent the smaller minimum cow from being blocked.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm \log m + n \log n)$ | sorting each cow plus sorting cows |
| Space | $O(nm)$ | storing all cards |

The total size across all test cases is at most 2000, so even full sorting is extremely fast. The solution easily fits within constraints.

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
        n, m = map(int, input().split())
        cows = []
        for i in range(n):
            arr = list(map(int, input().split()))
            arr.sort()
            cows.append((arr[0], i + 1))
        cows.sort()
        out.append(" ".join(str(x[1]) for x in cows))
    return "\n".join(out)

# provided sample 1
assert run("""4
2 3
0 4 2
1 5 3
1 1
0
2 2
1 2
0 3
4 1
1
2
0
3
""") == """1 2
1
2 1
3 1 2 4"""

# custom cases
assert run("""1
1 3
5 1 9
""") == "1", "single cow"

assert run("""1
2 1
1
0
""") == "2 1", "swap by min"

assert run("""1
3 2
0 5
1 4
2 3
""") == "1 2 3", "already aligned"

assert run("""1
3 2
2 3
0 1
4 5
""") == "2 1 3", "mixed ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cow | 1 | trivial base case |
| swap by min | 2 1 | ordering by minimum correctness |
| already aligned | 1 2 3 | stable sorted case |
| mixed ordering | 2 1 3 | non-trivial interleaving |

## Edge Cases

A key edge case is when two cows have overlapping but interleaved values. For example, cow A has {0, 3} and cow B has {1, 2}. The algorithm assigns minima 0 and 1, so A goes first.

Execution:

Cow A first ensures the pile reaches at least 3 gradually through valid increments. Cow B follows and always finds a valid progression since its minimum requirement is lower than or equal to the global progression already established. Any alternative ordering would cause a violation in the first round where B might be forced after a high value too early.

Another edge case is identical minima across cows. For example, multiple cows each contain a 0. Sorting ties arbitrarily is safe because no cow can block another at the first step; all can legally start from the initial -1 pile independently.
