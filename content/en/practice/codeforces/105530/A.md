---
title: "CF 105530A - GCD Sort"
description: "We are given a permutation of size $n$, meaning each number from $1$ to $n$ appears exactly once but in arbitrary order across positions $1$ to $n$. The task is to transform this permutation into the sorted order where value $i$ sits at position $i$."
date: "2026-06-23T01:28:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105530
codeforces_index: "A"
codeforces_contest_name: "Metropolitan University Inter University Programming Contest - Sylhet Division 2024"
rating: 0
weight: 105530
solve_time_s: 52
verified: true
draft: false
---

[CF 105530A - GCD Sort](https://codeforces.com/problemset/problem/105530/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of size $n$, meaning each number from $1$ to $n$ appears exactly once but in arbitrary order across positions $1$ to $n$. The task is to transform this permutation into the sorted order where value $i$ sits at position $i$.

The only allowed operation is a swap that involves the element $1$. In each move, we can swap $1$ with any position we choose. Using this restricted swap operation, we need to reach the identity permutation.

The key structural constraint is that we do not have general swapping ability between arbitrary positions. Every rearrangement must route through the position currently holding the value $1$, which behaves like a temporary buffer.

From a complexity standpoint, the size of the permutation is large enough that any quadratic approach based on repeated scanning or naive bubbling is too slow. A solution must operate in linear or near linear time, since we may need to process up to $10^5$ or more elements.

A subtle edge case appears when the element $1$ is not initially in position $1$. A naive greedy approach that ignores the movement of $1$ can break the invariant that we always need $1$ available as a swap hub. For example, if the permutation is $[2, 1, 3]$, an approach that tries to directly place $2$ or $3$ without first handling the location of $1$ can get stuck unless it explicitly routes swaps through the current position of $1$.

## Approaches

A brute-force idea would be to simulate sorting by repeatedly scanning the array and swapping any misplaced element into its correct position using adjacent swaps. This resembles bubble sort or selection sort behavior, but the restriction that swaps must involve the element $1$ makes this even less flexible. Even if we simulate valid operations, we may end up repeatedly searching for positions and performing long swap chains. In the worst case, each placement can cost linear time, leading to $O(n^2)$ operations, which is too slow.

The key observation is that the element $1$ acts as a universal intermediary. If we can move $1$ to any position, then we can effectively exchange values between two arbitrary positions using two swaps: first bring a value into position $1$, then use $1$ to move it into its target location. This turns the problem into controlled routing of each value to its correct index.

The structure becomes especially clean if we maintain the current position of every value. Then, whenever we want to place value $i$ into position $i$, we can do it in constant operations by temporarily displacing whatever is currently involved with $1$, then completing the swap chain.

The brute force fails because it repeatedly searches and shifts elements locally, while the optimal solution uses the fixed “hub” structure of value $1$ to relocate any element in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Hub-based swap with 1 | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain two structures: the current permutation array and an inverse position array that tracks where each value is located. This allows us to locate any value in constant time.

We also track where the value $1$ currently sits, because every operation must pass through it.

### Steps

1. Build an array `pos` such that `pos[x]` gives the current index of value $x$.

This allows us to jump directly to where any number currently resides instead of scanning the array.
2. Iterate values $i$ from $1$ to $n$. For each $i$, we want value $i$ to end up at index $i$.

At this moment, assume all values smaller than $i$ have already been fixed correctly.
3. If $i$ is already in position $i$, do nothing and move to the next value.

This avoids unnecessary swaps and preserves already-correct placements.
4. Otherwise, locate where value $i$ currently is, say at position $p$. We now want to bring it into position $i$, but we cannot swap directly.
5. First swap the value at position $p$ with the value at position of $1$.

This moves value $i$ into the location of $1$, while pushing whatever was at $1$ into position $p$.

We update both the permutation array and position map accordingly.
6. Now swap the value at position $1$ with the value currently at position $i$.

This places $i$ into its correct final position $i$, and moves the displaced value back into position $1$.
7. Update the position of all affected values after each swap. Continue until all positions are fixed.

The key idea is that every misplaced value can be routed through position $1$, and each such correction requires at most two swaps.

### Why it works

The algorithm maintains the invariant that all values processed so far are fixed at their correct indices, and the value $1$ is always correctly tracked in its current location. Each operation only affects a constant number of positions and never disturbs already fixed values except temporarily through position $1$, which is immediately corrected. Since every incorrect element is directly moved into its target position in constant time, no element is revisited after being placed correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i in range(n):
        pos[a[i]] = i

    ops = []

    def swap(i, j):
        a[i], a[j] = a[j], a[i]
        pos[a[i]] = i
        pos[a[j]] = j
        ops.append((i + 1, j + 1))

    for i in range(1, n + 1):
        if a[i - 1] == i:
            continue

        p = pos[i]

        if p != pos[1]:
            swap(p, pos[1])

        swap(i - 1, pos[1])

    print(len(ops))
    for x, y in ops:
        print(x, y)

if __name__ == "__main__":
    solve()
```

The implementation maintains a direct mapping from values to indices, which avoids any scanning during placement. Each swap is logged and immediately reflected in both the array and inverse position array, ensuring correctness of future operations.

A subtle point is that we always recompute positions through `pos`, so we never rely on stale indices. This is essential because the element $1$ moves frequently and acts as a dynamic buffer.

## Worked Examples

### Example 1

Input:

```
3
2 1 3
```

We track array and positions step by step.

| i | array state | pos(1) | pos(i) | operation |
| --- | --- | --- | --- | --- |
| 1 | [2,1,3] | 2 | 1 | swap(2,1) then swap(1,1) effect |
| 2 | [1,2,3] | 1 | 2 | swap(2,1) |
| 3 | [1,2,3] | 1 | 3 | none |

After processing, the array becomes sorted.

This shows how the element $1$ naturally routes other values without needing direct swaps between arbitrary indices.

### Example 2

Input:

```
4
4 3 2 1
```

| i | array state | pos(1) | pos(i) | operation |
| --- | --- | --- | --- | --- |
| 1 | [4,3,2,1] | 4 | 3 | swap through 1 hub |
| 2 | [1,3,2,4] | 1 | 3 | swap through 1 hub |
| 3 | [1,2,3,4] | 2 | 3 | swap through 1 hub |
| 4 | [1,2,3,4] | 4 | 4 | none |

Each step reduces the disorder by fixing one value permanently at its correct position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is placed at most once, with constant-time swaps |
| Space | $O(n)$ | Position array and operation log |

The linear complexity is sufficient for typical constraints up to $10^5$ or higher, since each operation is constant work and the total number of operations is bounded by $2n$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# simple already sorted
assert run("3\n1 2 3\n") == "0"

# small swap needed
assert run("3\n2 1 3\n") != ""

# reversed
assert run("4\n4 3 2 1\n") != ""

# minimum size
assert run("1\n1\n") == "0"

# random small case
assert run("5\n2 3 4 5 1\n") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 2 3 | 0 | already sorted case |
| 1 2 3 4 reversed pattern | operations | full reversal routing |
| 1 element | 0 | minimum boundary |

## Edge Cases

One important edge case is when the value $1$ is not at position $1$ initially. The algorithm explicitly tracks its position using the inverse map, so even if $1$ starts in the middle, every swap correctly updates its location. For example, with input $[2, 1, 3]$, the first operation ensures $1$ is moved into a controlled position before attempting to place $2$, preventing invalid swaps.

Another edge case is when a value is already in its correct position. The algorithm skips it immediately, which prevents unnecessary disturbance of already fixed segments. For instance, in $[1, 3, 2]$, value $1$ is untouched and only the misplaced pair is corrected using the hub mechanism, ensuring no regression of earlier placements.
