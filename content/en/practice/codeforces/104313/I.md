---
title: "CF 104313I - \u041c\u0435\u0442\u0440\u043e"
description: "We are given a collection of straight lines on the plane, each defined by an equation of the form $y = kx + b$. We are not asked to analyze intersections between arbitrary pairs of lines or to find a geometric intersection point."
date: "2026-07-01T19:47:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104313
codeforces_index: "I"
codeforces_contest_name: "II \u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 104313
solve_time_s: 56
verified: true
draft: false
---

[CF 104313I - \u041c\u0435\u0442\u0440\u043e](https://codeforces.com/problemset/problem/104313/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of straight lines on the plane, each defined by an equation of the form $y = kx + b$. We are not asked to analyze intersections between arbitrary pairs of lines or to find a geometric intersection point. Instead, we only care about where these lines intersect the vertical axis $x = 0$, that is, the y-axis.

Every line contributes exactly one point on the y-axis: its value at $x = 0$, which is simply $b$. However, the problem is not just about listing these values. Multiple lines may share the same intercept $b$, meaning they pass through the same point on the y-axis. The task is to choose an integer coordinate $y$ on the y-axis such that the maximum number of lines pass through the point $(0, y)$. If several y-values achieve this maximum frequency, we must return the smallest such y.

So the entire problem reduces to finding the most frequent value among all given $b$ coefficients, with a tie-breaker favoring the smallest value.

The input size reaches up to $10^5$, which immediately rules out any $O(n^2)$ comparisons. We must reduce the problem to a frequency aggregation problem, solvable in linear or near-linear time using hashing or sorting.

A naive but instructive edge case appears when many lines share the same intercept:

Input:

```
4
2 5
3 5
-1 5
10 5
```

All lines intersect the y-axis at $y = 5$, so the correct answer is 5. Any approach that mistakenly tries to consider intersections between lines instead of just evaluating at $x = 0$ would overcomplicate the task and likely fail under time constraints.

Another subtle case involves tie-breaking:

Input:

```
3
1 1
2 2
3 2
```

Here, y = 2 appears twice while y = 1 appears once, so answer is 2. If frequencies are equal, for example:

```
3
1 1
2 2
3 1
```

both 1 and 2 appear twice, so we must output 1 since it is smaller.

## Approaches

The brute-force interpretation would be to compare every pair of lines and somehow deduce which y-axis point is “most shared”. But since each line contributes independently to exactly one y-axis intercept, pairwise comparisons are unnecessary. A naive approach might try to compute counts by checking each line against all others, resulting in $O(n^2)$ time. With $n = 10^5$, this becomes $10^{10}$ operations, which is infeasible.

The key observation is that every line is fully characterized for this problem by a single number: its y-intercept $b$. The slope $k$ never affects where it meets the y-axis. Therefore, the problem reduces to counting frequencies of integers and selecting the most frequent one with a lexicographically smallest tie-break.

This transforms the problem into a standard histogram construction over up to $10^5$ integers, which can be handled efficiently using a dictionary or sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Comparison | $O(n^2)$ | $O(1)$ | Too slow |
| Frequency Counting (Hash Map / Sorting) | $O(n)$ average / $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We proceed by reducing each line to a single value and then solving a frequency maximization problem.

1. Read all lines and extract only the intercept $b$ from each equation. This is the only value that determines the y-axis intersection, since setting $x = 0$ eliminates the slope term.
2. Maintain a frequency map from integer values of $b$ to how many times they appear. Each occurrence corresponds to one line passing through the same point on the y-axis.
3. Iterate through all entries in the frequency map and track the best candidate. The best candidate is defined first by maximum frequency, and in case of ties by smaller $b$.
4. Output the chosen $b$.

The subtle part is the tie-breaking rule. It must be enforced explicitly: whenever we see the same frequency as the current best, we only update the answer if the new value is smaller.

### Why it works

Each line contributes exactly one point on the y-axis, and no two distinct lines can contribute anything other than their intercepts. Therefore, counting how many lines pass through a given y-coordinate is exactly equivalent to counting how many times that intercept appears in the input. The algorithm exhaustively counts all contributions and selects the maximum-frequency value with a deterministic tie-break, so it cannot miss a better candidate or select a suboptimal one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    freq = {}

    for _ in range(n):
        k, b = map(int, input().split())
        freq[b] = freq.get(b, 0) + 1

    best_y = None
    best_cnt = 0

    for y, cnt in freq.items():
        if cnt > best_cnt or (cnt == best_cnt and (best_y is None or y < best_y)):
            best_cnt = cnt
            best_y = y

    print(best_y)

if __name__ == "__main__":
    solve()
```

The solution isolates the intercept $b$ immediately and ignores $k$ entirely since it has no effect on intersections with the y-axis. The frequency dictionary aggregates occurrences in linear time. The final scan over the dictionary ensures correct selection under both primary and secondary ordering conditions.

Care must be taken in initialization: `best_y` starts as `None` so that the first encountered value is always accepted, and comparisons correctly handle the tie-breaking rule.

## Worked Examples

### Example 1

Input:

```
3
3 1
0 0
-10 1
```

We process intercepts and build frequencies.

| Step | b | freq[b] after update |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 0 | 1 |
| 3 | 1 | 2 |

Now evaluate best candidate:

| y | count | best_y | best_cnt | decision |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 | initialize |
| 0 | 1 | 1 | 2 | ignored |

Output is 1.

This confirms that repeated intercepts correctly accumulate and dominate smaller singleton values.

### Example 2

Input:

```
4
1 5
2 3
3 3
4 5
```

Frequencies:

| Step | b | freq[b] after update |
| --- | --- | --- |
| 1 | 5 | 1 |
| 2 | 3 | 1 |
| 3 | 3 | 2 |
| 4 | 5 | 2 |

Now selection:

| y | count | best_y | best_cnt | decision |
| --- | --- | --- | --- | --- |
| 5 | 2 | 5 | 2 | initialize |
| 3 | 2 | 3 | 2 | tie, smaller wins |

Output is 3.

This demonstrates correct tie-breaking behavior when multiple y-values share the same maximum frequency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each line is processed once and dictionary aggregation is constant amortized time |
| Space | $O(n)$ | Frequency map may store all distinct intercepts |

With $n \le 10^5$, linear time and memory usage comfortably fit within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import builtins
    input_backup = builtins.input

    def fake_input():
        return sys.stdin.readline().rstrip("\n")

    builtins.input = fake_input

    try:
        solve()
        return output.getvalue().strip()
    finally:
        builtins.input = input_backup
        sys.stdout = sys.__stdout__

# sample-like cases
assert run("3\n3 1\n0 0\n-10 1\n") == "1"
assert run("3\n1 1\n2 2\n3 2\n") == "2"

# all equal
assert run("4\n1 7\n2 7\n3 7\n4 7\n") == "7"

# tie-breaking
assert run("4\n1 5\n2 3\n3 3\n4 5\n") == "3"

# single element
assert run("1\n10 42\n") == "42"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same b | single value | uniform frequency handling |
| mixed tie | smallest y chosen | correct tie-breaking |
| single line | direct output | base case correctness |

## Edge Cases

One edge case is when all lines share the same intercept. For example:

```
3
1 10
2 10
3 10
```

The frequency map becomes `{10: 3}`, and the algorithm selects 10 immediately as both maximum and only candidate. No tie logic is triggered, confirming that the initialization path is correct.

Another case is alternating intercepts:

```
6
1 1
2 2
3 1
4 2
5 3
6 3
```

Frequencies are all equal. The algorithm scans entries in arbitrary dictionary order, but tie-breaking ensures the smallest value is selected. Even if iteration order is unpredictable, comparisons enforce deterministic selection of 1.

A final case is minimal input:

```
1
100 -5
```

The map contains only `-5`, so it is selected directly. This confirms correctness when no comparison step meaningfully occurs.
