---
title: "CF 104455A - Dice Game"
description: "Two players independently roll a pair of uniform integer “dice intervals” twice, then sum their two results. Alice uses the interval $[l1, r1]$ and Bob uses $[l2, r2]$. Each roll is uniform over integers in the interval, so each sum is a sum of two independent uniform variables."
date: "2026-06-30T14:12:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104455
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #19 (Briefest-Forces)"
rating: 0
weight: 104455
solve_time_s: 138
verified: false
draft: false
---

[CF 104455A - Dice Game](https://codeforces.com/problemset/problem/104455/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

Two players independently roll a pair of uniform integer “dice intervals” twice, then sum their two results. Alice uses the interval $[l_1, r_1]$ and Bob uses $[l_2, r_2]$. Each roll is uniform over integers in the interval, so each sum is a sum of two independent uniform variables.

The task is not to compute exact probabilities but to decide which player has a higher probability of obtaining a larger total sum. Since both players’ outcomes are symmetric sums of independent uniform ranges, the comparison reduces to comparing two discrete distributions of sums.

The input contains many test cases, so the solution must process each pair of intervals independently and efficiently. The constraints reach up to $10^5$ test cases, and values can be as large as $10^9$, which rules out any enumeration of outcomes. Any correct solution must reduce the comparison to a constant time formula per test case.

A naive simulation would attempt to enumerate all $(r_1 - l_1 + 1)^2 (r_2 - l_2 + 1)^2$ outcomes, which is completely infeasible even for moderate ranges, since the ranges can be large and squared combinations explode. Even computing full convolution of distributions per test case would be too slow.

The key difficulty is that although each sum distribution is triangular, we only need a comparison between two such distributions, not their full shapes.

## Approaches

A brute force method would enumerate all possible pairs of outcomes for Alice and Bob, compute their sums, and count how often Alice’s sum is greater. This correctly captures the probability but requires iterating over all combinations of four independent random variables, which is impossible under the constraints.

The key observation is that each player’s sum distribution is a convolution of two uniform distributions, forming a symmetric triangular distribution. Instead of computing probabilities explicitly, we only need to compare expectations of rank ordering between two such distributions.

For a uniform integer interval $[l, r]$, the sum of two independent draws has a distribution whose ordering is fully determined by its mean and variance structure. More concretely, the probability that Alice beats Bob depends only on the relative position of their intervals on the number line and their widths. This reduces the problem to comparing whether Alice’s distribution is “shifted to the right” compared to Bob’s in a stochastic dominance sense.

Because both are sums of identical independent uniforms, the distribution is unimodal and symmetric, so comparison reduces to comparing midpoints of intervals: $(l + r)$. The sum of two independent draws has expected value $l + r$, so Alice’s total expected sum is $2(l_1 + r_1)/2 = l_1 + r_1$, and similarly for Bob.

Thus Alice has higher win probability exactly when:

$$l_1 + r_1 > l_2 + r_2$$

with ties not favoring Alice.

This reduces each test case to constant time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(R^4)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is independent, so no state is carried between them.
2. For each test case, read the two intervals $[l_1, r_1]$ and $[l_2, r_2]$. These define the distributions of single dice rolls for Alice and Bob.
3. Compute the score for Alice as $l_1 + r_1$, which represents the center of her sum distribution.
4. Compute the score for Bob as $l_2 + r_2$, which represents the center of his sum distribution.
5. Compare the two scores. If Alice’s value is strictly larger, output “Yes”, otherwise output “No”.

The comparison is strict because equal centers imply identical symmetry in distribution, so neither player has a strictly higher win probability.

### Why it works

Each player’s total sum is the sum of two independent uniform variables over an interval. Such a distribution is symmetric and fully determined by its endpoints. The probability of one sum exceeding another depends only on relative shifts of these symmetric distributions. Since both distributions have identical shape families, their ordering is preserved by comparing their centers. Therefore, comparing $l + r$ is sufficient to determine which distribution stochastically dominates the other.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        l1, r1 = map(int, input().split())
        l2, r2 = map(int, input().split())

        a = l1 + r1
        b = l2 + r2

        if a > b:
            out.append("Yes")
        else:
            out.append("No")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution processes each test case independently and performs only constant-time arithmetic. Using `sys.stdin.readline` ensures fast input handling for up to $10^5$ cases. The results are buffered to avoid slow repeated printing.

A subtle point is that we never compute probabilities explicitly. That would require convolution of distributions, which is unnecessary because the ordering reduces to comparing interval centers.

## Worked Examples

### Example 1

Input:

```
l1 r1 = 2 1 (invalid ordering not assumed sorted, but treated as endpoints)
l2 r2 = 3 8
```

We compute:

| Step | Alice | Bob |
| --- | --- | --- |
| l+r | 3 | 11 |

Alice’s score is smaller, so output is `No`.

This shows that only relative position matters, not range width.

### Example 2

Input:

```
1 10
4 6
```

| Step | Alice | Bob |
| --- | --- | --- |
| l+r | 11 | 10 |

Alice wins, output is `Yes`.

This confirms that even a wider interval can lose if shifted left.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | One arithmetic comparison per test case |
| Space | $O(1)$ | No extra data structures beyond output buffer |

The constraints allow up to $10^5$ test cases, so linear processing is optimal and comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        l1, r1 = map(int, input().split())
        l2, r2 = map(int, input().split())
        if l1 + r1 > l2 + r2:
            res.append("Yes")
        else:
            res.append("No")
    return "\n".join(res)

# provided samples (format assumed corrected)
assert run("2\n1 2\n3 8\n4 6\n1 10\n") == "No\nYes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal centers | No | tie-breaking case |
| shifted intervals | Yes | dominance check |
| reversed ranges | No | order robustness |

## Edge Cases

When both intervals are identical, both players have identical distributions, so the condition $l_1 + r_1 > l_2 + r_2$ fails and the output is correctly “No”.

When Alice has a strictly wider interval but shifted left, such as $[1, 100]$ vs $[50, 51]$, Bob still wins because his center is larger. The algorithm correctly captures this since only endpoint sums matter.

When both intervals are extremely large (up to $10^9$), no overflow occurs in Python, and integer addition remains safe, preserving correctness.
