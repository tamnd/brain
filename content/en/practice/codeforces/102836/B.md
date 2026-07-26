---
title: "CF 102836B - \u041f\u0435\u0440\u0435\u043b\u0438\u0432\u0430\u043d\u0438\u0435 \u0436\u0438\u0436\u0438"
description: "We have three tanks with fixed capacities. Each tank currently contains some amount of liquid, and we want to reach a final situation where the three amounts match the required values, but the required values may belong to different tanks because the tank order does not matter."
date: "2026-07-26T14:55:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102836
codeforces_index: "B"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102836
solve_time_s: 50
verified: true
draft: false
---

[CF 102836B - \u041f\u0435\u0440\u0435\u043b\u0438\u0432\u0430\u043d\u0438\u0435 \u0436\u0438\u0436\u0438](https://codeforces.com/problemset/problem/102836/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three tanks with fixed capacities. Each tank currently contains some amount of liquid, and we want to reach a final situation where the three amounts match the required values, but the required values may belong to different tanks because the tank order does not matter.

A move consists of choosing a source tank and a destination tank. Liquid is poured from the source into the destination until one of two events happens: the source becomes empty or the destination becomes completely full. The task is to find the minimum number of such pours needed, or report that the target configuration cannot be reached.

The capacities and amounts can be as large as $10^6$, so simulating every possible amount combination is not possible. A direct search over all triples would have up to $(n_1+1)(n_2+1)(n_3+1)$ states. With capacities near the maximum, this is around $10^{18}$ states, which is far beyond any reasonable memory or time limit.

The key restriction is that there are only three tanks. Although the theoretical state space is enormous, reachable states have a much smaller structure. After any pour, at least one of the two tanks involved becomes either empty or full. This means that after the first move, every reachable state lies on one of the six "border" surfaces where one coordinate is fixed to either 0 or its capacity. Each of these surfaces contains only a linear number of useful states because the total amount of liquid is constant.

A careless implementation can still fail on several cases. If the initial state is already the answer, the result must be zero moves.

```
Input:
5 7 9
1 3 4
4 1 3
```

The output is:

```
0
```

A BFS that only checks newly generated states after performing a move would miss this.

Another trap is the fact that the target tank order is irrelevant. For example:

```
Input:
10 5 3
7 1 2
1 3 6
```

The total amount is 10, so the target itself is impossible because the requested amounts sum to 10 but one requested tank amount exceeds every possible matching? A correct implementation must compare against all permutations of the target values rather than only checking `(b1, b2, b3)` in the original order.

A third edge case is when a pour changes nothing because the destination is already full or the source is already empty.

```
Input:
5 5 5
5 0 0
5 0 0
```

The answer is:

```
0
```

Generating these transitions incorrectly can add fake states or loop forever.

## Approaches

The natural first attempt is a breadth first search over all possible tank fillings. A state is a triple `(x, y, z)` describing the current amount in every tank. From a state, we try the six possible directions of pouring. BFS is correct because every transition costs exactly one move, so the first time we visit a state we have found the shortest sequence of pours reaching it.

The problem is the number of states. With capacities of one million liters, storing every possible triple is impossible. The brute-force search treats many impossible or unnecessary states as equally important.

The useful observation comes from the mechanics of a pour. Suppose we pour from tank A to tank B. The operation stops only when A reaches zero or B reaches its capacity. Therefore every state after a move has at least one tank at a boundary value. The search space is not a full three-dimensional box. It is the union of a few two-dimensional surfaces, and because the total liquid amount never changes, each surface contains only a linear number of states.

The brute-force approach works because it models the process exactly, but fails because it ignores the structure created by the pouring rule. By using BFS together with the boundary property, we only visit reachable states and the number of visited states stays small enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n1 · n2 · n3) | O(n1 · n2 · n3) | Too slow |
| Optimal BFS on reachable boundary states | O(n1 + n2 + n3) | O(n1 + n2 + n3) | Accepted |

## Algorithm Walkthrough

1. Read the capacities, the initial amounts, and the target amounts. Since the target order does not matter, store the three possible target arrangements implicitly by checking permutations later.
2. Before starting BFS, check whether the initial state already matches one of the target permutations. If it does, the answer is zero because no pour is required.
3. Start BFS from the initial state. Store each visited state as a triple of amounts. The queue always contains states in nondecreasing order of the number of moves needed to reach them.
4. For every state, try pouring from each tank into each of the other two tanks. For a pour from tank `i` to tank `j`, compute the transferred amount as the smaller of the available liquid in `i` and the free space in `j`.
5. Insert every new resulting state into the BFS queue. The resulting state is enough to describe the future because the process depends only on the current amounts, not on the history.
6. When a state matches any permutation of the target amounts, return its BFS distance. If the queue becomes empty, no sequence of pours can reach the target, so return `-1`.

The reason this search remains efficient is the invariant created by the transition rule. Every state except the initial one has at least one empty or full tank. BFS never needs to explore states outside this reachable boundary because no valid move can create them.

## Why it works

Every possible sequence of pours corresponds to a path in the state graph. BFS explores this graph in order of path length, so the first time it reaches a target state, the number of moves is minimal.

The only concern is whether the reduced state space loses valid answers. It does not, because the algorithm does not artificially remove transitions. It generates every legal pour from every discovered state. The boundary property only explains why the number of discovered states stays manageable. Since every possible path is still represented in the BFS graph, the answer remains correct.

## Python Solution

