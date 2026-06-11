---
title: "CF 1234E - Special Permutations"
description: "We are given a sequence x of length m. For every value i from 1 to n, we construct a special permutation: pi = [i, 1, 2, ..., i-1, i+1, ..., n] This permutation differs from the identity permutation only because the value i has been moved to the front."
date: "2026-06-11T22:20:19+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1234
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 590 (Div. 3)"
rating: 2000
weight: 1234
solve_time_s: 106
verified: true
draft: false
---

[CF 1234E - Special Permutations](https://codeforces.com/problemset/problem/1234/E)

**Rating:** 2000  
**Tags:** math  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence `x` of length `m`. For every value `i` from `1` to `n`, we construct a special permutation:

`p_i = [i, 1, 2, ..., i-1, i+1, ..., n]`

This permutation differs from the identity permutation only because the value `i` has been moved to the front.

For each permutation, we must compute the total distance between consecutive elements of `x` when those elements are viewed inside that permutation. If two neighboring values in `x` occupy positions `a` and `b` in the permutation, they contribute `|a-b|` to the answer.

The task is to output this value for every permutation `p_1, p_2, ..., p_n`.

The constraints are the first thing that drives the solution. Both `n` and `m` can reach `2·10^5`. There are `n` different permutations and each answer depends on `m-1` adjacent pairs from `x`. A direct computation would require roughly `n·m`, which becomes about `4·10^10` operations in the worst case. That is completely impossible within two seconds.

The structure of the permutations is extremely special. Every permutation is obtained from the identity by moving exactly one value to the first position. That means most positions remain unchanged, and only a small subset of distances are affected when we move from one permutation index to another.

Several edge cases are easy to mishandle.

Consider:

```
3 3
2 2 2
```

Every adjacent pair is `(2,2)`, whose distance is always zero regardless of the permutation. The correct output is:

```
0 0 0
```

A solution that assumes adjacent values are distinct may incorrectly introduce updates.

Consider:

```
4 2
1 4
```

The answer for `p_1` is `|1-4|=3`. For `p_4`, positions become `(2,1)`, giving distance `1`. The distance changes dramatically when one endpoint equals the moved element.

Consider:

```
5 2
2 3
```

The pair never contains many values, yet every answer still depends on where the moved element lies relative to the interval `[2,3]`. Any approach that only updates endpoints and ignores interval effects will produce wrong answers.

The central challenge is understanding how a single adjacent pair contributes to all permutations simultaneously.

## Approaches

The brute force solution is straightforward. For every permutation `p_i`, compute the position of every value, then iterate through the `m-1` adjacent pairs of `x` and sum the corresponding distances.

The position function in permutation `p_k` is:

- `pos(k)=1`
- `pos(v)=v+1` for `v<k`
- `pos(v)=v` for `v>k`

Using this formula, each distance can be evaluated in constant time. Unfortunately we still have `n` permutations and `m-1` pairs, leading to `O(nm)` work. With both parameters equal to `2·10^5`, the operation count is around forty billion.

The key observation is that the total answer is a sum over adjacent pairs of `x`.

Instead of fixing a permutation and evaluating every pair, we reverse the viewpoint. Take one adjacent pair `(a,b)` and determine how its contribution changes across all permutations.

Let

```
g_k(a,b) = |pos_k(a)-pos_k(b)|
```

where `k` is the value moved to the front.

For most values of `k`, the distance is unchanged from the identity permutation. Only when `k` is equal to one endpoint or lies between the two endpoints does the distance change.

This means a single pair affects only an interval of permutation indices. Since there are only `m-1` pairs, we can process each pair independently and accumulate its effect into a difference array.

The identity permutation answer is easy to compute:

```
base = Σ |x_i - x_{i+1}|
```

Then for each adjacent pair we compute how much its contribution differs from the base answer for all relevant permutations. These changes can be added using range updates.

The entire problem becomes an interval-addition problem on the permutation index `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Deriving the Contribution Formula

Assume `a < b`.

In the identity permutation the contribution is

```
b-a
```

Now consider moving value `k` to the front.

If `k=a`, then

```
pos(a)=1
pos(b)=b
```

Contribution becomes

```
b-1
```

Difference from the base:

```
(b-1)-(b-a)=a-1
```

If `k=b`, then

```
pos(a)=a+1
pos(b)=1
```

Contribution becomes

```
a
```

Difference:

```
a-(b-a)=2a-b
```

If `a<k<b`, then

```
pos(a)=a+1
pos(b)=b
```

Contribution becomes

```
b-a-1
```

Difference:

```
-1
```

For all other `k`, the contribution remains unchanged.

Thus one pair contributes:

```
a-1          at k=a
-1           for a<k<b
2a-b         at k=b
0            elsewhere
```

This compact description is the whole solution.

## Algorithm Walkthrough

1. Compute the answer for the identity permutation.

Let

```
ans = Σ |x_i - x_{i+1}|
```

Every permutation answer will start from this value and then receive corrections.
2. Create a difference array of size `n+3`.

We will store all changes relative to the identity answer.
3. Process every adjacent pair `(u,v)` in `x`.

If `u=v`, the contribution is always zero and no updates are needed.
4. Let `a=min(u,v)` and `b=max(u,v)`.

The derived formula depends only on the ordered endpoints.
5. Add the point update for `k=a`.

The correction is `a-1`.
6. Add the point update for `k=b`.

The correction is `2*a-b`.
7. Add the range update on `(a,b)`.

Every permutation index strictly between `a` and `b` receives `-1`.

This is the interval where the moved value lies between the two endpoints, reducing their distance by one.
8. After all pairs are processed, convert the difference array into actual corrections using a prefix sum.
9. For every `k` from `1` to `n`, output

```
base + correction[k]
```

### Why it works

For every adjacent pair of values, we explicitly compute the exact change of its distance compared with the identity permutation. The derivation above exhausts all possible positions of the moved value `k`.

A pair contributes only in three situations: when `k` equals the left endpoint, when `k` equals the right endpoint, or when `k` lies strictly between them. The update rules encode precisely these cases.

Because the total answer is the sum of contributions from all adjacent pairs, linearity allows us to add all pair corrections independently. After all updates are accumulated, the correction stored for permutation `k` equals the sum of the contribution changes of every pair, which is exactly the difference between `f(p_k)` and the identity answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def add_range(diff, l, r, val):
    if l > r:
        return
    diff[l] += val
    diff[r + 1] -= val

def solve():
    n, m = map(int, input().split())
    x = list(map(int, input().split()))

    base = 0
    diff = [0] * (n + 3)

    for i in range(m - 1):
        u = x[i]
        v = x[i + 1]

        if u == v:
            continue

        a = min(u, v)
        b = max(u, v)

        base += b - a

        diff[a] += a - 1
        diff[a + 1] -= a - 1

        if a + 1 <= b - 1:
            add_range(diff, a + 1, b - 1, -1)

        diff[b] += 2 * a - b
        diff[b + 1] -= (2 * a - b)

    cur = 0
    res = []

    for k in range(1, n + 1):
        cur += diff[k]
        res.append(str(base + cur))

    print(" ".join(res))

solve()
```

The solution starts by computing the identity-permutation answer. This serves as a baseline from which all other answers are derived.

For each adjacent pair, we apply the three correction rules derived earlier. Point updates are implemented as length-one range updates inside the difference array. The interval `(a,b)` receives a range update of `-1`.

The difference array is crucial. Without it, updating every index between `a` and `b` would make the algorithm quadratic. A difference array turns each interval modification into constant work.

One subtle detail is the update at `k=b`. Its value is `2a-b`, not `a-b` or `a-1`. This comes directly from the exact distance when `b` itself is moved to the front.

Another easy mistake is handling equal consecutive values. When `u=v`, the distance is always zero. The derived formulas assume distinct endpoints and should be skipped entirely.

All arithmetic comfortably fits inside 64-bit integers. The maximum answer is on the order of `m·n`, approximately `4·10^10`.

## Worked Examples

### Sample 1

Input:

```
4 4
1 2 3 4
```

Adjacent pairs are `(1,2)`, `(2,3)`, `(3,4)`.

Base answer:

```
1 + 1 + 1 = 3
```

| Pair | a | b | Update at a | Range | Update at b |
| --- | --- | --- | --- | --- | --- |
| (1,2) | 1 | 2 | 0 | none | 0 |
| (2,3) | 2 | 3 | +1 | none | +1 |
| (3,4) | 3 | 4 | +2 | none | +2 |

Accumulated corrections:

| k | Correction |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 3 |
| 4 | 2 |

Final answers:

| k | Base | Correction | Answer |
| --- | --- | --- | --- |
| 1 | 3 | 0 | 3 |
| 2 | 3 | 1 | 4 |
| 3 | 3 | 3 | 6 |
| 4 | 3 | 2 | 5 |

Output:

```
3 4 6 5
```

This example shows that even though the identity answer is only `3`, moving larger values to the front increases several pair distances simultaneously.

### Sample 2

Input:

```
5 5
2 1 5 3 5
```

Base answer:

```
1 + 4 + 2 + 2 = 9
```

Pair contributions:

| Pair | a | b | Effect |
| --- | --- | --- | --- |
| (2,1) | 1 | 2 | updates near 1 and 2 |
| (1,5) | 1 | 5 | interval [2,4] gets -1 |
| (5,3) | 3 | 5 | interval [4,4] gets -1 |
| (3,5) | 3 | 5 | interval [4,4] gets -1 |

After accumulating all updates:

| k | Correction | Answer |
| --- | --- | --- |
| 1 | 0 | 9 |
| 2 | -1 | 8 |
| 3 | 3 | 12 |
| 4 | -3 | 6 |
| 5 | -1 | 8 |

Output:

```
9 8 12 6 8
```

This trace demonstrates the importance of interval updates. Most changes come not from endpoints but from values lying between the pair endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One pass over adjacent pairs and one prefix-sum pass |
| Space | O(n) | Difference array and output array |

The constraints allow up to `2·10^5` values. An `O(n+m)` algorithm performs only a few hundred thousand operations and easily fits within the time limit. The memory usage is linear in `n`, far below the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    x = list(map(int, input().split()))

    base = 0
    diff = [0] * (n + 3)

    for i in range(m - 1):
        u = x[i]
        v = x[i + 1]

        if u == v:
            continue

        a = min(u, v)
        b = max(u, v)

        base += b - a

        diff[a] += a - 1
        diff[a + 1] -= a - 1

        if a + 1 <= b - 1:
            diff[a + 1] -= 1
            diff[b] += 1

        val = 2 * a - b
        diff[b] += val
        diff[b + 1] -= val

    cur = 0
    ans = []

    for i in range(1, n + 1):
        cur += diff[i]
        ans.append(str(base + cur))

    return " ".join(ans)

# sample 1
assert run("4 4\n1 2 3 4\n") == "3 4 6 5"

# sample 2
assert run("5 5\n2 1 5 3 5\n") == "9 8 12 6 8"

# minimum sizes
assert run("2 2\n1 1\n") == "0 0"

# all equal values
assert run("5 4\n3 3 3 3\n") == "0 0 0 0 0"

# interval update stress
assert run("5 2\n1 5\n") == "4 3 3 3 1"

# symmetric pair
assert run("3 2\n2 3\n") == "1 2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / 1 1` | `0 0` | Minimum constraints |
| `5 4 / 3 3 3 3` | `0 0 0 0 0` | Repeated values |
| `5 2 / 1 5` | `4 3 3 3 1` | Long interval update |
| `3 2 / 2 3` | `1 2 2` | Endpoint correction formulas |

## Edge Cases

Consider:

```
3 3
2 2 2
```

Every adjacent pair has identical endpoints. The algorithm immediately skips each pair because `u == v`. No updates are applied, the base answer remains zero, and every permutation answer is zero:

```
0 0 0
```

Now consider:

```
5 2
1 5
```

The base answer is `4`. For the pair `(1,5)`, the interval `(1,5)` receives `-1`, so permutations `2,3,4` all lose one unit. At `k=5`, the special endpoint correction contributes `-3`, giving answer `1`. The output becomes:

```
4 3 3 3 1
```

This verifies that the right endpoint update `2a-b` is handled correctly.

Finally consider:

```
5 2
2 3
```

The base answer is `1`.

The updates are:

```
k=2 : +1
k=3 : +1
```

No interval exists between the endpoints. Answers become:

```
1 2 2 1 1
```

This checks the boundary case where `b=a+1`, ensuring the interval update is not accidentally applied to an empty range.
