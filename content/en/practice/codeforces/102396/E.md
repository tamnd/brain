---
title: "CF 102396E - Unique Solution"
description: "We are given a nonzero ternary vector a, where every a i ​ is −1, 0, or 1. We have to construct another integer array x and a modulus m such that, among all nonzero ternary vectors c, the divisibility condition i=1 ∑ n ​ c i ​ x i ​ ≡0(modm) holds for exactly two vectors, namely…"
date: "2026-08-12T05:42:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "E"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 886
verified: false
draft: false
---

[CF 102396E - Unique Solution](https://codeforces.com/problemset/problem/102396/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a nonzero ternary vector a, where every a i ​ is −1, 0, or 1. We have to construct another integer array x and a modulus m such that, among all nonzero ternary vectors c, the divisibility condition

i=1 ∑ n ​ c i ​ x i ​ ≡0(modm)

holds for exactly two vectors, namely the prescribed vector a and its negation −a. The construction itself is the answer, so there is no input modulus or array x to process.

The restriction n≤30 is the central numerical constraint. It allows powers of two up to 2 29, which still fit strictly below the required 2 30 bound for every x i ​. At the same time, the modulus must be smaller than 2 n, so a construction based on the binary number 2 n −1 is especially natural. Brute-forcing all ternary vectors would require 3 n −1 candidates, which is about 2.06×10 14 candidates when n=30. Even checking each candidate in constant time would be hopeless, and checking its dot product in O(n) is worse.

There are two edge cases that a careless construction can mishandle. For example, with

```
1
1
```

the only nonzero ternary vectors are 1 and −1, so m=1, x 1 ​ =1 is already valid. A construction that insists on m>1 would unnecessarily fail here.

Zeros in the target vector are more subtle. For

```
2
1 0
```

we must distinguish (1,0) from (1,1) and (1,−1). Simply setting x i ​ =a i ​ 2 i gives x 2 ​ =0, which makes every choice of the second coefficient irrelevant and creates many unwanted solutions. The construction must give zero positions their own weights while still preventing them from participating in a divisible sum.

The official problem allows any valid construction, not necessarily the sample construction.

## Approaches

A direct approach would enumerate every vector c∈{−1,0,1} n except the all-zero vector, compute ∑c i ​ x i ​, and test divisibility by m. There are exactly 3 n −1 such vectors. For n=30, this is roughly 2.06×10 14 possibilities, so brute force is completely infeasible.

The useful observation is that we do not actually need to search for x. The coefficient set {−1,0,1} interacts very cleanly with powers of two. If we give the coordinates weights 1,2,4,…, every signed sum has a rigid binary structure. In particular, the only way to obtain 2 k −1 using coefficients from {−1,0,1} on the weights 1,2,…,2 k−1 is to use every coefficient as +1, and the only way to obtain its negative is to use every coefficient as −1.

The remaining difficulty is that some target coefficients may be zero. The trick is to separate zero positions from nonzero positions by magnitude. Give all zero positions the smallest powers of two, and give all nonzero positions the larger powers. Then the target vector uses exactly all of the larger weights, so its dot product becomes a carefully chosen modulus.

Let z be the number of zero entries and k=n−z the number of nonzero entries. Assign the zero positions the weights

1,2,…,2 z−1 ,

and assign the nonzero positions

2 z ,2 z+1 ,…,2 n−1 .

For a nonzero target entry, multiply its assigned weight by a i ​, so the target signs are built directly into x i ​. For a zero target entry, use the assigned positive weight.

The target dot product is then

a i ​  =0 ∑ ​ a i ​ (a i ​ 2 j )= j=z ∑ n−1 ​ 2 j =2 n −2 z .

We choose exactly this value as m. It is positive because k≥1, and it is smaller than 2 n, as required.

The construction works because the total absolute value of any ternary combination is at most

1+2+⋯+2 n−1 =2 n −1.

Our modulus satisfies m≥2 n−1, so the only possible multiples of m in this range are 0, m, and −m. The low z bits then force every zero-position coefficient to vanish, after which the remaining problem reduces to the unique binary representation of 2 k −1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n3 n ) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count how many entries of the target vector are zero. Let this number be z. The other k=n−z entries are nonzero, and k≥1.
2. Set

m=2 n −2 z .

This is exactly the sum of the powers 2 z ,2 z+1 ,…,2 n−1, which will be the weights assigned to the nonzero target positions. Since k≥1, we have m≥1, and clearly m<2 n.

