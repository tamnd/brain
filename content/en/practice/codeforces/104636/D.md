---
title: "CF 104636D - Watering System"
description: "We are given a pipe system with $n$ outlets, each outlet having a size $si$. Arkady pours a fixed amount of water $A$ into the system, but he is allowed to block any subset of outlets before doing so."
date: "2026-06-29T17:06:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104636
codeforces_index: "D"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u043c\u0430\u0441\u0441\u0438\u0432\u044b, \u0441\u0442\u0440\u043e\u043a\u0438"
rating: 0
weight: 104636
solve_time_s: 82
verified: false
draft: false
---

[CF 104636D - Watering System](https://codeforces.com/problemset/problem/104636/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a pipe system with $n$ outlets, each outlet having a size $s_i$. Arkady pours a fixed amount of water $A$ into the system, but he is allowed to block any subset of outlets before doing so. The water then distributes only among the unblocked outlets in proportion to their sizes.

The key rule is that if the unblocked outlets have total size $S$, then outlet $i$ receives $\frac{s_i}{S} \cdot A$ units of water. Our goal is to make sure the first outlet receives at least $B$ units of water. We are asked to minimize how many outlets we block to achieve this condition.

The first important observation is that blocking changes only the denominator of the fraction, not the numerator of the first outlet. The amount received by the first outlet depends only on how small we can make the sum of remaining sizes while still keeping the first outlet available.

Since $n$ can be as large as $100{,}000$, any solution that tries all subsets of blocked holes is impossible. Even checking all subsets would require $2^n$ operations, which is far beyond any feasible limit. Even sorting subsets or recomputing sums repeatedly would lead to at least $O(n^2)$ behavior in the worst case, which is also too slow.

The constraints on $A$ and $B$ are small ($\le 10^4$), but they are not the main limiting factor. The real bottleneck is the number of holes, which forces us into an $O(n \log n)$ or $O(n)$ solution.

A subtle edge case appears when the first hole already provides enough water without blocking anything. For example, if $s_1$ is very large compared to others, or if $B \cdot \sum s_i \le A \cdot s_1$, then the answer is zero. A naive approach might still try removing elements unnecessarily.

Another edge case is when we must block almost everything. If all other holes are large except the first, the optimal strategy is to keep only hole 1 and block the rest. Any incorrect greedy ordering that ignores the impact of large holes in the denominator will fail here.

## Approaches

The brute-force idea is straightforward: try every possible subset of holes to block, compute the resulting sum of remaining sizes, and check whether the first hole receives at least $B$ water. For each subset, we recompute the total size $S$, then evaluate whether $\frac{s_1}{S} \cdot A \ge B$. This works because it directly simulates the process described in the problem.

However, there are $2^n$ subsets, and even evaluating one subset takes $O(n)$ if done naively. This leads to an exponential algorithm that is completely infeasible for $n = 100{,}000$.

The key observation is that blocking holes other than the first only helps by reducing the denominator $S$. To maximize the water received by the first hole, we want to minimize $S$, which means we should remove the largest holes first. Each removed hole reduces the denominator as much as possible per removal operation.

This turns the problem into selecting how many of the largest non-first elements we remove, so that the inequality becomes true. Once we sort the other holes in descending order, we greedily remove them one by one until the condition is satisfied.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal (sorting + greedy removal) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We isolate the size of the first hole because it is always kept and directly determines the numerator of the final fraction.

We compute the initial total sum of all hole sizes, since this is the starting denominator before blocking anything.

We check whether no blocking is needed by verifying whether $A \cdot s_1 \ge B \cdot S$. If this already holds, we can immediately return zero because any blocking would only reduce $S$, but we are already satisfied.

We collect all holes except the first one and sort them in descending order of size. This ordering ensures that when we remove holes, we always reduce the denominator as aggressively as possible.

We then iterate through the sorted list, removing one hole at a time from the total sum and counting how many removals we perform. After each removal, we check whether the condition $A \cdot s_1 \ge B \cdot S$ is satisfied. The first time it becomes true, we stop and return the number of removed holes.

### Why it works

The process maintains a clear invariant: at any step, we have removed exactly the largest $k$ holes among all non-first holes. This guarantees that the current sum $S$ is the smallest possible sum achievable by removing any $k$ holes. Since the condition depends only on $S$, minimizing $S$ for a fixed number of removals is optimal, and therefore the first time the inequality holds corresponds to the minimal number of removals required.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, A, B = map(int, input().split())
    s = list(map(int, input().split()))
    
    s1 = s[0]
    others = s[1:]
    
    total = sum(s)
    
    if A * s1 >= B * total:
        print(0)
        return
    
    others.sort(reverse=True)
    
    removed = 0
    for x in others:
        total -= x
        removed += 1
        if A * s1 >= B * total:
            print(removed)
            return

    print(n - 1)

if __name__ == "__main__":
    solve()
```

The solution starts by reading the input and separating the first hole from the rest. This is important because the first hole is never blocked, so its contribution remains constant throughout the process.

We compute the total sum once and use it as the evolving denominator. The early exit check avoids unnecessary sorting and iteration when the initial configuration already satisfies the requirement.

Sorting the remaining holes in descending order ensures that each removal gives the maximum possible reduction in the denominator. During iteration, we continuously update the total and check the inequality in its cross-multiplied form to avoid floating-point errors.

The final fallback `n - 1` only triggers if even removing all other holes is insufficient, which corresponds to the case where only the first hole remains.

## Worked Examples

### Sample 1

Input:

```
4 10 3
2 2 2 2
```

We start with $s_1 = 2$ and total $S = 8$. We need $10 \cdot 2 \ge 3 \cdot S$, meaning $20 \ge 3S$, so $S \le 6.66$.

| Step | Removed holes | Remaining sum $S$ | Condition satisfied |
| --- | --- | --- | --- |
| 0 | none | 8 | no |
| 1 | 2 | 6 | yes |

After removing one hole of size 2, the total becomes 6, and the condition holds. So the answer is 1.

This confirms that greedy removal of the largest available hole is sufficient.

### Sample 2

Input:

```
4 80 20
2 1 4 3
```

Here $s_1 = 2$, total $S = 10$, requirement is $80 \cdot 2 \ge 20 \cdot S$, i.e. $160 \ge 20S$, so $S \le 8$.

| Step | Removed holes | Remaining sum $S$ | Condition satisfied |
| --- | --- | --- | --- |
| 0 | none | 10 | no |
| 1 | 4 | 6 | yes |

Removing the largest non-first hole immediately drops the sum enough to satisfy the constraint.

This shows that sometimes a single removal is sufficient and earlier termination is critical.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting the $n-1$ remaining holes dominates the runtime, while scanning is linear |
| Space | $O(n)$ | We store the list of hole sizes excluding the first |

The solution comfortably fits within constraints since $n \le 10^5$, and sorting at this scale is well within time limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, A, B = map(int, input().split())
    s = list(map(int, input().split()))
    
    s1 = s[0]
    others = s[1:]
    total = sum(s)
    
    if A * s1 >= B * total:
        return "0\n"
    
    others.sort(reverse=True)
    removed = 0
    
    for x in others:
        total -= x
        removed += 1
        if A * s1 >= B * total:
            return str(removed) + "\n"
    
    return str(n - 1) + "\n"

# provided samples
assert run("4 10 3\n2 2 2 2\n") == "1\n"
assert run("4 80 20\n2 1 4 3\n") == "1\n"

# custom cases
assert run("1 5 3\n10\n") == "0\n"  # only hole already satisfies
assert run("5 10 100\n1 9 9 9 9\n") == "4\n"  # must remove all but first
assert run("5 10 1\n5 4 3 2 1\n") == "0\n"  # already sufficient
assert run("6 10 50\n1 10 10 10 10 10\n") == "4\n"  # progressive removals
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal case |
| heavy requirement | 4 | near-full removal |
| already satisfied | 0 | no action needed |
| gradual threshold crossing | 4 | greedy correctness |

## Edge Cases

One edge case is when no blocking is required. For input like $n=1$, $s_1$ is the only hole, the denominator never changes, so the condition is checked once and returns zero immediately. The algorithm handles this via the early inequality check.

Another edge case is when all other holes are extremely large compared to the first. In such a case, the greedy loop will remove all of them. For example, if $s = [1, 100, 100, 100]$, the initial sum is 301 and the condition fails. After removing 100 three times, the sum becomes 1, and the condition becomes trivially satisfied. The algorithm correctly returns 3, which is optimal because any smaller number of removals leaves a larger denominator.

A final edge case is when floating-point errors could appear if implemented directly. The solution avoids this entirely by multiplying both sides of the inequality, ensuring all comparisons are done using integers, which keeps the logic stable even for maximum input sizes.
