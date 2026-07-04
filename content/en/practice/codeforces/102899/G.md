---
title: "CF 102899G - KK \u770b\u8df3\u821e"
description: "We are given multiple test cases. Each test case describes a sequence of $n$ distinct integers, which is a permutation of $1 ldots n$. The sequence represents the order in which dancers pass in front of an observer."
date: "2026-07-04T08:21:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102899
codeforces_index: "G"
codeforces_contest_name: "The 2nd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102899
solve_time_s: 42
verified: true
draft: false
---

[CF 102899G - KK \u770b\u8df3\u821e](https://codeforces.com/problemset/problem/102899/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple test cases. Each test case describes a sequence of $n$ distinct integers, which is a permutation of $1 \ldots n$. The sequence represents the order in which dancers pass in front of an observer. At the moment of observation, the dancers are arranged in a circle and moving either clockwise or counterclockwise. Because of this circular motion, what the observer sees is a consecutive segment of the circle, but that segment could be read in either direction depending on orientation.

The task is to decide whether the observed sequence could come from taking a circular arrangement of $1 \ldots n$ and reading all elements consecutively either in clockwise order or in counterclockwise order. In other words, we are asked whether the permutation is a circular rotation of the identity order or a circular rotation of the reversed order.

The constraint $n \le 10^4$ per test case and at most 10 test cases implies a total input size around $10^5$. This rules out any $O(n^2)$ comparison per test case as borderline but still potentially acceptable only with small constants. However, the structure suggests a much simpler linear check is sufficient.

A naive misunderstanding often happens here: one might think any permutation that can be reordered into a cycle is valid, but the condition is stricter. The sequence must be monotone around the circle without jumps.

A few subtle edge cases illustrate the requirement.

Consider $n = 4$, sequence $[1, 3, 2, 4]$. This is not a single-direction traversal of the circle, because after going from 1 to 3, we skip 2 and then go back, which breaks adjacency on the cycle.

Consider $n = 5$, sequence $[3, 4, 5, 1, 2]$. This is valid because it is a rotation of the sorted order.

Consider $n = 4$, sequence $[4, 3, 2, 1]$. This is also valid because it corresponds to reversed traversal.

The key property is adjacency modulo $n$.

## Approaches

A brute-force idea is to try every possible starting point in the circle and attempt to match the sequence either in increasing or decreasing order modulo $n$. For each starting index, we simulate traversal and check whether the permutation aligns. Each simulation costs $O(n)$, and there are $n$ starting positions, leading to $O(n^2)$ per test case. With $n = 10^4$, this becomes $10^8$ operations per test case, which is too slow for the time limit.

The structure of the problem removes the need to try all rotations. If the sequence is valid, then every consecutive pair must represent neighbors on the cycle. That means once we fix the direction using the first step, all subsequent steps are forced. The only ambiguity is direction: increasing order or decreasing order modulo $n$.

So instead of checking all rotations, we check whether the permutation is consistent with either a +1 step sequence modulo $n$ (with wrap-around) or a -1 step sequence modulo $n$. This reduces the problem to two linear scans.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We treat the numbers as points on a cycle of length $n$, where after $n$ comes 1 and before 1 comes $n$.

1. Read the sequence and compute differences between consecutive elements under modulo $n$. Instead of raw subtraction, we normalize adjacency as whether two consecutive numbers differ by exactly 1 forward or 1 backward on the cycle. This means for adjacent values $a$ and $b$, we check whether $b = a + 1$, $b = a - 1$, or the wrap cases $(a, b) = (n, 1)$ or $(1, n)$.
2. Determine the direction from the first pair. If the first transition is increasing by 1 (including wrap from $n \to 1$), we test the entire sequence assuming forward direction. If it is decreasing by 1 (including wrap from $1 \to n$), we test the backward direction. If neither holds, the answer is immediately NO.
3. For the chosen direction, scan the sequence from left to right and verify that every adjacent pair follows the same step rule. The direction must remain consistent for all transitions.
4. If all transitions match for either forward or backward direction, output YES, otherwise output NO.

### Why it works

A valid circular traversal has a rigid local structure: every element has exactly two neighbors on the cycle. Once we observe two consecutive elements, we determine which neighbor relationship is being used. Because the cycle is uniform, this local decision determines the global structure. If any later transition deviates from this adjacency pattern, the sequence cannot correspond to a continuous traversal of the cycle in any direction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check(a):
    n = len(a)

    def ok_forward():
        for i in range(n - 1):
            if a[i + 1] != a[i] + 1 and not (a[i] == n and a[i + 1] == 1):
                return False
        return True

    def ok_backward():
        for i in range(n - 1):
            if a[i + 1] != a[i] - 1 and not (a[i] == 1 and a[i + 1] == n):
                return False
        return True

    return ok_forward() or ok_backward()

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print("YES" if check(a) else "NO")
```

The implementation directly encodes the two possible traversals of the cycle. The forward check enforces that every step increments by one, except for the special wrap case from $n$ back to $1$. The backward check symmetrically enforces decrements with wrap from $1$ to $n$.

A subtle point is that we do not attempt to “rotate” the sequence. Rotation is irrelevant because adjacency is preserved under rotation. Any valid cycle traversal will satisfy the adjacency property regardless of starting point.

## Worked Examples

### Example 1: $[1, 2, 3, 4]$

| i | a[i] | a[i+1] | Check |
| --- | --- | --- | --- |
| 0 | 1 | 2 | +1 valid |
| 1 | 2 | 3 | +1 valid |
| 2 | 3 | 4 | +1 valid |

Forward check passes completely, so output is YES.

Backward check fails immediately at first transition since 2 is not 0 or wrap from 1.

This demonstrates a clean monotone traversal in one direction.

### Example 2: $[3, 2, 1, 4]$

| i | a[i] | a[i+1] | Check |
| --- | --- | --- | --- |
| 0 | 3 | 2 | -1 valid |
| 1 | 2 | 1 | -1 valid |
| 2 | 1 | 4 | wrap valid |

Backward direction holds throughout, so output is YES.

This confirms that rotations of reversed order are accepted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each test case scans the array a constant number of times |
| Space | $O(1)$ | No auxiliary structures beyond input storage |

With $\sum n \le 10^5$, the solution runs comfortably within limits because each element is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        def check(a):
            n = len(a)

            def ok_forward():
                for i in range(n - 1):
                    if a[i + 1] != a[i] + 1 and not (a[i] == n and a[i + 1] == 1):
                        return False
                return True

            def ok_backward():
                for i in range(n - 1):
                    if a[i + 1] != a[i] - 1 and not (a[i] == 1 and a[i + 1] == n):
                        return False
                return True

            return ok_forward() or ok_backward()

        output.append("YES" if check(a) else "NO")
    return "\n".join(output)

# sample-like tests
assert run("1\n3\n1 2 3\n") == "YES"
assert run("1\n3\n1 3 2\n") == "YES"

# custom tests
assert run("1\n4\n1 3 2 4\n") == "NO"
assert run("1\n4\n4 3 2 1\n") == "YES"
assert run("1\n5\n2 3 4 5 1\n") == "YES"
assert run("1\n5\n1 3 2 4 5\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 3 / 1 2 3 | YES | basic forward cycle |
| 1 3 / 1 3 2 | YES | reverse cycle |
| 1 4 / 1 3 2 4 | NO | broken adjacency |
| 1 4 / 4 3 2 1 | YES | full reverse |
| 1 5 / 2 3 4 5 1 | YES | rotation of cycle |
| 1 5 / 1 3 2 4 5 | NO | mixed jumps |

## Edge Cases

A minimal case like $n = 1$ always passes, since a single element trivially forms both a forward and backward cycle.

For $n = 2$, both $[1, 2]$ and $[2, 1]$ are valid because each step is a valid neighbor move on a two-node cycle. The algorithm accepts both since each direction check succeeds immediately.

For wrap-heavy sequences such as $[n, 1, 2, \ldots, n-1]$, the forward check validates the wrap transition from $n \to 1$ and continues consistently. The backward check fails immediately, but only one direction is required.

For mixed sequences like $[1, 3, 2, 4]$, the first transition might suggest a direction, but the second transition violates adjacency. The scan detects this immediately at the second comparison, preventing any false acceptance.