1. Traverse the target array. For every zero entry, assign the next unused low power of two, starting from 1. Thus the zero positions receive 2 0 ,2 1 ,…,2 z−1.
2. For every nonzero entry a i ​, assign the next unused high power of two and multiply it by a i ​. Thus a target value 1 gets a positive weight and a target value −1 gets the corresponding negative weight.
3. The resulting target dot product is exactly m. Its negation has dot product −m, so both prescribed solutions are valid.
4. Consider any nonzero ternary vector c satisfying the divisibility condition. Its absolute dot product is at most 2 n −1, while m≥2 n−1. Hence its dot product must be one of 0,m,−m.
5. If the dot product is zero, look at the largest power of two whose coefficient is nonzero. That power is strictly larger than the sum of all smaller powers, so cancellation is impossible. Thus every coefficient must be zero, contradicting the requirement that c be nonzero.
6. Suppose the dot product is m or −m. Reduce the equation modulo 2 z. Every high weight is divisible by 2 z, while the zero-position weights are exactly 1,2,…,2 z−1. Their signed sum has absolute value below 2 z, so it must actually equal zero. The uniqueness of signed binary representation forces every coefficient on a zero target position to be zero.
7. After removing those zero positions and dividing the remaining equation by 2 z, the weights become 1,2,…,2 k−1, and the required absolute sum is 2 k −1. The only possible ternary representation is all +1, or all −1, depending on the sign of the original sum. Undoing the signs stored in x i ​, the only solutions are a and −a.

### Why it works

The key invariant is that the low powers of two belong exclusively to coordinates where the desired answer is zero, while every nonzero target coordinate receives a multiple of 2 z. Any divisible combination must first have its low part equal to zero, forcing all zero-target coefficients to disappear. The remaining high powers form a complete binary sequence whose only ternary representations of 2 k −1 and −(2 k −1) are the all-positive and all-negative choices. The signs stored in x i ​ convert those choices exactly into a and −a.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    z = a.count(0)

    # Sum of powers 2^z, ..., 2^(n-1).
    m = (1 << n) - (1 << z)

    x = [0] * n

    low_power = 0
    high_power = z

    for i in range(n):
        if a[i] == 0:
            x[i] = 1 << low_power
            low_power += 1
        else:
            x[i] = a[i] * (1 << high_power)
            high_power += 1

    print(m)
    print(*x)

if __name__ == "__main__":
    solve()
```

The first line of `solve` reads the target vector, and `z` records how many coordinates must eventually have coefficient zero. This count determines where the boundary between low and high powers of two lies.

The modulus is computed as `(1 << n) - (1 << z)`. This is the sum of every power from 2 z through 2 n−1, so it is exactly the absolute dot product obtained by the desired vector.

The two counters have different roles. `low_power` starts at zero and is used only for target zeros. `high_power` starts at `z` and is used only for nonzero target entries. Consequently, the two groups occupy disjoint ranges of binary positions.

For a nonzero `a[i]`, the expression `a[i] * (1 << high_power)` stores the desired sign directly into `x[i]`. If the target coefficient is −1, the corresponding `x[i]` is negative. When the student chooses the target coefficient −1, their product with `x[i]` is positive, contributing the required power of two to the target sum.

The largest assigned absolute value is 2 n−1. Since n≤30, it is at most 2 29, strictly below 2 30. Python integers also have arbitrary precision, so there is no overflow issue.

There is no multiple-test-case loop because the original input contains exactly one instance. The construction uses only integer shifts and one linear pass through the array.

## Worked Examples

### Example 1

Consider the provided sample.

```
2
1 -1
```

There are no zero entries, so z=0. The modulus is

m=2 2 −2 0 =3.

The two target entries receive weights 1 and 2, with their signs included in x.

| Index | a i ​ | Power | x i ​ |
| --- | --- | --- | --- |
| 1 | 1 | 2 0 =1 | 1 |
| 2 | -1 | 2 1 =2 | -2 |

The target gives

1⋅1+(−1)⋅(−2)=3,

so it is divisible by 3. Its negation gives −3.

Any nonzero ternary combination has absolute value at most 1+2=3. The only possible divisible values are 0,±3. Zero has only the all-zero representation, while 3 and −3 have only the all-positive and all-negative representations. Thus the only solutions are (1,−1) and (−1,1).

The sample output uses a different valid choice, x=(1,4), but the problem accepts any valid construction.

### Example 2

Consider the custom input

```
3
1 0 -1
```

There is one zero, so z=1. The modulus is

m=2 3 −2 1 =6.

The zero position gets 2 0 =1, while the nonzero positions get 2 1 =2 and 2 2 =4.

| Index | a i ​ | Assigned power | x i ​ |
| --- | --- | --- | --- |
| 1 | 1 | 2 1 =2 | 2 |
| 2 | 0 | 2 0 =1 | 1 |
| 3 | -1 | 2 2 =4 | -4 |

For the target,

1⋅2+0⋅1+(−1)⋅(−4)=6.

The negation gives −6.

Now consider any other ternary vector. Its absolute dot product is at most 1+2+4=7, so a divisible value can only be 0,±6. A zero value is impossible for a nonzero vector because powers of two have unique signed representations.

For 6, reducing modulo 2 immediately forces the coefficient of the weight 1 to be zero. The remaining equation is 2u+4v=6, or u+2v=3, whose only ternary solution is u=v=1. This recovers exactly (1,0,−1).

The trace demonstrates why zero coordinates cannot simply be assigned weight zero. They need the low binary weights so that divisibility itself forces their student coefficients to vanish.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The array is scanned once and every operation is constant time. |
| Space | O(n) | The input and constructed array both contain n integers. |

With n≤30, the algorithm performs only a few dozen arithmetic operations and stays far below the one-second time limit. Every output value also satisfies the required bounds because all absolute values are powers of two below 2 30, while m=2 n −2 z <2 n.

## Test Cases

The test harness below does not compare against one fixed output, because this is a constructive problem and many different outputs are valid. Instead, it runs the construction and independently checks that exactly the two required ternary vectors satisfy the produced congruence.

```python
import sys
import io
from itertools import product

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    z = a.count(0)
    m = (1 << n) - (1 << z)

    x = [0] * n
    low_power = 0
    high_power = z

    for i in range(n):
        if a[i] == 0:
            x[i] = 1 << low_power
            low_power += 1
        else:
            x[i] = a[i] * (1 << high_power)
            high_power += 1

    print(m)
    print(*x)

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

