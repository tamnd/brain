---
title: "CF 105556K - GCD of Set"
description: "We are given a set of distinct positive integers. The set must be partitioned into exactly k non-empty subsets. Each subset contributes the gcd of all numbers inside it, and we want the maximum possible sum of these gcd values."
date: "2026-06-25T06:09:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105556
codeforces_index: "K"
codeforces_contest_name: "The 6th FanRuan Cup Southeast University Programming Contest (Winter)"
rating: 0
weight: 105556
solve_time_s: 95
verified: true
draft: false
---

[CF 105556K - GCD of Set](https://codeforces.com/problemset/problem/105556/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of distinct positive integers. The set must be partitioned into exactly `k` non-empty subsets. Each subset contributes the gcd of all numbers inside it, and we want the maximum possible sum of these gcd values.

The numbers are distinct, each value is at most `10^6`, and across all test cases the sum of the maximum value appearing in each test case is at most `10^6`. That last condition is the real hint. It strongly suggests a solution that works in roughly `O(M log M)` per test case, where `M` is the largest value in the set. A quadratic algorithm in `n` would be hopeless when `n` itself can reach `10^6`.

The tricky part is that the partition is completely unrestricted. A direct search over partitions is impossible, even for very small inputs.

A common mistake is to focus on the gcd values themselves and try to build subsets greedily. The partition structure is actually much simpler than it first appears.

Consider the set `{3, 5, 6}` with `k = 2`.

If we choose subsets `{5}` and `{3, 6}`, the sum is:

`5 + gcd(3, 6) = 5 + 3 = 8`

This is optimal.

A second easy-to-miss case is when some numbers divide others.

For `{5, 9, 10, 11, 13}` with `k = 4`, putting `10` together with `5` is beneficial because the subset gcd becomes `5`. The optimal partition is:

`{13}, {11}, {9}, {5, 10}`

giving

`13 + 11 + 9 + 5 = 38`

A naive strategy of always isolating the largest numbers does not explain why `10` should be merged instead of `5`.

## Approaches

The brute force idea is straightforward. Enumerate all ways to partition the set into `k` non-empty subsets, compute the gcd of every subset, and keep the best answer.

This is correct because it checks every valid partition. The problem is that the number of partitions grows super-exponentially. Even for a few dozen elements it is already impossible.

The key observation comes from asking what happens inside an optimal partition.

Suppose a subset contains at least two elements and its gcd is `g`. Pick any element `x` in that subset that is not the smallest one. Since `g` divides every element in the subset, we have `g ≤ x`.

If we remove `x` from the subset and make it a singleton subset, the contribution changes from

`g`

to

`g + x`.

The total sum increases by at least `x - g ≥ 0`.

This means that, whenever we are allowed to create more subsets, separating elements is never harmful.

Since we must end with exactly `k` subsets, an optimal partition always has:

`k - 1` singleton subsets and one remaining subset containing the other `n - k + 1` elements.

Let

`m = n - k + 1`.

If the remaining subset is `R`, then the answer becomes

`sum(all elements) - sum(R) + gcd(R)`.

The total sum of all numbers is fixed, so we only need to maximize

`gcd(R) - sum(R)`,

where `|R| = m`.

Now fix a possible gcd value `d`.

If `gcd(R) = d`, every element of `R` must be divisible by `d`.

Among all elements divisible by `d`, the best choice is clearly the `m` smallest ones, because the term `-sum(R)` should be as large as possible.

So for every divisor `d`, if at least `m` numbers in the set are divisible by `d`, we compute

`d - (sum of the m smallest present multiples of d)`.

The best such value over all `d` gives the optimal correction term.

The structure of the constraints makes a divisor-sieve solution natural. For each `d`, we scan its multiples in increasing order. Since multiples are visited in increasing numeric order, the first `m` present multiples are exactly the `m` smallest divisible numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(M log M) | O(M) | Accepted |

## Algorithm Walkthrough

1. Read the set and compute the total sum `S` of all elements.
2. Let `m = n - k + 1`.

This is the size of the single non-singleton subset in an optimal partition.
3. Build a presence array for all values up to the maximum value in the set.
4. For every possible divisor `d` from `1` to `max_value`:

Scan all multiples of `d` in increasing order.
5. Whenever a multiple is present in the set, add it to a running sum and increase a counter.

Because multiples are processed in increasing order, the first `m` present multiples are exactly the `m` smallest divisible elements.
6. Once the counter reaches `m`, compute

`candidate = d - current_sum`.

Update the best value.
7. The final answer is

`S + best`.

### Why it works

The crucial property is that every optimal partition can be transformed into one with exactly `k - 1` singleton subsets and one larger subset, without decreasing the answer.

After that transformation, every solution is uniquely described by the set `R` of size `m = n - k + 1`.

Its contribution is

`S - sum(R) + gcd(R)`.

For a fixed gcd value `d`, every element of `R` must be divisible by `d`. To maximize

`d - sum(R)`,

we must minimize `sum(R)`, which means choosing the `m` smallest available numbers divisible by `d`.

Checking every divisor `d` covers every possible gcd. The best value found is exactly the maximum achievable value of

`gcd(R) - sum(R)`.

Hence the algorithm always returns the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        S = sum(a)
        m = n - k + 1
        mx = max(a)

        present = [0] * (mx + 1)
        for x in a:
            present[x] = 1

        best = -10**18

        for d in range(1, mx + 1):
            cnt = 0
            cur_sum = 0

            for multiple in range(d, mx + 1, d):
                if present[multiple]:
                    cnt += 1
                    cur_sum += multiple

                    if cnt == m:
                        value = d - cur_sum
                        if value > best:
                            best = value
                        break

        ans.append(str(S + best))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first part computes the fixed quantity `S`, the sum of all elements.

The value `m = n - k + 1` comes directly from the structural proof that an optimal partition consists of one larger subset and `k - 1` singleton subsets.

The presence array allows constant-time checks for whether a value belongs to the set. Because all values are distinct, a boolean array is sufficient.

For each divisor `d`, we walk through its multiples. The traversal order is increasing, so the first `m` present multiples are automatically the `m` smallest divisible numbers. No sorting is needed.

The moment we reach `m` elements, we already know the optimal subset sum for this divisor, so we can stop scanning larger multiples of `d`.

All arithmetic fits comfortably in Python integers.

## Worked Examples

### Example 1

Input:

```
n = 3
k = 2
set = {3, 5, 6}
```

Here:

`S = 14`

`m = 2`

| d | First 2 present multiples | Sum | d - Sum |
| --- | --- | --- | --- |
| 1 | 3, 5 | 8 | -7 |
| 2 | 6 | not enough | - |
| 3 | 3, 6 | 9 | -6 |
| 4 | none | not enough | - |
| 5 | 5 | not enough | - |
| 6 | 6 | not enough | - |

The best value is `-6`.

Answer:

`14 + (-6) = 8`

This corresponds to choosing `R = {3, 6}`. The partition is `{5}` and `{3, 6}`.

### Example 2

Input:

```
n = 5
k = 4
set = {5, 9, 10, 11, 13}
```

Here:

`S = 48`

`m = 2`

| d | First 2 present multiples | Sum | d - Sum |
| --- | --- | --- | --- |
| 1 | 5, 9 | 14 | -13 |
| 2 | 10 | not enough | - |
| 5 | 5, 10 | 15 | -10 |
| 9 | 9 | not enough | - |

The best value is `-10`.

Answer:

`48 + (-10) = 38`

The chosen set is `R = {5, 10}`. The remaining numbers become singleton subsets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log M) | Harmonic-series divisor sieve over values up to `M` |
| Space | O(M) | Presence array of size `M + 1` |

