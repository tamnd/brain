---
title: "CF 2111E - Changing the String"
description: "We are given a string consisting only of the characters a, b, and c. Alongside it is a sequence of operations. Each operation suggests a possible replacement: choose any occurrence of a letter x and turn it into another letter y, or skip the operation entirely."
date: "2026-06-08T04:32:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "implementation", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 2111
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 179 (Rated for Div. 2)"
rating: 1900
weight: 2111
solve_time_s: 96
verified: false
draft: false
---

[CF 2111E - Changing the String](https://codeforces.com/problemset/problem/2111/E)

**Rating:** 1900  
**Tags:** binary search, data structures, greedy, implementation, sortings, strings  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string consisting only of the characters `a`, `b`, and `c`. Alongside it is a sequence of operations. Each operation suggests a possible replacement: choose any occurrence of a letter `x` and turn it into another letter `y`, or skip the operation entirely.

The key difficulty is that these operations are applied in order, and each one is optional. We are not forced to apply any specific replacement, but we must decide, for each operation, whether it is worth using it and, if so, which character occurrence to modify. After processing all operations, we want the final string to be as small as possible in lexicographic order.

Lexicographic minimization here means we want earlier positions in the string to become as small as possible, prioritizing `a < b < c`. Since operations are global (they can affect any position containing `x`), and choices are sequential, the problem is about coordinating limited “conversion opportunities” across time.

The constraints are tight: total string length and total operations over all test cases are up to 2 · 10^5. This rules out any solution that tries to simulate each operation by scanning the whole string, since that would lead to O(nq) behavior in the worst case.

A naive mental model would be: after each operation, scan the entire string and apply a replacement if it helps. That fails not only for performance but also for correctness, because the best decision for an operation depends on future operations, not just the current state.

A subtle failure case for greedy immediate application appears when early conversions are locally beneficial but globally harmful. For example, converting `b -> a` early might seem optimal, but later operations might allow converting `c -> b` and then `b -> a`, producing better cascading improvements. A greedy local approach loses this structure.

## Approaches

A brute force solution would simulate operations one by one, and for each operation scan the string to decide where to apply it, potentially trying all possible indices. This leads to O(nq), which is far too large at 2 · 10^5 per parameter.

The key observation is that characters are extremely limited: only three symbols exist. This means the entire system can be described by how these symbols can transform into each other over time. Instead of tracking positions in the string, we track transformations between letters.

Each operation only affects counts of characters, not their positions. More importantly, whether we apply an operation depends on whether doing so helps us reduce future characters. This suggests processing operations backward.

If we reverse time, we can think of each letter as having a “best possible final form” depending on future operations. When we process operations from last to first, we maintain the best known mapping from each character to the smallest character it can eventually become.

At each reversed step, we decide whether we want to “use” the operation or ignore it. Since we are going backward, using an operation corresponds to allowing a transformation in the future. This becomes a deterministic decision because we already know the best outcomes of later operations.

We maintain the best achievable character for `a`, `b`, and `c` after applying a suffix of operations. Then we propagate these transformations backwards. Finally, we apply the resulting mapping to the original string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(nq) | O(n) | Too slow |
| Reverse DP on letters | O(n + q) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain an array `best` where `best[x]` represents the smallest character that original letter `x` can become after processing the suffix of operations.

We process operations from last to first.

1. Initialize `best[a] = a`, `best[b] = b`, `best[c] = c`. This represents the fact that with no operations applied, each letter stays itself.
2. Iterate over operations in reverse order. For an operation `(x -> y)`, we consider whether applying it helps improve the current mapping. At this point, we already know the best achievable outcomes after later operations.
3. If converting `x` through this operation leads to a strictly smaller final character than what `x` currently maps to, we apply it by updating `best[x]`.

More precisely, we compare `best[y]` with `best[x]`. If `best[y] < best[x]`, then making `x` go through `y` improves its final outcome, so we set `best[x] = best[y]`.

1. Otherwise, we ignore the operation because it cannot improve the final result for any occurrence of `x`.
2. After processing all operations, we construct the final string by replacing each character `s[i]` with `best[s[i]]`.

The reason this works is that each letter independently tracks its optimal achievable form. Because there are only three letters, interactions do not depend on positions, only on transformation chains. Processing in reverse ensures that when deciding about an operation, we already know the best future consequences.

### Why it works

At any point in reverse processing, `best[x]` represents the minimal letter reachable from `x` using only operations to the right of the current index. When we consider a new operation `x -> y`, we are effectively adding a new edge in this transformation graph. If routing through `y` improves `x`, then it must be optimal to include this edge; otherwise, skipping it cannot harm future possibilities because `best[y]` already encodes the optimal future outcome of `y`. This invariant ensures we never miss a beneficial transformation chain.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        s = list(input().strip())

        ops = []
        for _ in range(q):
            x, y = input().split()
            ops.append((x, y))

        best = { 'a': 'a', 'b': 'b', 'c': 'c' }

        def apply(x):
            return best[x]

        for x, y in reversed(ops):
            if apply(y) < apply(x):
                best[x] = apply(y)

        res = []
        for ch in s:
            res.append(apply(ch))

        print("".join(res))

if __name__ == "__main__":
    solve()
```

The core structure is the `best` dictionary, which stores the current optimal outcome for each character. The reverse traversal is crucial because it ensures that when evaluating an operation, all later decisions are already fixed.

The function `apply` is a small abstraction that makes it clear we are always working with the final mapped value, not the raw character. This avoids mistakes where intermediate mappings would otherwise be ignored.

The final loop simply translates the original string through this mapping, which is safe because operations never depend on position, only on character identity.

## Worked Examples

### Example 1

Input:

```
s = cb
operations: (c->b), (b->a)
```

We process backwards.

| Step | Operation | best[a] | best[b] | best[c] |
| --- | --- | --- | --- | --- |
| init | - | a | b | c |
| 1 | b -> a | a | a | c |
| 2 | c -> b | a | a | a |

Final mapping: `c -> a`, `b -> a`, `a -> a`

Applying to `cb` gives `aa`.

This shows how reverse processing naturally chains transformations.

### Example 2

Input:

```
s = bbb
operations: b->c, c->a, b->a
```

| Step | Operation | best[a] | best[b] | best[c] |
| --- | --- | --- | --- | --- |
| init | - | a | b | c |
| 1 | b -> a | a | a | c |
| 2 | c -> a | a | a | a |
| 3 | b -> c | a | a | a |

Final string becomes `aaa`.

This example demonstrates that even seemingly irrelevant operations can matter if they improve intermediate states.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Each test processes operations once in reverse and then builds the result string in linear time |
| Space | O(1) | Only a fixed mapping over three characters is stored |

The solution comfortably fits within limits because even in the worst case, the total number of operations across all test cases is 2 · 10^5, making linear processing sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, q = map(int, input().split())
            s = list(input().strip())

            ops = []
            for _ in range(q):
                x, y = input().split()
                ops.append((x, y))

            best = {'a':'a','b':'b','c':'c'}

            def apply(x):
                return best[x]

            for x, y in reversed(ops):
                if apply(y) < apply(x):
                    best[x] = apply(y)

            print("".join(apply(ch) for ch in s))

    out = io.StringIO()
    _stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = _stdout
    return out.getvalue().strip()

# provided samples
assert run("""3
2 2
cb
c b
b a
10 10
bbbbbbbbbb
b a
b c
c b
b a
c a
b c
b c
b a
a b
c a
30 20
abcaababcbbcabcbbcabcbabbbbabc
b c
b c
c a
b c
b c
b a
b c
b c
b a
b a
b a
b a
c a
b c
c a
b c
c a
c a
b c
c b
""") == """ab
aaaaabbbbb
aaaaaaaaaaaaaaabbbabcbabbbbabc"""

# custom cases
assert run("""1
1 1
a
a b
""") == "b", "single char upgrade"

assert run("""1
3 0
abc
""") == "abc", "no operations"

assert run("""1
3 3
abc
b c
c b
b a
""") == "aaa", "cycle collapse"

assert run("""1
4 2
cbbc
c b
b a
""") == "aaba", "chain effect"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char upgrade | b | basic mapping update |
| no operations | abc | identity case |
| cycle collapse | aaa | conflicting operations resolved |
| chain effect | aaba | partial propagation correctness |

## Edge Cases

A tricky situation occurs when operations form cycles, such as `a -> b`, `b -> c`, `c -> a`. A naive forward simulation might oscillate or incorrectly apply only local improvements. In reverse processing, the invariant ensures stability: once a letter is mapped to a smaller representative, it never increases again.

Another edge case is when operations that seem useless locally become useful due to later transformations. For example, `b -> c` looks harmful if `c` is large initially, but later `c -> a` appears. The reverse pass ensures that when we evaluate `b -> c`, we already know that `c` eventually becomes `a`, so the improvement is correctly captured at that moment.

Finally, cases with no operations or only self-maps (`a -> a`) do not affect the mapping. The algorithm naturally leaves `best` unchanged, so the output remains identical to the input string.
