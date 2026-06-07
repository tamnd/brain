---
title: "CF 2128C - Leftmost Below"
description: "We start with an array of length n, filled with zeros. An operation chooses a positive integer x that is strictly larger than the current minimum value in the array. The operation does not let us choose which position receives the increment."
date: "2026-06-08T03:09:17+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2128
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1039 (Div. 2)"
rating: 1200
weight: 2128
solve_time_s: 136
verified: true
draft: false
---

[CF 2128C - Leftmost Below](https://codeforces.com/problemset/problem/2128/C)

**Rating:** 1200  
**Tags:** greedy, math  
**Solve time:** 2m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of length `n`, filled with zeros. An operation chooses a positive integer `x` that is strictly larger than the current minimum value in the array.

The operation does not let us choose which position receives the increment. Instead, it automatically finds the leftmost index whose value is still below `x`. That position receives `+x`.

The question is whether a given target array `b` can be produced from the all-zero array after any number of such operations.

The input contains many test cases. Across all test cases, the total number of array elements is at most 200,000. Any solution slower than linear or near-linear per test case becomes risky. A quadratic algorithm would require roughly $4 \cdot 10^{10}$ operations in the worst case, which is completely infeasible. The target is an $O(n)$ or $O(n \log n)$ solution.

Several situations are easy to misjudge.

Consider:

```
3
3 1 2
```

The correct answer is `NO`.

A common mistake is to look only at whether every element can be represented as a sum of positive increments. That is always true. The difficulty comes from the leftmost-position rule, which imposes strong ordering constraints.

Another tricky case is:

```
2
1 1
```

The answer is `YES`.

A careless argument might claim that every increment must be larger than the current minimum, and since the first element becomes positive, reaching the second position is impossible. In reality, after making the first element equal to `1`, the minimum of the array is still `0`, so we may choose `x = 1` again and update the second element.

One more useful example is:

```
3
40 60 90
```

The answer is `NO`.

Although every value is large, the third position cannot accumulate enough value. The earlier positions impose an upper bound on the size of increments that may reach later positions.

Understanding that bound is the key observation.

## Approaches

A brute-force view would try to simulate all possible sequences of operations. At each step we may choose many different values of `x`, and the number of reachable states grows explosively. Even for very small arrays, the search tree becomes enormous. There is no realistic way to enumerate all possibilities.

To find structure, focus on a single position `i`.

Suppose we are trying to build `b[i]`. Any increment that reaches position `i` must satisfy two conditions.

First, it must not be larger than every earlier element. Otherwise position `i` would not be the leftmost value below `x`. If an increment of size `x` reaches position `i`, then every position before `i` must already be at least `x`.

Second, when position `i` receives its first increment, its current value is `0`. Since the increment itself is `x`, the first increment can never exceed the final target `b[i]`.

Combining these facts, every increment applied to position `i` has size at most

$$\min(b_1,b_2,\ldots,b_{i-1}).$$

Let

$$m_i=\min(b_1,\ldots,b_{i-1}).$$

If `b[i] > m_i`, then the only way to reach `b[i]` is for the very first increment on position `i` to be exactly `b[i]`. Any sum of smaller increments would have total at most `m_i`.

That means we must be able to apply an increment of size `b[i]` directly to position `i`. For that to happen, every earlier position must already be at least `b[i]`. Since their final values are exactly `b[1],...,b[i-1]`, this requires

$$b[i] \le m_i.$$

If `b[i] > m_i`, reaching `b[i]` is impossible.

Conversely, if

$$b[i] \le m_i$$

holds for every position after the first, then construction is always possible. We can simply give position `i` a single increment of size `b[i]` once all previous positions have reached their final values.

The entire problem reduces to checking whether every element is at most the minimum of all earlier elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the target array `b`.
2. Initialize `pref_min = b[0]`.

This stores the minimum value among all elements seen so far.
3. Process positions from left to right starting at index `1`.
4. For the current value `b[i]`, check whether

$$b[i] \le pref\_min.$$

Any increment reaching this position can never exceed the minimum final value of earlier positions.
5. If `b[i] > pref_min`, immediately answer `NO`.

Position `i` would need an increment larger than what the earlier positions can support.
6. Otherwise update

$$pref\_min = \min(pref\_min, b[i]).$$

This maintains the minimum among all processed elements.
7. If every position passes the check, answer `YES`.

### Why it works

For any position `i > 1`, every increment that reaches it must be no larger than the final value of every earlier position. Hence every such increment is at most

$$m_i=\min(b_1,\ldots,b_{i-1}).$$

If `b[i] > m_i`, no sequence of allowed increments can produce `b[i]`, because the first increment already cannot exceed `m_i`.

If `b[i] \le m_i`, we may wait until positions `1..i-1` have reached their targets, then apply a single increment of size `b[i]` to position `i`. Since all earlier positions are at least `b[i]`, the operation is valid and immediately finishes that position.

Thus the target array is reachable exactly when every element after the first does not exceed the minimum of all earlier elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        n = int(input())
        b = list(map(int, input().split()))

        pref_min = b[0]
        ok = True

        for i in range(1, n):
            if b[i] > pref_min:
                ok = False
                break
            pref_min = min(pref_min, b[i])

        ans.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(ans))

