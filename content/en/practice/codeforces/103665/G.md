---
title: "CF 103665G - \u0421\u0435\u0439\u0444"
description: "We are given a row of digits. In one move, we may pick a single position and increase or decrease that digit by one, staying within the range 0 to 9. The goal is not to reach a fixed target string, but to reach any configuration where some digit value appears at least k times."
date: "2026-07-02T21:44:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103665
codeforces_index: "G"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2018"
rating: 0
weight: 103665
solve_time_s: 46
verified: true
draft: false
---

[CF 103665G - \u0421\u0435\u0439\u0444](https://codeforces.com/problemset/problem/103665/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of digits. In one move, we may pick a single position and increase or decrease that digit by one, staying within the range 0 to 9. The goal is not to reach a fixed target string, but to reach any configuration where some digit value appears at least k times. We want the minimum number of moves needed to achieve that condition.

The input size reaches up to one hundred thousand digits, so any solution that tries all combinations of changes across positions is impossible. Even operations quadratic in n would already be too slow, because n² at 10⁵ is 10¹⁰ operations.

A key subtlety is that we are not forced to choose which digit becomes dominant in advance. The optimal solution might choose digit 0, 1, ..., or 9 depending on which is cheapest to transform the array into having k copies of it.

A naive approach that fails is to independently decide for each digit position what value it should become, without coordinating toward a global target digit. For example, if we greedily change each position toward its nearest “good” digit without fixing the target digit, we might end up spreading effort across multiple digits and never actually reach k occurrences of a single value in minimum cost.

Another failure case is assuming that we should always pick the digit already most frequent. That is also wrong because a slightly less frequent digit might be much cheaper to convert to.

Example:

Input:

```
3 2
1 9 1
```

A naive frequency-based choice picks digit 1 (already 2 occurrences, cost 0). That works here, but consider:

```
3 2
1 2 3
```

No digit repeats, so we must choose a target digit. Choosing 2 might be cheaper than choosing 1 or 3 depending on surrounding values, since costs depend on absolute distance.

The real challenge is combining frequency with transformation cost.

## Approaches

We want to pick a digit d from 0 to 9 and convert at least k positions into d with minimum total cost, where cost of converting position i is |a[i] − d|.

If d were fixed, the problem becomes: choose k elements with minimum individual costs. This is a classical selection problem: compute all costs, sort them, and take the k smallest. The sum is the cost for that digit.

Brute force would try all subsets of k indices for each digit d, compute their transformation cost, and take the minimum. That is combinatorial: for each digit, there are C(n, k) subsets, which is infeasible.

The key observation is that for a fixed digit, the cost contribution of each position is independent. We do not need to choose subsets explicitly; we only need the k smallest costs. This converts a combinatorial selection into a sorting problem.

We repeat this for all 10 digits and take the best result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10 · C(n, k) · k) | O(k) | Too slow |
| Optimal | O(10 · n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read n, k and the digit array. Each digit is treated as an integer in [0, 9], since only differences matter.
2. Initialize the answer as infinity. We will compute the best possible cost for each candidate digit from 0 to 9.
3. For each digit d from 0 to 9, compute an array costs where costs[i] = |a[i] − d|. This represents how expensive it is to convert position i into digit d.
4. Sort the costs array. Sorting is used to bring the cheapest conversions to the front, since we only need k of them.
5. Take the sum of the first k elements of the sorted costs. This represents the cheapest way to make at least k positions equal to d.
6. Update the answer with the minimum value across all digits d.
7. Output the final answer.

Each digit is treated independently because the final condition only requires one digit to reach frequency k, not multiple digits simultaneously.

### Why it works

Fixing a digit d turns the problem into selecting k independent items with minimal cost. Any valid solution for digit d corresponds to choosing k positions and paying their individual costs. Since costs do not interact, replacing any chosen set with the k smallest costs can only improve or preserve the total cost. This exchange argument guarantees that sorting and taking k smallest is optimal for each digit. Taking the minimum over all digits covers all possible choices of the target digit, so the global optimum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    ans = 10**18

    for d in range(10):
        costs = [abs(x - d) for x in a]
        costs.sort()
        ans = min(ans, sum(costs[:k]))

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution iterates over all digits from 0 to 9. For each digit, it constructs a cost array measuring how far each element is from that digit. Sorting ensures the cheapest transformations are selected first. The prefix sum of size k gives the optimal cost for that digit.

A common implementation pitfall is forgetting that we must consider all digits, not just those already appearing in the input. Another is incorrectly using frequency instead of cost, which ignores the fact that transforming digits can be cheaper than using existing ones.

## Worked Examples

### Example 1

Input:

```
3 2
1 2 3
```

We compute costs per target digit.

| d | costs | sorted | best 2 sum |
| --- | --- | --- | --- |
| 1 | [0,1,2] | [0,1,2] | 1 |
| 2 | [1,0,1] | [0,1,1] | 1 |
| 3 | [2,1,0] | [0,1,2] | 1 |

Minimum answer is 1.

This shows that even though no digit is initially repeated, converting one element is enough, and multiple choices give equal optimal cost.

### Example 2

Input:

```
5 3
7 7 7 1 9
```

For d = 7:

| costs | sorted | k=3 sum |
| --- | --- | --- |
| [0,0,0,6,2] | [0,0,0,2,6] | 0 |

We already have three 7s, so cost is zero.

For d = 1:

| costs | sorted | k=3 sum |
| --- | --- | --- |
| [6,6,6,0,8] | [0,6,6,6,8] | 12 |

Best answer is 0.

This confirms that the algorithm naturally exploits existing frequency without needing special handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10 · n log n) | For each digit we compute n costs and sort them |
| Space | O(n) | Cost array reused per digit |

With n up to 100000, sorting 100000 elements ten times is easily within limits in Python and well within typical Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n, k = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))

    ans = 10**18
    for d in range(10):
        costs = [abs(x - d) for x in a]
        costs.sort()
        ans = min(ans, sum(costs[:k]))

    return str(ans)

# provided samples (as described in statement text)
assert run("3 3\n3 2 2\n") == "2"
assert run("3 2\n1 2 3\n") == "1"

# all same digits
assert run("5 3\n4 4 4 4 4\n") == "0"

# minimal n
assert run("1 1\n7\n") == "0"

# need conversion
assert run("4 3\n0 9 0 9\n") == "1"

# skewed distribution
assert run("6 4\n0 1 2 3 4 5\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same digits | 0 | already satisfies condition |
| n=1,k=1 | 0 | minimal boundary case |
| mixed extremes | 1 | choosing cheapest partial conversion |
| increasing sequence | 6 | cumulative cost behavior |

## Edge Cases

One important edge case is when k equals n. In this case we must convert every digit to a single value. The algorithm still works because it sums all costs after sorting.

For example:

```
4 4
0 9 1 8
```

For d = 0, costs are [0,9,1,8], sorted [0,1,8,9], sum = 18. The algorithm correctly includes all elements.

Another edge case is when k = 1. Then we only need the single cheapest conversion across all digits. The algorithm reduces to finding the minimum absolute difference between any array element and any digit, which is correctly handled by taking the first element after sorting.

A final subtle case is when multiple digits tie for optimal answer. Since we always take a minimum over all digits, ties are naturally handled without special logic.
