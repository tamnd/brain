---
title: "CF 102254D - Donimo's"
description: "We have 2n pizza slices, where slice i has size a[i]. We must divide all slices among n people, giving exactly two slices to each person. A person's amount is the sum of the two slices they receive."
date: "2026-08-17T21:07:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102254
codeforces_index: "D"
codeforces_contest_name: "IME++ Starters Try-outs 2019"
rating: 0
weight: 102254
solve_time_s: 261
verified: false
draft: false
---

[CF 102254D - Donimo's](https://codeforces.com/problemset/problem/102254/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We have `2n` pizza slices, where slice `i` has size `a[i]`. We must divide all slices among `n` people, giving exactly two slices to each person. A person's amount is the sum of the two slices they receive.

The goal is not to make every person's amount individually as large or small as possible. We want the entire set of `n` pair sums to be as tightly clustered as possible. If the smallest pair sum is `L` and the largest is `R`, the quality of a division is `R - L`. We need the minimum possible value of this difference.

The constraints give at most `2 * 10^4` slice sizes, each as large as `10^9`. An approach that examines pairings explicitly is completely infeasible because the number of ways to partition `2n` objects into pairs grows factorially. Sorting the slices is easily affordable, taking `O(n log n)`, so the intended solution needs to exploit the ordering of the slice sizes rather than enumerate pairings.

There are several edge cases that can make a careless implementation fail. With `n = 2` and slices `1 4 3 2`, sorting gives `1 2 3 4`. Pairing adjacent elements produces sums `3` and `7`, but the optimal pairing is `1+4` and `2+3`, giving answer `0`. This catches solutions that assume sorted adjacent elements should be paired.

Duplicate values also matter. For `n = 2` and slices `1 1 1 2`, the optimal pairing is `1+2` and `1+1`, so the answer is `1`. A proof or implementation that relies on all slice sizes being distinct is unnecessary and can accidentally mishandle equal boundaries.

The largest slice values also require integer arithmetic without narrowing. For example, `n = 2` and slices `1000000000 1000000000 1 1` produce pair sums `1000000001` and `1000000001`, so the answer is `0`. The sums themselves can reach `2 * 10^9`, which is safe in Python's integers and also requires at least a signed 32-bit range in languages with fixed-width integers.

## Approaches

A direct brute-force solution would enumerate every possible way to partition the `2n` slices into `n` unordered pairs. For every pairing, we could calculate all `n` pair sums and take the difference between the largest and smallest. This is correct because every valid division is considered.

The number of pairings of `2n` distinct positions is

(2n−1)!!= 2 n n! (2n)! ​ .

Each pairing requires `n` pair-sum computations, so the total work is `O(n(2n-1)!!)`. For `n = 10000`, this is far beyond anything executable within one second. Even the number of pairings becomes enormous long before reaching the constraint limit.

The useful observation comes from sorting the slices:

a 1 ​ ≤a 2 ​ ≤⋯≤a 2n ​ .

Consider the particular division that pairs the smallest slice with the largest, the second smallest with the second largest, and so on. Its pair sums are

a 1 ​ +a 2n ​ ,a 2 ​ +a 2n−1 ​ ,…,a n ​ +a n+1 ​ .

Why should this be optimal? The key property is stronger than simply saying that this pairing "balances" the values. For any possible pairing, every one of these complementary sums lies between that pairing's smallest pair sum and largest pair sum.

Suppose some complementary sum `a_k + a_{2n+1-k}` were larger than the largest sum `M` of another pairing. Look at the `k` largest slices. Every one of them has value at least `a_{2n+1-k}`. Since its pair sum is at most `M`, its partner must be strictly smaller than `a_k`. But there are only `k-1` slices strictly smaller than `a_k`, while the `k` largest slices need `k` distinct partners. That is impossible.

The same argument works from the other side. If `a_k + a_{2n+1-k}` were smaller than the smallest sum `m` of another pairing, then each of the `k` smallest slices would need a partner strictly larger than `a_{2n+1-k}`. Only `k-1` slices can be strictly larger than that boundary value, which is again impossible.

Thus all complementary sums lie inside the range of every valid pairing. The complementary pairing consequently has the smallest possible range.

The brute-force works because it explicitly considers every possible pairing, but fails because there are factorially many of them. The ordering observation lets us replace the entire matching problem with one sort and one scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n(2n-1)!!)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read the `2n` slice sizes and sort them in nondecreasing order. Sorting gives us direct access to the smallest and largest remaining slices, which is exactly the structure used by the optimal pairing.
2. Pair `a[i]` with `a[2n - 1 - i]` for every `i` from `0` through `n - 1`. These are the two elements symmetrically positioned around the center of the sorted array.
3. For each pair, calculate its sum. Track the smallest pair sum and the largest pair sum seen so far. There is no need to store the pair sums because only their minimum and maximum affect the answer.
4. Output `maximum_pair_sum - minimum_pair_sum`. The proof above shows that the range produced by these symmetric pairs cannot be larger than the range of any other division, so it is the required minimum.

Why it works can be stated as an invariant. After sorting, define

c k ​ =a k ​ +a 2n+1−k ​ .

