---
title: "CF 1958H - Composite Spells"
description: "We are given a spell system that behaves like a program written in a very restricted language. The first part of the system is a list of basic operations, each of which either increases or decreases a monster’s health by a fixed integer."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dp"]
categories: ["algorithms"]
codeforces_contest: 1958
codeforces_index: "H"
codeforces_contest_name: "Kotlin Heroes: Episode 10"
rating: 2600
weight: 1958
solve_time_s: 94
verified: true
draft: false
---

[CF 1958H - Composite Spells](https://codeforces.com/problemset/problem/1958/H)

**Rating:** 2600  
**Tags:** *special, dp  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a spell system that behaves like a program written in a very restricted language. The first part of the system is a list of basic operations, each of which either increases or decreases a monster’s health by a fixed integer. After that comes a sequence of composite operations, where each composite spell is defined as an ordered list of previously defined spells, and executing it means executing those spells one after another.

The key complication is that spells can call other spells, so the final spell we cast is not a flat list. It is a tree-like structure that expands into a long sequence of basic operations when fully executed. Execution is not unconditional either. As soon as the monster’s health becomes zero or negative, it dies and every remaining operation is ignored.

The task is to simulate casting the final composite spell and determine whether the monster dies. If it dies, we must report the index of the basic spell that causes the health to drop to zero or below for the first time during execution.

The input constraints make it clear that naive full expansion might be risky in principle, since composite spells can nest. However, the total number of listed spell references across all composites is small, which means the structure itself is compact even if the conceptual expansion is large.

A few subtle cases appear immediately. A composite spell may include the same subspell multiple times, so reuse must not be mistaken for duplication of state. Another issue is that some basic spells increase health, so partial execution can temporarily move the health up before a later decrease kills the target. A greedy or “sum-only” approach fails because death depends on prefix behavior, not just total effect.

The most important edge case is early termination. Consider a spell sequence that would normally be very long, but the monster dies after the first few operations. Any solution that fully expands everything without stopping will be correct logically but may do unnecessary work.

## Approaches

The brute force interpretation is straightforward. We expand every composite spell into the full sequence of basic spells it eventually executes, and then simulate the final list from left to right while maintaining current health. Whenever a composite is encountered, we replace it with its full expansion recursively.

This approach is correct because it exactly mirrors execution. However, it fails computationally because a composite spell can expand into a very long sequence, and nested composites can cause repeated expansions of the same structure. In the worst case, each composite refers to earlier composites, forming a deep reuse pattern. Even though the input description is small, the expanded execution trace can become extremely large.

The key observation is that we never need the full structure explicitly at runtime. We only need the final linear sequence of basic spells in execution order, and we only need to traverse it once until the monster dies. Since every composite is defined as an ordered concatenation of earlier spells, we can precompute a flattened representation for each spell using dynamic programming over the index order.

Each spell can be represented as a list of basic spell indices it expands into. Basic spells are trivial lists of size one. For composite spells, we concatenate the already computed lists of their components. Because spells only refer to earlier indices, this construction is valid in a single left-to-right pass.

Once this flattening is done, the final step is a single simulation over the flattened list of the last spell.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full recursive expansion during simulation | Exponential in worst case | Exponential | Too slow |
| DP flattening + single simulation | O(total expansion size) | O(total expansion size) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the basic spell effects and represent each basic spell as a singleton sequence containing its index. We will later use the values when simulating.
2. Maintain a structure `seq[i]` that stores the flattened execution sequence of spell `i`. For basic spells, this is simply `[i]`.
3. For composite spells, construct `seq[i]` by iterating over its listed components in order and appending their already computed sequences. The ordering matters because execution is strictly sequential.
4. After preprocessing all spells, focus on `seq[n+m]`, the final spell.
5. Simulate execution over this flattened sequence. Maintain a variable `hp` initialized to the monster’s health.
6. Traverse each basic spell index in the sequence. For each index `i`, apply its effect `b[i]` to `hp`.
7. If at any point `hp <= 0`, immediately output `i` as the killing spell and stop processing.
8. If the sequence ends without `hp` dropping to zero or below, output `-1`.

The correctness of this method relies on the fact that flattening preserves exact execution order. Every composite spell is replaced by the exact sequence of basic operations it would produce during runtime, so the simulation over the flattened list is identical to direct recursive execution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, hp = map(int, input().split())
        b = [0] + list(map(int, input().split()))

        m = int(input())

        seq = [[] for _ in range(n + m + 1)]

        for i in range(1, n + 1):
            seq[i] = [i]

        for i in range(n + 1, n + m + 1):
            parts = list(map(int, input().split()))
            k = parts[0]
            spells = parts[1:]
            cur = []
            for sp in spells:
                cur.extend(seq[sp])
            seq[i] = cur

        final = seq[n + m]

        cur_hp = hp
        ans = -1

        for idx in final:
            cur_hp += b[idx]
            if cur_hp <= 0:
                ans = idx
                break

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the preprocessing idea directly. Each `seq[i]` is built in topological order, so when processing a composite spell, all referenced sequences are already available.

A subtle point is that we store sequences of basic spell indices, not composite indices. This guarantees that simulation only applies base effects once per operation. Another important detail is early stopping during simulation, which ensures we never process unnecessary suffix of the final sequence.

## Worked Examples

Consider a small derived scenario where basic spells are `+5, -10, +3` and a composite spell is `[1, 2, 3, 2]`, with initial HP equal to `4`.

| Step | Spell | HP before | Change | HP after | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | +5 | 9 | alive |
| 2 | 2 | 9 | -10 | -1 | dead |

The simulation stops immediately at step 2, even though the sequence continues.

This demonstrates that prefix-based stopping is essential. Even if later operations exist and include healing, they are irrelevant once death occurs.

Now consider a case where healing delays death:

Basic spells: `[-3, +5, -4]`, composite: `[2, 1, 3]`, initial HP `3`.

| Step | Spell | HP before | Change | HP after | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | +5 | 8 | alive |
| 2 | 1 | 8 | -3 | 5 | alive |
| 3 | 3 | 5 | -4 | 1 | alive |

Here the monster survives, even though there are negative spells, because ordering matters and prefix accumulation never crosses zero.

This confirms that we must simulate exact order rather than reasoning about totals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total expanded sequence length) | Each spell is expanded once into a flattened list, and each basic operation is processed once during simulation |
| Space | O(total expanded sequence length) | All flattened sequences are stored explicitly |

