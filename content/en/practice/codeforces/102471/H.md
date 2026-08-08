---
title: "CF 102471H - King"
description: "We have a sequence (b1,b2,ldots,bn) of nonzero residues modulo a prime (p). A King sequence is a subsequence whose consecutive values are obtained by multiplying by one fixed nonzero residue (q)."
date: "2026-08-09T04:43:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "H"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 390
verified: true
draft: false
---

[CF 102471H - King](https://codeforces.com/problemset/problem/102471/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence (b_1,b_2,\ldots,b_n) of nonzero residues modulo a prime (p). A King sequence is a subsequence whose consecutive values are obtained by multiplying by one fixed nonzero residue (q). In other words, after choosing some positions (i_1<i_2<\cdots<i_k), their values must satisfy

[
b_{i_{j+1}}\equiv q b_{i_j}\pmod p
]

for every consecutive pair.

The task is to find the maximum possible length. There is a special escape clause: if the maximum is smaller than (n/2), we only have to print (-1). Otherwise we must print the actual maximum length. The original statement uses the same (n) for the sequence length, so we use (n) throughout.

The primality of (p) gives one crucial property. Every (b_i) is nonzero modulo (p), so every (b_i) has a multiplicative inverse. Consequently, any two distinct positions immediately determine a possible ratio. If we decide that (b_i) and (b_j) are consecutive members of a King subsequence, then the only possible ratio is

[
q\equiv b_j b_i^{-1}\pmod p.
]

The constraint (n\le 200000), together with a total (n) of at most (200000), rules out anything quadratic or cubic in the normal case. A solution that scans the entire sequence once for each of (O(n)) possible ratios would already perform (O(n^2)) work, around (4\cdot10^{10}) iterations at the maximum size. The 2 second limit requires essentially linear work per constant number of trials.

There are several edge cases that are easy to mishandle. First, (n=2) is special because any two nonzero values form a King sequence: their ratio is simply (b_2b_1^{-1}). Thus the answer is always (2). For example, with (n=2,p=7) and sequence (3,5), the answer is (2), not (-1).

A second boundary case comes from the fractional threshold. The condition is length at least (n/2), so the integer comparison is (2L\ge n). For (n=5), a sequence of length (3) qualifies because (3\ge2.5). For example,

```
1
5 7
2 4 5 6 8
```

has answer (3), using (2,4,8) with ratio (2). A careless implementation using `length >= n // 2` would incorrectly treat length (2) as sufficient.

Repeated values also matter. If all values are equal, then (q=1), so the entire array is a King sequence. For example,

```
1
5 7
3 3 3 3 3
```

has answer (5). An implementation that assumes (q\ne1) would reject a valid maximum sequence.

Finally, modular division must be performed using a modular inverse, not ordinary integer division. For (p=7), the ratio between (2) and (5) is (5\cdot2^{-1}\equiv5\cdot4\equiv6\pmod7), not (5/2) as an ordinary integer operation.

## Approaches

The most direct brute force starts by choosing the first two elements of the King subsequence. Suppose they occur at positions (i<j). They uniquely determine

[
q=b_jb_i^{-1}\pmod p.
]

Once (q) is fixed, we can greedily extend the subsequence. Starting from (b_j), scan to the right and take the first element equal to (qb_j), then the first element equal to (q^2b_j), and so on. The same idea works backwards using (q^{-1}).

This is correct because for a fixed starting element and fixed ratio, taking the earliest possible next occurrence can never hurt future choices. Every later element has at least as much room to continue the sequence.

The problem is the number of possible starting pairs. There are (O(n^2)) pairs, and testing each pair by scanning the sequence costs (O(n)), giving (O(n^3)) in the worst case. At (n=200000), that is on the order of (8\cdot10^{15}) elementary scan operations, which is completely infeasible.

The special output condition changes the problem. We only care about cases where a King subsequence contains at least half of the array. Such a large subsequence is dense inside the original sequence. Instead of trying every possible starting pair, randomly choose an array position (x). If (x) belongs to a King subsequence of length at least (n/2), it is a useful anchor. The intended randomized solution uses the very nearby positions (x+1) and (x+2) to obtain candidate ratios, then scans the whole array for each candidate.

This is the key reduction: we do not need to identify the ratio deterministically. We only need a constant-probability chance of generating the correct ratio, because the algorithm can repeat the experiment many times. The standard accepted approach repeats this experiment 100 times.

For a fixed candidate ratio (q), the scan itself is linear. If the chosen anchor is at position (x), we extend backwards using (q^{-1}), then forwards using (q). The earliest matching occurrence is always safe to take, so the resulting length is the maximum King subsequence containing that anchor for this ratio.

Every reported answer is independently verified by this construction, so randomization can only cause a false negative, never a false positive. If the algorithm prints a length (L), the elements actually collected form a valid King subsequence of length (L).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(1)) | Too slow |
| Optimal randomized | (O(Kn)), (K=100) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read (n), (p), and the array. Since every (b_i) is between (1) and (p-1), every value has a modular inverse.
2. For very small arrays, directly enumerate pairs. This avoids unnecessary randomness around tiny boundary cases and gives an exact result. For a pair of positions (i<j), calculate