For any arbitrary valid pairing whose pair sums lie in `[L,R]`, every `c_k` also lies in `[L,R]`. If some `c_k > R`, the `k` largest slices would require `k` distinct partners smaller than `a_k`, but only `k-1` such slices exist. If some `c_k < L`, the `k` smallest slices would require `k` distinct partners larger than `a_{2n+1-k}`, but only `k-1` such slices exist. Hence the symmetric pairing's minimum and maximum sums are both contained in every possible pairing's range. Its range is consequently no larger than any competitor's range.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    n = int(input())    a = list(map(int, input().split()))
    a.sort()
    mn = 10**30    mx = -10**30
    for i in range(n):        pair_sum = a[i] + a[2 * n - 1 - i]        mn = min(mn, pair_sum)        mx = max(mx, pair_sum)
    print(mx - mn)

if __name__ == "__main__":    solve()
```

The input contains exactly `2n` integers, so the whole array can be read with one call to `input()`. The array is sorted because the optimal pairing depends only on the relative order of the slice sizes.

The loop runs only `n` times. At iteration `i`, `a[i]` is the `i`-th smallest slice and `a[2*n-1-i]` is the corresponding `i`-th largest slice. The index `2*n-1-i` is the zero-based equivalent of the mathematical index `2n+1-(i+1)`.

The variables `mn` and `mx` are updated after every pair. Initializing them with values far outside the possible pair-sum range avoids special handling for the first iteration. Python integers have arbitrary precision, so there is no overflow risk even though a pair sum can reach `2 * 10^9`.

There is only one test case in the problem, so no test-case loop is needed.

## Worked Examples

For Sample 1, the input is:

```
21 4 3 2
```

After sorting, the slices are `[1, 2, 3, 4]`.

| `i` | Small slice | Large slice | Pair sum | `mn` | `mx` |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 5 | 5 | 5 |
| 1 | 2 | 3 | 5 | 5 | 5 |

The two people both receive pizza of size `5`, so the difference is `5 - 5 = 0`. This demonstrates why pairing extremes is better than pairing adjacent sorted elements.

For Sample 2, the input is:

```
45 1 1 4 3 2 11 3
```

Sorting gives `[1, 1, 2, 3, 3, 4, 5, 11]`.

| `i` | Small slice | Large slice | Pair sum | `mn` | `mx` |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 11 | 12 | 12 | 12 |
| 1 | 1 | 5 | 6 | 6 | 12 |
| 2 | 2 | 4 | 6 | 6 | 12 |
| 3 | 3 | 3 | 6 | 6 | 12 |

The resulting pair sums are `12, 6, 6, 6`, so the answer is `12 - 6 = 6`. The large slice necessarily creates the largest amount, while pairing the remaining extremes keeps the other three amounts equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting `2n` values dominates the `O(n)` pairing scan |
| Space | `O(n)` | The array contains `2n` slice sizes |

With `n <= 10^4`, sorting at most `20000` integers is comfortably within the one-second time limit. The memory usage is also tiny compared with the `256 MB` limit.

## Test Cases

```python
Pythonimport sysimport io

def solve():    n = int(input())    a = list(map(int, input().split()))
    a.sort()
    mn = 10**30    mx = -10**30
    for i in range(n):        pair_sum = a[i] + a[2 * n - 1 - i]        mn = min(mn, pair_sum)        mx = max(mx, pair_sum)
    print(mx - mn)

def run(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()
    try:        solve()        return sys.stdout.getvalue().strip()    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout

# Provided samplesassert run("2\n1 4 3 2\n") == "0", "sample 1"assert run("4\n5 1 1 4 3 2 11 3\n") == "6", "sample 2"
# Minimum-size inputassert run("2\n1 2 3 4\n") == "0", "minimum n with perfectly balanced pairs"
# All values equalassert run("5\n7 7 7 7 7 7 7 7 7 7\n") == "0", "all pair sums are equal"
# Boundary values near 1e9assert run("2\n1 1 1000000000 1000000000\n") == "0", "large integer values"
# Case where adjacent pairing is not optimalassert run("2\n1 2 3 10\n") == "4", "extreme pairing gives 11 and 5"
# Maximum-size input, generated rather than written literallymax_input = "10000\n" + " ".join(["1000000000"] * 20000) + "\n"assert run(max_input) == "0", "maximum n and all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2 3 4` | `0` | Minimum allowed `n` and perfectly balanced extreme pairs |
| `5 / 7 7 7 7 7 7 7 7 7 7` | `0` | Duplicate values and identical pair sums |
| `2 / 1 1 1000000000 1000000000` | `0` | Maximum slice values and large pair sums |
| `2 / 1 2 3 10` | `4` | Correct extreme pairing instead of adjacent pairing |
| `n = 10000`, all `10^9` | `0` | Maximum input size and performance |

## Edge Cases

For the first edge case, consider

```
21 4 3 2
```

Sorting gives `[1, 2, 3, 4]`. The algorithm pairs `1` with `4` and `2` with `3`, producing sums `5` and `5`. Thus `mn = 5`, `mx = 5`, and the output is `0`. An adjacent-pair strategy would instead obtain `3` and `7`, giving the wrong answer `4`.

For duplicate values, consider

```
21 1 1 2
```

The sorted array is already `[1, 1, 1, 2]`. The symmetric pairs have sums `3` and `2`, so the algorithm outputs `1`. Equal values cause no special indexing problem because the proof uses positions, not distinct slice values.

For large values, consider

```
21 1 1000000000 1000000000
```

The symmetric pair sums are both `1000000001`. The tracked minimum and maximum are identical, so the result is `0`. The implementation performs all arithmetic directly as integers and does not use floating point.

For the maximum input size, take `n = 10000` and make all `20000` slice sizes equal to `1000000000`. Every symmetric pair has sum `2000000000`, so the answer is `0`. The algorithm only sorts the array and performs `10000` pair checks afterward, so it remains comfortably within the required complexity.
