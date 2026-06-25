---
title: "CF 106368A - Forgetful Shustrik and the Remote Control"
description: "We have a calculator whose screen starts with a value A. The calculator has a fixed number M, and every button press applies one of four transformations: add M, subtract M, multiply by M, or replace the current value with its remainder after division by M."
date: "2026-06-25T08:14:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106368
codeforces_index: "A"
codeforces_contest_name: "Innopolis Open 2025-2026. Final round"
rating: 0
weight: 106368
solve_time_s: 50
verified: true
draft: false
---

[CF 106368A - Forgetful Shustrik and the Remote Control](https://codeforces.com/problemset/problem/106368/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a calculator whose screen starts with a value `A`. The calculator has a fixed number `M`, and every button press applies one of four transformations: add `M`, subtract `M`, multiply by `M`, or replace the current value with its remainder after division by `M`. The goal is not to reach an exact value. We only need the final screen value to have the same remainder as `B` when divided by `N`. The task is to output the shortest sequence of button presses that achieves this, or report that it is impossible.

The values of `A` and `M` can be as large as `10^9`, but `N` is at most `2 * 10^6`. This immediately rules out storing actual calculator values because they can grow extremely large after multiplications. We need a state representation based on remainders, and the number of states must be close to `N` to fit the limit. A solution doing something like trying all possible values up to `M` is impossible because `M` has no useful small bound.

The difficult edge cases come from the `%` operation. It does not behave like the other operations when we only know the value modulo `N`, because `% M` depends on the value modulo `M`.

For example:

```
A = 5, M = 6, B = 1, N = 6
```

The answer is `-1`. A careless implementation that only tracks values modulo `N` might think the `%` operation can always create residue `5 mod 6`, but the calculator value after `%` must be in the range `[0, M - 1]`, and here the reachable residues never include `1`.

Another important case is when the multiplication has happened before `%`:

```
A = 5, M = 9, B = 1, N = 8
```

One optimal sequence is:

```
*%+
```

After `*`, the value becomes `45`, which is divisible by `M`, so `%` produces `0`, not `A mod M`. If an implementation assumes `%` always gives the original value modulo `M`, it will miss valid paths.

## Approaches

A direct brute force approach would simulate every possible sequence of button presses. Since there are four choices at every step, a depth `d` search explores up to `4^d` sequences. Even though the answer is guaranteed to be at most `N`, with `N` reaching two million this approach is far beyond what is possible.

The useful observation is that we never need the full calculator value. We only need the value modulo `N`, plus enough information to predict what `%` will do.

Let the current value be `X`. We track two things:

The first is `X mod N`, because this tells us whether we have already reached the required condition.

The second is `X mod M`, because `%` replaces `X` with exactly this remainder.

The surprising part is that `X mod M` has only two possible values during the whole process. Initially it is `A mod M`. Adding or subtracting `M` does not change it. Multiplying by `M` makes it `0`. The `%` operation keeps the same value modulo `M`, because the new number is already equal to the old remainder.

So every state can be represented as:

```
(current value modulo N, current value modulo M is A mod M or 0)
```

This gives at most `2N` states. Every operation becomes a normal graph edge, and the shortest sequence is found with breadth first search.

The brute-force search fails because it explores sequences. The observation above converts the problem into finding the shortest path in a small graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4^N) | O(4^N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build a graph implicitly where every state is a pair `(r, t)`. Here `r` is the current value modulo `N`, and `t` tells whether the current value modulo `M` is the original value `A mod M` or zero.
2. Start BFS from `(A mod N, 0)`. The flag is initially zero because before any multiplication happens, the value modulo `M` is still `A mod M`.
3. For each popped state, generate the four possible operations.

The `+` operation changes only the remainder modulo `N`:

```
r -> (r + M) mod N
```

The flag stays the same because adding `M` does not change the remainder modulo `M`.
4. Apply the `-` operation similarly:

```
r -> (r - M) mod N
```

Again, the modulo `M` remainder is unchanged.
5. Apply multiplication:

```
r -> (r * M) mod N
```

The new flag becomes one because the value is now divisible by `M`.
6. Apply `%`.

If the flag is zero, the new value is `A mod M`. If the flag is one, the new value is zero. The flag itself does not change.
7. Stop BFS when a state with remainder `B` is reached. Because BFS explores states by increasing distance, the first such state gives the shortest sequence.
8. Store the previous state and the operation used to reach every new state. Follow these links backwards from the answer state to reconstruct the operation sequence.

Why it works:

The BFS graph contains every possible calculator situation compressed into an equivalent state. Two calculator values with the same modulo `N` remainder and the same modulo `M` remainder always have identical future behavior for all four operations. Since the second component can only be `A mod M` or `0`, the graph contains all relevant possibilities. BFS finds the shortest path in this complete state graph, so the reconstructed sequence is minimal.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    A, M, B, N = map(int, input().split())

    base = A % M

    total = 2 * N
    parent = [-1] * total
    parent_op = [''] * total

    def get_id(flag, rem):
        return flag * N + rem

    start = get_id(0, A % N)

    q = deque([start])
    parent[start] = start

    answer = -1

    while q:
        cur = q.popleft()
        flag = cur // N
        rem = cur % N

        if rem == B:
            answer = cur
            break

        nxt = [
            (flag, (rem + M) % N, '+'),
            (flag, (rem - M) % N, '-'),
            (1, (rem * M) % N, '*'),
            (flag, base % N if flag == 0 else 0, '%')
        ]

        for nf, nr, op in nxt:
            nid = get_id(nf, nr)
            if parent[nid] == -1:
                parent[nid] = cur
                parent_op[nid] = op
                q.append(nid)

    if answer == -1:
        print(-1)
        return

    path = []
    while answer != start:
        path.append(parent_op[answer])
        answer = parent[answer]

    path.reverse()

    print(len(path))
    if path:
        print(''.join(path))

if __name__ == "__main__":
    solve()
```

The code stores each state as an integer. States with flag `0` occupy indices `0` through `N-1`, and states with flag `1` occupy indices `N` through `2N-1`. This keeps the BFS arrays compact and avoids tuples in the hot loop.

The transition list directly follows the four calculator operations. The `%` transition is the only one requiring the extra flag. A common mistake is to change the flag after `%`, but the remainder modulo `M` stays the same because the result of `%` is already that remainder.

The parent arrays allow reconstruction without storing complete strings in the BFS queue. This matters because the graph can contain up to four million states in the largest cases.

## Worked Examples

For the first sample:

```
1 3 2 5
```

A shortest path is `+*`.

| Step | State flag | Value mod N | Operation |
| --- | --- | --- | --- |
| 0 | original | 1 | start |
| 1 | original | 4 | + |
| 2 | zero | 2 | * |

After the multiplication, the flag changes because the calculator value becomes divisible by `M`. The final remainder is `2`, which matches the target.

For the second sample:

```
6 7 2 4
```

| Step | State flag | Value mod N | Operation |
| --- | --- | --- | --- |
| 0 | original | 2 | start |

The initial value already has the desired remainder, so BFS immediately returns an empty sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | There are at most `2N` states and four transitions per state. |
| Space | O(N) | BFS queues and parent arrays store a constant amount of data per state. |

The maximum value of `N` is two million, so the graph has at most four million states. The algorithm avoids dependence on the size of `A` or `M`, which is what makes it fit the constraints.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    A, M, B, N = map(int, sys.stdin.readline().split())

    base = A % M
    total = 2 * N
    parent = [-1] * total
    parent_op = [''] * total

    def gid(flag, rem):
        return flag * N + rem

    start = gid(0, A % N)
    q = deque([start])
    parent[start] = start
    ans = -1

    while q:
        cur = q.popleft()
        flag = cur // N
        rem = cur % N

        if rem == B:
            ans = cur
            break

        for nf, nr, op in [
            (flag, (rem + M) % N, '+'),
            (flag, (rem - M) % N, '-'),
            (1, (rem * M) % N, '*'),
            (flag, base % N if flag == 0 else 0, '%')
        ]:
            nxt = gid(nf, nr)
            if parent[nxt] == -1:
                parent[nxt] = cur
                parent_op[nxt] = op
                q.append(nxt)

    if ans == -1:
        out = "-1"
    else:
        res = []
        while ans != start:
            res.append(parent_op[ans])
            ans = parent[ans]
        res.reverse()
        out = str(len(res)) + ("\n" + ''.join(res) if res else "")

    sys.stdin = old
    return out

assert run("1 3 2 5\n") == "2\n+*", "sample 1"
assert run("6 7 2 4\n") == "0", "sample 2"

assert run("5 6 1 6\n") == "-1", "impossible case"
assert run("0 6 3 7\n") == "3\n---", "negative moves are useful"
assert run("5 9 1 8\n") == "3\n*%+", "multiplication changes modulo M state"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 2 5` | `2` operations | Basic shortest path reconstruction |
| `6 7 2 4` | `0` operations | Already satisfying the condition |
| `5 6 1 6` | `-1` | Detecting unreachable states |
| `0 6 3 7` | `3` operations | Repeated subtraction and boundary residues |
| `5 9 1 8` | `3` operations | Correct handling of `%` after `*` |

## Edge Cases

When the starting value already satisfies the condition, BFS must return immediately. For input:

```
6 7 2 4
```

the initial remainder is `6 mod 4 = 2`, which equals `B`, so the empty sequence is the shortest possible answer.

When `%` is used after multiplication, the modulo `M` state is zero. For:

```
5 9 1 8
```

the sequence `*%+` works. The multiplication changes the hidden modulo `M` value to zero, `%` keeps the screen at zero, and `+` moves the remainder to the target. Tracking only `A mod M` would miss this path.

When the answer does not exist, BFS explores every reachable compressed state and never reaches a remainder of `B`. For:

```
5 6 1 6
```

all possible states are exhausted without finding residue `1`, so the algorithm correctly prints `-1`.
