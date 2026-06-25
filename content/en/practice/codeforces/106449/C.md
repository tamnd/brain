---
title: "CF 106449C - Bag Balancing"
description: "The problem asks whether a set of grocery items can be split between two bags so that the total weight in both bags is exactly the same. Each item must go into exactly one bag."
date: "2026-06-25T09:21:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106449
codeforces_index: "C"
codeforces_contest_name: "2026 Spring UT CS104c Midterm #2"
rating: 0
weight: 106449
solve_time_s: 35
verified: true
draft: false
---

[CF 106449C - Bag Balancing](https://codeforces.com/problemset/problem/106449/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks whether a set of grocery items can be split between two bags so that the total weight in both bags is exactly the same. Each item must go into exactly one bag. The input gives the number of items and the weight of every item, and the output is whether such a division exists.

The key detail is that the total weight of all items is small enough to make the target sum manageable. Although the number of items can reach 100, the total weight does not exceed 1000. This immediately suggests that solutions depending on the total weight rather than the number of possible subsets are reasonable. A brute force solution that tries every subset would need up to $2^{100}$ choices, which is far beyond what can run in a contest. A solution around $O(N \times S)$, where $S$ is the total weight, is easily acceptable because $S$ is at most 1000.

Several edge cases can break a careless implementation. The first is an odd total weight. For input:

```
3
1 2 4
```

the correct output is:

```
no
```

because the two bags would need to each contain half of 7, which is impossible. A solution that only checks if some subset exists without considering the required half may give a wrong result.

Another case is when the total is even but the only possible split uses a single item. For input:

```
3
1 2 3
```

the correct output is:

```
yes
```

because one bag can contain the item with weight 3 and the other can contain weights 1 and 2. Implementations that assume both bags need multiple items would fail.

A final common mistake is forgetting that items are individual objects. For:

```
3
100 100 100
```

the output is:

```
no
```

The total is 300, but no subset has weight 150. Counting only the possible sums of weights without tracking achievable sums correctly can lead to incorrect conclusions.

## Approaches

The direct approach is to try every possible assignment of items to the first bag. Each item has two choices, so with $N$ items this creates $2^N$ possible distributions. For each distribution we can calculate the weight of one bag and check whether it equals half of the total. This is correct because it explores every possible way to split the items. The problem is the number of operations. With $N = 100$, the search space is around $1.27 \times 10^{30}$, which is impossible to traverse.

The useful observation is that the weights, not the number of items, are the limiting factor. We only care whether a certain total weight can be formed by choosing some items. Since the final target is at most 500, we can store all reachable sums while processing the items one by one. This turns the problem into a subset sum problem.

The brute force works because it checks every possible subset. It fails because there are too many subsets. The observation that the total weight is small lets us replace the search over subsets with a dynamic programming state that represents all achievable weights.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N) | O(1) | Too slow |
| Dynamic Programming | O(N × S) | O(S) | Accepted |

## Algorithm Walkthrough

1. Read all item weights and calculate the total weight. If the total weight is odd, immediately output `no` because two equal bags would require a non integer half.
2. Let the target weight be half of the total. Create a dynamic programming array where `dp[x]` means that it is possible to choose some processed items whose total weight is exactly `x`.
3. Initialize `dp[0]` as true because choosing no items creates a sum of zero.
4. Process every item weight. For each possible current sum, update whether adding this item creates a new reachable sum. The iteration must go from larger sums down to smaller sums so that the same item is not used multiple times.
5. After all items are processed, check `dp[target]`. If it is true, there is a subset of items for one bag with exactly the target weight, so the other bag automatically has the same weight.

Why it works: the invariant is that after processing any prefix of the items, `dp[x]` is true exactly when some subset of that prefix has total weight `x`. Initially this is true for the empty prefix. When a new item is considered, every old reachable sum either stays reachable by ignoring the item, or creates a new reachable sum by taking the item. Because we update backwards, the item cannot contribute more than once. After processing everything, the target state exactly represents whether a valid first bag exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)
    weights = list(map(int, input().split()))

    total = sum(weights)

    if total % 2:
        print("no")
        return

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for w in weights:
        for s in range(target - w, -1, -1):
            if dp[s]:
                dp[s + w] = True

    print("yes" if dp[target] else "no")

if __name__ == "__main__":
    solve()
```

The solution first computes the total weight because the target state is determined by the final balance requirement. The odd total check avoids unnecessary dynamic programming work and handles an impossible case immediately.

The `dp` array only stores values from zero to half of the total because sums above the target can never be part of a valid answer. The reverse loop is the critical implementation detail. If the loop moved upward, a weight could be added to a sum created using the same item during the same iteration, which would incorrectly allow using an item multiple times.

Python integers do not have overflow concerns here because the largest stored value is only 1000, but limiting the array size still keeps the implementation simple and efficient.

## Worked Examples

For the first sample:

```
6
30 100 70 20 1 21
```

The total is 242, so the target is 121.

| Item processed | Weight | Newly reachable target state |
| --- | --- | --- |
| Start | 0 | 0 |
| 30 | 30 | 30 |
| 100 | 100 | 100, 130 |
| 70 | 70 | 70, 100, 121 |
| 20 | 20 | 20, 30, 50, 70, 90, 120 |
| 1 | 1 | 121 becomes reachable |
| 21 | 21 | 121 remains reachable |

The dynamic programming finds that 121 can be formed, for example with weights 100, 20, and 1. The remaining items also total 121, so the answer is `yes`.

For the second sample:

```
3
100 100 100
```

The total is 300, so the target is 150.

| Item processed | Weight | Is 150 reachable |
| --- | --- | --- |
| Start | 0 | No |
| 100 | 100 | No |
| 100 | 200 | No |
| 100 | 300 | No |

No subset creates weight 150, so the output is `no`. This demonstrates why checking only whether the total is even is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N × S) | Each item updates all possible sums up to the target, where S is the total weight bound. |
| Space | O(S) | The DP array stores one boolean for every possible sum. |

The maximum total weight is only 1000, so the dynamic programming performs at most around 100,000 transitions. This is well within the limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    weights = list(map(int, input().split()))

    total = sum(weights)
    if total % 2:
        return "no\n"

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for w in weights:
        for s in range(target - w, -1, -1):
            if dp[s]:
                dp[s + w] = True

    return ("yes" if dp[target] else "no") + "\n"

assert solution("6\n30 100 70 20 1 21\n") == "yes\n"
assert solution("3\n100 100 100\n") == "no\n"

assert solution("1\n1\n") == "no\n"
assert solution("4\n5 5 5 5\n") == "yes\n"
assert solution("5\n1 2 4 8 16\n") == "no\n"
assert solution("6\n1 2 4 8 16 31\n") == "yes\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `no` | Minimum size and odd total handling |
| `5 5 5 5` | `yes` | Equal values and direct split |
| `1 2 4 8 16` | `no` | Cases where greedy choices fail |
| `1 2 4 8 16 31` | `yes` | Large target construction |

## Edge Cases

For the odd total case:

```
3
1 2 4
```

the algorithm calculates a total of 7. Since 7 cannot be divided into two equal integer weights, it returns `no` before building the DP table.

For the single item split case:

```
3
1 2 3
```

the target is 3. Processing the weights makes `dp[3]` true after considering the last item, so the algorithm returns `yes`. It does not require both bags to contain the same number of items, only the same weight.

For repeated weights:

```
3
100 100 100
```

the target is 150. The DP states become 100, then 200, then 300, but 150 is never reached. The algorithm correctly rejects the arrangement instead of assuming an even total is sufficient.
