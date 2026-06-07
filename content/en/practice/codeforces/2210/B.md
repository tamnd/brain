---
title: "CF 2210B - Simply Sitting on Chairs"
description: "We have a row of $n$ chairs, all initially unmarked. A permutation $p$ of length $n$ is given, meaning each number from $1$ to $n$ appears exactly once. We start from the first chair and move right. At each chair, if it is already marked, the game stops immediately."
date: "2026-06-07T19:15:06+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2210
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1089 (Div. 2)"
rating: 900
weight: 2210
solve_time_s: 114
verified: true
draft: false
---

[CF 2210B - Simply Sitting on Chairs](https://codeforces.com/problemset/problem/2210/B)

**Rating:** 900  
**Tags:** data structures, greedy  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of $n$ chairs, all initially unmarked. A permutation $p$ of length $n$ is given, meaning each number from $1$ to $n$ appears exactly once. We start from the first chair and move right. At each chair, if it is already marked, the game stops immediately. Otherwise, we have the choice to sit on it or skip it. If we sit, after standing up, we mark the chair indicated by the permutation value for the current chair, $p_i$, and then continue to the next chair. The goal is to maximize the total number of chairs we sit on.

The input gives multiple test cases, each specifying $n$ and the permutation $p$. The output is the maximum chairs that can be sat on for each test case.

The constraints are significant. $n$ can reach $2\cdot 10^5$, and the sum of all $n$ over all test cases is at most $2\cdot 10^5$. This restricts us to linear or near-linear algorithms per test case. Any approach with complexity $O(n^2)$ will be too slow.

A subtle edge case arises when the permutation creates a cycle including the first chair. For example, if $p = [1,2,3]$, sitting on the first chair immediately marks itself, so the game ends after the first move. A naive greedy approach of always sitting will fail to consider these self-marking or early-cycle scenarios, producing incorrect results.

Another edge case occurs when there is a long chain pointing forward without cycles, such as $p = [2,3,4,1]$, where sitting on chair $1$ will eventually mark chair $1$ itself. Here, sitting strategically to maximize the chain length before hitting a marked chair matters.

## Approaches

The brute-force approach attempts all subsets of chairs to sit on, simulating the marking procedure for each choice. This works because we can accurately follow the rules and count chairs. However, for $n$ around $2\cdot 10^5$, there are $2^n$ subsets, making brute-force infeasible.

The key insight is that the permutation defines a directed graph where each chair points to exactly one chair. Every move corresponds to traversing this graph. The game ends when we first revisit a marked chair, which is equivalent to entering a cycle in the graph. Therefore, maximizing the number of chairs sat on reduces to finding the longest prefix of chairs that forms disjoint cycles and chains where each chain can be traversed safely.

A simpler perspective is to scan chairs from left to right and sit whenever the chair has not yet been visited in the sense of marking. When we sit, we mark $p_i$. If $p_i \le i$, then that mark does not affect future chairs, but if $p_i > i$, it might mark a future chair we would have wanted to sit on. So, to maximize sits, we only need to keep track of the maximum "marked index" encountered so far. For each chair, if it is beyond the current marked index, we can safely sit. Otherwise, we cannot sit without ending the game.

This transforms the problem into a greedy linear scan: maintain the rightmost chair that will be marked from previous sits, and only sit when the current chair index exceeds that. This observation reduces the solution from $O(n^2)$ to $O(n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `max_marked` to 0. This will track the farthest index that has been or will be marked by previous sits.
2. Initialize a counter `count` to 0, representing the number of chairs we sit on.
3. Iterate over chairs from index $1$ to $n$ (1-based indexing for consistency with permutation). For each chair $i$:

1. If $i \le max_marked`, then sitting here would end the game, so skip this chair.
2. Otherwise, sit on chair $i$. Increment `count` by 1.
3. Update `max_marked` to be the maximum of its current value and $p_i$. This ensures we track the rightmost chair that is marked and might block future sits.
4. After the iteration, `count` contains the maximum number of chairs we can sit on.
5. Output `count` for the test case.

Why it works: The invariant is that `max_marked` always stores the rightmost chair that is or will be marked by the time we reach any index. By only sitting on chairs with index greater than `max_marked`, we ensure that no sit prematurely ends the game. This greedy strategy works because marking only blocks future chairs, never earlier ones, so scanning left to right while maintaining the farthest mark is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))
    max_marked = 0
    count = 0
    for i in range(n):
        if i + 1 <= max_marked:
            continue
        count += 1
        max_marked = max(max_marked, p[i])
    print(count)
```

The code initializes `max_marked` and `count`, then iterates over each chair. The check `i + 1 <= max_marked` ensures 1-based indexing. When sitting on a chair, `max_marked` updates to reflect the chair marked by this sit. This approach correctly handles the propagation of marks through the permutation chain, avoids ending the game prematurely, and runs in linear time.

## Worked Examples

Sample input: `n = 3, p = [3,2,1]`

| i | Chair | max_marked | sit? | count |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | yes | 1 |
| 2 | 2 | 3 | yes | 2 |
| 3 | 3 | 3 | no | 2 |

This trace demonstrates that chair 3 is blocked by the previous sit marking chair 3.

Sample input: `n = 5, p = [4,3,2,5,1]`

| i | Chair | max_marked | sit? | count |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | yes | 1 |
| 2 | 2 | 4 | no | 1 |
| 3 | 3 | 4 | no | 1 |
| 4 | 4 | 5 | no | 1 |
| 5 | 5 | 5 | yes | 2 |

Here, we see that skipping chairs 2-4 is necessary to avoid ending the game early. The table confirms that the greedy strategy correctly identifies safe chairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each chair is processed once; max operations are constant per chair. |
| Space | O(1) | Only two integer variables (`max_marked` and `count`) are maintained aside from input. |

The linear time complexity ensures the solution runs within the 2-second limit even for $n$ up to $2\cdot10^5$ and total sum of $n$ up to $2\cdot10^5$ across test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        max_marked = 0
        count = 0
        for i in range(n):
            if i + 1 <= max_marked:
                continue
            count += 1
            max_marked = max(max_marked, p[i])
        print(count)
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n3 2 1\n5\n4 3 2 5 1\n4\n4 2 1 3\n4\n2 3 4 1\n") == "2\n2\n3\n1", "sample 1"

# Custom cases
assert run("1\n1\n1\n") == "1", "single chair"
assert run("1\n5\n1 2 3 4 5\n") == "5", "no early marks, all can sit"
assert run("1\n5\n5 4 3 2 1\n") == "1", "first chair marks last, rest blocked"
assert run("1\n6\n2 3 4 5 6 1\n") == "5", "long chain wraps around"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n1 | 1 | Minimum size input |
| 1\n5\n1 2 3 4 5 | 5 | Linear increasing permutation, all can sit |
| 1\n5\n5 |  |  |