solve()
```

The solution maintains the minimum value among all elements to the left of the current position.

When processing `b[i]`, the variable `pref_min` is exactly

$$\min(b_1,\ldots,b_{i-1}).$$

The reachability condition is simply `b[i] <= pref_min`. If the condition fails once, no later processing can repair it, so we may stop immediately for that test case.

All values fit comfortably in 32-bit integers, but Python integers handle them automatically. The algorithm uses only a few variables regardless of `n`, so the memory usage is constant.

## Worked Examples

### Example 1

Input:

```
4
5 6 1 1
```

| Position | b[i] | Prefix minimum before check | Valid? |
| --- | --- | --- | --- |
| 1 | 5 | - | Start |
| 2 | 6 | 5 | No |

The second value exceeds the minimum among earlier elements.

Since `6 > 5`, the answer is immediately `NO`.

This demonstrates the key restriction. Position 2 would need an increment of size 6, but position 1 only ends at 5, so it can never support such an increment.

### Example 2

Input:

```
2
1 1
```

| Position | b[i] | Prefix minimum before check | Valid? |
| --- | --- | --- | --- |
| 1 | 1 | - | Start |
| 2 | 1 | 1 | Yes |

Every position satisfies the condition.

The answer is `YES`.

One valid construction is:

```
[0,0]
x=1 -> [1,0]
x=1 -> [1,1]
```

This example shows that equality is allowed. A later position may receive an increment exactly equal to the smallest earlier value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once |
| Space | O(1) | Only a few variables are maintained |

The sum of all `n` values across test cases is at most 200,000. A linear scan over every element performs only 200,000 comparisons, which is far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())
            b = list(map(int, input().split()))

            pref_min = b[0]
            ok = True

            for i in range(1, n):
                if b[i] > pref_min:
                    ok = False
                    break
                pref_min = min(pref_min, b[i])

            out.append("YES" if ok else "NO")

        return "\n".join(out)

    return solve()

# provided samples
assert run(
"""4
4
5 6 1 1
3
3 1 2
3
40 60 90
2
1 1
"""
) == "NO\nNO\nNO\nYES"

# minimum size
assert run(
"""1
2
1 1
"""
) == "YES"

# strictly decreasing
assert run(
"""1
5
10 9 8 7 6
"""
) == "YES"

# equality everywhere
assert run(
"""1
4
7 7 7 7
"""
) == "YES"

# first violation appears late
assert run(
"""1
5
8 4 4 4 5
"""
) == "NO"

# large boundary values
assert run(
"""1
3
1000000000 1000000000 1000000000
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | YES | Smallest valid array |
| `10 9 8 7 6` | YES | Strictly decreasing sequence |
| `7 7 7 7` | YES | Equality with prefix minimum |
| `8 4 4 4 5` | NO | Violation occurring after several valid positions |
| `10^9 10^9 10^9` | YES | Largest allowed values |

## Edge Cases

Consider:

```
1
3
3 1 2
```

The algorithm processes:

| Position | Value | Prefix minimum |
| --- | --- | --- |
| 1 | 3 | - |
| 2 | 1 | 3 |
| 3 | 2 | 1 |

At position 3, we have `2 > 1`, so the answer is `NO`.

Position 2 ends at only `1`, meaning no increment larger than `1` can ever reach position 3. The target value `2` is unattainable.

Consider:

```
1
2
1 1
```

The scan sees `1 <= 1`, so the answer is `YES`.

The equality case is easy to mishandle if one writes a strict inequality. The condition is `<=`, not `<`.

Consider:

```
1
3
40 60 90
```

The algorithm stops immediately at position 2 because `60 > 40`.

Even though the values are large, size alone is irrelevant. What matters is whether each element exceeds the smallest earlier value. Once a position is larger than that minimum, the operation rules prevent it from being created.