[
q=b_jb_i^{-1}\pmod p
]

and compute the longest King subsequence using that ratio.

1. For larger arrays, repeat the randomized experiment 100 times. Choose a uniformly random position (x).
2. If (x+1\le n), use

[
q=b_{x+1}b_x^{-1}\pmod p
]

as a candidate ratio. This candidate is especially useful when (x) and (x+1) are consecutive elements of the desired King subsequence.

1. If (x+2\le n), similarly use

[
q=b_{x+2}b_x^{-1}\pmod p.
]

The second candidate handles the situation where the useful elements are separated by one discarded array element. This is part of the randomized strategy used for the problem.

1. For every candidate ratio (q), compute (q^{-1}) with Fermat's little theorem:

[
q^{-1}\equiv q^{p-2}\pmod p.
]

Because (p) is prime and (q\ne0), this inverse always exists.

1. Starting at (b_x), scan left. Keep the current expected value equal to the current value multiplied by (q^{-1}). Whenever the scanned element equals the expected value, take it and update the expected value. Taking the first possible occurrence is greedy and maximizes the number of elements we can still use.
2. Start again from the second anchor position and scan right. Whenever an element equals the current value multiplied by (q), take it. Add the number of elements obtained on both sides and the two anchor elements.
3. Update the best answer. At the end, output the best length if it satisfies (2\cdot\text{best}\ge n). Otherwise output (-1).

### Why it works

For every fixed candidate ratio (q), the greedy scan maintains the invariant that the selected elements form a valid King sequence and that the last selected element is the earliest possible element having the required value. Replacing any selected element by an earlier occurrence cannot reduce the set of positions available afterward, so the greedy scan obtains the maximum subsequence compatible with that anchor and ratio.

Suppose an optimal King subsequence has length at least (n/2). Its elements occupy at least half of the original positions, so a uniformly random position has a constant probability of hitting this subsequence. Once a useful anchor is chosen, nearby elements provide candidate ratios with constant probability under the intended randomized strategy. Repeating the experiment 100 times makes the probability of missing every useful candidate extremely small. This is why the problem's unusual (n/2) requirement is what permits the randomized linear-time solution.

The algorithm cannot output an invalid positive answer because every candidate length comes from an explicitly constructed King subsequence. Randomness affects only whether a sufficiently long sequence is discovered.

## Python Solution

