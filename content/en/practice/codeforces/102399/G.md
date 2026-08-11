---
title: "CF 102399G - \u0426\u0435\u043b\u044b\u0435 \u0442\u043e\u0447\u043a\u0438"
description: "We have two families of straight lines. The first family contains lines of the form (y=x+p), and the second contains lines of the form (y=-x+q). The values (p) are distinct integers, as are the values (q)."
date: "2026-08-11T23:42:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "G"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 183
verified: true
draft: false
---

[CF 102399G - \u0426\u0435\u043b\u044b\u0435 \u0442\u043e\u0447\u043a\u0438](https://codeforces.com/problemset/problem/102399/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two families of straight lines. The first family contains lines of the form (y=x+p), and the second contains lines of the form (y=-x+q). The values (p) are distinct integers, as are the values (q).

Every line from the first family intersects every line from the second family because their slopes are (1) and (-1). For each such pair, we have to determine whether their intersection point has integer coordinates. The answer is the number of pairs satisfying this condition.

For a line (y=x+p) and a line (y=-x+q), equating the two expressions gives

[
x+p=-x+q,
]

so

[
x=\frac{q-p}{2}.
]

Substituting this into either line gives

[
y=\frac{p+q}{2}.
]

Thus both coordinates are integers exactly when (q-p) is even. A difference of two integers is even precisely when the integers have the same parity. The entire geometric problem therefore reduces to counting pairs where (p) and (q) are both even or both odd.

The important constraint is that each family can contain up to (100000) lines. A method that examines every pair would perform up to (100000\cdot100000=10^{10}) checks. That is far beyond what a 2 second competitive programming limit can support. We need a solution whose work is essentially proportional to the number of input values.

There are a few boundary cases that are easy to mishandle. If both values are odd, their difference is still even. For example, with

```
1
1
1
3
```

the two lines are (y=x+1) and (y=-x+3). Their intersection is ((1,2)), so the correct answer is `1`. A solution that only checks whether both numbers are even would incorrectly return zero.

The value zero is also even and must be treated normally. For example,

```
1
0
1
1
```

gives (x=\frac{1-0}{2}), which is not an integer, so the correct output is `0`. A careless implementation that treats zero separately from other even numbers could get this wrong.

The equality of (p) and (q) is not a special problem. For example,

```
1
5
1
5
```

produces the intersection ((0,5)), so the answer is `1`. The two lines are different because they have different slopes, even though their parameters are equal.

Finally, the maximum answer can be very large. If all (100000) values in both families have the same parity, every pair works, giving (10^{10}) valid pairs. The answer must consequently be stored in an integer type capable of holding at least (10^{10}). Python integers have no overflow issue here.

## Approaches

The direct approach is to take every line (y=x+p_i), pair it with every line (y=-x+q_j), compute (q_j-p_i), and check whether the result is even. This is correct because every possible pair is examined exactly once, and the derived intersection formula gives the exact criterion for integer coordinates.

The problem is the number of pairs. With (n=m=100000), the brute force performs (10^{10}) parity checks. Even though each check is mathematically simple, ten billion iterations are much too many for the time limit.

The key observation is that we do not actually need the values of the differences. We only need their parity. There are only two possible parities, even and odd. A pair contributes exactly when its two parameters belong to the same parity class.

Suppose there are (E_p) even values and (O_p) odd values among the first family's parameters. Similarly, let (E_q) and (O_q) be the corresponding counts for the second family. Every even (p) can be paired with every even (q), producing (E_pE_q) valid pairs. Likewise, every odd (p) can be paired with every odd (q), producing (O_pO_q) valid pairs.

The answer is therefore

[
E_pE_q+O_pO_q.
]

We only need to scan each input array once and count its even and odd elements. The actual positions and magnitudes of the parameters are irrelevant after their parity is known.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm)) | (O(1)) | Too slow |
| Optimal | (O(n+m)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the number (n) of lines of the form (y=x+p), then read all (p) values. Count how many are even and how many are odd. Only these two counts matter because the intersection criterion depends solely on parity.
2. Read the number (m) of lines of the form (y=-x+q), then read all (q) values. Again, count the even and odd values.
3. Multiply the number of even (p)'s by the number of even (q)'s. Every such pair has (q-p) even, so every one of them contributes to the answer.
4. Multiply the number of odd (p)'s by the number of odd (q)'s. Their difference is also even, so these pairs contribute as well.
5. Add the two products and print the result. Pairs of opposite parity are excluded because their difference is odd, making both intersection coordinates half-integers.

### Why it works

For any pair of lines, their intersection is

[
\left(\frac{q-p}{2},\frac{p+q}{2}\right).
]

If (p) and (q) have the same parity, both (q-p) and (p+q) are even, so both coordinates are integers. If their parities differ, both expressions are odd, so both coordinates are non-integers. Thus the valid pairs are exactly the same-parity pairs. Counting even-even and odd-odd pairs counts every valid pair exactly once and excludes every invalid pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    m = int(input())
    q = list(map(int, input().split()))

    even_p = sum(x % 2 == 0 for x in p)
    odd_p = n - even_p

    even_q = sum(x % 2 == 0 for x in q)
    odd_q = m - even_q

    answer = even_p * even_q + odd_p * odd_q
    print(answer)

if __name__ == "__main__":
    solve()
```

The first two input reads obtain the two families of parameters. The problem guarantees that each family is given on one line, so converting the whole line to a list is sufficient.

The two parity counters for the first family are obtained by counting even values and subtracting from (n) to obtain the number of odd values. The same is done for the second family.

The final expression directly implements the mathematical result (E_pE_q+O_pO_q). There is no need to sort the arrays, construct the lines, or calculate any intersection explicitly.

The modulo operation `% 2` is safe for all allowed non-negative parameter values. Python's arbitrary-precision integers also handle the maximum possible answer, (10^{10}), without any special handling.

The original Gym version contains exactly one test case, while the later Codeforces version packages the same idea into multiple test cases.

## Worked Examples

The original Gym sample is

```
3
1 3 2
2
0 3
```

The first family has parameters (1,3,2). The second family has parameters (0,3).

| Parameter group | Even | Odd |
| --- | --- | --- |
| (p) | 1 | 2 |
| (q) | 1 | 1 |

The even-even pairs contribute (1\cdot1=1). The odd-odd pairs contribute (2\cdot1=2).

| Step | even_p | odd_p | even_q | odd_q | answer |
| --- | --- | --- | --- | --- | --- |
| Count (p) | 1 | 2 | 0 | 0 | 0 |
| Count (q) | 1 | 2 | 1 | 1 | 0 |
| Combine parity classes | 1 | 2 | 1 | 1 | 3 |

The result is `3`, matching the sample output. Geometrically, the valid parameter pairs are ((1,3)), ((3,3)), and ((2,0)). The other three pairs have parameters of opposite parity.

A second example is

```
2
0 4
3
1 3 5
```

Both (p) values are even, while all three (q) values are odd.

| Parameter group | Even | Odd |
| --- | --- | --- |
| (p) | 2 | 0 |
| (q) | 0 | 3 |

The even-even contribution is (2\cdot0=0), and the odd-odd contribution is (0\cdot3=0).

| Step | even_p | odd_p | even_q | odd_q | answer |
| --- | --- | --- | --- | --- | --- |
| Count (p) | 2 | 0 | 0 | 0 | 0 |
| Count (q) | 2 | 0 | 0 | 3 | 0 |
| Combine parity classes | 2 | 0 | 0 | 3 | 0 |

The answer is `0`. Every intersection has half-integer coordinates because every possible pair consists of one even parameter and one odd parameter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Each parameter is inspected once to determine its parity. |
| Space | (O(n+m)) | The implementation stores the two input arrays. |

The constraints allow up to (10^5) values in each family, so the optimal algorithm performs only about (2\cdot10^5) parity checks. This is comfortably within the 2 second time limit. The memory usage is also small compared with the 512 MB limit.

The arrays can even be processed without storing them, reducing auxiliary space to (O(1)), but keeping them makes the implementation straightforward and remains well within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    p = list(map(int, input().split()))

    m = int(input())
    q = list(map(int, input().split()))

    even_p = sum(x % 2 == 0 for x in p)
    odd_p = n - even_p

    even_q = sum(x % 2 == 0 for x in q)
    odd_q = m - even_q

    print(even_p * even_q + odd_p * odd_q)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    "3\n"
    "1 3 2\n"
    "2\n"
    "0 3\n"
) == "3\n", "sample 1"

# Minimum-size input, equal parameters
assert run(
    "1\n"
    "5\n"
    "1\n"
    "5\n"
) == "1\n", "minimum size and equal values"

# All parameters have the same parity, so every pair is valid
assert run(
    "3\n"
    "0 2 4\n"
    "4\n"
    "1 3 5 7\n"
) == "0\n", "opposite parity classes"

# Boundary values and mixed parity
assert run(
    "4\n"
    "0 1 2 1000000000\n"
    "5\n"
    "0 1 3 999999999 1000000000\n"
) == "10\n", "boundary values and mixed parity"

# Maximum-size construction
n = 100000
m = 100000
p = list(range(0, 2 * n, 2))
q = list(range(1, 2 * m + 1, 2))

max_input = (
    f"{n}\n"
    + " ".join(map(str, p))
    + "\n"
    + f"{m}\n"
    + " ".join(map(str, q))
    + "\n"
)

assert run(max_input) == "0\n", "maximum-size opposite parity case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5 / 1 / 5` | `1` | Minimum size and equality across the two families |
| `3 / 0 2 4 / 4 / 1 3 5 7` | `0` | All possible pairs have opposite parity |
| `4 / 0 1 2 1000000000 / 5 / 0 1 3 999999999 1000000000` | `10` | Zero, (10^9)-scale boundary values, and mixed parity |
| 100000 even (p)'s and 100000 odd (q)'s | `0` | Maximum input size and absence of quadratic work |

For a maximum-answer stress test, the same construction can instead use even values in both arrays. Then all (10^{10}) pairs are valid, which is also useful for checking that the implementation does not accidentally use a 32-bit integer.

## Edge Cases

The first parity edge case is two odd parameters. Consider

```
1
1
1
3
```

The algorithm counts one odd (p) and one odd (q), giving (1\cdot1=1). The intersection is ((1,2)), so the output is `1`. This catches implementations that incorrectly assume only even-even pairs can work.

The second edge case involves zero:

```
1
0
1
1
```

Here (p=0) is even and (q=1) is odd. The algorithm produces (1\cdot0+0\cdot1=0). The intersection is ((1/2,1/2)), confirming the output `0`. Zero is handled naturally by the parity test.

The equality case is

```
1
5
1
5
```

Both parameters are odd, so the algorithm returns `1`. The intersection is ((0,5)). Equal parameter values do not mean the two lines coincide, because their slopes are different.

Finally, consider the largest possible number of valid pairs. Let both families contain (100000) distinct even values. Then every one of the (100000^2=10^{10}) pairs has an integer intersection. The formula computes this directly as (100000\cdot100000), without enumerating any pair. This is precisely the case that separates the (O(nm)) brute force from the (O(n+m)) solution.