def validate(inp: str) -> str:
    out = solution(inp).split()
    data = list(map(int, out))

    n = int(inp.split()[0])
    a = list(map(int, inp.split()[1:n + 1]))

    m = data[0]
    x = data[1:]

    assert len(x) == n
    assert 1 <= m < (1 << n)
    assert all(-(1 << 30) < v < (1 << 30) for v in x)

    found = []

    for c in product((-1, 0, 1), repeat=n):
        if all(v == 0 for v in c):
            continue

        s = sum(c[i] * x[i] for i in range(n))
        if s % m == 0:
            found.append(c)

    expected = {tuple(a), tuple(-v for v in a)}
    assert set(found) == expected

    return out

# Provided sample
validate("""\
2
1 -1
""")

# Minimum-size input
validate("""\
1
1
""")

# A zero coordinate, catching constructions that accidentally set x_i = 0
validate("""\
2
1 0
""")

# Mixed signs and zeros
validate("""\
6
0 -1 1 0 1 -1
""")

# Maximum-size input
validate("30\n" + " ".join(["1"] * 30) + "\n")

# All nonzero values with mixed signs
validate("""\
8
1 -1 1 -1 -1 1 -1 1
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 -1` | Any valid construction | Provided sample and mixed signs |
| `1 / 1` | `m=1`, `x_1=1` is valid | Minimum size and modulus boundary |
| `2 / 1 0` | Any valid construction, such as `m=2, x=(2,1)` | Zero-coordinate handling |
| `6 / 0 -1 1 0 1 -1` | Any valid construction | Separation of low and high powers |
| `30 / 1 1 ... 1` | Any valid construction | Maximum n and largest power 2 29 |
| `8 / 1 -1 1 -1 -1 1 -1 1` | Any valid construction | Sign handling across many coordinates |

## Edge Cases

For the minimum case

```
1
1
```

we have z=0, so m=2 1 −1=1 and x 1 ​ =1. Both possible nonzero choices, 1 and −1, have sums divisible by 1, and there are no other nonzero ternary vectors. The construction deliberately permits m=1, which is legal.

For a target containing zeros, consider

```
2
1 0
```

Here z=1, so m=4−2=2. The zero position receives weight 1, and the nonzero position receives weight 2, giving

```
2
2 1
```

The target has sum 2, while its negation has sum −2. A vector using the zero position has a contribution of ±1, so it cannot be divisible by 2 unless another contribution cancels it. The only other available weight is 2, which cannot cancel an odd contribution. Thus the zero coefficient is forced to remain zero.

For a target with several zeros, consider

```
4
0 0 1 -1
```

There are z=2 zeros, so

m=2 4 −2 2 =12.

The zero positions receive 1 and 2, while the nonzero positions receive 4 and 8, with the sign of the last weight reversed:

```
12
1 2 4 -8
```

Any divisible sum must lie between −15 and 15, so it can only be 0,±12. Modulo 4, the low part is a combination of 1 and 2 whose absolute value is at most 3, so it must be exactly zero. The coefficients of both low weights are consequently zero. The remaining equation is based on weights 4 and 8, and only the required signs can produce 12 or −12.

At the maximum size n=30, the largest weight is 2 29 =536870912, which is safely below 2 30. The modulus is at most 2 30 −1, so both output restrictions remain satisfied exactly at the boundary.

The all-nonzero case is also worth checking because then z=0. The construction reduces to the cleanest form, with weights 1,2,4,…,2 n−1 and modulus 2 n −1. The signs of the target vector are placed directly into x i ​, so the only two divisible ternary vectors are the prescribed vector and its negation.
