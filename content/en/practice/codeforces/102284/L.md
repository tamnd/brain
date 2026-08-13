---
title: "CF 102284L - \u0412\u044b\u0431\u043e\u0440 \u0432\u0435\u0447\u0451\u0440\u043a\u0438"
description: "There are (n) students, and each student names one of (k) possible drinks. Andrew has exactly (lceil n/2rceil) packages. Each package contains two half-portions, so one package can satisfy at most two students, and both of those students must have requested the same drink."
date: "2026-08-13T09:02:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "L"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 192
verified: true
draft: false
---

[CF 102284L - \u0412\u044b\u0431\u043e\u0440 \u0432\u0435\u0447\u0451\u0440\u043a\u0438](https://codeforces.com/problemset/problem/102284/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) students, and each student names one of (k) possible drinks. Andrew has exactly (\lceil n/2\rceil) packages. Each package contains two half-portions, so one package can satisfy at most two students, and both of those students must have requested the same drink.

Andrew is free to choose which drink every package contains. The goal is not to make every student happy, but to maximize the number of students whose requested drink is actually supplied to them.

Suppose a particular drink was requested by (c) students. To satisfy all of them, Andrew needs (\lceil c/2\rceil) packages of that drink. Two students with the same request can share one package, while a group of odd size needs one package with an unused half.

The central difficulty is that every drink with an odd number of requests consumes one more half-package than its students would suggest. We need to choose which drinks to satisfy so that the total number of required packages does not exceed (\lceil n/2\rceil).

The constraints are small enough that (O(nk)) would already be acceptable, since both (n) and (k) are at most (1000). However, the structure of the problem gives an (O(n+k)) solution. We only need the frequency of every requested drink and then the number of frequencies that are odd.

There are two easy cases where a careless solution can fail. First, an odd number of students does not mean that every odd-sized drink group causes a problem. For example,

```
1 1
1
```

has one student and one package, so the answer is (1). The single half-package left over can simply be taken by Andrew.

The more interesting case is several odd-sized groups. Consider

```
4 4
1
2
3
4
```

Every drink is requested once. There are only two packages, so at most two of the four students can receive their desired drinks. The correct answer is (2). A solution that simply sums all requests would incorrectly claim that all four can be satisfied.

The parity of (n) also matters. For

```
5 3
1
3
1
1
2
```

the request counts are (3,1,1). There are three packages. We can use two packages for drink (1), satisfying three students, and one package for either drink (2) or drink (3), satisfying one more student. The answer is (4), not (3).

## Approaches

A direct brute-force approach is to decide which drink types Andrew will include in the evening selection. For every subset of the (k) drinks, we can calculate how many packages are required. If drink (i) was requested (c_i) times and it is selected, it costs (\lceil c_i/2\rceil) packages and contributes (c_i) satisfied students. We keep the best subset whose package cost is at most (\lceil n/2\rceil).

This brute force is correct because every possible choice of drink types is explicitly considered. The problem is the number of subsets. There are (2^k) of them, and with (k=1000) that is already (2^{1000}) possibilities. Even if the cost of each subset were maintained in constant time, the search would be hopeless. A straightforward implementation that scans all (k) drink types for every subset would perform (O(k2^k)), roughly (1000\cdot2^{1000}), which is far beyond any practical limit.

The useful observation is that every drink group has a very special cost-to-value relationship. If (c) is even, then

[
\left\lceil\frac c2\right\rceil=\frac c2,
]

so satisfying those students costs exactly half as many packages. If (c) is odd, then

[
\left\lceil\frac c2\right\rceil=\frac{c+1}{2}.
]

Thus every odd-sized group introduces exactly one extra package compared with the ideal cost of (c/2).

Let (O) be the number of drink types whose request count is odd. If we tried to satisfy everybody, the required number of packages would be

\frac{n+O}{2}.
]

