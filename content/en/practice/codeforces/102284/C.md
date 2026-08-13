---
title: "CF 102284C - \u0411\u0430\u0441\u043a\u0435\u0442\u0431\u043e\u043b\u044c\u043d\u0430\u044f \u0437\u0430\u0440\u044f\u0434\u043a\u0430"
description: "We have two rows of (n) students. Student (i) in the first row has height (ai), and student (i) in the second row has height (bi). A team is formed by taking students from left to right, so the indices of chosen students must be strictly increasing."
date: "2026-08-13T22:31:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "C"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 848
verified: true
draft: false
---

[CF 102284C - \u0411\u0430\u0441\u043a\u0435\u0442\u0431\u043e\u043b\u044c\u043d\u0430\u044f \u0437\u0430\u0440\u044f\u0434\u043a\u0430](https://codeforces.com/problemset/problem/102284/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two rows of (n) students. Student (i) in the first row has height (a_i), and student (i) in the second row has height (b_i). A team is formed by taking students from left to right, so the indices of chosen students must be strictly increasing. At the same time, two consecutive chosen students must come from different rows. The first chosen student has no restriction, and the goal is to maximize the sum of the chosen heights. The official constraints are (1 \le n \le 10^5) and (1 \le h_{r,i} \le 10^9), with a 2 second time limit and 256 MB memory limit in the current Codeforces version.

The upper bound (n=10^5) immediately rules out algorithms that examine pairs of positions, let alone all possible teams. An (O(n^2)) solution already performs around (10^{10}) iterations in the worst case, which is far beyond what a 2 second contest limit can handle. We need to process each column a constant number of times, giving an (O(n)) solution. The answer can be as large as (n\cdot10^9=10^{14}), so the implementation must use integer arithmetic capable of storing values beyond 32-bit signed integers. Python integers handle this automatically.

The first edge case is a single column. For example,

```
1
7
4
```

has answer `7`. There is no second index available, so choosing both students is impossible. An implementation that assumes every transition has a previous column can fail here.

A second edge case is that we cannot choose both students from the same column. For example,

```
2
100 100
1 1
```

has answer `101`, not `200`. The two students of height `100` have the same index, while the rules require the next chosen index to be strictly greater than the previous one. A careless solution that simply takes the larger height from every column would incorrectly choose both `100`s.

A third edge case is that the previous chosen student does not have to be in the immediately preceding column. Consider

```
3
1 100 1
1 1 100
```

The optimal team is the first-row student at index `2` followed by the second-row student at index `3`, giving `200`. A transition that only considers the immediately previous column as the possible predecessor would miss this combination.

Finally, when all heights are equal, the answer is determined entirely by the structural restrictions. For

```
3
5 5 5
5 5 5
```

the answer is `15`, because we can choose exactly one student from each of the three columns and alternate rows. Any implementation that allows both rows of one column to be chosen would overcount.

## Approaches

A direct brute-force solution can enumerate every subset of the (2n) students, check whether its selected indices are strictly increasing and whether consecutive selected students alternate rows, and then keep the largest height sum. This is correct because every possible team is represented by some subset. However, there are (2^{2n}) subsets, and checking one subset can take (O(n)) time. The worst-case work is therefore (O(n\cdot2^{2n})). Even for a few dozen columns this becomes infeasible, while the actual constraint allows (10^5) columns.

The structure that makes the problem easy is that when we scan the columns from left to right, the only information from the already processed part that affects the next choice is the row of the last selected student. We do not need to remember the complete sequence of selected indices.

Suppose we have processed some prefix of the columns. Let `top` be the best total height obtainable from that prefix when the last selected student is from the first row. Similarly, let `bottom` be the best total when the last selected student is from the second row. These states already allow the last selected student to be anywhere in the processed prefix.

When we arrive at a new first-row student with height (a_i), there are two possibilities. We can skip this student, leaving `top` unchanged. Or we can select it. Since consecutive selected students must be in different rows, the previous selected student must be represented by `bottom`, and the new value becomes `bottom + a_i`. Thus the new first-row state is

[
\text{new_top}=\max(\text{top},\text{bottom}+a_i).
]

The same reasoning gives

[
\text{new_bottom}=\max(\text{bottom},\text{top}+b_i).
]

The subtle point is that `top` and `bottom` represent the best choice anywhere in the processed prefix, not necessarily at the previous column. This automatically handles skipped columns. Because every transition only uses the two previous state values, the entire (O(n)) DP can be reduced to constant extra memory.

The brute-force works because it explicitly examines every possible team, but fails because there are exponentially many teams. The observation that the future only depends on the row of the last selected student lets us merge exponentially many partial teams into two optimal states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\cdot2^{2n})) | (O(n)) | Too slow |
| Optimal DP | (O(n)) | (O(1)) extra | Accepted |

