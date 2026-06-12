---
title: "CF 908E - New Year and Entity Enumeration"
description: "We work with binary vectors of length m, which can be viewed as integers from 0 to 2^m - 1. A valid set S must satisfy three structural properties. First, it contains every vector from the given set T. Second, it is closed under XOR."
date: "2026-06-12T23:45:15+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 908
codeforces_index: "E"
codeforces_contest_name: "Good Bye 2017"
rating: 2500
weight: 908
solve_time_s: 549
verified: false
draft: false
---

[CF 908E - New Year and Entity Enumeration](https://codeforces.com/problemset/problem/908/E)

**Rating:** 2500  
**Tags:** bitmasks, combinatorics, dp, math  
**Solve time:** 9m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We work with binary vectors of length `m`, which can be viewed as integers from `0` to `2^m - 1`.

A valid set `S` must satisfy three structural properties.

First, it contains every vector from the given set `T`.

Second, it is closed under XOR. If two vectors belong to `S`, then their bitwise XOR must also belong to `S`.

Third, it is closed under bitwise AND. If two vectors belong to `S`, then their bitwise AND must also belong to `S`.

The task is to count how many different sets `S` satisfy all of these requirements.

The constraints immediately suggest that we are not supposed to build sets of vectors explicitly. The ambient space contains `2^m` vectors, and `m` can be as large as `1000`. Any approach that reasons about vectors one by one is impossible.

The unusual part of the input is that `n` is very small. We have at most `50` given vectors, while the dimension `m` can reach `1000`. That asymmetry is the key. Instead of thinking about rows, we should think about columns.

A common mistake is to focus on the vectors themselves and try to generate the closure of `T` under XOR and AND. Even for moderate dimensions that closure can already contain exponentially many vectors.

Another easy mistake is to assume that closure under XOR alone is enough. For example:

```
m = 2
T = {10, 01}
```

The XOR-closure is the entire space `{00,01,10,11}`. That set is indeed valid, but it is not the only linear-algebra object involved. The AND condition is what gives the problem its real structure.

A second subtle case appears when several coordinates look identical across all vectors of `T`.

```
m = 2
T = {11}
```

Both coordinates behave identically inside `T`. There are two valid sets:

```
{00,11}
```

and

```
{00,01,10,11}
```

A solution that treats identical coordinates as permanently merged would miss one of them.

## Approaches

A brute-force viewpoint is useful because it reveals the underlying algebraic structure.

Suppose we try to enumerate every set `S` containing `T` and test whether it is closed under XOR and AND. The universe contains `2^m` vectors, so the number of candidate sets is

$$2^{2^m}.$$

Even for `m = 20` this is absurdly large.

A more sophisticated brute force would start from `T` and repeatedly add all XOR and AND results until closure is reached. That computes the smallest valid set containing `T`, but the problem asks for all valid sets, not only the minimal one.

The key observation is that closure under XOR makes `S` a vector space over `F₂`, while closure under AND means that `S` is also closed under coordinatewise multiplication.

A subspace of `F₂^m` that is closed under coordinatewise multiplication is a Boolean subring of `F₂^m`.

Such subrings have a very rigid form.

Consider two coordinate positions `i` and `j`. If every vector in `S` always has the same bit in these two positions, then the coordinates are indistinguishable inside `S`. This relation partitions the coordinates into blocks.

For any block, every vector of `S` must be constant on that block. Conversely, once a partition of coordinates is fixed, the set of all vectors that are constant on each block is closed under both XOR and AND.

Hence every valid set corresponds exactly to a partition of the coordinate positions.

Now impose the requirement that every vector of `T` belongs to `S`.

Take two coordinates `i` and `j`. They may lie in the same block only if every vector of `T` has the same bit at positions `i` and `j`.

For each coordinate, form its column signature:

$$(t_1[i], t_2[i], \dots, t_n[i]).$$

Coordinates with different signatures can never be placed in the same block.

Coordinates with the same signature are completely interchangeable. Inside such a group of size `c`, we may partition the coordinates in any way we like, and every such partition produces a distinct valid set.

The number of partitions of a set of size `c` is the Bell number `Bell(c)`.

Different signature groups are independent, so the answer is

$$\prod Bell(c_i),$$

where `c_i` are the sizes of the signature groups.

The only remaining task is computing Bell numbers up to `1000`.

Using the Stirling-number recurrence

$$S(n,k)=S(n-1,k-1)+kS(n-1,k),$$

we can compute all Bell numbers

$$Bell(n)=\sum_{k=0}^{n} S(n,k)$$

in `O(m²)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `2^m` | Exponential | Too slow |
| Optimal | `O(m² + mn)` | `O(m²)` | Accepted |

## Algorithm Walkthrough

1. Read all `n` binary strings.
2. For every coordinate position `j`, build its column signature consisting of the `j`-th bits of all input strings.
3. Group coordinates by identical signatures and record the size of each group.
4. Precompute Bell numbers up to `m`.
5. Use the Stirling recurrence

$$S(n,k)=S(n-1,k-1)+kS(n-1,k)$$

modulo `10^9+7`.
6. For every `n`, sum all `S(n,k)` to obtain `Bell(n)`.
7. Initialize the answer as `1`.
8. For each signature group of size `c`, multiply the answer by `Bell(c)` modulo `10^9+7`.
9. Output the result.

The reason Step 3 is sufficient is that coordinates with different signatures can never belong to the same partition block, while coordinates sharing a signature may be partitioned arbitrarily.

### Why it works

Every good set is a Boolean subring of `F₂^m`. Boolean subrings of `F₂^m` are exactly the collections of vectors that are constant on the blocks of some partition of the coordinates.

The vectors of `T` restrict which coordinates may share a block. Two coordinates can be merged only when all vectors of `T` assign the same bit to both positions, which is exactly the condition that their column signatures are equal.

Within one signature class, any partition is allowed. Different signature classes are independent. The number of partitions of a class of size `c` is `Bell(c)`, so multiplying Bell numbers over all classes counts every valid set exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    m, n = map(int, input().split())
    rows = [input().strip() for _ in range(n)]

    groups = {}

    for col in range(m):
        sig = tuple(rows[r][col] for r in range(n))
        groups[sig] = groups.get(sig, 0) + 1

    # Stirling numbers of the second kind
    stir = [[0] * (m + 1) for _ in range(m + 1)]
    stir[0][0] = 1

    bell = [0] * (m + 1)
    bell[0] = 1

    for i in range(1, m + 1):
        for k in range(1, i + 1):
            stir[i][k] = (
                stir[i - 1][k - 1] +
                k * stir[i - 1][k]
            ) % MOD

        bell[i] = sum(stir[i][1:i + 1]) % MOD

    ans = 1
    for cnt in groups.values():
        ans = (ans * bell[cnt]) % MOD

    print(ans)

solve()
```

The first part of the implementation builds the column signatures. Since `n ≤ 50`, storing a signature as a tuple of characters is completely safe. Two coordinates belong to the same group exactly when these tuples are equal.

The Bell numbers are computed through Stirling numbers of the second kind. With `m ≤ 1000`, the `O(m²)` dynamic program performs about one million state updates, which easily fits the limits.

A common implementation error is to try computing Bell numbers directly from their recursive definition. That recurrence involves all previous Bell numbers and quickly becomes quadratic anyway. The Stirling recurrence is straightforward and numerically stable modulo `10^9+7`.

Another subtle point is that `Bell(0)=1`. Although no signature group ever has size zero, this base case is required to start the Stirling DP correctly.

## Worked Examples

### Sample 1

Input:

```
5 3
11010
00101
11000
```

Column signatures:

| Position | Signature |
| --- | --- |
| 1 | (1,0,1) |
| 2 | (1,0,1) |
| 3 | (0,1,0) |
| 4 | (1,0,0) |
| 5 | (0,1,0) |

Grouping:

| Signature | Count |
| --- | --- |
| (1,0,1) | 2 |
| (0,1,0) | 2 |
| (1,0,0) | 1 |

Bell values:

| Size | Bell |
| --- | --- |
| 1 | 1 |
| 2 | 2 |

Answer:

| Group Size | Contribution |
| --- | --- |
| 2 | 2 |
| 2 | 2 |
| 1 | 1 |

$$2 \times 2 \times 1 = 4.$$

Output:

```
4
```

This example shows that each signature class contributes independently.

### Custom Example

Input:

```
2 1
11
```

Column signatures:

| Position | Signature |
| --- | --- |
| 1 | (1) |
| 2 | (1) |

There is one signature class of size `2`.

| Size | Bell |
| --- | --- |
| 2 | 2 |

Answer:

$$2.$$

The two partitions are:

```
{1,2}
```

and

```
{1},{2}
```

which correspond to the two valid good sets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(m² + mn)` | Bell-number DP plus signature construction |
| Space | `O(m²)` | Stirling DP table |

The dominant term is the `O(m²)` Stirling-number computation. With `m = 1000`, this is roughly one million DP states, which comfortably fits within the time limit. The memory usage is also acceptable for a `1001 × 1001` table.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    m, n = map(int, input().split())
    rows = [input().strip() for _ in range(n)]

    groups = {}

    for col in range(m):
        sig = tuple(rows[r][col] for r in range(n))
        groups[sig] = groups.get(sig, 0) + 1

    stir = [[0] * (m + 1) for _ in range(m + 1)]
    stir[0][0] = 1

    bell = [0] * (m + 1)
    bell[0] = 1

    for i in range(1, m + 1):
        for k in range(1, i + 1):
            stir[i][k] = (stir[i - 1][k - 1] + k * stir[i - 1][k]) % MOD
        bell[i] = sum(stir[i][1:i + 1]) % MOD

    ans = 1
    for c in groups.values():
        ans = (ans * bell[c]) % MOD

    return str(ans)

# provided sample
assert run(
"""5 3
11010
00101
11000
"""
) == "4"

# minimum size
assert run(
"""1 1
0
"""
) == "1"

# one signature class of size 2
assert run(
"""2 1
11
"""
) == "2"

# three identical columns, Bell(3)=5
assert run(
"""3 1
111
"""
) == "5"

# all signatures distinct
assert run(
"""3 2
101
010
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `1` | Smallest possible instance |
| `2 1 / 11` | `2` | Bell number for size 2 |
| `3 1 / 111` | `5` | Bell number for size 3 |
| `3 2 / 101 / 010` | `1` | Every signature unique |

## Edge Cases

Consider

```
1 1
0
```

There is only one coordinate, so there is exactly one signature class of size `1`. Since `Bell(1)=1`, the algorithm returns `1`. No special handling is required.

Consider

```
2 1
11
```

Both coordinates have the same signature `(1)`. The group size is `2`, giving `Bell(2)=2`. The algorithm correctly counts both possible coordinate partitions.

Consider

```
3 2
101
010
```

The signatures are:

```
(1,0), (0,1), (1,0)
```

Coordinates `1` and `3` may interact, but coordinate `2` cannot join them. The answer becomes

$$Bell(2)\cdot Bell(1)=2.$$

This demonstrates why grouping by column signatures is the correct criterion. Two coordinates are mergeable exactly when every vector of `T` sees them as identical.