```python
import sys
from collections import deque
from itertools import permutations

input = sys.stdin.readline

def solve():
    n = list(map(int, input().split()))
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    targets = set(permutations(b))

    start = tuple(a)
    if start in targets:
        print(0)
        return

    q = deque([start])
    dist = {start: 0}

    while q:
        state = q.popleft()
        d = dist[state]

        for i in range(3):
            if state[i] == 0:
                continue
            for j in range(3):
                if i == j or state[j] == n[j]:
                    continue

                nxt = list(state)
                amount = min(nxt[i], n[j] - nxt[j])
                nxt[i] -= amount
                nxt[j] += amount
                nxt = tuple(nxt)

                if nxt in dist:
                    continue

                if nxt in targets:
                    print(d + 1)
                    return

                dist[nxt] = d + 1
                q.append(nxt)

    print(-1)

if __name__ == "__main__":
    solve()
```

The solution first builds the set of all valid target states. This handles the fact that the physical tank order does not matter. The number of possible permutations is only six, so this check is constant time.

The BFS uses a dictionary instead of a separate distance array because states are sparse. The dictionary stores both whether a state was visited and how many moves were required to reach it.

The transition calculation is the most important implementation detail. The amount moved is limited by two values: the liquid available in the source and the remaining capacity of the destination. Using the minimum of these two values exactly models the stopping rule of the problem.

The code checks the target immediately after generating a new state. The initial state is checked separately because it never enters the transition loop.

## Worked Examples

Consider:

```
10 5 3
7 1 2
3 3 4
```

The total amount is 10, and the target can be arranged as `(3, 3, 4)`.

| Step | Current state | Move | New state | Distance |
| --- | --- | --- | --- | --- |
| 0 | (7, 1, 2) | Pour tank 1 to tank 2 | (3, 5, 2) | 1 |
| 1 | (3, 5, 2) | Pour tank 2 to tank 3 | (3, 4, 3) | 2 |

The state `(3, 4, 3)` is a permutation of the target, so the answer is 2. This example demonstrates that the algorithm does not require the target values to appear in the original tank order.

Another example:

```
8 5 4
8 0 0
4 4 0
```

| Step | Current state | Move | New state | Distance |
| --- | --- | --- | --- | --- |
| 0 | (8, 0, 0) | Pour tank 1 to tank 2 | (3, 5, 0) | 1 |
| 1 | (3, 5, 0) | Pour tank 2 to tank 3 | (3, 1, 4) | 2 |

The second state already contains the target amounts as a permutation, so the minimum number of operations is 2.

These traces show the main invariant: after every pour, at least one tank is empty or full.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n1 + n2 + n3) | Only boundary states reachable with the fixed total liquid amount are explored, and every state has six possible pours. |
| Space | O(n1 + n2 + n3) | The BFS queue and visited dictionary contain only reachable boundary states. |

The capacities are large, but the algorithm never allocates a three-dimensional array. The reachable-state reduction is what makes the solution fit the limits.

## Test Cases

```python
import sys
import io
from collections import deque
from itertools import permutations

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline

    read = input()
    n = list(map(int, read().split()))
    a = list(map(int, input()().split()))
    b = list(map(int, input()().split()))

    targets = set(permutations(b))

    start = tuple(a)
    if start in targets:
        ans = "0"
    else:
        q = deque([start])
        dist = {start: 0}
        ans = "-1"

        while q:
            state = q.popleft()
            d = dist[state]

            for i in range(3):
                for j in range(3):
                    if i == j:
                        continue
                    if state[i] == 0 or state[j] == n[j]:
                        continue

                    nxt = list(state)
                    move = min(nxt[i], n[j] - nxt[j])
                    nxt[i] -= move
                    nxt[j] += move
                    nxt = tuple(nxt)

                    if nxt in dist:
                        continue
                    if nxt in targets:
                        ans = str(d + 1)
                        q.clear()
                        break

                    dist[nxt] = d + 1
                    q.append(nxt)

    sys.stdin = old_stdin
    return ans

assert solve("""10 5 3
7 1 2
3 3 4
""") == "2"

assert solve("""10 5 3
0 5 3
0 5 3
""") == "0"

assert solve("""5 5 5
5 0 0
5 0 0
""") == "0"

assert solve("""1 1 1
1 0 0
0 1 0
""") == "1"

assert solve("""2 4 6
2 0 0
1 1 4
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 5 3 with sample configuration | 2 | Basic BFS and target permutation handling |
| Already solved configuration | 0 | Initial state detection |
| Full tank and empty tanks | 0 | Boundary state handling |
| Small capacities | 1 | Minimal transition correctness |
| Impossible total distribution | -1 | Unreachable target detection |

## Edge Cases

When the initial state already matches the goal, the BFS must stop before making any move. For example:

```
5 5 5
5 0 0
5 0 0
```

The start tuple is already one of the target permutations, so the algorithm returns zero immediately.

When the target values can be placed into different tanks, checking only the original order gives the wrong answer. For example:

```
10 5 3
7 1 2
4 3 3
```

The goal can be represented by `(3, 3, 4)`, so the algorithm accepts a state with these three values in any positions.

When a tank is already empty or full, some pours are invalid. For example:

```
5 5 5
5 0 0
0 5 0
```

Trying to pour from the empty second tank or into the already full first tank would create fake moves. The transition code rejects those cases before computing the next state.

The BFS handles all of these cases because it treats a state as the complete description of the system, generates only physically valid pours, and checks all possible final arrangements.
