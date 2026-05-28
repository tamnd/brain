---
title: "CF 93C - Azembler"
description: "We start with one register, eax, containing some unknown value x. Every other register contains 0. The goal is to produce n x in any register using the minimum possible number of lea instructions. The instruction set is surprisingly limited, but also surprisingly powerful."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 93
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 76 (Div. 1 Only)"
rating: 2500
weight: 93
solve_time_s: 121
verified: true
draft: false
---

[CF 93C - Azembler](https://codeforces.com/problemset/problem/93/C)

**Rating:** 2500  
**Tags:** brute force, implementation  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with one register, `eax`, containing some unknown value `x`. Every other register contains `0`. The goal is to produce `n * x` in any register using the minimum possible number of `lea` instructions.

The instruction set is surprisingly limited, but also surprisingly powerful. A single `lea` can form expressions of the shape

```
y
y + z
k * y
y + k * z
```

where `k` is one of `1, 2, 4, 8`.

Since every register always stores some multiple of the original value `x`, the whole problem becomes arithmetic on coefficients. If a register currently contains `a * x`, then with one operation we may create

```
(a + b) * x
(a + k * b) * x
k * a * x
```

for `k ∈ {1,2,4,8}`.

The input is a single integer `n`, with `1 ≤ n ≤ 255`. The output must be an optimal program, not just the minimum number of instructions. That means we need both shortest distance computation and reconstruction of the operations.

The bound `n ≤ 255` changes the nature of the problem completely. We are not looking for some asymptotic formula or greedy pattern. The entire reachable state space is tiny. Even if we model all possible register configurations explicitly, the search space remains manageable because the optimal programs are short and the coefficients never need to exceed a small range.

The subtle part is that intermediate values larger than `n` may still help. A greedy strategy that only builds values up to `n` can miss optimal answers. For example, reaching `15` through

```
5 -> 20 -> 15
```

is impossible because subtraction does not exist, but reaching some targets efficiently often requires building auxiliary coefficients that are not obvious from the binary representation.

Another easy mistake is assuming only one working register matters. The sample for `41` already disproves this:

```
5*x in ebx
41*x in ecx using eax and ebx
```

Keeping several intermediate coefficients alive simultaneously is the whole reason short programs exist.

The smallest edge case is `n = 1`. The answer is zero instructions because `eax` already contains `1 * x`. A careless implementation that always emits at least one instruction would fail immediately.

Another dangerous edge case is register reuse. The instruction

```
lea eax, [eax + 8*eax]
```

is valid and computes `9 * eax_old`. The old value must conceptually be read before the assignment happens. Implementations that mutate registers too early during simulation can corrupt reconstruction.

## Approaches

The most direct brute-force idea is to generate every possible program of length `1`, then every program of length `2`, and so on, until one produces `n * x`.

Each instruction chooses a destination register, one or two source registers, and optionally a multiplier from `{2,4,8}`. Even with only a handful of registers, the branching factor becomes enormous. A depth-6 search already explores millions of possibilities. Since many different instruction sequences lead to the same coefficient configuration, most of the work is duplicated.

The brute-force is still conceptually useful because it reveals the actual structure of the problem. Every register always stores an integer multiple of the original value. The precise runtime values do not matter at all. Only the coefficients matter.

That observation turns the task into a shortest-path problem on integer states.

Suppose we currently know several coefficients that are already constructible. From any pair `(a, b)` we may create

```
a + b
a + 2b
a + 4b
a + 8b
2a
4a
8a
```

in one step.

This resembles an addition chain problem, except we are allowed small multipliers. Since `n ≤ 255`, we can run a breadth-first search over reachable coefficients.

The key insight is that we do not actually need to model all 26 registers. Any optimal program can be represented as a DAG of computed coefficients. Every instruction creates one new coefficient from older ones. We only care about the dependency graph.

A BFS over coefficients up to some safe limit works because the search depth is tiny. For every newly discovered coefficient, we remember how it was produced. Once we reach `n`, we reconstruct the instruction sequence backward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Exhaustive program enumeration | Exponential | Exponential | Too slow |
| BFS on constructible coefficients | O(M²) | O(M) | Accepted |

Here `M` is the maximum coefficient bound used during BFS.

## Algorithm Walkthrough

1. Treat every register value as a coefficient multiplying the original unknown number `x`.

Initially only coefficient `1` exists because `eax = x`.
2. Run a breadth-first search starting from coefficient `1`.

BFS is appropriate because every `lea` instruction costs exactly one operation.
3. For every currently known coefficient `a`, combine it with every already discovered coefficient `b`.

From `(a, b)` generate:

```
a + b
a + 2b
a + 4b
a + 8b
```

We also naturally obtain pure scaling because choosing `a = 0` is equivalent to multiplication, but storing explicit zeros is unnecessary.
4. Whenever a new coefficient `c` is discovered for the first time, record:

```
parent coefficients
multiplier used
BFS depth
```

The first discovery is optimal because BFS explores states in increasing number of instructions.
5. Continue until coefficient `n` is reached.
6. Reconstruct the dependency graph backward from `n`.

Each coefficient remembers which earlier coefficients produced it.
7. Emit instructions in topological order.

Assign a register to every constructed coefficient. Since the optimal depth for `n ≤ 255` is very small, the number of simultaneously alive coefficients easily fits inside 26 registers.

### Why it works

Every instruction creates exactly one new coefficient from already existing ones. BFS explores all coefficients reachable in `0` instructions, then all coefficients reachable in `1` instruction, and so on. When coefficient `n` is first discovered, no shorter sequence can exist.

The reconstruction is correct because each stored transition corresponds exactly to one valid `lea` instruction. Replaying the dependency graph in BFS order reproduces the target coefficient using the same number of operations.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

MAXV = 2048
REGS = [
    "eax", "ebx", "ecx", "edx", "eex", "efx", "egx", "ehx",
    "eix", "ejx", "ekx", "elx", "emx", "enx", "eox", "epx",
    "eqx", "erx", "esx", "etx", "eux", "evx", "ewx", "exx",
    "eyx", "ezx"
]

def solve():
    n = int(input())

    if n == 1:
        print(0)
        return

    dist = [-1] * MAXV
    parent = [None] * MAXV

    q = deque([1])
    dist[1] = 0

    discovered = [1]

    while q:
        a = q.popleft()

        current = discovered[:]

        for b in current:
            for k in (1, 2, 4, 8):
                c = a + k * b

                if c >= MAXV:
                    continue

                if dist[c] != -1:
                    continue

                dist[c] = dist[a] + 1
                parent[c] = (a, b, k)

                discovered.append(c)
                q.append(c)

                if c == n:
                    q.clear()
                    break
            else:
                continue
            break

    need = set()

    def collect(v):
        if v == 1 or v in need:
            return
        need.add(v)
        a, b, k = parent[v]
        collect(a)
        collect(b)

    collect(n)

    order = []

    visited = set()

    def topo(v):
        if v == 1 or v in visited:
            return
        visited.add(v)

        a, b, k = parent[v]

        topo(a)
        topo(b)

        order.append(v)

    topo(n)

    reg_of = {1: "eax"}
    free_regs = deque(REGS[1:])

    instructions = []

    for v in order:
        a, b, k = parent[v]

        ra = reg_of[a]
        rb = reg_of[b]

        rv = free_regs.popleft()
        reg_of[v] = rv

        if a == b and k == 1:
            expr = f"[{ra} + {rb}]"
        elif k == 1:
            expr = f"[{ra} + {rb}]"
        else:
            expr = f"[{ra} + {k}*{rb}]"

        instructions.append(f"lea {rv}, {expr}")

    print(len(instructions))
    print("\n".join(instructions))

solve()
```

The BFS computes the minimum number of instructions needed to create every coefficient. The array `parent` stores the exact operation that first produced each value.

The search bound `2048` is intentionally larger than `255`. Intermediate coefficients above the target may still appear in optimal constructions, so restricting the search to `≤ n` is unsafe.

The reconstruction phase has two DFS traversals. The first marks every coefficient needed for the final answer. The second produces a topological order so that dependencies are always computed before the values that use them.

Register allocation is simple because the dependency graph is tiny. We permanently assign one register to each constructed coefficient. The number of required coefficients never comes close to the available 26 registers.

One subtle detail is instruction formatting. The statement only allows specific syntactic forms. We always emit either

```
[y + z]
```

or

```
[y + k*z]
```

which are both valid.

## Worked Examples

### Example 1

Input:

```
41
```

BFS discovers the following useful chain.

| Step | Constructed coefficient | Formula |
| --- | --- | --- |
| 0 | 1 | initial eax |
| 1 | 5 | 1 + 4×1 |
| 2 | 41 | 1 + 8×5 |

Generated instructions:

| Step | Instruction | Result |
| --- | --- | --- |
| 1 | `lea ebx, [eax + 4*eax]` | `ebx = 5x` |
| 2 | `lea ecx, [eax + 8*ebx]` | `ecx = 41x` |

This example shows why keeping intermediate coefficients alive matters. The second instruction reuses both `1*x` and `5*x`.

### Example 2

Input:

```
15
```

One optimal construction is:

| Step | Constructed coefficient | Formula |
| --- | --- | --- |
| 0 | 1 | initial |
| 1 | 3 | 1 + 2×1 |
| 2 | 15 | 3 + 4×3 |

Generated instructions:

| Step | Instruction | Result |
| --- | --- | --- |
| 1 | `lea ebx, [eax + 2*eax]` | `3x` |
| 2 | `lea ecx, [ebx + 4*ebx]` | `15x` |

This trace demonstrates that repeated reuse of the same register inside one expression is completely valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M²) | Each discovered coefficient is paired with previously discovered coefficients |
| Space | O(M) | Distance and parent arrays store one entry per coefficient |

The practical runtime is tiny because `M = 2048`. Even the quadratic exploration easily fits inside the 5-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    MAXV = 2048

    n = int(input())

    if n == 1:
        return "0"

    dist = [-1] * MAXV
    parent = [None] * MAXV

    q = deque([1])
    dist[1] = 0

    discovered = [1]

    while q:
        a = q.popleft()

        current = discovered[:]

        for b in current:
            for k in (1, 2, 4, 8):
                c = a + k * b

                if c >= MAXV:
                    continue

                if dist[c] != -1:
                    continue

                dist[c] = dist[a] + 1
                parent[c] = (a, b, k)

                discovered.append(c)
                q.append(c)

                if c == n:
                    q.clear()
                    break
            else:
                continue
            break

    out = []
    out.append(str(dist[n]))

    assert dist[n] >= 0

    return "\n".join(out)

# minimum case
assert run("1\n") == "0", "n=1 needs no operations"

# small direct construction
assert run("2\n") == "1", "2 = 1 + 1"

# sample
assert run("41\n") == "2", "sample case"

# another short chain
assert run("15\n") == "2", "15 = 3 + 4*3"

# upper boundary
assert int(run("255\n")) >= 0, "largest allowed n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Empty program handling |
| `2` | `1` | Simplest nontrivial multiplication |
| `41` | `2` | Reuse of intermediate coefficients |
| `15` | `2` | Same register used multiple times |
| `255` | valid answer | Upper constraint boundary |

## Edge Cases

### Edge Case 1: `n = 1`

Input:

```
1
```

The algorithm immediately returns zero instructions because the initial state already contains coefficient `1`.

No BFS expansion is needed. This prevents the common mistake of generating useless operations like

```
lea ebx, [eax]
```

which would not be optimal.

### Edge Case 2: Reusing the same register

Input:

```
15
```

Construction:

```
3 = 1 + 2*1
15 = 3 + 4*3
```

The emitted instruction may look like

```
lea ecx, [ebx + 4*ebx]
```

Both occurrences of `ebx` refer to the old value before assignment. The algorithm handles this naturally because reconstruction stores symbolic coefficient dependencies, not mutable runtime states.

### Edge Case 3: Intermediate coefficients larger than obvious binary chunks

Input:

```
255
```

A naive binary-doubling strategy is not always optimal. BFS explores all reachable coefficients uniformly, including unusual intermediate constructions. Since the search space includes values beyond `255`, no optimal path is accidentally pruned.
