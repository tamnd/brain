---
title: "CF 245C - Game with Coins"
description: "Each move is defined by choosing an integer x such that 2x + 1 ≤ n. The move removes one coin from chest x, chest 2x, and chest 2x + 1. If one of those chests is already empty, nothing happens to that chest during the move. We are given the initial number of coins in every chest."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "C"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 1700
weight: 245
solve_time_s: 111
verified: true
draft: false
---

[CF 245C - Game with Coins](https://codeforces.com/problemset/problem/245/C)

**Rating:** 1700  
**Tags:** greedy  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

Each move is defined by choosing an integer `x` such that `2x + 1 ≤ n`. The move removes one coin from chest `x`, chest `2x`, and chest `2x + 1`. If one of those chests is already empty, nothing happens to that chest during the move.

We are given the initial number of coins in every chest. The task is to determine the minimum total number of moves needed to make all chests empty. If this is impossible, we print `-1`.

The operation structure is the whole problem. Every move affects exactly three specific positions connected by the formula `(x, 2x, 2x+1)`. We are not free to remove coins arbitrarily.

The constraints are small enough that even cubic or exponential approaches over `n` might look tempting at first glance, because `n ≤ 100`. The dangerous part is that the coin counts can reach `1000`, so simulating all possible move sequences quickly becomes impossible. A brute-force search over states would explode immediately because the state space is roughly `1000^100`.

The small value of `n` hints that the graph structure of the operations matters more than raw optimization. We need to derive exact equations describing how many times each move must be used.

Several edge cases are easy to mishandle.

If `n = 1`, there is no valid `x` because `2x + 1 ≤ 1` has no positive solution. No move can ever be performed.

Input:

```
1
1
```

Correct output:

```
-1
```

A naive implementation that only checks whether the total number of coins is positive would fail here.

Another tricky case appears when some chest can never be touched by any move. For example:

Input:

```
2
1 1
```

Correct output:

```
-1
```

There is still no valid move because `x = 1` would require `3 ≤ 2`, which is false.

There are also cases where the system of equations becomes inconsistent.

Input:

```
3
1 1 2
```

Only move `x = 1` exists, and it affects all three chests equally. Using it once removes `(1,1,1)`, using it twice removes `(2,2,2)`, and so on. We can never obtain `(1,1,2)`, so the answer is `-1`.

A careless greedy simulation may repeatedly apply valid moves and incorrectly assume every configuration is solvable.

## Approaches

The most direct brute-force idea is to search over all possible move sequences. Since every move removes up to three coins, the total number of moves is at most about `100000`, but the branching factor is up to `50` because `x` can range from `1` to `⌊(n-1)/2⌋`.

That produces an astronomically large search tree. Even memoization over states does not help because each chest can contain up to `1000` coins, giving roughly `1001^100` possible states.

The brute-force approach is still useful conceptually because it exposes the key property of the problem: every move type acts independently. If we decide that move `x` is used `t_x` times, then the final effect on every chest is completely determined.

This turns the game into a system of linear equations.

Move `x` contributes:

- `1` removal from chest `x`
- `1` removal from chest `2x`
- `1` removal from chest `2x+1`

Suppose `t_x` is the number of times we use move `x`. Then every chest `i` must satisfy:

```
a_i = t_i + t_parent(i)
```

where:

- `t_i` contributes because move `i` removes from chest `i`
- `t_parent(i)` contributes because the parent move also removes from chest `i`

More concretely:

- if `i` is even, parent is `i/2`
- if `i` is odd and `i > 1`, parent is `(i-1)/2`

This immediately resembles a binary tree. Each node receives removals from itself and from its parent.

Now the structure becomes simple. For every chest:

```
t_i = a_i - t_parent(i)
```

So once we know the parent value, the current value is forced. There is no freedom at all.

Leaves are especially important. If `i > (n-1)/2`, then move `i` does not exist because `2i+1 > n`. That means `t_i = 0`. Therefore:

```
a_i = t_parent(i)
```

This allows us to determine parent values from the leaves and propagate upward uniquely.

If any equation becomes inconsistent or produces a negative value, the configuration is impossible.

The total number of moves is simply:

```
sum(t_i)
```

because `t_i` counts how many times move `i` is used.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an array `t` where `t[i]` represents how many times move `i` is used.
2. Any index `i` with `2i + 1 > n` cannot be chosen as a move. These are leaves in the operation tree, so their move count must be zero.
3. Process chests from `n` down to `1`.
4. For chest `i`, determine how many removals come from its children moves. Specifically:

- move `i` itself removes from chest `i`
- move `parent(i)` also removes from chest `i`
5. Rearranging the equation gives:

```
t_i = a_i - contribution_from_parent
```
6. A cleaner implementation uses a bottom-up relation:

- every leaf forces the value of its parent
- if two children imply different values for the same parent, the system is impossible
7. More explicitly:

- for every valid move `x`
- both chests `2x` and `2x+1` must satisfy:

```
a[2x] - t[2x] = t[x]
a[2x+1] - t[2x+1] = t[x]
```
- these two values must match
8. Since leaves have `t[leaf] = 0`, we can determine all parent values recursively upward.
9. If at any point:

- a required value becomes negative
- two equations disagree
- the root move count becomes invalid

then print `-1`.
10. Otherwise print the sum of all `t[i]`.

### Why it works

Every move type is independent and commutative. Only the number of times each move is used matters, not the order.

For any chest `i`, coins can disappear only through:

- move `i`
- move `parent(i)`

No other move touches that chest. That creates a complete system of equations with one unique possible solution.

Leaves cannot be selected as moves, so their move counts are forced to zero. This uniquely determines their parents, which determines higher ancestors recursively.

If the derived values satisfy every equation and remain non-negative, then executing move `i` exactly `t[i]` times empties every chest exactly. Since the solution is unique, its total move count is automatically minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))

    t = [0] * (n + 1)

    # Leaves cannot be chosen as moves
    for i in range(n, 0, -1):
        if 2 * i + 1 > n:
            t[i] = 0

    # Process internal nodes bottom-up
    for i in range((n - 1) // 2, 0, -1):
        left = 2 * i
        right = 2 * i + 1

        val_left = a[left] - t[left]
        val_right = a[right] - t[right]

        if val_left != val_right or val_left < 0:
            print(-1)
            return

        t[i] = val_left

    # Verify every chest exactly
    for i in range(1, n + 1):
        removed = t[i]

        if i > 1:
            removed += t[i // 2]

        if removed != a[i]:
            print(-1)
            return

    print(sum(t))

solve()
```

The core idea is that `t[i]` represents how many times move `i` is used. Leaves are initialized to zero because those moves do not exist.

The bottom-up phase reconstructs all internal move counts. For node `i`, both children must imply the same value for `t[i]`. If they disagree, there is no valid sequence of moves.

The final verification loop is important. Even though the recursive reconstruction already encodes the equations, explicitly checking every chest prevents subtle mistakes and guarantees correctness.

The condition:

```
removed = t[i]
if i > 1:
    removed += t[i // 2]
```

matches the problem structure exactly. Chest `i` is touched by move `i` and by its parent move.

The implementation uses 1-based indexing because the move relationships are defined naturally through binary heap indices.

## Worked Examples

### Example 1

Input:

```
1
1
```

Processing:

| i | Is leaf | t[i] |
| --- | --- | --- |
| 1 | yes | 0 |

Verification:

| Chest | Removed | Needed |
| --- | --- | --- |
| 1 | 0 | 1 |

Mismatch occurs, so the answer is `-1`.

This example demonstrates the impossible case where no move exists at all.

### Example 2

Input:

```
3
3 3 3
```

Only move `1` exists.

Initialization:

| i | Is leaf | t[i] |
| --- | --- | --- |
| 3 | yes | 0 |
| 2 | yes | 0 |

Bottom-up reconstruction:

| i | val_left | val_right | t[i] |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 3 |

Verification:

| Chest | Formula | Result |
| --- | --- | --- |
| 1 | t1 | 3 |
| 2 | t2 + t1 | 0 + 3 |
| 3 | t3 + t1 | 0 + 3 |

All equations match, so the answer is:

```
3
```

This confirms that repeating move `1` exactly three times empties all chests.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is processed a constant number of times |
| Space | O(n) | The array `t` stores one value per chest |

With `n ≤ 100`, this solution easily fits inside the limits. Even Python executes it instantly.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = [0] + list(map(int, input().split()))

    t = [0] * (n + 1)

    for i in range(n, 0, -1):
        if 2 * i + 1 > n:
            t[i] = 0

    for i in range((n - 1) // 2, 0, -1):
        left = 2 * i
        right = 2 * i + 1

        val_left = a[left] - t[left]
        val_right = a[right] - t[right]

        if val_left != val_right or val_left < 0:
            return "-1"

        t[i] = val_left

    for i in range(1, n + 1):
        removed = t[i]

        if i > 1:
            removed += t[i // 2]

        if removed != a[i]:
            return "-1"

    return str(sum(t))

# provided sample
assert run("1\n1\n") == "-1", "sample 1"

# valid simple case
assert run("3\n3 3 3\n") == "3", "single move repeated"

# inconsistent children
assert run("3\n1 1 2\n") == "-1", "children force different counts"

# deeper valid tree
assert run("7\n3 5 5 2 2 2 2\n") == "7", "multi-level reconstruction"

# minimum impossible size
assert run("2\n1 1\n") == "-1", "no valid moves exist"

# all zeros after one move chain
assert run("7\n2 3 3 1 1 1 1\n") == "4", "balanced hierarchy"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `-1` | No valid move exists |
| `3 / 3 3 3` | `3` | Single move repeated multiple times |
| `3 / 1 1 2` | `-1` | Inconsistent equations |
| `7 / 3 5 5 2 2 2 2` | `7` | Multi-level propagation |
| `2 / 1 1` | `-1` | Boundary where no move exists |
| `7 / 2 3 3 1 1 1 1` | `4` | Correct parent-child reconstruction |

## Edge Cases

Consider again the smallest input:

Input:

```
1
1
```

The algorithm marks chest `1` as a leaf because `2*1+1 > 1`. Hence `t[1]=0`. During verification, chest `1` receives zero removals although it needs one. The algorithm correctly returns `-1`.

Now examine an inconsistent configuration:

Input:

```
3
1 1 2
```

Leaves are `2` and `3`, so `t[2]=t[3]=0`.

For node `1`:

- left child implies `t[1]=1`
- right child implies `t[1]=2`

These values disagree, so no valid move count assignment exists. The algorithm immediately prints `-1`.

Finally, consider a deeper valid example:

Input:

```
7
3 5 5 2 2 2 2
```

Leaves `4,5,6,7` force:

```
t[2]=2
t[3]=2
```

Then:

```
t[1]=3
```

Verification gives:

- chest 1: `3`
- chest 2: `2+3=5`
- chest 3: `2+3=5`
- leaves: `0+2=2`

Every equation matches, and the total number of moves is:

```
3+2+2=7
```

This confirms the recursive reconstruction works correctly through multiple tree levels.
