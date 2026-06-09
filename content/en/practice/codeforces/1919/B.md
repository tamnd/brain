---
title: "CF 1919B - Plus-Minus Split"
description: "The string consists only of '+' and '-'. We can interpret each character as a number: '+' becomes +1, and '-' becomes -1. We are allowed to split this sequence into any number of contiguous non-empty pieces."
date: "2026-06-08T19:33:29+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1919
codeforces_index: "B"
codeforces_contest_name: "Hello 2024"
rating: 800
weight: 1919
solve_time_s: 118
verified: true
draft: false
---

[CF 1919B - Plus-Minus Split](https://codeforces.com/problemset/problem/1919/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The string consists only of `'+'` and `'-'`. We can interpret each character as a number: `'+'` becomes `+1`, and `'-'` becomes `-1`.

We are allowed to split this sequence into any number of contiguous non-empty pieces. For each piece, we compute:

$$\text{penalty} = |\text{sum of piece}| \times \text{length of piece}$$

The total penalty is the sum of penalties of all pieces. Our goal is to choose the split that minimizes this total.

The length of a string is at most 5000, and there can be up to 1000 test cases. The statement explicitly says there is no bound on the sum of all $n$, so we should look for a solution that processes each test case in linear time. Anything quadratic per test case would become risky.

The tricky part is that the penalty depends both on the sum and on the length of a segment. Many partition problems require dynamic programming, so it is natural to wonder whether we must try many possible splits. The key observation is that the structure of values is extremely restricted: every element is either $+1$ or $-1$.

A few edge cases are easy to mishandle.

Consider:

```
+
```

The array contains only one value, $+1$. No split is possible. The answer is $1$, not $0$.

Consider:

```
+-
```

The whole segment has sum $0$, so its penalty is $0$. The answer is $0$. A solution that only counts individual characters would incorrectly return $2$.

Consider:

```
+++
```

Every element is $+1$. No zero-sum segment exists. Splitting into single elements gives penalty $1+1+1=3$, which is already optimal. The answer is $3$.

These examples suggest that what really matters is how many pluses and minuses can cancel each other.

## Approaches

A brute-force solution would try every possible way to split the array.

For a length-$n$ array, there are $2^{n-1}$ possible partition positions. Even for $n=50$, this is completely infeasible. We need something much simpler.

To discover the shortcut, look at a single segment.

Its sum is an integer. Since every element is either $+1$ or $-1$, the sum equals:

$$(\text{number of pluses})-(\text{number of minuses})$$

Suppose a segment has sum $0$. Then its penalty is

$$|0| \times \text{length}=0$$

Such a segment contributes nothing.

Now suppose a segment has sum $k\neq 0$. Since every element contributes either $+1$ or $-1$, the segment contains at least $|k|$ unmatched signs. The penalty is

$$|k| \times \text{length}$$

and the length is at least $1$, so

$$|k| \times \text{length}\ge |k|$$

This means every segment contributes at least the absolute value of its sum.

Let the segment sums be $s_1,s_2,\dots,s_m$. Their total equals the sum of the entire array:

$$s_1+s_2+\cdots+s_m=S$$

The total penalty is at least

$$|s_1|+|s_2|+\cdots+|s_m|$$

By the triangle inequality,

$$|s_1|+|s_2|+\cdots+|s_m|\ge |S|$$

Hence every possible partition has penalty at least $|S|$.

Now we ask whether this lower bound can actually be achieved.

Yes. Split the array into single elements. Every segment has length $1$, so its penalty is exactly $1$. Each `'+'` contributes $1$, each `'-'` contributes $1$.

Whenever we have one plus and one minus, we can merge them into a larger zero-sum segment. That segment contributes $0$ instead of $2$. Every matched plus-minus pair removes exactly $2$ from the total.

If the string contains $P$ pluses and $M$ minuses, then $\min(P,M)$ pairs can cancel. The number of unmatched symbols is

$$|P-M|$$

and that is exactly $|S|$.

Thus the minimum penalty is simply

$$|P-M|$$

No actual partition needs to be constructed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Count how many `'+'` characters appear in the string. Let this be `plus`.
2. Count how many `'-'` characters appear in the string. Let this be `minus`.
3. Compute:

$$|plus-minus|$$

This equals the absolute value of the sum of the whole array.

1. Output the result.

The reason this works is that every matched plus-minus pair can be placed inside a zero-sum segment and contribute nothing. Only the excess symbols of the majority sign remain unavoidable, and their count is exactly $|plus-minus|$.

### Why it works

Let the sums of the chosen segments be $s_1,s_2,\dots,s_k$.

Every segment penalty satisfies

$$|s_i|\cdot \text{len}_i \ge |s_i|$$

because every length is at least $1$.

Hence total penalty satisfies

$$\sum |s_i|\cdot \text{len}_i \ge \sum |s_i| \ge \left|\sum s_i\right|$$

The final quantity is exactly the absolute value of the sum of the whole array, namely $|P-M|$.

This proves no partition can achieve a penalty smaller than $|P-M|$.

On the other hand, all matching plus-minus pairs can be grouped into zero-sum segments, leaving exactly $|P-M|$ unmatched symbols. Each unmatched symbol contributes penalty $1$, so a partition with total penalty $|P-M|$ exists.

Since we have both a lower bound and a matching construction, $|P-M|$ is the minimum possible penalty.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    s = input().strip()

    plus = s.count('+')
    minus = n - plus

    print(abs(plus - minus))
```

The implementation directly follows the mathematical result.

First, we count the number of `'+'` characters. Since every other character must be `'-'`, the number of minuses is simply `n - plus`.

The answer is the absolute difference between these counts. No partitioning logic is required because the proof shows that every optimal partition has the same minimum value, namely the absolute sum of the entire array.

There are no overflow concerns because $n \le 5000$, so all values are tiny compared to Python's integer limits.

## Worked Examples

### Example 1

Input:

```
+-+-+-
```

| Position | Character | Plus Count | Minus Count |
| --- | --- | --- | --- |
| 1 | + | 1 | 0 |
| 2 | - | 1 | 1 |
| 3 | + | 2 | 1 |
| 4 | - | 2 | 2 |
| 5 | + | 3 | 2 |
| 6 | - | 3 | 3 |

Final computation:

$$|3-3|=0$$

Answer:

```
0
```

This demonstrates complete cancellation. Every plus can be matched with a minus, so the entire penalty can be reduced to zero.

### Example 2

Input:

```
--+++++++-
```

| Position | Character | Plus Count | Minus Count |
| --- | --- | --- | --- |
| 1 | - | 0 | 1 |
| 2 | - | 0 | 2 |
| 3 | + | 1 | 2 |
| 4 | + | 2 | 2 |
| 5 | + | 3 | 2 |
| 6 | + | 4 | 2 |
| 7 | + | 5 | 2 |
| 8 | + | 6 | 2 |
| 9 | + | 7 | 2 |
| 10 | - | 7 | 3 |

Final computation:

$$|7-3|=4$$

Answer:

```
4
```

There are four more pluses than minuses. Those four excess pluses cannot be cancelled by any partition, so the minimum penalty is exactly four.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to count characters |
| Space | $O(1)$ | Only a few integer counters are stored |

The algorithm processes each character exactly once. Even if many test cases are provided, linear time per test case is easily fast enough for the given limits, and the memory usage remains constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        plus = s.count('+')
        minus = n - plus

        ans.append(str(abs(plus - minus)))

    return "\n".join(ans)

# provided sample
assert run(
"""5
1
+
5
-----
6
+-+-+-
10
--+++++++-
20
+---++++-+++++---++-
"""
) == "1\n5\n0\n4\n4"

# minimum size
assert run(
"""1
1
-
"""
) == "1"

# perfectly balanced
assert run(
"""1
2
+-
"""
) == "0"

# all equal
assert run(
"""1
5
+++++
"""
) == "5"

# odd length with one excess plus
assert run(
"""1
7
+-+-+++
"""
) == "3"

# another balanced arrangement
assert run(
"""1
8
++--++--
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `-` | `1` | Smallest possible test case |
| `+-` | `0` | Complete cancellation |
| `+++++` | `5` | All values identical |
| `+-+-+++` | `3` | Excess pluses remain after matching |
| `++--++--` | `0` | Balanced counts regardless of order |

## Edge Cases

Consider the input:

```
1
1
+
```

We have `plus = 1` and `minus = 0`. The algorithm returns:

$$|1-0|=1$$

There is only one segment, whose penalty is also $1$. The answer is correct.

Consider:

```
1
2
+-
```

The counts are `plus = 1` and `minus = 1`. The algorithm returns:

$$|1-1|=0$$

Indeed, taking the whole array as one segment gives sum $0$ and penalty $0$.

Consider:

```
1
3
+++
```

The counts are `plus = 3` and `minus = 0`. The algorithm returns:

$$|3-0|=3$$

No minus signs exist to cancel any plus signs. The best achievable penalty is exactly $3$, which matches the result.

Consider:

```
1
6
---+++
```

The counts are equal, so the algorithm returns:

$$|3-3|=0$$

Even though all minuses come first and all pluses come later, order does not matter. The whole array has sum $0$, so a zero penalty is achievable. This case confirms that only the counts of pluses and minuses matter.
