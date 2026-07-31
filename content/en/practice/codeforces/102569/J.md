---
title: "CF 102569J - The Battle of Mages"
description: "This is an output-only construction problem. There is no input because the task is not to process data, but to print two sets of creature strengths that create a very specific probability relationship."
date: "2026-07-31T07:55:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102569
codeforces_index: "J"
codeforces_contest_name: "2020, XIII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102569
solve_time_s: 91
verified: false
draft: false
---

[CF 102569J - The Battle of Mages](https://codeforces.com/problemset/problem/102569/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
# Problem Understanding

This is an output-only construction problem. There is no input because the task is not to process data, but to print two sets of creature strengths that create a very specific probability relationship.

We need create the first mage's multiset of strengths and the second mage's multiset of strengths. When both mages randomly choose exactly `k` creatures, the first mage must be more likely to win for `k = 1` and `k = 3`, while the second mage must be more likely to win for `k = 2`.

The constraints are small. Each set can contain between 3 and 10 creatures, and every strength must be between 1 and 10. This means the intended solution is not an algorithmic search during execution. We only need to discover one valid construction and print it. The submitted program can simply output fixed numbers.

The subtle part is that ties cause the game to restart. The final winner probability is not determined by the first comparison alone. If the first mage wins a single round with probability `W1`, loses with probability `W2`, and ties with probability `T`, then after removing repeated ties the winner comparison becomes `W1` versus `W2`. So we only need the number of winning outcomes to be greater than the number of losing outcomes for the required values of `k`.

A common mistake is to only compare average strengths. Average strength alone does not determine the winner because the random subset distributions matter. For example, using the sample idea:

```
3
1 2 3
3
2 2 2
```

the first mage has a chance to win for `k = 1`, but for `k = 3` both totals are equal, so the game becomes a draw. The construction needs to control all three subset sizes at once.

## Approaches

The brute-force way to solve this kind of output problem would be to enumerate all possible sets, calculate the probabilities for `k = 1`, `k = 2`, and `k = 3`, and stop when a valid pair is found. Since each set has at most 10 elements and strengths range from 1 to 10, such a search is possible offline. However, putting that search into the submitted solution is unnecessary and much larger than the actual task. A naive enumeration over all multisets of size 10 would consider roughly `C(19,10)` possibilities for each side, which already gives hundreds of thousands of candidates before checking combinations.

The useful observation is that we do not need complicated distributions. A three creature construction is enough. For three creatures, `k = 3` is just a comparison of total sums. We can make the first mage win there by giving the first set a larger total. At the same time, for `k = 2`, the possible pairs are closely related to the total because each pair is the total minus one creature. This lets us make the strongest pairs of the first mage appear too rarely.

The successful construction is:

```
First mage: 1 7 8
Second mage: 5 5 5
```

For `k = 1`, the first mage has two creatures stronger than 5 and one weaker, so he wins more single creature comparisons.

For `k = 2`, the first mage's pair sums are 8, 9, and 15. The second mage's pair sum is always 10. The first mage loses twice and wins once.

For `k = 3`, the totals are 16 and 15, so the first mage wins.

The brute-force idea works because the search space is small enough for discovery, but the final solution can be reduced to printing this one verified construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^10) or worse depending on enumeration | O(1) | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Print the first mage's set as `1 7 8`. The total strength is 16, which is larger than the second mage's total, giving the required advantage when all creatures are selected.
2. Print the second mage's set as `5 5 5`. Its fixed values make the subset comparisons easy to control because every choice has the same strength.
3. Verify the three required cases. With one creature, the first mage has two winning values. With two creatures, the first mage's pair sums are mostly below the second mage's fixed pair sum. With three creatures, the first mage's total is larger.

The reason this construction works is that the same three numbers create opposite behavior for individual creatures and pairs. The high values help for `k = 1`, but combining those high values leaves the first mage with only one very strong pair, causing losses for `k = 2`. The total remains high enough to win for `k = 3`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    print(3)
    print("1 7 8")
    print(3)
    print("5 5 5")

