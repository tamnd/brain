---
title: "CF 105020J - Hide and Seek"
description: "Each test case describes a park with several trees, where each tree has a fixed height. Amr chooses one tree to hide behind. Whether he gets caught depends only on a comparison between his height and the height of that chosen tree."
date: "2026-06-28T01:59:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105020
codeforces_index: "J"
codeforces_contest_name: "TCPC Tunisian Collegiate Programming Contest 2022"
rating: 0
weight: 105020
solve_time_s: 72
verified: false
draft: false
---

[CF 105020J - Hide and Seek](https://codeforces.com/problemset/problem/105020/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

Each test case describes a park with several trees, where each tree has a fixed height. Amr chooses one tree to hide behind. Whether he gets caught depends only on a comparison between his height and the height of that chosen tree.

The rule is simple: Gamal catches Amr only when the tree Amr is hiding behind is shorter than Amr himself. If the tree is tall enough or equal in height, Amr remains safe.

So for every tree, we are asked to decide independently whether its height is strictly less than a given value $x$, which represents Amr’s height. The output is a sequence of binary decisions, one per tree.

The constraints allow up to $10^3$ test cases and a total of $10^5$ trees overall. This already tells us the solution must process each height in constant time. Any approach that revisits elements multiple times per test case would still pass only if it stays linear overall. Anything quadratic, such as comparing every tree with every other tree, is far beyond the limit because it would reach $10^{10}$ operations in the worst case.

The main edge cases come from boundary comparisons around equality and extremes:

If all trees have height equal to $x$, none should be counted as caught. For example, $x = 5$, heights $[5, 5, 5]$, output must be $[0, 0, 0]$. A careless implementation using $\leq$ instead of strict comparison would incorrectly mark all as caught.

If all trees are shorter than $x$, for example $x = 10$, heights $[1, 2, 9]$, then every position should return $1$. Any mistake in flipping the condition would invert the result completely.

If trees include values greater than $x$, those must be safe positions even though they are not equal, which can trip implementations that only check equality or use incorrect boolean logic.

## Approaches

The brute-force idea is to treat each tree independently. For every tree, we compare its height with Amr’s height and decide whether it satisfies the “strictly smaller” condition. This already gives a correct solution because the decision for one tree does not depend on any other tree.

A naive misunderstanding would be to recompute or scan additional structure per tree, but nothing in the problem requires interaction between positions. Even a double loop that, for each tree, compares against all others would be unnecessary and wasteful. That would lead to $O(n^2)$ behavior per test case, which in the worst case means around $10^{10}$ comparisons and is completely infeasible.

The key observation is that the condition is purely local. Each output depends only on a single comparison $h_i < x$. This eliminates the need for any preprocessing or data structures. We can process the array in one pass and emit answers immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is independent, so no information needs to be carried across them.
2. For each test case, read $n$ and $x$, which define how many trees exist and Amr’s height.
3. Read the list of tree heights. Each value will be checked exactly once.
4. For each height $h_i$, compare it directly with $x$. If $h_i < x$, output 1, otherwise output 0. This works because the problem condition defines a strict inequality as the only way Amr gets caught.
5. Print all results for the test case in a single line to match the required format.

### Why it works

Each decision is independent and based solely on whether a single number lies below a fixed threshold $x$. There is no hidden interaction between trees, so the output is exactly the result of applying a simple predicate $h_i < x$ to every element. Since the predicate is evaluated once per element, no incorrect coupling between positions can occur, and the result must match the problem definition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out_lines = []

    for _ in range(t):
        n, x = map(int, input().split())
        h = list(map(int, input().split()))

        res = []
        for hi in h:
            if hi < x:
                res.append("1")
            else:
                res.append("0")

        out_lines.append(" ".join(res))

    print("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algorithm exactly. Each test case is handled in isolation, and for every tree height we perform a single comparison. The result is accumulated as strings to avoid repeated printing overhead, which keeps the solution efficient in Python under tight constraints.

A common pitfall here is accidentally using `<=` instead of `<`, which would incorrectly mark equal-height trees as caught. Another subtle issue is printing per element instead of joining results, which can slow down Python significantly when $n$ is large.

## Worked Examples

### Example 1

Input:

```
n = 5, x = 4
heights = [1, 4, 2, 7, 3]
```

| i | h_i | h_i < x | output |
| --- | --- | --- | --- |
| 1 | 1 | true | 1 |
| 2 | 4 | false | 0 |
| 3 | 2 | true | 1 |
| 4 | 7 | false | 0 |
| 5 | 3 | true | 1 |

Output:

```
1 0 1 0 1
```

This trace shows that equality with $x$ does not count as caught, only strict inequality matters.

### Example 2

Input:

```
n = 4, x = 6
heights = [6, 6, 1, 10]
```

| i | h_i | h_i < x | output |
| --- | --- | --- | --- |
| 1 | 6 | false | 0 |
| 2 | 6 | false | 0 |
| 3 | 1 | true | 1 |
| 4 | 10 | false | 0 |

Output:

```
0 0 1 0
```

This example highlights that values greater than $x$ are also safe, reinforcing that the condition is strictly about being below the threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each tree height is checked exactly once against $x$ |
| Space | $O(1)$ auxiliary | Only output storage is used aside from input array |

The total number of tree checks across all test cases is at most $10^5$, which fits comfortably within the limit of a linear scan. Memory usage stays minimal since no additional structures are required.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, x = map(int, input().split())
        h = list(map(int, input().split()))
        res = ["1" if hi < x else "0" for hi in h]
        out.append(" ".join(res))
    print("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided sample (formatted consistently)
assert run("""1
5 4
1 4 2 7 3
""") == "1 0 1 0 1"

# all equal case
assert run("""1
3 5
5 5 5
""") == "0 0 0"

# all smaller
assert run("""1
4 10
1 2 3 4
""") == "1 1 1 1"

# all larger
assert run("""1
4 2
5 6 7 8
""") == "0 0 0 0"

# boundary mix
assert run("""1
5 3
3 2 3 1 4
""") == "0 1 0 1 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal to x | all 0 | strict inequality correctness |
| all smaller | all 1 | full acceptance case |
| all larger | all 0 | rejection case |
| boundary mix | mixed | correct per-element logic |

## Edge Cases

When every tree has height exactly equal to $x$, the algorithm evaluates each comparison as false, producing a sequence of zeros. For an input like $x = 5$, heights $[5, 5, 5]$, each check $h_i < x$ fails, so no position is marked as caught.

When all trees are strictly below $x$, every comparison succeeds. For $x = 10$, heights $[1, 2, 9]$, each comparison returns true and the output becomes all ones.

When values exceed $x$, the comparison naturally filters them out without special handling. For $x = 3$, heights $[4, 5]$, both are greater and therefore safe, producing zeros consistently.
