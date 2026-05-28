---
title: "CF 81C - Average Score"
description: "We are given a sequence of marks, but the subject for each mark was lost. There are only two subjects, and we know exactly how many marks belong to each one. If subject 1 must receive a marks, then subject 2 automatically receives b = n - a marks."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 81
codeforces_index: "C"
codeforces_contest_name: "Yandex.Algorithm Open 2011: Qualification 1"
rating: 1700
weight: 81
solve_time_s: 211
verified: true
draft: false
---

[CF 81C - Average Score](https://codeforces.com/problemset/problem/81/C)

**Rating:** 1700  
**Tags:** greedy, math, sortings  
**Solve time:** 3m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of marks, but the subject for each mark was lost. There are only two subjects, and we know exactly how many marks belong to each one. If subject 1 must receive `a` marks, then subject 2 automatically receives `b = n - a` marks.

Our task is to assign every mark to one of the two subjects so that the sum of the two subject averages is as large as possible. Among all optimal assignments, we must output the lexicographically smallest sequence of subject labels.

The averages are:

$$\frac{\text{sum of subject 1 marks}}{a}
+
\frac{\text{sum of subject 2 marks}}{b}$$

The marks themselves are tiny, only from 1 to 5, but the number of marks can reach $10^5$. That immediately rules out any exponential search over assignments. Even $O(n^2)$ would already be risky at this scale in Python. We need something close to $O(n \log n)$, which usually suggests sorting or greedy processing.

The tricky part is that maximizing the total average is not the only requirement. If several assignments achieve the same maximum value, we must choose the lexicographically smallest assignment. A solution that only optimizes the averages but ignores tie-breaking can silently fail.

Consider this example:

```
n = 4
a = 2
b = 2
marks = [5, 1, 5, 1]
```

If we put both 5s into the same subject, the averages become:

```
(5 + 5) / 2 + (1 + 1) / 2 = 5 + 1 = 6
```

If we split them evenly:

```
(5 + 1) / 2 + (5 + 1) / 2 = 3 + 3 = 6
```

Both are optimal. But the lexicographically smallest assignment prefers earlier positions labeled `1`. A careless greedy strategy that only sorts by value could produce the wrong ordering.

Another subtle case appears when one subject is much smaller than the other:

```
n = 5
a = 1
b = 4
marks = [1, 2, 3, 4, 5]
```

The optimal strategy is to place the largest mark into the smaller denominator, because every point there contributes more to the final expression:

```
5 / 1 + (1 + 2 + 3 + 4) / 4 = 5 + 2.5 = 7.5
```

A naive “balance the subjects” intuition would fail badly here.

One more pitfall comes from equal marks. Suppose:

```
n = 5
a = 2
b = 3
marks = [4, 4, 4, 4, 4]
```

Every assignment has exactly the same score. The entire problem reduces to producing the lexicographically smallest valid sequence. The correct answer is:

```
1 1 2 2 2
```

because we want the earliest possible positions assigned to subject 1.

## Approaches

The brute-force solution is straightforward conceptually. We try every possible choice of which `a` positions belong to subject 1, compute the two averages, and keep the best assignment. Since there are:

$$\binom{n}{a}$$

possible assignments, this becomes completely infeasible even for moderate `n`. For example, with `n = 40` and `a = 20`, the number of possibilities already exceeds $10^{11}$. With `n = 10^5`, exhaustive search is impossible.

The key observation comes from rewriting the objective function. Suppose a mark `x` is assigned to subject 1. Its contribution to the total score is:

$$\frac{x}{a}$$

If the same mark is assigned to subject 2, its contribution becomes:

$$\frac{x}{b}$$

So every mark independently contributes either `x/a` or `x/b`.

That means the problem is really asking:

“Which marks should receive the larger coefficient?”

If `a < b`, then:

$$\frac{1}{a} > \frac{1}{b}$$

so larger marks should go to subject 1. If `b < a`, then larger marks should go to subject 2.

This transforms the problem into a greedy sorting problem. The smaller group should receive the largest marks.

After that, the lexicographic requirement becomes the remaining challenge. Suppose subject 1 is the smaller group and should receive the largest marks. Among equal marks, giving earlier indices to subject 1 produces a lexicographically smaller answer. So when values tie, we should prioritize smaller indices.

If subject 2 is the smaller group, the opposite happens. Since we want earlier positions to become `1` whenever possible, we should delay assigning positions to subject 2. So among equal marks, later indices should go to subject 2.

That single tie-breaking rule is the entire subtlety of the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\binom{n}{a} \cdot n)$ | $O(n)$ | Too slow |
| Optimal Greedy + Sorting | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all marks together with their original indices.
2. Determine which subject has the smaller size.