if __name__ == "__main__":
    solve()
```

The program does not read anything because the input is intentionally empty. It directly prints the two creature sets found above.

The first two printed lines describe the first mage's collection, and the next two describe the second mage's collection. There are no loops or calculations because the problem only asks for one valid witness.

The small output format is also why there are no overflow or boundary issues. All values are inside the allowed range.

## Worked Examples

### Example 1

The provided sample is not a valid answer, so we trace the submitted construction instead.

| k | First mage choices | Second mage choices | Result |
| --- | --- | --- | --- |
| 1 | 1, 7, 8 | 5, 5, 5 | Wins: 2, losses: 1 |
| 2 | 8, 9, 15 | 10 | Wins: 1, losses: 2 |
| 3 | 16 | 15 | First mage wins |

This trace shows the key property of the construction. The same set that is stronger in total becomes weaker for most two-creature selections.

### Example 2

| k | First mage choices | Second mage choices | Result |
| --- | --- | --- | --- |
| 1 | 7 versus 5 | 5 | Win |
| 1 | 1 versus 5 | 5 | Loss |
| 2 | 7 + 8 = 15 | 5 + 5 = 10 | Win |
| 2 | 1 + 7 = 8 | 5 + 5 = 10 | Loss |
| 2 | 1 + 8 = 9 | 5 + 5 = 10 | Loss |

This example highlights why checking only the maximum strength is misleading. The first mage has the strongest possible pair, but most pairs are weak.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The program only prints four lines. |
| Space | O(1) | No additional storage is used. |

The constraints are tiny because this is a construction problem. A constant time output solution is comfortably within the limits.

## Test Cases

Since the official input is empty, testing focuses on verifying that the generated output satisfies the format and the probability conditions.

```python
import sys
import io
import itertools

def run(inp: str) -> str:
    return "3\n1 7 8\n3\n5 5 5\n"

def check(output):
    data = list(map(int, output.split()))
    n1 = data[0]
    a = data[1:1+n1]
    n2 = data[1+n1]
    b = data[2+n1:2+n1+n2]

    assert 3 <= n1 <= 10
    assert 3 <= n2 <= 10
    assert all(1 <= x <= 10 for x in a)
    assert all(1 <= x <= 10 for x in b)

    for k in (1, 2, 3):
        x = [sum(c) for c in itertools.combinations(a, k)]
        y = [sum(c) for c in itertools.combinations(b, k)]
        win = sum(i > j for i in x for j in y)
        lose = sum(i < j for i in x for j in y)

        if k in (1, 3):
            assert win > lose
        else:
            assert win < lose

assert run("") == "3\n1 7 8\n3\n5 5 5\n"

check(run(""))

# Minimum size style validation
check("3\n1 7 8\n3\n5 5 5\n")

# Maximum allowed style validation of parser logic
assert len(run("").split()) == 8
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty input | Fixed construction | Matches the output-only requirement |
| Generated output | Same construction | Checks formatting and validity |
| Repeated validation | Same construction | Confirms the probability conditions |

## Edge Cases

The first edge case is when all selected creatures have the same total strength for `k = 3`. A construction like `1 2 3` versus `2 2 2` fails because both totals are 6. The game never produces a winner at `k = 3`. The submitted construction avoids this because `1 + 7 + 8 = 16` and `5 + 5 + 5 = 15`.

The second edge case is relying only on average strength. The first mage's average is higher in the final construction, but that fact alone does not explain the `k = 2` result. The actual pair sums are `8`, `9`, and `15`, so two of three choices lose against the fixed value `10`. A careless solution that checks only totals would miss this behavior.

The third edge case is ties. If the number of winning and losing outcomes were equal, repeated rounds would not create an advantage. Here, for `k = 1`, there are two winning comparisons and one losing comparison. For `k = 2`, there is one winning comparison and two losing comparisons. There are no hidden equalities that change the result.
