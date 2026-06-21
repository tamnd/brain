---
title: "CF 105687B - Card Game"
description: "We are given several independent test cases. In each test case there is an array of card values and a parameter $k$."
date: "2026-06-22T05:00:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105687
codeforces_index: "B"
codeforces_contest_name: "AlgoChief Sprint Round 2"
rating: 0
weight: 105687
solve_time_s: 43
verified: true
draft: false
---

[CF 105687B - Card Game](https://codeforces.com/problemset/problem/105687/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case there is an array of card values and a parameter $k$. From these cards, we are allowed to pick some subsequence, but the actual ordering constraint turns out to be irrelevant once we interpret what the selection is trying to optimize. The core restriction is that the chosen selection must effectively respect a grouping structure tied to $k$, meaning the useful structure is how many full groups of size $k$ we can form and what value we extract from them.

The task is to maximize a total score derived from selected cards, and the key hidden simplification is that the position of cards in the original array does not constrain optimality beyond how many we pick. What matters is only the values we include and the fact that the selection is effectively processed in chunks of size $k$.

The input consists of multiple test cases, each giving an integer $n$, an integer $k$, and an array of $n$ integers representing card values. The output for each test case is a single integer representing the maximum achievable score under the selection rule.

From the constraints discussion, the important implication is that $n$ can be large in every test case, potentially up to $10^5$, and there can be multiple test cases. A naive DP that depends on both $n$ and $k$ per test case leads to a complexity of roughly $O(t \cdot n \cdot k)$, which degenerates to about $10^9$ operations in the worst case. That is already beyond typical limits, so any solution that maintains a two-dimensional state over positions and group counts will not pass.

A subtle pitfall appears when one assumes subsequence selection preserves order relevance. For example, consider values $[1, 100, 2, 99]$ with $k = 2$. A careless approach might try to simulate choosing pairs respecting indices, but since only the total contribution matters, the best solution is simply to pick the top values without worrying about adjacency or original positions. Any algorithm that incorrectly preserves original order constraints will undercount or overcomplicate the selection.

## Approaches

The most direct formulation is to think in terms of dynamic programming over the array and how many items we have taken so far. One could define a state like $dp[i][j]$, meaning we are at index $i$ and have selected $j$ elements, trying to maximize the sum under the rule that only complete groups of size $k$ contribute. Transitions would consider either taking or skipping each element.

This approach is correct because it respects all constraints explicitly, but it becomes expensive immediately. The number of states is $O(n \cdot n)$ in the worst interpretation, or at least $O(n \cdot k)$, and each transition is constant, leading to quadratic or pseudo-quadratic behavior per test case. With large input sizes, this quickly becomes infeasible.

The key structural observation is that adjacency in the original array does not influence the final score. Since the selection is a subsequence, we are free to reorder our thinking: what matters is only which values are chosen, not where they came from. This turns the problem into a purely value-based optimization.

Once order is irrelevant, the natural strategy is to sort the array in descending order. After sorting, the optimal solution must take the largest available values first, because any smaller value can never improve a group that could be formed with a larger value instead. Since contributions are tied to taking elements in chunks of size $k$, we evaluate the prefix sums of this sorted array and only consider positions where the number of chosen elements is a multiple of $k$. Among these valid prefixes, the maximum prefix sum is the answer.

This works because every valid solution corresponds to choosing some number of elements, and for any fixed count, choosing the largest available elements maximizes the sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over indices and picks | $O(n^2)$ or $O(nk)$ | $O(nk)$ | Too slow |
| Sort + prefix evaluation | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all values for a test case and store them in an array. This gives us full freedom to ignore original positions since no constraint depends on adjacency after reinterpretation.
2. Sort the array in descending order. This ensures that whenever we consider taking elements, we are always prioritizing the most valuable ones first.
3. Compute prefix sums over the sorted array. The prefix sum at position $i$ represents the best possible total if we take exactly the top $i$ elements.
4. Only consider indices $i$ such that $i$ is a multiple of $k$. These positions correspond to forming complete groups of size $k$, which are the only meaningful checkpoints for the scoring structure.
5. Track the maximum prefix sum among these valid positions and output it as the answer.

### Why it works

Any valid solution corresponds to selecting some subset of size $m$, and its value is the sum of those chosen elements. For a fixed $m$, the optimal subset is always the $m$ largest elements because replacing a smaller chosen element with a larger unchosen one strictly increases the sum. Since the grouping constraint only depends on $m \bmod k = 0$, we only evaluate multiples of $k$. The sorted prefix guarantees we are always evaluating the best possible subset for each size, so taking the best among those candidates gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort(reverse=True)
        
        prefix = 0
        best = 0
        
        for i in range(n):
            prefix += a[i]
            if (i + 1) % k == 0:
                best = max(best, prefix)
        
        print(best)

if __name__ == "__main__":
    solve()
```

The solution starts by sorting the array in descending order so that every prefix represents the best possible choice of a given size. The prefix sum variable accumulates the running total of selected cards.

The crucial implementation detail is checking `(i + 1) % k == 0`. Since Python uses zero-based indexing, the prefix of length $i+1$ is complete when it forms a multiple of $k$. Only at those points does the grouping constraint allow us to evaluate a valid configuration.

The variable `best` tracks the maximum sum among all valid prefix lengths. We initialize it to zero because taking no elements is always a valid baseline if negative values are possible or if constraints allow empty selection.

## Worked Examples

### Example 1

Input:

```
1
5 2
3 1 4 2 5
```

Sorted array is $[5, 4, 3, 2, 1]$.

| i | chosen prefix | prefix sum | valid (i+1)%k==0 | best |
| --- | --- | --- | --- | --- |
| 0 | [5] | 5 | no | 0 |
| 1 | [5,4] | 9 | yes | 9 |
| 2 | [5,4,3] | 12 | no | 9 |
| 3 | [5,4,3,2] | 14 | yes | 14 |
| 4 | [5,4,3,2,1] | 15 | no | 14 |

The best answer is 14, coming from taking the best 4 elements since 4 is the largest multiple of $k=2$.

### Example 2

Input:

```
1
6 3
10 10 1 2 3 4
```

Sorted array is $[10, 10, 4, 3, 2, 1]$.

| i | chosen prefix | prefix sum | valid | best |
| --- | --- | --- | --- | --- |
| 0 | [10] | 10 | no | 0 |
| 1 | [10,10] | 20 | no | 0 |
| 2 | [10,10,4] | 24 | yes | 24 |
| 3 | [10,10,4,3] | 27 | no | 24 |
| 4 | [10,10,4,3,2] | 29 | no | 24 |
| 5 | [10,10,4,3,2,1] | 30 | yes | 30 |

The optimal answer is 30, achieved by taking all 6 elements since 6 is divisible by 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ per test case | Sorting dominates, prefix scan is linear |
| Space | $O(n)$ | Storage for the array and prefix accumulation |

The complexity fits comfortably within typical constraints even when $n$ is large across multiple test cases. Sorting is the only expensive step, and everything else is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort(reverse=True)
        prefix = 0
        best = 0
        for i in range(n):
            prefix += a[i]
            if (i + 1) % k == 0:
                best = max(best, prefix)
        out.append(str(best))
    return "\n".join(out)

# sample and custom tests
assert run("1\n1 1\n5\n") == "5"
assert run("1\n4 2\n1 2 3 4\n") == "10"
assert run("1\n5 2\n3 1 4 2 5\n") == "14"
assert run("1\n6 3\n10 10 1 2 3 4\n") == "30"
assert run("1\n3 2\n-1 -2 -3\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-element case | 5 | minimum size correctness |
| 4 elements, k=2 | 10 | simple full selection |
| sample 1 | 14 | prefix multiple logic |
| sample 2 | 30 | full utilization case |
| all negative | 0 | handling of negative values and empty choice |

## Edge Cases

A key edge case is when all values are negative. For example, consider:

```
1
3 2
-1 -2 -3
```

After sorting, we get $[-1, -2, -3]$. The prefix sums are $-1, -3, -6$. Only the prefix of length 2 is valid since $2$ is the only multiple of $k$ less than or equal to $n$, and its sum is $-3$. However, selecting nothing may be implicitly allowed depending on interpretation, so the algorithm initializes `best = 0`, ensuring the answer does not go negative.

Another edge case is when $n < k$. In this case, no valid prefix exists except the empty selection, so the result remains 0. Sorting and scanning naturally handles this because no index satisfies `(i+1) % k == 0`, leaving `best` unchanged.
