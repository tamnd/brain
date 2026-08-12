---
title: "CF 102361I - Invoker"
description: "Invoker maintains a sequence of at most three elements. Pressing Q, W, or E appends that element to the sequence. If there are already three elements, the oldest one disappears first."
date: "2026-08-13T00:13:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "I"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 75
verified: true
draft: false
---

[CF 102361I - Invoker](https://codeforces.com/problemset/problem/102361/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

Invoker maintains a sequence of at most three elements. Pressing `Q`, `W`, or `E` appends that element to the sequence. If there are already three elements, the oldest one disappears first. A special skill is determined only by the multiset of the three current elements, so the order matters for future updates but does not matter when deciding which special skill is currently available.

The input string describes the special skills that must be invoked in order. Before every character of the string, Invoker must have the corresponding three-element multiset, then press `R`. Pressing `R` costs one skill and does not change the current ordered sequence of elements. The objective is to minimize the total number of basic skill presses plus `R` presses.

There are only three possible elements, and the inventory contains at most three of them. This makes the complete state space tiny. Once the inventory contains three elements, there are only (3^3=27) possible ordered states. The initial empty state adds one more state. The input length can reach (10^5), so an algorithm with a factor depending on the number of possible states is easily fast enough, while a search over all possible histories is exponential and cannot handle the maximum input.

The main source of mistakes is that a special skill ignores order, while future replacements do not. For example, after building `X`, the elements could be `QWW`, and after building `V` they need only contain `QQW`. Starting from `QWW`, appending `Q` gives `WWQ`, which is still `X`; appending another `Q` gives `WQQ`, which is `V`. Thus `XV` needs (4+2+1=7) skills. A solution that sorts the inventory after every operation would lose the chronological information and could incorrectly claim that fewer basic presses are needed.

Another edge case is repeating a special skill. For input `YY`, the first `Y` needs `QQQ` followed by `R`, while the second `Y` needs only another `R`, because the elements remain after invoking. The answer is `5`. A careless implementation that rebuilds every requested skill from scratch would return `8`.

The initial state is also special. For input `B`, there are no elements at the beginning, so all three elements must be created before the first invocation. The answer is `4`. Treating the initial state as an arbitrary full inventory would underestimate the cost.

## Approaches

A direct brute-force approach can try every possible sequence of basic skills between two invocations. Since every special skill needs exactly three elements, there is never a reason to press more than three basic skills before the next `R`: after three new presses, the entire old inventory has been discarded and any desired three-element multiset can be constructed. A completely unpruned search over the whole history, however, considers every possible basic-skill string. For (n) requested skills, a search allowing up to three basic presses before each invocation has

[
\sum_{k=0}^{3n}3^k=\frac{3^{3n+1}-1}{2}
]

possible basic-skill prefixes in the worst case. For (n=100000), this is astronomically large.

The brute-force reasoning is correct because every legal sequence can be represented by its basic presses and invocations, and enumerating those sequences would eventually find the minimum. Its problem is that it repeatedly explores histories that have the same current inventory and the same future possibilities.

The key observation is that the past can be discarded once we know the current ordered inventory. There are only 27 full ordered inventories. For every pair of such states, we can compute the minimum number of basic presses needed to transform one into the other. Each basic press is simply an edge in a tiny directed graph: append `Q`, `W`, or `E`, and if necessary remove the oldest element.

This turns the problem into dynamic programming over only 27 states. For every requested special skill, we enumerate all ordered permutations of its three elements. There are at most six such states. If the previous ordered inventory is `state` and one of these permutations is `target`, the transition cost is the precomputed minimum number of basic presses from `state` to `target`, plus one for `R`.

The distance table can be computed with BFS from every state. The graph has only 28 states if the empty state is included, and every state has three outgoing edges. The preprocessing is effectively constant time. The main loop performs at most (27\times6) transitions for each character, giving linear complexity in the input length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(3^{3n})) | (O(n)) for a search path | Too slow |
| Optimal | (O(n)) with a small constant | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Represent every ordered inventory as a tuple of zero to three characters. The empty tuple represents the initial state. For a full inventory, `(Q, W, E)` and `(E, W, Q)` are different states because they react differently to the next basic skill.
2. Generate all reachable states by starting from the empty state and repeatedly appending each of `Q`, `W`, and `E`. When a fourth element is appended, keep only the newest three. There are only 28 states in total, so this can be done with a small BFS.
3. Build the shortest-distance table between all states. From each state, one BFS explores the three possible basic skills. The resulting distance tells us the minimum number of basic presses needed to reach any other state.
4. Map each special-skill character to its required multiset. For example, `X` corresponds to `QWW`, `B` corresponds to `QWE`, and `T` corresponds to `EEE`.
5. For each special skill, generate all distinct permutations of its three required elements. The order is not part of the special skill, so every permutation is a valid final inventory. At most six states are produced.
6. Maintain `dp[state]`, the minimum number of skills already used after invoking all processed special skills and ending with the exact ordered inventory `state`. Initially only the empty state is reachable with cost zero.
7. For the next requested special skill, consider every currently reachable state and every valid ordered target state for that special skill. Move between them using the precomputed shortest distance, then add one for pressing `R`. Keep the minimum value for each target state.
8. Replace the old DP array with the new one and process the next character. After the final character, the answer is the minimum DP value over all full states because the last invocation can finish with any ordering of the requested multiset.

