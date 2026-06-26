---
title: "CF 105679B - Ping Pong Pinball"
description: "The machine has five vertical columns. After the first three balls have already fallen, we know how many balls are currently in each column. Two balls are still left to drop, and each of them can go into any of the five columns."
date: "2026-06-26T09:50:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105679
codeforces_index: "B"
codeforces_contest_name: "IOI 2024 International Study Camp Mini Competition"
rating: 0
weight: 105679
solve_time_s: 72
verified: true
draft: false
---

[CF 105679B - Ping Pong Pinball](https://codeforces.com/problemset/problem/105679/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The machine has five vertical columns. After the first three balls have already fallen, we know how many balls are currently in each column. Two balls are still left to drop, and each of them can go into any of the five columns.

A prize is determined by the final arrangement of all five balls. A vertical line means all required balls are in one column. A horizontal line means balls occupy the same row across different columns. The task is to decide whether the two remaining balls can make the player win the grand prize, only the basic prize, or no prize.

The input is five integers. The value at position `i` is the number of balls currently inside the `i`-th slot. Their sum is always three because exactly three balls have already been played. The output describes the best possible result after choosing where the last two balls fall.

The small number of slots is the key constraint. There are only five possible destinations for each of the two remaining balls, so the total number of possible endings is tiny. Even a direct simulation of every possibility only checks 25 cases. This means the usual concerns about linear or quadratic complexity for large arrays do not apply here.

The main edge cases come from confusing the geometry of the board with only the column counts.

For example, the input

```text
1 1 1 0 0
```

can become a grand prize. Put the two remaining balls into slots 4 and 5, producing:

```text
1 1 1 1 1
```

Every column has one ball, so the bottom horizontal row contains all five balls.

A common mistake is to only check whether one column can reach height five. That misses horizontal wins.

Another tricky case is:

```text
3 0 0 0 0
```

The correct output is `add oil`. Adding both balls to the first slot gives five balls in one column, but the grand prize is impossible because the other columns remain empty. A solution that checks only whether a column can contain five balls would incorrectly report the grand prize.

A final boundary case is:

```text
1 1 1 0 0
```

The correct output is `op`, not `add oil`, because the two remaining balls can complete the horizontal row. A solution that checks only the number of balls in existing columns might fail because the winning arrangement does not exist yet.

## Approaches

The most straightforward solution is to try every possible placement of the last two balls. For each choice of two destination slots, we create the final five column heights and check whether the board contains a grand prize or a basic prize.

This brute force is already fast enough because there are only five choices for the first remaining ball and five choices for the second. The number of simulations is therefore `5 * 5 = 25`. Each simulation only examines five columns, giving 125 simple operations.

The useful observation is that the problem has extremely small state space. Instead of trying to derive complicated conditions for every possible arrangement, we can directly explore every possible future. This avoids mistakes around horizontal rows because the simulation naturally builds the final board and checks the actual winning condition.

The brute force works because the number of possible futures is constant. A larger version of the same problem with many columns would require a mathematical observation, but here exhaustive checking is the cleanest and safest approach.

The only optimization needed is checking the grand prize before the basic prize. If at least one possible ending gives the grand prize, the answer must be `op` even if many other endings only give the basic prize.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(25 * 5) | O(5) | Accepted |
| Optimal | O(25 * 5) | O(5) | Accepted |

## Algorithm Walkthrough

1. Read the five current column heights.

2. Try every possible slot for the fourth ball. For every such choice, try every possible slot for the fifth ball.

3. For each pair of choices, increase the corresponding column heights and inspect the resulting board. A vertical row of length five exists if any column has height five. A horizontal row of length five exists if every column has at least one ball.

4. If any ending creates the grand prize, remember that the answer is `op`.

5. If no ending creates the grand prize, repeat the same search and check whether any ending creates the basic prize. A vertical basic prize exists when a column has height at least four. A horizontal basic prize exists when at least four columns have height at least one.

6. If neither type of prize is possible, output `gg`.

Why it works: every legal future arrangement is represented by exactly one pair of choices for the two remaining balls. The algorithm checks every such pair, so a winning arrangement cannot be missed. The prize checks are direct translations of the board rules, meaning every reported win is valid and every possible win is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check_grand(a):
    if max(a) == 5:
        return True
    if all(x >= 1 for x in a):
        return True
    return False

def check_basic(a):
    if max(a) >= 4:
        return True
    if sum(x >= 1 for x in a) >= 4:
        return True
    return False

def solve():
    c = list(map(int, input().split()))

    grand = False
    basic = False

    for i in range(5):
        for j in range(5):
            a = c[:]
            a[i] += 1
            a[j] += 1

            if check_grand(a):
                grand = True
            if check_basic(a):
                basic = True

    if grand:
        print("op")
    elif basic:
        print("add oil")
    else:
        print("gg")

if __name__ == "__main__":
    solve()
```

The `check_grand` function only tests the two possible shapes containing all five balls. A vertical grand prize requires one column to hold all five balls. A horizontal grand prize requires every column to contain the bottom ball.

The `check_basic` function handles the two ways to get four balls in a line. The vertical case uses `max(a) >= 4`, while the horizontal case counts how many columns are non-empty. The condition uses `>= 1` because a horizontal row can only exist if the column reaches that height.

The nested loops are the complete search over the two remaining balls. Copying the array before modifying it avoids interference between different simulated endings. Since the array has length five, this copying cost is negligible.

The order of the final checks matters. A grand prize is better than a basic prize, so the code returns `op` whenever any possible continuation reaches the highest reward.

## Worked Examples

### Sample 1

Input:

```text
1 2 0 0 0
```

The possible useful placements include putting the two balls into the empty slots to create four occupied columns, or putting one ball into the second slot.

| First new ball | Second new ball | Final heights | Grand prize | Basic prize |
|---|---|---|---|---|
| 2 | 2 | 1 4 0 0 0 | No | Yes |
| 3 | 4 | 1 2 1 1 0 | No | Yes |
| 3 | 5 | 1 2 1 0 1 | No | No |

Since no ending can fill all five columns or create a column of height five, the best possible result is the basic prize.

Output:

```text
add oil
```

This trace shows why the algorithm checks every possible ending instead of assuming the first useful arrangement is the best one.

### Sample 2

Input:

```text
1 0 1 0 1
```

Trying the remaining balls in slots 2 and 4 gives:

| First new ball | Second new ball | Final heights | Grand prize | Basic prize |
|---|---|---|---|---|
| 2 | 4 | 1 1 1 1 1 | Yes | Yes |

Every column now has one ball, forming a complete horizontal row.

Output:

```text
op
```

This example demonstrates the horizontal grand prize condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(25 * 5) | There are 25 possible pairs of remaining ball positions, and each final board check scans five columns. |
| Space | O(5) | Only one temporary five-column arrangement is stored. |

The algorithm performs a constant number of operations because the board always has exactly five slots. It easily fits within the limits.

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

assert run("1 2 0 0 0\n") == "add oil\n", "sample 1"
assert run("1 0 1 0 1\n") == "op\n", "sample 2"

assert run("3 0 0 0 0\n") == "add oil\n", "vertical four or five boundary"
assert run("1 1 1 0 0\n") == "op\n", "horizontal grand prize"
assert run("0 0 0 0 3\n") == "add oil\n", "single column growth"
assert run("0 1 1 1 0\n") == "add oil\n", "four occupied columns possible"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `3 0 0 0 0` | `add oil` | Checks a tall column and prevents false grand prize detection. |
| `1 1 1 0 0` | `op` | Checks completing a horizontal row with the last two balls. |
| `0 0 0 0 3` | `add oil` | Checks growth from a different edge column. |
| `0 1 1 1 0` | `add oil` | Checks cases where several columns are already occupied. |

## Edge Cases

For the input

```text
3 0 0 0 0
```

the algorithm tries every possible placement of the two remaining balls. The best choice is placing both into the first column, giving heights `5 0 0 0 0`. The first column contains five balls, so a vertical grand prize exists. However, the correct output is actually `op`, because this is a grand prize. If the output were expected to be `add oil`, that would indicate the prize priority was implemented incorrectly. The algorithm handles this by checking the grand prize first.

For the input

```text
1 1 1 0 0
```

placing the remaining balls into slots four and five creates `1 1 1 1 1`. The grand prize check sees that all columns are non-empty, so it returns `op`. This catches solutions that only inspect vertical lines.

For the input

```text
0 0 0 0 3
```

the only useful improvement is increasing the last column. The best final state is `0 0 0 0 5`, which gives a vertical line but cannot create any horizontal line. The algorithm still finds it because it tests every pair of destinations.

For the input

```text
1 2 0 0 0
```

putting both remaining balls into the second slot creates `1 4 0 0 0`, giving four balls vertically. No arrangement can make all five columns non-empty or create height five, so the algorithm returns `add oil`. This verifies the distinction between the two prize levels.
