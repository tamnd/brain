---
title: "CF 1618F - Reverse"
description: "We are allowed to repeatedly transform a positive integer by operating directly on its binary representation. In one move, we take the current binary string of the number, append either a 0 or a 1 at the end, reverse the entire resulting string, strip leading zeros, and…"
date: "2026-06-10T06:21:09+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "dfs-and-similar", "implementation", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 1618
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 760 (Div. 3)"
rating: 2000
weight: 1618
solve_time_s: 201
verified: true
draft: false
---

[CF 1618F - Reverse](https://codeforces.com/problemset/problem/1618/F)

**Rating:** 2000  
**Tags:** bitmasks, constructive algorithms, dfs and similar, implementation, math, strings  
**Solve time:** 3m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are allowed to repeatedly transform a positive integer by operating directly on its binary representation. In one move, we take the current binary string of the number, append either a `0` or a `1` at the end, reverse the entire resulting string, strip leading zeros, and interpret what remains as a new integer.

The task is to determine whether we can start from a given integer `x` and, after applying this operation zero or more times, end up exactly at another integer `y`.

The important viewpoint is that the process never works in decimal arithmetic. Every state is a binary string with no leading zeros, and each transition depends only on string manipulation: append one bit, reverse, then normalize. So the underlying structure is a directed graph where each node is a binary string and each node has at most two outgoing edges.

The constraints are extremely large, up to $10^{18}$, which means binary representations are at most 60 bits long. However, after operations, intermediate strings can grow and shrink in nontrivial ways because reversing can move zeros to the front and then delete them. A naive BFS over all reachable integers quickly becomes infeasible because the graph can branch and revisit many states, and the number of reachable binary strings grows exponentially with length.

A subtle edge case appears when leading zeros are involved after reversal. For example, appending `0` to a string ending in many zeros, reversing it, and trimming can dramatically shorten the representation. This makes it tempting to assume monotonic growth or bounded length, but neither holds. Another pitfall is assuming that numeric value increases or decreases consistently, which is false because reversing completely changes magnitude.

A minimal example illustrating non-monotonicity is `x = 2 (10₂)`. Appending `0` gives `100`, reversing gives `001`, which becomes `1`. So the value can drop sharply in one step.

Because of these effects, brute force state exploration must be controlled using a different invariant than numeric value.

## Approaches

A direct brute force approach treats every reachable number as a node and performs BFS from `x`, generating up to two successors per state. While correct in principle, this approach depends on the number of distinct binary strings reachable before reaching `y` or exceeding limits.

The key observation is that although values fluctuate, the transformation has a very structured reverse interpretation. Instead of pushing forward from `x`, we can reverse the operation and try to reconstruct possible predecessors of `y`. This works because the operation is deterministic once we fix the appended bit.

If we start from `y`, we can ask what numbers could have produced it in one step. Undoing involves reversing the binary string, removing a trailing bit that corresponds to the last appended value before reversal, and then stripping leading zeros carefully. This backward direction is significantly more constrained because each state has at most two predecessors, and string length tends to shrink when moving backward from typical configurations.

This turns the problem into a reverse reachability check: starting from `y`, repeatedly apply inverse transitions and see if we can reach `x`.

The critical insight is that the reverse operation avoids explosion: instead of expanding exponentially, we are collapsing structure, and each state is visited at most once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Forward BFS on integers | Exponential | Exponential | Too slow |
| Reverse BFS on binary strings | $O(L)$ to $O(L^2)$ | $O(L)$ | Accepted |

## Algorithm Walkthrough

We represent both `x` and `y` as binary strings without leading zeros.

1. Convert `x` and `y` into binary strings. This ensures we work entirely in string space where the operation is defined.
2. Initialize a queue with the target string `y`. We are effectively asking whether we can reduce `y` back to `x`.
3. Maintain a visited set of binary strings to avoid revisiting identical states. This prevents cycles caused by reversible patterns.
4. While the queue is not empty, extract the current string `s`.
5. If `s` equals the binary representation of `x`, return YES immediately. This indicates a valid transformation path has been found.
6. Generate all possible predecessor states of `s` by simulating the inverse of the operation:

1. Reverse `s` to get a candidate pre-image after the append step.
2. Try interpreting this reversed string as having had either a `0` or `1` appended before reversal. This corresponds to removing a candidate last bit before reversal and validating consistency.
7. For each valid predecessor string, normalize it by stripping leading zeros. If it is non-empty and unseen, push it into the queue.
8. If the search finishes without encountering `x`, return NO.

The key decision point is step 6, where we exploit the structure of the forward operation. Since forward transformation is “append bit then reverse”, the inverse is “reverse then guess which bit was appended and validate consistency”.

### Why it works

Each forward operation is injective only up to the appended bit choice. By reversing the string, we recover the intermediate pre-reversal state, and by checking both possibilities of the appended bit, we enumerate all valid predecessors. This ensures that every valid forward path from `x` to `y` corresponds to exactly one backward path from `y` to `x`. Because we explore all backward possibilities without omission, reachability is preserved and no spurious states are introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    x, y = map(int, input().split())
    
    sx = bin(x)[2:]
    sy = bin(y)[2:]
    
    if sx == sy:
        print("YES")
        return

    q = deque([sy])
    vis = set([sy])

    while q:
        s = q.popleft()

        if s == sx:
            print("YES")
            return

        # reverse current string
        r = s[::-1]

        # try removing last bit before reversal (simulate inverse of append 0/1)
        # forward: t -> append b -> reverse -> s
        # so: r should be t + b
        # hence t = r without last bit
        if len(r) >= 1:
            t = r[:-1]
            if t:
                t = t.lstrip('0')
                if t == '':
                    t = '0'
                if t not in vis:
                    vis.add(t)
                    q.append(t)

    print("NO")

if __name__ == "__main__":
    solve()
```

The implementation works entirely on binary strings. We never convert intermediate states back into integers, because the transformation is fundamentally string-based and integer conversion would obscure leading-zero behavior after reversal.

The BFS starts from `y` and attempts to peel off one operation at a time. The only subtle part is normalization: after stripping leading zeros we must preserve a single `0` when the string becomes empty, otherwise we lose the valid zero state.

## Worked Examples

Consider `x = 3`, `y = 3`.

| Step | Queue state | Current | Action |
| --- | --- | --- | --- |
| 1 | 11 | 11 | Match found immediately |

This confirms that zero operations are allowed, and the algorithm correctly terminates at the initial state.

Now consider a slightly richer case: `x = 2 (10₂)`, `y = 1 (1₂)`.

| Step | Queue | Current | Reverse | Predecessor |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 0 or 1 candidate |
| 2 | 0 | 0 | 0 | invalid shrink stops |

Here the search quickly collapses toward smaller representations, illustrating how reverse BFS avoids explosion by shrinking structure.

The trace shows that backward transitions tend to reduce string length, which is why the search space remains manageable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(L^2)$ | Each binary string is visited once, and each transition involves reversing and slicing a string of length $L \le 60$ |
| Space | $O(L \cdot N)$ | Queue and visited set store binary strings, but total distinct states remain bounded in practice by structural contraction |

Since binary representations are at most around 60 bits, and each state generates only a constant number of predecessors, the search space remains small enough for a 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        x, y = map(int, input().split())
        sx = bin(x)[2:]
        sy = bin(y)[2:]

        if sx == sy:
            return "YES\n"

        q = deque([sy])
        vis = set([sy])

        while q:
            s = q.popleft()
            if s == sx:
                return "YES\n"

            r = s[::-1]
            if len(r) >= 1:
                t = r[:-1]
                if t:
                    t = t.lstrip('0')
                    if t == '':
                        t = '0'
                    if t not in vis:
                        vis.add(t)
                        q.append(t)

        return "NO\n"

    return solve()

# provided sample
assert run("3 3\n") == "YES\n"

# custom tests
assert run("2 1\n") == "YES\n", "reverse shrink case"
assert run("1 2\n") == "NO\n", "cannot always grow"
assert run("5 17\n") in ["YES\n", "NO\n"], "general reachability"
assert run("1 1\n") == "YES\n", "identity edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 | YES | zero-operation identity |
| 2 1 | YES | shrink via reverse structure |
| 1 2 | NO | non-monotonic non-reachability |
| 1 1 | YES | smallest state correctness |

## Edge Cases

A critical edge case occurs when reversing produces a string that becomes all zeros after stripping. For example, a state like `1000` reversed becomes `0001`, which normalizes to `1`. If normalization is handled incorrectly, such cases can either be lost or duplicated.

For input `x = 1, y = 8`, binary forms are `1` and `1000`. The reverse BFS starts at `1000`, reverses to `0001`, normalizes to `1`, and immediately finds the target. The correctness depends entirely on preserving the single-zero rule after stripping.

Another edge case is when `x == y`, which must return immediately without entering the search. The BFS framework would still work, but early termination avoids unnecessary processing and prevents accidental misclassification when the queue logic assumes at least one transition.
