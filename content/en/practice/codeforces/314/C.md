---
title: "CF 314C - Sereja and Subsequences"
description: "We are given an array of positive integers. Consider every distinct non-empty non-decreasing subsequence of the array. For each such subsequence $y = (y1,dots,yk)$, we count all positive integer sequences $x = (x1,dots,xk)$ satisfying $$xi le yi$$ for every position."
date: "2026-06-06T01:18:08+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 314
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 187 (Div. 1)"
rating: 2000
weight: 314
solve_time_s: 159
verified: true
draft: false
---

[CF 314C - Sereja and Subsequences](https://codeforces.com/problemset/problem/314/C)

**Rating:** 2000  
**Tags:** data structures, dp  
**Solve time:** 2m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers.

Consider every **distinct non-empty non-decreasing subsequence** of the array. For each such subsequence $y = (y_1,\dots,y_k)$, we count all positive integer sequences $x = (x_1,\dots,x_k)$ satisfying

$$x_i \le y_i$$

for every position.

For a fixed subsequence $y$, the number of valid sequences $x$ is simply

$$y_1 \cdot y_2 \cdots y_k$$

because each position can independently choose any value from $1$ to $y_i$.

The task is to compute the sum of these products over all **distinct non-decreasing subsequences** of the original array.

The array length reaches $10^5$, and values reach $10^6$. Enumerating subsequences is immediately impossible because an array of length $10^5$ can have exponentially many subsequences. Even $O(n^2)$ is far too slow here, since it would require around $10^{10}$ operations.

The value bound is much smaller than the number of possible subsequences. That suggests building a dynamic program indexed by value rather than by subsequence.

A subtle point is the word **distinct**. Two subsequences chosen from different positions but producing the same value sequence must be counted only once.

For example:

```
2
1 1
```

The non-decreasing subsequences are:

```
[1]
[1]
[1,1]
```

but the distinct ones are only:

```
[1]
[1,1]
```

Their contribution is

```
1 + 1 = 2
```

A DP that blindly counts subsequence occurrences would produce 3 instead of 2.

Another easy mistake appears when equal values occur many times.

```
3
2 2 2
```

The distinct non-decreasing subsequences are:

```
[2]
[2,2]
[2,2,2]
```

The answer is

```
2 + 4 + 8 = 14
```

A solution must carefully overwrite old contributions for value 2 instead of accumulating duplicate sequences.

## Approaches

The brute force idea is straightforward. Generate every subsequence, keep only the non-decreasing ones, store them in a set to remove duplicates, compute the product of each sequence, and sum the results.

This is correct because every distinct non-decreasing subsequence is explicitly generated and counted once.

The problem is the number of subsequences. An array of length $10^5$ has $2^{100000}$ subsequences. Even for $n=50$, enumeration is already hopeless.

The key observation is that we never need the subsequences themselves. We only need the sum of their products.

Suppose we process the array from left to right. Let

$$F(v)$$

denote the total contribution of all distinct non-decreasing subsequences whose last value is exactly $v$.

When we encounter a new array element $x$, every existing subsequence ending with a value at most $x$ can be extended by $x$. Since appending $x$ multiplies the subsequence product by $x$, the total contribution of all newly formed subsequences ending at $x$ is

$$x \cdot \sum_{t \le x} F(t).$$

We must also include the one-element subsequence $[x]$, whose product is $x$.

That gives

$$\text{new}(x) = x \cdot \left(1 + \sum_{t \le x} F(t)\right).$$

The remaining challenge is handling distinctness.

If the value $x$ appeared earlier, some subsequences ending with $x$ have already been represented in $F(x)$. The standard trick is to replace the old contribution for value $x$ by the newly computed one. The newer occurrence can generate every distinct sequence ending in $x$ that is currently possible, so the old value becomes obsolete.

We need two operations efficiently:

1. Query $\sum_{t \le x} F(t)$.
2. Replace $F(x)$ by a new value.

Since values are at most $10^6$, a Fenwick tree over value coordinates supports both operations in $O(\log 10^6)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | Exponential | Too slow |
| Optimal | $O(n \log V)$ | $O(V)$ | Accepted |

Here $V = 10^6$.

## Algorithm Walkthrough

1. Create a Fenwick tree indexed by values from 1 to $10^6$.
2. Maintain an array `last[v]`, which stores the current contribution $F(v)$.
3. Process the input array from left to right.
4. For the current value $x$, query the Fenwick tree for

$$S = \sum_{t \le x} F(t).$$

This represents the total contribution of all distinct non-decreasing subsequences whose last element is at most $x$.
5. Compute

$$cur = x \cdot (1 + S).$$

The term $1$ creates the single-element subsequence $[x]$. The term $S$ extends every valid subsequence ending with a value at most $x$.
6. Let `old = last[x]`.

We are replacing the entire contribution of value $x$, not adding to it. This is what removes duplicates created by repeated occurrences of the same value.
7. Update the Fenwick tree by adding

$$cur - old.$$

After this operation, the Fenwick tree again stores the correct values $F(v)$.
8. Set `last[x] = cur`.
9. After all elements are processed, the answer is the sum of all $F(v)$, which equals the Fenwick prefix sum over the whole range.

### Why it works

After processing any prefix of the array, $F(v)$ is defined as the total product-sum of all **distinct** non-decreasing subsequences obtainable from that prefix whose final value equals $v$.

When a new value $x$ arrives, every subsequence ending with a value at most $x$ can be extended by $x$, and every product is multiplied by $x$. Adding the one-element subsequence produces exactly

$$x \cdot \left(1 + \sum_{t \le x} F(t)\right).$$

If $x$ appeared earlier, the newly computed value already represents the complete set of distinct subsequences ending in $x$ that can be formed from the current prefix. Replacing the previous $F(x)$ prevents duplicate counting of identical value sequences. By induction over the processed positions, the invariant remains true for every value. The final sum of all $F(v)$ is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007
MAXV = 1000000

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, delta):
        n = self.n
        bit = self.bit
        while idx <= n:
            bit[idx] = (bit[idx] + delta) % MOD
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        bit = self.bit
        while idx > 0:
            res += bit[idx]
            res %= MOD
            idx -= idx & -idx
        return res

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    fw = Fenwick(MAXV)
    last = [0] * (MAXV + 1)

    for x in a:
        s = fw.sum(x)
        cur = x * (1 + s) % MOD

        old = last[x]
        last[x] = cur

        fw.add(x, (cur - old) % MOD)

    print(fw.sum(MAXV))

