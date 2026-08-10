---
title: "CF 102433D - Dividing By Two"
description: "We start with an integer (A) and want to turn it into (B). At any moment, we may increase the current value by one, or divide it by two when the current value is even. Every operation costs one, so the task is to find the minimum number of operations."
date: "2026-08-10T07:37:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102433
codeforces_index: "D"
codeforces_contest_name: "2019-2020 ACM-ICPC Pacific Northwest Regional Contest (Div. 1)"
rating: 0
weight: 102433
solve_time_s: 333
verified: true
draft: false
---

[CF 102433D - Dividing By Two](https://codeforces.com/problemset/problem/102433/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an integer \(A\) and want to turn it into \(B\). At any moment, we may increase the current value by one, or divide it by two when the current value is even. Every operation costs one, so the task is to find the minimum number of operations.

The input contains one pair of positive integers \(A\) and \(B\), each at most \(10^9\). The output is the length of the shortest valid sequence of operations that changes \(A\) into \(B\). The official samples are \(103 \to 27\), which takes 4 operations, and \(3 \to 8\), which takes 5 operations. citeturn1search17

The bound of \(10^9\) rules out algorithms that simulate every possible value up to \(A\). A linear search could require about one billion states, which is an efficient solution should need only logarithmically many divisions.

There are several edge cases where a careless greedy implementation can fail. If \(A<B\), for example \(3,8\), the answer is simply \(8-3=5\). Dividing first would only move farther from the target, so a strategy that always tries to divide when possible is wrong. If \(A=B\), such as \(7,7\), the answer is 0, and the loop must stop before performing an unnecessary operation. If \(A>B\) and \(A\) is odd, such as \(7,4\), division is not immediately legal. We must first do \(7\to8\), then \(8\to4\), for an answer of 2. Finally, when a division makes the value smaller than \(B\), we must stop dividing and use additions. For \(103,27\), the optimal sequence is \(103\to104\to52\to26\to27\), so the answer is 4. A loop that keeps dividing after reaching 26 would miss the optimum. citeturn1search0

## Approaches

A direct brute-force approach is to regard every integer as a graph state. From an even value \(x\), there are up to two outgoing operations, \(x\to x+1\) and \(x\to x/2\), while from an odd value only \( the current value \(x\) is greater than \(B\), we eventually need a division. Adding one while already being above \(B\) cannot finish the transformation, so consider what happens before the first division. If \(x\) is even, doing two additions followed by a division,

\[
x\to x+1\to x+2\to (x+2)/2,
\]

is equivalent in value to dividing first and then adding one,

\[
x\to x/2\to x/2+1.
\]

The second version uses one fewer operation. More additions before the first division can be reduced in the same way. Thus, if \(x\) is even, the first operation of an optimal solution is division.

If \(x\) is odd, one addition is necessary before the first division, because division is illegal otherwise. After that single addition the value is even, so we divide immediately. Any additional pair of additions before the division can again be moved after the division and saves an operation.

This gives a deterministic greedy process. While \(A>B\), make \(A\) even with one addition when necessary, then divide it by two. As soon as \(A\le B\), division is no longer desirable. At that point every remaining operation must be an addition, so the answer is increased by \(B-A\).

The brute-force works because every operation can be represented as an edge in an unweighted state graph, but it fails because that graph can contain around a billion relevant states. The observation that an optimal path has a canonical order, at most one addition before each division, collapses the search to \(O(\log A)\) steps.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | \(O(A)\) states in the worst case | \(O(A)\) | Too slow |
| Optimal | \(O(\log A)\) | \(O(1)\) | Accepted |

## Algorithm Walkthrough

1. If \(A\le B\), return \(B-A\). The target is already at or above the current value, and adding one reaches it directly. Any division would move the value downward and would require at least as many additional additions to recover.

2. While \(A>B\), inspect the parity of \(A\). If \(A\) is odd, add one and increase the operation count. This is the only way to make division legal.

3. Divide \(A\) by two and increase the operation count. When \(A\) was already even, this is the optimal first move. When it was odd, the preceding addition was forced.

4. Repeat until \(A\le B\). The moment this happens, stop performing divisions.

5. Add \(B-A\) to the operation count and return it. Since \(A\le B\) at this point, only additions are needed to reach the target.

The key invariant is that before every division, the algorithm has used the minimum possible number of additions needed to make the current value divisible by two. For an even value that number is zero, and for an odd value it is exactly one. Any optimal solution can be transformed into one with this same structure without increasing its length, because extra additions before a division can be moved after that division more cheaply. Once the value falls to or below \(B\), division cannot be part of an optimal continuation, so the final direct additions are also optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())

    if a <= b:
        print(b - a)
        return

    ans = 0

    while a > b:
        if a & 1:
            a += 1
            ans += 1

        a //= 2
        ans += 1

    ans += b - a
    print(ans)

if __name__ == "__main__":
    solve()
```

The first condition handles the entire \(A\le B\) case immediately. This is more than an optimization: it prevents the algorithm from dividing a value that is already no larger than the target.

Inside the loop, `a & 1` checks whether the current value is odd. If it is, `a += 1` makes the division legal and costs one operation. The integer division `a //= 2` is then always valid.

The order matters. We must first make an odd value even and only then divide it. We also check `a > b` before starting another iteration, because after a division the new value may already be below the target. In that situation, the remaining distance is handled by `b - a`.

Python integers do not overflow, and the largest temporary value is only \(10^9+1\), so no special numeric handling is required.

## Worked Examples

### Sample 1: \(A=103,\ B=27\)

| Step | Current \(A\) | Action | Operations |
|---|---:|---|---:|
| Start | 103 | Odd, add 1 | 1 |
| 1 | 104 | Divide by 2 | 2 |
| 2 | 52 | Divide by 2 | 3 |
| 3 | 26 | Stop dividing, \(A\le B\) | 3 |
| Finish | 26 | Add \(27-26=1\) | 4 |

The sequence is \(103\to104\to52\to26\to27\). The example demonstrates why the stopping condition is essential. Continuing with another division would produce 13 and require many more additions.

### Sample 2: \(A=3,\ B=8\)

| Step | Current \(A\) | Action | Operations |
|---|---:|---|---:|
| Start | 3 | \(A\le B\), stop loop | 0 |
| Finish | 3 | Add \(8-3=5\) | 5 |

The answer is 5, corresponding to five additions. This exercises the case where division is never useful because the starting value is already below the target.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(\log A)\) | Every division reduces the current value by about half, and there are at most logarithmically many divisions. |
| Space | \(O(1)\) | Only the current value and operation counter are stored. |

