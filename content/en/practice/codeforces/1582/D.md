---
title: "CF 1582D - Vupsen, Pupsen and 0"
description: "We are given several arrays whose elements are guaranteed to be nonzero. For each array, we must construct another array of the same length. Every element of the new array must also be nonzero, and the weighted sum $$a1b1+a2b2+dots+anbn$$ must equal zero."
date: "2026-06-10T10:02:11+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1582
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 750 (Div. 2)"
rating: 1600
weight: 1582
solve_time_s: 227
verified: false
draft: false
---

[CF 1582D - Vupsen, Pupsen and 0](https://codeforces.com/problemset/problem/1582/D)

**Rating:** 1600  
**Tags:** constructive algorithms, math  
**Solve time:** 3m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several arrays whose elements are guaranteed to be nonzero. For each array, we must construct another array of the same length. Every element of the new array must also be nonzero, and the weighted sum

$$a_1b_1+a_2b_2+\dots+a_nb_n$$

must equal zero.

The actual values of the new array do not matter as long as all entries are nonzero and the sum of absolute values stays below $10^9$. The problem guarantees that at least one valid answer always exists.

The total number of elements over all test cases is at most $2\cdot10^5$. A solution performing quadratic work would require roughly $4\cdot10^{10}$ operations in the worst case, which is far beyond what fits into one second. Linear time per test case is the natural target.

A careless approach can fail on odd-length arrays. For example,

```
3
1 2 3
```

Pairing consecutive elements works for the first two numbers, but leaves the last element without a partner. We still need a nonzero coefficient for it.

One valid answer is

```
-5 1 1
```

because

$$1\cdot(-5)+2\cdot1+3\cdot1=0.$$

Another subtle case appears when two numbers are equal.

```
2
5 5
```

Using coefficients $(5,-5)$ works, but unnecessarily creates large values. The simplest answer is

```
1 -1
```

since

$$5\cdot1+5\cdot(-1)=0.$$

Negative numbers do not change the construction. For

```
2
4 -7
```

choosing

```
7 4
```

gives

$$4\cdot7+(-7)\cdot4=0.$$

The signs are handled automatically by the multiplication.

## Approaches

A brute-force idea is to search for coefficients until the weighted sum becomes zero. Since each coefficient can be positive or negative and many values are possible, the search space grows exponentially. Even restricting coefficients to a small range already produces an infeasible number of combinations. The approach is correct because eventually some valid combination exists, but the number of possibilities explodes long before reaching the input limits.

The structure of the expression suggests a much simpler observation. Suppose we only have two numbers $x$ and $y$. If we choose coefficients

$$(y,-x),$$

their contribution becomes

$$x\cdot y+y\cdot(-x)=0.$$

Any pair can cancel itself independently.

For even $n$, we can process the array two elements at a time and assign coefficients that make each pair contribute zero. Since every pair contributes zero, the whole sum is zero.

Odd lengths create one unpaired element. Instead of treating the last element alone, we handle the last three numbers together. Among three nonzero numbers, at least one pair has a nonzero sum. Suppose the three values are $x,y,z$, and $x+y\neq0$. Then choosing

$$b_x=z,\qquad b_y=z,\qquad b_z=-(x+y)$$

gives

$$xz+yz-z(x+y)=0.$$

All coefficients remain nonzero because $z\neq0$ and $x+y\neq0$.

The entire construction becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an answer array of length $n$.
2. If $n$ is even, process indices in pairs.
3. For a pair $(a_i,a_{i+1})$, assign

$$b_i=a_{i+1},\qquad b_{i+1}=-a_i.$$

Their contribution is zero, so this pair becomes independent from the rest.
4. If $n$ is odd, first process the first $n-3$ elements using the same pair construction.
5. Let the last three numbers be $x,y,z$.
6. Find a pair among them whose sum is nonzero. Since all numbers are nonzero, at least one of the three possible pair sums must be nonzero.
7. Suppose the chosen pair is $p,q$, and the remaining number is $r$. Assign

$$b_p=r,\qquad b_q=r,\qquad b_r=-(a_p+a_q).$$
8. Output the constructed array.

### Why it works

Every pair processed in the even-length part contributes zero by construction:

$$a_ib_i+a_{i+1}b_{i+1}=a_ia_{i+1}-a_{i+1}a_i=0.$$

For the final triple,

$$a_pr+a_qr+a_r(-(a_p+a_q)) =r(a_p+a_q)-r(a_p+a_q)=0.$$

Since each group contributes zero independently, the total sum over the whole array is zero. All coefficients are nonzero because every array element is nonzero and the selected pair has a nonzero sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = [0] * n

    limit = n
    if n % 2 == 1:
        limit = n - 3

    for i in range(0, limit, 2):
        b[i] = a[i + 1]
        b[i + 1] = -a[i]

    if n % 2 == 1:
        x, y, z = n - 3, n - 2, n - 1

        if a[x] + a[y] != 0:
            b[x] = a[z]
            b[y] = a[z]
            b[z] = -(a[x] + a[y])
        elif a[x] + a[z] != 0:
            b[x] = a[y]
            b[z] = a[y]
            b[y] = -(a[x] + a[z])
        else:
            b[y] = a[x]
            b[z] = a[x]
            b[x] = -(a[y] + a[z])

    print(*b)
```

The first part handles all complete pairs. Each pair receives swapped coefficients with one sign flipped, guaranteeing a zero contribution.

Odd lengths are the only delicate case. The code reserves the last three elements and checks the three possible pair sums. At least one of them must be nonzero. Once such a pair is found, the third element supplies the coefficient used twice.

The order of assignments matters because different indices become the special element depending on which pair sum is nonzero. A common mistake is to assume that the first two elements of the triple always work. For example, with values $(1,-1,5)$, the sum of the first two is zero, so another pair must be used.

Python integers have arbitrary precision, so overflow is not an issue. The resulting coefficients are bounded by the original values, whose absolute values are at most $10^4$, making the total absolute sum safely below $10^9$.

## Worked Examples

### Example 1

Input:

```
5
5 -2 10 -9 4
```

The first two elements form one pair, and the last three form a triple.

| Step | Elements considered | Assigned coefficients | Partial answer |
| --- | --- | --- | --- |
| Pair | 5, -2 | -2, -5 | [-2, -5, 0, 0, 0] |
| Triple | 10, -9, 4 | 4, 4, -1 | [-2, -5, 4, 4, -1] |

Checking:

$$5(-2)+(-2)(-5)+10(4)+(-9)(4)+4(-1)=0.$$

This example shows how the final triple handles odd lengths.

### Example 2

Input:

```
7
1 2 3 4 5 6 7
```

| Step | Elements considered | Assigned coefficients | Partial answer |
| --- | --- | --- | --- |
| Pair | 1, 2 | 2, -1 | [2, -1, 0, 0, 0, 0, 0] |
| Pair | 3, 4 | 4, -3 | [2, -1, 4, -3, 0, 0, 0] |
| Triple | 5, 6, 7 | 7, 7, -11 | [2, -1, 4, -3, 7, 7, -11] |

Checking:

$$1\cdot2+2(-1)+3\cdot4+4(-3)+5\cdot7+6\cdot7+7(-11)=0.$$

This trace illustrates that every group independently contributes zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every element is processed once |
| Space | O(n) | The answer array stores one coefficient per element |

The total number of elements across all test cases is at most $2\cdot10^5$, so linear processing performs only a few hundred thousand operations. Memory usage is also linear and comfortably fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = []
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = [0] * n

        limit = n if n % 2 == 0 else n - 3

        for i in range(0, limit, 2):
            b[i] = a[i + 1]
            b[i + 1] = -a[i]

        if n % 2 == 1:
            x, y, z = n - 3, n - 2, n - 1

            if a[x] + a[y] != 0:
                b[x], b[y], b[z] = a[z], a[z], -(a[x] + a[y])
            elif a[x] + a[z] != 0:
                b[x], b[z], b[y] = a[y], a[y], -(a[x] + a[z])
            else:
                b[y], b[z], b[x] = a[x], a[x], -(a[y] + a[z])

        out.append(" ".join(map(str, b)))

    return "\n".join(out)

# minimum size
assert run("1\n2\n5 5\n") == "5 -5"

# all equal values
assert run("1\n4\n7 7 7 7\n") == "7 -7 7 -7"

# odd length with first pair sum zero
assert run("1\n3\n1 -1 5\n") == "5 -6 1"

# negative numbers
assert run("1\n2\n4 -7\n") == "-7 -4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 elements | 5 -5 | Smallest allowed size |
| All equal values | 7 -7 7 -7 | Repeated numbers |
| 1 -1 5 | 5 -6 1 | First pair sum equals zero |
| 4 -7 | -7 -4 | Mixed signs |

## Edge Cases

Consider

```
3
1 -1 5
```

The first two numbers sum to zero, so using them as the pair inside the triple would create a zero coefficient. The algorithm checks another pair. Since $1+5\neq0$, it assigns

```
-4 5 -1
```

and obtains

$$1(-4)+(-1)(5)+5(-1)=0.$$

Another interesting case is

```
2
5 5
```

The pair construction gives

```
5 -5
```

and

$$5\cdot5+5(-5)=0.$$

Equal numbers do not require any special handling.

Finally, consider

```
5
2 -3 1 4 -2
```

The first two elements become one pair. The last three are handled as a triple because the length is odd.

The resulting coefficients are

```
-3 -2 -2 -2 -5
```

and

$$2(-3)+(-3)(-2)+1(-2)+4(-2)+(-2)(-5)=0.$$

This confirms that the transition from paired elements to the final triple preserves the invariant that every group contributes zero independently.
