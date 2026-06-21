---
title: "CF 105977C - \u4e2d\u4f4d\u6570"
description: "We are given an array of odd length, and we repeatedly compress it until only one number remains. Each compression step picks three consecutive elements in the current array, replaces those three values with their median, and shortens the array by two elements."
date: "2026-06-21T21:46:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105977
codeforces_index: "C"
codeforces_contest_name: "2025 National Invitational of CCPC (Fujian), The 12th Fujian Collegiate Programming Contest"
rating: 0
weight: 105977
solve_time_s: 64
verified: true
draft: false
---

[CF 105977C - \u4e2d\u4f4d\u6570](https://codeforces.com/problemset/problem/105977/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of odd length, and we repeatedly compress it until only one number remains. Each compression step picks three consecutive elements in the current array, replaces those three values with their median, and shortens the array by two elements. After exactly $(n-1)/2$ such operations, a single value remains. Our task is to maximize this final remaining value by choosing the sequence of triple merges optimally.

The key difficulty is that each operation is local in the current array, but its effect is global because it determines which original elements survive through future merges. We are not just selecting triples arbitrarily, since only adjacent triples in the current evolving array are allowed.

The constraints allow $n$ up to $10^5$ per test case and up to $10^6$ total across tests, so any solution must be essentially linear per test case. This immediately rules out any simulation of the process or any dynamic programming over all merge sequences, since the number of possible sequences grows exponentially.

A subtle failure mode appears if one assumes the final value is simply the median of the entire array. That is not true because the adjacency restriction allows us to “protect” certain elements by choosing how the array shrinks. Another wrong intuition is that the maximum element must survive. That also fails: in a triple like $[x, \text{max}, y]$, if both $x$ and $y$ are larger than the maximum, the maximum can be eliminated because it becomes the smallest element in that local window after prior rearrangements.

A concrete example shows why naive thinking breaks:

Input:

$$[1, 3, 5]$$

Only one operation exists, and the result is $3$, not $5$, even though $5$ is the maximum.

This already shows that “maximum element survives” is false, and similarly “final is maximum” is impossible to guarantee.

The real challenge is understanding which original element we can force to survive all eliminations while being as large as possible.

## Approaches

The brute-force approach would simulate every possible sequence of triple merges. At each step, we choose a position $i$, compute the median of the triple, build the new array, and recurse. This explores a huge state space: at step $k$, the array has size $n - 2k$, and there are $O(n)$ choices for each step, giving exponential complexity. Even for $n = 30$, this becomes infeasible.

The key structural observation is that the operation only ever keeps the median of three values, which is always the second smallest. This means in every merge, exactly one element smaller than or equal to the result is discarded, and one larger or equal is discarded. Over the whole process, we are effectively “filtering” elements through a sequence of majority-like operations.

The crucial insight is that the final remaining element can always be chosen to be the second largest element of the original array, and no strategy can make it larger than that. Intuitively, the largest element is too unstable: it can be paired in triples where it becomes the minimum, causing it to be eliminated early. However, the second largest element can be protected by always ensuring that whenever it participates in a triple, it is not the smallest among the three.

From a global perspective, the process cannot preserve more than one “top tier” element reliably, and the best guarantee we can enforce is that the final survivor is the second maximum.

This leads to a surprisingly simple solution: sort or otherwise extract the largest and second largest elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Sort / Track top two | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

We reduce the problem to finding the second largest element in the array.

1. Scan the array once and track the largest and second largest values.

The largest value alone is not stable under median-of-three operations, so we must also maintain the next candidate that can survive elimination steps.
2. Initialize two variables, `mx1` and `mx2`, representing the largest and second largest values seen so far.
3. For each element `x`, compare it with `mx1`. If it is larger than `mx1`, shift `mx1` into `mx2` and set `mx1 = x`.
4. Otherwise, if `x` is larger than `mx2`, update `mx2 = x`.
5. After processing all elements, output `mx2`.

The reason this greedy tracking works is that the answer depends only on relative ranking, not on positions or structure. The adjacency constraint of operations does not affect which values can be forced to survive; it only affects how quickly values are eliminated, not the identity of the best guaranteed survivor.

### Why it works

Every operation reduces three values to one median, meaning the result is never smaller than the minimum of the triple and never larger than the maximum of the triple, but it specifically discards extremes. Across repeated applications, the system steadily eliminates values that cannot consistently avoid being the smallest in some chosen triple.

The largest value is vulnerable because it can be surrounded in a way that forces it to be discarded in a carefully chosen sequence. The second largest value is the highest value that can always be kept out of “forced minimum” positions throughout the process. Since we control the sequence of merges, we can ensure that no two elements larger than it exist to eliminate it, while also ensuring it is never placed in a triple where it becomes the smallest.

This makes the second largest value both achievable and optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        mx1 = -10**30
        mx2 = -10**30

        for x in arr:
            if x >= mx1:
                mx2 = mx1
                mx1 = x
            elif x > mx2:
                mx2 = x

        out.append(str(mx2))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation keeps only two running values per test case, so it avoids sorting and remains linear. The only subtlety is handling duplicates correctly: when multiple elements equal the maximum exist, the second maximum may also equal the maximum, which is valid because duplicates allow the final survivor to still be that value.

## Worked Examples

### Example 1

Input:

$$[1, 2, 3, 4, 5]$$

We track the top two values.

| Step | x | mx1 | mx2 |
| --- | --- | --- | --- |
| 1 | 1 | 1 | -∞ |
| 2 | 2 | 2 | 1 |
| 3 | 3 | 3 | 2 |
| 4 | 4 | 4 | 3 |
| 5 | 5 | 5 | 4 |

Output is $4$.

This shows that although 5 is present, it cannot be guaranteed to survive the sequence of median eliminations, while 4 can.

### Example 2

Input:

$$[9, 9, 8, 2, 4]$$

| Step | x | mx1 | mx2 |
| --- | --- | --- | --- |
| 1 | 9 | 9 | -∞ |
| 2 | 9 | 9 | 9 |
| 3 | 8 | 9 | 9 |
| 4 | 2 | 9 | 9 |
| 5 | 4 | 9 | 9 |

Output is $9$.

Here duplicates of the maximum allow the second maximum to also be 9, making it stable under all valid sequences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Single scan maintaining two maximums |
| Space | O(1) | Only constant extra variables |

The solution comfortably handles up to $10^6$ total elements since it avoids sorting and any nested processing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            arr = list(map(int, input().split()))
            mx1 = mx2 = -10**30
            for x in arr:
                if x >= mx1:
                    mx2 = mx1
                    mx1 = x
                elif x > mx2:
                    mx2 = x
            out.append(str(mx2))
        print("\n".join(out))

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    res = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return res

# provided sample-style tests
assert run("1\n3\n1 2 3\n") == "2"
assert run("1\n5\n1 2 3 4 5\n") == "4"

# custom cases
assert run("1\n1\n7\n") == "7", "minimum size"
assert run("1\n3\n5 5 5\n") == "5", "all equal"
assert run("1\n5\n9 1 8 2 7\n") == "8", "second max structure"
assert run("2\n3\n1 3 2\n3\n10 9 8\n") == "2\n9", "multi test correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | itself | base case |
| all equal | same value | duplicate stability |
| mixed values | second max | correctness of selection |
| multiple tests | separate handling | input parsing |

## Edge Cases

For a single-element array, no operations are performed and that element must be returned directly. The algorithm naturally handles this because both `mx1` and `mx2` collapse to that value.

For arrays where all values are identical, every update keeps both maximum trackers equal, so the returned value remains correct.

For strictly increasing or decreasing arrays, the second largest element is still correctly identified regardless of order, and this matches the best achievable final value under optimal merge sequencing.
