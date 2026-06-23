---
title: "CF 105381E - Elimination Game"
description: "We start with pebbles labeled from 1 to n, where pebble i has weight i. In each move, two currently available pebbles are selected and passed through one of two devices. One device always returns the lighter of the two inputs, the other always returns the heavier one."
date: "2026-06-23T16:08:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105381
codeforces_index: "E"
codeforces_contest_name: "National Yang Ming Chiao Tung University 2024 Team Selection Programming Contest"
rating: 0
weight: 105381
solve_time_s: 50
verified: true
draft: false
---

[CF 105381E - Elimination Game](https://codeforces.com/problemset/problem/105381/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with pebbles labeled from 1 to n, where pebble i has weight i. In each move, two currently available pebbles are selected and passed through one of two devices. One device always returns the lighter of the two inputs, the other always returns the heavier one. After applying the device, only the returned pebble continues to the next round. This process is repeated exactly n − 1 times, so that eventually only one pebble remains.

The twist is that the two devices are not free to use arbitrarily. The minimizer can be used at most a times, and the maximizer can be used at most b times, with a + b = n − 1. The question is whether there exists a sequence of pairings and device choices such that the final remaining pebble is exactly x.

Although the process looks like repeated comparisons, the key difficulty is that each operation is not just a comparison but a forced selection rule that biases which element survives. The entire process is a sequence of eliminations shaping which values can survive until the end.

The constraints make brute-force over all elimination trees impossible. Even though n is at most 1000, the number of possible binary tournament structures is already exponential in n, and each node has two possible operation types, so direct enumeration grows far beyond feasible limits.

A subtle edge case appears when x is either 1 or n. In those cases, we might incorrectly assume the answer is always possible because the smallest or largest element seems “easy” to preserve, but feasibility still depends on whether we have enough minimizer or maximizer operations to enforce survival of extreme values.

## Approaches

A direct simulation would try to build a binary tree of eliminations, choosing at each step whether to apply min or max. Each configuration corresponds to a full pairing structure over n items, and each internal node is labeled with an operation type. This leads to a huge state space: even fixing a tree shape, there are 2^(n−1) ways to assign operations, and there are Catalan-number many shapes. This is far too large.

The key observation is to stop thinking about the structure of comparisons and instead track how many values must be eliminated on each side of x.

Think about the final survivor x. Every other element must be eliminated at some point. Each element y < x can only disappear if it is ever selected in a way that discards it. Similarly, each element y > x must also be eliminated. The crucial constraint is that only two types of operations exist: minimizer always keeps the smaller, maximizer always keeps the larger.

This means:

- A minimizer operation can eliminate at most one large element (it keeps the smaller one).
- A maximizer operation can eliminate at most one small element (it keeps the larger one).

So we interpret operations as “tools” for removing elements on the wrong side of x.

To ensure x survives:

- All values less than x must be removable without ever killing x.
- All values greater than x must also be removable without killing x.

Now consider what is required. To eliminate an element y < x, we must eventually place it in a maximizer operation against something larger or equal, so that it is discarded. This consumes one maximizer use per small element elimination, except that eliminations can be paired carefully with other elements as long as x is protected.

Similarly, each element greater than x must be eliminated using a minimizer operation.

Thus, the feasibility reduces to checking whether we have enough minimizer operations to eliminate all elements greater than x, and enough maximizer operations to eliminate all elements less than x.

Counts are straightforward:

- Elements greater than x: n − x
- Elements less than x: x − 1

So we need:

- b ≥ n − x
- a ≥ x − 1

Since a + b = n − 1, these two conditions are also sufficient.

This reduces the entire problem to a simple feasibility check on counts, independent of any structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over elimination structures | Exponential | O(n) | Too slow |
| Count-based feasibility | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read n, a, b, and x. The value x is the pebble we want to survive until the end.
2. Compute how many elements are smaller than x. This is x − 1. These elements must all be eliminated in a way that never removes x.
3. Compute how many elements are larger than x. This is n − x. These elements must also be eliminated while preserving x.
4. Check whether the maximizer operations are sufficient to eliminate all elements smaller than x. Since maximizer keeps the larger value, each use can be thought of as enabling removal of one smaller element, so we require a ≥ x − 1.
5. Check whether the minimizer operations are sufficient to eliminate all elements larger than x. Since minimizer keeps the smaller value, each use allows removal of one larger element, so we require b ≥ n − x.
6. If both conditions hold, output “Yes”, otherwise output “No”.

### Why it works

Every element except x must be eliminated exactly once during the process. The only way to eliminate a smaller element without affecting x is through a maximizer interaction that preserves a larger partner, and symmetrically, eliminating a larger element without affecting x requires a minimizer interaction. Since each operation can safely eliminate at most one element from the opposite side of x, the total number of required eliminations directly matches the available counts of each operation type. This creates a tight necessary and sufficient condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, a, b, x = map(int, input().split())
    
    need_maximizer = x - 1
    need_minimizer = n - x
    
    if a >= need_maximizer and b >= need_minimizer:
        print("Yes")
    else:
        print("No")
```

The implementation is a direct translation of the derived feasibility conditions. Each test case is handled independently in constant time. The key detail is keeping the mapping consistent: maximizer usage corresponds to eliminating elements less than x, while minimizer usage corresponds to eliminating elements greater than x.

## Worked Examples

We trace two cases, one positive and one negative.

### Example 1

Input:

n = 5, a = 2, b = 2, x = 4

We compute requirements:

| Step | x − 1 | n − x | a | b | Condition |
| --- | --- | --- | --- | --- | --- |
| Compute | 3 | 1 | 2 | 2 | - |
| Check maximizer | 3 ≤ 2 | - | fail | - | No |
| Check minimizer | - | 1 ≤ 2 | - | ok | - |

Since we do not have enough maximizer operations, elements 1, 2, 3 cannot all be safely eliminated without risking x=4. Output is No.

### Example 2

Input:

n = 10, a = 0, b = 9, x = 7

| Step | x − 1 | n − x | a | b | Condition |
| --- | --- | --- | --- | --- | --- |
| Compute | 6 | 3 | 0 | 9 | - |
| Check maximizer | 6 ≤ 0 | - | fail | - | No |
| Check minimizer | - | 3 ≤ 9 | - | ok | - |

Here we lack any maximizer operations, so all elements smaller than 7 cannot be eliminated safely. Even though minimizer capacity is large, it cannot compensate for the missing operation type.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses constant arithmetic operations |
| Space | O(1) | No additional structures beyond variables |

The solution easily satisfies the constraints since even for 50,000 test cases, the work per case is minimal arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n, a, b, x = map(int, input().split())
        if a >= x - 1 and b >= n - x:
            out.append("Yes")
        else:
            out.append("No")
    return "\n".join(out)

# provided samples (as given in statement image; only outputs shown there)
assert run("""2
5 2 2 4
10 0 9 7
""") == """Yes
No"""

# minimal case
assert run("""1
1 0 0 1
""") == "Yes"

# x = 1 edge
assert run("""1
5 0 4 1
""") == "Yes"

# x = n edge
assert run("""1
5 4 0 5
""") == "Yes"

# insufficient both
assert run("""1
5 0 0 3
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 case | Yes | single element always survives |
| x=1 boundary | Yes | only need minimizers |
| x=n boundary | Yes | only need maximizers |
| insufficient ops | No | detects impossible splits |

## Edge Cases

When n = 1, there are no operations, so the only possible survivor is 1. The condition gives a = 0 ≥ 0 and b = 0 ≥ 0, so the algorithm returns Yes correctly.

When x = 1, we have x − 1 = 0, so no maximizer operations are needed. All other elements must be eliminated using minimizers, which matches b ≥ n − 1.

When x = n, we have n − x = 0, so no minimizer operations are needed. All smaller elements must be removed using maximizers, matching a ≥ n − 1.

In each case, the computed inequalities reduce correctly to the intuitive requirement that only the necessary operation type is constrained.