Here `M` is the maximum value in the current test case.

Because the sum of all test-case maxima is at most `10^6`, the total work across the entire input remains well within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    def solve():
        input = sys.stdin.readline
        t = int(input())

        res = []

        for _ in range(t):
            n, k = map(int, input().split())
            a = list(map(int, input().split()))

            S = sum(a)
            m = n - k + 1
            mx = max(a)

            present = [0] * (mx + 1)
            for x in a:
                present[x] = 1

            best = -10**18

            for d in range(1, mx + 1):
                cnt = 0
                cur = 0

                for x in range(d, mx + 1, d):
                    if present[x]:
                        cnt += 1
                        cur += x

                        if cnt == m:
                            best = max(best, d - cur)
                            break

            res.append(str(S + best))

        print("\n".join(res))

    solve()

    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided samples
assert run(
"""4
3 2
3 6 5
5 4
13 11 10 9 5
4 2
4 2 5 3
4 3
4 2 5 3
"""
) == """8
38
6
10"""

# custom cases
assert run(
"""1
1 1
7
"""
) == "7"

assert run(
"""1
2 1
4 8
"""
) == "4"

assert run(
"""1
2 2
4 8
"""
) == "12"

assert run(
"""1
3 2
2 4 8
"""
) == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7` | `7` | Minimum size |
| `2 1 / 4 8` | `4` | Single subset, gcd of whole set |
| `2 2 / 4 8` | `12` | All singleton subsets |
| `3 2 / 2 4 8` | `10` | Best remaining subset uses divisibility |

## Edge Cases

Consider:

```
1
3 2
3 5 6
```

A tempting approach is to isolate the largest element and assume the rest contributes its minimum element. The remaining subset `{3, 6}` contributes `3`, not its minimum by accident but because its gcd is exactly `3`. The algorithm checks divisor `3`, finds the first two divisible elements `{3, 6}`, and obtains the correct answer `8`.

Now consider:

```
1
5 4
13 11 10 9 5
```

The best solution is not obtained by grouping the two smallest numbers. The optimal remaining subset is `{5, 10}` because its gcd is `5`. When the algorithm processes divisor `5`, it immediately finds exactly two present multiples, giving the value `5 - (5 + 10) = -10`, which is better than every other divisor.

Finally:

```
1
4 2
2 3 4 5
```

The optimal answer is `6`. The algorithm chooses `R = {2, 3, 4}` because among all size-3 subsets it maximizes `gcd(R) - sum(R)`. The resulting partition is `{5}` and `{2, 3, 4}`, giving `5 + 1 = 6`. This confirms that the remaining subset is not required to have a gcd larger than `1`.
