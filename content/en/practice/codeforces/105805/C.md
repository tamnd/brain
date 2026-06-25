---
title: "CF 105805C - Again Sort Permutation"
description: "We are given a permutation of the numbers from 1 to n. An operation chooses two positions whose current values are a and b. If a + b is a composite number, we may swap those two values."
date: "2026-06-25T15:31:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105805
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #41 (Magical-Forces)"
rating: 0
weight: 105805
solve_time_s: 52
verified: true
draft: false
---

[CF 105805C - Again Sort Permutation](https://codeforces.com/problemset/problem/105805/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers from `1` to `n`.

An operation chooses two positions whose current values are `a` and `b`. If `a + b` is a composite number, we may swap those two values.

The question is whether, after performing any number of such swaps, we can transform the permutation into the sorted permutation

```
1 2 3 ... n
```

The number of test cases is large, and the sum of all `n` values is at most `2 · 10^5`. Any solution significantly slower than linear or near-linear per test case will struggle. Something like `O(n^2)` per test case is already too expensive when `n` approaches `2 · 10^5`.

The interesting part is that the operation depends only on the values being swapped, not on their positions. If values `x` and `y` satisfy that `x + y` is composite, then those two values can be swapped whenever they appear in the permutation.

A few small cases reveal the structure.

For

```
n = 2
p = [2, 1]
```

the only pair is `(1,2)` and `1 + 2 = 3`, which is prime. No swap is possible, so the answer is `NO`.

For

```
n = 3
p = [1, 3, 2]
```

the pair `(1,3)` can be swapped because `1 + 3 = 4` is composite, but value `2` is isolated. Since `2` is already in its correct position, sorting is possible and the answer is `YES`.

A careless implementation might assume that every permutation is sortable once `n ≥ 3`, which is false. For example:

```
n = 4
p = [2, 1, 4, 3]
```

Values `{1,3}` form one group and `{2,4}` form another. Values can move only inside their own group. Position `1` ultimately needs value `1`, but currently contains value `2` from a different group, making sorting impossible.

## Approaches

The brute-force view is to build a graph whose vertices are the values `1..n`. Two values are connected if their sum is composite. Every allowed swap corresponds to swapping two vertices connected by an edge.

One could repeatedly simulate swaps and explore reachable permutations. This is correct for tiny inputs, but the state space is `n!`, so it becomes hopeless almost immediately.

The key observation is that we do not actually care about individual swap sequences.

Consider the graph on values `1..n` where an edge exists between `x` and `y` when `x + y` is composite.

A classical fact from permutation groups is that if a graph component is connected, then swaps along its edges generate every permutation of the vertices in that component. In practical terms, all values inside the same connected component can be rearranged arbitrarily among the positions currently occupied by that component's values.

This turns the problem into a connected-component question.

Suppose a component contains values `{1,3}`. No operation can ever move a value from this component into a position currently occupied by a value from another component. The set of positions occupied by component values remains unchanged forever.

To sort the permutation, value `i` must eventually reach position `i`. Thus, for every position `pos`, the current value `p[pos]` and the target value `pos` must belong to the same connected component.

The remaining task is to understand the component structure of the graph.

For `n ≥ 5`, the graph is connected.

All odd numbers form a clique because the sum of two odd numbers is an even number at least `4`, hence composite.

All even numbers form a clique because the sum of two even numbers is an even number at least `4`, hence composite.

Value `5` exists when `n ≥ 5`, and

```
5 + 2 = 7
5 + 4 = 9
```

At least one even number connects to the odd clique, creating a bridge between the parity groups. Thus the entire graph becomes connected.

The only exceptional values of `n` are:

```
n = 1
component: {1}

n = 2
components: {1}, {2}

n = 3
components: {1,3}, {2}

n = 4
components: {1,3}, {2,4}
```

Once this is known, the solution becomes very small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the permutation.
2. If `n = 1`, output `YES`.
3. If `n ≥ 5`, output `YES`.

The graph of values is connected, so any permutation can be transformed into any other permutation.
4. If `n = 2`, each value is isolated.

The permutation is sortable only if it is already sorted.
5. If `n = 3` or `n = 4`, there are exactly two components:

`A = {1,3}` and `B = {2,4}` restricted to values that actually exist.
6. For every position `i`, check whether `i` and `p[i]` belong to the same component.
7. If every position passes the check, output `YES`; otherwise output `NO`.

### Why it works

Connected components determine which values can ever exchange places. Values from different components can never cross component boundaries.

Inside a connected component, swaps along graph edges generate arbitrary permutations of the component's values. Thus the only obstruction is whether a value needs to move into a position belonging to a different component.

Checking that `component(i) = component(p[i])` for every position exactly verifies that every value can be rearranged to its target location using only swaps inside its component. This condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))

    if n == 1:
        print("YES")
        continue

    if n >= 5:
        print("YES")
        continue

    ok = True

    for i, x in enumerate(p, start=1):
        if (i & 1) != (x & 1):
            ok = False
            break

    print("YES" if ok else "NO")
