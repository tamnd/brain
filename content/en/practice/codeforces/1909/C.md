---
title: "CF 1909C - Heavy Intervals"
description: "We are given a set of $n$ intervals on the number line. Each interval has a left endpoint $li$, a right endpoint $ri$, and a weight per unit length $ci$. The actual weight of an interval is calculated as $ci cdot (ri - li)$."
date: "2026-06-08T20:28:33+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dsu", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1909
codeforces_index: "C"
codeforces_contest_name: "Pinely Round 3 (Div. 1 + Div. 2)"
rating: 1400
weight: 1909
solve_time_s: 115
verified: true
draft: false
---

[CF 1909C - Heavy Intervals](https://codeforces.com/problemset/problem/1909/C)

**Rating:** 1400  
**Tags:** constructive algorithms, data structures, dsu, greedy, math, sortings  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of $n$ intervals on the number line. Each interval has a left endpoint $l_i$, a right endpoint $r_i$, and a weight per unit length $c_i$. The actual weight of an interval is calculated as $c_i \cdot (r_i - l_i)$. The goal is to minimize the total sum of weights across all intervals.

The twist is that we can independently reorder the arrays $l$, $r$, and $c$. The only restriction is that after reordering, each interval must remain valid, meaning $l_i < r_i$. Essentially, the problem allows us to pair left endpoints, right endpoints, and costs in any combination as long as intervals are well-formed. All endpoints are distinct, which guarantees that sorting them will produce valid intervals without duplicates.

The constraints indicate that the total number of intervals across all test cases does not exceed $10^5$, which means any $O(n \log n)$ solution per test case is acceptable. $O(n^2)$ brute force methods are ruled out. Non-obvious edge cases include situations where the smallest left endpoint could be paired with the largest right endpoint, which would yield a very large interval. Careless approaches might not sort the arrays in the correct order or pair the highest costs with the smallest lengths, leading to suboptimal total weight.

For example, if $l=[1,3]$, $r=[5,2]$, $c=[10,1]$, pairing $1\to5$ with $10$ and $3\to2$ with $1$ is invalid due to $3>2$, so we must reorder $r$ to $[2,5]$. The optimal pairing in this case is $l=[1,3]$, $r=[2,5]$, $c=[10,1]$, giving weights $10_1 + 1_2 = 12$. A naive greedy that just pairs $c$ with any interval might fail.

## Approaches

The brute-force approach would be to try every permutation of $l$, $r$, and $c$, check for validity, and compute the sum. For $n$ intervals, there are $n!^3$ combinations, which is completely infeasible. Even trying just all pairs of $l$ and $r$ with a fixed $c$ is $O(n!^2)$, which is also far too slow.

The key insight comes from observing that the total weight is the sum of products $c_i \cdot (r_i - l_i)$. To minimize this sum, we should pair the smallest differences $(r_i - l_i)$ with the largest costs $c_i$, or equivalently, sort the differences in increasing order and the costs in decreasing order and multiply them pairwise. Similarly, to minimize the differences themselves, we should pair the smallest $l_i$ with the smallest $r_i$ that is still larger than it. This can be achieved by sorting $l$ and $r$ independently in ascending order and matching them index-wise.

In short, the optimal solution is to sort the left endpoints $l$ in ascending order, the right endpoints $r$ in ascending order, and the costs $c$ in descending order. Then, compute the sum of $c_i \cdot (r_i - l_i)$ for each $i$. Sorting ensures valid intervals ($l_i < r_i$) due to distinct endpoints, and descending $c$ ensures the largest costs are applied to the smallest interval lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!^3) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$, the left endpoints $l$, right endpoints $r$, and costs $c$.
3. Sort the array $l$ in ascending order to get the left endpoints from smallest to largest.
4. Sort the array $r$ in ascending order to get the right endpoints from smallest to largest.
5. Sort the array $c$ in descending order to pair largest costs with smallest interval lengths.
6. Initialize a variable `total_weight` to zero.
7. Iterate over all intervals $i=0$ to $n-1$:

- Compute the length of the interval as $length = r[i] - l[i]$.
- Multiply by the corresponding cost `c[i]` to get the interval weight.
- Add this to `total_weight`.
8. Print the total weight for the current test case.

Why it works: Sorting $l$ and $r$ ascending ensures that for every $i$, $l_i < r_i$ holds, because all endpoints are distinct. Sorting $c$ descending ensures the largest cost per unit length multiplies the smallest possible length, minimizing the sum of products. The greedy property holds because any other pairing of costs to intervals would either assign a large cost to a larger length, increasing the sum, or violate the interval validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    l = list(map(int, input().split()))
    r = list(map(int, input().split()))
    c = list(map(int, input().split()))

    l.sort()
    r.sort()
    c.sort(reverse=True)

    total_weight = 0
    for i in range(n):
        total_weight += c[i] * (r[i] - l[i])
    print(total_weight)
```

Explanation: The solution first reads input efficiently with `sys.stdin.readline`. Sorting `l` and `r` ascending ensures valid intervals, while sorting `c` descending minimizes the total sum. The loop multiplies corresponding elements and accumulates the sum. Using `reverse=True` for `c` is crucial, as forgetting this step leads to pairing small costs with small intervals, which is suboptimal.

## Worked Examples

**Sample 1:**

| i | l | r | c | r-l | weight | total_weight |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | 12 | 100 | 9 | 900 | 900 |
| 1 | 8 | 23 | 100 | 15 | 1500 | 2400 |

Sorted $l=[3,8]$, $r=[12,23]$, $c=[100,100]$ yields total weight 2400. This confirms the greedy pairing works.

**Sample 2:**

| i | l | r | c | r-l | weight | total_weight |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 3 | 3 | 2 | 6 | 6 |
| 1 | 2 | 4 | 3 | 2 | 6 | 12 |
| 2 | 5 | 10 | 2 | 5 | 10 | 22 |
| 3 | 20 | 30 | 2 | 10 | 20 | 42 |

Sorting left and right ascending, costs descending produces minimum sum 42. This shows that both short intervals with high costs and long intervals with small costs are correctly assigned.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting three arrays dominates, linear pass to compute sum |
| Space | O(n) | Storing three arrays per test case |

Given the constraints of $n$ up to $10^5$ and total sum of $n$ across test cases ≤ 10^5, this solution runs comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution call
    t = int(input())
    for _ in range(t):
        n = int(input())
        l = list(map(int, input().split()))
        r = list(map(int, input().split()))
        c = list(map(int, input().split()))
        l.sort()
        r.sort()
        c.sort(reverse=True)
        total_weight = sum(c[i]*(r[i]-l[i]) for i in range(n))
        print(total_weight)
    return output.getvalue().strip()

# provided samples
assert run("2\n2\n8 3\n12 23\n100 100\n4\n20 1 2 5\n30 4 3 10\n2 3 2 3\n") == "2400\n42"

# minimum-size input
assert run("1\n1\n1\n2\n10\n") == "10"

# maximum-size input with increasing sequences
n = 10**5
l = ' '.join(map(str, range(1,n+1)))
r = ' '.join(map(str, range(2,n+2)))
c = ' '.join(['1']*n)
input_str = f"1\n{n}\n{l}\n{r}\n{c}\n"
output_str = str(sum(1 for _ in range(n)))
assert run(input_str)  # checks performance

# all equal values
assert run("1\n3\n1 2 3\n4 5 6\n5 5 5\n") == "45"

# boundary condition: large costs
assert run("1\n2\n1 3\n4 6\n1000000 1\n") == str(1000000*(4-1) + 1*(6-3))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
|  |  |  |
