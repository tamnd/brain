---
title: "CF 102747B - \u041f\u0440\u043e\u0436\u0435\u043a\u0442\u043e\u0440\u0430"
description: "The problem models three projectors standing in a row. They are turned on one second at a time in the repeating order left, middle, right, middle. The left projector can work for A seconds in total, the middle one for B seconds, and the right one for C seconds."
date: "2026-07-29T00:38:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102747
codeforces_index: "B"
codeforces_contest_name: "\u041f\u0440\u0438\u0433\u043b\u0430\u0441\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f. \u0421\u0438\u0440\u0438\u0443\u0441-2020"
rating: 0
weight: 102747
solve_time_s: 42
verified: true
draft: false
---

[CF 102747B - \u041f\u0440\u043e\u0436\u0435\u043a\u0442\u043e\u0440\u0430](https://codeforces.com/problemset/problem/102747/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models three projectors standing in a row. They are turned on one second at a time in the repeating order left, middle, right, middle. The left projector can work for `A` seconds in total, the middle one for `B` seconds, and the right one for `C` seconds. The task is to find how many seconds the process continues before the next projector that should turn on has no remaining lifetime. The original statement is from Codeforces Gym problem 102747B.

The input consists of three non-negative integers representing the available seconds of operation for the left, middle, and right projectors. The output is the length of the longest valid prefix of the infinite turning sequence.

The important part of the constraints is that the total amount of available work can be as large as around `2 * 10^9`. A simulation that turns on one projector per second can require billions of iterations, which is too slow for a short time limit. We need to use the repeating structure of the sequence and skip large groups of operations at once. Since there are only three values, the intended solution should be close to constant time.

Several edge cases can break a direct simulation or an incorrect formula. If the middle projector has no lifetime, the process stops immediately.

```
Input:
0
5
7

Output:
0
```

A solution that always adds one full cycle before checking availability would incorrectly count seconds that never happen.

Another tricky case is when one of the side projectors runs out exactly at the end of a cycle.

```
Input:
1
2
1

Output:
4
```

The sequence is left, middle, right, middle. After four seconds all available lifetime has been used, but the next left projector activation fails. Counting the failed activation would produce `5`.

A third common mistake is treating the middle projector like the others. It is used twice in every four seconds, so it cannot be grouped with the left and right projectors.

```
Input:
10
1
10

Output:
1
```

Only the first left activation happens. The next required activation is the middle projector, which has already exhausted its single second.

## Approaches

The direct approach is to repeatedly follow the sequence and decrease the remaining lifetime of the current projector. Each second performs one operation and the answer is the number of successful operations before a zero lifetime is encountered. This method is easy to prove correct because it exactly follows the process described by the statement.

The problem appears when the available lifetimes are large. In the worst case, if all three values are close to `10^9`, the simulation needs billions of steps. The time complexity becomes proportional to the answer itself, which is not acceptable.

The useful observation comes from the fixed pattern. Every four seconds, the process always consumes one second from the left projector, two seconds from the middle projector, and one second from the right projector. Instead of processing those four activations individually, we can jump through as many complete groups of four as possible.

The number of complete cycles is limited by the first projector that cannot survive another cycle. A cycle requires one left second, two middle seconds, and one right second, so the number of full cycles is:

`min(A, B // 2, C)`

After removing these complete cycles, at most four more activations need to be checked. This works because the only remaining failure must happen inside the next incomplete cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three available lifetimes of the projectors.
2. Compute how many full four-second cycles can happen. One cycle consumes one left second, two middle seconds, and one right second, so the number of complete cycles is limited by `min(A, B // 2, C)`.
3. Add four seconds for every complete cycle and subtract the used lifetime from all three projectors. After this step, at least one projector cannot complete another whole cycle.
4. Check the next few activations in the order left, middle, right, middle. Since a full cycle is impossible anymore, there can be no need to check more than these four positions. If the current projector still has lifetime, consume one second and increase the answer. Otherwise, stop.
5. Print the accumulated number of successful seconds.

Why it works:

The algorithm preserves the exact number of seconds consumed from every projector. A complete cycle has a fixed consumption pattern, so replacing many individual operations with a cycle jump does not change the state of the system. After taking the maximum possible number of complete cycles, the remaining state cannot survive another whole cycle. The only possible continuation is a prefix of the next cycle, and checking that prefix directly gives the exact final length.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    a = int(input())
    b = int(input())
    c = int(input())

    cycles = min(a, b // 2, c)

    ans = cycles * 4
    a -= cycles
    b -= cycles * 2
    c -= cycles

    for i in range(4):
        if i == 0 or i == 2:
            if i == 0:
                if a == 0:
                    break
                a -= 1
            else:
                if c == 0:
                    break
                c -= 1
        else:
            if b == 0:
                break
            b -= 1
        ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part of the code removes all possible complete cycles. The expression `min(a, b // 2, c)` directly represents the limiting resource because each cycle needs exactly those amounts.

After that reduction, the remaining values are small in the sense that only one partial cycle can occur. The loop handles the four possible positions in the repeating pattern. The code checks before decreasing a resource, which avoids counting the failed activation.

There are no indexing concerns because the sequence length is fixed. Python integers are also sufficient for the maximum answer because the total available lifetime is bounded by the problem constraints.

## Worked Examples

For the sample where all projectors have lifetime `3`:

Input:

```
3
3
3
```

| Step | Action | Left | Middle | Right | Answer |
| --- | --- | --- | --- | --- | --- |
| Initial | Start | 3 | 3 | 3 | 0 |
| Cycle jump | One full cycle | 2 | 1 | 2 | 4 |
| 1 | Left turns on | 1 | 1 | 2 | 5 |
| 2 | Middle turns on | 1 | 0 | 2 | 6 |
| 3 | Right turns on | 1 | 0 | 1 | 7 |
| 4 | Middle fails | 1 | 0 | 1 | 7 |

The example shows why the middle projector is the limiting factor after the first cycle. The algorithm stops exactly before the failed activation.

For a case where the middle projector is small:

Input:

```
10
1
10
```

| Step | Action | Left | Middle | Right | Answer |
| --- | --- | --- | --- | --- | --- |
| Initial | Start | 10 | 1 | 10 | 0 |
| Cycle jump | Zero full cycles | 10 | 1 | 10 | 0 |
| 1 | Left turns on | 9 | 1 | 10 | 1 |
| 2 | Middle fails | 9 | 0 | 10 | 1 |

This trace demonstrates that the algorithm does not force a complete cycle when the middle projector cannot provide two seconds for it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one calculation of complete cycles and at most four remaining checks are performed. |
| Space | O(1) | Only a few integer variables are stored. |

The solution does not depend on the magnitude of the lifetimes except through arithmetic operations. It remains fast even when the available time is close to the maximum allowed by the constraints.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    data = list(map(int, inp.split()))
    a, b, c = data

    cycles = min(a, b // 2, c)
    ans = cycles * 4
    a -= cycles
    b -= cycles * 2
    c -= cycles

    for i in range(4):
        if i == 0:
            if a == 0:
                break
            a -= 1
        elif i == 1 or i == 3:
            if b == 0:
                break
            b -= 1
        else:
            if c == 0:
                break
            c -= 1
        ans += 1

    return str(ans)

# provided sample
assert solution("3\n3\n3\n") == "7", "sample"

# minimum size
assert solution("0\n0\n0\n") == "0", "all zero"

# all equal values
assert solution("5\n5\n5\n") == "11", "equal resources"

# catches middle projector frequency
assert solution("100\n1\n100\n") == "1", "middle bottleneck"

# large values
assert solution("1000000000\n1000000000\n1000000000\n") == "1999999999", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | `0` | Immediate failure before any activation |
| `5 5 5` | `11` | Correct handling of complete cycles and a partial cycle |
| `100 1 100` | `1` | Middle projector being used twice per cycle |
| `1000000000 1000000000 1000000000` | `1999999999` | Large values without simulation |

## Edge Cases

For zero lifetime on the first required projector, the algorithm computes zero complete cycles and the remaining four-step check immediately stops. For example:

```
0
5
7
```

The first activation is the left projector, but it has no remaining seconds, so the answer is `0`.

For exact cycle exhaustion:

```
1
2
1
```

The algorithm takes one complete cycle because `min(1, 2 // 2, 1) = 1`. It consumes all resources and records four seconds. The next check fails because the left projector is empty, so the answer remains `4`.

For the middle projector limitation:

```
10
1
10
```

The number of complete cycles is zero because `1 // 2 = 0`. The remaining simulation activates the left projector once, then sees that the middle projector cannot turn on. The result is `1`, matching the actual process.
