---
title: "CF 106394B - Cursed Coins"
description: "Alice finds a room containing n chests. Each chest has a value written in a[i]. A positive value means opening that chest gives Alice coins, while a negative value means the chest contains cursed coins and reduces her total."
date: "2026-06-25T10:09:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106394
codeforces_index: "B"
codeforces_contest_name: "RUCP x WiCS Mini-Contest"
rating: 0
weight: 106394
solve_time_s: 34
verified: true
draft: false
---

[CF 106394B - Cursed Coins](https://codeforces.com/problemset/problem/106394/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
# Problem Understanding

Alice finds a room containing `n` chests. Each chest has a value written in `a[i]`. A positive value means opening that chest gives Alice coins, while a negative value means the chest contains cursed coins and reduces her total. Alice owns exactly `k` keys, so she can open at most `k` chests. Her goal is to choose which chests to open so that her final number of coins is as large as possible.

The input contains several independent test cases. For each case, we receive the number of chests, the number of available keys, and the value of every chest. The output is the maximum possible balance after Alice makes the best choice.

The constraints are the main clue. The total number of chests across all test cases can reach `2 * 10^5`, so a solution that tries every subset of chests is impossible. Even checking all choices of `k` chests would be exponential. A solution close to linear or `O(n log n)` per test case is required.

The key edge cases come from the fact that Alice does not have to use every key. A careless implementation may assume she must always open exactly `k` chests.

For example:

```
Input
1
3 2
5 -10 -20

Output
5
```

Alice has two keys, but opening any cursed chest decreases her result. The correct choice is to open only the chest worth `5`. A solution that blindly selects two chests would produce a smaller value.

Another case is when every chest is cursed:

```
Input
1
4 3
-1 -2 -3 -4

Output
0
```

Alice starts with zero coins and can simply avoid using her keys. Sorting values and always taking the first `k` elements without checking their sign would incorrectly make the answer negative.

## Approaches

A direct brute-force approach would try every possible set of chests Alice could open, calculate its total value, and keep the maximum. This is correct because every possible decision is examined. However, the number of subsets is `2^n`, which becomes impossible even for a few dozen chests. With `n = 2 * 10^5`, this approach is far beyond the available time.

A better way to look at the problem is to focus on what contributes to the answer. Opening a chest with a positive value increases the final balance. Opening a chest with a negative value decreases it. Since there is no requirement to spend all keys, negative values never help.

The only useful operation is selecting the largest positive values. If there are fewer than `k` positive chests, Alice takes all of them. If there are more than `k`, she should keep the best `k` positive values because every key spent on a smaller value prevents taking a larger reward.

This observation transforms the problem into a sorting problem. We collect all positive values, sort them from largest to smallest, and add at most `k` of them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

The sorting step dominates the running time. The rest of the algorithm only scans the array and sums selected values.

## Algorithm Walkthrough

1. Read the number of test cases and process each test case independently.
2. Inspect every chest value and keep only values greater than zero. These are the only chests that can improve Alice's balance.
3. Sort the remaining positive values in descending order. The first elements after sorting are the most profitable choices.
4. Add the first `k` values from this sorted list, or all available values if there are fewer than `k`.
5. Print the resulting sum.

The reason this greedy choice works is that every selected chest consumes one key. If a solution contains a smaller positive chest while a larger positive chest is not selected, swapping them increases or keeps the total unchanged. Repeating this exchange leaves only the largest positive values selected.

Why it works: the algorithm maintains the invariant that after considering the available positive chests, the selected values are always the highest possible rewards for the keys used. Negative chests can only decrease the total, so removing them never hurts. The final chosen set is exactly the set with the maximum possible sum.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        positive = [x for x in a if x > 0]
        positive.sort(reverse=True)

        ans.append(str(sum(positive[:k])))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The list comprehension filters out all cursed chests because negative values can never be part of an optimal solution. The sort places the highest rewards first, matching the greedy reasoning from the algorithm section.

The slice `positive[:k]` is also the boundary condition that prevents using more keys than Alice owns. If fewer than `k` profitable chests exist, Python automatically returns the whole list.

The sum uses Python integers, so there is no overflow risk even if the accumulated value exceeds 32-bit or 64-bit ranges.

## Worked Examples

For the first example:

```
Input
3
2 1
5 10
2 1
5 -10
3 3
1 -2 3
```

The first test case chooses one chest because there is one key.

| Step | Positive values | Sorted values | Current answer |
| --- | --- | --- | --- |
| Read chests | 5, 10 | 10, 5 | 0 |
| Take first 1 value | 10 | 10 | 10 |

The algorithm chooses the largest available reward.

The second test case demonstrates that cursed chests are ignored.

| Step | Positive values | Sorted values | Current answer |
| --- | --- | --- | --- |
| Read chests | 5 | 5 | 0 |
| Take first 1 value | 5 | 5 | 5 |

The negative chest never enters consideration.

For the third test case:

| Step | Positive values | Sorted values | Current answer |
| --- | --- | --- | --- |
| Read chests | 1, 3 | 3, 1 | 0 |
| Take first 3 values | 3, 1 | 3, 1 | 4 |

There are only two useful chests, so both are opened even though Alice has three keys.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the positive chest values dominates the work |
| Space | O(n) | The list of positive values may contain every chest |

The total number of chests over all test cases is bounded by `2 * 10^5`, so sorting all collected positive values fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        pos = [x for x in a if x > 0]
        pos.sort(reverse=True)
        res.append(str(sum(pos[:k])))

    return "\n".join(res)

# provided samples
assert solution("""3
2 1
5 10
2 1
5 -10
3 3
1 -2 3
""") == """10
5
4""", "samples"

# minimum size
assert solution("""1
1 1
-7
""") == "0", "all negative minimum"

# all equal values
assert solution("""1
5 3
4 4 4 4 4
""") == "12", "equal positives"

# boundary where k exceeds positive count
assert solution("""1
6 5
8 -1 3 -2 0 4
""") == "15", "ignore non-positive values"

# large k with mixed values
assert solution("""1
7 2
-5 100 -10 50 20 1 -1
""") == "150", "take largest positives only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / -7` | `0` | Alice can choose not to use a key |
| `1 / 5 3 / 4 4 4 4 4` | `12` | Equal positive values are handled correctly |
| `1 / 6 5 / 8 -1 3 -2 0 4` | `15` | Negative and zero values are ignored |
| `1 / 7 2 / -5 100 -10 50 20 1 -1` | `150` | Only the best `k` rewards are selected |

## Edge Cases

When all chests are cursed, the positive list becomes empty. For:

```
Input
1
4 3
-1 -2 -3 -4
```

the algorithm removes every value during filtering. Sorting does nothing, and the sum of the selected values is `0`, which matches Alice choosing no chests.

When there are fewer positive chests than keys:

```
Input
1
5 4
6 -2 3 -8 1
```

the filtered list is `[6, 3, 1]`. After sorting it remains `[6, 3, 1]`, and taking the first four elements simply takes all three values. The answer is `10`.

When there are more profitable chests than keys:

```
Input
1
5 2
9 7 5 3 1
```

the sorted list is `[9, 7, 5, 3, 1]`. Only the first two values are used, giving `16`. Any replacement with a smaller value would decrease the result, so the greedy choice is optimal.
