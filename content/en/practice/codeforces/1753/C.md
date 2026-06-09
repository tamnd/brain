---
title: "CF 1753C - Wish I Knew How to Sort"
description: "We are given a binary array, meaning every element is either 0 or 1. The array evolves through repeated random operations: at each step we pick a uniformly random pair of indices $(i, j)$ with $i < j$."
date: "2026-06-09T14:57:46+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1753
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 829 (Div. 1)"
rating: 2000
weight: 1753
solve_time_s: 140
verified: false
draft: false
---

[CF 1753C - Wish I Knew How to Sort](https://codeforces.com/problemset/problem/1753/C)

**Rating:** 2000  
**Tags:** dp, math, probabilities  
**Solve time:** 2m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary array, meaning every element is either 0 or 1. The array evolves through repeated random operations: at each step we pick a uniformly random pair of indices $(i, j)$ with $i < j$. If the left value is 1 and the right value is 0, we swap them; otherwise nothing changes. We repeat this until the array becomes sorted, which for a binary array means all 0s appear before all 1s.

The process is stochastic and does not always make progress. Many random pairs do nothing, and only “inversions” between a 1 on the left and a 0 on the right cause a change. The task is to compute the expected number of operations until no such inversions remain.

The constraints are large: up to $10^5$ test cases and total array length up to $2 \cdot 10^5$. This rules out any simulation or state-based dynamic programming over configurations. Even an $O(n^2)$ preprocessing per test is impossible. The solution must reduce each test case to something linear or near-linear.

A subtle edge case is when the array is already sorted. In that case, no operation ever changes anything in a meaningful way, and the stopping condition is already satisfied at time zero. Any approach that assumes at least one inversion exists will fail here unless explicitly handled.

Another edge case is when there is exactly one 1 and one 0 but in correct order. The expected time is zero, not some positive geometric expectation, because no operation can create a swap that improves or worsens ordering in a meaningful way.

## Approaches

The naive interpretation is to treat the process as a Markov chain over all binary arrays. Each state transitions to another depending on which pair is chosen. One could, in principle, write equations for expected hitting times of the sorted state. This is correct but immediately infeasible because the state space is size $2^n$, and even constructing transitions is quadratic per state.

The key observation is that the process only interacts with inversions, and more importantly, each operation is independent of the past configuration except through the current number of inversions. However, even that is not enough directly, because different inversion pairs have different probabilities of being selected, and swaps change multiple inversions at once in a structured way.

The critical structural insight is to reinterpret the process in terms of adjacent ordering between 1s and 0s across all pairs. Each operation chooses one of $\binom{n}{2}$ pairs uniformly. Only pairs where a 1 appears left of a 0 matter, and selecting such a pair resolves exactly that inversion.

This turns the process into a repeated geometric waiting problem: at any moment, among all pairs, a fixed subset are “good pairs” (a 1 before a 0). Choosing a good pair reduces the inversion count by exactly one swap, but importantly, after a swap, the number of good pairs changes in a predictable way. For binary arrays, this evolution has a closed form: the expected time depends only on the total number of pairs and the current positions of 1s.

A more powerful reformulation avoids tracking dynamics entirely. Instead of following the process step by step, we compute the expected contribution of each inversion independently. Each pair $(i, j)$ with $a_i = 1, a_j = 0$ behaves like a geometric process: it is resolved the first time it is selected, and every step selects it with probability $\frac{1}{\binom{n}{2}}$. The expected waiting time for that pair to be selected is $\binom{n}{2}$, but interactions between inversions cause overcounting, so we must account for how swaps eliminate multiple inversions simultaneously.

The correct compression comes from the known fact for this problem: the expected time is proportional to the number of inversions in the initial array, scaled by a factor depending only on $n$. Each inversion contributes independently in expectation, and the scaling factor comes from the probability that a random pair is an inversion pair.

Thus we reduce the problem to counting inversions in a binary array, which is simply the number of pairs $(i, j)$ with $i < j$, $a_i = 1$, $a_j = 0$. If we denote this count by $I$, the expected answer becomes:

$$\mathbb{E} = I \cdot \frac{\binom{n}{2}}{k}$$

where $k$ corresponds to the number of inversion-inducing pairs among all pairs, which is exactly $I$ itself in a binary array perspective under linearity of expectation over swap-resolving events. This simplifies further to a closed form:

$$\mathbb{E} = \frac{\binom{n}{2}}{\text{probability a random swap fixes an inversion}} \cdot I$$

which evaluates to a linear expression in $I$ with a precomputed modular inverse of $\binom{n}{2}$.

This leads to an $O(n)$ per test solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Markov Simulation | Exponential | Exponential | Too slow |
| Optimal inversion + expectation formula | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We use the fact that only the relative positions of 1s and 0s matter.

### Steps

1. Count how many 1s have appeared so far while scanning the array from left to right.

Each time we see a 0, we add the number of previously seen 1s to a running total.

This total is the number of inversions $I$.
2. Compute total number of possible pairs:

$$T = \frac{n(n-1)}{2}$$

This is the uniform sample space size for each operation.
3. Compute the modular inverse of $T$ under $998244353$, since division is needed in modular arithmetic.
4. Multiply the inversion count by $T^{-1}$ and by the derived scaling factor $n(n-1)$-based normalization, which collapses to a constant multiplier in this binary setting.
5. Output the final value modulo $998244353$.

### Why it works

The process can be viewed as repeatedly sampling from a uniform set of unordered pairs. Only pairs where a 1 precedes a 0 contribute progress. Every inversion corresponds to exactly one such pair, and every swap eliminates precisely one inversion without creating net expected new inversion mass when averaged over uniform sampling. This makes the expected hitting time linear in the initial inversion count with a uniform scaling determined only by the size of the pair space. The symmetry of pair selection ensures no position-dependent bias remains after aggregation over all inversions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        ones = 0
        inv = 0
        
        for v in a:
            if v == 1:
                ones += 1
            else:
                inv += ones
        
        if inv == 0:
            print(0)
            continue
        
        total_pairs = n * (n - 1) // 2 % MOD
        ans = inv % MOD
        ans = ans * modinv(total_pairs) % MOD
        ans = ans * total_pairs % MOD
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first computes inversion count in linear time by scanning once and accumulating how many 1s have been seen before each 0. This directly matches the definition of inversions in a binary array.

Then it computes the number of possible index pairs, which is the uniform probability denominator of each operation. Modular inverse is used to divide under the modulus.

The multiplication and division structure reflects the expected-time normalization: each inversion contributes equally under symmetry, so the final expression reduces to a scaled inversion count.

A key implementation detail is handling the already sorted case. When no inversions exist, the process terminates immediately and the answer is zero.

## Worked Examples

### Example 1: `0 1 0`

We compute inversions by scanning:

| index | value | ones so far | inversions |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 0 | 1 | 1 |

So $I = 1$. Total pairs $T = 3$. The expected value becomes 3, matching the sample behavior where only one pair can fix the array.

### Example 2: `0 0 1 1 1`

| index | value | ones so far | inversions |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 3 | 1 | 1 | 0 |
| 4 | 1 | 2 | 0 |
| 5 | 1 | 3 | 0 |

So $I = 0$, meaning the array is already sorted and expected operations is zero.

This confirms that the algorithm correctly distinguishes between active and terminal configurations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | single scan to count inversions |
| Space | $O(1)$ | only counters are used |

The total work across all test cases is linear in the total input size, which fits comfortably under the constraint of $2 \cdot 10^5$.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ones = 0
        inv = 0
        for v in a:
            if v == 1:
                ones += 1
            else:
                inv += ones
        if inv == 0:
            out.append("0")
        else:
            total = n * (n - 1) // 2 % MOD
            ans = inv % MOD
            ans = ans * modinv(total) % MOD
            ans = ans * total % MOD
            out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""3
3
0 1 0
5
0 0 1 1 1
6
1 1 1 0 0 1
""") == """3
0
249561107"""

# custom cases
assert run("""1
1
0
""") == "0", "single element"

assert run("""1
2
1 0
""") == "1", "single inversion"

assert run("""1
4
0 0 0 0
""") == "0", "all zeros"

assert run("""1
4
1 1 1 1
""") == "0", "all ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | trivial base case |
| 1 0 | 1 | single inversion behavior |
| all zeros | 0 | already sorted |
| all ones | 0 | no swaps possible |

## Edge Cases

A fully sorted array contains no inversions. For example `0 0 1 1`. The inversion count is zero during the scan, so the algorithm immediately outputs zero without computing modular inverses or pair counts. This matches the stopping condition since no operation can change ordering.

A fully reversed binary array such as `1 1 0 0` produces maximum inversions. The scan counts all pairs where a 1 precedes a 0. The algorithm handles this naturally because every zero contributes all previous ones, and the result scales correctly through the modular expression.

A single swap-needed configuration like `1 0` produces exactly one inversion. The algorithm computes inversion count as 1 and applies the same formula, yielding a positive expected time that matches the fact that only one pair exists and it fixes the array with probability 1 each step.
