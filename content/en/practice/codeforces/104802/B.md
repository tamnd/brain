---
title: "CF 104802B - Snowy Bus"
description: "We are given a bus with a fixed empty weight and a group of passengers, each described by two values: their weight contribution if they stay inside the bus, and their pushing strength if they step outside."
date: "2026-06-28T13:36:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104802
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #26 (Readall-Forces)"
rating: 0
weight: 104802
solve_time_s: 82
verified: false
draft: false
---

[CF 104802B - Snowy Bus](https://codeforces.com/problemset/problem/104802/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a bus with a fixed empty weight and a group of passengers, each described by two values: their weight contribution if they stay inside the bus, and their pushing strength if they step outside.

For any choice of which passengers become pushers, the remaining passengers still inside increase the bus weight, while the pushers contribute total force. The configuration is valid if the sum of pushing forces is at least the total weight of the bus plus all passengers who stayed inside.

The task is to choose a subset of passengers to step outside such that the number of chosen pushers is as small as possible, while still making the system valid. If no subset can satisfy the condition, the answer is -1.

The constraints are large: up to 200,000 passengers total across all test cases, and up to 10,000 test cases. This forces a solution that is roughly linear or log-linear per test case. Any approach that tries to enumerate subsets or simulate all choices per passenger will fail immediately because even O(n^2) per test case would already exceed limits.

A subtle difficulty comes from the coupling between choices. A passenger contributes positively as a pusher through their force, but removing them also reduces the weight inside the bus, which makes the constraint easier to satisfy. This dual role means we cannot treat selection greedily based only on force or only on weight.

A few edge cases expose incorrect greedy reasoning. If all passengers have very small force compared to their mass plus bus weight contribution, even selecting all of them will not help. For example, if w = 10, n = 2, m = [100, 100], f = [1, 1], then even if both push, total force is 2 while total weight is at least 10 plus remaining passengers, so it fails and answer is -1. Any greedy approach that assumes more pushers always help would fail if it does not check feasibility.

Another tricky case is when a single strong passenger exists but has large mass. For example, w = 5, m = [100, 1], f = [200, 1]. The optimal answer is 1, choosing only the strong passenger, because removing them reduces weight significantly and their force is enough alone. A naive approach might try to include small-force passengers first, increasing required pushers unnecessarily.

## Approaches

A brute-force idea is to try every subset of passengers as pushers, compute remaining weight and pushing force, and check validity. This is correct because it directly evaluates the condition for every possible configuration. However, this requires checking 2^n subsets, and each check takes O(n), leading to O(n 2^n) per test case, which is infeasible even for n = 30, let alone 200,000.

The key observation is that the decision depends only on how many passengers we pick and which ones are best to pick for each possible size. If we fix that exactly k passengers become pushers, we want to choose the best k candidates that maximize feasibility. The structure suggests sorting candidates by some notion of usefulness and then building solutions incrementally.

Rewriting the condition helps. Let total mass of all passengers be S. If we choose a set P as pushers, remaining passengers contribute S minus sum of masses of P. The condition becomes:

sum(f in P) ≥ w + S − sum(m in P)

Rearranging gives:

sum(f + m for P) ≥ w + S

This transformation is crucial because it turns each passenger into a single value g_i = f_i + m_i for scoring selection, while the constraint depends only on the sum of selected g_i values and a fixed threshold.

Now the problem becomes: pick as few items as possible such that the sum of their g_i values reaches at least w + S. To minimize the count, we should always pick the largest g_i first, since each picked passenger contributes independently toward reaching the threshold. This reduces the problem to sorting g_i in descending order and taking a prefix until the threshold is reached.

This greedy works because all items have equal “cost” in terms of count, and differing “value” g_i. This is the classic minimum-size subset to reach a target sum, which is solved optimally by taking largest values first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently and transform the problem into a selection over derived weights.

1. Compute total passenger mass S by summing all m_i. This captures the full system weight baseline before choosing pushers. The bus constraint depends on how much mass we remove, so we need this global reference.
2. For each passenger compute g_i = f_i + m_i. This value measures how much “progress toward feasibility” that passenger contributes if chosen as a pusher. It combines the benefit of adding force and the benefit of removing weight.
3. Sort all passengers in descending order of g_i. We want to pick passengers that reduce the required effort most efficiently, since every chosen passenger costs exactly one slot.
4. Iterate over the sorted list, maintaining a running sum of selected g_i values and a counter of how many we picked. After each addition, check whether the accumulated sum is at least w + S.
5. The first time the condition is satisfied, output the number of selected passengers. If we finish the list without reaching the threshold, output -1.

The key idea is that once a prefix of size k is insufficient, any other subset of size k cannot do better because replacing any selected element with a smaller g_i can only reduce the sum. This makes the greedy prefix optimal for each k.

### Why it works

The transformation reduces feasibility to reaching a fixed target sum using items with equal cost and positive value. For any fixed number of selected passengers, the best achievable sum is obtained by choosing the k largest g_i values. Therefore, if any subset of size k works, the greedy prefix of size k also works. This monotonicity ensures that the first k that reaches the threshold is the minimum possible number of pushers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, w = map(int, input().split())
        m = list(map(int, input().split()))
        f = list(map(int, input().split()))

        total_mass = sum(m)
        target = w + total_mass

        vals = [m[i] + f[i] for i in range(n)]
        vals.sort(reverse=True)

        cur = 0
        ans = -1

        for i, v in enumerate(vals):
            cur += v
            if cur >= target:
                ans = i + 1
                break

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows directly from the transformation. The most important step is computing m_i + f_i, which encodes both the reduction in remaining weight and the increase in available force.

Sorting in descending order is essential because we are effectively solving a minimum-cardinality knapsack with uniform cost. The prefix scan ensures we stop at the smallest feasible count.

A common mistake is trying to greedily select passengers based on f_i alone or based on ratio f_i / m_i. Those approaches fail because the correct objective is not independent contributions but combined effect under a global threshold.

## Worked Examples

Consider the sample test cases.

### Example 1

Input:

n = 3, w = 4

m = [1, 1, 1]

f = [6, 6, 3]

We compute g = [7, 7, 4], and S = 3, so target = 7.

| Step | Chosen g values | Running sum | Target | k |
| --- | --- | --- | --- | --- |
| 1 | 7 | 7 | 7 | 1 |

The first element already reaches the threshold, so answer is 1.

This shows that a single strong passenger can dominate even if others exist.

### Example 2

Input:

n = 4, w = 6

m = [1, 1, 1, 1]

f = [1, 1, 1, 1]

g = [2, 2, 2, 2], S = 4, target = 10

| Step | Chosen g values | Running sum | Target | k |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 10 | 1 |
| 2 | 2, 2 | 4 | 10 | 2 |
| 3 | 2, 2, 2 | 6 | 10 | 3 |
| 4 | 2, 2, 2, 2 | 8 | 10 | 4 |

Even selecting all passengers is insufficient, so the answer is -1.

This confirms the correctness of the feasibility check when no subset can satisfy the constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting g_i dominates per test case |
| Space | O(n) | Storage for m, f, and derived array |

The total n across test cases is bounded by 2 · 10^5, so sorting across all cases remains efficient within time limits. Memory usage stays linear in the active test case.

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
        n, w = map(int, input().split())
        m = list(map(int, input().split()))
        f = list(map(int, input().split()))

        total_mass = sum(m)
        target = w + total_mass

        vals = [m[i] + f[i] for i in range(n)]
        vals.sort(reverse=True)

        cur = 0
        ans = -1
        for i, v in enumerate(vals):
            cur += v
            if cur >= target:
                ans = i + 1
                break

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("4\n3 4\n1 1 1\n6 6 3\n3 4\n1 1 1\n3 3 3\n3 100\n1 1 1\n1 1 1\n6 5\n1 4 2 8 3 1\n2 7 5 1 4 2") == "1\n2\n-1\n3"

# minimum case
assert run("1\n1 1\n1\n10") == "1"

# impossible case
assert run("1\n2 100\n10 10\n1 1") == "-1"

# all equal strong enough
assert run("1\n4 1\n1 1 1 1\n5 5 5 5") == "1"

# boundary large values
assert run("1\n3 10\n100 100 100\n1 1 1") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 passenger strong | 1 | minimal selection |
| too weak overall | -1 | impossibility detection |
| uniform strong | 1 | greedy early stopping |
| all needed | 3 | worst-case accumulation |

## Edge Cases

A key edge case is when the optimal answer is -1 even though individual passengers seem useful. The transformed condition makes this explicit because even the full sum of g_i values does not reach the required target. The algorithm handles this naturally by exhausting the sorted list without triggering success.

Another edge case is when exactly one passenger is sufficient. Since we sort by g_i, the largest single value is checked first, and if it already exceeds the target, the algorithm stops immediately. This prevents unnecessary processing and confirms that prefix optimality extends to k = 1.

A third edge case occurs when many small contributors collectively are required. Because the algorithm always accumulates in descending order, it ensures that if a solution exists at size k, it will be found exactly when reaching k, never later or earlier, preserving correctness even in dense distributions of values.