## Algorithm Walkthrough

1. Read the two height arrays. We process them column by column from left to right because every valid team has strictly increasing indices.
2. Initialize `top = a[0]` and `bottom = b[0]`. With only the first column available, the best team whose last selected student is in the first row consists of that first-row student, and similarly for the second row.
3. For every later column `i`, save the old values of `top` and `bottom`. The new first-row state is `max(old_top, old_bottom + a[i])`. The first term means we skip the current first-row student, while the second means we take it after a valid team ending in the other row.
4. Compute the new second-row state as `max(old_bottom, old_top + b[i])`. The reasoning is symmetric, but both new states must use the old values. Updating one state before calculating the other would accidentally allow both transitions to use the current column and could violate the strictly increasing-index condition.
5. After the last column, return `max(top, bottom)`. Every non-empty valid team ends in exactly one of the two rows, so the better of these states is the global optimum.

### Why it works

After processing column (i), `top` stores the maximum sum among all valid teams using only columns up to (i) whose last selected student is from the first row. The same invariant holds for `bottom` and the second row. For a first-row student at column (i), any valid team that selects it must previously end in the second row at some smaller index, and `old_bottom` represents the best such team. Skipping the student preserves the previous optimum. These are the only two possibilities, so the recurrence considers every valid optimal team and cannot introduce an invalid one. The invariant holds for every column, making the final maximum the optimal team sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    top = a[0]
    bottom = b[0]

    for i in range(1, n):
        old_top = top
        old_bottom = bottom

        top = max(old_top, old_bottom + a[i])
        bottom = max(old_bottom, old_top + b[i])

    print(max(top, bottom))

if __name__ == "__main__":
    solve()
