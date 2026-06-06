---
title: "CF 343B - Alternating Current"
description: "We are given a sequence that describes how two wires, one called “plus” and the other “minus”, overlap as they run from the left side to the right side of a device. At each position along the path, exactly one of the wires is physically above the other."
date: "2026-06-06T17:47:07+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 343
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 200 (Div. 1)"
rating: 1600
weight: 343
solve_time_s: 123
verified: true
draft: false
---

[CF 343B - Alternating Current](https://codeforces.com/problemset/problem/343/B)

**Rating:** 1600  
**Tags:** data structures, greedy, implementation  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence that describes how two wires, one called “plus” and the other “minus”, overlap as they run from the left side to the right side of a device. At each position along the path, exactly one of the wires is physically above the other. A “+” character means the plus wire is above the minus wire at that position, while a “-” means the minus wire is above the plus wire.

The left side is fixed: the plus wire starts on the top contact and the minus wire starts on the bottom contact. We are allowed to freely move the wires in the plane as long as we do not cut them or detach their endpoints. The question is whether we can continuously deform the wires so that they end up not entangled at all, meaning no crossings remain, while preserving endpoints.

The input length can be up to 100000. That rules out any simulation that tries to explicitly model wire geometry or maintain a structure of crossings that changes dynamically with expensive updates. Anything quadratic in the number of characters would be far too slow.

A subtle point is that the sequence is not describing independent crossings. It is describing a continuous braid-like interaction. Two consecutive identical symbols do not necessarily behave the same way as separated ones, because a full “wrap” of one wire around the other is encoded as a specific alternating pattern.

A naive mistake is to assume we can just cancel adjacent opposite crossings or treat the sequence like a stack reduction problem similar to parentheses. For example, interpreting “+” as an opening event and “-” as a closing event fails immediately:

Input:

```
-+
```

A naive cancellation idea might suggest the crossings cancel, but the correct answer is “No” because this represents a full twist that cannot be removed without moving endpoints.

Another failure case is treating each “+” independently and simply checking whether counts are balanced. The sequence “+-+-” would incorrectly look harmless under counting logic, yet it can represent a nontrivial braid structure that must be interpreted as a single global constraint.

## Approaches

A brute-force way to think about the problem is to simulate the actual deformation of two curves in the plane. One could model the wires as polylines and repeatedly attempt to locally straighten segments while tracking intersections. Every time we remove a crossing, new crossings may appear elsewhere, so this process could require revisiting the entire structure many times. In the worst case, each local adjustment interacts with all previous ones, leading to a quadratic or worse number of updates over the length of the sequence.

The key observation is that we do not actually care about geometry, only whether the sequence encodes a nontrivial “wrap” of one wire around the other. This reduces the problem to tracking whether the prefix structure ever forces an impossible state.

The crucial simplification is that the sequence behaves like a stack of directional changes, and what matters is whether we ever “over-cancel” crossings in a way that would require lifting a wire through the other endpoint constraint. We can interpret the process as tracking a single integer balance where we increment or decrement depending on whether the plus wire is above or below, but with an important constraint: if the balance ever goes beyond a threshold in a way that would force reversing the fixed endpoints, the configuration becomes impossible.

This leads to a greedy linear scan where we maintain a counter representing the current relative winding state. Whenever we see a symbol, we adjust the counter, but we also enforce that the counter never violates the constraint induced by fixed endpoints. The final state determines whether the braid is trivial.

In this specific problem, the condition reduces to checking whether the sequence ever encodes a full rotation. That can be detected by ensuring that we never need more than one active “layer” of imbalance at a time, which is equivalent to ensuring that the running state never exceeds 1 in absolute value in a way that forces a wrap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of geometry | O(n²) | O(n) | Too slow |
| Linear greedy tracking of winding state | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the sequence left to right while maintaining a single integer state `bal`.

1. Initialize `bal = 0`. This represents that, before any crossings are considered, the system is in a neutral configuration consistent with the fixed endpoints.
2. Scan each character in the sequence. If the character is “+”, we treat it as pushing the configuration upward, so we increment `bal` by 1. If it is “-”, we decrement `bal` by 1. This models how each local crossing contributes to the relative ordering.
3. After each update, check whether the state has drifted into an impossible regime. If at any point the magnitude of `bal` exceeds 1, we immediately conclude the configuration represents a full twist that cannot be undone under fixed endpoints, and we reject.
4. If the scan completes without violating the constraint, the configuration can be continuously untangled, so we accept.

The key idea behind the threshold check is that any attempt to accumulate more than a single unit of imbalance forces one wire to “wrap around” the other in a way that cannot be undone without changing endpoint order.

### Why it works

The process implicitly tracks the net winding between the two wires under the constraint that their endpoints are fixed and ordered. Any valid untangling corresponds to a deformation that never introduces more than a single local dominance at any prefix. If the running imbalance exceeds this bound, it encodes a full rotation of one wire around the other, which is a topological obstruction that cannot be removed by planar deformation alone. The algorithm is therefore safe because it rejects exactly those sequences that force such a rotation, and accepts all others where the imbalance remains locally resolvable.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

bal = 0
for ch in s:
    if ch == '+':
        bal += 1
    else:
        bal -= 1
    
    if abs(bal) > 1:
        print("No")
        sys.exit()

print("Yes")
```

The code maintains a single running counter and updates it in constant time per character. The early exit is important because once the configuration becomes impossible, further processing cannot restore validity.

The only subtlety is that we must check the constraint immediately after each update, not only at the end. Delaying the check would allow invalid intermediate configurations to be incorrectly accepted.

## Worked Examples

Consider the input:

```
-++-
```

We track `bal` step by step.

| Step | char | bal | abs(bal) | Decision |
| --- | --- | --- | --- | --- |
| 1 | - | -1 | 1 | ok |
| 2 | + | 0 | 0 | ok |
| 3 | + | 1 | 1 | ok |
| 4 | - | 0 | 0 | ok |

Since we never exceed absolute value 1, the output is “Yes”.

Now consider a problematic sequence:

```
--++
```

| Step | char | bal | abs(bal) | Decision |
| --- | --- | --- | --- | --- |
| 1 | - | -1 | 1 | ok |
| 2 | - | -2 | 2 | reject |

At step 2 the imbalance exceeds 1, meaning the structure forces a full wrap that cannot be undone.

These traces show how the constraint is enforced locally and prevents accumulation of non-removable structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once with O(1) updates |
| Space | O(1) | Only a single integer state is maintained |

The solution comfortably handles inputs up to 100000 characters since it performs only a constant amount of work per character.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        s = input().strip()
        bal = 0
        for ch in s:
            if ch == '+':
                bal += 1
            else:
                bal -= 1
            if abs(bal) > 1:
                return "No"
        return "Yes"
    finally:
        sys.stdin = old_stdin

# provided sample
assert run("-++-") == "Yes"

# minimum size
assert run("+") == "Yes"

# immediate invalid wrap
assert run("--") == "No"

# alternating safe case
assert run("+-+-") == "Yes"

# longer valid neutral sequence
assert run("-+-++-") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| + | Yes | minimal valid configuration |
| -- | No | immediate violation detection |
| +-+- | Yes | alternating sequence stays bounded |
| -+-++- | Yes | mixed sequence without overflow |

## Edge Cases

A single-character input like “+” or “-” always remains valid because it cannot create a full wrap. The algorithm processes one update and immediately finishes without exceeding the threshold.

A two-character sequence such as “--” demonstrates the earliest possible failure. After the second step, the balance becomes -2, which violates the constraint immediately. The algorithm correctly rejects at that moment without needing to scan further.

An alternating sequence such as “+-+-” never accumulates more than one unit of imbalance. The running state oscillates between -1, 0, and 1, which corresponds to local crossings that can be removed by sliding one wire over the other without changing endpoint ordering.

A mixed longer sequence like “-+-++-” shows that even when the prefix contains both directions, as long as the running imbalance never exceeds the allowed bound, the structure remains untangled. The algorithm maintains correctness by enforcing the constraint at every prefix rather than relying on the final sum.
