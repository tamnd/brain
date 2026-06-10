---
title: "CF 1490B - Balanced Remainders"
description: "We are given an array whose length is always divisible by three. For every number, only its remainder modulo 3 matters. A single move increases one array element by 1."
date: "2026-06-10T22:39:59+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1490
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 702 (Div. 3)"
rating: 1000
weight: 1490
solve_time_s: 310
verified: true
draft: false
---

[CF 1490B - Balanced Remainders](https://codeforces.com/problemset/problem/1490/B)

**Rating:** 1000  
**Tags:** brute force, constructive algorithms, math  
**Solve time:** 5m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array whose length is always divisible by three. For every number, only its remainder modulo 3 matters.

A single move increases one array element by 1. From the perspective of remainders, increasing a number by 1 moves it along the cycle:

0 → 1 → 2 → 0

Our goal is to make the counts of numbers with remainders 0, 1, and 2 all equal. Since the array length is divisible by 3, each remainder class must end up containing exactly `n / 3` elements.

The actual values in the array are largely irrelevant. The only information that affects the answer is how many numbers currently belong to each remainder class. If we know the counts

`c[0]`, `c[1]`, `c[2]`

then the task becomes balancing these three buckets using the cheapest possible transfers around the circular remainder graph.

The constraints are very friendly. The total number of array elements across all test cases is at most 150,000. Any algorithm that processes each element a constant number of times is easily fast enough. Even an `O(n)` solution per test case is trivial within the limit. There is no need for dynamic programming, graph algorithms, or heavy data structures.

A subtle edge case appears when all excess elements must travel through multiple remainder classes.

Consider:

```
n = 6
remainders: [0,0,0,0,0,0]
```

The counts are:

```
c0 = 6, c1 = 0, c2 = 0
target = 2
```

The correct answer is 6.

Two elements move from class 0 to class 1, costing 2 moves total. Two more elements must move from class 0 to class 2. Since there is no direct operation from remainder 0 to remainder 2, each such transfer costs 2 moves, contributing 4 more moves. The total is 6.

A careless solution that only transfers directly into deficient classes would incorrectly compute 4.

Another easy mistake is stopping after one balancing pass.

Consider:

```
n = 6
remainders: [2,2,2,2,2,2]
```

Counts:

```
c0 = 0, c1 = 0, c2 = 6
target = 2
```

Moving two elements from class 2 to class 0 costs 2 moves each, creating:

```
c0 = 2, c1 = 0, c2 = 4
```

The array is still not balanced. Class 2 remains excessive and must send two more elements to class 1. The final answer is 6. A single-pass redistribution misses this second correction.

A third edge case occurs when the array is already balanced.

```
n = 6
a = [0,1,2,3,4,5]
```

Counts:

```
c0 = c1 = c2 = 2
```

The answer is 0. Any solution that blindly performs transfers without checking surplus counts may add unnecessary moves.

## Approaches

The most direct idea is to simulate individual operations. Whenever some remainder class contains too many elements, pick an element from that class and repeatedly increase it until it reaches a deficient class.

This approach is correct because it follows the allowed operations exactly. The problem is that we are thinking about individual numbers when only the counts matter. In larger variants of this idea, we may perform many unnecessary simulations. Tracking actual elements provides no additional information.

The key observation is that every operation only changes a remainder class. Increasing a number once moves one item from class `r` to class `(r+1) mod 3`.

Instead of manipulating elements, we can manipulate counts.

Suppose class `i` currently contains more than the target amount. The excess

```
c[i] - target
```

must eventually leave this class. The cheapest destination is always the next remainder class in the cycle, because one increment performs exactly that transition.

Whenever a class has excess elements, we transfer all excess to the next class, pay one move per transferred element, and update the counts. This may create a surplus in the next class, which will be handled later.

Since there are only three remainder classes, repeatedly propagating excess around the cycle quickly reaches balance. Running through the classes several times is enough. The standard solution performs six iterations, which guarantees that any surplus can travel at most two full rounds around the cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of elements | O(n + answer) | O(n) | Unnecessarily slow |
| Count redistribution | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many array elements have remainders 0, 1, and 2 modulo 3.
2. Compute the target size of each class:

```
target = n / 3
```
3. Initialize the answer to zero.
4. Iterate through remainder classes several times. Six iterations are sufficient because there are only three classes and surplus may need to travel around the cycle more than once.
5. For each class `i`, check whether `c[i] > target`.
6. If it is excessive, let

```
extra = c[i] - target
```

move all those elements into class `(i + 1) % 3`.
7. Each transferred element requires one increment, so add `extra` to the answer.
8. Update the counts:

```
c[i] -= extra
c[(i + 1) % 3] += extra
```
9. After all passes, the counts are balanced and the accumulated cost is the minimum number of moves.

### Why it works

The only allowed operation moves one element from remainder class `r` to remainder class `(r+1) mod 3` and costs exactly one move. Whenever a class contains more than the target number of elements, every excess element must leave that class eventually. Sending excess directly to the next class is the cheapest possible action because that is exactly what one increment does.

The algorithm maintains the invariant that no element is moved unless it belongs to a surplus class. Every transfer reduces the surplus of the current class as much as possible. If the receiving class becomes excessive, that excess is propagated later. Since surplus can only move forward around the cycle and every move is counted exactly once, the total cost equals the minimum number of increments required to reach balanced counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cnt = [0, 0, 0]
        for x in a:
            cnt[x % 3] += 1

        target = n // 3
        moves = 0

        for i in range(6):
            r = i % 3

            if cnt[r] > target:
                extra = cnt[r] - target
                cnt[r] -= extra
                cnt[(r + 1) % 3] += extra
                moves += extra

        ans.append(str(moves))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first part computes the three remainder counts. This reduces the problem from an array-balancing task to a three-bucket balancing task.

The variable `target` stores the required size of each bucket. Since `n` is divisible by three, no rounding issues exist.

The redistribution loop is the core of the solution. Whenever a class contains more than `target` elements, all excess is pushed forward by one remainder step. Each transferred element corresponds to exactly one increment operation, so `moves` increases by the same amount.

The loop runs six times rather than three. One complete pass may create a new surplus in the next class. The second pass allows that surplus to continue moving. With only three remainder classes, six iterations are enough for all excess to propagate completely.

No integer overflow concerns exist because the maximum answer is small compared to Python's integer range.

## Worked Examples

### Sample 1

Input:

```
6
0 2 5 5 4 8
```

Initial counts:

```
c0 = 1
c1 = 1
c2 = 4
target = 2
```

| Step | Counts (c0,c1,c2) | Extra moved | Cost added | Total |
| --- | --- | --- | --- | --- |
| Start | (1,1,4) | - | - | 0 |
| r=2 | (2,1,3) | 1 | 1 | 1 |
| r=2 again | (3,1,2) | 1 | 1 | 2 |
| r=0 | (2,2,2) | 1 | 1 | 3 |

Final answer:

```
3
```

This example shows surplus repeatedly propagating around the cycle. Excess from class 2 first creates additional elements in class 0, and only afterward can class 0 donate to class 1.

### Sample 2

Input:

```
6
2 0 2 1 0 0
```

Remainders:

```
2,0,2,1,0,0
```

Counts:

```
c0 = 3
c1 = 1
c2 = 2
target = 2
```

| Step | Counts (c0,c1,c2) | Extra moved | Cost added | Total |
| --- | --- | --- | --- | --- |
| Start | (3,1,2) | - | - | 0 |
| r=0 | (2,2,2) | 1 | 1 | 1 |

Final answer:

```
1
```

This case demonstrates the simplest situation where one surplus class directly fixes one deficient class.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting remainders dominates the work |
| Space | O(1) | Only three counters are stored |

The total number of array elements across all test cases is at most 150,000. Processing each element once is easily within the time limit, and constant auxiliary memory is negligible compared to the available memory limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cnt = [0, 0, 0]
        for x in a:
            cnt[x % 3] += 1

        target = n // 3
        moves = 0

        for i in range(6):
            r = i % 3
            if cnt[r] > target:
                extra = cnt[r] - target
                cnt[r] -= extra
                cnt[(r + 1) % 3] += extra
                moves += extra

        out.append(str(moves))

    return "\n".join(out)

# provided sample
assert run(
"""4
6
0 2 5 5 4 8
6
2 0 2 1 0 0
9
7 1 3 4 2 10 3 9 6
6
0 1 2 3 4 5
"""
) == """3
1
3
0"""

# minimum size, already balanced
assert run(
"""1
3
0 1 2
"""
) == "0"

# all elements in remainder class 0
assert run(
"""1
6
0 3 6 9 12 15
"""
) == "6"

# all elements in remainder class 2
assert run(
"""1
6
2 5 8 11 14 17
"""
) == "6"

# one surplus bucket fixing one deficit
assert run(
"""1
6
0 0 0 1 1 2
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 0 1 2` | `0` | Minimum valid size and already balanced |
| Six multiples of 3 | `6` | Multi-step propagation through the cycle |
| Six numbers with remainder 2 | `6` | Surplus wrapping around modulo 3 |
| `0 0 0 1 1 2` | `1` | Single direct transfer |

## Edge Cases

Consider:

```
1
6
0 3 6 9 12 15
```

All numbers belong to remainder class 0.

Initial counts:

```
(6,0,0)
```

Target:

```
2
```

The algorithm moves four excess elements from class 0 to class 1, costing 4. Counts become:

```
(2,4,0)
```

Class 1 now has surplus 2, which moves to class 2 with cost 2 more. Final counts:

```
(2,2,2)
```

Total answer:

```
6
```

This confirms that excess may need to travel through intermediate classes.

Consider:

```
1
6
2 5 8 11 14 17
```

Initial counts:

```
(0,0,6)
```

The first redistribution sends four elements from class 2 to class 0:

```
(4,0,2)
```

Cost becomes 4.

Next, class 0 sends two excess elements to class 1:

```
(2,2,2)
```

Cost becomes 6.

This demonstrates why multiple passes are required. Balancing one class can create a new surplus elsewhere.

Consider:

```
1
6
0 1 2 3 4 5
```

Initial counts:

```
(2,2,2)
```

No class exceeds the target. The redistribution loop performs no transfers, and the answer remains 0. This confirms that the algorithm does not introduce unnecessary moves when the array is already balanced.