We only have (\lceil n/2\rceil) packages. The excess is exactly the number of odd groups that must be handled.

Instead of choosing arbitrary subsets, we can think about removing students from the set of satisfied students. Removing one student from an odd-sized group changes that group to even, reducing the number of odd groups by one. Removing another student from the same group would make it odd again, so there is no benefit in doing that while we are trying to fix the package shortage.

For even (n), the number (O) is even. We need to remove (O/2) students, one from each of (O/2) odd groups. For odd (n), (O) is odd, and one odd group can use the single half-package that remains. We only need to remove ((O-1)/2) students.

This gives a direct formula. For even (n), the answer is

[
n-\frac O2.
]

For odd (n), the answer is

[
n-\frac{O-1}{2}.
]

Equivalently, we can compute the number of students that have to be sacrificed as (\lfloor O/2\rfloor), because the parity of (O) is the same as the parity of (n). Thus the answer is simply

[
\boxed{n-\left\lfloor\frac O2\right\rfloor}.
]

The entire problem has now been reduced to counting the frequencies and counting how many of them are odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over drink subsets | (O(k2^k)) | (O(k)) | Too slow |
| Count frequencies and odd groups | (O(n+k)) | (O(k)) | Accepted |

## Algorithm Walkthrough

1. Create an array `cnt` of size (k+1), where `cnt[x]` will store how many students requested drink (x). Counting frequencies is enough because the identities and ordering of students do not affect how packages can be distributed.
2. Read all (n) requests and increment the corresponding frequency. After this step, the whole input is represented by the (k) values (c_1,c_2,\ldots,c_k).
3. Count how many frequencies are odd. Call this number `odd`. Every such group needs one extra half-package compared with an even group of comparable size.
4. Compute `odd // 2`. This is the minimum number of students that must be left unsatisfied. Pairing the odd groups in pairs explains this value: from every pair of odd groups, one student must be removed so that both groups can be handled with the available packages.
5. Output `n - odd // 2`. The parity of (n) already determines whether one odd group can use the single leftover half-package, so no additional special case is needed.

Why it works. Suppose the request counts are (c_1,\ldots,c_k), and (O) of them are odd. If we satisfy every student, the number of required packages is ((n+O)/2). Our budget is (\lceil n/2\rceil), so every pair of odd groups creates exactly one package of excess demand. Removing one student from one group in such a pair makes that group even and removes one unit of excess. Hence at least (\lfloor O/2\rfloor) students must be sacrificed. We can achieve exactly this by choosing one student from one group in every pair of odd groups. After those removals, at most one odd group remains when (n) is odd, which fits into the single partially used package. Thus the lower bound is achievable, and the answer is exactly (n-\lfloor O/2\rfloor).

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    cnt = [0] * (k + 1)

    for _ in range(n):
        drink = int(input())
        cnt[drink] += 1

    odd = sum(c & 1 for c in cnt)

    print(n - odd // 2)

if __name__ == "__main__":
    solve()
```

The array `cnt` stores the frequency of every drink. Since drink numbers are between (1) and (k), direct indexing is simpler and faster than using a dictionary.

The expression `c & 1` checks whether a frequency is odd. It is equivalent to `c % 2`, but makes the parity operation explicit. Summing these values gives exactly the number (O) from the proof.

The final expression `n - odd // 2` handles both parities of (n). When (n) is even, `odd` is necessarily even, so `odd // 2` is exactly the number of students that must be removed. When (n) is odd, `odd` is necessarily odd, and integer division gives ((O-1)/2), leaving one odd group to use the single leftover half-package.

There are no indexing tricks involving the drink numbers beyond allocating `k + 1` elements, so drink (k) is safely represented. Python integers also have no overflow issue for these constraints.

## Worked Examples

For the provided sample, the requests are `1, 3, 1, 1, 2`. The frequencies become (3,1,1), so all three drink types have odd frequencies.

| Drink | Frequency | Odd? |
| --- | --- | --- |
| 1 | 3 | yes |
| 2 | 1 | yes |
| 3 | 1 | yes |
| Total odd groups | 3 |  |

Since `odd = 3`, we need to leave `3 // 2 = 1` student unsatisfied. The result is (5-1=4).

Concretely, two packages of drink (1) can satisfy the three students requesting drink (1), because one package serves two of them and the second package serves the remaining one. The third package can satisfy either the student requesting drink (2) or the student requesting drink (3). Four students can consequently receive what they requested.

For a second example, consider four students who all request different drinks.

```
4 4
1
2
3
4
```

The frequency trace is:

| Drink | Frequency | Odd? |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 1 | yes |
| 3 | 1 | yes |
| 4 | 1 | yes |
| Total odd groups | 4 |  |

Here `odd // 2` equals (2), so the answer is (4-2=2). There are only two packages, and each singleton request needs its own package. Choosing any two drink types satisfies exactly two students.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+k)) | Read and count (n) requests, then inspect (k+1) frequencies |
| Space | (O(k)) | Store one frequency for every drink |

