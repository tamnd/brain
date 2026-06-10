---
title: "CF 1535B - Array Reodering"
description: "We are given an array of integers and may permute it however we like. After choosing an ordering, a pair of positions $(i,j)$ with $i<j$ is called good if $$gcd(ai, 2aj) 1.$$ The task is to maximize the number of good pairs. The input contains multiple test cases."
date: "2026-06-10T15:40:23+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1535
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 110 (Rated for Div. 2)"
rating: 900
weight: 1535
solve_time_s: 239
verified: true
draft: false
---

[CF 1535B - Array Reodering](https://codeforces.com/problemset/problem/1535/B)

**Rating:** 900  
**Tags:** brute force, greedy, math, number theory, sortings  
**Solve time:** 3m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and may permute it however we like. After choosing an ordering, a pair of positions $(i,j)$ with $i<j$ is called good if

$$\gcd(a_i, 2a_j) > 1.$$

The task is to maximize the number of good pairs.

The input contains multiple test cases. For each test case we receive one array and must output the largest possible number of good pairs after reordering.

The constraint that matters most is the total size of all arrays. Although there may be up to 1000 test cases, the sum of all $n$ values is at most 2000. That changes the complexity picture completely. An $O(n^2)$ algorithm is perfectly safe because

$$2000^2 = 4 \cdot 10^6,$$

which is tiny for a 2-second limit. There is no need for advanced number theory or sophisticated data structures.

A subtle point is that the condition involves $2a_j$, not $a_j$. This makes every even number extremely valuable. For example:

Input:

```
1
2
2 3
```

If we place the array as $[2,3]$, then

$$\gcd(2, 2\cdot3)=\gcd(2,6)=2,$$

so the pair is good.

A careless solution that checks $\gcd(a_i,a_j)$ instead would incorrectly conclude that

$$\gcd(2,3)=1.$$

Another easy mistake is assuming that only pairs of even numbers matter.

Input:

```
1
3
2 3 5
```

Ordering it as $[2,3,5]$ gives

$$\gcd(2,6)=2,\qquad
\gcd(2,10)=2.$$

Both pairs involving the leading even number are good.

A final edge case occurs when all numbers are odd.

Input:

```
1
3
1 3 5
```

No reordering creates an even first element. The answer comes entirely from checking the gcd condition directly among odd numbers.

## Approaches

The brute-force idea is straightforward. Generate every possible permutation, count how many pairs satisfy the condition, and keep the maximum.

This works because the definition of a good pair is easy to evaluate. Unfortunately, the number of permutations is $n!$. Even for $n=15$, that is already enormous. Since $n$ can reach 2000, this approach is completely impossible.

The key observation comes from looking at the condition

$$\gcd(a_i,2a_j)>1.$$

Suppose $a_i$ is even. Then $2a_j$ is also even, so both numbers are divisible by $2$. Therefore

$$\gcd(a_i,2a_j)\ge 2.$$

That means every pair whose first element is even is automatically good.

This suggests a greedy strategy. We want as many indices as possible to contain even numbers before odd numbers. If all even numbers are moved to the front, then every pair whose first element is one of those even numbers becomes good automatically.

After placing all evens first, the remaining pairs are pairs of odd numbers. For those pairs we simply test the gcd condition directly.

Once the array is reordered in this way, counting the answer is easy. We examine every pair $(i,j)$ and count those satisfying

$$\gcd(a_i,2a_j)>1.$$

Since $n\le 2000$, an $O(n^2)$ pair scan is entirely acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | $O(n!\cdot n^2)$ | $O(n)$ | Too slow |
| Greedy Reordering + Pair Check | $O(n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Split the array into even numbers and odd numbers.
2. Construct a new ordering by placing all even numbers first, followed by all odd numbers.
3. Initialize the answer to zero.
4. For every pair of indices $(i,j)$ with $i<j$, compute

$$\gcd(a_i,2a_j).$$

1. If the gcd is greater than $1$, increment the answer.
2. Output the final count.

The reason step 2 is optimal is that every even number placed earlier creates automatic good pairs with every later element. Moving an even number to the front can only increase the number of such pairs and never decreases them.

### Why it works

Consider any even value $x$. For every later value $y$,

$$\gcd(x,2y)\ge 2.$$

Thus every pair whose first element is even is guaranteed to be good.

To maximize the number of guaranteed good pairs, every even number should appear before every odd number. Any ordering that leaves an odd number before an even number wastes a potential automatic good pair. After moving all evens to the front, the number of guaranteed good pairs is maximized.

Among the remaining odd-odd pairs, no further structural simplification exists. We must evaluate the gcd condition directly. Therefore the described ordering followed by direct counting produces the maximum possible answer.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    even = []
    odd = []

    for x in a:
        if x % 2 == 0:
            even.append(x)
        else:
            odd.append(x)

    a = even + odd

    ans = 0

    for i in range(n):
        for j in range(i + 1, n):
            if gcd(a[i], 2 * a[j]) > 1:
                ans += 1

    print(ans)
```

The first part separates even and odd values. This implements the greedy ordering. The relative order inside the even group and inside the odd group does not matter.

After building the reordered array, the nested loops examine every pair exactly once. The condition from the statement is checked literally, using Python's built-in `gcd`.

No overflow issues exist because

$$a_i \le 10^5,$$

so

$$2a_j \le 2\cdot 10^5.$$

The nested loop runs at most about two million pair checks across all test cases, which easily fits within the limits.

## Worked Examples

### Example 1

Input:

```
4
3 6 5 3
```

After reordering:

```
6 3 5 3
```

| Pair | gcd(ai, 2aj) | Good? |
| --- | --- | --- |
| (6,3) | gcd(6,6)=6 | Yes |
| (6,5) | gcd(6,10)=2 | Yes |
| (6,3) | gcd(6,6)=6 | Yes |
| (3,5) | gcd(3,10)=1 | No |
| (3,3) | gcd(3,6)=3 | Yes |
| (5,3) | gcd(5,6)=1 | No |

Total good pairs = 4.

This example shows why placing the even number first is beneficial. Every pair beginning with 6 is automatically good.

### Example 2

Input:

```
5
1 4 2 4 1
```

After reordering:

```
4 2 4 1 1
```

| Pair | gcd(ai, 2aj) | Good? |
| --- | --- | --- |
| (4,2) | 4 | Yes |
| (4,4) | 4 | Yes |
| (4,1) | 2 | Yes |
| (4,1) | 2 | Yes |
| (2,4) | 2 | Yes |
| (2,1) | 2 | Yes |
| (2,1) | 2 | Yes |
| (4,1) | 2 | Yes |
| (4,1) | 2 | Yes |
| (1,1) | 1 | No |

The answer is 9.

This example demonstrates that every pair starting with an even number contributes automatically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Check every pair once after reordering |
| Space | $O(n)$ | Store the reordered array |

Because the sum of all $n$ values is at most 2000, the total number of pair checks is bounded by roughly four million. This comfortably fits within the time limit.

## Test Cases

```python
import sys
import io
from math import gcd

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        even = [x for x in a if x % 2 == 0]
        odd = [x for x in a if x % 2 == 1]
        a = even + odd

        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                if gcd(a[i], 2 * a[j]) > 1:
                    ans += 1

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

assert run("3\n4\n3 6 5 3\n2\n1 7\n5\n1 4 2 4 1\n") == "4\n0\n9", "sample"

assert run("1\n2\n2 4\n") == "1", "all even"
assert run("1\n2\n1 1\n") == "0", "all odd"
assert run("1\n3\n2 3 5\n") == "2", "single even in front"
assert run("1\n4\n2 2 2 2\n") == "6", "all pairs good"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 4` | `1` | Smallest nontrivial all-even case |
| `1 1` | `0` | Gcd never exceeds 1 |
| `2 3 5` | `2` | Even-first greedy effect |
| `2 2 2 2` | `6` | Every pair becomes good |

## Edge Cases

Consider an array consisting entirely of even numbers:

```
1
4
2 4 6 8
```

Every pair satisfies the condition because the first element of every pair is even. The algorithm places all numbers in front, then counts

$$\binom{4}{2}=6$$

good pairs.

Consider an array consisting entirely of odd numbers:

```
1
3
1 3 5
```

The reordered array is unchanged. The algorithm checks every pair directly:

$$\gcd(1,6)=1,\quad
\gcd(1,10)=1,\quad
\gcd(3,10)=1.$$

The answer is 0.

Consider a mixture with only one even number:

```
1
3
3 2 5
```

The algorithm reorders to

```
2 3 5
```

The pairs are

$$(2,3),\ (2,5),\ (3,5).$$

The first two are good because the leading element is even. The last is not. The answer is 2, which is maximal.
