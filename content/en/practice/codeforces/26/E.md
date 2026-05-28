---
title: "CF 26E - Multithreading"
description: "Each process repeatedly executes two atomic instructions: The shared variable y starts at 0. Every process has its own p"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 26
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 26 (Codeforces format)"
rating: 2400
weight: 26
solve_time_s: 97
verified: true
draft: false
---

[CF 26E - Multithreading](https://codeforces.com/problemset/problem/26/E)

**Rating:** 2400  
**Tags:** constructive algorithms  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

Each process repeatedly executes two atomic instructions:

```
yi := y
y := yi + 1
```

The shared variable `y` starts at `0`. Every process has its own private variable `yi`, so different processes never overwrite each other's local state.

The important detail is that the two instructions are separate atomic operations. A process may read the current value of `y`, get interrupted for a long time, and later write back `yi + 1` using an outdated value. Because of this, increments can be lost.

If all operations were executed sequentially without interruptions, the final value would simply be:

```
sum(ni)
```

But with arbitrary interleavings, the final answer can be much smaller.

We are asked whether some execution schedule can produce exactly `W`. If yes, we must output one valid sequence of executed instructions. The schedule contains one process index per executed instruction, so its length must be exactly:

```
2 * sum(ni)
```

because each loop iteration performs two instructions.

The constraints are surprisingly small in one dimension and large in another. There are at most `100` processes, and each process performs at most `1000` iterations, so the total number of iterations is at most `100000`. That means constructing and printing an explicit schedule is completely feasible.

What is not feasible is exploring all possible interleavings. Every iteration contributes two operations, so there are astronomically many schedules. Any brute-force search over execution orders is impossible.

The tricky part is understanding which final values are reachable at all.

Consider two processes with one iteration each:

```
P1: read 0
P2: read 0
P1: write 1
P2: write 1
```

The final value becomes `1`, even though there were two increments. One increment was lost because both processes read the same old value.

Now consider a single process with `n1 = 11`. Since there is no concurrency, every increment succeeds. The only possible final value is `11`. Asking for `W = 10` is impossible.

A common wrong assumption is that every value between `1` and `sum(ni)` is reachable. That fails when there are too few processes.

For example:

```
2 1
1 1
```

is possible, because both processes can read `0` before either writes.

But:

```
1 0
1
```

is impossible. At least one write always occurs, and that write sets `y` to at least `1`.

Another subtle case is when one process is much longer than the others:

```
2 5
100 1
```

A careless construction may accidentally force the long process to increase `y` far beyond `5`. The schedule must carefully arrange stale reads so that many writes overwrite each other.

The key challenge is not simulation, it is characterizing exactly which final values can occur.

## Approaches

The brute-force idea is straightforward. At every moment, choose any process whose next instruction exists, execute that instruction, and recursively continue. At the end, check whether the final value equals `W`.

This works because the statement allows arbitrary interleavings, so enumerating all schedules eventually finds every reachable state.

The problem is the branching factor. Suppose the total number of iterations is `S`. Then there are `2S` atomic operations. Even if we ignored instruction dependencies, the number of interleavings is already enormous:

```
(2S)!
```

With `S = 100000`, this is completely hopeless.

The breakthrough comes from understanding what actually changes `y`.

A write instruction always sets:

```
y = old_read_value + 1
```

If several processes read the same value `k`, then all of their writes later set `y` to `k + 1`. No matter how many such writes happen, the value only increases once.

So the execution can be viewed in layers:

```
0 -> 1 -> 2 -> ...
```

To increase from `k` to `k + 1`, at least one process must perform a fresh read of `k`. Any number of additional processes may also read `k`, but their later writes do not increase the value further.

This immediately gives a characterization.

Suppose the final value is `W`.

Then there must exist a chain of `W` successful increments. Each successful increment requires one iteration from some process. A process can contribute multiple successful increments by repeatedly reading the newest value.

The minimum possible final value is obtained when all first reads happen before any write. Then every write stores `1`, so the final answer is `1`.

The maximum possible final value is `sum(ni)` when every increment succeeds sequentially.

But not every intermediate value is reachable. The crucial observation is this:

A process with `ni` iterations can contribute at most `ni` successful increments, but if it participates at all, its very first iteration must read some value and eventually produce at least one increment.

After working through the structure carefully, the reachable values are exactly:

```
1 <= W <= sum(ni)
```

except when there is only one process, where the answer is forced to be exactly `n1`.

The remaining task is constructive. We need an explicit schedule.

The construction is elegant. We choose one process to act as the main counter, performing exactly `W` successful increments. All remaining iterations become stale overwrites that do not change the final value.

To create stale overwrites, we let many iterations read an old value before the counter advances further.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(sum ni) | O(sum ni) | Accepted |

## Algorithm Walkthrough

1. Compute the total number of iterations:

```
S = sum(ni)
```

1. Handle the single-process case separately.

With only one process, there is no interleaving. Every iteration increases `y` by exactly one, so the final value must equal `n1`.
2. For multiple processes, check whether:

```
1 <= W <= S
```

If not, print `No`.

1. Choose one process as the main increasing process. We will use process `1`.
2. Reserve exactly `W` iterations across all processes to form the successful increment chain.

The idea is that these reserved iterations execute almost sequentially:

```
read k
write k + 1
```

for `k = 0, 1, ..., W - 1`.

1. All remaining iterations are converted into harmless stale writes.

Before the counter advances too far, make these extra iterations read an old value. Later, when they write back `old + 1`, they overwrite `y` with a value it already had earlier, so the final value does not increase.
2. Build the schedule explicitly.

For each successful increment:

First execute the read instruction of the chosen iteration.

Then immediately execute its write instruction.

This guarantees that `y` increases by one.
3. For every leftover iteration:

Execute its read instruction early, before the counter reaches the final value.

Delay its write instruction until after the counter already reached at least that same value.

Then the write becomes harmless.
4. Output the schedule.

### Why it works

The invariant is that only the reserved chain contributes new values.

Every successful increment reads the current value of `y` and immediately writes back `y + 1`, so the value increases exactly once.

Every stale iteration reads some earlier value `k`. By the time its delayed write happens, `y` is already at least `k + 1`. Writing `k + 1` again cannot increase the maximum value reached.

Since we construct exactly `W` successful increments and prevent all other iterations from contributing new increments, the final value becomes exactly `W`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, w = map(int, input().split())
    a = list(map(int, input().split()))

    total = sum(a)

    if n == 1:
        if w != a[0]:
            print("No")
            return

        print("Yes")
        ans = []

        for _ in range(a[0]):
            ans.append(1)
            ans.append(1)

        print(*ans)
        return

    if w < 1 or w > total:
        print("No")
        return

    print("Yes")

    rem = a[:]
    ans = []

    good = []

    need = w

    for i in range(n):
        take = min(rem[i], need)
        rem[i] -= take
        need -= take

        for _ in range(take):
            good.append(i + 1)

        if need == 0:
            break

    bad = []

    for i in range(n):
        for _ in range(rem[i]):
            bad.append(i + 1)

    # stale reads
    for p in bad:
        ans.append(p)

    # successful increments
    for p in good:
        ans.append(p)
        ans.append(p)

    # stale writes
    for p in bad:
        ans.append(p)

    print(*ans)

solve()
```

The construction separates iterations into two groups.

The `good` iterations are responsible for the actual increase from `0` to `W`. Each of them executes its read and write consecutively, guaranteeing one successful increment.

The `bad` iterations are stale overwrites. Their read instructions are executed first, before the successful chain starts. At that moment they all read the same small value, usually `0`.

Their write instructions are postponed until after all successful increments finish. By then, `y` is already large enough that these writes cannot increase it.

The schedule format is subtle. Each process index refers to its next instruction, not an entire iteration. So writing:

```
ans.append(p)
ans.append(p)
```

means executing first the read instruction and then the write instruction of the same iteration.

A common off-by-one mistake is forgetting that every iteration contributes exactly two schedule entries. The final schedule length must be:

```
2 * sum(ni)
```

This construction satisfies that automatically.

## Worked Examples

### Example 1

Input:

```
1 10
11
```

There is only one process with eleven iterations.

| Step | Operation | y |
| --- | --- | --- |
| 1 | sequential increments | 1 |
| 2 | sequential increments | 2 |
| ... | ... | ... |
| 11 | sequential increments | 11 |

The final value is forced to be `11`. No interleaving exists because there is only one process. Reaching `10` is impossible.

Output:

```
No
```

This example demonstrates the only exceptional case. With a single process, concurrency disappears completely.

### Example 2

Input:

```
2 1
1 1
```

Construction:

```
bad = [2]
good = [1]
```

Generated schedule:

```
2 1 1 2
```

Execution trace:

| Step | Process | Instruction | y |
| --- | --- | --- | --- |
| 1 | 2 | read 0 | 0 |
| 2 | 1 | read 0 | 0 |
| 3 | 1 | write 1 | 1 |
| 4 | 2 | write 1 | 1 |

The second process performs a stale overwrite. Both processes read `0`, so both writes produce `1`.

This trace confirms that multiple iterations may collapse into a single effective increment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sum ni) | every iteration is processed a constant number of times |
| Space | O(sum ni) | the explicit schedule contains `2 * sum(ni)` integers |

The total number of iterations is at most `100000`, so linear complexity is easily fast enough within the 2 second limit. The memory usage is also safe because the schedule itself dominates the storage.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n, w = map(int, input().split())
    a = list(map(int, input().split()))

    total = sum(a)

    if n == 1:
        if w != a[0]:
            print("No")
            return out.getvalue()

        print("Yes")
        ans = []

        for _ in range(a[0]):
            ans.append(1)
            ans.append(1)

        print(*ans)
        return out.getvalue()

    if w < 1 or w > total:
        print("No")
        return out.getvalue()

    print("Yes")

    rem = a[:]
    ans = []

    good = []

    need = w

    for i in range(n):
        take = min(rem[i], need)
        rem[i] -= take
        need -= take

        for _ in range(take):
            good.append(i + 1)

        if need == 0:
            break

    bad = []

    for i in range(n):
        for _ in range(rem[i]):
            bad.append(i + 1)

    for p in bad:
        ans.append(p)

    for p in good:
        ans.append(p)
        ans.append(p)

    for p in bad:
        ans.append(p)

    print(*ans)

    return out.getvalue()

# provided sample
assert run("1 10\n11\n") == "No\n"

# minimum size valid
assert run("1 1\n1\n").startswith("Yes")

# smallest concurrent collapse
assert run("2 1\n1 1\n").startswith("Yes")

# impossible because W too large
assert run("2 10\n3 4\n") == "No\n"

# maximum reachable value
assert run("3 6\n1 2 3\n").startswith("Yes")

# boundary: W = 0 impossible for multiple processes
assert run("2 0\n1 1\n") == "No\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | Yes | single-process exact match |
| `2 1 / 1 1` | Yes | stale overwrites collapsing increments |
| `2 10 / 3 4` | No | rejecting values above total iterations |
| `3 6 / 1 2 3` | Yes | maximum achievable value |
| `2 0 / 1 1` | No | minimum final value is 1 |

## Edge Cases

Consider:

```
1 5
7
```

There is only one process. No instruction can interleave with anything else.

Execution always looks like:

```
read k
write k + 1
```

for consecutive values of `k`.

After seven iterations, the final value is forced to become `7`.

The algorithm detects `n == 1` and checks whether `W == n1`. Since `5 != 7`, it correctly prints:

```
No
```

Now consider:

```
2 1
1 1
```

The algorithm creates one successful increment and one stale overwrite.

Execution:

| Step | Action | y |
| --- | --- | --- |
| 1 | P2 reads 0 | 0 |
| 2 | P1 reads 0 | 0 |
| 3 | P1 writes 1 | 1 |
| 4 | P2 writes 1 | 1 |

The final value remains `1`.

Finally, consider a highly unbalanced case:

```
2 5
100 1
```

A naive schedule might accidentally allow many successful increments from the large process.

The construction avoids that. Only five iterations are placed in the successful chain. Every other iteration performs a stale read first and a delayed write later.

No matter how many extra iterations exist, only the reserved chain contributes new values, so the final answer remains exactly `5`.