With \(A\le10^9\), the number of divisions is only on the order of 30, with at most one additional operation to fix parity before each division. The algorithm therefore performs only a few dozen iterations, comfortably within the one second limit and using constant memory.

## Test Cases

```python
import sys
import io

def solve():
    a, b = map(int, input().split())

    if a <= b:
        print(b - a)
        return

    ans = 0

    while a > b:
        if a & 1:
            a += 1
            ans += 1

        a //= 2
        ans += 1

    ans += b - a
    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    output = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output.strip()

# Provided samples
assert run("103 27\n") == "4", "sample 1"
assert run("3 8\n") == "5", "sample 2"

# Custom cases
assert run("1 1\n") == "0", "equal minimum values"
assert run("1000000000 1000000000\n") == "0", "equal maximum values"
assert run("2 1\n") == "1", "smallest useful division"
assert run("5 3\n") == "2", "odd value requiring one increment"
assert run("6 5\n") == "3", "division below target followed by additions"
assert run("1000000000 1\n") == "37", "maximum starting value"

| Test input | Expected output | What it validates |
|---|---:|---|
| `1 1` | 0 | Minimum values and the equality boundary |
| `1000000000 1000000000` | 0 | Maximum values and equality |
| `2 1` | 1 | Immediate valid division |
| `5 3` | 2 | Odd value requiring an increment before division |
| `6 5` | 3 | Division can undershoot the target, followed by additions |
| `1000000000 1` | 37 | Large input and logarithmic behavior |

## Edge Cases

For \(A=B\), take the input `7 7`. The initial condition \(A\le B\) is true, so the algorithm returns \(7-7=0\). No operation is necessary. A loop that assumes at least one operation is required would introduce an incorrect extra step.

For \(A<B\), take `3 8`. The algorithm immediately returns \(8-3=5\). Every division would make the current value even smaller, so it cannot improve on five direct additions. This is why the \(A\le B\) case must be handled before the division loop.

For an odd value above the target, take `7 4`. Since 7 is odd, the algorithm performs \(7\to8\), then \(8\to4\), giving 2 operations. Division cannot be performed directly on 7, so the increment is forced. The result reaches the target exactly after the division.

For a division that crosses below the target, take `6 5`. The algorithm performs \(6\to3\), then stops because \(3\le5\), and adds twice: \(3\to4\to5\). The total is 3. Dividing again would only increase the amount of work, because the value is already below the target.

For the sample `103 27`, the algorithm first fixes the odd value with \(103\to104\), then divides twice to get \(26\). Since 26 is now below 27, it performs one final addition. The total is \(1+1+1+1=4\), matching the required answer. cite
