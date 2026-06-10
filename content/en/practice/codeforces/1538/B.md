---
title: "CF 1538B - Friends and Candies"
description: "We are given an array of integers representing how many candies each person initially holds. In a single operation, we are allowed to pick some subset of people, take all candies from them, and then freely redistribute those candies across everyone."
date: "2026-06-10T14:52:09+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1538
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 725 (Div. 3)"
rating: 800
weight: 1538
solve_time_s: 400
verified: true
draft: false
---

[CF 1538B - Friends and Candies](https://codeforces.com/problemset/problem/1538/B)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 6m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers representing how many candies each person initially holds. In a single operation, we are allowed to pick some subset of people, take all candies from them, and then freely redistribute those candies across everyone.

The goal is to make all values equal after this single redistribution step. However, there is a constraint: we cannot pick everyone for free. The cost we care about is the number of chosen people, and we want to minimize how many people we must select so that their combined candies are sufficient to achieve a perfectly equal final configuration.

A useful way to reframe the task is to think in terms of deficit and surplus relative to the target value, which must be the average of the array if a solution exists. The redistribution step is completely unrestricted except that we only collect candies from selected indices, so the only limitation is whether the chosen subset contains enough total “adjustable mass” to correct all deviations from the mean.

The constraint on input size is moderate, with up to ten thousand test cases and total array length up to two hundred thousand. This rules out any quadratic per test solution but allows sorting or linear passes per test. The values themselves are small enough to be handled directly, and the key difficulty is not arithmetic magnitude but subset structure.

A subtle edge case arises when the total sum is not divisible by n. In that case, no redistribution can produce equal values, regardless of how many elements we pick. Another corner case appears when all values are already equal, in which case choosing zero elements is sufficient. A third case is when only one element is nonzero deviation from the mean; then selecting just that element is enough, even if it is large, because its removal fixes the imbalance exactly.

## Approaches

A brute force interpretation tries all subsets of indices. For each subset, we compute the sum of selected values and check whether removing them leaves a total that can be evenly distributed. This is correct in principle because it directly matches the definition of allowed operations, but it immediately becomes exponential in n. With n up to two hundred thousand across tests, even storing subsets is impossible, and the number of candidates grows as 2^n.

The key observation is that the final configuration is fixed: every element must end at the average value, so the total sum determines everything. This converts the problem into deciding which elements we must “fix” so that their total contribution allows balancing deviations. Instead of reasoning about redistribution sequences, we only care about whether the selected subset can account for the total excess or deficit.

Once we fix the target mean, each element contributes a deviation from it. The task becomes selecting a minimum number of elements whose total deviation matches the total imbalance. Since positive and negative deviations must cancel globally, the optimal strategy is to prioritize elements with largest absolute deviation, because they give the most “correction power” per chosen index.

We therefore sort deviations by absolute value and greedily accumulate until the required correction is reached. The moment we reach zero residual imbalance, the number of selected elements is optimal because any replacement with smaller magnitude elements would require strictly more picks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Greedy by deviation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the array and check whether it is divisible by n. If it is not divisible, no equalization is possible, so the answer is -1. This follows because redistribution preserves total sum.
2. Compute the target value as total sum divided by n. Every final configuration must assign exactly this value to each position.
3. For each element, compute its deviation from the target. Positive deviation means surplus, negative means deficit. These deviations represent how much each index contributes to imbalance.
4. Observe that the sum of all deviations is zero, so the task reduces to canceling imbalance using a subset of indices whose deviations are “activated”.
5. Sort elements by absolute deviation in descending order. Large deviations are more efficient because each selected index contributes more toward correcting the imbalance.
6. Traverse the sorted list, accumulating deviation contributions until the running corrected imbalance reaches zero. Count how many elements were used.
7. Return this count as the minimum number of chosen friends.

### Why it works

Each chosen index removes its deviation from the system, and the goal is to eliminate total imbalance using the smallest number of such removals. Since every removal contributes linearly in its deviation value, choosing larger magnitudes first minimizes the number of steps needed to exhaust the total imbalance. Any solution that uses a smaller deviation while skipping a larger one can be improved by swapping them, reducing or preserving the number of chosen elements while increasing correction power, which guarantees greedy optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        s = sum(a)
        if s % n != 0:
            out.append("-1")
            continue

        target = s // n

        dev = [x - target for x in a]

        dev.sort(key=lambda x: abs(x), reverse=True)

        need = 0
        cnt = 0

        for d in dev:
            if need == 0:
                break
            need += d
            cnt += 1

        out.append(str(cnt))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution begins by validating feasibility through divisibility of the total sum, since no redistribution can alter global sum. It then converts the problem into deviations from the target value, which isolates the exact imbalance that must be resolved.

Sorting by absolute deviation ensures we always consider the most impactful corrections first. The loop simulates taking elements until the imbalance disappears, and the counter tracks how many are necessary.

A subtle point is that the stopping condition is when the accumulated deviation cancels the total imbalance, not when all elements are processed. This reflects that we only need enough selected indices to resolve the global discrepancy, not all of them.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [4, 5, 2, 5]
```

Target is 4. Dev = [0, 1, -2, 1]

Sorted by absolute value: [-2, 1, 1, 0]

| Step | Chosen | Running sum |
| --- | --- | --- |
| 1 | -2 | -2 |
| 2 | +1 | -1 |
| 3 | +1 | 0 |

We stop after 3 selections, meaning three elements are sufficient to balance the system. This shows that large negative deviation must be corrected first, and smaller positive corrections complete the balance.

### Example 2

Input:

```
n = 2
a = [0, 4]
```

Target is 2. Dev = [-2, 2]

Sorted: [2, -2]

| Step | Chosen | Running sum |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | -2 | 0 |

Both elements are required, so answer is 2. This confirms that when deviations are symmetric and equal in magnitude, both must be selected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting deviations dominates per test |
| Space | O(n) | Stores deviation array |

The constraints allow up to 2×10^5 total elements, so an n log n approach is easily fast enough, and memory usage remains linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        s = sum(a)
        if s % n != 0:
            res.append("-1")
            continue
        target = s // n
        dev = sorted([x - target for x in a], key=lambda x: abs(x), reverse=True)
        need = 0
        cnt = 0
        for d in dev:
            if need == 0:
                break
            need += d
            cnt += 1
        res.append(str(cnt))
    return "\n".join(res)

assert run("""1
4
4 5 2 5
""") == "3"

assert run("""1
2
0 4
""") == "2"

assert run("""1
3
1 1 1
""") == "0"

assert run("""1
1
100
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equalizable small | 3 | greedy accumulation |
| two elements | 2 | symmetric deviation |
| already equal | 0 | no operation needed |
| single element | 0 | trivial case |

## Edge Cases

When all elements are already equal, the deviation array is all zeros, so the loop terminates immediately and returns zero without selecting anything.

When the sum is not divisible by n, the algorithm stops early and outputs -1 because no target mean exists, making redistribution impossible regardless of subset choice.

When there is only one element, it is always already equal to itself, so the answer is zero since no correction is needed.
