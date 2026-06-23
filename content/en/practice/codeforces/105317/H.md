---
title: "CF 105317H - Juan vs. Man"
description: "We are asked to construct an array of length $n$, where every element lies between $1$ and $m$, with a global restriction on its subarrays."
date: "2026-06-23T15:13:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105317
codeforces_index: "H"
codeforces_contest_name: "JPC 1.0"
rating: 0
weight: 105317
solve_time_s: 51
verified: true
draft: false
---

[CF 105317H - Juan vs. Man](https://codeforces.com/problemset/problem/105317/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct an array of length $n$, where every element lies between $1$ and $m$, with a global restriction on its subarrays. The restriction is not about ordering or distinctness, but about prefix sums: no contiguous segment of the array is allowed to have a sum that is divisible by $m$.

Equivalently, if we define prefix sums $s_i = a_1 + a_2 + \dots + a_i$, then for any two indices $i \le j$, we must avoid $s_j \equiv s_{i-1} \pmod m$. The condition “no subarray sum divisible by $m$” is exactly the same as saying that no two prefix sums have the same remainder modulo $m$, except that we implicitly include $s_0 = 0$. So the constraint becomes: all prefix sums modulo $m$ must be distinct.

The input gives multiple independent test cases, each specifying a pair $(n, m)$, and for each case we either construct a valid array or report that it is impossible.

The constraints allow up to $10^5$ test cases with total $n$ summing to $3 \cdot 10^5$. This forces any solution to run in essentially linear time over all test cases combined. Anything that tries to check subarrays explicitly is immediately infeasible since a single array of size $n$ has $O(n^2)$ subarrays.

A subtle failure mode comes from confusing the condition with something local. For example, one might try to ensure that no single element is divisible by $m$, or that no partial sum equals zero only at the end. Both are insufficient because the violation can occur between two internal positions.

For instance, if $m = 5$, the array $[2, 3, 5]$ looks harmless element-wise, but the subarray $[2, 3]$ sums to $5$, which is divisible by $m$. A naive greedy that ignores prefix interactions will fail on such cases.

Another common mistake is assuming that because values are bounded by $m$, we always have enough flexibility to avoid collisions. In reality, once prefix sums modulo $m$ repeat, the construction fails permanently, since the repetition is irreversible.

## Approaches

A brute-force approach would try to construct the array step by step and, at each position, test all candidate values from $1$ to $m$, checking whether adding it creates a forbidden subarray. To check validity, we would need to track all previous prefix sums modulo $m$ and ensure no repetition occurs. This can be done with a hash set of prefix remainders.

However, the key difficulty is that for each position we may try up to $m$ values, and for each attempt we update a prefix and check membership. Even with hashing, this becomes $O(nm)$ per test case in the worst case, which is far beyond the limits when $m$ can be up to $10^6$.

The structure of the problem becomes clearer when viewed through prefix sums modulo $m$. We are essentially trying to build a sequence of $n+1$ prefix residues $s_0, s_1, \dots, s_n$ such that all are distinct modulo $m$. But there are only $m$ possible residues in total. Since we already have $s_0 = 0$, the maximum number of additional distinct residues we can have is $m-1$. This immediately implies a necessary condition: $n \le m-1$.

Once we recognize this bound, the construction becomes natural. We just need to walk through distinct residues modulo $m$, never repeating one. The simplest way is to keep increasing prefix sums by a fixed step, typically $1$, and avoid wrapping modulo $m$ too early. However, using step size $1$ directly leads to full coverage of residues in order, which gives a clean deterministic construction.

We define $a_i = 1$ for all $i$, which yields prefix sums $1, 2, 3, \dots, n$. These are all distinct modulo $m$ as long as $n < m$. If $n \ge m$, then by pigeonhole principle, two prefix sums must be congruent modulo $m$, so a valid array cannot exist.

Thus the problem collapses into a simple feasibility check followed by a constant-time construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(m)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read $n$ and $m$. We first determine whether a valid construction is possible. Since prefix sums modulo $m$ must all be distinct and there are only $m$ residues, we require $n < m$. If this condition fails, no construction can satisfy the requirement.
2. If $n \ge m$, immediately output “NO”. This is a direct consequence of the pigeonhole principle applied to prefix sums modulo $m$. No arrangement of values in $[1, m]$ can avoid repeating a modulo state.
3. If $n < m$, construct the array by setting every element to $1$. This produces prefix sums $s_i = i$, which are strictly increasing as integers.
4. Since $s_i = i$, all prefix sums are distinct modulo $m$ as long as no two integers between $0$ and $n$ differ by a multiple of $m$. Because $n < m$, this is impossible.
5. Output “YES” followed by the constructed array.

### Why it works

The key invariant is that prefix sums are strictly increasing by exactly one at each step, so no two prefix sums can ever coincide as integers. Because modulo equality implies integer difference is a multiple of $m$, and all differences between prefix sums lie in $[1, n]$, no difference can reach $m$. This guarantees that no prefix sum repeats modulo $m$, which is equivalent to saying no subarray sum is divisible by $m$.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    n, m = map(int, input().split())
    
    if n >= m:
        out.append("NO")
        continue
    
    out.append("YES")
    out.append(" ".join(["1"] * n))

sys.stdout.write("\n".join(out))
```

The implementation follows exactly the structure of the algorithm. The feasibility check `n >= m` is the only decision point, derived directly from the pigeonhole argument on prefix residues. The construction uses a constant array of ones, which avoids any risk of modular repetition.

The output is buffered to avoid repeated I/O overhead across up to $10^5$ test cases.

## Worked Examples

Consider the input $(n, m) = (3, 5)$. Since $3 < 5$, we construct the array.

| i | a[i] | prefix sum | mod 5 |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 2 | 2 |
| 3 | 1 | 3 | 3 |

All prefix residues are distinct, so no subarray sum can be divisible by 5. This confirms correctness for a typical valid case.

Now consider $(n, m) = (5, 3)$. Since $5 \ge 3$, we immediately reject.

| Step | Action | Reason |
| --- | --- | --- |
| 1 | Detect $n \ge m$ | More prefix sums than residues |
| 2 | Output NO | Pigeonhole violation unavoidable |

This shows the impossibility case where any array must fail.

The first example demonstrates how the construction avoids modular repetition, while the second shows that the impossibility is structural and not dependent on choice of values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each test case constructs or rejects in constant or linear time over output |
| Space | $O(1)$ | Only stores current test case variables and output buffer |

The total work across all test cases is proportional to the total $n$, which is bounded by $3 \cdot 10^5$, comfortably within limits for a 1 second runtime in Python when using buffered output.

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
        n, m = map(int, input().split())
        if n >= m:
            out.append("NO")
        else:
            out.append("YES")
            out.append(" ".join(["1"] * n))

    return "\n".join(out)

# provided samples (as interpreted from statement formatting)
assert run("3\n3 5\n3 4\n3 6\n") == "YES\n1 1 1\nYES\n1 1 1\nYES\n1 1 1"

# minimum case
assert run("1\n1 2\n") == "YES\n1"

# impossible small
assert run("1\n2 2\n") == "NO"

# boundary just possible
assert run("1\n2 3\n") == "YES\n1 1"

# large m, small n
assert run("1\n5 1000000\n") == "YES\n1 1 1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n < m | YES + ones | constructive correctness |
| n = m | NO | tight boundary failure |
| n = 1 | YES | minimal valid structure |
| large m | YES | scalability and uniform construction |

## Edge Cases

When $n = 1$, the algorithm immediately passes the feasibility check if $m \ge 2$ and outputs a single element array `[1]`. The prefix sum is `1`, which is non-zero modulo $m$, so no subarray can violate the condition.

When $n = m$, the algorithm rejects. For example, with $n = 3, m = 3$, any array produces 4 prefix sums including 0, but only 3 residue classes exist. A manual trace confirms repetition is unavoidable regardless of values chosen.

When $m$ is extremely large relative to $n$, such as $(n, m) = (10^5, 10^6)$, the construction outputs a long sequence of ones. Prefix sums run from 1 to $10^5$, all distinct modulo $m$, so the condition holds trivially since wraparound never occurs within the range.
