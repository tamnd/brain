---
title: "CF 102569E - Fluctuations of Mana"
description: "The journey consists of visiting magical sources in a fixed order. Each source changes the mage's current mana by a given amount, and the only failure condition is that the mana level drops below zero at any moment."
date: "2026-07-31T07:49:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102569
codeforces_index: "E"
codeforces_contest_name: "2020, XIII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102569
solve_time_s: 79
verified: true
draft: false
---

[CF 102569E - Fluctuations of Mana](https://codeforces.com/problemset/problem/102569/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
# Problem Understanding

The journey consists of visiting magical sources in a fixed order. Each source changes the mage's current mana by a given amount, and the only failure condition is that the mana level drops below zero at any moment. The task is to determine the smallest starting mana value that allows the mage to survive the entire sequence.

The input array describes the mana changes caused by the sources. Positive values increase the current mana, negative values consume mana, and zero values leave it unchanged. The output is not the final mana after the journey, but the minimum initial amount required so that every prefix of the journey keeps the mana non-negative.

The constraint of up to 500000 sources means the solution must process the array in linear time. An approach that tries many possible starting values or repeatedly simulates the journey would perform too many operations. With a 2 second limit, an algorithm around O(n) or O(n log n) is expected, while O(n²) approaches are far beyond the feasible range.

A few cases commonly break incorrect solutions. A sequence containing only positive changes has answer zero because the mage never loses mana. For example:

```
3
5 2 8
```

The correct output is:

```
0
```

A solution that assumes some positive starting mana is always required would fail here.

A large negative value at the beginning must be handled before later positive values are considered. For example:

```
3
-10 20 -5
```

The correct output is:

```
10
```

The first source immediately requires at least 10 mana. A careless approach that only looks at the final sum would see that the journey gains 5 mana overall and might incorrectly answer zero.

Another subtle case is when the worst deficit happens in the middle rather than at the end. For example:

```
5
4 -7 1 1 10
```

The correct output is:

```
3
```

After the first two sources the total change is -3, so three starting mana are needed. Looking only at the total sum, which is 9, would miss the temporary drop.

# Approaches

The direct approach is to guess the initial mana and simulate the journey. For a fixed starting value, checking whether the mage survives takes O(n) time because every source must be visited once. We could try all possible starting values from zero upward until one works. Since the answer can be as large as the sum of many negative changes, this can require up to around 500000 × 10^9 operations in the worst case, which is impossible.

A binary search over the answer improves this idea. The condition is monotonic: if a starting mana value works, any larger value also works. This gives an O(n log A) approach, where A is the size of the possible answer range. However, the structure of the problem allows an even simpler observation.

Instead of repeatedly asking whether a chosen starting value is enough, track the mana changes themselves. Imagine starting with zero mana and following the entire journey. At every point, the running sum tells us how far below zero the mage would have fallen. The largest drop below zero is exactly the amount of mana that was missing at the beginning. Adding that missing amount shifts every prefix upward just enough to make the minimum prefix equal to zero.

For example, if the running totals are:

```
3, -1, 1, -2, -4, 3
```

the lowest value is -4. Starting with 4 mana moves these totals to:

```
7, 3, 5, 2, 0, 7
```

Every value is now valid, and any smaller starting amount would still leave the lowest point negative.

The brute-force works because it tests whether a starting value protects every prefix of the journey, but it repeats the same simulation many times. The observation that only the minimum prefix sum matters lets us find the answer in a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × answer) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with a running mana balance of zero and a variable storing the minimum balance reached so far. The running balance represents what would happen if the mage started with zero mana.
2. Process each mana change in order and add it to the running balance. After each addition, update the minimum balance if the current value is smaller.
3. After the entire sequence is processed, if the minimum balance is negative, return its absolute value. If the minimum balance is zero or positive, return zero.

The reason the minimum prefix is enough is that every moment of danger occurs after some prefix of the array has been processed. The largest required initial mana is exactly the amount needed to lift the lowest prefix back to zero.

Why it works: The running sums describe all possible points where the mage could die when starting with zero mana. Suppose the minimum running sum is `-x`. Any starting mana smaller than `x` would leave that point below zero, so at least `x` mana is necessary. Starting with exactly `x` increases every running sum by `x`, making the minimum value zero and all other values non-negative. Thus `x` is both necessary and sufficient.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return

    n = int(n_line)
    a = list(map(int, input().split()))

    current = 0
    minimum = 0

    for value in a:
        current += value
        if current < minimum:
            minimum = current

    print(-minimum)