The smaller subject has the larger coefficient in the objective function, so it should receive the largest marks.
3. Sort the marks by value in descending order.

This places the most valuable marks first, which is exactly what the greedy choice needs.
4. Handle equal values carefully for lexicographic order.

If subject 1 is the smaller group, then among equal values we sort indices in ascending order. Earlier positions become `1`, making the final sequence lexicographically smaller.

If subject 2 is the smaller group, then among equal values we sort indices in descending order. This delays assigning `2` to earlier positions, again minimizing the final sequence lexicographically.
5. Take the first `min(a, b)` elements from the sorted order and assign them to the smaller subject.

All remaining positions belong to the larger subject.
6. Construct the final answer array in original order and print it.

### Why it works

The objective function is linear:

$$\sum \frac{x_i}{a} + \sum \frac{y_j}{b}$$

Each mark independently gains either coefficient `1/a` or `1/b`. The larger coefficient always belongs to the smaller subject size. So every optimal solution must place the largest marks into the smaller subject.

Once values are fixed, equal marks contribute identically regardless of placement. The only remaining freedom is lexicographic order. Assigning earlier indices to subject 1 minimizes the sequence, because `1 < 2`. The tie-breaking rules above achieve exactly that while preserving optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a, b = map(int, input().split())
    t = list(map(int, input().split()))

    arr = []

    if a <= b:
        # Subject 1 is smaller
        for i, x in enumerate(t):
            arr.append((-x, i))

        arr.sort()

        ans = [2] * n

        for j in range(a):
            _, idx = arr[j]
            ans[idx] = 1

    else:
        # Subject 2 is smaller
        for i, x in enumerate(t):
            arr.append((-x, -i))

        arr.sort()

        ans = [1] * n

        for j in range(b):
            _, neg_idx = arr[j]
            idx = -neg_idx
            ans[idx] = 2

    print(*ans)