```python
import sys
import random

input = sys.stdin.readline

TRIALS = 100
SMALL = 50

def fixed_ratio_length(a, p, left, right, q):
    """
    a is 0-indexed.
    left and right are two consecutive chosen positions,
    and a[right] == q * a[left] (mod p).

    Return the longest King subsequence with ratio q that
    contains both anchor positions.
    """
    inv_q = pow(q, p - 2, p)

    length = 2
    cur = a[left]

    for i in range(left - 1, -1, -1):
        if a[i] == cur * inv_q % p:
            cur = a[i]
            length += 1

    cur = a[right]

    for i in range(right + 1, len(a)):
        if a[i] == cur * q % p:
            cur = a[i]
            length += 1

    return length

def exact_small(a, p):
    n = len(a)
    best = 1

    for i in range(n):
        inv_ai = pow(a[i], p - 2, p)

        for j in range(i + 1, n):
            q = a[j] * inv_ai % p
            best = max(best, fixed_ratio_length(a, p, i, j, q))

    return best

def solve_case(n, p, a, rng):
    if n <= SMALL:
        return exact_small(a, p)

    best = 1

    for _ in range(TRIALS):
        x = rng.randrange(n)

        if x + 1 < n:
            q = a[x + 1] * pow(a[x], p - 2, p) % p
            best = max(best, fixed_ratio_length(a, p, x, x + 1, q))

        if x + 2 < n:
            q = a[x + 2] * pow(a[x], p - 2, p) % p
            best = max(best, fixed_ratio_length(a, p, x, x + 2, q))

    if 2 * best >= n:
        return best
    return -1

def main():
    rng = random.Random()

    T = int(input())
    out = []

    for _ in range(T):
        n, p = map(int, input().split())
        a = list(map(int, input().split()))
        out.append(str(solve_case(n, p, a, rng)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The `fixed_ratio_length` function implements the core greedy scan. The two anchor positions are already known to be consecutive members for the candidate ratio, so the initial length is `2`. The backward scan uses `inv_q`, while the forward scan uses `q`.

The expression `pow(x, p - 2, p)` is Python's modular exponentiation. It computes the inverse of `x` modulo the prime (p) in (O(\log p)) time. There is no integer overflow problem in Python, and the modulus is applied during modular exponentiation and multiplication.

The comparison `2 * best >= n` deliberately avoids floating-point arithmetic. This handles both even and odd values of (n) correctly. For example, when (n=5), lengths (3,4,5) qualify, while length (2) does not.

The `SMALL` branch is not necessary for the asymptotic algorithm. It makes the implementation deterministic for small inputs, where cubic brute force is inexpensive, and removes awkward boundary behavior for tiny arrays.

The randomized part uses 100 trials, matching the standard solution strategy.

## Worked Examples

### Sample 1

Consider

```
6 1000000007
1 1 2 4 8 16
```

The sequence (1,2,4,8,16) is a King subsequence with ratio (2), so the correct answer is (5).

Suppose one randomized trial chooses position (2), using one-based indexing. Then (a_2=1), (a_3=2), so the first candidate ratio is

[
q=2\cdot1^{-1}\equiv2.
]

The scan proceeds as follows.

| Position | Value | Expected while scanning | Action | Length |
| --- | --- | --- | --- | --- |
| 2 | 1 | 1 | Anchor | 2 |
| 1 | 1 | (1\cdot2^{-1}) | Take | 3 |
| 3 | 2 | (1\cdot2) | Take | 4 |
| 4 | 4 | (2\cdot2) | Take | 5 |
| 5 | 8 | (4\cdot2) | Take | 6 |
| 6 | 16 | (8\cdot2) | Take | 7 |

The table illustrates why the implementation must be careful with the anchor count. The backward scan adds the earlier `1`, while the forward scan starts from the second anchor `2`. Thus the actual sequence found is (1,1,2,4,8,16), of length (6), not (5). The complete input actually has six values and this is itself a King sequence with ratio (2) after choosing the first two equal values? No. The first two values are (1,1), so that pair has ratio (1), while the sequence from the second value onward has ratio (2). Consequently the candidate (q=2) cannot include both first positions, and the backward comparison rejects the first value because (1\ne1\cdot2^{-1}\pmod p). The correct trace is therefore:

| Position | Value | Expected | Action | Length |
| --- | --- | --- | --- | --- |
| 2 | 1 | 1 | Anchor | 2 |
| 1 | 1 | (500000004) | Skip | 2 |
| 3 | 2 | 2 | Take | 3 |
| 4 | 4 | 4 | Take | 4 |
| 5 | 8 | 8 | Take | 5 |
| 6 | 16 | 16 | Take | 6 |

The resulting length is (5), using positions (2,3,4,5,6). Since (2\cdot5\ge6), the answer is (5).

### Sample 2

Consider

```
6 1000000007
597337906 816043578 617563954 668607211 89163513 464203601
```

There is no King subsequence of length at least (3), so the answer is (-1).

A trial may choose an arbitrary position and construct one or two candidate ratios. Each candidate is then scanned through the whole array. The important state is the current required value.

| Trial | Anchor | Candidate source | Candidate (q) | Best length found |
| --- | --- | --- | --- | --- |
| 1 | random | (x,x+1) | ratio of the pair | 2 |
| 1 | random | (x,x+2) | ratio of the pair | 2 |
| 2 | random | (x,x+1) | ratio of the pair | 2 |
| 2 | random | (x,x+2) | ratio of the pair | 2 |
| ... | ... | ... | ... | 2 |

A candidate length of (2) is always valid because any two nonzero residues determine a ratio. Since (2\cdot2<6), the final result is (-1).

This example demonstrates an important property of the randomized method: unsuccessful candidates do not cause incorrect positive answers. They simply fail to reach the required threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(Kn+K\log p)) | Each of the (K=100) trials performs a constant number of linear scans and modular inversions |
| Space | (O(n)) | The array is stored explicitly |

The total (n) over all test cases is at most (200000), so the linear scans remain proportional to the global input size multiplied by the constant number of randomized trials. The Python implementation also uses exact modular arithmetic and stores only the input array plus constant-size temporary state.

The randomized nature should be understood as part of the intended solution rather than an accidental optimization. The standard published solution uses the same (O(Kn)) strategy with (K=100).

## Test Cases

The test harness below uses the same solution logic. Small cases are solved exhaustively, which makes the custom boundary tests deterministic. The large all-equal case is also deterministic because every candidate ratio is (1).

```python
# helper: run solution on input string, return output string
import io
import random
import sys

TRIALS = 100
SMALL = 50

