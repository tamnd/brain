---
title: "CF 102861G - Game Show!"
description: "The game starts with Ricardo having a balance of 100 sbecs. The boxes are arranged in a fixed order, and he may open some prefix of them. After opening a box, its hidden value is added to the current balance."
date: "2026-07-25T14:04:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102861
codeforces_index: "G"
codeforces_contest_name: "2020-2021 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102861
solve_time_s: 35
verified: true
draft: false
---

[CF 102861G - Game Show!](https://codeforces.com/problemset/problem/102861/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The game starts with Ricardo having a balance of 100 sbecs. The boxes are arranged in a fixed order, and he may open some prefix of them. After opening a box, its hidden value is added to the current balance. At any moment he may stop and take the current amount, including before opening any box at all.

The task is to find the maximum balance achievable by choosing the best stopping point. Since opening exactly the first k boxes gives a balance of 100 plus the sum of those k values, the problem is equivalent to finding the best prefix sum, while also allowing the empty prefix.

The input contains the number of boxes followed by the value inside each box in order. The output is the largest final balance Ricardo can obtain.

The number of boxes is at most 100, and every value is between -1000 and 1000. These limits are small enough that even simple linear processing is more than sufficient. A quadratic approach would still pass for this particular bound, but the structure of the problem gives a direct one-pass solution. There is no need for complex data structures because each box only affects future choices through the current accumulated balance.

The main edge case is a sequence where every box is negative. A careless implementation might assume Ricardo must open at least one box and return the least damaging loss. For example:

```
3
-5
-2
-8
```

The correct output is `100`, because Ricardo can quit immediately. An approach that only checks non-empty prefixes would incorrectly return `95`.

Another edge case is when the best answer happens after several negative boxes. For example:

```
4
-10
-10
30
-100
```

The correct output is `110`, because opening the first three boxes gives a net gain of 10. A method that stops whenever the current sum becomes negative would fail, because it would discard a prefix that later becomes profitable.

## Approaches

A direct brute-force solution would simulate every possible decision. Since Ricardo can stop after any number of opened boxes, we could try every possible stopping position, calculate the balance at that point, and keep the maximum. There are C + 1 possible stopping positions, including stopping immediately. If each one recomputes the prefix sum from the beginning, the total work is O(C²). With C = 100 this is acceptable, but it ignores the fact that every consecutive stopping position shares almost all of its information with the previous one.

The useful observation is that the only changing value while moving through the boxes is the current balance. After opening the next box, the new balance is simply the old balance plus that box value. We can scan the boxes once, updating the current balance and remembering the largest value seen so far. This works because every possible final state corresponds exactly to one point during this scan.

The brute-force method works because every possible stopping choice is examined, but it repeats the same prefix calculations many times. The observation that each next choice differs only by adding one new value reduces the problem to a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C²) | O(1) | Accepted for given limits, but unnecessary |
| Optimal | O(C) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the current balance equal to 100 and the answer equal to 100. The initial answer represents the option of quitting before opening any box.
2. Read each box value in order and add it to the current balance. The current balance now represents the amount Ricardo would receive if he stopped after opening this box.
3. Compare the current balance with the best answer found so far and keep the larger value. Every stopping position is considered exactly once during the scan.
4. After all boxes have been processed, output the stored maximum balance.

Why it works:

After processing the first i boxes, the current balance is exactly the amount Ricardo would have after opening those i boxes. The algorithm stores the maximum balance among all stopping points from 0 through i. When the next box is processed, the new stopping point is added to this set of possibilities, and the maximum is updated if needed. By the time all boxes are processed, every possible strategy has been considered, so the stored answer is the optimal final balance.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    c = int(input())
    balance = 100
    answer = 100

    for _ in range(c):
        balance += int(input())
        if balance > answer:
            answer = balance

    print(answer)

if __name__ == "__main__":
    solve()
```

The variable `balance` stores the amount Ricardo would have if he continues opening boxes up to the current position. It starts at 100 because choosing zero boxes is a valid strategy.

The variable `answer` stores the best balance among all stopping points seen so far. Initializing it to 100 handles the case where every box is harmful and Ricardo should never open one.

The loop processes each box exactly once. The update happens before comparing with `answer`, because opening the current box creates a new possible stopping point. Python integers do not overflow for the given limits, so no special handling is needed.

There is no indexing involved, which avoids off-by-one mistakes. The algorithm naturally handles the last box because it checks the balance immediately after every addition.

## Worked Examples

For the first example, using the values:

```
4
-1
-2
-3
-4
```

the trace is:

| Step | Box Value | Current Balance | Best Answer |
| --- | --- | --- | --- |
| Start | none | 100 | 100 |
| 1 | -1 | 99 | 100 |
| 2 | -2 | 97 | 100 |
| 3 | -3 | 94 | 100 |
| 4 | -4 | 90 | 100 |

The trace shows why the empty prefix matters. Every opened box decreases the balance, so the optimal choice is to stop immediately.

For the second example:

```
3
-10
-30
-50
```

the trace is:

| Step | Box Value | Current Balance | Best Answer |
| --- | --- | --- | --- |
| Start | none | 100 | 100 |
| 1 | -10 | 90 | 100 |
| 2 | -30 | 60 | 100 |
| 3 | -50 | 10 | 100 |

This confirms that a sequence of negative values does not force Ricardo to lose money because he can always choose not to begin.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(C) | Each box is read and processed once |
| Space | O(1) | Only the current balance and answer are stored |

The maximum number of boxes is only 100, so this linear solution easily fits within the required limits. Its constant memory usage also makes it suitable for much larger versions of the same problem.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# provided samples
assert run("4\n-1\n-2\n-3\n-4\n") == "100\n", "sample 1"
assert run("3\n-10\n-30\n-50\n") == "100\n", "sample 2"

# custom cases
assert run("1\n0\n") == "100\n", "single zero value"
assert run("5\n5\n-20\n30\n-10\n-100\n") == "115\n", "best prefix in the middle"
assert run("3\n1000\n1000\n1000\n") == "3100\n", "maximum positive growth"
assert run("100\n-1000\n" * 100) == "100\n", "maximum size all negative input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One zero box | 100 | The algorithm keeps the initial balance when nothing improves |
| Mixed positive and negative values | 115 | The best stopping point can occur before the end |
| All positive values | 3100 | The algorithm continues through every profitable box |
| 100 negative boxes | 100 | The solution handles the largest input and the empty prefix case |

## Edge Cases

For the all-negative case:

```
3
-5
-2
-8
```

the algorithm begins with `balance = 100` and `answer = 100`. After each addition, the balance becomes 95, 93, and 85. None of these values improve the answer, so the final result remains 100. This matches the strategy of quitting before opening any box.

For the case where a temporarily bad prefix becomes the best choice:

```
4
-10
-10
30
-100
```

the balances during the scan are 90, 80, 110, and 10. The algorithm keeps the maximum seen value, so when it reaches 110 after the third box, that value becomes the answer. The final negative box cannot remove the fact that stopping earlier was already a valid choice.

For the minimum-size input:

```
1
-50
```

the algorithm checks the only possible opened-box result, 50, against the initial option of 100. The final answer is 100, confirming that a single harmful box does not need to be opened.

I can also adapt this into a shorter Codeforces-style editorial format if you want something closer to what would appear on the contest page.
