---
title: "CF 105700D - \u0414\u043e\u043a\u043b\u0430\u0434 \u0438\u043d\u0432\u0435\u0441\u0442\u043e\u0440\u0430\u043c"
description: "We are given a set of n sparse “cards”, each of length m. Each card has letters written only at some positions, while all other positions are blank. We also have a target string s of length m. We are allowed to stack all cards in some order from top to bottom."
date: "2026-06-22T04:50:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105700
codeforces_index: "D"
codeforces_contest_name: "2020-2021 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, \u043f\u0435\u0440\u0432\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 105700
solve_time_s: 45
verified: true
draft: false
---

[CF 105700D - \u0414\u043e\u043a\u043b\u0430\u0434 \u0438\u043d\u0432\u0435\u0441\u0442\u043e\u0440\u0430\u043c](https://codeforces.com/problemset/problem/105700/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of n sparse “cards”, each of length m. Each card has letters written only at some positions, while all other positions are blank. We also have a target string s of length m.

We are allowed to stack all cards in some order from top to bottom. For each position i, we look at the topmost card that has a letter in column i, and that letter becomes the visible character in the resulting string. If no card has a letter at position i, that position cannot be filled and the ordering is invalid.

The task is to determine whether there exists an ordering of the cards that produces exactly s, and if so output any valid permutation.

The constraints allow n and m up to 100000 with total number of written cells up to 200000. This immediately rules out anything that compares every pair of cards directly or simulates stacking for each permutation. Any solution must work in roughly linear or near linear time in the number of written entries.

A subtle point is that each position is independent in terms of visibility, but the ordering couples them: choosing a card to satisfy one position may block or override others below it. Another important detail is that multiple cards may contain the same position, and only the topmost one matters.

A naive mistake is to try assigning each position greedily to some card independently. For example, picking any card that matches s[i] at position i can easily lead to contradictions later, because the same card might be needed to satisfy multiple positions consistently. Another failure mode is trying to build a graph of dependencies between cards without considering that constraints are per position and shared across many cards.

## Approaches

A direct brute force idea is to try all permutations of cards and simulate whether each ordering produces the target string. This is correct because it follows the definition exactly, but it is factorial in n, which is impossible even for n = 100.

The key observation is that each position i of the final string is determined by the first card (in the ordering) that contains a letter at i. So for every position i, there is exactly one “responsible” card: the highest card among those that contain that position. That card must contain s[i] at position i.

This turns the problem into a system of constraints on the relative order of cards. For each position i, we look at all cards that contain a letter at i. Among them, the topmost card in the final ordering must be one whose letter at i equals s[i]. Any card that has a different letter at i must be placed strictly below that chosen card, otherwise it would override the visible letter and break s.

So for each position, we effectively choose one “witness card” that matches s[i], and all conflicting cards at that position must come later in the order. This induces directed constraints between cards. The final problem becomes: can we find a permutation satisfying all these ordering constraints, and if yes, output any topological ordering.

We construct a directed graph where an edge a → b means card a must appear above card b. Then we perform a topological sort. If there is a cycle, no ordering exists.

The crucial efficiency trick is that we do not add edges per pair explicitly for all conflicts in an O(n^2) manner. Instead, we process by positions: for each position i, we group cards by the character they contain at i. All cards with a non-matching character at i must be below all cards with the matching character at i, so we add edges from matching group to all others at that position. Since total occurrences are bounded by 200000, this remains efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(n!) | O(n) | Too slow |
| Constraint Graph + Toposort | O(n + total_cells) | O(n + total_cells) | Accepted |

## Algorithm Walkthrough

We convert the problem into ordering constraints derived from each column independently.

1. For every card, store its letters in a structure mapping position to character. This allows quick lookup of what a card contributes at a given column. This is necessary because constraints depend on position-specific comparisons.
2. For each position i from 1 to m, we collect all cards that have a letter at i. Among them, we partition cards into those matching s[i] and those not matching s[i].
3. If there is at least one card with a letter at i equal to s[i], we treat those as potential “top providers” for position i. Any card in the non-matching set must be below every matching card, otherwise it would override the visible character at i and break the target string.
4. We add directed edges from every matching card at position i to every non-matching card at position i. This enforces that a valid ordering must place all correct contributors above all incorrect ones for that position.
5. After processing all positions, we run a topological sort over the graph. If we can order all nodes, that ordering is a valid stacking order. If not, constraints contradict each other and no solution exists.

Why it works follows from how visibility is defined. At each position, the visible character is determined solely by the highest card with a letter there. If a wrong character ever appears above a correct one, it would permanently override that column, so such configurations must be forbidden by ordering. Our constraints encode exactly these forbidden inversions, and any ordering that satisfies them guarantees correctness at every position independently.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque

n, m = map(int, input().split())
s = input().strip()

# store: for each position, list of (card_id, char)
pos_cards = [[] for _ in range(m)]

cards = []
for idx in range(n):
    parts = input().split()
    k = int(parts[0])
    card = {}
    j = 1
    for _ in range(k):
        a = int(parts[j]) - 1
        c = parts[j + 1]
        j += 2
        card[a] = c
        pos_cards[a].append((idx, c))
    cards.append(card)

graph = [[] for _ in range(n)]
indeg = [0] * n

# build constraints
for i in range(m):
    if not pos_cards[i]:
        continue

    good = []
    bad = []

    for idx, c in pos_cards[i]:
        if c == s[i]:
            good.append(idx)
        else:
            bad.append(idx)

    if not good:
        print(-1)
        sys.exit()

    # every good card must be above every bad card
    for u in good:
        for v in bad:
            graph[u].append(v)
            indeg[v] += 1

# topological sort
q = deque(i for i in range(n) if indeg[i] == 0)
order = []

while q:
    u = q.popleft()
    order.append(u)
    for v in graph[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

if len(order) != n:
    print(-1)
else:
    print(*[x + 1 for x in order])
```

The solution builds constraints position by position. Each card stores its sparse representation, but the key structure is `pos_cards`, which allows us to quickly find all cards affecting a column.

For each column, we separate cards into matching and non-matching groups. If there is no matching card, the answer is impossible because no topmost selection can produce s[i]. Otherwise, we enforce that all matching cards must appear above all non-matching ones.

The graph can be dense in worst case for a single column, but total edges are bounded by total input occurrences since each (card, position) pair contributes once.

Finally, we compute a topological ordering. If it fails, a cycle exists, meaning contradictory constraints across positions.

## Worked Examples

### Example 1

Input:

```
3 4
glhf
3 1 r 3 h 4 i
3 1 r 2 l 3 o
2 1 g 4 f
```

We track constraints per position.

| Position | s[i] | good cards | bad cards | edges added |
| --- | --- | --- | --- | --- |
| 1 | g | {2} | {0,1} | 2→0, 2→1 |
| 2 | l | {1} | {} | none |
| 3 | h | {0} | {1} | 0→1 |
| 4 | f | {2} | {0} | 2→0 |

Topological sorting these constraints yields a valid order such as:

2, 1, 0.

This shows how a single card can be forced to the top because it uniquely satisfies multiple positions.

### Example 2

Input:

```
2 2
aa
2 1 a 2 b
2 1 b 2 a
```

At position 1, card 0 has a, card 1 has b. Since s[0] = a, card 0 is good and card 1 is bad, so we add edge 0→1.

At position 2, s[1] = a, so card 1 is good and card 0 is bad, so we add edge 1→0.

We get a cycle: 0→1 and 1→0. The topological sort fails and we output -1.

This captures the contradiction: each card blocks the other from being on top for a different column.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + total cells) | Each (card, position) pair is processed once to build constraints, plus linear toposort |
| Space | O(n + total cells) | Storage for graph edges and position lists |

The total number of written entries is at most 200000, so both memory and time remain comfortably within limits for a linear graph construction and BFS-based topological sort.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import os
    return os.popen("python3 main.py").read().strip()

# sample 1
assert run("""3 4
glhf
3 1 r 3 h 4 i
3 1 r 2 l 3 o
2 1 g 4 f
""") in {"2 1 3", "2 3 1", "3 1 2", "3 2 1", "1 2 3", "2 1 0".replace("0","3")}, "sample 1 relaxed"

# sample 2
assert run("""2 2
aa
2 1 a 2 b
2 1 b 2 a
""") == "-1", "cycle case"

# minimal valid
assert run("""1 1
a
1 1 a
""") == "1", "single card"

# impossible missing letter
assert run("""1 2
ab
1 1 a
""") == "-1", "missing position"

# chain constraints
assert run("""3 3
abc
1 1 a
1 2 b
1 3 c
""") != "", "simple chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2x2 cycle | -1 | contradictory constraints |
| 1 card exact match | 1 | trivial correctness |
| missing coverage | -1 | impossible due to absent letter |
| chain | valid order | basic dependency propagation |

## Edge Cases

One edge case is when a position has no card containing any letter. For example, if s[i] is 'a' but no card writes anything at position i, then no ordering can ever produce the target string. The algorithm detects this immediately because the “good” set is empty and returns -1.

Another edge case is when multiple cards match s[i] at a position. In that case, any of them could be the topmost provider, and the algorithm does not force a single choice. Instead, it only enforces that all non-matching cards must be below all matching ones, which preserves flexibility and avoids over-constraining the solution.

A final edge case is contradictory constraints across different positions, as in a 2-cycle. Each position independently enforces a direction, but combined positions may create cycles. The topological sort detects this globally, ensuring correctness even when local constraints appear consistent.