With (n,k\le1000), this performs only a few thousand basic operations. The solution is comfortably within the stated constraints and uses very little memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    k = next(it)

    cnt = [0] * (k + 1)

    for _ in range(n):
        x = next(it)
        cnt[x] += 1

    odd = sum(c & 1 for c in cnt)

    return str(n - odd // 2)

# provided sample
assert solve_data(
    """5 3
1
3
1
1
2
"""
) == "4", "sample 1"

# minimum-size input
assert solve_data(
    """1 1
1
"""
) == "1", "single student"

# all students want the same drink
assert solve_data(
    """6 3
2
2
2
2
2
2
"""
) == "6", "all equal"

# even n, every drink requested once
assert solve_data(
    """4 4
1
2
3
4
"""
) == "2", "four odd groups"

# odd n, three odd groups
assert solve_data(
    """5 3
1
2
3
1
1
"""
) == "4", "odd n with three odd groups"

# maximum-size input, all students request one drink
max_case = "1000 1000\n" + "1\n" * 1000
assert solve_data(max_case) == "1000", "maximum n and k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Minimum size and the single leftover half-package |
| `6 3 / 2 2 2 2 2 2` | `6` | All requests are equal, so there is no package waste |
| `4 4 / 1 2 3 4` | `2` | Several odd groups and the even-(n) boundary |
| `5 3 / 1 2 3 1 1` | `4` | Odd (n), where one odd group can use the leftover half |
| `n=1000`, all requests equal | `1000` | Maximum input size and frequency counting |

## Edge Cases

The smallest possible input is

```
1 1
1
```

There is one package and one student. The student receives half of the package, while Andrew keeps the other half. The only frequency is (1), so `odd = 1` and `odd // 2 = 0`. The algorithm outputs (1), which is optimal.

When all students request the same drink, there is only one frequency and it is odd exactly when (n) is odd. For example,

```
5 2
1
1
1
1
1
```

gives `odd = 1`, so the answer is (5). Two packages can serve four students completely, and a third package can serve the fifth student, with its other half remaining for Andrew.

The case with many odd groups is where the main formula matters. For

```
6 6
1
2
3
4
5
6
```

all six frequencies are odd, so `odd = 6`. The answer is (6-6/2=3). There are three packages, and each satisfied singleton request needs one package. Choosing three of the six drinks satisfies three students.

Finally, the odd-(n) boundary is different from the even-(n) case. For

```
5 3
1
2
3
1
1
```

the frequencies are (3,1,1), giving `odd = 3`. The algorithm removes only `3 // 2 = 1` student and returns (4). The reason is that after satisfying the three students requesting drink (1), one additional package can satisfy either singleton request. The remaining singleton is exactly the one student that cannot be satisfied. The one unused half of the final package is Andrew's, as allowed when the number of students is odd.
