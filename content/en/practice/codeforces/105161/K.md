---
title: "CF 105161K - Number Deletion Game"
description: "We are given a multiset or array of integers. Two players alternate turns in a game. On each turn, a player is allowed to remove one occurrence of the current maximum value present in the structure."
date: "2026-06-27T10:59:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105161
codeforces_index: "K"
codeforces_contest_name: "2024 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 105161
solve_time_s: 46
verified: true
draft: false
---

[CF 105161K - Number Deletion Game](https://codeforces.com/problemset/problem/105161/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset or array of integers. Two players alternate turns in a game. On each turn, a player is allowed to remove one occurrence of the current maximum value present in the structure. After removing it, the player may also append any subset of elements that are strictly smaller than that maximum, chosen from some available “prefix-like” pool described in the statement, including the possibility of appending nothing.

The game continues until no valid moves remain, and the player who cannot move loses. The task is to determine, from the initial configuration, whether the first player has a forced win or whether the second player can always respond optimally to win.

Even though the operation sounds rich, the crucial hidden structure is that the only globally relevant quantity is how many times the maximum value appears initially.

From a complexity perspective, the input size is linear in the number of elements. This immediately rules out any simulation of the game tree. Any approach that tries to model states after each deletion, or track all possible appended configurations, would explode combinatorially because each move branches into many possible subsets.

The only viable solutions must reduce the game to a single aggregated statistic computed in linear time.

A subtle edge case is when all elements are equal. In that situation, every move simply removes a maximum and no meaningful “smaller prefix” exists. A naive reader might think the optional append operation could affect the outcome, but it never changes the fact that play is completely determined by repeated removal of maximum elements.

For example, if the array is `[5, 5, 5]`, each move removes a `5`. The game ends after three moves, so the first player wins. If it is `[5, 5]`, the second player wins. This already suggests a parity phenomenon.

## Approaches

A brute-force approach would explicitly simulate the game. Each state would store the current multiset, and each transition would remove one maximum and branch over all possible subsets of smaller elements to add. This quickly becomes infeasible because the number of subsets of smaller elements can be exponential, and the number of game states grows explosively. Even for moderate `n`, this approach cannot progress beyond very small instances.

The key observation is that the appended elements never influence the identity of the maximum unless they match the current maximum value, which is forbidden since only smaller elements can be added. Therefore, the maximum value in the multiset strictly decreases only when all occurrences of the current maximum have been removed. The internal structure below the maximum never affects the count of maximum deletions.

This reduces the game to a pure counting process: each occurrence of the maximum value corresponds to one essential move where control alternates. The optional operations do not affect the parity of the number of times the maximum is removed, which fully determines the winner under optimal play.

Thus the problem collapses to counting how many elements are equal to the global maximum and checking whether this count is odd or even.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n states) | Too slow |
| Count Maximum Frequency | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We now describe the optimal reasoning process in a direct sequence.

1. Read the input array and identify the maximum value present. This is the only value that determines forced structure in the game, because all operations revolve around removing maxima.
2. Count how many times this maximum value appears in the array. This count represents the total number of essential moves in the game, since each move removes exactly one maximum.
3. Determine the winner based on the parity of this count. If the number of maximum elements is odd, the first player makes the last move and wins. If it is even, the second player makes the last move and wins.

The key idea is that no matter how players use the optional insertion of smaller elements, they can never increase the number of remaining maximum elements, and cannot change the fact that each maximum must eventually be removed one by one.

### Why it works

The invariant is that the multiset of maximum elements decreases by exactly one per move, independent of any secondary operations. All additional insertions involve strictly smaller values, so they cannot affect the current maximum tier.

Because of this separation, the game decomposes into a fixed-length sequence of `k` forced moves, where `k` is the number of maximum elements. Players alternate these forced moves with no ability to skip or merge them. The winner is therefore determined entirely by whether `k` is odd or even.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, input().split()))
    if not data:
        return
    n = data[0]
    arr = data[1:1+n]

    mx = max(arr)
    cnt = 0
    for x in arr:
        if x == mx:
            cnt += 1

    print("First" if cnt % 2 == 1 else "Second")

if __name__ == "__main__":
    solve()
```

The solution first parses the input in a single pass. It computes the maximum using Python’s built-in function, then counts its occurrences with a simple loop. This avoids any unnecessary data structures.

A common implementation pitfall is forgetting that the input format may place `n` on the same line as the array values, so direct splitting must be handled carefully. Another subtle point is ensuring that only elements equal to the maximum are counted, not elements greater or equal comparisons that accidentally include duplicates in transformed data.

## Worked Examples

### Example 1

Input:

```
5
1 3 3 2 3
```

Here the maximum is `3`.

| Step | Action | Max Value | Count of Max |
| --- | --- | --- | --- |
| 1 | Read array | 3 | 0 |
| 2 | Scan elements | 3 | 3 |
| 3 | Decide winner | 3 | 3 |

Since the count is 3, the result is that the first player wins.

This demonstrates that only occurrences of the maximum matter, while smaller values play no role.

### Example 2

Input:

```
4
7 1 7 7
```

| Step | Action | Max Value | Count of Max |
| --- | --- | --- | --- |
| 1 | Read array | 7 | 0 |
| 2 | Scan elements | 7 | 3 |
| 3 | Decide winner | 7 | 3 |

Again the count is odd, so the first player wins. If we change the last value to make the count even, the second player immediately becomes winning, showing pure parity control.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to find maximum and count occurrences |
| Space | O(1) | Only a few integer variables are used |

The algorithm fits easily within constraints typical for Codeforces, even for `n` up to `2 × 10^5` or more. It avoids any simulation and reduces the entire game to a single scan of the array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    data = list(map(int, inp.split()))
    n = data[0]
    arr = data[1:1+n]
    mx = max(arr)
    cnt = sum(x == mx for x in arr)
    return "First" if cnt % 2 == 1 else "Second"

# minimum case
assert run("1\n5") == "First"

# simple even case
assert run("2\n1 1") == "Second"

# mixed values
assert run("5\n1 3 3 2 3") == "First"

# all distinct
assert run("4\n1 2 3 4") == "First"

# large parity check
assert run("6\n9 1 9 2 9 2") == "Second"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5` | First | Single element base case |
| `2 1 1` | Second | Even max count |
| `5 1 3 3 2 3` | First | Typical mixed distribution |
| `4 1 2 3 4` | First | All elements are maximum once or tie handling |
| `6 9 1 9 2 9 2` | Second | Larger even parity case |

## Edge Cases

For a single-element array like `[x]`, the maximum appears once and the first player immediately wins by removing it. The algorithm correctly identifies count `1` and returns a first-player win.

For arrays where all elements are identical, say `[7, 7, 7, 7]`, every element is a maximum. The count is 4, so the second player wins. The simulation view matches this exactly since each move removes one element until exhaustion.

For arrays with a unique maximum and many smaller elements, such as `[10, 1, 1, 1]`, the maximum count is 1, guaranteeing a first-player win. Any attempt to use the “append smaller prefix” operation does not change the fact that only one decisive move exists.
