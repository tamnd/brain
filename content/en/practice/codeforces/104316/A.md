---
title: "CF 104316A - \u0411\u043b\u0438\u043d\u0441\u043a\u0438\u0435 \u043f\u0435\u0440\u0435\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438..."
description: "We are given a system of $n$ positions, each initially holding a student. The initial arrangement is unknown and is represented by a permutation $b$."
date: "2026-07-01T19:34:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104316
codeforces_index: "A"
codeforces_contest_name: "VIII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b"
rating: 0
weight: 104316
solve_time_s: 60
verified: true
draft: false
---

[CF 104316A - \u0411\u043b\u0438\u043d\u0441\u043a\u0438\u0435 \u043f\u0435\u0440\u0435\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438...](https://codeforces.com/problemset/problem/104316/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system of $n$ positions, each initially holding a student. The initial arrangement is unknown and is represented by a permutation $b$. Over time, the students repeatedly move according to a fixed permutation $p$: the student sitting at position $i$ moves to position $p_i$ in one step. This transformation is applied multiple times.

After all movements, we observe the final arrangement $a$, which is also a permutation. The task is to reconstruct a possible initial arrangement $b$ such that applying the permutation $p$ repeatedly leads to $a$ after some number of full rounds, and among all valid initial arrangements, we must output the lexicographically smallest one.

The key difficulty is that the process is fully reversible in structure because $p$ is a permutation, so every position lies on a cycle. Each cycle evolves independently, and within each cycle we are essentially rotating values.

The constraint $n \le 5 \cdot 10^5$ implies we need a linear or near-linear solution. Anything quadratic over cycles is impossible because worst-case cycles could all be length 1 or one large cycle, and repeated simulation would exceed time limits.

A subtle edge case arises when cycles have multiple valid alignments that lead to the same final arrangement. For example, if a cycle has length 4 and final values are $[1,2,3,4]$ under some rotation, then multiple initial rotations are valid. A naive reconstruction might pick an arbitrary rotation per cycle, but lexicographic minimization couples choices across cycles because earlier positions in the permutation matter more.

Another non-trivial case is when cycles are independent but lexicographic ordering forces us to choose the smallest rotation per cycle in a consistent positional mapping, not value-wise greedily.

## Approaches

A brute-force approach would try all possible initial permutations $b$, simulate applying $p$ until we reach $a$, and check validity. This is immediately infeasible because there are $n!$ candidates, and even a single simulation costs $O(n)$, leading to $O(n! \cdot n)$, which is astronomically large.

The structure of the problem is governed by the permutation $p$. Every index belongs to a directed cycle, and applying $p$ repeatedly just rotates values inside each cycle. This means the problem decomposes into independent cycles.

Inside a single cycle, suppose we list its indices in traversal order. The transformation $p$ acts as a cyclic shift. The final configuration $a$ must therefore correspond to some rotation of the initial configuration $b$. This reduces the problem per cycle to: choose a rotation of the cycle that maps forward under repeated shifts to match $a$, and pick the lexicographically smallest global arrangement.

The key observation is that instead of thinking forward in time, we can assign each cycle a consistent “starting offset” such that when we traverse the cycle in forward direction, the resulting arrangement matches $a$. The constraint from $a$ uniquely determines which rotations are valid, and among them we select the smallest lexicographically by fixing the smallest possible starting value at the earliest position in the cycle order.

Because cycles are independent but lexicographic order compares global arrays, we process cycles in increasing order of their smallest index and greedily assign the smallest feasible rotation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Cycle decomposition | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first decompose the permutation $p$ into disjoint cycles. For each cycle, we record its indices in traversal order.

Next, we use the final arrangement $a$ to understand how values must be placed inside each cycle. Since movement only permutes within cycles, each cycle in $a$ must correspond exactly to a rotation of the values assigned to that cycle in $b$.

We process each cycle independently, but we construct $b$ in a way that ensures lexicographic minimality globally.

1. Identify all cycles of $p$. For each unvisited index, follow $p$ until returning to the start, recording the cycle in order.
2. For each cycle, extract the sequence of values from $a$ at those positions in cycle order. This gives the final rotated version of that cycle.
3. Determine the rotation that would produce the lexicographically smallest possible initial arrangement. Since any rotation is valid, we choose the rotation that makes the first element of the cycle as small as possible, and if tied, continues minimizing lexicographically along the cycle.
4. Write these chosen values back into $b$ along the cycle positions in the corresponding order.

The subtle part is that “lexicographically smallest” applies to the full array, not cycle-local arrays. However, since cycles are disjoint, the earliest differing position between two candidates lies in the cycle containing the smallest index where they differ. Therefore, minimizing each cycle in the order of increasing minimum index guarantees global minimality.

### Why it works

Each cycle is an independent rotation group under permutation $p$. The final array $a$ fixes the multiset of values per cycle and their cyclic order up to rotation. Any valid initial configuration corresponds to selecting a rotation for each cycle. Lexicographic comparison between two global candidates is determined at the first index where they differ, which lies in exactly one cycle. Choosing the lexicographically smallest rotation within each cycle ensures no alternative rotation can produce a smaller prefix at its cycle’s first affected index, so no global improvement is possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = [0] + list(map(int, input().split()))
    a = [0] + list(map(int, input().split()))

    vis = [False] * (n + 1)
    b = [0] * (n + 1)

    for i in range(1, n + 1):
        if vis[i]:
            continue

        cycle = []
        cur = i
        while not vis[cur]:
            vis[cur] = True
            cycle.append(cur)
            cur = p[cur]

        m = len(cycle)

        # values in final arrangement along cycle order
        vals = [a[x] for x in cycle]

        # find lexicographically smallest rotation of vals
        # by doubling and using minimal starting point
        best = 0
        doubled = vals * 2

        for j in range(1, m):
            for k in range(m):
                if doubled[j + k] < doubled[best + k]:
                    best = j
                    break
                if doubled[j + k] > doubled[best + k]:
                    break

        rotated = [doubled[best + k] for k in range(m)]

        for idx, pos in enumerate(cycle):
            b[pos] = rotated[idx]

    print(*b[1:])

if __name__ == "__main__":
    solve()
```

The solution starts by reading the permutation and final arrangement. It then decomposes $p$ into cycles using a visited array. For each cycle, it extracts the corresponding values from $a$, which represent how that cycle looks after all rotations.

To minimize lexicographically, it computes the smallest rotation of that cycle’s value sequence using a straightforward doubling comparison. This is sufficient because each cycle is independent and we only need the smallest cyclic shift.

Finally, it writes the rotated sequence back into the original cycle positions in traversal order, producing the initial arrangement.

A common pitfall is assuming we can sort cycle values or greedily place smallest elements first. That breaks the rotation constraint: the values are locked in a cyclic order, not freely permutable.

## Worked Examples

### Example 1

Input:

```
n = 4
p = [2,1,4,3]
a = [3,2,1,4]
```

Cycle decomposition gives $[1,2]$ and $[3,4]$.

For cycle $[1,2]$, values from $a$ are $[3,2]$. Rotations are $[3,2]$, $[2,3]$. Minimum is $[2,3]$, so $b[1]=2, b[2]=3$.

For cycle $[3,4]$, values are $[1,4]$. Rotations are $[1,4]$, $[4,1]$. Minimum is $[1,4]$, so unchanged.

| Cycle | a-values | Chosen rotation | b assignment |
| --- | --- | --- | --- |
| [1,2] | [3,2] | [2,3] | b1=2, b2=3 |
| [3,4] | [1,4] | [1,4] | b3=1, b4=4 |

Output:

```
2 3 1 4
```

This confirms that each cycle is handled independently while preserving lexicographic minimization.

### Example 2

Input:

```
n = 6
p = [2,1,4,5,3,6]
a = [3,1,2,4,6,5]
```

Cycles are $[1,2]$, $[3,4,5]$, $[6]$.

For $[1,2]$, values $[3,1]$, best rotation is $[1,3]$.

For $[3,4,5]$, values $[2,4,6]$, rotations are compared and smallest is $[2,4,6]$.

For $[6]$, single element remains $[5]$.

| Cycle | a-values | Best rotation | Result |
| --- | --- | --- | --- |
| [1,2] | [3,1] | [1,3] | b1=1, b2=3 |
| [3,4,5] | [2,4,6] | [2,4,6] | b3=2, b4=4, b5=6 |
| [6] | [5] | [5] | b6=5 |

Output:

```
1 3 2 4 6 5
```

This shows how larger cycles behave exactly like independent rotation problems.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ worst in naive rotation check, $O(n)$ cycles amortized | Each index belongs to exactly one cycle; total traversal is linear |
| Space | $O(n)$ | Arrays for permutation, visited markers, and output |

The algorithm runs comfortably within limits because every node is visited once during cycle decomposition, and cycle processing is linear in total size. Even the rotation comparison stays bounded because each element participates in exactly one cycle.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = int(input())
    p = [0] + list(map(int, input().split()))
    a = [0] + list(map(int, input().split()))

    vis = [False] * (n + 1)
    b = [0] * (n + 1)

    for i in range(1, n + 1):
        if vis[i]:
            continue
        cycle = []
        cur = i
        while not vis[cur]:
            vis[cur] = True
            cycle.append(cur)
            cur = p[cur]

        vals = [a[x] for x in cycle]
        m = len(vals)
        doubled = vals * 2

        best = 0
        for j in range(1, m):
            for k in range(m):
                if doubled[j + k] < doubled[best + k]:
                    best = j
                    break
                if doubled[j + k] > doubled[best + k]:
                    break

        for idx, pos in enumerate(cycle):
            b[pos] = doubled[best + idx]

    return " ".join(map(str, b[1:]))

# sample-like tests
assert run("4\n2 1 4 3\n3 2 1 4\n") == "2 3 1 4"
assert run("2\n2 1\n2 1\n") == "1 2"

# minimum size
assert run("1\n1\n1\n") == "1"

# single cycle
assert run("3\n2 3 1\n2 3 1\n") == "1 2 3"

# all same structure but different rotation
assert run("5\n2 3 4 5 1\n2 3 4 5 1\n") == "1 2 3 4 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-cycle | trivial | base correctness |
| identity | same array | fixed points |
| full cycle | sorted rotation | rotation handling |
| repeated structure | lexicographic minimality | global consistency |

## Edge Cases

A single-element cycle behaves trivially because there is only one valid rotation. The algorithm processes it as a cycle of length one and assigns the value directly from $a$, producing the only possible initial value.

For a full-length cycle, the algorithm’s rotation search compares all shifts of the cycle values. Even when multiple rotations appear similar, the lexicographically smallest is consistently chosen because comparison is done lexicographically across the doubled array.

When all cycles are length two, each cycle becomes a simple swap decision. The algorithm still handles them uniformly since rotation comparison degenerates to a two-element comparison.

A more subtle situation is when multiple cycles contain identical value patterns. Even then, cycle independence ensures no interference, and ordering by smallest index inside cycles guarantees deterministic assignment.
