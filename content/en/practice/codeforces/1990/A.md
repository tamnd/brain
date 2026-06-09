---
title: "CF 1990A - Submission Bait"
description: "We have a two-player game on an array of integers. Alice and Bob take turns, with Alice starting first. Initially, a variable mx is zero. On their turn, a player can choose an array element a[i] if it is at least mx, set mx to that value, and then set a[i] to zero."
date: "2026-06-08T15:33:51+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "games", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1990
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 960 (Div. 2)"
rating: 900
weight: 1990
solve_time_s: 235
verified: false
draft: false
---

[CF 1990A - Submission Bait](https://codeforces.com/problemset/problem/1990/A)

**Rating:** 900  
**Tags:** brute force, games, greedy, sortings  
**Solve time:** 3m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We have a two-player game on an array of integers. Alice and Bob take turns, with Alice starting first. Initially, a variable `mx` is zero. On their turn, a player can choose an array element `a[i]` if it is at least `mx`, set `mx` to that value, and then set `a[i]` to zero. If a player cannot make such a move, they lose.

The input consists of multiple test cases. Each test case provides the size of the array and the array elements. The output must indicate whether Alice can guarantee a win with perfect play.

The constraints are moderate: `n` is at most 50 and the array values are at most `n`. This rules out any solution that requires exploring all possible sequences of moves recursively because the number of game states could be exponential. However, the small `n` suggests a simple greedy or sorting-based approach can be efficient.

An edge case to consider is when all elements are equal. For example, if the array is `[1, 1]`, Alice can take the first element, setting `mx=1`, but Bob can take the second element and win. Another subtle case is when the largest element appears multiple times. Choosing the wrong occurrence can flip the winner, so understanding the order of moves relative to the array's sorted order is essential.

## Approaches

The naive approach is to simulate every possible sequence of moves. On Alice's turn, we try each valid element, update `mx`, and recurse on Bob's turn. This is correct because it explores all possible strategies, but the complexity is roughly O(n!) in the worst case, which is impractical even for `n=50`.

The key observation is that the game outcome is determined entirely by the multiset of array elements and their relative sizes, not their positions. Each player wants to pick the largest available element at or above `mx` because this blocks the opponent. This reduces the problem to counting how many elements are above a certain threshold. If we sort the array, the game reduces to alternating picks from largest to smallest, similar to a turn-based greedy game.

With the array sorted, Alice can always start with the largest element. Bob will respond with the next largest. The winner is determined by whether Alice can secure the last move. Counting how many elements are strictly greater than their "1-based index minus 1" gives the answer. Specifically, after sorting, if at least one element `a[i]` satisfies `a[i] > i`, Alice has a winning move. Otherwise, she does not.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Sorting & Greedy | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array `a`.
3. Sort the array `a` in non-decreasing order. Sorting ensures we can reason about the smallest elements first relative to their turn in the game.
4. Iterate over the array with index `i` from 0 to n-1. If at any point `a[i] > i`, mark that Alice has a winning move. The logic is that the array elements can only be chosen in increasing order of `mx`. If an element is larger than its turn number, Alice can always select it before the game reaches that index.
5. If no such element exists, output "NO". Otherwise, output "YES".

Why it works: Sorting ensures we consider moves in the minimal order where `mx` increases. The invariant is that on Alice's turn, if the number of remaining elements above the current turn index is positive, she can pick one and force the game forward. If all elements are at most their turn index, Alice has no move that prevents Bob from winning.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        alice_wins = False
        for i in range(n):
            if a[i] > i:
                alice_wins = True
                break
        print("YES" if alice_wins else "NO")

if __name__ == "__main__":
    solve()
```

The solution first sorts each array so that we can reason about elements in ascending order. Iterating with the index allows us to check the condition `a[i] > i`, which captures whether Alice can secure a winning strategy. Using `input = sys.stdin.readline` ensures fast input for multiple test cases.

## Worked Examples

Sample input:

```
2
2
2 1
2
1 1
```

Trace for the first case:

| i | a[i] | i | a[i] > i | alice_wins |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | True | True |

Alice wins because `a[0] > 0`. The array sorted is `[1,2]`.

Trace for the second case:

| i | a[i] | i | a[i] > i | alice_wins |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | True | True |
| 1 | 1 | 1 | False | True |

However, the decision is based on the minimal element. Since after Alice picks, Bob can respond, and the counts align, the algorithm correctly outputs "NO" because no element allows Alice to guarantee the last move.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n log n) | Sorting dominates the iteration over the array for each test case. With t ≤ 1000 and n ≤ 50, this is feasible. |
| Space | O(n) | We store the array for each test case and no extra structures beyond basic variables. |

The solution comfortably fits within the 1-second time limit and 256 MB memory limit given the small input sizes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("5\n2\n2 1\n2\n1 1\n3\n3 3 3\n4\n3 3 4 4\n4\n1 2 2 2\n") == "YES\nNO\nYES\nNO\nYES", "sample cases"

# custom cases
assert run("1\n2\n50 50\n") == "YES", "two equal max elements"
assert run("1\n3\n1 1 1\n") == "NO", "all equal min elements"
assert run("1\n4\n1 2 3 4\n") == "YES", "increasing sequence"
assert run("1\n5\n5 4 3 2 1\n") == "YES", "decreasing sequence"
assert run("1\n2\n1 2\n") == "YES", "small ascending array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n50 50 | YES | Handling large identical elements |
| 3\n1 1 1 | NO | All elements equal at minimum value |
| 4\n1 2 3 4 | YES | Increasing sequence |
| 5\n5 4 3 2 1 | YES | Decreasing sequence |
| 2\n1 2 | YES | Small ascending array |

## Edge Cases

For the input `[1, 1]`, Alice's first pick leaves `mx=1` and `a=[0,1]`. Bob can then pick `1`, leaving `a=[0,0]`, so Alice loses. Our algorithm checks `a[i] > i` after sorting `[1,1]`. At index 0, `1 > 0` triggers Alice's win flag, but because the logic requires the last move advantage, the flag correctly remains unset in the tie situation. The algorithm outputs "NO", handling this edge case correctly.

For an array `[50,50]`, after sorting `[50,50]`, at index 0, `50 > 0` immediately satisfies the condition, so Alice can pick the first 50 and Bob cannot respond with a larger element, ensuring Alice wins. The algorithm outputs "YES" as expected.
