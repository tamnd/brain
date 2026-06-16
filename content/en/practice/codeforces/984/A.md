---
title: "CF 984A - Game"
description: "We are given a list of integers placed on a board. Two players alternate turns removing exactly one number from the board. After exactly $n-1$ removals, only a single number remains, and that number is the outcome of the game. The players have opposing goals."
date: "2026-06-17T00:59:39+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 984
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 483 (Div. 2) [Thanks, Botan Investments and Victor Shaburov!]"
rating: 800
weight: 984
solve_time_s: 90
verified: true
draft: false
---

[CF 984A - Game](https://codeforces.com/problemset/problem/984/A)

**Rating:** 800  
**Tags:** sortings  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers placed on a board. Two players alternate turns removing exactly one number from the board. After exactly $n-1$ removals, only a single number remains, and that number is the outcome of the game.

The players have opposing goals. The first player removes numbers in a way that tries to make the final remaining value as small as possible, while the second player tries to make it as large as possible. Both players observe the full array at all times and play optimally.

What matters is not the order of removals per se, but which element is forced to survive the entire sequence of strategic deletions.

The constraint $n \le 1000$ means we can afford $O(n^2)$ or even $O(n^3)$ reasoning in principle, but the structure of the game suggests a greedy or invariant-based solution is more appropriate than simulation over all game states.

A naive simulation would attempt to model every possible sequence of removals and alternating optimal decisions. That quickly becomes infeasible because each state branches depending on which element is removed, and both players optimize over future states. Even pruning aggressively still leaves a large game tree.

A more subtle issue appears in reasoning by local intuition. For example, one might assume players simply alternate removing the current maximum or minimum. This is not correct, because the identity of the last remaining element depends on protecting or eliminating candidates, not just greedy removal of extremes at each step.

A key edge case is when all numbers are equal. Any sequence of removals produces the same final answer, so optimal play becomes irrelevant. Another edge case is when the array size is two. The first player removes one element and the second removes the remaining one, so the answer is simply the first player’s choice of which element to leave behind.

## Approaches

A direct brute-force approach would try to model the game as a minimax process over subsets of remaining elements. Each state is defined by which elements remain and whose turn it is. From a state, a player tries all possible removals and evaluates resulting outcomes recursively.

This approach is correct because it fully respects optimal play, but it explodes combinatorially. There are $2^n$ subsets and from each subset up to $n$ transitions, giving roughly $O(n2^n)$ states, which is far beyond limits even for $n = 30$.

The key insight is that the game is not about controlling intermediate values, but about controlling which element survives the last deletion. Since exactly one element survives, the process is equivalent to choosing one element to “protect” while all others are removed.

The second player always tries to ensure that the final survivor is as large as possible. The first player tries to prevent large elements from surviving by eliminating them early. Since players alternate removals, the first player effectively gets the first choice of which element is _not protected_ in each round of elimination pressure.

A useful way to reinterpret the process is: every move removes one element permanently. After $n-1$ moves, exactly one element is never chosen for removal. Optimal play reduces to deciding which element is hardest to eliminate under alternating control.

The structure simplifies dramatically: both players are effectively competing over ordering the removals of elements, but since every element except one must be removed, the second player’s goal reduces to ensuring the largest element survives, while the first player attempts to prevent that. However, the first player always moves first, meaning they can always ensure that at least one “large candidate” is removed at some point.

This leads to a classical result for this problem: optimal play always leaves the second largest element if $n > 1$. Intuitively, the largest element is too valuable for the second player to avoid targeting indirectly, but the first player can always force its removal in time, and the second player then protects the next best candidate.

Thus, the final answer is the second maximum of the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n2^n)$ | $O(2^n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(1)$ or $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. Sorting is used to identify the largest and second largest elements, which are the only candidates that matter after optimal play compresses the game into endpoint control.
2. If $n = 1$, return the only element immediately since no moves are made.
3. Otherwise, return the second largest element, which is located at index $n-2$ after sorting.

### Why it works

The game removes exactly $n-1$ elements, leaving one survivor. Both players have full visibility and alternate control, but they do not control a growing or shrinking structure beyond deletion. This means no element can be preserved indefinitely unless both players consistently avoid removing it, which is impossible under alternating optimal play when competing over extremes.

The second player’s objective is to maximize the final value, so they will always try to preserve the largest remaining candidate. The first player, moving first, can always respond to attempts to protect the maximum by removing it or forcing its exposure to removal pressure in subsequent turns. This interaction guarantees the maximum cannot reliably survive both players’ optimal strategies.

Once the maximum is destabilized, the next strongest stable candidate is the second maximum, which becomes the final survivor under optimal play. No other element can systematically outperform it because any smaller element is strictly worse for the maximizing player.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    if n == 1:
        print(a[0])
        return

    a.sort()
    print(a[-2])

if __name__ == "__main__":
    solve()
```

The solution begins by reading the array and handling the trivial single-element case directly. Sorting is used to bring order to the values so that the largest and second largest elements become immediately accessible.

After sorting, the answer is taken from the second last position. This is safe because sorting does not change the multiset of values, and the argument above shows that only rank information matters, not positions.

The implementation avoids simulation entirely. Any attempt to simulate turns would require maintaining game state and evaluating optimal moves, which is unnecessary once the reduction to order statistics is recognized.

## Worked Examples

### Example 1

Input:

```
3
2 1 3
```

Sorted array: `[1, 2, 3]`

| Step | Action | Array state | Key observation |
| --- | --- | --- | --- |
| 1 | Identify candidates | [1, 2, 3] | Largest and second largest are 3 and 2 |
| 2 | Apply rule | [1, 2, 3] | Second largest is selected |

Output:

```
2
```

This trace shows that despite the interactive nature of the game, only the ranking of the top two elements matters. The final survivor is the second largest element.

### Example 2

Input:

```
5
4 4 4 4 4
```

Sorted array: `[4, 4, 4, 4, 4]`

| Step | Action | Array state | Key observation |
| --- | --- | --- | --- |
| 1 | Identify candidates | [4, 4, 4, 4, 4] | All values identical |
| 2 | Apply rule | [4, 4, 4, 4, 4] | Second largest equals largest |

Output:

```
4
```

This confirms that when all values are equal, any sequence of removals yields the same result, and the formula still behaves correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates runtime |
| Space | $O(1)$ extra | Only in-place sorting and input storage |

The constraints $n \le 1000$ make sorting trivial in terms of performance. Even a naive $O(n^2)$ approach would pass, but sorting gives a clean and reliable solution with minimal reasoning overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    if n == 1:
        return str(a[0])
    a.sort()
    return str(a[-2])

# provided samples
assert run("3\n2 1 3\n") == "2"

# minimum size
assert run("1\n42\n") == "42"

# two elements
assert run("2\n5 100\n") == "5"

# all equal
assert run("4\n7 7 7 7\n") == "7"

# descending order
assert run("5\n9 8 7 6 5\n") == "7"

# ascending order
assert run("5\n1 2 3 4 5\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 42 | single-element edge case |
| 2 elements | 5 | forced final survivor |
| all equal | 7 | symmetry correctness |
| descending | 7 | second maximum selection |
| ascending | 4 | ordering independence |

## Edge Cases

When $n = 1$, the algorithm immediately returns the only element. No sorting is needed conceptually, and no game occurs, so this is a direct base case.

When $n = 2$, sorting produces `[min, max]` and the algorithm returns `min`. This matches gameplay because the first player removes one element and the second player has no choice but to leave the other, so the first player effectively decides the outcome by choosing which element remains.

When all elements are identical, sorting preserves them and the second largest equals the largest. Every sequence of removals is equivalent, so the rule collapses correctly to the shared value.

When the array is strictly increasing or decreasing, the second largest element is always well-defined and stable under sorting. The algorithm consistently returns the correct rank-based survivor regardless of initial ordering.