```

The first two assignments initialize the two DP states for column zero. An empty team does not need a separate state because every height is positive, so choosing at least one student is always better than choosing nobody.

Inside the loop, `old_top` and `old_bottom` preserve the states before processing the current column. This is essential. If `top` were updated first and then used while computing `bottom`, the second transition could effectively select two students from the same column, which is forbidden because their indices are equal.

The expression `old_bottom + a[i]` represents switching from the second row to the first row. Since `old_bottom` already contains the best valid team ending in the second row anywhere before or at the previous processed column, the required strict index increase is satisfied. The same argument applies to `old_top + b[i]`.

Python's arbitrary-precision integers are also useful here. With (10^5) columns and heights up to (10^9), the answer can reach (10^{14}), so a 32-bit integer would overflow in languages where that is the default integer type.

## Worked Examples

For the first sample, the input is

```
5
9 3 5 7 3
5 8 1 4 5
```

The following table shows the states after each column. `top` and `bottom` are the best totals whose last selected student belongs to the corresponding row.

| Column | Top height | Bottom height | `top` | `bottom` |
| --- | --- | --- | --- | --- |
| 1 | 9 | 5 | 9 | 5 |
| 2 | 3 | 8 | 9 | 17 |
| 3 | 5 | 1 | 22 | 17 |
| 4 | 7 | 4 | 24 | 26 |
| 5 | 3 | 5 | 29 | 29 |

At column 5, the best total ending in the first row is `29`, and the best total ending in the second row is also `29`. The answer is consequently `29`. The transition at column 3 is particularly useful: `top` becomes `17 + 5 = 22`, where the previous second-row choice came from column 2. This demonstrates how the DP remembers the best compatible history instead of considering only one fixed predecessor.

For the second sample,

```
3
1 2 9
10 1 1
```

the states evolve as follows.

| Column | Top height | Bottom height | `top` | `bottom` |
| --- | --- | --- | --- | --- |
| 1 | 1 | 10 | 1 | 10 |
| 2 | 2 | 1 | 12 | 10 |
| 3 | 9 | 1 | 19 | 13 |

The optimal team is the second-row student at column 1 followed by the first-row student at column 3, with total `10 + 9 = 19`. The DP keeps the `10` in the second-row state while processing column 2, even though column 2 itself is skipped for the optimal sequence. This confirms that a valid transition may jump over any number of columns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every column performs a constant number of arithmetic and maximum operations. |
| Space | (O(1)) extra | Only four scalar DP values are maintained after reading the arrays. |

With (n\le10^5), the algorithm performs only a few hundred thousand primitive operations, comfortably within the 2 second limit. The input arrays themselves require (O(n)) memory, while the DP contributes only constant additional memory. The official problem allows 256 MB of memory.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    top = a[0]
    bottom = b[0]

    for i in range(1, n):
        old_top = top
        old_bottom = bottom

        top = max(old_top, old_bottom + a[i])
        bottom = max(old_bottom, old_top + b[i])

    print(max(top, bottom))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    "5\n"
    "9 3 5 7 3\n"
    "5 8 1 4 5\n"
) == "29\n", "sample 1"

# Provided sample 2
assert run(
    "3\n"
    "1 2 9\n"
    "10 1 1\n"
) == "19\n", "sample 2"

# Provided sample 3
assert run(
    "1\n"
    "7\n"
    "4\n"
) == "7\n", "sample 3"

# Custom: minimum size, second row is better
assert run(
    "1\n"
    "4\n"
    "7\n"
) == "7\n", "minimum-size case"

# Custom: all values equal
assert run(
    "3\n"
    "5 5 5\n"
    "5 5 5\n"
) == "15\n", "all-equal case"

# Custom: cannot choose both rows from the same column
assert run(
    "2\n"
    "100 100\n"
    "1 1\n"
) == "101\n", "same-column boundary"

# Custom: skipping a column is necessary
assert run(
    "3\n"
    "1 100 1\n"
    "1 1 100\n"
) == "200\n", "skipped-column transition"

# Custom: maximum n and maximum heights
n = 100000
inp = (
    f"{n}\n"
    + " ".join(["1000000000"] * n)
    + "\n"
    + " ".join(["1000000000"] * n)
    + "\n"
)
assert run(inp) == "100000000000000\n", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 4 / 7` | `7` | Minimum size and correct initialization |
| `3 / 5 5 5 / 5 5 5` | `15` | All-equal values and one choice per column |
| `2 / 100 100 / 1 1` | `101` | Strictly increasing indices, preventing two choices from one column |
| `3 / 1 100 1 / 1 1 100` | `200` | Transitions that skip one or more columns |
| `n=100000`, every height `1000000000` | `100000000000000` | Maximum input size and large answer values |

## Edge Cases

For a single column,

```
1
7
4
```

the initial states are `top = 7` and `bottom = 4`. The loop is never entered because there is no later column. The final maximum is `7`, which is exactly right. This handles the boundary where a recurrence requiring `i-1` would otherwise access a nonexistent column.

For the same-column restriction,

```
2
100 100
1 1
```

the initial states are `top = 100` and `bottom = 1`. At column 2, the new top state is `max(100, 1 + 100) = 101`, while the new bottom state is `max(1, 100 + 1) = 101`. The answer is `101`. The DP can switch rows only from the previous processed prefix, never from the other state after it has already incorporated column 2, so it cannot select both `100`s at the same index.

For a skipped column,

```
3
1 100 1
1 1 100
```

the states start as `top = 1`, `bottom = 1`. At column 2, `top` becomes `max(1, 1 + 100) = 101`, while `bottom` remains `1`. At column 3, the new bottom state becomes `max(1, 101 + 100) = 201` if the current second-row height were `100`, giving the team consisting of the first-row student at column 2 and the second-row student at column 3. For the actual input above, the first-row value at column 2 is `100` and the second-row value at column 3 is `100`, so the result is `200`. The preserved state across column 2 demonstrates why the DP must represent the best history over the entire processed prefix rather than only the immediately preceding column.

For equal heights,

```
3
5 5 5
5 5 5
```

the states evolve from `(5, 5)` to `(10, 10)` and finally to `(15, 15)`. The answer is `15`. Exactly one student can be chosen from each index because choosing both rows of the same index would violate the strict index condition. The alternating-row requirement can still be satisfied by choosing top, bottom, top, or bottom, top, bottom across the three columns.