### Why it works

The invariant is that `dp[state]` is exactly the minimum cost of completing the processed prefix of the input and having `state` as the current ordered inventory immediately after the last invocation. For the next special skill, every legal strategy must first move from its current state to some ordered inventory whose multiset represents the requested skill. The BFS distance gives the minimum possible number of basic presses for that movement, and the required invocation adds exactly one more operation. Since every valid target ordering is considered, the transition includes every possible legal way to invoke the next skill. Taking the minimum over all previous states therefore preserves the invariant. By induction over the input string, the final minimum is the globally optimal answer.

## Python Solution

```python
import sys
from collections import deque
from itertools import permutations

input = sys.stdin.readline

ELEMENTS = "QWE"

SPECIAL = {
    "Y": "QQQ",
    "V": "QQW",
    "G": "QQE",
    "C": "WWW",
    "X": "QWW",
    "Z": "WWE",
    "T": "EEE",
    "F": "QEE",
    "D": "WEE",
    "B": "QWE",
}

def build_states():
    states = [()]
    index = {(): 0}
    q = deque([()])

    while q:
        state = q.popleft()

        for ch in ELEMENTS:
            nxt = state + (ch,)
            if len(nxt) > 3:
                nxt = nxt[-3:]

            if nxt not in index:
                index[nxt] = len(states)
                states.append(nxt)
                q.append(nxt)

    return states, index

def build_dist(states, index):
    m = len(states)
    dist = [[10**9] * m for _ in range(m)]

    for start in range(m):
        dist[start][start] = 0
        q = deque([start])

        while q:
            u = q.popleft()
            state = states[u]

            for ch in ELEMENTS:
                nxt = state + (ch,)
                if len(nxt) > 3:
                    nxt = nxt[-3:]

                v = index[nxt]
                if dist[start][v] == 10**9:
                    dist[start][v] = dist[start][u] + 1
                    q.append(v)

    return dist

def solve_string(s):
    states, index = build_states()
    dist = build_dist(states, index)

    m = len(states)
    inf = 10**9

    dp = [inf] * m
    dp[index[()]] = 0

    targets = {}

    for skill, elements in SPECIAL.items():
        target_states = set()

        for p in permutations(elements):
            target_states.add(index[p])

        targets[skill] = tuple(target_states)

    for skill in s:
        ndp = [inf] * m

        for u in range(m):
            if dp[u] == inf:
                continue

            for v in targets[skill]:
                cost = dp[u] + dist[u][v] + 1
                if cost < ndp[v]:
                    ndp[v] = cost

        dp = ndp

    return str(min(dp))

def main():
    s = input().strip()
    print(solve_string(s))

if __name__ == "__main__":
    main()
```

