---
title: "CF 106045C - Cursed Queries"
description: "We have an array and a fixed integer $m$, called the cursed number. Two kinds of operations must be processed online. An update replaces one array element with a new value. A query looks at a subarray and a value $k$, then asks how many elements of that subarray are k-good."
date: "2026-06-25T12:40:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106045
codeforces_index: "C"
codeforces_contest_name: "IUT Intra University Programming Contest 2025"
rating: 0
weight: 106045
solve_time_s: 58
verified: true
draft: false
---

[CF 106045C - Cursed Queries](https://codeforces.com/problemset/problem/106045/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array and a fixed integer $m$, called the cursed number.

Two kinds of operations must be processed online. An update replaces one array element with a new value. A query looks at a subarray and a value $k$, then asks how many elements of that subarray are _k-good_.

The definition is slightly indirect. A number is considered good if it is not divisible by $m$. A number $x$ is k-good if after adding $k$ any number of times, it always remains good. In other words, none of the values

$$x,\; x+k,\; x+2k,\; x+3k,\dots$$

may ever become divisible by $m$.

The input contains up to $10^4$ test cases, but the important constraint is that the total $n$ and total $q$ over all test cases are at most $10^5$. Any solution around $O((n+q)\log n)$ per test case is easily fast enough. A quadratic scan over a subarray for every query would be far too slow because a single test could already contain $10^5$ operations.

The main difficulty is understanding the k-good condition. Once that is simplified, the problem becomes a dynamic range counting problem.

Consider a few situations that can easily lead to wrong reasoning.

If $m=8$, $k=12$, and $x=1$, then the sequence modulo $8$ is

$$1,5,1,5,\dots$$

It never reaches $0$, so $x$ is k-good.

If $m=8$, $k=12$, and $x=4$, then modulo $8$ we get

$$4,0,4,0,\dots$$

The second term is divisible by $8$, so $x$ is not k-good.

A common mistake is to test only whether $x$ itself is divisible by $m$. The definition requires checking all future additions as well.

Another subtle case appears when $k$ is a multiple of $m$. For example, $m=10$, $k=20$. Adding $k$ never changes the residue modulo $m$. Then a number is k-good exactly when it is not divisible by $10$. Any solution that treats all values of $k$ uniformly without examining $\gcd(k,m)$ will miss this behavior.

## Approaches

The brute force interpretation follows the definition directly. For every query, inspect each element of the subarray and determine whether repeated additions of $k$ can ever produce a multiple of $m$.

One way to do that is to work modulo $m$. Starting from $a_i \bmod m$, repeatedly add $k \bmod m$ until the sequence repeats. Since there are only $m$ residues, this takes $O(m)$ time per element.

With $m \le 5000$, a query on a range of length $10^5$ could require roughly

$$10^5 \cdot 5000$$

operations, which is completely infeasible.

The key observation comes from modular arithmetic.

We want to know whether there exists some $t \ge 0$ such that

$$a_i + t k \equiv 0 \pmod m.$$

This linear congruence has a solution if and only if

$$\gcd(k,m) \mid a_i.$$

Let

$$g = \gcd(k,m).$$

Then:

$$a_i \text{ is k-good}
\iff g \nmid a_i.$$

The entire complicated definition collapses into a simple divisibility test.

Now the query becomes:

Count elements in $[l,r]$ that are **not divisible by** $g$.

Since $m$ never changes and $g$ must be a divisor of $m$, only divisors of $m$ can ever appear in queries. The number of divisors of any integer up to $5000$ is small, at most a few dozen.

For every divisor $d$ of $m$, maintain a Fenwick tree storing which positions currently contain numbers divisible by $d$.

Then:

$$\text{answer}
=
(r-l+1)
-
\#\{\text{elements divisible by } g\}.$$

Updates modify one position, so we update every divisor tree once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l+1)\cdot m)$ per query | $O(1)$ | Too slow |
| Optimal | $O(D\log n)$ per operation | $O(Dn)$ | Accepted |

