---
title: "CF 106488C - Baba has exam"
description: "The problem is about maximizing profit while baking buns. There is a fixed amount of dough available. A bun can either be made with no stuffing, or with one of several stuffing types."
date: "2026-06-25T08:46:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106488
codeforces_index: "C"
codeforces_contest_name: "XXX Spain Olympiad in Informatics, Day 2"
rating: 0
weight: 106488
solve_time_s: 34
verified: true
draft: false
---

[CF 106488C - Baba has exam](https://codeforces.com/problemset/problem/106488/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is about maximizing profit while baking buns. There is a fixed amount of dough available. A bun can either be made with no stuffing, or with one of several stuffing types. Each stuffed bun consumes some dough and some amount of one particular stuffing, then gives a certain amount of money. Unstuffed buns only consume dough and have their own fixed cost and reward. The goal is to choose how many buns of each type to bake so the total revenue is as large as possible.

The input gives the available dough, the number of stuffing types, and the requirements and rewards of every bun type. For each stuffing type, we know how much stuffing exists, how much stuffing one bun consumes, how much dough it needs, and how much money it earns. The output is the maximum possible income after using any combination of buns.

The amount of dough is at most 1000, and there are at most 10 stuffing types. The small dough limit is the main clue. A solution that depends on the amount of dough can afford a dynamic programming state. A solution that tries every possible number of buns of every type would grow exponentially with the number of stuffing types, so it is not suitable.

A common mistake is to treat each stuffing independently and maximize every stuffing choice separately. This fails because all bun types share the same dough resource. For example:

```
Input:
10 1 10 100
5 5 4 100

Output:
200
```

The best choice is to bake two stuffed buns, using 8 dough and 10 stuffing. A greedy choice based only on stuffing profit density could incorrectly reserve dough for unstuffed buns or choose fewer stuffed buns.

Another edge case is when a stuffing cannot make even one complete bun. For example:

```
Input:
5 1 1 1
3 4 10 100

Output:
5
```

The stuffing exists, but there is not enough dough for a stuffed bun. The only possible action is making five plain buns. A solution that only checks stuffing availability and ignores dough requirements would produce a wrong answer.

A final boundary case is when leftover resources cannot be used. For example:

```
Input:
7 1 3 5
4 4 2 10

Output:
15
```

Two stuffed buns use 4 dough and 8 stuffing, but only one stuffed bun can actually be made because the stuffing amount is limited. The remaining resources cannot be converted into another partial bun.

## Approaches

The direct approach is to try every possible number of buns for every stuffing type. For each stuffing type, we might choose anywhere from zero buns to the maximum allowed by the available stuffing. After choosing all stuffed buns, we fill the remaining dough with plain buns. This is correct because every valid baking plan corresponds to some combination considered by the enumeration.

The problem is the number of combinations. A stuffing amount can allow up to 100 choices, and there can be 10 stuffing types. In the worst case, exploring all possibilities means around $100^{10}$ combinations, which is far beyond what any contest time limit can handle.

The key observation is that dough is the only resource shared by every bun type. Stuffing resources are local to their own bun types, and the dough amount is only 1000. Instead of tracking every stuffing decision separately, we can process stuffing types one by one and maintain the best profit for every possible amount of dough already spent.

For one stuffing type, we have a bounded number of identical choices: bake zero buns, one bun, two buns, and so on until either the stuffing or dough runs out. This is a bounded knapsack transition. After processing all stuffed buns, the remaining dough can always be converted into plain buns, so the final answer is obtained by checking every possible amount of dough used for stuffed buns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100^m) | O(1) | Too slow |
| Optimal | O(m * n * 100) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a dynamic programming array where `dp[x]` represents the maximum money obtainable after using exactly `x` grams of dough on stuffed buns processed so far. Initially, only using zero dough is possible, so `dp[0] = 0` and every other state is impossible.
2. Process each stuffing type independently. For the current stuffing, calculate the maximum number of buns that can be made from it. This limit comes from both the available stuffing amount and the available dough.
3. Try every possible count of buns made with this stuffing. If we make `k` buns, they consume `k * c` dough and give `k * d` money. Update the next dynamic programming state from the previous state by adding this choice.
4. Replace the old states with the newly computed states after finishing this stuffing type. This prevents using the same stuffing more times than it exists.
5. After all stuffing types are processed, consider every possible amount of dough used for stuffed buns. If `x` dough was used, the remaining `n - x` dough can create `(n - x) / c0` plain buns, giving additional profit of `((n - x) / c0) * d0`.
6. Take the maximum value over all possible `x`. This covers every valid combination of stuffed and plain buns.