if __name__ == "__main__":
    solve()
```

The Fenwick tree stores the current values $F(v)$. A prefix query gives $\sum_{t \le x} F(t)$, which is exactly the quantity needed by the recurrence.

The array `last` is the crucial detail. Without it, repeated values would accumulate contributions instead of replacing them, causing duplicate subsequences to be counted multiple times.

The update uses `cur - old` because the Fenwick tree stores the current value of $F(x)$. We are performing an assignment, not an increment. Working modulo $10^9+7$ means the difference must also be reduced modulo the modulus before insertion.

The final answer is the sum of all $F(v)$, obtained by a full Fenwick prefix query.

## Worked Examples

### Example 1

Input:

```
1
42
```

| Step | x | Prefix Sum S | cur | F(42) |
| --- | --- | --- | --- | --- |
| 1 | 42 | 0 | 42 | 42 |

Final answer:

```
42
```

The only distinct non-decreasing subsequence is `[42]`, whose contribution is 42.

### Example 2

Input:

```
2
1 1
```

| Step | x | Prefix Sum S | cur | Old F(1) | New F(1) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 0 | 1 |
| 2 | 1 | 1 | 2 | 1 | 2 |

Final answer:

```
2
```

The distinct subsequences are:

```
[1]
[1,1]
```

with contributions

```
1 + 1 = 2.
```

The trace shows why replacement is necessary. After the second occurrence, `F(1)` becomes 2, not 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log V)$ | One Fenwick query and one update per element |
| Space | $O(V)$ | Fenwick tree and `last` array over values $1 \ldots 10^6$ |

With $n = 10^5$ and $V = 10^6$, $\log V$ is about 20. The solution performs only a few million primitive operations and comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 1000000007
MAXV = 1000000

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, delta):
            while idx <= self.n:
                self.bit[idx] = (self.bit[idx] + delta) % MOD
                idx += idx & -idx

        def sum(self, idx):
            res = 0
            while idx > 0:
                res = (res + self.bit[idx]) % MOD
                idx -= idx & -idx
            return res

    n = int(input())
    a = list(map(int, input().split()))

    fw = Fenwick(MAXV)
    last = [0] * (MAXV + 1)

    for x in a:
        s = fw.sum(x)
        cur = x * (1 + s) % MOD
        fw.add(x, (cur - last[x]) % MOD)
        last[x] = cur

    return str(fw.sum(MAXV)) + "\n"

# provided sample
assert run("1\n42\n") == "42\n", "sample 1"

# custom cases
assert run("1\n1\n") == "1\n", "minimum size"
assert run("2\n1 1\n") == "2\n", "duplicate values"
assert run("2\n1 2\n") == "5\n", "strictly increasing"
assert run("3\n2 2 2\n") == "14\n", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Smallest possible instance |
| `1 1` | `2` | Distinct subsequence handling |
| `1 2` | `5` | Basic extension recurrence |
| `2 2 2` | `14` | Repeated overwriting of the same value |

## Edge Cases

Consider:

```
2
1 1
```

After the first value, `F(1)=1`. After the second value, the prefix sum up to 1 is also 1, giving `cur=2`. The algorithm replaces `F(1)` by 2. The final answer is 2, corresponding exactly to `[1]` and `[1,1]`. A naive accumulation would incorrectly produce 3.

Consider:

```
3
2 2 2
```

The states are:

```
F(2)=2
F(2)=6
F(2)=14
```

Each update replaces the previous value. The final answer becomes 14, which equals

```
2 + 4 + 8
```

for the distinct subsequences `[2]`, `[2,2]`, and `[2,2,2]`.

Consider:

```
2
2 1
```

The subsequence `[2,1]` is not non-decreasing and cannot contribute. The algorithm naturally enforces this because extensions are allowed only from values `<= x`. When processing `1`, the contribution from sequences ending in `2` is excluded from the prefix query. The answer becomes

```
2 + 1 = 3
```

which matches the valid subsequences `[2]` and `[1]`.
