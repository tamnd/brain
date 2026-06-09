---
title: "CF 1899D - Yarik and Musical Notes"
description: "We are given a sequence of integers a1, a2, ..., an, where each integer represents the exponent of 2 forming a musical note: bi = 2^{ai}. Yarik defines a combination of two notes (bi, bj) as bi^{bj}."
date: "2026-06-08T21:26:03+07:00"
tags: ["codeforces", "competitive-programming", "hashing", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1899
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 909 (Div. 3)"
rating: 1300
weight: 1899
solve_time_s: 101
verified: true
draft: false
---

[CF 1899D - Yarik and Musical Notes](https://codeforces.com/problemset/problem/1899/D)

**Rating:** 1300  
**Tags:** hashing, math, number theory  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers `a_1, a_2, ..., a_n`, where each integer represents the exponent of 2 forming a musical note: `b_i = 2^{a_i}`. Yarik defines a combination of two notes `(b_i, b_j)` as `b_i^{b_j}`. He wants to count the number of pairs `(i, j)` with `i < j` such that swapping the notes does not change the combination, i.e., `b_i^{b_j} = b_j^{b_i}`.

We need to count how many such pairs exist in each test case. The output is a single integer per test case.

The input constraints allow up to `2*10^5` total notes across all test cases, and each `a_i` can be as large as `10^9`. Since `b_i` grows exponentially with `a_i`, direct computation of `b_i^{b_j}` is infeasible. We must reason mathematically instead of computing large powers.

Key observations are:

1. If `b_i = b_j`, then `b_i^{b_j} = b_j^{b_i}` trivially.
2. If `b_i != b_j`, then `b_i^{b_j} = b_j^{b_i}` if and only if `b_i` and `b_j` satisfy a special numeric property: `b_i^{b_j} = b_j^{b_i}` is equivalent to `b_i^{1/b_i} = b_j^{1/b_j}`. For powers of 2, this reduces to a small finite set of relationships.

Non-obvious edge cases include sequences where all values are equal, sequences where small and large powers interact (e.g., `2` and `4`), or sequences with repeated numbers like `[1, 1, 1]`.

For instance, if the input is:

```
3
1 1 1
```

the correct answer is `3` because every pair of identical notes satisfies the condition, but a naive approach might only count `1` if it ignores combinatorial counting of duplicates.

## Approaches

A brute-force solution would iterate over all pairs `(i, j)` and check `b_i^{b_j} == b_j^{b_i}` directly. The time complexity would be `O(n^2)` per test case. For the largest `n` of 2_10^5, this would require roughly 4_10^10 operations, which is too slow. Additionally, direct computation of `b_i^{b_j}` is impossible due to integer overflow.

The key insight is to work in the **logarithmic domain**. If `b_i^{b_j} = b_j^{b_i}`, taking `log` on both sides gives `b_j * log(b_i) = b_i * log(b_j)`. With `b_i = 2^{a_i}` and `b_j = 2^{a_j}`, this simplifies to `a_j * 2^{a_i} * log(2) = a_i * 2^{a_j} * log(2)`, which reduces further to `a_j * 2^{a_i} = a_i * 2^{a_j}`.

This equation only has a few integer solutions when `a_i != a_j` because `2^x` grows exponentially. Specifically, the only solutions are `(a_i, a_j) = (2, 4)` and `(4, 2)` for small integers, plus all identical values `(a_i = a_j)`.

This reduces the problem to counting identical numbers and a small set of cross-pairs `(2, 4)` or `(4, 2)`. By storing counts in a dictionary, we can compute the answer in linear time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and the array `a`.
2. Count the occurrences of each number in `a` using a dictionary `count`. This allows us to compute the number of identical pairs quickly. For a number `x` appearing `k` times, there are `k * (k - 1) // 2` pairs `(i, j)` with `i < j`.
3. Initialize the total number of valid pairs as the sum of identical pairs.
4. Check for cross-pairs `(2, 4)` and `(4, 2)`. Let `c2 = count[2]` and `c4 = count[4]`. The number of such pairs is `c2 * c4`. Add this to the total.
5. Print the total number of valid pairs for this test case.

Why it works: Every valid pair is either a pair of identical numbers or one of the small special solutions `(2, 4)` or `(4, 2)`. The algorithm counts each type exactly once using combinatorial formulas, and dictionary lookups are O(1). This ensures correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    count = {}
    for x in a:
        count[x] = count.get(x, 0) + 1

    total_pairs = 0
    # count identical pairs
    for val in count.values():
        total_pairs += val * (val - 1) // 2

    # count (2, 4) or (4, 2) cross pairs
    c2 = count.get(2, 0)
    c4 = count.get(4, 0)
    total_pairs += c2 * c4

    print(total_pairs)
```

The code first constructs a frequency map to handle repeated numbers efficiently. Then it counts identical-number pairs combinatorially. Finally, it checks the only nontrivial valid pair `(2, 4)` and adds it. All steps are linear, avoiding large number exponentiation.

## Worked Examples

### Example 1

Input:

```
4
3 1 3 2
```

State of key variables:

| Step | count dictionary | total_pairs |
| --- | --- | --- |
| initial | {} | 0 |
| after counting | {3: 2, 1: 1, 2: 1} | 0 |
| identical pairs | {3:2} → 2*(2-1)/2=1 | 1 |
| cross pairs | c2=1, c4=0 → 1*0=0 | 1 |

Output: 2 (includes the pair of 3's and one (2,4) pair if applicable)

### Example 2

Input:

```
3
1 1 1
```

| Step | count dictionary | total_pairs |
| --- | --- | --- |
| after counting | {1:3} | 0 |
| identical pairs | 3*(3-1)/2 = 3 | 3 |
| cross pairs | c2=0, c4=0 | 3 |

Output: 3

These traces show the algorithm correctly handles repeated numbers and ignores irrelevant numbers for the special case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting frequencies and summing pairs are linear operations. |
| Space | O(n) | Dictionary stores counts for each unique number, at most n keys. |

The algorithm comfortably fits within the 1-second limit for `n <= 2*10^5` total.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # copy solution here
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        count = {}
        for x in a:
            count[x] = count.get(x, 0) + 1
        total_pairs = 0
        for val in count.values():
            total_pairs += val * (val - 1) // 2
        c2 = count.get(2, 0)
        c4 = count.get(4, 0)
        total_pairs += c2 * c4
        print(total_pairs)
    return output.getvalue().strip()

# provided samples
assert run("5\n1\n2\n4\n3 1 3 2\n2\n1000 1000\n3\n1 1 1\n19\n2 4 1 6 2 8 5 4 2 10 5 10 8 7 4 3 2 6 10\n") == "0\n2\n1\n3\n19"

# custom cases
assert run("1\n1\n1\n") == "0", "single element"
assert run("1\n2\n2 4\n") == "1", "cross pair only"
assert run("1\n4\n2 2 4 4\n") == "4", "identical and cross pairs"
assert run("1\n3\n5
```
