---
title: "CF 105925A - Ambiguous Schr\u00f6dinger Cat"
description: "We are given a system with two binary pieces of information: whether a box is open or closed, and the actual internal state of a cat inside it. The first value, C, describes observability. If the box is closed, the state of the cat cannot be observed externally."
date: "2026-06-21T11:58:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105925
codeforces_index: "A"
codeforces_contest_name: "SBC Brazilian Phase Zero 2025"
rating: 0
weight: 105925
solve_time_s: 47
verified: true
draft: false
---

[CF 105925A - Ambiguous Schr\u00f6dinger Cat](https://codeforces.com/problemset/problem/105925/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system with two binary pieces of information: whether a box is open or closed, and the actual internal state of a cat inside it.

The first value, C, describes observability. If the box is closed, the state of the cat cannot be observed externally. If the box is open, the state becomes fully observable.

The second value, G, describes the true internal state of the cat, alive or dead. However, this value only becomes meaningful in terms of output when the box is open, since only then it is possible to confirm the state directly.

The task is to decide what can be said about the cat from an external observer’s point of view. If the box is closed, both possibilities remain valid regardless of the hidden value, so the system remains ambiguous. If the box is open, the observer can directly determine whether the cat is alive or dead from G.

The input size is constant, consisting of only two bits of information, so there are no algorithmic constraints that require optimization beyond constant time evaluation. Any approach beyond direct case analysis would be unnecessary overhead.

A common mistake would be to always trust G regardless of C. For example, if the input is C = 1 and G = 0, one might incorrectly output that the cat is dead. This is wrong because when the box is closed, the observer has no access to G, so both outcomes remain indistinguishable.

Another mistake is to ignore G entirely and always output ambiguity. For example, C = 0 and G = 1 must produce a definite answer, since opening the box collapses the uncertainty.

## Approaches

The brute-force interpretation is to simulate the idea of observability directly: consider both possible interpretations of the system when the box is closed, and only one interpretation when it is open. When C = 1, we would treat the cat as potentially alive and potentially dead simultaneously, since no observation is possible. When C = 0, we would simply read G and output the corresponding state.

This brute-force reasoning works but is conceptually redundant. The branching over “possible realities” when the box is closed is unnecessary because both branches always remain valid regardless of G. The observation that C completely controls whether G is readable reduces the problem to a simple conditional rule.

Once we recognize that C acts as a gate on whether G matters, the entire problem collapses into a two-case decision.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Too slow in structure, unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers C and G. These represent observability and the hidden state respectively.
2. Check whether C equals 1, meaning the box is closed. In this case, the observer cannot distinguish between alive and dead regardless of G, so the output must reflect uncertainty.
3. If C equals 0, the box is open, so the hidden value G becomes fully observable. In this case, map G directly to the final answer: 1 corresponds to alive, and 0 corresponds to dead.
4. Print the resulting state string.

### Why it works

The correctness comes from the fact that C partitions the problem into two regimes with fundamentally different information access. When C = 1, no observation can reduce uncertainty, so both states remain valid interpretations simultaneously. When C = 0, the system reveals G completely, making the output deterministic. There is no interaction between multiple inputs beyond this gating behavior, so no intermediate state can arise.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    C, G = map(int, input().split())
    
    if C == 1:
        print("vivo e morto")
    else:
        if G == 1:
            print("vivo")
        else:
            print("morto")

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the two regimes described in the algorithm. The first branch handles the closed box case, where the output is fixed regardless of G. The second branch handles the open box case, where G is used as a direct lookup for the final state. There are no edge cases beyond these two conditions, and no additional normalization or preprocessing is required.

## Worked Examples

### Example 1

Input:

```
1 0
```

| Step | C | G | Condition | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | C = 1 | vivo e morto |

When the box is closed, the value of G is irrelevant. Even though G is 0, the observer cannot access it, so both alive and dead remain possible interpretations.

### Example 2

Input:

```
0 1
```

| Step | C | G | Condition | Output |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | C = 0 | vivo |

Here the box is open, so the hidden value is fully revealed. Since G = 1, the cat is definitively alive.

This trace shows how opening the box eliminates ambiguity entirely and reduces the problem to a direct read of G.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of conditional checks and one input read |
| Space | O(1) | No additional data structures are used |

The solution fits easily within all constraints since it performs a fixed number of operations independent of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# To properly test, we redefine run with capture
def run(inp: str) -> str:
    old_in = sys.stdin
    old_out = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_in
        sys.stdout = old_out

# provided samples
assert run("1 0\n") == "vivo e morto", "sample 1"
assert run("0 1\n") == "vivo", "sample 2"

# custom cases
assert run("0 0\n") == "morto", "open box, dead cat"
assert run("1 1\n") == "vivo e morto", "closed box ignores G"
assert run("0 1\n") == "vivo", "open box, alive cat"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | vivo e morto | closed box forces ambiguity |
| 0 0 | morto | open box correctly reads dead state |
| 1 1 | vivo e morto | confirms G is ignored when closed |
| 0 1 | vivo | confirms direct observation when open |

## Edge Cases

The only meaningful edge distinction is whether C flips between 0 and 1.

For input:

```
1 1
```

the algorithm enters the closed-box branch and immediately outputs ambiguity, ignoring G entirely. This confirms that even a clearly “alive” internal state does not affect observability when the system is sealed.

For input:

```
0 0
```

the algorithm enters the open-box branch and reads G directly. Since G is 0, it outputs “morto”, demonstrating that no ambiguity remains once C allows observation.

Both cases confirm that the algorithm correctly separates the epistemic condition (C) from the physical state (G), which is the core structure of the problem.