solve()
```

The solution starts by pairing every mark with its original position. We cannot lose the indices because the output must follow the original order.

The two branches correspond to which subject is smaller. If subject 1 is smaller, we want the largest marks assigned to it. Sorting by `(-value, index)` gives descending values and ascending indices for ties. That automatically produces the lexicographically smallest assignment.

The second branch is slightly more subtle. When subject 2 is smaller, we still want the largest marks there, but now assigning an early position to subject 2 hurts lexicographic order because `2` is larger than `1`. Sorting by `(-value, -index)` makes later equal positions chosen first.

The answer array is initialized entirely with the larger subject label. Then we overwrite exactly the required number of positions for the smaller subject.

Using negative values in sorting avoids writing custom comparators and keeps the implementation concise and fast.

## Worked Examples

### Example 1

Input:

```
5
3 2
4 4 5 4 4
```

Since `b = 2` is smaller, subject 2 should receive the largest marks.

Sorted order:

| Value | Index |

|---|---|---|

| 5 | 2 |

| 4 | 4 |

| 4 | 3 |

| 4 | 1 |

| 4 | 0 |

We use descending indices among equal values because subject 2 is the smaller one.

The first two positions go to subject 2.

| Position | Assigned Subject |
| --- | --- |
| 2 | 2 |
| 4 | 2 |

All others become subject 1.

Final answer:

```
1 1 2 1 2
```

This trace demonstrates the lexicographic tie-breaking. Among equal 4s, the later index `4` is chosen before earlier indices, keeping the beginning of the answer as small as possible.

### Example 2

Input:

```
5
1 4
1 2 3 4 5
```

Subject 1 is smaller, so it should receive the largest mark.

Sorted order:

| Value | Index |
| --- | --- |
| 5 | 4 |
| 4 | 3 |
| 3 | 2 |
| 2 | 1 |
| 1 | 0 |

The first one element goes to subject 1.

| Position | Assigned Subject |
| --- | --- |
| 4 | 1 |

All others become subject 2.

Final answer:

```
2 2 2 2 1
```

The single largest value gets the larger coefficient `1/a = 1`, maximizing the total score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Dominated by sorting the marks |
| Space | $O(n)$ | Arrays for indices and final answer |

With $n \le 10^5$, sorting is easily fast enough within the 2-second limit. The memory usage is linear and comfortably fits inside 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())
        a, b = map(int, input().split())
        t = list(map(int, input().split()))

        arr = []

        if a <= b:
            for i, x in enumerate(t):
                arr.append((-x, i))

            arr.sort()

            ans = [2] * n

            for j in range(a):
                _, idx = arr[j]
                ans[idx] = 1

        else:
            for i, x in enumerate(t):
                arr.append((-x, -i))

            arr.sort()

            ans = [1] * n

            for j in range(b):
                _, neg_idx = arr[j]
                idx = -neg_idx
                ans[idx] = 2

        return " ".join(map(str, ans))

    return solve()

# provided sample
assert run(
    "5\n3 2\n4 4 5 4 4\n"
) == "1 1 2 1 2", "sample 1"

# minimum size
assert run(
    "2\n1 1\n5 1\n"
) == "1 2", "minimum case"

# all equal values
assert run(
    "5\n2 3\n4 4 4 4 4\n"
) == "1 1 2 2 2", "lexicographic tie-breaking"

# smaller second group
assert run(
    "5\n4 1\n1 2 3 4 5\n"
) == "1 1 1 1 2", "largest value goes to smaller group"

# equal top values with lexicographic issue
assert run(
    "4\n2 2\n5 1 5 1\n"
) == "1 2 1 2", "correct tie handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 1 / 5 1` | `1 2` | Minimum valid input |
| All marks equal | `1 1 2 2 2` | Lexicographic ordering among equivalent solutions |
| `a = 4, b = 1` | `1 1 1 1 2` | Smaller group gets largest marks |
| Two equal maximum values | `1 2 1 2` | Correct tie-breaking with equal values |

## Edge Cases

Consider the case where all marks are identical:

```
5
2 3
4 4 4 4 4
```

Every assignment produces the same total average because all values are equal. The algorithm enters the branch `a <= b`, sorts by `(value descending, index ascending)`, and assigns the first two positions to subject 1. The output becomes:

```
1 1 2 2 2
```

This is the lexicographically smallest valid assignment because the earliest possible positions receive label `1`.

Now consider the opposite imbalance:

```
5
1 4
1 2 3 4 5
```

Subject 1 has size 1, so its coefficient is largest. The algorithm assigns the single maximum value `5` to subject 1. Any other choice would reduce the objective value. The produced assignment is:

```
2 2 2 2 1
```

Finally, examine the subtle equal-value tie case:

```
4
2 2
5 1 5 1
```

Both subjects have equal size, so maximizing the score does not care which 5 goes where. The lexicographically smallest answer should assign the earlier 5 to subject 1:

```
1 2 1 2
```

Because the sorting uses ascending indices for equal values when subject 1 is chosen, the algorithm automatically produces the correct ordering.
