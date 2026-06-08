---
title: "CF 2116C - Gellyfish and Flaming Peony"
description: "We are given an array of positive integers. In one operation, we choose two different positions and replace one value with the gcd of the two values. The process may be repeated as many times as needed."
date: "2026-06-09T04:00:32+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "dp", "math", "number-theory", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 2116
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1028 (Div. 2)"
rating: 1500
weight: 2116
solve_time_s: 123
verified: true
draft: false
---

[CF 2116C - Gellyfish and Flaming Peony](https://codeforces.com/problemset/problem/2116/C)

**Rating:** 1500  
**Tags:** brute force, dfs and similar, dp, math, number theory, shortest paths  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. In one operation, we choose two different positions and replace one value with the gcd of the two values.

The process may be repeated as many times as needed. The goal is to make every element in the array equal, while using the minimum possible number of operations.

The key question is not whether it can be done, because the statement guarantees that it always can. The challenge is finding the smallest number of operations.

The constraints are unusually small. Every array value is at most 5000, and the sum of all array lengths over the entire input is also at most 5000. This immediately suggests that algorithms involving states over possible gcd values are feasible. Since gcd values can never exceed 5000, a dynamic programming or shortest-path style solution on the value space is practical.

A brute-force search over arrays is impossible because the number of reachable arrays grows exponentially. We need to exploit the structure of gcd operations rather than simulate all possibilities.

There are several non-obvious situations that can easily lead to incorrect reasoning.

Consider:

```
3
2 2 2
```

The answer is `0`. The array is already equal. Any solution that automatically tries to construct new gcd values will overcount.

Consider:

```
3
2 4 6
```

The gcd of the whole array is `2`, and `2` is already present. The answer is `2`.

We can turn `4` into `2` in one operation and `6` into `2` in another. A common mistake is to first "create" a gcd value even though it already exists.

Consider:

```
3
6 10 15
```

The global gcd is `1`, but no element equals `1`.

The answer is not simply `n-1 = 2`. Before we can spread the value `1`, we must first create a `1` somewhere. This extra cost is the central difficulty of the problem.

Consider:

```
2
6 10
```

The global gcd is `2`, but neither element equals `2`.

One operation can produce `2` from either element:

```
6 -> gcd(6,10)=2
```

giving `[2,10]`.

A second operation changes `10` into `2`.

The answer is `2`, not `1`. Producing the target value and propagating it are separate tasks.

## Approaches

A natural brute-force idea is to treat each array configuration as a state and perform BFS until all elements become equal.

This is correct because every operation has unit cost, so BFS would find the minimum number of operations.

Unfortunately, it is completely infeasible. Even with small values, the number of possible arrays grows exponentially with `n`, and each state has `O(n²)` possible moves. The state space explodes almost immediately.

To find something better, we need to understand what value the final array must contain.

Every operation replaces a value by a gcd. Gcd operations can only decrease numbers, never increase them. Because of that, the only value that can eventually appear everywhere is the gcd of the entire array.

Let

```
G = gcd(a1, a2, ..., an)
```

The final array must be:

```
[G, G, ..., G]
```

Now the problem becomes much more structured.

Suppose an element already equals `G`. Then that element can be used as a "source". Any other element can be converted to `G` in exactly one operation:

```
x -> gcd(x, G) = G
```

So if there are already `cnt` occurrences of `G`, we only need:

```
n - cnt
```

operations.

The interesting case is when no element equals `G`.

Before we can spread `G`, we must first create one occurrence of `G`.

How many operations does that require?

Observe what happens when we repeatedly apply gcd operations to a single position. After several operations, that position becomes the gcd of some subset of array elements.

For example:

```
gcd(a3, a7, a2, a5)
```

can be produced by repeatedly taking gcds into one location.

Thus, creating the first `G` is equivalent to finding the smallest subset whose gcd is `G`.

If a subset has size `k`, then producing its gcd requires exactly `k-1` operations.

After obtaining one copy of `G`, we still need `n-1` more operations to convert all remaining positions.

Total cost:

```
(k - 1) + (n - 1)
= n + k - 2
```

So the problem reduces to finding the minimum subset size whose gcd equals `G`.

Since every array value is at most 5000, we can run DP on gcd values.

Let:

```
dp[g] = minimum subset size whose gcd is g
```

Process the array elements one by one. For each existing gcd state, either start a new subset with the current element or extend a previous subset.

The number of possible gcd values is only 5000, making this approach efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force on Array States | Exponential | Exponential | Too slow |
| DP on GCD Values | O(n · V) where V=5000 | O(V) | Accepted |

## Algorithm Walkthrough

1. Compute the global gcd `G` of the entire array.
2. Count how many elements are already equal to `G`.
3. If this count is positive, return `n - count`.

Every remaining element can be transformed into `G` in one operation using an existing occurrence of `G`.
4. Otherwise, compute the minimum subset size whose gcd equals `G`.
5. Maintain a DP array where `dp[g]` stores the minimum number of selected elements needed to obtain gcd `g`.
6. For each array element `x`:

Start a new subset consisting only of `x`.

Also extend every previously reachable gcd state `g` into a new state `gcd(g, x)`.
7. After processing all elements, let `k = dp[G]`.

This is the minimum subset size whose gcd equals the target value.
8. Creating the first occurrence of `G` requires `k - 1` operations.
9. Once one `G` exists, converting all remaining positions requires `n - 1` operations.
10. Return:

```
n + k - 2
```

### Why it works

The final value must be the gcd of the whole array, because gcd operations never increase values and every final element must divide every original element.

If an occurrence of `G` already exists, each non-`G` element can be converted directly into `G` in one operation, and no faster solution exists because every such element must be modified at least once.

When no occurrence of `G` exists, some sequence of operations must create the first `G`. Any value obtained by repeatedly taking gcds at one position equals the gcd of a subset of the original elements. If the smallest such subset has size `k`, then at least `k-1` operations are necessary to combine those elements, and exactly `k-1` operations are sufficient.

After one copy of `G` exists, every remaining position still requires one operation to become `G`, giving another `n-1` operations.

The DP computes the smallest subset size for every reachable gcd value, so it finds the optimal `k`. Combining the two phases yields the minimum possible answer.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

MAXV = 5000
INF = 10**9

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    G = 0
    for x in a:
        G = gcd(G, x)

    cnt = sum(1 for x in a if x == G)

    if cnt > 0:
        print(n - cnt)
        continue

    dp = [INF] * (MAXV + 1)

    for x in a:
        ndp = dp[:]

        ndp[x] = min(ndp[x], 1)

        for g in range(1, MAXV + 1):
            if dp[g] == INF:
                continue

            ng = gcd(g, x)
            ndp[ng] = min(ndp[ng], dp[g] + 1)

        dp = ndp

    k = dp[G]
    print(n + k - 2)
```

The first part computes the global gcd `G`.

Next we count how many elements already equal `G`. If at least one exists, the answer is immediate. Every other element needs exactly one operation, and there is already a source value available.

The second branch handles the harder case. The DP stores the smallest subset size that can achieve each gcd value.

When processing a number `x`, there are two possibilities. We either start a new subset containing only `x`, or we append `x` to a previously formed subset. Appending changes the gcd from `g` to `gcd(g,x)` and increases the subset size by one.

Using a copied array `ndp` is important. Updating the DP in place would allow the same element to be used multiple times during one iteration.

At the end, `dp[G]` is the minimum subset size whose gcd equals the global gcd. The formula `n + k - 2` follows directly from the proof above.

All values remain below 5000, so the DP state space is tiny.

## Worked Examples

### Example 1

Input:

```
3
12 20 30
```

Global gcd:

```
G = 2
```

No element equals `2`.

| Step | Relevant gcd state | Minimum subset size |
| --- | --- | --- |
| Start with 12 | 12 | 1 |
| Add 20 | gcd(12,20)=4 | 2 |
| Add 30 | gcd(4,30)=2 | 3 |

The smallest subset with gcd `2` has size:

```
k = 3
```

Answer:

```
n + k - 2
= 3 + 3 - 2
= 4
```

This matches the sample.

### Example 2

Input:

```
6
1 9 1 9 8 1
```

Global gcd:

```
G = 1
```

Count of existing ones:

```
cnt = 3
```

| Variable | Value |
| --- | --- |
| n | 6 |
| G | 1 |
| cnt | 3 |

Answer:

```
n - cnt
= 6 - 3
= 3
```

Each non-one element can be turned into `1` in a single operation using any existing `1`.

This example demonstrates the shortcut case where no DP is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 5000) | For each element we scan all possible gcd values |
| Space | O(5000) | DP array over gcd values |

Since the sum of all `n` across test cases is at most 5000, the total work is roughly 25 million simple operations in the worst case. This comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        G = 0
        for x in a:
            G = gcd(G, x)

        cnt = sum(1 for x in a if x == G)

        if cnt:
            print(n - cnt)
            continue

        INF = 10**9
        dp = [INF] * 5001

        for x in a:
            ndp = dp[:]
            ndp[x] = min(ndp[x], 1)

            for g in range(1, 5001):
                if dp[g] == INF:
                    continue

                ng = gcd(g, x)
                ndp[ng] = min(ndp[ng], dp[g] + 1)

            dp = ndp

        print(n + dp[G] - 2)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

# provided samples
assert run(
"""3
3
12 20 30
6
1 9 1 9 8 1
3
6 14 15
"""
) == "4\n3\n3\n"

# minimum size
assert run(
"""1
1
7
"""
) == "0\n"

# already equal
assert run(
"""1
5
4 4 4 4 4
"""
) == "0\n"

# global gcd already present
assert run(
"""1
3
2 4 6
"""
) == "2\n"

# need to create gcd first
assert run(
"""1
2
6 10
"""
) == "2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[7]` | `0` | Single-element array |
| `[4,4,4,4,4]` | `0` | Already equal |
| `[2,4,6]` | `2` | Global gcd already exists |
| `[6,10]` | `2` | Must create gcd before spreading |

## Edge Cases

Consider:

```
1
3
2 2 2
```

The global gcd is `2`, and all three elements already equal `2`.

The count of elements equal to `G` is `3`, so the algorithm returns:

```
3 - 3 = 0
```

No operations are needed.

Consider:

```
1
3
2 4 6
```

The global gcd is `2`.

One element already equals `2`, so:

```
cnt = 1
```

The answer becomes:

```
3 - 1 = 2
```

The DP phase is skipped completely. This avoids the common mistake of paying extra cost to create a value that already exists.

Consider:

```
1
3
6 10 15
```

The global gcd is `1`, but no element equals `1`.

The DP finds:

```
gcd(6,10,15) = 1
```

and no smaller subset has gcd `1`, so:

```
k = 3
```

The answer is:

```
3 + 3 - 2 = 4
```

The algorithm correctly accounts for both stages: creating the first `1`, then spreading it.

Consider:

```
1
2
6 10
```

The global gcd is `2`.

No element equals `2`.

The DP finds a subset of size `2` whose gcd is `2`, so:

```
k = 2
```

The answer becomes:

```
2 + 2 - 2 = 2
```

One operation creates a `2`, and one more operation converts the remaining element. This confirms that producing the target value and propagating it are counted separately.
