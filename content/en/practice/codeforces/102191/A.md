---
title: "CF 102191A - Generous Eater"
description: "We start with n candies and want to give candies to as many distinct friends as possible, one candy per friend. After every second friend receives a candy, we eat one candy ourselves if any candy remains."
date: "2026-08-23T09:12:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "A"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 1443
verified: true
draft: false
---

[CF 102191A - Generous Eater](https://codeforces.com/problemset/problem/102191/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 24m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with `n` candies and want to give candies to as many distinct friends as possible, one candy per friend. After every second friend receives a candy, we eat one candy ourselves if any candy remains. The process continues until we can no longer give another candy to a friend.

The task is to compute the maximum number of friends who can receive a candy.

The value of `n` can be as large as `10^9`. That immediately rules out any simulation that performs one operation per candy, because in the worst case it would execute around one billion iterations. Even with a small constant amount of work per iteration, that is far beyond what a sub-second competitive programming solution can afford. We need to derive the answer directly from the structure of the process.

The most subtle cases occur around the moment when there is no candy left to eat. For example, with input `2`, the answer is `2`, not `1`. We give one candy to each of two friends, and then there is nothing left for us to eat, so both friends are served. A careless formula that always subtracts one candy after every pair would incorrectly reject the second friend.

Another boundary case is `4`. The correct answer is `3`. We give candies to the first two friends, eat one candy, and have one candy remaining for the third friend. After that, the process stops. A naive calculation of one eaten candy for every two friends might incorrectly expect more than four candies to serve three friends.

Input `6` is another useful boundary case. The answer is `4`, not `5`. After serving two friends, one candy is eaten, leaving three. We then serve two more friends, leaving one, and that final candy is eaten. There is nothing left for a fifth friend. This catches formulas that treat every remaining candy as automatically available to a friend.

## Approaches

A direct brute-force solution can simulate the actual process. Keep the number of candies, repeatedly give one candy to a new friend, and after every second friend eat one candy whenever possible. The simulation is correct because it follows exactly the rules of the process. However, it can perform Θ(`n`) iterations. With `n = 10^9`, that means up to one billion iterations, which is much too slow for the time limit.

The useful observation is that the process has a simple repeating pattern. Consider three candies. They can produce two friends: two candies go to two friends, and the third candy is eaten. Thus, every complete group of three candies effectively contributes two friends. The candies left after those complete groups can all be given to additional friends, because there are fewer than three of them and they cannot force another full eating cycle.

Let

`n = 3q + r`, where `r` is `0`, `1`, or `2`.

The `q` complete groups of three candies cause exactly `q` candies to be eaten, while the remaining `r` candies go to friends. Hence the number of friends is

`n - q = n - floor(n / 3)`.

The same result can be understood from the opposite direction. To serve `k` friends, the process needs the `k` candies given to friends plus one eaten candy after every pair that is followed by another friend. This creates the same ratio of two useful candies for every three candies consumed, with the final incomplete group handled directly by the remainder.

So the entire simulation collapses to one integer division and one subtraction.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of candies `n`. The only information needed is the total count, because the process does not distinguish between candies or friends.

2. Compute `n // 3`. This is the number of complete groups of three candies. Each such group contains one candy that must be eaten instead of being given to a friend.

3. Subtract that number from `n`. The result, `n - n // 3`, is the number of candies that can ultimately be given to friends.

4. Print the result.

Why does grouping by three work even when the final group has one or two candies? A complete group accounts for one eaten candy and two candies given to friends. Any remainder of one or two candies occurs after all complete eating cycles and can be given directly to friends, so no additional subtraction is needed.

### Why it works

The key invariant is that every complete block of three consumed candies reduces the number available to friends by exactly one. Two candies in such a block are given to friends, while one is eaten. If `n = 3q + r`, there are exactly `q` complete blocks and `r < 3` leftover candies. The complete blocks account for exactly `q` eaten candies, while all `r` leftovers can be given to friends. Thus exactly `q = floor(n / 3)` candies are lost to eating, and the maximum number of friends is `n - floor(n / 3)`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
print(n - n // 3)
```

The input is a single integer, so the program reads it directly as `n`. Python integers easily handle `10^9`, although even a 32-bit signed integer would be sufficient here.

The expression `n // 3` performs integer division and gives the number of complete groups of three. Subtracting it from `n` gives the number of candies that reach friends.

There is no loop, so there are no simulation boundaries or off-by-one transitions to manage. In particular, using integer division is what correctly handles values such as `2`, `4`, and `5`: their quotients by three are `0`, `1`, and `1`, respectively.

## Worked Examples

### Sample 1

For `n = 4`, integer division gives `4 // 3 = 1`. One candy is lost to eating, leaving three candies that can be given to friends.

| `n` | `n // 3` | Friends `n - n // 3` |
|---:|---:|---:|
| 4 | 1 | 3 |

The corresponding process is to give candies to two friends, eat one candy, then give the remaining candy to a third friend. The output is `3`.

### Sample 2

For `n = 5`, there is still only one complete group of three, so exactly one candy is lost to eating. The other four candies reach friends.

| `n` | `n // 3` | Friends `n - n // 3` |
|---:|---:|---:|
| 5 | 1 | 4 |

The process can serve four friends: two receive candies, one candy is eaten, and the remaining two candies go to two more friends. The output is `4`.

These examples also show why the remainder matters. After removing one complete group of three from five candies, two candies remain, and both can be given away without creating another eating cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(1) | The solution performs one integer division and one subtraction. |
| Space | O(1) | Only the input integer and a constant amount of temporary storage are used. |

The largest possible input is `10^9`, but the algorithm never iterates over the candies. It performs a fixed number of arithmetic operations, so it comfortably fits the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    print(n - n // 3)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    output = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output

# provided samples
assert run("4\n") == "3\n", "sample 1"
assert run("5\n") == "4\n", "sample 2"
assert run("6\n") == "4\n", "sample 3"

# custom cases
assert run("1\n") == "1\n", "minimum input"
assert run("2\n") == "2\n", "no candy remains to eat after the second friend"
assert run("7\n") == "5\n", "two complete groups plus one remainder"
assert run("1000000000\n") == "666666667\n", "maximum input"
```

| Test input | Expected output | What it validates |
|---|---:|---|
| `1` | `1` | Minimum-size input and no pair of friends |
| `2` | `2` | Boundary where the second friend can be served without an extra candy to eat |
| `7` | `5` | Remainder after two complete groups of three |
| `1000000000` | `666666667` | Maximum input and constant-time arithmetic |

## Edge Cases

For `n = 1`, the algorithm computes `1 // 3 = 0`, so the answer is `1`. There is only one candy and it goes directly to one friend. No eating cycle is triggered.

For `n = 2`, the algorithm computes `2 // 3 = 0`, giving the answer `2`. We can serve both friends, and after the second candy there is no candy left to eat. This is the boundary that breaks an implementation that blindly removes one candy after every pair.

For `n = 4`, the algorithm computes `4 // 3 = 1`, giving `4 - 1 = 3`. The actual sequence is two candies given, one eaten, and the final candy given to a third friend. The single complete group of three accounts for the one candy eaten.

For `n = 6`, the algorithm computes `6 // 3 = 2`, giving `6 - 2 = 4`. The first two friends consume two candies and trigger one eaten candy. The next two friends consume another two candies and trigger the second eaten candy. The remaining candies cannot support a fifth friend, so four is maximal.

For `n = 10^9`, the algorithm performs exactly the same constant amount of work as for any smaller input. Since `10^9 // 3 = 333333333`, the answer is `1000000000 - 333333333 = 666666667`. This confirms that the solution does not depend on the magnitude of `n` through iteration count.