```

The implementation follows the component characterization directly.

For `n = 3` and `n = 4`, the components are exactly the odd values and the even values. Checking whether position `i` and value `p[i]` belong to the same component is equivalent to checking that they have the same parity.

For `n = 2`, the same parity check still works. Position `1` can only contain `1`, and position `2` can only contain `2`.

The early return for `n ≥ 5` is the main optimization. Once the graph becomes connected, every permutation is sortable, so no further work is needed.

## Worked Examples

### Example 1

Input:

```
n = 4
p = [2, 1, 4, 3]
```

| Position | Value | Position Parity | Value Parity | Match |
| --- | --- | --- | --- | --- |
| 1 | 2 | Odd | Even | No |

The first position already violates the component condition.

Output:

```
NO
```

This example demonstrates that values cannot move between the odd and even components.

### Example 2

Input:

```
n = 4
p = [3, 2, 1, 4]
```

| Position | Value | Position Parity | Value Parity | Match |
| --- | --- | --- | --- | --- |
| 1 | 3 | Odd | Odd | Yes |
| 2 | 2 | Even | Even | Yes |
| 3 | 1 | Odd | Odd | Yes |
| 4 | 4 | Even | Even | Yes |

All positions satisfy the component condition.

Output:

```
YES
```

Values `1` and `3` can swap with each other, while `2` and `4` stay fixed. Sorting is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan of the permutation |
| Space | O(1) | Only a few variables are used |

Since the sum of all `n` values across test cases is at most `2 · 10^5`, a linear solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        if n == 1:
            ans.append("YES")
            continue

        if n >= 5:
            ans.append("YES")
            continue

        ok = True
        for i, x in enumerate(p, start=1):
            if (i & 1) != (x & 1):
                ok = False
                break

        ans.append("YES" if ok else "NO")

    return "\n".join(ans)

# provided samples
assert run(
"""4
1
1
2
2 1
2
1 2
4
2 1 4 3
"""
) == "YES\nNO\nYES\nNO"

# minimum size
assert run(
"""1
1
1
"""
) == "YES"

# n = 2 unsorted
assert run(
"""1
2
2 1
"""
) == "NO"

# n = 4 sortable inside components
assert run(
"""1
4
3 2 1 4
"""
) == "YES"

# n >= 5 always sortable
assert run(
"""1
5
5 4 3 2 1
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` | `YES` | Smallest possible case |
| `2 1` for `n=2` | `NO` | No swaps available |
| `3 2 1 4` for `n=4` | `YES` | Rearrangement inside components |
| Reverse permutation for `n=5` | `YES` | Connected graph case |

## Edge Cases

Consider

```
1
2
2 1
```

The graph has two isolated vertices because `1 + 2 = 3` is prime. No swap is legal. The parity check fails immediately:

```
position 1 -> value 2
odd != even
```

The algorithm outputs `NO`, which is correct.

Now consider

```
1
3
3 2 1
```

The components are `{1,3}` and `{2}`.

The check gives:

```
position 1 -> value 3
position 2 -> value 2
position 3 -> value 1
```

Every position and value belong to the same component. Swapping `1` and `3` is allowed because their sum is `4`, so the permutation can be sorted. The algorithm outputs `YES`.

Finally, consider

```
1
5
5 4 3 2 1
```

For `n ≥ 5`, the graph is connected. Every value can reach every position through a sequence of allowed swaps. The algorithm immediately returns `YES`, matching the actual reachability structure of the graph.
