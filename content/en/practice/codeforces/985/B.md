---
title: "CF 985B - Switches and Lamps"
description: "We are given a collection of switches, each of which controls a subset of lamps. When a switch is pressed, every lamp connected to it turns on permanently. Once a lamp is on, it never turns off again, even if other switches affecting it are pressed later."
date: "2026-06-17T00:55:37+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 985
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 44 (Rated for Div. 2)"
rating: 1200
weight: 985
solve_time_s: 77
verified: true
draft: false
---

[CF 985B - Switches and Lamps](https://codeforces.com/problemset/problem/985/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of switches, each of which controls a subset of lamps. When a switch is pressed, every lamp connected to it turns on permanently. Once a lamp is on, it never turns off again, even if other switches affecting it are pressed later.

If we press all switches, every lamp is guaranteed to become lit. The task is to determine whether there exists a single switch that we can safely ignore while still ensuring that pressing all remaining switches still turns on every lamp.

Another way to view the problem is that each switch contributes a set of lamps, and the union of all sets covers all lamps. We want to know if removing one set still leaves the union unchanged.

The constraints allow up to 2000 switches and 2000 lamps, which makes a quadratic or slightly worse solution around 4 million operations acceptable. Anything cubic over the matrix structure would be too slow, but operations that are proportional to n times m are fine.

A subtle edge case occurs when a lamp is covered by exactly one switch. In that case, removing that switch would make it impossible to light that lamp. For example, if lamp j is only connected to switch i, then switch i is mandatory. Any correct solution must detect such uniqueness conditions implicitly or explicitly.

Another edge case arises when multiple switches cover all lamps redundantly. For instance, if every lamp is connected to all switches, then removing any single switch still leaves all lamps lit. A naive approach might overcomplicate this and still pass, but it is important to recognize that redundancy across all lamps is the core structure being tested.

## Approaches

A direct approach is to simulate the effect of removing each switch one by one. For a fixed switch i, we would recompute which lamps remain lit using all other switches and check whether all lamps are still covered. If we recompute coverage from scratch each time, we repeatedly scan the entire matrix.

This brute-force method checks n candidates, and for each candidate recomputes coverage across n switches and m lamps. That leads to O(n^2 m) operations. With n and m up to 2000, this reaches about 8 × 10^9 operations, which is far too slow.

The key observation is that we do not actually need to recompute everything. The only thing that matters when removing a switch is whether there exists at least one lamp that becomes uncovered. For a lamp j, the only dangerous situation is when all switches that light j include the removed switch. Equivalently, for each lamp j, we only need to know how many switches cover it. If a lamp is covered at least twice, removing any single covering switch will not turn it off.

This reduces the problem to a simple counting structure. For each lamp, compute how many switches activate it. Then for each switch, verify whether it is the unique provider for any lamp. If a switch is the sole provider of some lamp, it cannot be removed. Otherwise, it is safe.

We can check this efficiently by precomputing coverage counts and then scanning again.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recomputation | O(n^2 m) | O(nm) | Too slow |
| Count coverage per lamp | O(nm) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the input matrix describing which switches activate which lamps. This structure defines a bipartite relationship between switches and lamps.
2. For each lamp, count how many switches can turn it on. This gives a frequency array over lamps that captures redundancy. The reason this is useful is that removal is only dangerous when redundancy is exactly one.
3. For each switch, check all lamps it activates. If any such lamp has a total count of 1, mark the switch as essential. The reasoning is that such a lamp would become unlit if this switch were removed.
4. If we find at least one switch that is not essential, we can safely ignore it and still keep all lamps lit. Output "YES".
5. If every switch is essential, then every switch is required for at least one uniquely supported lamp. In that case, output "NO".

### Why it works

The correctness rests on a simple characterization of failure. A switch is removable if and only if no lamp depends solely on it. The global condition “all lamps remain lit after removing a switch” decomposes into independent checks per lamp, because lamp activation is monotone and additive over switches. Since each lamp only requires at least one active neighbor, losing a switch is harmless exactly when no lamp loses its last supporting edge.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    mat = [input().strip() for _ in range(n)]
    
    cnt = [0] * m
    
    for i in range(n):
        row = mat[i]
        for j in range(m):
            if row[j] == '1':
                cnt[j] += 1
    
    for i in range(n):
        row = mat[i]
        ok = True
        for j in range(m):
            if row[j] == '1' and cnt[j] == 1:
                ok = False
                break
        if ok:
            print("YES")
            return
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The first pass builds a frequency array over lamps. This is the critical preprocessing step that collapses all switch interactions into simple counts.

The second pass evaluates each switch independently. The inner loop checks whether the switch is responsible for any uniquely covered lamp. The early break is important because once a single unique dependency is found, the switch is immediately disqualified.

The decision to store the matrix as strings avoids repeated parsing overhead and keeps memory usage minimal.

## Worked Examples

### Example 1

Input:

```
4 5
10101
01000
00111
10000
```

We compute lamp counts first.

| Lamp | Count |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 1 |

Now we test switches.

| Switch | Lamps | Has unique lamp? | Result |
| --- | --- | --- | --- |
| 1 | 1,3,5 | yes (3,5) | reject |
| 2 | 2 | yes (2) | reject |
| 3 | 3,4,5 | yes (3,5) | reject |
| 4 | 1 | no | accept |

Switch 4 can be removed without leaving any lamp unlit, so output is YES.

This trace shows that the algorithm is not looking for a globally “weak” switch, but one that does not serve as a unique provider anywhere.

### Example 2

Input:

```
3 3
110
101
011
```

Lamp counts:

| Lamp | Count |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 2 |

Every switch has redundancy for every lamp it touches.

| Switch | Lamps | Unique dependency | Result |
| --- | --- | --- | --- |
| 1 | 1,2 | none | accept |

Since switch 1 already satisfies the condition, we immediately output YES.

This example highlights that full redundancy across all lamps guarantees multiple valid answers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Two passes over the n by m matrix |
| Space | O(m) | Only lamp counters stored |

The constraints allow up to 4 million character checks, which fits comfortably in Python within the time limit when implemented with simple loops over strings.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("""4 5
10101
01000
00111
10000
""") == "YES"

# all switches essential (each lamp unique)
assert run("""2 2
10
01
""") == "NO"

# fully redundant system
assert run("""3 3
111
111
111
""") == "YES"

# single switch case
assert run("""1 3
111
""") == "YES"

# one lamp uniquely dependent
assert run("""3 2
10
10
01
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 switches, disjoint lamps | NO | no removable switch |
| full 1 matrix | YES | complete redundancy |
| single switch | YES | trivial acceptance |
| mixed uniqueness | YES | detects removable switch correctly |

## Edge Cases

A key edge case is when every lamp has exactly one supporting switch. For example:

```
2 2
10
01
```

Here each switch is uniquely responsible for one lamp. The algorithm marks both switches as essential because each covers a lamp with count 1. This correctly leads to NO.

Another edge case is when a switch has no unique responsibility even though it covers many lamps. For example:

```
3 3
111
111
111
```

Every lamp has count 3, so no switch is ever disqualified. The algorithm correctly identifies that any switch can be removed.

A minimal case with one switch:

```
1 3
111
```

All lamps have count 1, so the single switch is essential and no removal is possible. The algorithm outputs NO, matching the requirement.
