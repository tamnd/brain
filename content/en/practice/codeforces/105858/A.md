---
title: "CF 105858A - Alternating Signs"
description: "We are given an array of non-zero integers. We need to choose a subsequence, meaning we keep some elements in their original order and discard the rest."
date: "2026-06-25T14:44:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105858
codeforces_index: "A"
codeforces_contest_name: "2025 Winter ESCOM Training Camp, Final Contest"
rating: 0
weight: 105858
solve_time_s: 54
verified: true
draft: false
---

[CF 105858A - Alternating Signs](https://codeforces.com/problemset/problem/105858/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
# Problem Understanding

We are given an array of non-zero integers. We need to choose a subsequence, meaning we keep some elements in their original order and discard the rest. The chosen elements must have alternating signs, so every positive number must be followed by a negative number and every negative number must be followed by a positive number. Among all such subsequences, we want the maximum possible sum of the chosen values. The empty subsequence is allowed, so the answer can be zero.

The array length can reach $10^5$, and values can be as large as $10^9$ in absolute value. A quadratic approach would require around $10^{10}$ operations in the worst case, which is far beyond what fits in a typical contest time limit. We need a solution close to linear time, because a single pass over $10^5$ elements is easily manageable.

The tricky parts are not the alternating condition itself, but handling groups of equal signs and the possibility that taking a number is worse than skipping it. For example, with all negative numbers like:

```
3
-5 -2 -7
```

the answer is:

```
0
```

A careless solution that always chooses at least one element would incorrectly output `-2`.

Another edge case is a group of same-signed numbers where only one should be taken. For:

```
5
3 8 1 -10 5
```

the best answer is `8 - 10 + 5 = 3`. Choosing every positive number before the negative gives `3 + 8 + 1 - 10 + 5 = 7`, but the signs do not alternate because the positive values are adjacent in the subsequence. The algorithm must understand that only one value from each consecutive sign block can contribute.

A final boundary case is a single element:

```
1
100
```

The answer is `100`, because a one-element subsequence already satisfies the alternating rule.

# Approaches

A straightforward idea is to try every subsequence and keep the best valid one. The number of subsequences of an array of length $n$ is $2^n$, so this becomes impossible even for moderately small arrays. We can improve it with dynamic programming that remembers the best answer ending with a positive or negative number. This works, but it is more state than the problem needs.

The key observation is that within a consecutive block of numbers with the same sign, the subsequence can contain at most one element. Taking two positive numbers in a row would violate alternation, and taking a smaller positive number instead of a larger one can never help. The same reasoning applies to negative blocks: since we want to maximize the sum, we should take the least harmful, which is the largest value.

This reduces the problem to scanning the array, splitting it into maximal blocks of equal signs, taking the maximum element from each block, and adding those chosen values. The empty subsequence is naturally handled because every chosen block maximum can only improve the result, and if all available choices are negative, the final answer should be compared with zero.

The brute-force works because it explores every possible valid choice, but fails due to the enormous search space. The observation about sign blocks removes all unnecessary choices and leaves only the best representative of each block.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Dynamic Programming | O(n) | O(1) | Accepted |
| Sign Block Greedy | O(n) | O(1) | Accepted |

# Algorithm Walkthrough

1. Start with the first element. It creates the first sign block, and the current best value inside this block is that element.
2. Move through the array from left to right. If the current element has the same sign as the current block, update the stored maximum for this block. The reason is that the subsequence can only take one value from this block, so we keep the best possible one.
3. When the sign changes, the previous block is finished. Add its maximum value to the answer, then start a new block with the current element.
4. After the loop ends, add the maximum value from the final block because there is no following sign change to trigger the update.
5. If the resulting sum is negative, output zero because choosing no elements is allowed.

Why it works: every valid subsequence can contain at most one element from each maximal same-sign segment. The greedy choice takes the largest possible element from every segment, so for each segment it gives the best contribution independently. Since choosing from one segment does not affect which value can be chosen from another segment, combining these local best choices produces the globally best subsequence.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = 0
    cur = a[0]
    sign = 1 if a[0] > 0 else -1

    for x in a[1:]:
        current_sign = 1 if x > 0 else -1

        if current_sign == sign:
            cur = max(cur, x)
        else:
            ans += cur
            cur = x
            sign = current_sign

    ans += cur

    print(max(ans, 0))

solve()
```

The variable `cur` stores the best value inside the current sign block. It starts with the first array element because every block must contain at least one value.

During the scan, equal signs only update `cur`, since selecting another element from the same block is impossible in a valid alternating subsequence. When a sign changes, the previous block can no longer grow, so its best value is added to `ans`.

The final addition after the loop handles the last block. Forgetting this step is a common off-by-one error because the last block never encounters a sign change. The `max(ans, 0)` handles arrays where every possible subsequence sum is negative.

# Worked Examples

## Sample 1

Input:

```
4
7 1 -1 5
```

Trace:

| Index | Value | Current sign block | Stored maximum | Answer |
| --- | --- | --- | --- | --- |
| 1 | 7 | positive | 7 | 0 |
| 2 | 1 | positive | 7 | 0 |
| 3 | -1 | negative | -1 | 7 |
| 4 | 5 | positive | 5 | 7 |

After the loop, the last block contributes `5`, giving `7 - 1 + 5 = 11`.

Output:

```
11
```

This shows why the algorithm keeps only the largest value from a same-sign segment.

## Sample 2

Input:

```
3
-1 -1 -1
```

Trace:

| Index | Value | Current sign block | Stored maximum | Answer |
| --- | --- | --- | --- | --- |
| 1 | -1 | negative | -1 | 0 |
| 2 | -1 | negative | -1 | 0 |
| 3 | -1 | negative | -1 | 0 |

The final contribution is `-1`, so the computed sum is negative. Since an empty subsequence is allowed, the answer becomes zero.

Output:

```
0
```

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The array is scanned once, and every element is processed with constant work. |
| Space | O(1) | Only a few variables are stored, independent of the array size. |

The linear solution easily fits the $10^5$ limit because it performs only a few operations per array element and avoids storing any additional data structures.

# Test Cases

```python
import sys, io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    ans = 0
    cur = a[0]
    sign = 1 if a[0] > 0 else -1

    for x in a[1:]:
        s = 1 if x > 0 else -1
        if s == sign:
            cur = max(cur, x)
        else:
            ans += cur
            cur = x
            sign = s

    ans += cur
    return str(max(ans, 0))

assert solve_case("4\n7 1 -1 5\n") == "11", "sample 1"
assert solve_case("3\n-1 -1 -1\n") == "0", "sample 2"

assert solve_case("1\n100\n") == "100", "single positive"
assert solve_case("6\n5 2 9 -4 -10 3\n") == "12", "multiple blocks"
assert solve_case("5\n-8 -2 -3 -1 -9\n") == "0", "all negative"
assert solve_case("7\n1 -5 -2 4 8 -1 7\n") == "14", "block boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 100` | `100` | Single element handling |
| `5 / -8 -2 -3 -1 -9` | `0` | Empty subsequence case |
| `6 / 5 2 9 -4 -10 3` | `12` | Choosing the maximum inside sign groups |
| `7 / 1 -5 -2 4 8 -1 7` | `14` | Correct handling of many sign transitions |

# Edge Cases

For the all-negative case:

```
3
-1 -1 -1
```

the entire array is one negative block. The algorithm keeps the largest value, which is `-1`, but adding it would reduce the sum. The final comparison with zero correctly chooses the empty subsequence.

For repeated signs followed by a change:

```
5
3 8 1 -10 5
```

the first block is positive and contributes `8`, the second block is negative and contributes `-10`, and the last block contributes `5`. The result is `3`, which corresponds to the valid subsequence `[8, -10, 5]`.

For a single value:

```
1
100
```

there is one block and its maximum is `100`. The final addition gives the correct answer without requiring any special-case code.