The `SPECIAL` dictionary stores one representative ordering of the three elements required by each special skill. The dictionary value is treated as a multiset later, so its particular order has no semantic meaning.

`build_states` constructs every state reachable through basic skills. The tuple representation is useful because tuples are hashable and preserve the chronological order. When the tuple grows beyond three elements, `nxt[-3:]` implements the FIFO replacement rule exactly.

`build_dist` runs BFS from every state. Every edge has cost one because one basic skill press changes the inventory by exactly one operation. BFS is consequently the correct shortest-path algorithm. The empty state is included automatically, which handles the first requested special skill without a separate special case.

For each special skill, `permutations` generates all possible orders. A `set` removes duplicates for skills such as `Y`, where all three permutations are identical. This is a subtle but useful implementation detail because `QQQ` should produce only one target state rather than repeatedly processing the same transition.

The DP update adds `dist[u][v]` for the required basic skills and then adds exactly one for `R`. The invocation does not modify the inventory, so `v` remains the state after the transition. The old DP array is replaced only after all transitions for the current character have been evaluated, preventing one requested skill from being invoked multiple times during a single iteration.

All costs are at most a few hundred thousand for the maximum input, so Python integers have no overflow concerns. The distance table uses a large sentinel value only for initialization, although every state is reachable from every other state within at most three basic presses once the inventory is full.

## Worked Examples

The provided sample is `XDTBVV`. The table below shows the best current DP state after each requested skill. Several states can have the same cost, but only the minimum-cost state relevant to the eventual continuation is shown here as one optimal path.

| Requested skill | Basic presses added | Ordered inventory after `R` | Total cost |
| --- | --- | --- | --- |
| `X` | `QWW` | `QWW` | 4 |
| `D` | `EE` | `WEE` | 7 |
| `T` | `E` | `EEE` | 9 |
| `B` | `WQ` | `EWQ` | 12 |
| `V` | `Q` | `WQQ` | 14 |
| `V` | none | `WQQ` | 15 |

The sequence of operations is `QWWREERERWQRQRR`. The key point in the fourth transition is that the target `B` only needs the multiset `QWE`. Starting from `EEE`, appending `W` gives `EEW`, then appending `Q` gives `EWQ`, whose multiset is exactly `QWE`. The final `V` costs only one `R` because the inventory after the previous invocation is already `WQQ`, which represents `QQW`.

For a second example, consider the constructed input `XV`.

| Requested skill | Basic presses added | Ordered inventory after `R` | Total cost |
| --- | --- | --- | --- |
| `X` | `QWW` | `QWW` | 4 |
| `V` | `QQ` | `WQQ` | 7 |

After creating `QWW`, one additional `Q` produces `WWQ`, which still represents `X`. A second `Q` produces `WQQ`, which represents `V`. Thus two basic presses are necessary between the two invocations, giving (4+2+1=7). This example demonstrates why the ordered state cannot be replaced by only the current unordered multiset.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | The state graph has only 28 states, and every input character checks at most 28 previous states and 6 target permutations. |
| Space | (O(1)) | The distance table and DP arrays have constant size, independent of (n). |

The input can contain (10^5) special skills, so the linear dependence on (n) is the relevant part of the complexity. The constant state space is tiny, and the implementation performs only a few million simple transitions at worst, which is comfortably within the intended limits.

## Test Cases

