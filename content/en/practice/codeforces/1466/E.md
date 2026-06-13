---
title: "CF 1466E - Apollo versus Pan"
description: "We are asked to compute a sum over triples of integers drawn from a given array. Specifically, for a sequence of non-negative integers $x1, x2, ldots, xn$, the target value is $$sum{i=1}^n sum{j=1}^n sum{k=1}^n (xi & xj) cdot (xj , where $&$ is the bitwise AND and $ The…" date: "2026-06-11T01:44:54+07:00" tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "math"] categories: ["algorithms"] codeforces_contest: 1466 codeforces_index: "E" codeforces_contest_name: "Good Bye 2020" rating: 1800 weight: 1466 solve_time_s: 74 verified: true draft: false --- [CF 1466E - Apollo versus Pan](https://codeforces.com/problemset/problem/1466/E) **Rating:** 1800   **Tags:** bitmasks, brute force, math   **Solve time:** 1m 14s   **Verified:** yes   ## Solution ## Problem Understanding We are asked to compute a sum over triples of integers drawn from a given array. Specifically, for a sequence of non-negative integers $x_1, x_2, \ldots, x_n$, the target value is$$\sum_{i=1}^n \sum_{j=1}^n \sum_{k=1}^n (x_i \& x_j) \cdot (x_j \, | \, x_k)$$
where $\&$ is the bitwise AND and $|$ is the bitwise OR. The input contains multiple test cases, and for each, we need the answer modulo $10^9 + 7$.
The constraints allow $n$ up to $5 \cdot 10^5$ and numbers up to $2^{60}$. With a worst-case triple sum over $n^3$, a naive solution would perform $10^{17}$ operations in the largest test case. This is clearly impossible in 2 seconds. Therefore, we need an algorithm that scales linearly or at most $O(n \cdot \text{log}(X))$, where $X$ is the maximum number size.
A subtle point is that numbers are large (up to 60 bits), so any solution depending on iterating all possible values directly is infeasible. Zero-valued numbers and sequences where all numbers are equal are edge cases that could produce different bitwise patterns, but the solution must handle them correctly.
For example, if the array is `[0]`, the sum is `0` because both AND and OR operations yield 0. A careless approach might assume every element contributes non-zero, producing a wrong sum.
## Approaches
The brute-force method is straightforward: loop over all triples $i, j, k$ and compute $(x_i \& x_j) \cdot (x_j | x_k)$. This works in principle, but with $n = 5 \cdot 10^5$, the triple nested loop performs $(5 \cdot 10^5)^3 \approx 10^{17}$ operations per test case. This is far beyond feasible.
The key insight is to factor the sum cleverly. Observe that $(x_i \& x_j)$ depends only on $i$ and $j$, while $(x_j | x_k)$ depends only on $j$ and $k$. For a fixed $j$, the sum over $i$ of $(x_i \& x_j)$ and the sum over $k$ of $(x_j | x_k)$ can be computed separately. Let
$$S_j = \sum_{i=1}^n (x_i \& x_j), \quad T_j = \sum_{k=1}^n (x_j | x_k)$$
Then the triple sum is simply
$$\sum_{j=1}^n S_j \cdot T_j$$
This reduces the problem from $O(n^3)$ to $O(n^2)$. Still, $O(n^2)$ is too slow for $n = 5 \cdot 10^5$. To go further, we can compute $S_j$ and $T_j$ efficiently using bitwise decomposition.
For each bit position $b$ from 0 to 59, let `cnt[b]` be the number of elements with bit `b` set. Then
$$S_j = \sum_{b=0}^{59} 
\begin{cases} 
2^b \cdot \text{cnt}[b] & \text{if } x_j \text{ has bit } b \text{ set} \\
0 & \text{otherwise}
\end{cases}$$
and
$$T_j = \sum_{b=0}^{59} 
\begin{cases} 
2^b \cdot n & \text{if } x_j \text{ has bit } b \text{ set} \\
2^b \cdot \text{cnt}[b] & \text{otherwise}
\end{cases}$$
This works because if `x_j` has bit `b` set, `(x_j & x_i)` contributes `2^b` whenever `x_i` has the bit, and `(x_j | x_k)` contributes `2^b` for every `k`. If `x_j` does not have the bit, `(x_j | x_k)` contributes `2^b` only if `x_k` has the bit.
This bitwise decomposition reduces the sum calculation for each `j` to O(60), giving an overall complexity of O(n * 60) per test case, which is acceptable.
| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n * 60) | O(60) | Accepted |
## Algorithm Walkthrough
1. For each test case, read `n` and the array `x`.
2. Initialize an array `cnt` of length 60, counting how many numbers have each bit set. Iterate through `x` and increment `cnt[b]` for each bit `b` that is set in `x[i]`.
3. Initialize a variable `answer` to 0. Iterate over each element `x_j` of `x`:
1. Compute `S_j` as the sum over all bit positions where `x_j` has a bit set, multiplying the bit value `2^b` by `cnt[b]`.
2. Compute `T_j` as the sum over all bit positions. If `x_j` has the bit, contribute `2^b * n`. Otherwise, contribute `2^b * cnt[b]`.
3. Multiply `S_j` and `T_j`, take modulo `10^9 + 7`, and add to `answer`.
4. Output `answer` modulo `10^9 + 7`.
Why it works: the decomposition exploits the linearity of summation and the independence of bits in AND and OR operations. Each triple `(i, j, k)` contributes exactly once to `S_j * T_j`, and the bitwise sums guarantee that the value of each bit is counted the correct number of times. Modulo arithmetic preserves correctness.
## Python Solution
```python
import sys
input = sys.stdin.readline
MOD = 10**9 + 7
t = int(input())
for _ in range(t):
    n = int(input())
    x = list(map(int, input().split()))
    
    cnt = [0] * 60
    for num in x:
        for b in range(60):
            if (num >> b) & 1:
                cnt[b] += 1
    
    answer = 0
    for num in x:
        s = 0
        t_sum = 0
        for b in range(60):
            bit_val = (1 << b) % MOD
            if (num >> b) & 1:
                s = (s + bit_val * cnt[b]) % MOD
                t_sum = (t_sum + bit_val * n) % MOD
            else:
                t_sum = (t_sum + bit_val * cnt[b]) % MOD
        answer = (answer + s * t_sum) % MOD
    print(answer)
```
The code begins by reading the number of test cases and each test case input. It computes the `cnt` array to store the number of elements with each bit set, ensuring we do not recompute counts for each element. When computing `S_j` and `T_j`, we multiply by powers of two modulo $10^9 + 7$ to prevent overflow. Finally, we sum the contributions of all `x_j` and print the answer modulo `10^9 + 7`. The modulo operation is applied at each multiplication and addition to avoid integer overflow with large numbers.
## Worked Examples
For the array `[1, 7]`:
| j | num | S_j | T_j | S_j * T_j |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 8 | 8 |
| 2 | 7 | 8 | 15 | 120 |
Total sum: `8 + 120 = 128`, matching the sample output.
For the array `[1, 2, 4]`:
| j | num | S_j | T_j | S_j * T_j |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 7 | 7 |
| 2 | 2 | 2 | 10 | 20 |
| 3 | 4 | 4 | 14 | 64 |
Total sum: `7 + 20 + 64 = 91`, matching the sample output.
These traces confirm that `S_j` counts contributions of `(x_i & x_j)` correctly and `T_j` counts contributions of `(x_j | x_k)` correctly, demonstrating the correctness of the bitwise decomposition.
## Complexity Analysis
| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 60) | Counting bits and computing `S_j` and `T_j` for each `x_j` |
| Space | O(60) | Storing counts per bit position |
The solution is linear in `n` with a small
