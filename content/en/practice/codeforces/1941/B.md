---
title: "CF 1941B - Rudolf and 121"
description: "We are given an array of non-negative integers. In one operation, we choose an index $i$ such that $2 le i le n-1$, and"
date: "2026-05-27T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1941
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 933 (Div. 3)"
rating: 1000
weight: 1941
solve_time_s: 167
verified: true
draft: false
---

[CF 1941B - Rudolf and 121](https://codeforces.com/problemset/problem/1941/B)

**Rating:** 1000  
**Tags:** brute force, dp, greedy, math  
**Solve time:** 2m 47s  
**Verified:** yes  

## Solution
# Problem Understanding

We are given an array of non-negative integers. In one operation, we choose an index $i$ such that $2 \le i \le n-1$, and decrease three consecutive elements in the following way:

$$a_{i-1} \mathrel{-}= 1,\quad
a_i \mathrel{-}= 2,\quad
a_{i+1} \mathrel{-}= 1$$

The operation may be used any number of times on any valid index. The goal is to determine whether it is possible to reduce the entire array to all zeros.

The important detail is that every operation only subtracts values. We are never allowed to increase an element. Therefore, once an element becomes negative, the process is invalid. A correct solution must determine whether there exists some sequence of operations that transforms the array into exactly all zeros without ever requiring negative values.

The constraints are large enough that efficiency matters:

| Constraint | Implication |
| --- | --- |
| $t \le 10^4$ | We must process many test cases efficiently. |
| $\sum n \le 2 \cdot 10^5$ | An $O(n)$ or $O(n \log n)$ solution per test case is safe. |
| $a_i \le 10^9$ | We cannot simulate operations one-by-one if their count becomes huge. |
| Time limit: 2 seconds | The total work across all test cases should stay near linear. |
| Memory limit: 256 MB | Storing arrays and a few auxiliary variables is completely fine. |

A naive simulation that repeatedly applies operations would fail because an element may be as large as $10^9$, leading to billions of operations.

Several edge cases are easy to mishandle.

### Arrays Already Equal to Zero

If every element is already zero, the answer should immediately be "YES". A careless implementation might still try to perform operations and accidentally reject the case.

### Small Arrays

The minimum size is $n=3$. In this situation, only the middle index can be chosen. The solution must correctly handle arrays where exactly one operation location exists.

### Negative Values During Greedy Processing

Suppose we try to eliminate values from left to right. If at some point the required operation count exceeds the available amount in neighboring elements, one of them becomes negative. That immediately proves the configuration impossible.

For example:

$$[1,1,1,1]$$

Trying to eliminate the first element requires one operation at index 2, but that would reduce the second element by 2 and make it negative.

### Nonzero Tail Elements

Even if the left side becomes zero successfully, the final two elements may remain nonzero. Since operations affect three consecutive positions, once we finish processing the left side there is no way to fix the tail independently. A correct algorithm must explicitly verify the final array.

# Approaches

## Brute Force

A straightforward idea is to repeatedly search for a valid operation and apply it until no more operations are possible. For example, we might pick any index $i$ where:

$$a_{i-1} \ge 1,\quad a_i \ge 2,\quad a_{i+1} \ge 1$$

and keep subtracting.

This approach is logically correct because every operation strictly decreases the total sum of the array, so the process eventually terminates. If we reach all zeros, the answer is "YES". Otherwise, it is "NO".

The problem is efficiency. Consider an array containing values near $10^9$. The number of operations could also be near $10^9$, making direct simulation impossible within the time limit.

Thus, brute force is far too slow.

## Optimal Approach

The key observation is that the operation structure forces a natural left-to-right greedy strategy.

Suppose we are currently examining position $i$. The only operation that can decrease $a_i$ while still affecting elements to its right is the operation centered at $i+1$.

That means once we move past index $i$, we will never again be able to modify it. Therefore, if $a_i$ is not zero at that moment, the only valid choice is to apply the operation at $i+1$ exactly $a_i$ times.

This creates a deterministic process.

If we apply the operation $x=a_i$ times at center $i+1$:

$$a_i \mathrel{-}= x$$

$$a_{i+1} \mathrel{-}= 2x$$

$$a_{i+2} \mathrel{-}= x$$

Since $x=a_i$, the current element becomes zero immediately.

If either neighboring value becomes negative, then no valid sequence exists.

By processing from left to right, we greedily eliminate each element exactly when it becomes fixed forever. At the end, if all elements are zero, the transformation is possible.

## Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\text{number of operations})$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ extra | Accepted |

# Algorithm Walkthrough

1. Read the array.
2. Process indices from left to right, specifically from $0$ to $n-3$.
3. At each position $i$, let:

$$x = a_i$$

Since future operations cannot modify $a_i$ except through the operation centered at $i+1$, we must eliminate it now.
4. Apply the operation $x$ times conceptually:

$$a_i \mathrel{-}= x$$

$$a_{i+1} \mathrel{-}= 2x$$

$$a_{i+2} \mathrel{-}= x$$
5. After updating, check whether either:

$$a_{i+1} < 0
\quad \text{or} \quad
a_{i+2} < 0$$

If so, output "NO".
6. Continue processing until index $n-3$.
7. After all operations, verify that every element equals zero.
8. If the entire array is zero, output "YES". Otherwise, output "NO".

# Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    possible = True

    for i in range(n - 2):
        x = a[i]

        a[i] -= x
        a[i + 1] -= 2 * x
        a[i + 2] -= x

        if a[i + 1] < 0 or a[i + 2] < 0:
            possible = False
            break

    if possible and all(v == 0 for v in a):
        print("YES")
    else:
        print("NO")
```

The program begins with fast I/O because the total input size can reach $2 \cdot 10^5$.

For each test case, we iterate from left to right. At position `i`, the current value `a[i]` determines exactly how many operations must be applied. We store this value in `x`.

The updates:

```
a[i + 1] -= 2 * x
a[i + 2] -= x
```

simulate performing the operation `x` times.

If either updated value becomes negative, the configuration is impossible, so we terminate early.

Finally, we verify that every element is exactly zero. This last check is essential because the final two elements might remain positive even though no more operations are available.

# Worked Examples

## Example 1

Input:

```
5
1 3 5 5 2
```

### Trace

| Step | i | x = a[i] | Array After Operation |
| --- | --- | --- | --- |
| Initial | - | - | [1, 3, 5, 5, 2] |
| 1 | 0 | 1 | [0, 1, 4, 5, 2] |
| 2 | 1 | 1 | [0, 0, 2, 4, 2] |
| 3 | 2 | 2 | [0, 0, 0, 0, 0] |

All elements become zero, so the answer is:

```
YES
```

This trace demonstrates the greedy principle clearly. At every step, the current element must be removed immediately because later operations cannot affect it anymore.

## Example 2

Input:

```
5
2 4 4 5 1
```

### Trace

| Step | i | x = a[i] | Array After Operation |
| --- | --- | --- | --- |
| Initial | - | - | [2, 4, 4, 5, 1] |
| 1 | 0 | 2 | [0, 0, 2, 5, 1] |
| 2 | 1 | 0 | [0, 0, 2, 5, 1] |
| 3 | 2 | 2 | [0, 0, 0, 1, -1] |

The last element becomes negative, so the process is impossible.

Output:

```
NO
```

This example shows why checking for negative values is necessary. The greedy process determines the only possible number of operations, and if that causes a deficit, no alternative sequence exists.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is processed once |
| Space | $O(1)$ extra | Only a few variables besides the input array |

The algorithm performs a constant amount of work per index, so the total complexity across all test cases is:

$$O\left(\sum n\right)$$

Since:

$$\sum n \le 2 \cdot 10^5$$

the solution easily fits within the time limit.

The algorithm modifies the array in place and uses only a few auxiliary variables, so the extra memory usage is constant.

# Edge Cases

## All Zeros

Consider:

```
3
0 0 0
```

The loop processes the first element with `x = 0`, so nothing changes. The final array is still all zeros, therefore the answer is "YES".

The algorithm handles this naturally without requiring any special case.

## Minimum Size Array

Consider:

```
3
1 2 1
```

There is only one possible operation location.

### Trace

| i | x | Array |
| --- | --- | --- |
| 0 | 1 | [0, 0, 0] |

The array becomes zero immediately, so the answer is "YES".

Now consider:

```
3
1 1 1
```

Applying one operation would produce:

```
[0, -1, 0]
```

Since a negative value appears, the algorithm correctly outputs "NO".

## Tail Cannot Be Fixed

Consider:

```
4
0 0 1 1
```

The first two elements are already zero, so the loop performs no meaningful operations.

However, after processing, the array remains:

```
[0, 0, 1, 1]
```

The final check fails because no operation can modify only the last two elements. The algorithm correctly outputs "NO".

## Large Values

Consider:

```
5
1000000000 2000000000 1000000000 0 0
```

The algorithm processes the huge numbers in constant time using arithmetic updates. No repeated simulation is needed.

This demonstrates why the greedy arithmetic approach is efficient enough for the constraints.
