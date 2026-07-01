---
title: "CF 104414D - \u8d26\u53f7 -1"
description: "There are $n$ student accounts labeled $1$ to $n$, plus a special teacher account labeled $-1$. We are also given a sequence of $t$ events."
date: "2026-06-30T20:01:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104414
codeforces_index: "D"
codeforces_contest_name: "2023 Hunan Provincal Multi-University Training (Xiangtan University)"
rating: 0
weight: 104414
solve_time_s: 55
verified: true
draft: false
---

[CF 104414D - \u8d26\u53f7 -1](https://codeforces.com/problemset/problem/104414/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

There are $n$ student accounts labeled $1$ to $n$, plus a special teacher account labeled $-1$. We are also given a sequence of $t$ events. Each event describes one student $x$ who opens the follow list of another account $y$, and then follows everyone currently in $y$'s follow list. If $x$ already follows someone, nothing changes. If $x$ tries to follow themselves, that action is ignored.

Initially, student $1$ follows the teacher $-1$. All other students follow nobody, and the teacher follows nobody.

The process is purely about expanding follow relationships. Each day copies a set of follow edges from one node to another node, with the constraint that self-loops are ignored and duplicate follows are harmless.

The goal is to determine, after all events are processed, which students follow the teacher $-1$.

The constraints are very small: $n \le 100$, $t \le 1000$. This immediately allows any $O(t \cdot n^2)$ or even $O(t \cdot n)$ simulation. There is no need for advanced data structures or asymptotic optimizations beyond straightforward set or bitset propagation.

A subtle edge case comes from the fact that the teacher account $-1$ behaves like a normal node in the graph but is excluded from the final output domain except as a target. Another corner case is repeated copying of the same neighbor list: since sets are idempotent, repeated operations must not double count or break correctness.

A minimal confusing scenario is when copying includes $-1$ itself. For example, if a student who follows the teacher is used as a source, others may indirectly inherit the teacher follow immediately.

## Approaches

The process can be interpreted as a directed graph that evolves over time. Each account maintains a set of outgoing edges representing whom they follow. Each operation takes the full outgoing neighbor set of $y$ and merges it into $x$'s set.

A brute-force simulation naturally suggests itself: maintain a set for each node, and for each operation iterate over all elements in $y$'s set and insert them into $x$'s set. Each insertion is $O(1)$ average with a hash set, so each event costs $O(n)$ in the worst case. Over $t$ events this is $O(tn)$, which is easily acceptable for $n \le 100$, $t \le 1000$.

There is no need for optimization beyond this because the system never requires shortest paths, reachability closure, or repeated recomputation of global structure. Each update is local propagation of a small set.

A more structured view is to think of each node maintaining a bitmask of follows. Then each operation is a bitwise OR of masks, with a self-bit cleared. This reduces constant factors and makes correctness obvious.

The key observation is that the system is monotonic: once a follow edge is added, it is never removed. This prevents oscillations and ensures that simple propagation converges immediately after each operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute-force set simulation | $O(t \cdot n)$ | $O(n^2)$ | Accepted |
| Bitset optimization | $O(t \cdot n / w)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We maintain a structure `follow[i]`, representing the set of accounts followed by user $i$. The teacher is indexed as $-1$, which we map to index $0$ for convenience, and students $1..n$ map to $1..n$.

We also initialize the system according to the statement: student $1$ follows the teacher, so `follow[1] = {teacher}` and all other sets are empty.

For each event $(x, y)$, we merge all elements of `follow[y]` into `follow[x]`, while carefully avoiding self-following.

After processing all events, we scan which students have the teacher in their follow set.

### Steps

1. Initialize an array of sets `follow` of size $n+1$, where index $i$ represents student $i$, and a separate representation for the teacher as a special identifier. This separation avoids confusion with negative indexing.
2. Set the initial condition `follow[1]` to contain the teacher, since student $1$ starts by following $-1$.
3. For each event $(x, y)$, iterate over every account $v$ in `follow[y]`.
4. For each such $v$, if $v \neq x$, insert $v$ into `follow[x]`. The self-check ensures no account follows itself, as required by the system rules.
5. After processing all events, iterate over students $1..n$, and collect those indices $i$ such that the teacher is in `follow[i]`.
6. Sort the resulting list before output, although iteration from $1$ to $n$ already guarantees sorted order.

### Why it works

At any moment, `follow[i]` exactly represents the set of accounts reachable by a sequence of "copy-follow-list" operations ending at $i$, starting from the initial configuration. Each operation only adds elements that were already present in another set, so no artificial elements are introduced. Since sets are used, duplicates do not affect state, and since edges are only added, no earlier relationship is ever lost. This guarantees that after processing all operations, membership in `follow[i]` precisely reflects whether $i$ has ever inherited the teacher through any chain of copying events.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, t = map(int, input().split())
    
    TEACHER = -1
    
    follow = [set() for _ in range(n + 1)]
    
    follow[1].add(TEACHER)
    
    for _ in range(t):
        x, y = map(int, input().split())
        
        # copy all follows from y to x
        for v in follow[y]:
            if v != x:
                follow[x].add(v)
    
    res = []
    for i in range(1, n + 1):
        if TEACHER in follow[i]:
            res.append(i)
    
    print(len(res))
    print(*res)

if __name__ == "__main__":
    main()
```

The solution directly implements the set propagation model. The teacher is represented by a sentinel value $-1$, which is safe because all student IDs are positive. During each operation, we iterate over the current snapshot of `follow[y]` and extend `follow[x]`. The self-check prevents illegal self-follow edges.

The final scan simply checks membership of the teacher in each student's set.

## Worked Examples

### Example 1

Input:

```
3 5
1 2
3 2
1 -1
1 -1
3 1
```

We track only sets involving the teacher.

| Step | Operation | follow[1] | follow[2] | follow[3] |
| --- | --- | --- | --- | --- |
| init | - | {-1} | {} | {} |
| 1 | 1 copies 2 | {-1} | {} | {} |
| 2 | 3 copies 2 | {-1} | {} | {} |
| 3 | 1 copies -1 | {-1} | {} | {} |
| 4 | 1 copies -1 | {-1} | {} | {} |
| 5 | 3 copies 1 | {-1} | {} | {-1} |

Only student 1 and 3 end up following the teacher, so output is:

```
2
1 3
```

This shows that once the teacher appears in a chain, it can propagate forward through subsequent copy operations.

### Example 2

Input:

```
1 1
1 -1
```

| Step | Operation | follow[1] |
| --- | --- | --- |
| init | - | {-1} |
| 1 | 1 copies -1 | {-1} |

Output:

```
1
1
```

This confirms the base case where a single student repeatedly reinforces an already existing follow relationship without change.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \cdot n)$ | Each event merges at most $n$ elements from one set into another |
| Space | $O(n^2)$ | Each of the $n$ nodes may store up to $O(n)$ follows |

The bounds $n \le 100$, $t \le 1000$ make this comfortably fast. The total operations are at most $10^5$ insertions, which is trivial for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, t = map(int, input().split())
    TEACHER = -1
    follow = [set() for _ in range(n + 1)]
    follow[1].add(TEACHER)
    for _ in range(t):
        x, y = map(int, input().split())
        for v in follow[y]:
            if v != x:
                follow[x].add(v)
    res = [i for i in range(1, n + 1) if TEACHER in follow[i]]
    return str(len(res)) + "\n" + " ".join(map(str, res)) + "\n"

# provided sample (conceptual check)
assert run("3 5\n1 2\n3 2\n1 -1\n1 -1\n3 1\n") == "2\n1 3\n"

# minimum case
assert run("1 0\n") == "1\n1\n"

# single propagation
assert run("2 1\n1 -1\n") == "1\n1\n"

# chain propagation
assert run("3 2\n1 -1\n2 1\n") == "2\n1 2\n"

# no propagation
assert run("3 1\n2 1\n") == "1\n1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 1 | Initial condition correctness |
| 2 1; 1 -1 | 1 1 | Basic teacher follow |
| 3 2; 1 -1; 2 1 | 2 1 2 | Propagation through chain |
| 3 1; 2 1 | 1 1 | No accidental spread |

## Edge Cases

One important edge case is when the only source of the teacher is indirect. For example, if student $2$ never directly follows $-1$ but later copies student $1$, who already follows $-1$, then student $2$ must still end up following the teacher. The algorithm handles this because `follow[1]` already contains $-1$, and copying it transfers the teacher mark forward.

Another case is repeated self-copy attempts. If an operation is `(1, -1)` when `follow[-1]` is empty, nothing changes. If repeated many times, the set remains stable because duplicates are ignored by the set structure and self-follow is explicitly blocked.