if __name__ == "__main__":
    solve()
```

The code keeps only two pieces of information while scanning the array. `current` is the mana level in the imaginary simulation where the mage starts with zero mana. `minimum` stores the lowest value reached by that simulation.

Whenever the running balance becomes smaller, it means the mage would need additional starting mana to survive that point. The final answer is the negative of the lowest balance. Since `minimum` starts at zero, sequences that never go negative automatically produce answer zero.

Python integers do not overflow, which matters because the sum of 500000 values with magnitude up to 10^9 can reach around 5 × 10^14. The algorithm also avoids storing unnecessary prefix sums, keeping memory usage constant.

# Worked Examples

For the sample input:

```
6
3 -4 2 -3 -2 7
```

the trace is:

| Source value | Current balance | Minimum balance |
| --- | --- | --- |
| 3 | 3 | 0 |
| -4 | -1 | -1 |
| 2 | 1 | -1 |
| -3 | -2 | -2 |
| -2 | -4 | -4 |
| 7 | 3 | -4 |

The minimum balance is -4, so the mage needs 4 starting mana. Adding 4 to every point of the journey prevents the balance from ever becoming negative.

A second example:

```
5
5 -2 -8 4 10
```

| Source value | Current balance | Minimum balance |
| --- | --- | --- |
| 5 | 5 | 0 |
| -2 | 3 | 0 |
| -8 | -5 | -5 |
| 4 | -1 | -5 |
| 10 | 9 | -5 |

The lowest simulated balance is -5, so the required initial mana is 5. This example shows that a large recovery at the end does not help with an earlier dangerous point.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every source is processed exactly once. |
| Space | O(1) | Only the current sum and the minimum prefix value are stored. |

The solution easily fits the constraints because it performs a single linear scan over at most 500000 values and does not allocate memory proportional to the input size.

# Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import builtins
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    current = 0
    minimum = 0

    for x in a:
        current += x
        minimum = min(minimum, current)

    result = str(-minimum)

    sys.stdin = old_stdin
    return result

assert solve_io("6\n3 -4 2 -3 -2 7\n") == "4", "sample 1"

assert solve_io("1\n0\n") == "0", "single zero"

assert solve_io("3\n5 2 8\n") == "0", "all positive values"

assert solve_io("3\n-10 20 -5\n") == "10", "large first deficit"

assert solve_io("5\n4 -7 1 1 10\n") == "3", "middle deficit"

assert solve_io("500000\n" + " ".join(["-1000000000"] * 500000) + "\n") == str(500000000000000), "maximum size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6\n3 -4 2 -3 -2 7` | `4` | Provided sample and general prefix tracking |
| `1\n0` | `0` | Minimum-size input and zero change |
| `5 2 8` | `0` | No negative prefix values |
| `-10 20 -5` | `10` | Immediate large deficit |
| `4 -7 1 1 10` | `3` | Deficit occurring before the end |
| 500000 values of `-1000000000` | `500000000000000` | Maximum input size and large integer handling |

# Edge Cases

For the all-positive case:

```
3
5 2 8
```

the running balances are 5, 7, and 15. The minimum prefix value remains zero because the simulated mage never loses mana. The algorithm returns `-0`, which is simply `0`, correctly handling the fact that no initial mana is required.

For the initial negative value case:

```
3
-10 20 -5
```

the running balances are -10, 10, and 5. The minimum prefix is -10, so the answer becomes 10. This matches the requirement because the mage must survive the very first source before any recovery is possible.

For the middle deficit case:

```
5
4 -7 1 1 10
```

the running balances are 4, -3, -2, -1, and 9. The minimum value is -3, so the answer is 3. The algorithm does not depend on the final mana amount and correctly identifies the most dangerous point during the journey.

For the maximum-size input:

```
500000
-1000000000 -1000000000 ... -1000000000
```

the balance decreases by 10^9 each step. The minimum balance after all sources is -500000000000000, so the answer is 500000000000000. The implementation handles this because Python integers can represent values much larger than 64-bit limits.
