---
title: "CF 102791D - Barrels"
description: "We have a row of barrels, and each barrel starts with some amount of water. A move consists of choosing one non-empty barrel and pouring any amount of its water into another barrel. We can perform at most k moves."
date: "2026-07-27T18:09:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102791
codeforces_index: "D"
codeforces_contest_name: "ICPC 2020-2021 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102791
solve_time_s: 62
verified: true
draft: false
---

[CF 102791D - Barrels](https://codeforces.com/problemset/problem/102791/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of barrels, and each barrel starts with some amount of water. A move consists of choosing one non-empty barrel and pouring any amount of its water into another barrel. We can perform at most `k` moves. The goal is to make the difference between the fullest barrel and the emptiest barrel as large as possible after all moves.

The operation is extremely flexible because we can move the entire content of a barrel in one step. The only thing that matters is how much water we can collect into one barrel and whether we can create an empty barrel at the same time.

The constraints allow up to `2 * 10^5` barrels. With a typical contest time limit, an approach that tries many possible sequences of moves is impossible because the number of states grows too quickly. Even checking many combinations of barrels would exceed the available time. We need a solution close to `O(n log n)` or better.

The tricky cases come from the interaction between empty barrels and the number of allowed moves.

Consider this input:

```
3 1
0 5 0
```

The answer is `5`. A careless solution might think one move is useless because two barrels are already empty, but we can pour the `5` liters into an empty barrel and still keep an empty barrel behind, giving a difference of `5`.

Another edge case is:

```
4 2
7 0 0 0
```

The answer is `7`. We can move the water between barrels twice and end with one barrel containing all `7` liters and at least one empty barrel. A solution that only considers moving from initially full barrels directly into the final barrel can miss this kind of case.

A final important case is when every barrel is empty:

```
3 2
0 0 0
```

The answer is `0`. The formula for the maximum collected water still gives `0`, and no operation can create water that was not there.

## Approaches

The direct brute-force approach would try to decide which barrels become donors and which barrel receives the water. For every chosen receiving barrel, we could simulate moving water from selected barrels into it. This is correct because the best final state must have some barrel containing the maximum amount of water, and the moves that increase this value are exactly the moves that transfer water into that barrel.

However, choosing the best set of donors is the problem. There are `n` barrels and we need to choose `k` donors plus one receiving barrel. Trying all choices requires combinatorial work, which is far beyond what is possible for `n = 2 * 10^5`.

The key observation is that the minimum value after the operations can always be made zero. Since `k < n`, we have at least one barrel that does not need to be the final receiver. By emptying barrels through our moves, we can leave an empty barrel behind.

Once the minimum is fixed at zero, maximizing the answer is the same as maximizing the largest barrel. One move can transfer all water from one barrel into another, so after `k` moves we can combine the contents of exactly `k` donor barrels into one destination barrel. The destination barrel also contributes its original water. Therefore, the final largest barrel can contain the sum of the largest `k + 1` initial amounts.

The brute-force method works because it correctly models all possible transfers, but fails because it searches too many choices. The observation that only the largest possible accumulated barrel matters reduces the problem to sorting and summing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `n` | O(n) | Too slow |
| Optimal | O(n log n) | O(1) extra space | Accepted |

## Algorithm Walkthrough

1. Read the amounts of water in all barrels and sort them in descending order.

Sorting lets us identify the barrels that contribute the most water to the final maximum. Any smaller barrel chosen instead of a larger one can only decrease the result.
2. Add the first `k + 1` values from the sorted array.

One barrel will hold the final maximum amount. The other `k` barrels are exactly the barrels whose water is moved into it. The destination barrel already contains its own initial water, so we need `k + 1` barrels in the sum.
3. Output this sum.

The minimum amount can be made zero, so this maximum amount is directly the required difference.

Why it works:

The final difference is `maximum - minimum`. Because at least one barrel can remain empty after at most `k` moves, the minimum can always become zero. The only remaining task is maximizing one barrel. Each pouring operation can completely transfer the content of one barrel, so `k` operations allow exactly `k` other barrels to contribute their water to a chosen destination. The best possible destination and donors are the `k + 1` barrels with the largest initial amounts. No other selection can produce a larger total because replacing any selected barrel with a smaller one never increases the sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort(reverse=True)
    
    print(sum(a[:k + 1]))

if __name__ == "__main__":
    solve()
```

The program first sorts the barrel amounts from largest to smallest. The first `k + 1` positions are the only values that can contribute to the final fullest barrel, so there is no need to process the remaining barrels.

The slice `a[:k + 1]` is safe because `k < n`, which means at least `k + 1` barrels always exist. Python integers handle the possible sum size automatically, so no special overflow handling is needed.

The implementation uses only the array storage plus the sorting memory used internally. The sorting step dominates the runtime.

## Worked Examples

For the input:

```
4 1
5 5 5 5
```

The sorted array is `[5, 5, 5, 5]`.

| Step | Sorted values | k + 1 values chosen | Current answer |
| --- | --- | --- | --- |
| Initial | 5, 5, 5, 5 | 5, 5 | 10 |

The first barrel that receives water keeps its original `5`, and one move transfers another `5` into it. An empty barrel remains, so the difference is `10`.

For the input:

```
5 2
1 8 3 10 5
```

The sorted array is `[10, 8, 5, 3, 1]`.

| Step | Sorted values | k + 1 values chosen | Current answer |
| --- | --- | --- | --- |
| Initial | 10, 8, 5, 3, 1 | 10, 8, 5 | 23 |

Two moves allow us to transfer the `8` and `5` into the barrel containing `10`. The final maximum is `23` and an untouched barrel can be empty.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the barrel amounts dominates the work |
| Space | O(1) extra space | Apart from the input array and sorting overhead |

With `n` up to `2 * 10^5`, sorting easily fits within the limits. The solution performs a single sort and a single linear pass through the chosen values.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    data = list(map(int, inp.split()))
    n, k = data[0], data[1]
    a = data[2:]
    a.sort(reverse=True)
    return str(sum(a[:k + 1])) + "\n"

assert solve("""4 1
5 5 5 5
""") == "10\n", "sample 1"

assert solve("""3 2
0 0 0
""") == "0\n", "sample 2"

assert solve("""2 1
1000000000 999999999
""") == "1999999999\n", "large values"

assert solve("""5 1
0 0 0 0 7
""") == "7\n", "single non-zero barrel"

assert solve("""6 3
4 1 9 2 8 7
""") == "28\n", "choose top k+1 values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 1 / 5 5 5 5` | `10` | Equal values and basic combining |
| `3 2 / 0 0 0` | `0` | All barrels empty |
| `2 1 / 1000000000 999999999` | `1999999999` | Large sums and integer handling |
| `5 1 / 0 0 0 0 7` | `7` | Empty barrels already present |
| `6 3 / 4 1 9 2 8 7` | `28` | Correct selection of the largest `k + 1` barrels |

## Edge Cases

For:

```
3 1
0 5 0
```

The sorted array is `[5, 0, 0]`. We take the largest `k + 1 = 2` values, giving `5 + 0 = 5`. One move can place the water in another barrel while leaving an empty barrel, so the difference is `5`.

For:

```
4 2
7 0 0 0
```

The sorted array is `[7, 0, 0, 0]`. We take the largest three values, giving `7`. Although two of the contributing barrels contain zero water, the final maximum cannot exceed the total amount of water in the system.

For:

```
3 2
0 0 0
```

The selected values are all zero, so the answer is zero. There is no water to move, and every possible final state has the same maximum and minimum amount.

For:

```
5 2
1 8 3 10 5
```

The algorithm selects `10`, `8`, and `5`. These are the only values that matter because the two allowed moves can transfer the contents of the `8` and `5` barrels into the barrel containing `10`. Any choice involving `3` or `1` would reduce the final maximum.

I can also adapt this into a shorter Codeforces-style editorial format or a more tutorial-style explanation if needed.
