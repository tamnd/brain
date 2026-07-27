---
title: "CF 102783D - Ghost-or-Treat"
description: "We have a line of ghosts, each with an integer age. A move consists of choosing two neighboring ghosts whose ages are different. The younger ghost disappears, while the older ghost remains and becomes one year older."
date: "2026-07-27T19:58:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102783
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 2"
rating: 0
weight: 102783
solve_time_s: 51
verified: true
draft: false
---

[CF 102783D - Ghost-or-Treat](https://codeforces.com/problemset/problem/102783/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of ghosts, each with an integer age. A move consists of choosing two neighboring ghosts whose ages are different. The younger ghost disappears, while the older ghost remains and becomes one year older. The order of the remaining ghosts stays the same after a ghost leaves.

The task is not to simulate the process. We only need to decide whether Boo can choose moves in some order so that exactly one ghost remains.

The input gives the number of ghosts followed by their ages in line order. The output is YES if there exists a sequence of valid matches that removes every ghost except one, and NO otherwise.

The important constraint is that the number of ghosts can be as large as 10000. A simulation of all possible choices is impossible because the number of possible match orders grows extremely quickly. Even trying every pair of neighboring choices leads to an exponential search space. We need a property of the ages that decides the answer directly.

The edge cases are small but easy to miss. If there is only one ghost, the answer is immediately YES because there is already exactly one remaining ghost.

For example:

```
Input
1
7

Output
YES
```

A solution that only checks whether all ages are equal might incorrectly reject this case.

Another important case is when every ghost has the same age and there is more than one ghost.

```
Input
4
5
5
5
5

Output
NO
```

No two adjacent ghosts have different ages, so the first move cannot even start.

A final case is when the equal ages are not all the same value.

```
Input
5
4
4
3
4
4

Output
YES
```

A careless approach might think the repeated values prevent progress, but the middle age 3 can fight a neighbor, allowing one ghost to grow and eventually eliminate the others.

## Approaches

The brute-force approach is to try every possible sequence of fights. For each state, we choose every adjacent pair with different ages, remove the smaller one, increase the larger one, and recursively check whether we can reach a single ghost. This exactly models the process, so it is correct, but the number of states is far too large. With 10000 ghosts, even the first few choices already create an enormous branching tree.

The key observation is that the only situation where a fight cannot begin is when every ghost has the same age. If there are at least two different ages, we can always make progress.

Suppose there is a ghost with an age different from some other ghost. Consider moving through the line by repeatedly fighting a ghost that is currently different from a neighbor. The older ghost in each fight survives and increases its age. Once a ghost has become strictly older than another ghost, it can continue defeating younger neighbors. Equal ages can be ignored until a stronger ghost reaches them, because the stronger ghost will then have a valid fight. Eventually one ghost can absorb all others.

The entire problem reduces to checking whether all ages are identical, with the special case that one ghost already satisfies the goal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all ghost ages. If there is only one ghost, output YES because no matches are required.
2. Compare every age with the first ghost's age. If all ages are equal, output NO because no adjacent pair can ever have different ages.
3. If at least one age differs from the first age, output YES because the existence of two different ages guarantees that the process can be arranged to leave one survivor.

The reason this works is that the exact order of fights does not matter for the decision. A non-uniform array always contains the starting point needed to create a ghost that becomes older after each successful fight. Growth only helps future fights because a surviving ghost never becomes younger.

Why it works:

If all ghosts have the same age and there is more than one ghost, every adjacent comparison fails, so no move exists.

Otherwise, there are two ghosts with different ages. The older one can defeat the younger one if they become adjacent, and after winning it increases its age. Increasing age can never make a future fight harder because a larger age only creates more possible opponents. Repeating this idea allows a single ghost to survive all matches. Therefore the only impossible situation is having multiple ghosts with identical ages.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ages = [int(input()) for _ in range(n)]

    if n == 1:
        print("YES")
        return

    first = ages[0]
    for age in ages[1:]:
        if age != first:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The solution stores the ages only because the input is given one value per line and the simplest implementation is to read them into an array. The actual algorithm only needs the first age and whether a different age exists, so the same idea can be implemented with constant extra memory.

The `n == 1` check comes before the equality check because a single ghost with any age is already a valid final state. For larger inputs, finding one different age is enough to prove that a sequence of fights exists.

There are no arithmetic operations involving large values, so integer overflow is not a concern in Python. The implementation also avoids simulating the fights, which is the main source of unnecessary complexity.

## Worked Examples

For the first sample:

```
Input
5
5
3
4
4
5
```

The important variable changes are:

| Step | Current age checked | First age | Decision |
| --- | --- | --- | --- |
| Start | 5 | 5 | Continue |
| Read 3 | 3 | 5 | Different value found |
| Finish |  |  | Output YES |

This trace demonstrates the main observation. The algorithm stops as soon as it finds a possible starting difference.

For the second sample:

```
Input
3
1
1
1
```

The trace is:

| Step | Current age checked | First age | Decision |
| --- | --- | --- | --- |
| Start | 1 | 1 | Continue |
| Read 1 | 1 | 1 | Continue |
| Read 1 | 1 | 1 | All values equal |
| Finish |  |  | Output NO |

This confirms the blocked case where no valid first move exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every ghost age is inspected at most once. |
| Space | O(N) | The implementation stores the input ages. |

The constraints allow a linear scan comfortably. The algorithm performs only simple comparisons, so it easily fits within the time limit. The stored array can also be removed to reduce memory usage to O(1), but the current version is already well within the memory limit.

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

# sample 1
assert run("""5
5
3
4
4
5
""") == "YES\n", "sample 1"

# sample 2
assert run("""3
1
1
1
""") == "NO\n", "sample 2"

# single ghost
assert run("""1
100
""") == "YES\n", "single ghost"

# all equal values
assert run("""6
8
8
8
8
8
8
""") == "NO\n", "all equal"

# different values separated by equal values
assert run("""5
4
4
3
4
4
""") == "YES\n", "middle different value"

# large value boundary
assert run("""2
1000000000
999999999
""") == "YES\n", "large ages"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One ghost | YES | Handles the already-finished case. |
| All ages equal | NO | Confirms that no first move is possible. |
| One different value among equal values | YES | Confirms that repeated ages do not block the process. |
| Very large ages | YES | Confirms that age size does not affect the logic. |

## Edge Cases

For the single ghost case:

```
Input
1
7
```

The algorithm checks `n == 1` immediately and returns YES. No fights are needed because the goal is already satisfied.

For the all-equal case:

```
Input
4
5
5
5
5
```

The scan compares every value with the first age. Since every comparison is equal, the algorithm returns NO. This matches the process because no adjacent pair has different ages, so Boo cannot perform even one operation.

For the case with equal groups around a different age:

```
Input
5
4
4
3
4
4
```

The scan finds that the third ghost has age 3 while the first ghost has age 4. This proves the line is not frozen. The older ghost can eventually use the younger ghost to increase its age and continue winning fights, so the answer is YES.

For a case where the different ages are at the ends:

```
Input
3
10
10
20
```

The algorithm finds the last value differs from the first and returns YES. The final ghost does not need to start next to every other ghost. The existence of any difference is enough because fights can be arranged to bring a growing survivor through the line.
