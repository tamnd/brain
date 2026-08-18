---
title: "CF 102268C - Cool Pairs"
description: "We need to construct two integer arrays a and b whose values are ordered according to two different permutations. The permutation p dictates the nondecreasing order of the values in a, while q dictates the nondecreasing order of the values in b."
date: "2026-08-19T04:01:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102268
codeforces_index: "C"
codeforces_contest_name: "300iq Contest 1"
rating: 0
weight: 102268
solve_time_s: 463
verified: false
draft: false
---

[CF 102268C - Cool Pairs](https://codeforces.com/problemset/problem/102268/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct two integer arrays `a` and `b` whose values are ordered according to two different permutations. The permutation `p` dictates the nondecreasing order of the values in `a`, while `q` dictates the nondecreasing order of the values in `b`.

For indices `i < j`, the pair is cool when `a[i] + b[j] < 0`. The task is to make exactly `k` such pairs. The values must stay between `-n` and `n`.

The constraints are large, with `n` up to `300000`, so checking all `O(n^2)` pairs is impossible. At the maximum size there are about `4.5 * 10^10` possible pairs, far beyond what a two second limit can handle. We need a construction whose running time is at most roughly `O(n log n)`, and ideally close to linear.

There is no impossible value of `k`. Every integer from `0` through `n(n-1)/2` can be realized by the construction below, so the answer is always `Yes`. The original problem uses exactly these bounds and ordering conditions.

The first edge case is `n = 1`. The only possible value is `k = 0`, because there is no pair with `i < j`. For example,

```
1 0
1
1
```

must produce `Yes`, not `No`. A solution that assumes at least one pair exists can accidentally fail here.

The second edge case is `k = 0`. For example,

```
3 0
1 2 3
1 2 3
```

needs every pair to be non-cool. It is not enough to construct a solution for positive `k` and then leave an uninitialized boundary value. The construction deliberately stops creating cool pairs after the target has reached zero.

The third edge case is the maximum possible value,

```
3 3
1 2 3
1 2 3
```

where every one of the three pairs must be cool. The construction handles this by making all relevant `b` values equal to zero and all `a` values negative. A careless implementation that uses `<= 0` instead of the required strict inequality can also make an incorrect boundary decision.

The fourth edge case is when the target falls strictly inside the contribution of one position. For example,

```
4 5
1 2 3 4
4 3 2 1
```

has to stop partway through one `q` position. Simply assigning each `b` either `0` or `n` can only produce certain totals. The partial assignment is what gives us the missing values.

## Approaches

The direct approach would be to try to assign values to `a` and `b`, then count every pair `(i,j)` with `i < j` and `a[i] + b[j] < 0`. Even if the arrays were already constructed, checking the answer this way takes `O(n^2)` operations. For `n = 300000`, that is about `4.5 * 10^10` pair checks, so it cannot be part of an accepted algorithm.

The useful observation is that we do not need to search over arbitrary arrays. We can deliberately make the values of `a` all distinct and negative. Put

`a[p_t] = t - 1 - n`.

Thus, along `p`, the values are exactly `-n, -n+1, ..., -1`, so the required ordering is automatic.

Now consider one fixed index `j` and suppose `b[j] = 0`. Since every `a[i]` is negative, every index `i < j` forms a cool pair with `j`. Its contribution is exactly `j - 1`.

At the other extreme, if `b[j] = n`, then `a[i] + b[j] >= 0` for every `i`, because `a[i] >= -n`. Its contribution is zero.

This gives us a convenient way to consume the target `k`. We process the positions in the order given by `q`. For a current position `x = q_t`, assigning `b[x] = 0` contributes exactly `x - 1`. If the remaining target is at least `x - 1`, we take all of those pairs.

Eventually there is a first position where the remaining target `r` is smaller than `x - 1`. At that point we need exactly `r` of the `x - 1` possible pairs involving `x`. Since the values `a[1], ..., a[x-1]` are distinct, sort them. If `c` is that sorted list, setting

`b[x] = -c[r]`

with zero-based indexing makes exactly `r` of those values satisfy `a[i] + b[x] < 0`.

After that position, every remaining `b` can be `n`, contributing zero.

The assignments also preserve the required order of `b`. Before the partial position, values are `0`. At the partial position, `b[x]` is between `1` and `n`. Afterwards values are `n`. Hence along `q` the sequence is nondecreasing.

This construction is the same central idea used in published solutions for the problem: make one array strictly ordered and use a single partially assigned position of the other array to realize the final remainder.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Create `a` according to `p` by setting `a[p[t]] = t - n - 1` for one-based `t`. The resulting values are `-n, -n+1, ..., -1`, so `a` is strictly increasing along `p` and every value is within the allowed range.
2. Initially set every `b[i] = n`. Such a value creates no cool pair because `a[i] + n >= 0`.
3. Process the elements of `q` from left to right. Let the current element be `x = q[t]`. If we set `b[x] = 0`, then every index `i < x` is cool with `x`, giving exactly `x - 1` new pairs.
4. If the remaining target `k` is at least `x - 1`, set `b[x] = 0` and subtract `x - 1` from `k`. This completely uses the contribution available at this position.
5. Otherwise, the remaining target satisfies `0 <= k < x - 1`. Consider the values `a[1], ..., a[x-1]` and sort them increasingly as `c`. Set `b[x] = -c[k]`, using zero-based indexing. Exactly the first `k` values of `c` are strictly smaller than `c[k]`, so exactly `k` indices `i < x` satisfy `a[i] + b[x] < 0`.
6. Leave every later `b[q[t]]` equal to `n`. They contribute nothing, so the total number of cool pairs stays unchanged.
7. Output `Yes`, followed by `a` and `b`. The target must have reached zero by this point because the total capacity of all positions is `1 + 2 + ... + (n-1) = n(n-1)/2`, which is the maximum allowed `k`.

### Why it works

The invariant is that after processing some prefix of `q`, the already assigned positions contribute exactly the amount of the original target that has been consumed, while all unprocessed positions contribute zero. When a whole contribution `x-1` fits, assigning zero to `b[x]` consumes exactly that many pairs. When it does not fit, the distinct values of `a[1..x-1]` let us choose exactly any number from `0` through `x-2` by selecting an appropriate threshold. Since all later values of `b` are `n`, no later pair can become cool. Thus the final number of cool pairs is exactly the requested `k`.

The ordering constraints follow from construction as well. The values of `a` increase strictly along `p`. The values of `b` along `q` have the form zeroes, possibly one value in `[1,n]`, then `n`s, so they are nondecreasing. Every assigned value lies in `[-n,n]`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    p = list(map(int, input().split()))
    q = list(map(int, input().split()))

    a = [0] * (n + 1)
    b = [n] * (n + 1)

    # Along p, a contains -n, -n+1, ..., -1.
    for pos, x in enumerate(p):
        a[x] = pos - n

    remaining = k

    for x in q:
        full = x - 1

        if full <= remaining:
            # b[x] = 0 makes every i < x cool.
            b[x] = 0
            remaining -= full
        else:
            # Need exactly 'remaining' cool pairs ending at x.
            # a[1..x-1] are all distinct.
            values = sorted(a[1:x])

            # values[remaining] is the (remaining + 1)-st
            # smallest value. Exactly 'remaining' values are smaller.
            b[x] = -values[remaining]

            remaining = 0
            break

    print("Yes")
    print(*a[1:])
    print(*b[1:])

if __name__ == "__main__":
    solve()
```

The first loop establishes the fixed structure of `a`. With zero-based `pos`, the assignment `pos - n` produces `-n` for the first element of `p` and `-1` for the last one.

The second loop implements the greedy process. The variable `remaining` is the number of cool pairs still required. When `x - 1 <= remaining`, setting `b[x]` to zero is safe because it uses all pairs ending at `x`.

The partial case is the only place where sorting is needed. The slice `a[1:x]` contains exactly the values belonging to indices smaller than `x`. Because all values of `a` are distinct, `values[remaining]` has exactly `remaining` smaller elements. Negating it gives the correct threshold for the strict inequality.

The expression `values[remaining]` rather than `values[remaining - 1]` is a common off-by-one point. If `remaining = 0`, we need no value of `a[1:x]` to satisfy the inequality, so we choose the smallest value and make the inequality strict enough to select zero elements.

The assignment `b[x] = -values[remaining]` is always inside the allowed range because every `a` value lies in `[-n,-1]`, so its negation lies in `[1,n]`.

Python integers have arbitrary precision, so the potentially large value `n(n-1)/2` does not overflow. The input is read with `sys.stdin.readline` as required for the large `n`.

## Worked Examples

### Sample 1

The official sample is

```
5 3
3 5 1 2 4
1 2 3 4 5
```

The construction first creates `a` from `p`.

| `t` | `p[t]` | `a[p[t]]` | Remaining `k` |
| --- | --- | --- | --- |
| 1 | 3 | -5 | 3 |
| 2 | 5 | -4 | 3 |
| 3 | 1 | -3 | 3 |
| 4 | 2 | -2 | 3 |
| 5 | 4 | -1 | 3 |

Thus `a = [-3,-2,-5,-1,-4]`.

We then process `q`.

| Current `x` | `x-1` | Remaining before | Action | Remaining after |
| --- | --- | --- | --- | --- |
| 1 | 0 | 3 | `b[1]=0` | 3 |
| 2 | 1 | 3 | `b[2]=0` | 2 |
| 3 | 2 | 2 | `b[3]=0` | 0 |
| 4 | 3 | 0 | partial assignment | 0 |

For `x=4`, the values before index `4` are `[-3,-2,-5]`. Sorted, they are `[-5,-3,-2]`. Since the remaining target is zero, we select `-5` and assign `b[4]=5`. The remaining position also stays at `5`.

One valid output produced by the algorithm is

```
Yes
-3 -2 -5 -1 -4
0 0 0 5 5
```

There are exactly three cool pairs: `(1,2)`, `(1,3)`, and `(2,3)`. The official sample uses a different valid construction, which is expected because the task asks for any valid arrays.

### Constructed Sample 2

Consider

```
4 5
1 2 3 4
4 3 2 1
```

Here `a = [-4,-3,-2,-1]`.

| Current `x` | `x-1` | Remaining before | Action | Remaining after |
| --- | --- | --- | --- | --- |
| 4 | 3 | 5 | `b[4]=0` | 2 |
| 3 | 2 | 2 | `b[3]=0` | 0 |
| 2 | 1 | 0 | partial assignment | 0 |

At `x=2`, the only earlier value is `a[1]=-4`. The smallest value is `-4`, so `b[2]=4`. This creates zero cool pairs at index `2`.

The final array is

```
a = [-4,-3,-2,-1]
b = [4,4,0,0]
```

The two pairs ending at index `3` are cool, and the three pairs ending at index `4` are cool, giving `2 + 3 = 5`. This example exercises the case where the target is reached exactly at one of the full contributions and then a zero-contribution partial position is used to preserve the ordering of `b`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | The construction is linear except for one sort of at most `n-1` values. |
| Space | `O(n)` | The permutations and the two constructed arrays require linear memory, and the temporary sorted prefix also uses linear memory. |

The algorithm performs only one potentially expensive sort, so `O(n log n)` is easily suitable for `n = 300000`. The memory usage is also linear and fits comfortably within the stated 256 MiB limit.

## Test Cases

The output is not unique, so the tests should verify the mathematical properties rather than compare the generated arrays with one particular answer.

```python
import io
import sys

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    k = next(it)

    p = [next(it) for _ in range(n)]
    q = [next(it) for _ in range(n)]

    a = [0] * (n + 1)
    b = [n] * (n + 1)

    for pos, x in enumerate(p):
        a[x] = pos - n

    remaining = k

    for x in q:
        full = x - 1

        if full <= remaining:
            b[x] = 0
            remaining -= full
        else:
            values = sorted(a[1:x])
            b[x] = -values[remaining]
            remaining = 0
            break

    return "Yes\n" + " ".join(map(str, a[1:])) + "\n" + \
           " ".join(map(str, b[1:])) + "\n"

def run(inp: str) -> str:
    return solve_data(inp)

def verify(inp: str, out: str):
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    k = next(it)
    p = [next(it) for _ in range(n)]
    q = [next(it) for _ in range(n)]

    lines = out.strip().splitlines()
    assert lines[0] == "Yes"

    a = list(map(int, lines[1].split()))
    b = list(map(int, lines[2].split()))

    assert len(a) == n
    assert len(b) == n

    assert all(-n <= x <= n for x in a)
    assert all(-n <= x <= n for x in b)

    for i in range(n - 1):
        assert a[p[i] - 1] <= a[p[i + 1] - 1]
        assert b[q[i] - 1] <= b[q[i + 1] - 1]

    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + b[j] < 0:
                count += 1

    assert count == k

# Provided sample
sample1 = """\
5 3
3 5 1 2 4
1 2 3 4 5
"""
out = run(sample1)
verify(sample1, out)

# Custom case: minimum n
case2 = """\
1 0
1
1
"""
out = run(case2)
verify(case2, out)

# Custom case: k = 0
case3 = """\
4 0
2 4 1 3
3 1 4 2
"""
out = run(case3)
verify(case3, out)

# Custom case: maximum k, producing all-zero b
case4 = """\
4 6
4 1 3 2
2 4 1 3
"""
out = run(case4)
verify(case4, out)

# Custom case: partial contribution, catches off-by-one errors
case5 = """\
4 5
1 2 3 4
4 3 2 1
"""
out = run(case5)
verify(case5, out)

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 3 / 3 5 1 2 4 / 1 2 3 4 5` | Any valid `Yes` construction | Official sample and ordinary partial-boundary behavior |
| `1 0 / 1 / 1` | `Yes` with `a=-1`, `b=0` | Minimum size and absence of pairs |
| `4 0 / 2 4 1 3 / 3 1 4 2` | Any valid `Yes` construction | Zero target |
| `4 6 / 4 1 3 2 / 2 4 1 3` | Any valid `Yes` construction | Maximum target and all pairs being cool |
| `4 5 / 1 2 3 4 / 4 3 2 1` | Any valid `Yes` construction | Partial contribution and strict inequality boundary |

The verifier deliberately checks every pair only in the test harness. That is fine because the test cases are tiny, while the submitted solution never performs this quadratic verification.

## Edge Cases

For `n=1`, the input

```
1 0
1
1
```

creates `a[1] = -1`. The current `q` position is `1`, whose full contribution is `0`, so `b[1]` becomes zero and the remaining target stays zero. There are no pairs at all, so the output is valid.

For `k=0`, consider

```
3 0
1 2 3
1 2 3
```

The first position has `x=1`, so its full contribution is zero. At `x=2`, the required target is already zero and `x-1=1`, so the algorithm enters the partial case. The only earlier value is `a[1]=-3`, and it assigns `b[2]=3`. Since `a[1]+3=0`, the strict inequality fails, giving zero cool pairs. The remaining `b` values are `3`, also producing zero pairs. The construction handles the strict boundary exactly.

For the maximum target,

```
3 3
1 2 3
1 2 3
```

the values of `a` are `[-3,-2,-1]`. The positions in `q` contribute `0`, `1`, and `2`, respectively, and all three are taken completely by assigning `b` equal to zero. Every pair has a negative `a` value plus zero, so all three pairs are cool.

For a partial contribution, consider

```
4 5
1 2 3 4
4 3 2 1
```

The first `q` value is `4`, contributing three pairs and leaving `2`. The next is `3`, contributing two more and leaving zero. The next position cannot contribute anything because the target is already zero, so the partial construction selects the smallest preceding `a` value as its threshold. This gives zero additional pairs, and the remaining positions receive `n`. The final count is exactly `5`.

The reason the construction never needs to print `No` is that every target in the allowed interval can be decomposed greedily into full contributions `q_t-1` plus one final remainder. The sum of all these capacities is

`(q_1-1) + (q_2-1) + ... + (q_n-1) = n(n-1)/2`.

The final partial position can realize every remainder below its capacity because the preceding `a` values are distinct. That combination covers the entire required range of `k`.