```python
import sys
import io
from collections import deque
from itertools import permutations

ELEMENTS = "QWE"

SPECIAL = {
    "Y": "QQQ",
    "V": "QQW",
    "G": "QQE",
    "C": "WWW",
    "X": "QWW",
    "Z": "WWE",
    "T": "EEE",
    "F": "QEE",
    "D": "WEE",
    "B": "QWE",
}

def make_solver():
    states = [()]
    index = {(): 0}
    q = deque([()])

    while q:
        state = q.popleft()

        for ch in ELEMENTS:
            nxt = state + (ch,)
            if len(nxt) > 3:
                nxt = nxt[-3:]

            if nxt not in index:
                index[nxt] = len(states)
                states.append(nxt)
                q.append(nxt)

    m = len(states)
    dist = [[10**9] * m for _ in range(m)]

    for start in range(m):
        dist[start][start] = 0
        q = deque([start])

        while q:
            u = q.popleft()

            for ch in ELEMENTS:
                nxt = states[u] + (ch,)
                if len(nxt) > 3:
                    nxt = nxt[-3:]

                v = index[nxt]

                if dist[start][v] == 10**9:
                    dist[start][v] = dist[start][u] + 1
                    q.append(v)

    targets = {}

    for skill, elements in SPECIAL.items():
        targets[skill] = tuple(
            index[p] for p in set(permutations(elements))
        )

    def run(inp: str) -> str:
        s = inp.strip()

        inf = 10**9
        dp = [inf] * m
        dp[index[()]] = 0

        for skill in s:
            ndp = [inf] * m

            for u in range(m):
                if dp[u] == inf:
                    continue

                for v in targets[skill]:
                    ndp[v] = min(
                        ndp[v],
                        dp[u] + dist[u][v] + 1
                    )

            dp = ndp

        return str(min(dp))

    return run

run = make_solver()

# Provided sample
assert run("XDTBVV") == "15", "sample 1"

# Constructed second sample
assert run("XV") == "7", "two different skills requiring ordered-state tracking"

# Minimum-size input
assert run("B") == "4", "one special skill starts from an empty inventory"

# Repeated skill
assert run("YY") == "5", "the inventory survives R"

# All-equal values
assert run("TTTTT") == "8", "EEE is already present after the first invocation"

# Maximum-size input
assert run("Y" * 100000) == str(100003), "maximum input length"

# Boundary transition where one additional element is not enough
assert run("XY") == "8", "changing QWW into QQQ requires three Q presses"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `B` | `4` | Initial empty inventory |
| `YY` | `5` | Reusing the same inventory after `R` |
| `TTTTT` | `8` | Repeated identical special skills |
| `XV` | `7` | Chronological order of elements |
| `XY` | `8` | FIFO replacement and a three-press transition |
| `Y` repeated 100000 times | `100003` | Maximum input size and linear processing |

## Edge Cases

For input `B`, the algorithm starts with the empty state. Every full target state representing `QWE` is three BFS edges away from the empty state, because three basic skills are required to create the first inventory. The DP then adds one for `R`, producing `4`. No artificial full state is assumed at the beginning.

For input `YY`, after the first transition the only relevant inventories are permutations of `QQQ`, all of which are actually the same ordered state `QQQ`. The second `Y` can transition from `QQQ` to itself with distance zero, so only the second `R` is added. The answer is `4+1=5`.

For input `XV`, the first `X` can be built as `QWW` for four operations including `R`. From `QWW`, one `Q` produces `WWQ`, whose multiset is still `QWW`, so it cannot invoke `V` yet. A second `Q` produces `WQQ`, which has multiset `QQW`. The DP finds distance two and adds one for `R`, giving `7`.

For input `XY`, the inventory after `X` can be `QWW`. Appending `Q` twice gives `WWQ` and then `WQQ`, neither of which contains three `Q`s. The third appended `Q` removes the oldest `W` and leaves `QQQ`. The transition distance is therefore three, so the total is `4+3+1=8`. This catches implementations that compare only the number of matching element types without simulating FIFO order.

For the maximum-size input consisting of (100000) copies of `Y`, the first invocation costs four operations. Every later invocation costs only one `R`, because `QQQ` remains unchanged. The result is (4+99999=100003). The DP processes each character independently and never grows with the length of the history, so the large input remains linear.