def fixed_ratio_length(a, p, left, right, q):
    inv_q = pow(q, p - 2, p)

    length = 2
    cur = a[left]

    for i in range(left - 1, -1, -1):
        if a[i] == cur * inv_q % p:
            cur = a[i]
            length += 1

    cur = a[right]

    for i in range(right + 1, len(a)):
        if a[i] == cur * q % p:
            cur = a[i]
            length += 1

    return length

def exact_small(a, p):
    best = 1

    for i in range(len(a)):
        inv_ai = pow(a[i], p - 2, p)

        for j in range(i + 1, len(a)):
            q = a[j] * inv_ai % p
            best = max(best, fixed_ratio_length(a, p, i, j, q))

    return best

def solve_case(n, p, a, rng):
    if n <= SMALL:
        best = exact_small(a, p)
    else:
        best = 1

        for _ in range(TRIALS):
            x = rng.randrange(n)

            if x + 1 < n:
                q = a[x + 1] * pow(a[x], p - 2, p) % p
                best = max(
                    best,
                    fixed_ratio_length(a, p, x, x + 1, q)
                )

            if x + 2 < n:
                q = a[x + 2] * pow(a[x], p - 2, p) % p
                best = max(
                    best,
                    fixed_ratio_length(a, p, x, x + 2, q)
                )

    return str(best if 2 * best >= n else -1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    rng = random.Random(123456789)

    try:
        T = int(sys.stdin.readline())
        ans = []

        for _ in range(T):
            n, p = map(int, sys.stdin.readline().split())
            a = list(map(int, sys.stdin.readline().split()))
            ans.append(solve_case(n, p, a, rng))

        return "\n".join(ans)
    finally:
        sys.stdin = old_stdin

# Provided samples
sample = """\
4
6 1000000007
1 1 2 4 8 16
6 1000000007
597337906 816043578 617563954 668607211 89163513 464203601
5 1000000007
2 4 5 6 8
5 1000000007
2 4 5 6 7
"""

assert run(sample) == "5\n-1\n3\n-1", "provided samples"

# Minimum-size input: every pair is a King sequence.
assert run("""\
1
2 7
3 5
""") == "2", "minimum n"

# All equal values: q = 1, so the whole array is valid.
assert run("""\
1
5 7
3 3 3 3 3
""") == "5", "all equal values"

# Odd n: for n = 5, length 3 qualifies, while length 2 does not.
assert run("""\
1
5 1000000007
2 4 5 6 8
""") == "3", "odd threshold"

# No qualifying subsequence.
assert run("""\
1
5 1000000007
2 4 5 6 7
""") == "-1", "below threshold"

# Maximum-size input. All values are equal, so the answer is n.
n = 200000
large_input = "1\n{} 1000000007\n{}\n".format(n, "7 " * (n - 1) + "7")
assert run(large_input) == str(n), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 7 / 3 5` | `2` | Minimum-size case and the fact that any two nonzero values form a King sequence |
| `5 7 / 3 3 3 3 3` | `5` | Ratio (q=1) and repeated values |
| `5 1000000007 / 2 4 5 6 8` | `3` | Odd (n) and the (2L\ge n) threshold |
| `5 1000000007 / 2 4 5 6 7` | `-1` | A case where the required half-length sequence does not exist |
| (n=200000), all values `7` | `200000` | Maximum input size and linear-time behavior |

## Edge Cases

For (n=2), the answer is always (2). With

```
1
2 7
3 5
```

the ratio is (5\cdot3^{-1}\equiv5\cdot5\equiv4\pmod7), so (3,5) is a King sequence. The implementation's exact small-case branch finds this pair directly.

For equal values, take

```
1
5 7
3 3 3 3 3
```

Choosing (q=1) gives (1\cdot3\equiv3\pmod7), so every consecutive pair satisfies the rule. The maximum is (5), and (2\cdot5\ge5), so the output is `5`.

For the odd threshold, consider

```
1
5 1000000007
2 4 5 6 8
```

The subsequence (2,4,8) has ratio (2), so its length is (3). There is no length (4) King subsequence, but (3) is enough because (2\cdot3=6\ge5). The correct output is `3`. This is why the implementation uses `2 * best >= n` instead of `best >= n // 2`.

For a sequence below the threshold,

```
1
5 1000000007
2 4 5 6 7
```

the longest King subsequence has length (2). Any two elements can define a ratio, but no ratio supports three elements in the required order. Since (2\cdot2=4<5), the output is `-1`.

At the maximum input size, consider (200000) copies of (7). The ratio (q=1) works throughout the array, so the answer is (200000). The algorithm does not need to store any dynamic-programming table indexed by values or ratios. It only keeps the array and repeatedly scans it, so memory remains (O(n)).

The modular inverse boundary is also safe when (q=1). Fermat's formula gives (1^{p-2}\equiv1), so the backward and forward scans correctly continue through equal values. Every input value is nonzero modulo (p), so no inverse of zero is ever requested.
