---
title: "CF 1136D - Nastya Is Buying Lunch"
description: "The queue is fixed initially, and the last person in the queue is Nastya. Some ordered pairs $(u,v)$ are given. A pair means that whenever pupil $u$ stands immediately in front of pupil $v$, those two pupils are willing to swap places."
date: "2026-06-12T04:01:37+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1136
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 546 (Div. 2)"
rating: 1800
weight: 1136
solve_time_s: 86
verified: true
draft: false
---

[CF 1136D - Nastya Is Buying Lunch](https://codeforces.com/problemset/problem/1136/D)

**Rating:** 1800  
**Tags:** greedy  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The queue is fixed initially, and the last person in the queue is Nastya. Some ordered pairs $(u,v)$ are given. A pair means that whenever pupil $u$ stands immediately in front of pupil $v$, those two pupils are willing to swap places.

Nastya wants to move as far toward the front of the queue as possible by repeatedly using such adjacent swaps. We need to determine how many positions she can advance.

The queue contains up to $3 \cdot 10^5$ pupils and there can be up to $5 \cdot 10^5$ allowed swap relations. These limits immediately rule out any simulation of swaps. Even an $O(n^2)$ algorithm would perform around $9 \cdot 10^{10}$ operations in the worst case, which is far beyond the time limit. We need something close to linear in the input size.

The subtle part of the problem is that Nastya does not swap directly with arbitrary people. Every swap must involve two adjacent pupils, and the permission depends on the identities of those two pupils.

A common mistake is to think that Nastya can pass a pupil $x$ if there exists a direct permission $(x,\text{Nastya})$. Sometimes she can bypass $x$ indirectly after rearranging other pupils.

Consider:

```
Queue: [1, 2, 3]
Nastya = 3

Permissions:
1 -> 3
1 -> 2
```

Nastya cannot pass pupil 2. Even though 1 can swap with 3, pupil 2 blocks access and cannot be crossed. The answer is 0.

Another easy mistake is to simulate only immediate opportunities.

```
Queue: [1, 2, 3, 4]
Nastya = 4

Permissions:
1 -> 4
2 -> 4
3 -> 4
```

Here Nastya can move all the way to the front. After passing 3, she becomes adjacent to 2, then to 1. The answer is 3.

The challenge is identifying exactly which pupils are unavoidable obstacles.

## Approaches

A brute-force view is to treat the queue as a state and repeatedly perform any available adjacent swap involving Nastya. One could try searching all reachable configurations or greedily simulating swaps. The difficulty is that rearrangements among other pupils can create new opportunities later. The state space is enormous, up to $n!$, so this direction is hopeless.

The key observation comes from looking at the queue from right to left.

Let $x$ be Nastya's number, which is the last element of the permutation.

Imagine examining the pupils standing before Nastya, starting from the one closest to her and moving toward the front.

Suppose we have already identified a set of pupils that must remain in front of Nastya no matter what. Call this set **blocked**.

Now consider another pupil $v$ farther left.

Can Nastya eventually pass $v$?

To pass $v$, she must at some moment become adjacent to $v$. Every currently blocked pupil must somehow move behind $v$ first. The only way that can happen is if $v$ is willing to swap with every blocked pupil that needs to cross it.

If even one blocked pupil $u$ exists such that the permission $(v,u)$ is absent, then $u$ can never move behind $v$. Consequently Nastya can never become adjacent to $v$, so $v$ itself becomes blocked.

On the other hand, if $v$ has permissions toward every currently blocked pupil, then all those blocked pupils can be moved behind $v$, allowing Nastya eventually to pass $v$.

This leads to a very compact greedy process.

Maintain the set of blocked pupils. Initially it contains only Nastya herself.

Process the queue from right to left, excluding Nastya.

For each pupil $v$, count how many blocked pupils $u$ satisfy the permission $(v,u)$.

If this count equals the current size of the blocked set, then $v$ can ultimately be bypassed.

Otherwise $v$ joins the blocked set.

At the end, every blocked pupil except Nastya represents a person whom Nastya can never pass. If there are $k$ such pupils, then she can pass the remaining $n-1-k$ pupils.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / state-space search | Huge | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the queue and identify Nastya's number, which is the last element of the permutation.
2. For every permission pair $(u,v)$, store $v$ in an adjacency set of $u$.
3. Create a set called `blocked` and initially place Nastya inside it.
4. Process the queue from right to left, starting with the pupil immediately before Nastya.
5. For the current pupil $v$, count how many members of `blocked` appear in $v$'s adjacency set.
6. If this count equals the size of `blocked`, then $v$ can eventually be crossed by Nastya, so do nothing.

The reason is that every currently blocked pupil can move behind $v$, allowing $v$ to become adjacent to Nastya at some point.
7. Otherwise add $v$ to `blocked`.

At least one blocked pupil can never move behind $v$, making $v$ an unavoidable obstacle.
8. After all pupils are processed, let `ans = len(blocked) - 1`.

These are the non-Nastya pupils who must remain ahead of her.
9. Output `(n - 1) - ans`.

### Why it works

The invariant is that after processing a suffix of the queue, `blocked` contains exactly the pupils from that suffix who can never be moved behind Nastya.

When examining a new pupil $v$, every currently blocked pupil must eventually cross $v$ if Nastya is to pass $v$. Such a crossing requires the permission $(v,u)$. If even one required permission is missing, at least one blocked pupil remains permanently ahead of $v$, preventing Nastya from ever reaching $v$. Hence $v$ must also be blocked.

If permissions exist toward every blocked pupil, all of them can be moved behind $v$, so $v$ does not become a permanent obstacle.

The invariant remains true after every step, and once the entire queue is processed, the blocked set contains exactly the pupils whom Nastya cannot pass. The answer is the number of remaining pupils.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    p = list(map(int, input().split()))

    adj = [set() for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].add(v)

    blocked = {p[-1]}  # Nastya

    for v in reversed(p[:-1]):
        cnt = 0
        s = adj[v]

        for u in blocked:
            if u in s:
                cnt += 1

        if cnt != len(blocked):
            blocked.add(v)

    cannot_pass = len(blocked) - 1
    print((n - 1) - cannot_pass)

solve()
```

The adjacency structure stores all permissions originating from each pupil. Membership testing is $O(1)$ on average.

The set `blocked` is the heart of the solution. It contains exactly the pupils that are guaranteed to stay ahead of Nastya. We scan from right to left because the status of a pupil depends only on people closer to Nastya than itself.

A subtle detail is that we compare the count with the current size of `blocked` before potentially inserting the current pupil. Reversing that order would incorrectly make a pupil depend on itself.

Another detail is that the answer is not `len(blocked)`. Nastya herself is always in the blocked set, so we subtract one before computing how many people remain ahead of her.

## Worked Examples

### Sample 1

Input:

```
2 1
1 2
1 2
```

Nastya is pupil 2.

| Current pupil | Blocked before | Has edges to all blocked? | Blocked after |
| --- | --- | --- | --- |
| 1 | {2} | Yes | {2} |

Final blocked set is `{2}`.

`cannot_pass = 0`

Answer = `1 - 0 = 1`.

Nastya can swap directly with pupil 1 and reach the front.

### Sample 2

```
3 3
1 2 3
1 3
1 2
2 3
```

Nastya is pupil 3.

| Current pupil | Blocked before | Has edges to all blocked? | Blocked after |
| --- | --- | --- | --- |
| 2 | {3} | Yes | {3} |
| 1 | {3} | Yes | {3} |

Final blocked set is `{3}`.

`cannot_pass = 0`

Answer = `2`.

Nastya can eventually pass both pupils and move to the front.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each edge is stored once, and each pupil is processed once |
| Space | O(n + m) | Adjacency sets plus the blocked set |

The total input size is at most $n=3\cdot10^5$ and $m=5\cdot10^5$. Linear storage and near-linear processing fit comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    p = list(map(int, input().split()))

    adj = [set() for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].add(v)

    blocked = {p[-1]}

    for v in reversed(p[:-1]):
        cnt = 0
        for u in blocked:
            if u in adj[v]:
                cnt += 1
        if cnt != len(blocked):
            blocked.add(v)

    cannot_pass = len(blocked) - 1
    return str((n - 1) - cannot_pass) + "\n"

# provided sample
assert run("2 1\n1 2\n1 2\n") == "1\n", "sample 1"

# minimum size
assert run("1 0\n1\n") == "0\n", "single pupil"

# no permissions
assert run("4 0\n1 2 3 4\n") == "0\n", "cannot move at all"

# can pass everyone
assert run(
    "4 3\n1 2 3 4\n1 4\n2 4\n3 4\n"
) == "3\n", "moves to front"

# one unavoidable blocker
assert run(
    "4 2\n1 2 3 4\n2 4\n3 4\n"
) == "2\n", "pupil 1 remains ahead"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 1` | `0` | Minimum size |
| No permissions | `0` | Nobody can be passed |
| Everyone points to Nastya | `3` | Nastya reaches the front |
| One missing critical permission | `2` | Detects unavoidable blockers correctly |

## Edge Cases

Consider the queue:

```
4 0
1 2 3 4
```

There are no permissions at all. Processing from right to left gives:

```
blocked = {4}
3 cannot reach all blocked -> add
blocked = {4,3}
2 cannot reach all blocked -> add
blocked = {4,3,2}
1 cannot reach all blocked -> add
blocked = {4,3,2,1}
```

Every pupil becomes blocked. The answer is `0`, which is correct because no swap can ever happen.

Now consider:

```
4 3
1 2 3 4
1 4
2 4
3 4
```

Processing gives:

```
blocked = {4}
3 reaches all blocked
2 reaches all blocked
1 reaches all blocked
```

No additional pupil enters the blocked set. The answer is `3`, meaning Nastya can pass everyone.

Finally consider:

```
4 2
1 2 3 4
2 4
3 4
```

Processing gives:

```
blocked = {4}
3 reaches all blocked
2 reaches all blocked
1 does not reach 4
blocked = {4,1}
```

Pupil 1 becomes an unavoidable obstacle. The answer is `2`, meaning Nastya can pass pupils 2 and 3 but never get ahead of pupil 1. This is exactly the behavior the greedy invariant captures.
