---
title: "CF 103765F - \u6458\u6a58\u5b50"
description: "We are given several independent scenarios of an orange orchard. In each scenario, there are $n$ trees, and the $i$-th tree contains $ai$ oranges. From each tree, we are allowed to pick any integer number of oranges between $0$ and $ai$, independently of other trees."
date: "2026-07-02T08:55:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103765
codeforces_index: "F"
codeforces_contest_name: "2022 Collegiate Programming Contest of Xiangtan University"
rating: 0
weight: 103765
solve_time_s: 50
verified: true
draft: false
---

[CF 103765F - \u6458\u6a58\u5b50](https://codeforces.com/problemset/problem/103765/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios of an orange orchard. In each scenario, there are $n$ trees, and the $i$-th tree contains $a_i$ oranges. From each tree, we are allowed to pick any integer number of oranges between $0$ and $a_i$, independently of other trees. After making choices for all trees, we obtain a total number of picked oranges.

There is also a fixed number $m$, representing teammates. A valid picking plan is one where the total number of picked oranges can be evenly divided among all teammates, meaning the sum of all chosen values is divisible by $m$. The task is to count how many different picking plans satisfy this divisibility condition, where two plans differ if at least one tree contributes a different number of picked oranges.

Each tree behaves like a bounded variable contributing to a sum, and we are counting how many ways to choose these variables so that the sum lies in a specific congruence class modulo $m$.

The constraints imply that $n$ can be up to $10^5$ per test suite and $m \le 50$. The number of test cases is large, up to $10^3$, but the total $n$ across all tests is also bounded by $10^5$. This strongly suggests a solution near linear in $n$ per test, with an additional factor depending on $m$, while anything quadratic in $n$ is impossible.

A naive enumeration over all choices would consider $\prod (a_i + 1)$ configurations, which is astronomically large even for moderate inputs. Even storing or iterating over all sums is infeasible.

A more subtle edge case appears when all $a_i$ are large and $m = 1$. In that case every selection is valid, so the answer should be $\prod (a_i + 1)$ modulo $998244353$. Any method that only tracks residues without accounting for total counts must still preserve this behavior.

Another corner case is when all $a_i = 0$. There is only one way to pick nothing, and the sum is $0$, which is always divisible by $m$. The answer should always be $1$, independent of $m$.

## Approaches

A direct approach is to think of each tree as contributing a small polynomial: from tree $i$, we can pick $0,1,\dots,a_i$, so its contribution to the generating function is $x^0 + x^1 + \dots + x^{a_i}$. The total number of valid ways is the coefficient sum over all monomials whose exponent is divisible by $m$ in the product of all these polynomials.

Expanding this product directly is impossible because degrees grow up to $10^5$ per term and the number of terms explodes combinatorially.

The key observation is that we do not care about the exact sum, only its value modulo $m$. This collapses the state space from potentially $10^5 \cdot n$ possible sums to only $m \le 50$ residue classes. This immediately suggests a dynamic programming over residues.

We maintain a DP array where `dp[r]` counts how many ways to achieve a total sum congruent to $r \bmod m$. Initially, `dp[0] = 1`. For each tree, we compute how many ways it contributes to each residue class, then convolve it with the global DP.

For a single tree with value $a$, define `cnt[t]` as the number of integers in $[0,a]$ that are congruent to $t \bmod m$. This can be computed in constant time per residue using arithmetic progression counting. Then the tree contributes a small polynomial over residues, and we update DP with a convolution over modulo $m$.

Each tree update costs $O(m^2)$, giving total $O(n m^2)$, which is acceptable since $m \le 50$ and total $n \le 10^5$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(\prod (a_i+1))$ | $O(n)$ | Too slow |
| DP over residues | $O(n m^2)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Initialize a DP array of size $m$, with all values zero except `dp[0] = 1`. This represents that before choosing any trees, the only achievable sum is 0.
2. For each tree $i$, compute how many integers in $[0, a_i]$ fall into each residue class modulo $m$. We do this by first writing $a_i = q \cdot m + r$. Each residue appears exactly $q$ times, and residues $0$ through $r$ appear one additional time. This gives a frequency array `cnt`.

This step matters because it compresses a large range into a compact representation over residues without losing combinatorial information.
3. Create a new DP array `ndp` initialized to zero. We will compute transitions from previous sums to new sums after processing this tree.
4. For every residue $j$ in the current DP state, and every residue $k$ from the current tree contribution, add:

$$ndp[(j+k)\bmod m] += dp[j] \cdot cnt[k]$$

This represents choosing a partial sum with residue $j$, then adding a choice from the current tree with residue $k$.
5. After filling `ndp`, replace `dp` with `ndp`.
6. After all trees are processed, the answer is `dp[0]`, since we only want sums divisible by $m$.

The correctness hinges on tracking all partial sums grouped by residue. At every step, `dp[r]` counts exactly the number of ways to obtain a sum congruent to $r$. The transition preserves this invariant because every extension of a valid partial configuration is counted exactly once, and residue addition mod $m$ correctly updates the class.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        dp = [0] * m
        dp[0] = 1

        for x in a:
            q, r = divmod(x, m)

            cnt = [q] * m
            for i in range(r + 1):
                cnt[i] += 1

            ndp = [0] * m
            for j in range(m):
                if dp[j] == 0:
                    continue
                for k in range(m):
                    if cnt[k] == 0:
                        continue
                    ndp[(j + k) % m] = (ndp[(j + k) % m] + dp[j] * cnt[k]) % MOD

            dp = ndp

        print(dp[0] % MOD)

if __name__ == "__main__":
    solve()
```

The DP array `dp` stores counts of achievable residues. For each tree, the array `cnt` compresses the range of choices into residue frequencies. The nested loops implement the convolution over modulo classes. The modulus is applied during transitions to avoid overflow and to match the required output format.

A subtle point is handling `cnt`: it always sums to $a_i + 1$, so the total number of ways is preserved across transitions. The modulo operation is applied only to the final residue index, not to the choice count structure itself.

## Worked Examples

Consider the input:

```
n = 3, m = 2
a = [1, 1, 1]
```

Each tree allows picking either 0 or 1. So each contributes one 0 and one 1.

After first tree, DP is:

| residue | dp |
| --- | --- |
| 0 | 1 |
| 1 | 1 |

After second tree:

| j (old dp) | cnt | contributions |
| --- | --- | --- |
| 0 | {0:1,1:1} | adds to 0 and 1 |
| 1 | {0:1,1:1} | adds to 1 and 0 |

Resulting dp:

| residue | dp |
| --- | --- |
| 0 | 2 |
| 1 | 2 |

After third tree, the same transformation applies, yielding:

| residue | dp |
| --- | --- |
| 0 | 4 |
| 1 | 4 |

So the answer is `dp[0] = 4`.

This trace shows that the DP remains symmetric because each tree contributes identical residue structure, and the invariant that dp represents full convolution over choices is preserved.

Now consider:

```
n = 1, m = 3
a = [4]
```

We can pick 0 to 4, giving residues:

0,1,2,0,1. So counts are:

| residue | cnt |
| --- | --- |
| 0 | 2 |
| 1 | 2 |
| 2 | 1 |

Starting from dp = [1,0,0], after convolution we get dp = [2,2,1]. The answer is 2, corresponding to picking 0 or 3 oranges.

This confirms that the residue compression correctly accounts for uneven distribution when $a_i$ is not a multiple of $m$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n m^2)$ | Each of $n$ trees performs a convolution over $m$ residue states |
| Space | $O(m)$ | Only two DP arrays of size $m$ are maintained |

With $m \le 50$ and total $n \le 10^5$, the total operations are around $2.5 \times 10^8$ in worst case constant factor form, but with small inner loops and tight integer operations, this fits within typical 2.5s limits in PyPy or optimized Python.

## Test Cases

```python
import sys, io

MOD = 998244353

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        dp = [0] * m
        dp[0] = 1
        for x in a:
            q, r = divmod(x, m)
            cnt = [q] * m
            for i in range(r + 1):
                cnt[i] += 1
            ndp = [0] * m
            for j in range(m):
                if dp[j] == 0:
                    continue
                for k in range(m):
                    if cnt[k] == 0:
                        continue
                    ndp[(j + k) % m] = (ndp[(j + k) % m] + dp[j] * cnt[k]) % MOD
            dp = ndp
        print(dp[0])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue().strip()

# sample-style tests
assert run("1\n3 2\n1 1 1\n") == "4"
assert run("1\n1 3\n4\n") == "2"

# edge cases
assert run("1\n3 1\n1000000000 1000000000 1000000000\n") == str((1000000001*1000000001*1000000001)%MOD)
assert run("1\n1 5\n0\n") == "1"
assert run("1\n2 2\n0 0\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones, m=2 | 4 | basic convolution correctness |
| single large range | 2 | uneven residue distribution |
| m=1 large values | product of (a_i+1) | modulus edge behavior |
| all zeros | 1 | trivial configuration |
| multiple zero trees | 1 | no-choice stability |

## Edge Cases

When $m = 1$, every sum is divisible by $m$, so the DP should effectively count all possible selections. The algorithm handles this because `cnt` always sums to $a_i + 1$, and `dp` has only one state, so it multiplies all contributions correctly without any residue mixing.

When all $a_i = 0$, each `cnt` array has `cnt[0] = 1` and all other entries zero. The DP never changes from its initial state, so `dp[0]` remains 1, matching the fact that there is exactly one way to pick nothing.

When $n$ is large but all $a_i < m$, the distribution inside `cnt` becomes highly sparse, but the convolution still works correctly because it explicitly iterates over all residues and preserves zero entries.
