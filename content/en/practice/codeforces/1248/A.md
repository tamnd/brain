---
title: "CF 1248A - Integer Points"
description: "We are given two families of straight lines on the plane. The first family consists of lines of the form $y = x + pi$, and the second family consists of lines of the form $y = -x + qj$. Every $pi$ is distinct within its own group, and every $qj$ is distinct within its own group."
date: "2026-06-13T20:48:09+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1248
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 594 (Div. 2)"
rating: 1000
weight: 1248
solve_time_s: 217
verified: true
draft: false
---

[CF 1248A - Integer Points](https://codeforces.com/problemset/problem/1248/A)

**Rating:** 1000  
**Tags:** geometry, math  
**Solve time:** 3m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two families of straight lines on the plane. The first family consists of lines of the form $y = x + p_i$, and the second family consists of lines of the form $y = -x + q_j$. Every $p_i$ is distinct within its own group, and every $q_j$ is distinct within its own group.

Each line from the first family intersects every line from the second family at exactly one point. The task is to count how many of these intersection points have both coordinates as integers.

A key observation is that we are not being asked to compute coordinates or check intersections geometrically in a general sense. We only need to decide, for each pair $(p_i, q_j)$, whether their intersection point lies on integer coordinates, and count how many such pairs satisfy this condition.

The constraints make it clear that brute force over all pairs is not feasible. With $n, m$ up to $10^5$ per test case and total sums up to $10^5$, an $O(nm)$ approach would require up to $10^{10}$ operations in the worst case, which is far beyond a 2 second limit. This immediately forces us toward an $O(n + m)$ or $O(n \log n)$ style solution per test.

A subtle point that often causes mistakes is misunderstanding what “integer intersection point” means in this setup. The intersection always exists and is unique, but it is not always integral even though all coefficients are integers. Another issue is double counting or trying to compute coordinates explicitly for all pairs, which is unnecessary.

A naive pitfall example is:

Input:

```
n = 2, p = [0, 1]
m = 2, q = [0, 2]
```

The intersection of $y = x + p$ and $y = -x + q$ happens at:

$$x = \frac{q - p}{2}, \quad y = \frac{p + q}{2}$$

Even though all inputs are integers, the result is only integral when both $q - p$ and $p + q$ are even. Many naive solutions incorrectly assume all intersections are integers or forget the parity condition.

## Approaches

A direct approach is to iterate over every pair $(p_i, q_j)$, compute the intersection point, and check whether both coordinates are integers. This is straightforward: solve the equations, compute $x = (q_j - p_i)/2$, $y = (q_j + p_i)/2$, and verify divisibility by 2. While correct, this requires $O(nm)$ time per test case, which becomes infeasible even for moderate input sizes.

The structure of the formula reveals a much simpler condition. The intersection point is integral if and only if both $q_j - p_i$ and $q_j + p_i$ are even. These two conditions are equivalent to requiring that $p_i$ and $q_j$ have the same parity. If $p_i$ is even and $q_j$ is odd, then $p_i + q_j$ is odd and cannot produce an integer $y$-coordinate. The same issue occurs if the parity is reversed.

So the entire problem reduces to counting how many pairs have matching parity. We simply split both arrays into even and odd counts and multiply corresponding groups.

Let $E_p, O_p$ be the counts of even and odd $p_i$, and similarly $E_q, O_q$ for $q_j$. Then the answer is:

$$E_p \cdot E_q + O_p \cdot O_q$$

The brute-force works because it explicitly checks every geometric intersection, but it fails because it recomputes the same parity condition repeatedly. The observation that integrality depends only on parity reduces the geometric problem into a counting problem on two buckets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| Optimal | $O(n + m)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the array $p$ and count how many values are even and how many are odd. This separates all lines of the form $y = x + p_i$ into two classes based on parity, which fully determines how they interact with the second family.
2. Read the array $q$ and similarly count even and odd values. This mirrors the same classification for lines $y = -x + q_j$.
3. Compute the number of valid pairs where both values are even, which contributes $E_p \cdot E_q$ intersections with integer coordinates.
4. Compute the number of valid pairs where both values are odd, which contributes $O_p \cdot O_q$ valid intersections.
5. Sum these two contributions and output the result.

### Why it works

The intersection of $y = x + p$ and $y = -x + q$ is:

$$x = \frac{q - p}{2}, \quad y = \frac{p + q}{2}$$

Both coordinates are integers exactly when $p + q$ is even, which happens if and only if $p$ and $q$ share the same parity. Since every pair behaves independently and depends only on parity, grouping values by parity preserves all necessary information and guarantees correctness.

## Python Solution

```
PythonRun
```

The solution processes each test case independently. The key implementation detail is separating parity counts in a single pass over each array, avoiding any nested iteration. The final multiplication step directly encodes the combinatorial pairing of matching parity classes.

A common mistake is recomputing intersection conditions explicitly or forgetting that both coordinates must be integers simultaneously. Another is mixing up the condition and counting mismatched parity pairs instead of matched ones.

## Worked Examples

### Example 1

Input:

```

```

| Step | Ep | Op | Eq | Oq | Contribution | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 0 | 0 | 0 | 0 | 0 | 0 |
| After p | 1 | 2 | 0 | 0 | 0 | 0 |
| After q | 1 | 2 | 1 | 1 | 1_1 + 2_1 | 3 |

The table shows how parity grouping reduces the problem to simple counting. The final answer matches the number of valid parity-aligned pairs.

### Example 2

Input:

```

```

| Step | Ep | Op | Eq | Oq | Contribution | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 0 | 0 | 0 | 0 | 0 | 0 |
| After p | 1 | 0 | 0 | 0 | 0 | 0 |
| After q | 1 | 0 | 0 | 1 | 1_0 + 0_1 | 0 |

This demonstrates the case where all intersections fail due to parity mismatch.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each array is scanned once per test case |
| Space | $O(1)$ | Only four counters are used regardless of input size |

The total input size across test cases is $10^5$, so a linear scan per test case remains easily within time limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all-even | 6 | full pairing among evens |
| all-odd | 4 | symmetry for odd-only sets |
| mixed parity | 2 | correct separation of parity groups |

## Edge Cases

One edge case is when all values in both arrays share the same parity. For example, if all $p_i$ and all $q_j$ are even, every pair contributes a valid integer intersection. The algorithm counts $n \cdot m$ because both odd counts are zero and even counts dominate, matching the full Cartesian product.

Another case is complete parity mismatch, such as all $p_i$ being even and all $q_j$ being odd. The intersection formula forces $p + q$ to always be odd, so no pair contributes. The algorithm correctly computes $E_p \cdot E_q = 0$ and $O_p \cdot O_q = 0$, yielding zero.

A final subtle case is minimal input sizes where $n = m = 1$. If $p_1 = q_1$, the answer depends solely on parity equality. The algorithm reduces correctly to a single comparison of parity, avoiding any special casing or off-by-one issues.
