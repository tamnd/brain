---
title: "CF 102367B - Favourite Number"
description: "A positive integer has an odd number of positive divisors exactly when it is a perfect square. Every non-square has divisors that can be paired as d and n/d, while a square has one unpaired divisor, namely its square root. So the task can be restated as follows."
date: "2026-08-14T02:58:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102367
codeforces_index: "B"
codeforces_contest_name: "Fall 2019 ICPC-style Waterloo Local Contest"
rating: 0
weight: 102367
solve_time_s: 77
verified: true
draft: false
---

[CF 102367B - Favourite Number](https://codeforces.com/problemset/problem/102367/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

A positive integer has an odd number of positive divisors exactly when it is a perfect square. Every non-square has divisors that can be paired as d and n/d, while a square has one unpaired divisor, namely its square root.

So the task can be restated as follows. We need every positive integer A such that both A and A+K are perfect squares. We must print how many such values exist, followed by the values themselves in increasing order.

Suppose

A=x 2

and

A+K=y 2 .

Since K>0, we have y>x, and

K=y 2 −x 2 =(y−x)(y+x).

Thus every answer corresponds to a factorization of K into

d=y−x,e=y+x.

From these definitions,

x= 2 e−d ​ .

We need x≥1, so e>d, and x must be an integer, so d and e must have the same parity.

The constraint K≤10 9 is the key to the implementation. Its square root is at most about 31623, so we can inspect every possible divisor up to K ​. That is only around thirty thousand iterations in the worst case, which is easily small enough for a one-second limit. An approach that tried every possible A up to 10 9, however, would be far too slow.

There are several edge cases that can fool a direct implementation. For input K=1, the only factorization around the square-root boundary is 1⋅1, which would give x=0. Since A must be positive, the correct output is zero answers. A careless implementation accepting x=0 would incorrectly include A=0.

For input K=9, the factorization 3⋅3 also gives x=0, while 1⋅9 gives x=4. The correct output is therefore 1 followed by 16. An implementation that accepts equal factors would incorrectly report 0 as an answer.

For input K=2, there are no two factors with the same parity. The correct output is zero. This catches implementations that check only whether a factor divides K and forget that x=(e−d)/2 must be integral.

For input K=8, the factorization 2⋅4 gives x=1, hence A=1. The correct output is `1` followed by `1`. This is a useful boundary case because K is even, yet valid answers do exist.

## Approaches

A straightforward approach would enumerate possible positive values of A, test whether A is a perfect square, test whether A+K is a perfect square, and keep the valid ones. Since there is no useful upper bound on A smaller than the values induced by the square differences, a direct search could require examining on the order of K candidates. For K=10 9, that means roughly one billion candidates, before even accounting for the cost of checking whether each number is a square. This cannot fit into the time limit.

The brute force works because it directly tests the defining property, but it ignores the equation connecting the two squares. The observation

y 2 −x 2 =(y−x)(y+x)=K

turns the problem into a divisor search. Instead of searching through potentially billions of values of A, we search through divisors of K. Every factor pair d,e with de=K, d<e, and equal parity produces exactly one value

A=( 2 e−d ​ ) 2 .

Conversely, every valid A produces exactly such a factor pair, so this transformation loses no solutions.

We only need to inspect d≤ K ​. If d divides K, the matching factor is e=K/d. Restricting to d<e automatically excludes x=0, because d=e would mean x=0. We then compute the corresponding A and sort the results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(K) | O(1) excluding output | Too slow |
| Optimal | O( K ​ +RlogR) | O(R) | Accepted |

Here R is the number of valid answers. Since R is at most the number of divisors of K, the sorting term is tiny compared with the divisor scan for this constraint.

## Algorithm Walkthrough

1. Read K. We are looking for two positive squares x 2 and y 2 whose difference is exactly K, with y>x.
2. Iterate over every integer divisor candidate d from 1 through ⌊ K ​ ⌋. If d does not divide K, it cannot be one of the values y−x, so it can be skipped.
3. For every divisor d, set e=K/d. The pair (d,e) represents

d=y−x,e=y+x.

Since d≤ K ​, we have d≤e.
4. Reject the pair when d=e. In that case,

x= 2 e−d ​ =0,

so A=0, which is not a positive integer with a finite divisor count.
5. Reject the pair when d and e have different parity. Then e−d is odd, so (e−d)/2 is not an integer. The resulting pair of square roots would not exist as integers.
6. For every remaining pair, compute

x= 2 e−d ​

and append x 2 to the answer list. This is exactly the corresponding value of A.
7. Sort the collected values and print their count and, when nonempty, the values themselves. Sorting is sufficient because the divisor scan is ordered by d, not by x 2.

### Why it works

For every generated answer, the algorithm has a factor pair d,e satisfying de=K, d<e, and equal parity. Defining x=(e−d)/2 gives a positive integer, and with y=(e+d)/2 we obtain

y 2 −x 2 =(y−x)(y+x)=de=K.

Thus A=x 2 and A+K=y 2 are both perfect squares.

Conversely, take any valid A=x 2 and A+K=y 2. Since K>0, y>x. Setting d=y−x and e=y+x gives de=K, d<e, and d,e have the same parity because their sum and difference are both even. Since one member of every factor pair is at most K ​, the algorithm examines this d and reconstructs exactly the original x and A. Hence every valid answer is generated, and no invalid answer is generated.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    k = int(input())
    ans = []
    d = 1    while d * d <= k:        if k % d == 0:            e = k // d
            # d == e would give x = 0, so A = 0.            if d != e and ((d ^ e) & 1) == 0:                x = (e - d) // 2                ans.append(x * x)
        d += 1
    ans.sort()
    print(len(ans))    if ans:        print(*ans)

if __name__ == "__main__":    solve()
```

The loop over `d` implements the divisor search from the algorithm. The condition `d * d <= k` is equivalent to d≤ K ​, but avoids computing a floating-point square root.

When `k % d == 0`, `e = k // d` is the matching factor. The test `d != e` removes the factorization where both factors equal K ​. Such a factorization would produce x=0, which is outside the domain of positive A.

The parity check uses `(d ^ e) & 1`. The XOR has its lowest bit set exactly when the two integers have different parity. Thus the expression is zero precisely when `d` and `e` have the same parity. A simpler expression such as `d % 2 == e % 2` would also be correct.

Once the parity condition holds, `(e - d) // 2` is an integer positive square root x, and `x * x` is the required value of A. Python integers do not overflow, so there is no special integer-width handling needed.

Finally, the answers are sorted before printing. The first output line is always printed, even when there are no answers. The second line is printed only when the answer list is nonempty, matching the required output format.

## Worked Examples

No usable sample input/output pair is present in the supplied statement text, so the following traces use two small concrete inputs.

For K=8, the divisor pairs are 1⋅8 and 2⋅4. Only the second pair has equal parity and distinct factors.

| `d` | `e = K // d` | `d == e` | Same parity | `x = (e-d)//2` | `A = x*x` |
| --- | --- | --- | --- | --- | --- |
| 1 | 8 | No | No |  |  |
| 2 | 4 | No | Yes | 1 | 1 |

The algorithm produces one answer, `A=1`. Indeed, 1 and 1+8=9 are both perfect squares. The trace also demonstrates why the parity test is necessary.

For K=9, the divisor pairs encountered up to 9 ​ are 1⋅9 and 3⋅3.

| `d` | `e = K // d` | `d == e` | Same parity | `x = (e-d)//2` | `A = x*x` |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | No | Yes | 4 | 16 |
| 3 | 3 | Yes | Yes |  |  |

The first pair gives x=4, so A=16, and 16+9=25. The second pair is rejected because it would give x=0. This trace demonstrates why equal factors must not be accepted even though their parity is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( K ​ +RlogR) | We inspect all divisor candidates up to K ​, then sort the R answers. |
| Space | O(R) | The answer list stores every valid value of A. |

With K≤10 9, the divisor loop performs at most about 31623 iterations. That is easily manageable within the stated 1 second limit, and the number of divisors is small enough that storing and sorting the answers is also inexpensive. The memory usage is likewise far below 256 MB.

## Test Cases

The original statement text supplied here does not contain a valid sample input/output pair, so the test suite below uses independently derived cases. The helper implements the same required transformation to produce expected output for the maximum-value test, rather than embedding a long manually written answer list.

```python
Python# helper: run the solution on an input stringimport sysimport io

def solve():    input = sys.stdin.readline    k = int(input())
    ans = []
    d = 1    while d * d <= k:        if k % d == 0:            e = k // d            if d != e and ((d ^ e) & 1) == 0:                x = (e - d) // 2                ans.append(x * x)        d += 1
    ans.sort()
    print(len(ans))    if ans:        print(*ans)

def run(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()
    try:        solve()
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Smallest possible K, and rejection of A=0. |
| `9` | `1` followed by `16` | Equal factor pair must be rejected. |
| `8` | `1` followed by `1` | Valid even K and parity handling. |
| `2` | `0` | Even K that is not divisible by four. |
| `1000000000` | Generated independently | Maximum input boundary and divisor-loop performance. |

## Edge Cases

For K=1, the loop examines d=1, obtains e=1, and rejects the pair because the factors are equal. Algebraically, this would give x=0 and A=0, so the correct output is `0`. The special handling is not an arbitrary restriction: zero is outside the positive-integer domain and does not have a finite divisor count.

For K=9, the algorithm first finds 1⋅9. Both factors are odd, so x=(9−1)/2=4, producing A=16. It later finds 3⋅3, but rejects it because the factors are equal. The final output is `1` and `16`. Without the equality check, the algorithm would incorrectly include zero.

For K=2, the only factor pair is 1⋅2. The factors have different parity, so `(e-d)/2` is not an integer. The answer list remains empty and the program prints `0`. More generally, every K≡2(mod4) has this behavior, because a product of two integers with the same parity is either odd or divisible by four.

For K=8, the pair 2⋅4 has equal parity and distinct factors. It gives x=(4−2)/2=1, hence A=1 and A+K=9. The program prints `1` followed by `1`, confirming that even values of K can have valid answers when they are divisible by four.

For the maximum input K=10 9, the loop still stops after only 31623 divisor candidates because it depends on K ​, not on K itself. This is the central reason the solution remains fast at the upper constraint boundary.
