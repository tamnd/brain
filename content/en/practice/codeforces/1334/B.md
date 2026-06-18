---
problem: 1334B
contest_id: 1334
problem_index: B
name: "Middle Class"
contest_name: "Educational Codeforces Round 85 (Rated for Div. 2)"
rating: 1100
tags: ["greedy", "sortings"]
answer: passed_samples
verified: true
solve_time_s: 150
date: 2026-06-14
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e0b1f-105c-83ec-b139-a797acfe317f
---

# CF 1334B - Middle Class

**Rating:** 1100  
**Tags:** greedy, sortings  
**Model:** gpt-5-5  
**Solve time:** 2m 30s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e0b1f-105c-83ec-b139-a797acfe317f  

---

## Solution

## Problem Understanding

We are given a group of people, each with some amount of money. A “wealthy” person is defined as someone whose final amount of money is at least a threshold value $x$.

We are allowed to perform an operation any number of times. Each operation picks any subset of people, takes all money from that subset, and then redistributes it equally among the same chosen people. After redistribution, the total sum inside the subset stays the same, but all selected people end up with an identical value.

The task is to determine the maximum number of people who can end up with at least $x$ after performing any sequence of such operations.

The constraints imply up to $10^5$ people across all test cases, so we need an $O(n \log n)$ or $O(n)$ solution per test case. Any approach that simulates operations or considers subsets directly is infeasible because the number of subsets is exponential.

A key subtlety is that money is perfectly transferable inside chosen groups, including fractional values. This means we are effectively allowed to redistribute total wealth arbitrarily across chosen groups, but only via equalization operations.

A naive intuition might suggest repeatedly grouping rich and poor people to balance things out, but that approach easily breaks because it ignores the global conservation of total sum and the constraint that all selected members become equal.

A few edge cases highlight the difficulty:

If all values are below $x$, but their total average is still below $x$, then no operation can create a wealthy person. For example:

Input:

```
3 10
3 3 3
```

Even grouping everyone gives average 3, so answer is 0.

If one very large value exists, it may be optimal to spread it over many people, not concentrate it.

These examples suggest that the key difficulty is choosing a subset whose average can be pushed above $x$ for as many people as possible.

## Approaches

The brute-force idea would be to try every possible subset of people and simulate the operation dynamics. For each subset, we could imagine redistributing money and checking how many people can reach at least $x$. However, this is exponential in the number of subsets, and each simulation is linear, leading to an impossible $O(2^n \cdot n)$ complexity.

The critical observation is that operations always replace a chosen subset by its average value. So the only values that matter are averages of selected groups, and the final configuration is equivalent to partitioning people into groups whose values are equal to group averages.

Now consider what we want: maximize the number of people whose final value is at least $x$. If a group ends up with value at least $x$, then its total sum must be at least group size times $x$. This suggests that high-value people can be formed by pooling excess from others.

A standard way to think about this is to sort the array in descending order. Suppose we decide that the top $k$ people will be made wealthy. To support this, we try to “fund” them using the largest values available. The best strategy is greedy: take largest values first and check if their cumulative sum is enough to sustain at least $k \cdot x$.

This transforms the problem into checking, for each prefix of sorted values, whether it is possible to make that prefix all at least $x$. Since higher values help satisfy the requirement, sorting ensures we always consider the most beneficial candidates first.

We compute prefix sums from largest to smallest and find the largest $k$ such that the sum of the largest $k$ elements is at least $k \cdot x$. That $k$ is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Sort the array in descending order so that we prioritize people with the highest savings. This ensures we always test the most promising candidates first.
2. Compute a running prefix sum over the sorted array. At step $k$, this sum represents the total wealth available among the top $k$ richest people.
3. For each $k$ from 1 to $n$, check whether the condition

$$\text{prefixSum}(k) \ge k \cdot x$$

holds. This checks whether we can redistribute enough total wealth to bring all $k$ selected people up to at least $x$.
4. Track the largest $k$ that satisfies the condition. This value is the maximum number of wealthy people achievable.

### Why it works

The key invariant is that any final configuration that makes $k$ people wealthy must have total wealth in those $k$ positions of at least $k \cdot x$. Since operations preserve total sum, no transformation can increase available wealth inside any chosen group.

Sorting ensures we always pick the strongest candidates for forming such a group. If even the top $k$ richest people cannot satisfy the condition, then no other subset of size $k$ can, because replacing any selected element with a smaller one only reduces the total sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort(reverse=True)
        
        total = 0
        ans = 0
        
        for i in range(n):
            total += a[i]
            k = i + 1
            if total >= k * x:
                ans = k
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first sorts the array in descending order so that we evaluate the strongest candidates first. The prefix sum `total` tracks the accumulated wealth of the current top segment. At each step, we compare it against the required threshold $k \cdot x$. The variable `ans` keeps the best valid prefix length found.

A subtle point is that we never need to explicitly simulate redistributions. The operations only matter insofar as they preserve total sum and allow arbitrary redistribution inside a chosen group, which is fully captured by the prefix sum condition.

## Worked Examples

### Example 1

Input:

```
4 3
5 1 2 1
```

Sorted:

```
[5, 2, 1, 1]
```

| k | Chosen prefix | Sum | k·x | Valid |
| --- | --- | --- | --- | --- |
| 1 | [5] | 5 | 3 | yes |
| 2 | [5,2] | 7 | 6 | yes |
| 3 | [5,2,1] | 8 | 9 | no |
| 4 | [5,2,1,1] | 9 | 12 | no |

Answer is 2.

This shows that only the strongest prefix can sustain enough average wealth per person.

### Example 2

Input:

```
4 10
11 9 11 9
```

Sorted:

```
[11, 11, 9, 9]
```

| k | Sum | k·x | Valid |
| --- | --- | --- | --- |
| 1 | 11 | 10 | yes |
| 2 | 22 | 20 | yes |
| 3 | 31 | 30 | yes |
| 4 | 40 | 40 | yes |

Answer is 4.

This demonstrates a case where redistribution allows full balancing at the threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates per test case |
| Space | $O(1)$ extra | in-place sort and prefix accumulation |

The total $n$ across test cases is at most $10^5$, so sorting all arrays remains efficient within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n, x = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))
        a.sort(reverse=True)

        total = 0
        ans = 0
        for i, v in enumerate(a):
            total += v
            if total >= (i + 1) * x:
                ans = i + 1
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("4\n4 3\n5 1 2 1\n4 10\n11 9 11 9\n2 5\n4 3\n3 7\n9 4 9\n") == "2\n4\n0\n3"

# custom cases
assert run("1\n1 5\n5\n") == "1", "single element already wealthy"
assert run("1\n3 10\n3 3 3\n") == "0", "cannot reach threshold"
assert run("1\n5 5\n10 1 1 1 1\n") == "2", "one rich supports limited others"
assert run("1\n4 4\n4 4 4 4\n") == "4", "all exactly at threshold"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal case |
| all small | 0 | impossible threshold |
| one large | 2 | redistribution limitation |
| uniform values | 4 | equality boundary |

## Edge Cases

For a single person with $a_1 \ge x$, the algorithm immediately counts it as valid because the prefix sum equals the requirement.

For an input where all values are below $x$, the prefix condition fails for every $k$, since total sum cannot reach $k \cdot x$. Sorting does not change this outcome.

For highly skewed inputs like one large value and many tiny ones, the prefix test correctly limits how many people can be supported, because each additional person increases the required threshold linearly while contributing only small marginal sum.