Here $D$ is the number of divisors of $m$.

## Algorithm Walkthrough

1. Compute all divisors of $m$.
2. Create one Fenwick tree for each divisor $d$.
3. For every array position $i$, insert value $1$ into divisor tree $d$ if $a_i$ is divisible by $d$.
4. For an update `1 i x`, remove the contribution of the old value from every divisor tree and add the contribution of the new value.

The number of divisors is small, so touching every divisor is inexpensive.
5. For a query `2 l r k`, compute

$$g=\gcd(k,m).$$
6. Use the Fenwick tree corresponding to divisor $g$ to count how many values in $[l,r]$ are divisible by $g$.
7. Let that count be `bad`. The number of k-good elements is

$$(r-l+1)-bad.$$
8. Output the result.

### Why it works

The crucial property is the classical linear congruence result:

$$a + tk \equiv 0 \pmod m$$

has a solution if and only if

$$\gcd(k,m)\mid a.$$

If $g=\gcd(k,m)$ divides $a$, some future term becomes divisible by $m$, so the number is not k-good.

If $g$ does not divide $a$, no term in the entire arithmetic progression can ever become divisible by $m$, so the number is k-good.

Thus every query reduces exactly to counting values not divisible by $g$, and the Fenwick trees maintain those divisibility counts correctly under updates.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, delta):
        n = self.n
        bit = self.bit
        while idx <= n:
            bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx):
        bit = self.bit
        res = 0
        while idx > 0:
            res += bit[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        divisors = []
        for d in range(1, m + 1):
            if m % d == 0:
                divisors.append(d)

        idx_of = {d: i for i, d in enumerate(divisors)}

        trees = [Fenwick(n) for _ in divisors]

        for pos, val in enumerate(a, start=1):
            for j, d in enumerate(divisors):
                if val % d == 0:
                    trees[j].add(pos, 1)

        q = int(input())

        for _ in range(q):
            query = list(map(int, input().split()))

            if query[0] == 1:
                _, i, x = query
                old = a[i - 1]

                for j, d in enumerate(divisors):
                    old_div = (old % d == 0)
                    new_div = (x % d == 0)

                    if old_div != new_div:
                        trees[j].add(i, 1 if new_div else -1)

                a[i - 1] = x

            else:
                _, l, r, k = query

                g = gcd(k, m)
                tree = trees[idx_of[g]]

                divisible = tree.range_sum(l, r)
                ans = (r - l + 1) - divisible

                out.append(str(ans))

    sys.stdout.write("\n".join(out))

solve()
```

The first part computes all divisors of $m$. Since every possible query uses $g=\gcd(k,m)$, and every such $g$ must be a divisor of $m$, these are the only divisibility classes we ever need.

Each Fenwick tree stores, for one divisor $d$, whether each position currently contains a multiple of $d$. A range sum immediately gives the number of multiples of $d$ inside any interval.

The update operation compares the old and new divisibility status for every divisor. Only when the status changes do we modify the Fenwick tree. This avoids unnecessary updates.

The query operation computes $g=\gcd(k,m)$, finds the corresponding Fenwick tree, counts multiples of $g$ in the range, and subtracts from the interval length.

All arithmetic fits comfortably inside Python integers, so there are no overflow concerns.

## Worked Examples

### Example 1

Input:

```
n = 5, m = 10
a = [1, 2, 3, 4, 5]

query: 2 1 5 2
```

Here:

$$g=\gcd(2,10)=2.$$

| Position | Value | Divisible by 2? |
| --- | --- | --- |
| 1 | 1 | No |
| 2 | 2 | Yes |
| 3 | 3 | No |
| 4 | 4 | Yes |
| 5 | 5 | No |

The Fenwick tree for divisor 2 reports 2 divisible elements.

| l | r | Length | Divisible by g | Answer |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 2 | 3 |

Output:

```
3
```

This demonstrates the main reduction. We never simulate repeated additions of $k$.

### Example 2

Input:

```
n = 4, m = 8
a = [1, 8, 6, 5]

update: 1 2 9
query: 2 1 4 12
```

After the update:

```
[1, 9, 6, 5]
```

$$g=\gcd(12,8)=4.$$

| Position | Value | Divisible by 4? |
| --- | --- | --- |
| 1 | 1 | No |
| 2 | 9 | No |
| 3 | 6 | No |
| 4 | 5 | No |

| Length | Divisible by 4 | Answer |
| --- | --- | --- |
| 4 | 0 | 4 |

Output:

```
4
```

This trace shows how updates propagate through the divisor structures before answering later queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(D \log n)$ per operation | Every update or query touches at most one Fenwick tree per divisor |
| Space | $O(Dn)$ | One Fenwick tree for each divisor of $m$ |

Since $m \le 5000$, the number of divisors $D$ is small. Combined with the global limit of $10^5$ array elements and queries, this comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i:
                s += self.bit[i]
                i -= i & -i
            return s

    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        divs = [d for d in range(1, m + 1) if m % d == 0]
        mp = {d: i for i, d in enumerate(divs)}

        fw = [Fenwick(n) for _ in divs]

        for p, val in enumerate(a, start=1):
            for j, d in enumerate(divs):
                if val % d == 0:
                    fw[j].add(p, 1)

        q = int(input())

        for _ in range(q):
            qv = list(map(int, input().split()))

            if qv[0] == 1:
                _, i, x = qv
                old = a[i - 1]

                for j, d in enumerate(divs):
                    if (old % d == 0) != (x % d == 0):
                        fw[j].add(i, 1 if x % d == 0 else -1)

                a[i - 1] = x
            else:
                _, l, r, k = qv
                g = gcd(k, m)

                tree = fw[mp[g]]
                divcnt = tree.sum(r) - tree.sum(l - 1)

                ans.append(str((r - l + 1) - divcnt))

    return "\n".join(ans)

# sample 1
assert run(
"""1
5 10
1 2 3 4 5
5
2 1 5 1
2 1 5 2
2 1 5 3
2 1 5 4
2 1 5 5
"""
) == "0\n3\n0\n3\n0"

# minimum size
assert run(
"""1
1 7
1
1
2 1 1 14
"""
) == "1"

# all equal values
assert run(
"""1
4 6
6 6 6 6
1
2 1 4 3
"""
) == "0"

# update changes answer
assert run(
"""1
3 8
1 8 5
3
2 1 3 4
1 2 7
2 1 3 4
"""
) == "2\n3"

# boundary interval
assert run(
"""1
3 12
4 6 9
1
2 2 2 18
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element, $m=7$ | 1 | Minimum size case |
| All values equal to $m$ | 0 | Every element divisible by the relevant gcd |
| Update replacing a divisible value | 2 then 3 | Correct update propagation |
| Query on a single position | 0 | Range boundary handling |

## Edge Cases

### Case 1: $k$ is a multiple of $m$

Input:

```
1
3 10
10 11 12
1
2 1 3 20
```

Here

$$g=\gcd(20,10)=10.$$

Only the first value is divisible by 10.

The Fenwick tree for divisor 10 reports one divisible element in the range. The interval length is 3, so the answer is

$$3-1=2.$$

This matches the actual behavior because adding 20 never changes a residue modulo 10.

### Case 2: Value not divisible by $m$, but still not k-good

Input:

```
1
1 8
4
1
2 1 1 12
```

We have

$$g=\gcd(12,8)=4.$$

The value 4 is divisible by 4, so it is counted as not k-good.

Indeed,

$$4+12=16,$$

which is divisible by 8.

The algorithm outputs 0, which is correct.

### Case 3: Single-position range after updates

Input:

```
1
1 6
6
2
1 1 5
2 1 1 3
```

After the update, the value becomes 5.

$$g=\gcd(3,6)=3.$$

Since 5 is not divisible by 3, the Fenwick tree reports zero divisible elements.

The answer is

$$1-0=1.$$

This confirms that updates and one-element ranges work correctly together.
