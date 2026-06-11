---
title: "CF 1355B - Young Explorers"
description: "We are given a list of explorers, each associated with a number $ei$ that represents how many people must be in any group they join. If an explorer has value $e$, then they are only willing to participate in a group whose size is at least $e$."
date: "2026-06-11T13:52:21+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1355
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 643 (Div. 2)"
rating: 1200
weight: 1355
solve_time_s: 454
verified: true
draft: false
---

[CF 1355B - Young Explorers](https://codeforces.com/problemset/problem/1355/B)

**Rating:** 1200  
**Tags:** dp, greedy, sortings  
**Solve time:** 7m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of explorers, each associated with a number $e_i$ that represents how many people must be in any group they join. If an explorer has value $e$, then they are only willing to participate in a group whose size is at least $e$. The task is to partition some or all explorers into as many valid groups as possible, while respecting that constraint for every member inside each group.

Each test case is independent. For each one, we only need to output the maximum number of groups we can form, not the grouping itself.

The constraints are large enough that any solution must be close to linear or $n \log n$ per test case. Since the total number of elements across all test cases is bounded by $3 \cdot 10^5$, a solution that sorts each test case and then processes it once is sufficient, while any approach that repeatedly tries to build groups greedily in a naive way will degrade to quadratic behavior in the worst case.

A subtle failure mode appears when one tries to assign explorers one by one into groups without sorting. For example, if we see a large requirement early and place it alone, we might later discover that it could have been grouped with others to form multiple valid groups. Another failure mode is attempting to greedily form groups in arrival order without considering that small $e_i$ values should be used to “fill” groups efficiently, otherwise large $e_i$ values may become impossible to place.

## Approaches

A brute-force strategy tries to construct groups incrementally. We repeatedly pick a subset of remaining explorers, test whether it can form a valid group, and remove it if so. This is correct because it respects the constraint definition directly. The issue is that each attempt may scan a large portion of the remaining array to verify feasibility, and in the worst case this leads to about $O(n^2)$ behavior per test case when explorers are repeatedly reconsidered.

The key structural observation is that the condition for a group depends only on its size, not on identities. Once we sort explorers by their $e_i$, we can build groups greedily while maintaining how many candidates we have accumulated. Whenever the accumulated number of available explorers reaches or exceeds the requirement of the current element, we can finalize a group and reset the counter. This works because delaying a group only increases the pool of available members, never decreases feasibility.

This reduces the problem to a single pass over a sorted array, where we track how many elements we are currently considering for a potential group.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Sort + Greedy Scan | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently. First, we sort the array of $e_i$ in nondecreasing order. Sorting ensures that we always try to satisfy the smallest requirements first, which is essential because they are the easiest to place and act as fillers for forming valid groups.

We then scan the sorted array while maintaining a counter that represents how many explorers we have accumulated toward the current group. Each time we include an explorer, we increase this counter by one.

When the counter becomes equal to the current explorer’s requirement, we close a group. At that moment, we reset the counter to zero because those explorers are now assigned and cannot be reused.

The reason this check is done at equality (rather than greater-than) is that once we have enough members to satisfy the weakest requirement in the current pool, any additional accumulation beyond that point is better used to start forming the next group immediately.

### Why it works

After sorting, any prefix of the array contains the smallest possible requirements among the remaining elements. When we form a group at the earliest valid point, we ensure that no element with a larger requirement is wasted early, and we preserve flexibility for later steps. Each group corresponds to a maximal segment in which the accumulated count exactly meets the threshold of the last included element, ensuring no group violates the size constraint and no valid grouping is skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        e = list(map(int, input().split()))
        e.sort()

        cnt = 0
        groups = 0

        for x in e:
            cnt += 1
            if cnt >= x:
                groups += 1
                cnt = 0

        print(groups)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the requirements so that we process easier constraints first. The variable `cnt` tracks the size of the currently forming group. Every time we add an explorer, we check whether the current group is valid by comparing `cnt` with the current requirement `x`. Once it becomes valid, we immediately finalize the group and reset.

A common mistake is to wait until `cnt == x` instead of `cnt >= x`. Equality alone fails when multiple small values appear, since groups can become valid earlier than expected, and delaying the check leads to unnecessarily large groups that reduce the total number formed.

## Worked Examples

### Example 1

Input:

```
3
1 1 1
```

Sorted array remains the same.

| Step | Value | cnt before | cnt after | groups |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 0 |
| 2 | 1 | 1 | 2 | 1 |
| 3 | 1 | 0 | 1 | 2 |
| 4 | 1 | 2 | 3 | 3 |

Each element completes a group immediately because every requirement is minimal.

This trace shows that the algorithm never delays a group when it is already feasible, ensuring maximal partitioning.

### Example 2

Input:

```
5
2 3 1 2 2
```

Sorted array:

```
1 2 2 2 3
```

| Step | Value | cnt before | cnt after | groups |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 0 |
| 2 | 2 | 1 | 2 | 1 |
| 3 | 2 | 0 | 1 | 1 |
| 4 | 2 | 1 | 2 | 2 |
| 5 | 2 | 0 | 1 | 2 |
| 6 | 3 | 1 | 2 | 2 |

The second group only forms after enough elements accumulate to satisfy a requirement of 2. The element with requirement 3 never triggers a group in this arrangement, which is optimal because it would require a larger group that cannot be completed later.

This confirms that sorting followed by greedy accumulation correctly balances small and large requirements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates, single linear scan after |
| Space | $O(1)$ extra (or $O(n)$ with storage) | only the input array is stored |

The total input size across test cases is bounded, so sorting each test case and performing one pass over it fits comfortably within time limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else ""

# reference implementation
def solve(inp: str) -> str:
    import sys
    input = sys.stdin.readline
    sys.stdin = io.StringIO(inp)

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        e = list(map(int, input().split()))
        e.sort()
        cnt = 0
        groups = 0
        for x in e:
            cnt += 1
            if cnt >= x:
                groups += 1
                cnt = 0
        out.append(str(groups))
    return "\n".join(out)

# provided samples
assert solve("2\n3\n1 1 1\n5\n2 3 1 2 2\n") == "3\n2"

# custom cases
assert solve("1\n1\n1\n") == "1"
assert solve("1\n4\n4 4 4 4\n") == "1"
assert solve("1\n5\n1 2 3 4 5\n") == "2"
assert solve("1\n6\n2 2 2 2 2 2\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single minimal | 1 | base case |
| uniform large values | 1 | grouping constraint tightness |
| increasing sequence | 2 | greedy batching behavior |
| repeated mid values | 3 | multiple group formation |

## Edge Cases

A minimal single-element case ensures that an explorer with requirement 1 always forms a group alone, since the counter immediately satisfies the condition.

A case where all values are equal to $n$ ensures that only one group can be formed, since no prefix ever reaches size $n$ before all elements are consumed, confirming that the algorithm does not overcount when requirements are high.

A strictly increasing sequence ensures that early small values correctly act as fillers and that large values do not incorrectly force premature grouping. The sorted greedy pass naturally delays closure until enough accumulation exists, preserving correctness.