The invariant is that after processing some stuffing types, `dp[x]` contains the best possible revenue among all choices that use exactly `x` dough on those processed stuffing types. Every possible choice for the next stuffing either uses zero buns or some valid number of buns, so the transition considers every way the invariant could continue to hold. After the final stuffing type, adding the best possible plain bun usage for each remaining dough amount gives the optimal complete baking plan.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, c0, d0 = map(int, input().split())

    stuffings = []
    for _ in range(m):
        a, b, c, d = map(int, input().split())
        stuffings.append((a, b, c, d))

    neg = -10**18
    dp = [neg] * (n + 1)
    dp[0] = 0

    for a, b, c, d in stuffings:
        ndp = [neg] * (n + 1)

        limit = a // b
        for used in range(n + 1):
            if dp[used] == neg:
                continue

            for cnt in range(limit + 1):
                dough = used + cnt * c
                if dough > n:
                    break
                ndp[dough] = max(ndp[dough], dp[used] + cnt * d)

        dp = ndp

    ans = 0
    for used in range(n + 1):
        if dp[used] == neg:
            continue
        plain = (n - used) // c0
        ans = max(ans, dp[used] + plain * d0)

    print(ans)

if __name__ == "__main__":
    solve()
```

The input parsing stores every stuffing type as a tuple because each type is handled separately during the dynamic programming transitions.

The array `dp` uses an impossible value for unreachable states. This avoids accidentally using a state that cannot be created. The value `-10**18` is safely below any possible answer, so it acts as negative infinity without overflow concerns in Python.

For each stuffing type, a new array is created. This is the part that prevents repeatedly taking the same stuffing beyond its available amount. The inner loop tries every possible count of buns from the current stuffing, and the boundary `dough > n` stops unnecessary work once the dough limit is exceeded.

The final loop is separate from the stuffing transitions because plain buns have unlimited availability. Once the amount of dough spent on stuffed buns is known, the best plain bun choice is deterministic. Integer division handles leftover dough correctly because incomplete buns cannot be made.

## Worked Examples

### Sample 1

Input:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

The important states after processing each stuffing type are:

| Step | Dough used | Best profit |
| --- | --- | --- |
| Initial | 0 | 0 |
| After stuffing 1 | 4 | 200 |
| After stuffing 1 | 10 | 200 |
| After stuffing 2 | 8 | 240 |
| After stuffing 2 | 10 | 241 |

The best stuffed-bun state uses 10 dough and earns 241. No dough remains for plain buns, so the final answer is 241.

This trace shows why the DP keeps different dough amounts instead of only keeping the highest profit. A state with less immediate profit can leave room for better future choices.

### Sample 2

Input:

```
100 1 25 50
15 5 20 10
```

| Step | Dough used | Best profit |
| --- | --- | --- |
| Initial | 0 | 0 |
| After stuffing | 20 | 10 |
| After stuffing | 40 | 20 |
| After stuffing | 60 | 30 |
| Final plain buns | 100 | 200 |

The stuffing buns are not profitable enough compared with plain buns. The final calculation correctly fills the unused dough with four plain buns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n * 100) | For each stuffing type, every dough state tries every possible stuffing count. |
| Space | O(n) | Only the current and next dough state arrays are stored. |

Here, `m` is at most 10 and `n` is at most 1000. The number of operations is around one million, which is easily within the limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
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
assert solution("""10 2 2 1
7 3 2 100
12 3 1 10
""") == "241\n", "sample 1"

assert solution("""100 1 25 50
15 5 20 10
""") == "200\n", "sample 2"

# minimum dough, only plain buns
assert solution("""1 1 1 7
1 1 1 1
""") == "7\n", "minimum size"

# stuffing unavailable for a full bun
assert solution("""5 1 1 1
3 4 10 100
""") == "5\n", "cannot use stuffing"

# all choices have the same value
assert solution("""10 2 2 2
10 2 2 4
10 2 2 4
""") == "20\n", "equal values"

# leftover dough and stuffing boundary
assert solution("""7 1 3 5
4 4 2 10
""") == "15\n", "boundary handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum dough case | 7 | Handles the smallest resource amount. |
| Insufficient stuffing case | 5 | Prevents creating impossible stuffed buns. |
| Equal-value choices | 20 | Checks that all equivalent transitions are considered. |
| Leftover resource case | 15 | Checks final plain-bun calculation and integer division. |

## Edge Cases

For the case where stuffing exists but a stuffed bun cannot be created:

```
5 1 1 1
3 4 10 100
```

The DP sees that the stuffing type can make zero buns only because every stuffed bun needs 10 dough while only 5 exists. The only reachable state is `dp[0] = 0`. The final step adds five plain buns, producing 5.

For the case where greedy profit selection fails:

```
10 1 10 100
5 5 4 100
```

The algorithm does not decide locally. It keeps both possibilities: spending dough on stuffed buns and saving dough for plain buns. It evaluates the final combinations and finds that two stuffed buns give 200, which is better than one plain bun.

For the case with leftover resources:

```
7 1 3 5
4 4 2 10
```

The stuffing transition creates states for making zero or one stuffed bun. Two stuffed buns are impossible because only four units of stuffing exist. The state with one stuffed bun uses two dough and earns 10. Five dough remain, which creates one plain bun for another 5, giving the final answer 15.