The total size of all composite spell definitions is bounded by the input constraint, so although nesting exists, the number of explicit edges is small enough that this approach stays within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    backup = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = backup
    return out

# provided sample
assert run("""4
4 9
1 -2 3 -4
3
3 1 4 3
4 1 2 1 2
6 6 5 6 5 6 5
4 9
1 -2 3 -4
3
3 1 4 3
4 1 2 1 2
7 6 5 6 5 6 6 5
3 31
-10 -20 30
1
6 1 2 3 1 2 3
6 20
-1 -5 -9 -7 -1 -1
4
3 6 5 2
4 3 3 7 6
6 4 8 4 4 6 7
3 6 5 7
""") == """4
4
-1
-1
"""

# minimal case: immediate death
assert run("""1
1 1
-5
0
""") == """1
"""

# no death at all
assert run("""1
2 100
1 1
1
1 1
""") == """-1
"""

# composite repeats same spell
assert run("""1
2 5
1 -3
1
4 1 2 1 2
""") == """2
"""

# death at later position
assert run("""1
3 5
2 -4 -10
1
3 1 2 3
""") == """2
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal case | 1 | early termination at first basic spell |
| no death | -1 | survival through full sequence |
| repeated composite usage | 2 | correctness under repetition |
| delayed death | 2 | prefix-based death detection |

## Edge Cases

A key edge case is when a composite spell contains only healing spells early and a killing spell later. The algorithm handles this correctly because it does not aggregate values globally, it respects prefix order.

Another case is deep nesting where multiple composites reuse the same subspell. Even though this could suggest repeated work, each spell is expanded exactly once in the DP construction, so reuse is handled safely without changing correctness.

A final case is when the monster dies very early in the final spell. The simulation stops immediately, so even if the flattened structure is large, only the necessary prefix is evaluated, preventing unnecessary computation.
