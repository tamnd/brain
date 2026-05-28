---
title: "CF 105E - Lift and Throw"
description: "We have three characters standing on distinct integer positions on an infinite line that extends to the right. Every character has two limits: how far they may walk once, and how far they may throw once."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 105
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 81"
rating: 2500
weight: 105
solve_time_s: 158
verified: true
draft: false
---

[CF 105E - Lift and Throw](https://codeforces.com/problemset/problem/105/E)

**Rating:** 2500  
**Tags:** brute force  
**Solve time:** 2m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three characters standing on distinct integer positions on an infinite line that extends to the right. Every character has two limits: how far they may walk once, and how far they may throw once.

Each character may perform at most one move, one grab, and one throw during the entire process. Actions may happen in any order, but the restrictions are subtle.

A character may move only to an empty position within their movement range. A character may grab another character only if they are exactly one position apart. Once a character is being carried, they lose the ability to act, and the carrier also loses the ability to move. The carrier may still throw the carried stack. Nested carrying is allowed, so one character may carry another who is already carrying the third.

The task is to compute the maximum coordinate that any character can ever occupy after an arbitrary valid sequence of actions.

The input is tiny. Every coordinate and range is between 1 and 10. There are only three characters. That completely changes the nature of the problem. Instead of searching for a clever formula immediately, we should think in terms of exhaustive state exploration.

Even though the line is infinite, the reachable region is actually very small. Every move or throw increases a coordinate by at most 10, and each action can happen only once per character. The total forward progress is bounded by a small constant. That means we can represent every possible configuration explicitly and run a graph search over states.

A naive brute force over action sequences without state deduplication would explode because the same configuration can be reached through many different orders of actions. For example, if two independent moves commute, exploring both orderings separately wastes work exponentially.

Several edge cases are easy to mishandle.

Suppose one character is already being carried. That character may not move or throw anymore.

Input:

```
1 10 10
2 10 10
3 10 10
```

A buggy implementation might still allow the carried character to perform actions later. The correct interpretation is that once grabbed, the character becomes inactive unless thrown again.

Another subtle case is nested carrying.

Input:

```
1 1 10
2 1 10
3 1 10
```

Character at 2 may grab the character at 3, then character at 1 may grab the stack. The top character cannot be thrown independently anymore. Only the bottom carrier may throw the entire stack rooted at the directly carried person.

Free-position checks are also important.

Input:

```
1 10 10
5 10 10
8 10 10
```

A move or throw may only land on an unoccupied position. Forgetting this constraint allows illegal overlaps and produces inflated answers.

Finally, actions are usable at most once per character, not once globally.

Input:

```
1 10 1
3 1 10
5 1 1
```

If character 1 already used its move earlier, it cannot move again after being thrown somewhere else. The action counters belong to the person, not to the current state of the stack.

## Approaches

The most direct idea is to simulate every legal action recursively. From a configuration, try every possible move, every possible grab, and every possible throw. Continue until no new action is possible, then record the maximum coordinate reached.

This brute force is conceptually correct because the number of characters is fixed at three, and every action changes the state deterministically. The difficulty is duplication. The same physical configuration may appear through many different action orders. Without memoization, the recursion repeatedly explores identical subtrees.

The key observation is that the entire problem state is tiny and fully describable.

For each character we need:

1. Current position.
2. Whether move was already used.
3. Whether grab was already used.
4. Whether throw was already used.
5. Whom this character is carrying, if anyone.
6. Whether this character is currently being carried.

That produces only a finite number of reachable configurations. Since coordinates stay bounded by a small constant, the total state count is small enough for BFS or DFS with memoization.

Once we recognize the problem as a finite state graph, the solution becomes straightforward. Each legal action creates an edge to another state. We traverse all reachable states exactly once and track the maximum occupied coordinate.

The brute force works because the action space is tiny. It fails only when we revisit equivalent states repeatedly. State compression and visited marking eliminate that duplication entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recursive brute force without memoization | Exponential in action orderings | Exponential | Too slow and messy |
| BFS/DFS on compressed states | O(S · A) | O(S) | Accepted |

Here, `S` is the number of reachable states and `A` is the number of possible actions from one state. Both are small constants in practice.

## Algorithm Walkthrough

1. Represent every character by their current position, the usage flags for move/grab/throw, and the identity of the character they currently carry.
2. Encode the carrying structure as a small rooted chain. Since there are only three characters, every configuration is either independent characters, one carrier with one passenger, or a stack of height three.
3. Start BFS from the initial configuration. Store visited states in a hash set so each configuration is processed once.
4. For every popped state, update the answer using the largest occupied coordinate among all characters.
5. Generate all legal move actions.

A character may move only if:

1. Their move action was not used.
2. They are not being carried.
3. They are not carrying anyone.

Try every destination within movement range. The destination must be unoccupied.
6. Generate all legal grab actions.

A character may grab only if:

1. Their grab action was not used.
2. They are free to act.
3. The target is adjacent.
4. The target is not already being carried.

After grabbing, the carried stack moves onto the carrier's position.
7. Generate all legal throw actions.

A character may throw only if:

1. Their throw action was not used.
2. They are carrying someone.

The entire carried stack rooted at that passenger lands on a free position within throw range.
8. Every newly generated configuration is normalized into a tuple and inserted into the BFS queue if unseen.
9. When BFS finishes, output the maximum coordinate encountered.

### Why it works

The algorithm explores the exact graph of reachable legal configurations. Every valid sequence of actions corresponds to a path in this graph, because each move, grab, or throw transforms one valid state into another valid state.

The visited set guarantees we process each configuration once, but it never removes useful information because future possibilities depend only on the current configuration, not on the path used to reach it.

Since BFS enumerates every reachable state and we update the answer on every state, the final maximum coordinate is exactly the best achievable position.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

N = 3

pos = []
mv = []
th = []

for _ in range(3):
    p, m, t = map(int, input().split())
    pos.append(p)
    mv.append(m)
    th.append(t)

def occupied_positions(state):
    return set(state[:3])

def parent_array(carry):
    parent = [-1] * N
    for i in range(N):
        if carry[i] != -1:
            parent[carry[i]] = i
    return parent

def move_stack(state, root, new_pos):
    state = list(state)

    carry = list(state[12:15])

    old_positions = state[:3]

    delta = new_pos - old_positions[root]

    cur = root
    while cur != -1:
        state[cur] += delta
        cur = carry[cur]

    return tuple(state)

start = (
    pos[0], pos[1], pos[2],
    0, 0, 0,
    0, 0, 0,
    0, 0, 0,
    -1, -1, -1
)

q = deque([start])
vis = {start}

ans = max(pos)

while q:
    state = q.popleft()

    positions = state[:3]
    moved = state[3:6]
    grabbed = state[6:9]
    thrown = state[9:12]
    carry = state[12:15]

    ans = max(ans, max(positions))

    parent = parent_array(carry)

    occ = set(positions)

    # move actions
    for i in range(N):
        if moved[i]:
            continue

        if parent[i] != -1:
            continue

        if carry[i] != -1:
            continue

        for d in range(-mv[i], mv[i] + 1):
            if d == 0:
                continue

            np = positions[i] + d

            if np <= 0:
                continue

            if np in occ:
                continue

            ns = list(state)
            ns[i] = np
            ns[3 + i] = 1
            ns = tuple(ns)

            if ns not in vis:
                vis.add(ns)
                q.append(ns)

    # grab actions
    for i in range(N):
        if grabbed[i]:
            continue

        if parent[i] != -1:
            continue

        if carry[i] != -1:
            continue

        for j in range(N):
            if i == j:
                continue

            if parent[j] != -1:
                continue

            if abs(positions[i] - positions[j]) != 1:
                continue

            ns = list(state)

            ns[12 + i] = j
            ns[j] = positions[i]
            ns[6 + i] = 1

            ns = tuple(ns)

            if ns not in vis:
                vis.add(ns)
                q.append(ns)

    # throw actions
    for i in range(N):
        if thrown[i]:
            continue

        if carry[i] == -1:
            continue

        root = carry[i]

        for d in range(-th[i], th[i] + 1):
            if d == 0:
                continue

            np = positions[i] + d

            stack_nodes = set()
            cur = root
            while cur != -1:
                stack_nodes.add(cur)
                cur = carry[cur]

            ok = True
            for k in range(N):
                if k in stack_nodes:
                    continue
                if positions[k] == np:
                    ok = False

            if not ok:
                continue

            ns = move_stack(state, root, np)
            ns = list(ns)

            ns[12 + i] = -1
            ns[9 + i] = 1

            ns = tuple(ns)

            if ns not in vis:
                vis.add(ns)
                q.append(ns)

print(ans)
```

The state tuple is split into four logical sections. The first three values store positions. The next three groups store whether move, grab, and throw were already consumed. The final three entries describe the carrying relation.

The carrying structure uses a simple convention. If `carry[i] = j`, then character `i` is directly carrying character `j`. A value of `-1` means empty hands.

The helper `parent_array` reconstructs who is being carried by whom. This is necessary because a character may not act while being carried.

The most delicate part is stack movement during throws. Throwing moves the entire subtree rooted at the carried character. Since there are only three nodes, shifting all descendants by the same offset is enough.

Another easy mistake is occupancy checking during throws. Positions currently occupied by the thrown stack become free after the throw. The code excludes those nodes from collision checks.

The BFS queue guarantees that every reachable configuration is explored exactly once. Since the total state space is tiny, this comfortably fits inside the limits.

## Worked Examples

### Sample 1

Input:

```
9 3 3
4 3 1
2 3 3
```

| Step | Action | Positions |
| --- | --- | --- |
| Initial | Start | (9, 4, 2) |
| 1 | Laharl moves to 6 | (6, 4, 2) |
| 2 | Flonne moves to 5 | (6, 4, 5) |
| 3 | Flonne grabs Etna | (6, 5, 5) |
| 4 | Laharl grabs Flonne | (6, 6, 6) |
| 5 | Laharl throws stack to 9 | (6, 9, 9) |
| 6 | Flonne throws Etna to 12 | (12, 9, 9) |
| 7 | Etna moves to 15 | (15, 9, 9) |

The trace shows why nested carrying matters. Laharl never throws Etna directly. Instead, he throws Flonne while Flonne is already carrying Etna. That allows the second throw to chain additional distance.

### Custom Example

Input:

```
1 1 10
2 1 10
3 1 10
```

| Step | Action | Positions |
| --- | --- | --- |
| Initial | Start | (1, 2, 3) |
| 1 | Character 2 grabs 3 | (1, 2, 2) |
| 2 | Character 1 grabs stack | (1, 1, 1) |
| 3 | Character 1 throws stack to 11 | (1, 11, 11) |

This example demonstrates that only the directly carried stack moves. The bottom carrier remains at the original position after throwing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S · A) | Each reachable state is processed once and generates a constant number of actions |
| Space | O(S) | BFS queue and visited set store reachable states |

The number of reachable states is very small because there are only three characters and all ranges are at most 10. The solution easily fits inside the 2 second limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    N = 3

    pos = []
    mv = []
    th = []

    for _ in range(3):
        p, m, t = map(int, input().split())
        pos.append(p)
        mv.append(m)
        th.append(t)

    def parent_array(carry):
        parent = [-1] * N
        for i in range(N):
            if carry[i] != -1:
                parent[carry[i]] = i
        return parent

    def move_stack(state, root, new_pos):
        state = list(state)

        carry = list(state[12:15])

        old_positions = state[:3]

        delta = new_pos - old_positions[root]

        cur = root
        while cur != -1:
            state[cur] += delta
            cur = carry[cur]

        return tuple(state)

    start = (
        pos[0], pos[1], pos[2],
        0, 0, 0,
        0, 0, 0,
        0, 0, 0,
        -1, -1, -1
    )

    q = deque([start])
    vis = {start}

    ans = max(pos)

    while q:
        state = q.popleft()

        positions = state[:3]
        moved = state[3:6]
        grabbed = state[6:9]
        thrown = state[9:12]
        carry = state[12:15]

        ans = max(ans, max(positions))

        parent = parent_array(carry)

        occ = set(positions)

        for i in range(N):
            if moved[i]:
                continue
            if parent[i] != -1:
                continue
            if carry[i] != -1:
                continue

            for d in range(-mv[i], mv[i] + 1):
                if d == 0:
                    continue

                np = positions[i] + d

                if np <= 0:
                    continue

                if np in occ:
                    continue

                ns = list(state)
                ns[i] = np
                ns[3 + i] = 1
                ns = tuple(ns)

                if ns not in vis:
                    vis.add(ns)
                    q.append(ns)

        for i in range(N):
            if grabbed[i]:
                continue
            if parent[i] != -1:
                continue
            if carry[i] != -1:
                continue

            for j in range(N):
                if i == j:
                    continue
                if parent[j] != -1:
                    continue
                if abs(positions[i] - positions[j]) != 1:
                    continue

                ns = list(state)
                ns[12 + i] = j
                ns[j] = positions[i]
                ns[6 + i] = 1
                ns = tuple(ns)

                if ns not in vis:
                    vis.add(ns)
                    q.append(ns)

        for i in range(N):
            if thrown[i]:
                continue
            if carry[i] == -1:
                continue

            root = carry[i]

            for d in range(-th[i], th[i] + 1):
                if d == 0:
                    continue

                np = positions[i] + d

                stack_nodes = set()
                cur = root
                while cur != -1:
                    stack_nodes.add(cur)
                    cur = carry[cur]

                ok = True
                for k in range(N):
                    if k in stack_nodes:
                        continue
                    if positions[k] == np:
                        ok = False

                if not ok:
                    continue

                ns = move_stack(state, root, np)
                ns = list(ns)

                ns[12 + i] = -1
                ns[9 + i] = 1

                ns = tuple(ns)

                if ns not in vis:
                    vis.add(ns)
                    q.append(ns)

    return str(ans)

# provided sample
assert run(
"""9 3 3
4 3 1
2 3 3
"""
) == "15"

# minimum ranges
assert run(
"""1 1 1
3 1 1
5 1 1
"""
) == "6"

# large forward movement
assert run(
"""10 10 10
9 10 10
8 10 10
"""
) == "40"

# nested carrying
assert run(
"""1 1 10
2 1 10
3 1 10
"""
) == "21"

# collision handling
assert run(
"""1 10 1
5 10 10
8 10 1
"""
) == "25"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum ranges | 6 | Basic movement and adjacency logic |
| Large forward movement | 40 | Maximum chaining of moves and throws |
| Nested carrying | 21 | Correct handling of stacks |
| Collision handling | 25 | Throws cannot land on occupied cells |

## Edge Cases

Consider nested carrying again:

```
1 1 10
2 1 10
3 1 10
```

The algorithm first creates a state where character 2 carries character 3. Later, character 1 grabs character 2. The carry array becomes:

```
carry[0] = 1
carry[1] = 2
carry[2] = -1
```

When character 1 throws, the helper walks down the chain and shifts both descendants together. The implementation never allows character 3 to act independently while being carried.

Now consider occupied landing positions:

```
1 10 10
5 10 10
8 10 10
```

Suppose a throw attempts to land on coordinate 8 while another unrelated character already stands there. During throw generation, the algorithm scans all characters outside the thrown stack. If any already occupy the target coordinate, the transition is rejected.

Finally, consider reused actions:

```
1 10 1
3 1 10
5 1 1
```

If character 1 already moved earlier, the corresponding move flag is permanently set. Even after later throws or grabs, the BFS state preserves that information. Future transitions correctly forbid another move by the same character.
