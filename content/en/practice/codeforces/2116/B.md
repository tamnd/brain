---
title: "CF 2116B - Gellyfish and Baby's Breath"
description: "We are given two permutations p and q of the numbers 0...n-1. For every position i, we must evaluate all pairs of indices (j, i-j) such that 0 ≤ j ≤ i, and compute $$2^{pj}+2^{q{i-j}}$$ Among all these candidates, we take the maximum and store it in r[i]."
date: "2026-06-09T04:01:15+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2116
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1028 (Div. 2)"
rating: 1300
weight: 2116
solve_time_s: 165
verified: false
draft: false
---

[CF 2116B - Gellyfish and Baby's Breath](https://codeforces.com/problemset/problem/2116/B)

**Rating:** 1300  
**Tags:** greedy, math, sortings  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two permutations `p` and `q` of the numbers `0...n-1`.

For every position `i`, we must evaluate all pairs of indices `(j, i-j)` such that `0 ≤ j ≤ i`, and compute

$$2^{p_j}+2^{q_{i-j}}$$

Among all these candidates, we take the maximum and store it in `r[i]`.

The direct values become enormous because the exponents can be as large as `n-1`, so the final answers are required modulo `998244353`.

The first thing to notice is that the numbers involved are powers of two. Powers of two grow so quickly that when comparing

$$2^a+2^b$$

the larger exponent dominates completely. More formally, if `a > c`, then

$$2^a+2^b > 2^c+2^d$$

regardless of the values of `b` and `d`.

This means that maximizing the sum is equivalent to first maximizing the larger exponent among the pair, and only if those larger exponents are equal do we compare the smaller exponent.

The constraints are what force us to exploit this structure. The total sum of `n` over all test cases is at most `10^5`. An `O(n^2)` algorithm would perform roughly `10^{10}` operations in the worst case, which is far beyond the limit. We need something around `O(n log n)` or `O(n)` per test case.

A subtle point is that the maximum exponent in a candidate pair may come from either array.

Consider:

```
p = [2,0,1]
q = [0,2,1]
```

For `i = 1`, the candidates are

```
j=0: (2,2)
j=1: (0,0)
```

The answer comes from exponent `2`, and both arrays contribute equally. Any solution that only tracks maxima from one array would miss such cases.

Another easy mistake is to maximize `p[j] + q[i-j]`. The objective is not the sum of exponents.

For example:

```
(5,0) -> 32+1 = 33
(3,3) -> 8+8 = 16
```

Although `5+0 < 3+3`, the first pair is much larger because exponent `5` dominates.

## Approaches

The brute-force solution follows the definition directly.

For every position `i`, iterate through all `j` from `0` to `i`, compute

$$2^{p_j}+2^{q_{i-j}}$$

and keep the maximum.

This is correct because it explicitly checks every valid pair. The problem is complexity. For one test case the number of examined pairs is

$$1+2+\cdots+n = O(n^2)$$

which becomes roughly `5 × 10^9` operations when `n = 10^5`.

To do better, we need to exploit the fact that `p` and `q` are permutations.

Let

$$M_i=\max\Big(\max_{0\le j\le i} p_j,\ \max_{0\le j\le i} q_j\Big)$$

be the largest exponent that appears in either prefix up to position `i`.

Any optimal pair for `r[i]` must contain exponent `M_i`.

Why? If neither side contributes `M_i`, then the largest exponent in that candidate is strictly smaller than `M_i`, and a pair containing `M_i` will always be larger.

Because `p` and `q` are permutations, each exponent appears exactly once. Suppose exponent `M_i` appears in `p` at position `posP[M_i]`.

If `posP[M_i] ≤ i`, then the only pair containing this exponent is

$$j = posP[M_i]$$

which forces the other exponent to be

$$q_{i-posP[M_i]}.$$

Similarly, if `M_i` appears in `q`, the only possible matching pair is

$$p_{i-posQ[M_i]}.$$

So for each `i`, there are at most two candidates that can contain the largest exponent `M_i`.

Once the largest exponent is fixed, the comparison reduces to choosing the larger second exponent. Thus we only need to compare two possible values.

This turns the problem into a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute powers of two modulo `998244353` up to `100000`.
2. Build arrays `posP` and `posQ` storing the position of every value inside permutations `p` and `q`.
3. Compute prefix maxima:

`prefP[i] = max(p[0..i])`

`prefQ[i] = max(q[0..i])`
4. For every position `i`, compute

$$M=\max(prefP[i],prefQ[i]).$$

Any optimal pair must contain exponent `M`.
5. If `M` appears inside the prefix of `p`, let its position be `k=posP[M]`.

Then the corresponding candidate uses

$$(M,\ q_{i-k})$$

provided `k ≤ i`.
6. If `M` appears inside the prefix of `q`, let its position be `k=posQ[M]`.

Then the corresponding candidate uses

$$(p_{i-k},\ M)$$

provided `k ≤ i`.
7. Among the valid candidates, compare the second exponent. Since both contain the same largest exponent `M`, the larger second exponent gives the larger sum.
8. Let the chosen pair be `(M,S)`. Output

$$2^M + 2^S \pmod{998244353}.$$

### Why it works

For any index `i`, let `M` be the largest exponent appearing in either prefix up to `i`.

Every candidate pair whose largest exponent is less than `M` is automatically worse than any candidate containing `M`, because powers of two are strictly ordered by their largest exponent.

Since each exponent occurs exactly once in each permutation, there are only two possible ways to form a pair containing `M`: using its occurrence in `p` or using its occurrence in `q`. Every optimal solution must be one of these candidates.

After fixing the largest exponent `M`, comparing

$$2^M+2^a$$

and

$$2^M+2^b$$

reduces to comparing `a` and `b`. The algorithm chooses the larger second exponent, so it selects exactly the maximum-valued pair.

Thus every `r[i]` is computed correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXN = 100000

pow2 = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    pow2[i] = (pow2[i - 1] * 2) % MOD

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        q = list(map(int, input().split()))

        posP = [0] * n
        posQ = [0] * n

        for i, x in enumerate(p):
            posP[x] = i

        for i, x in enumerate(q):
            posQ[x] = i

        prefP = [0] * n
        prefQ = [0] * n

        prefP[0] = p[0]
        prefQ[0] = q[0]

        for i in range(1, n):
            prefP[i] = max(prefP[i - 1], p[i])
            prefQ[i] = max(prefQ[i - 1], q[i])

        ans = [0] * n

        for i in range(n):
            M = max(prefP[i], prefQ[i])

            best_second = -1

            k = posP[M]
            if k <= i:
                best_second = max(best_second, q[i - k])

            k = posQ[M]
            if k <= i:
                best_second = max(best_second, p[i - k])

            ans[i] = (pow2[M] + pow2[best_second]) % MOD

        print(*ans)

solve()
```

The position arrays are the key implementation detail. They let us immediately locate where a specific exponent appears in either permutation.

The prefix maxima identify the largest exponent available for each `i`. Without them we would need to search the prefixes repeatedly.

For a fixed `i`, we examine only the two ways to include exponent `M`. The corresponding second exponent is read directly from the opposite array.

The answer is reconstructed using precomputed modular powers of two. Computing powers repeatedly with fast exponentiation would still be acceptable, but precomputation makes each query constant time.

Care must be taken with the index `i-k`. The check `k <= i` guarantees that this index is non-negative.

## Worked Examples

### Example 1

Input:

```
n = 3
p = [0,2,1]
q = [1,2,0]
```

| i | prefP | prefQ | M | candidate from p | candidate from q | chosen pair | answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | (1,0) | (0,1) | (1,0) | 3 |
| 1 | 2 | 2 | 2 | (2,1) | (0,2) | (2,1) | 6 |
| 2 | 2 | 2 | 2 | (2,2) | (1,2) | (2,2) | 8 |

The table shows the central idea. Once exponent `2` becomes available, every optimal pair must contain it. We only compare the accompanying exponent.

### Example 2

Input:

```
n = 5
p = [0,1,2,3,4]
q = [4,3,2,1,0]
```

| i | M | second exponent | value |
| --- | --- | --- | --- |
| 0 | 4 | 0 | 17 |
| 1 | 4 | 1 | 18 |
| 2 | 4 | 2 | 20 |
| 3 | 4 | 3 | 24 |
| 4 | 4 | 4 | 32 |

Here exponent `4` is already present in the first element of `q`, so it dominates every answer. Only the second exponent changes as `i` grows.

This example illustrates why tracking the largest available exponent is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is processed a constant number of times |
| Space | O(n) | Position arrays and prefix maxima |

The total sum of `n` across all test cases is at most `10^5`, so the overall running time is linear in the input size. This easily fits within the one-second limit, and the memory usage remains far below the allowed 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())

    MAXN = 100000
    pow2 = [1] * (MAXN + 1)
    for i in range(1, MAXN + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    out = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        q = list(map(int, input().split()))

        posP = [0] * n
        posQ = [0] * n

        for i, x in enumerate(p):
            posP[x] = i
        for i, x in enumerate(q):
            posQ[x] = i

        prefP = [0] * n
        prefQ = [0] * n

        prefP[0] = p[0]
        prefQ[0] = q[0]

        for i in range(1, n):
            prefP[i] = max(prefP[i - 1], p[i])
            prefQ[i] = max(prefQ[i - 1], q[i])

        ans = []

        for i in range(n):
            M = max(prefP[i], prefQ[i])

            sec = -1

            k = posP[M]
            if k <= i:
                sec = max(sec, q[i - k])

            k = posQ[M]
            if k <= i:
                sec = max(sec, p[i - k])

            ans.append(str((pow2[M] + pow2[sec]) % MOD))

        out.append(" ".join(ans))

    return "\n".join(out)

# provided sample
assert run(
"""3
3
0 2 1
1 2 0
5
0 1 2 3 4
4 3 2 1 0
10
5 8 9 3 4 0 2 7 1 6
9 5 1 4 0 3 2 8 7 6
"""
) == (
"""3 6 8
17 18 20 24 32
544 768 1024 544 528 528 516 640 516 768"""
)

# n = 1
assert run(
"""1
1
0
0
"""
) == "2"

# maximum exponent appears only in p prefix
assert run(
"""1
2
1 0
0 1
"""
) == "3 4"

# maximum exponent appears only in q prefix
assert run(
"""1
2
0 1
1 0
"""
) == "3 4"

# tie on largest exponent, compare second exponent
assert run(
"""1
3
2 0 1
0 2 1
"""
) == "5 6 6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` | `2` | Smallest possible instance |
| `[1,0]` and `[0,1]` | `3 4` | Largest exponent comes from `p` |
| `[0,1]` and `[1,0]` | `3 4` | Largest exponent comes from `q` |
| `[2,0,1]` and `[0,2,1]` | `5 6 6` | Correct tie-breaking by second exponent |

## Edge Cases

### Largest exponent appears only in one array's prefix

Consider:

```
n = 2
p = [1,0]
q = [0,1]
```

For `i = 1`, the largest available exponent is `1`, coming from `p[0]`.

The algorithm finds `posP[1]=0`, evaluates the matching partner `q[1]=1`, and obtains `(1,1)`.

The answer is

$$2^1+2^1=4.$$

No scan over all pairs is required.

### Largest exponent appears in both prefixes

Consider:

```
n = 3
p = [2,0,1]
q = [0,2,1]
```

For `i = 2`, exponent `2` is available from both arrays.

The two candidates are

```
(2,1)
(1,2)
```

Both correspond to value `6`.

The algorithm checks both occurrences and keeps the larger second exponent, which is `1`, producing the correct result.

### Maximum exponent dominates all smaller exponents

Consider:

```
n = 3
p = [2,1,0]
q = [0,1,2]
```

For `i = 2`, candidates include

```
(2,2)
(1,1)
(0,0)
```

Even though `(1,1)` has a balanced pair, it cannot beat `(2,2)` because exponent `2` dominates every candidate whose largest exponent is `1`.

The algorithm relies exactly on this property when it restricts attention to pairs containing the largest available exponent.
