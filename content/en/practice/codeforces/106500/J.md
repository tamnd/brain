---
title: "CF 106500J - Valuable Prizes"
description: "The contest organizers have gift cards and want to give exactly seven of them to the top seven contestants. After sorting the chosen cards from the first place prize down to the seventh place prize, the values must satisfy two fairness rules."
date: "2026-06-25T08:37:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106500
codeforces_index: "J"
codeforces_contest_name: "XXVIII Interregional Programming Olympiad, Vologda SU, 2026"
rating: 0
weight: 106500
solve_time_s: 45
verified: true
draft: false
---

[CF 106500J - Valuable Prizes](https://codeforces.com/problemset/problem/106500/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The contest organizers have gift cards and want to give exactly seven of them to the top seven contestants. After sorting the chosen cards from the first place prize down to the seventh place prize, the values must satisfy two fairness rules. The first place prize cannot be too large compared with the second and third place prizes together. Also, the first three prizes together must be smaller than the last four prizes together. Among all possible fair selections, we need the maximum total value of the seven chosen cards.

The input gives the number of available cards and their values. The output is either the largest possible sum of a valid group of seven cards, or `-1` when no such group exists.

The number of cards can be as large as 500000. This immediately rules out checking all groups of seven, because that would require about $N^7$ choices, which is far beyond what a normal time limit allows. Even $O(N^2)$ is too large for the maximum input size. We need a solution close to sorting complexity, such as $O(N \log N)$ or $O(N)$ after sorting.

The tricky part is that the largest seven values are not always the answer. A very large first prize can break the first inequality, and the distribution of the seven values matters. For example, with:

```
7
1 2 3 4 5 6 7
```

the only possible group is all cards. The output is:

```
-1
```

A careless solution that only checks the total sum of the seven largest cards would return 28, but the largest prize 7 is not smaller than 6 plus 5, so the distribution is invalid.

Another edge case appears when there are extra large cards that should be ignored. For:

```
10
5 5 5 5 5 5 10 5 5 5
```

the answer is:

```
35
```

A naive greedy approach might include the 10 because it increases the total sum. However, after sorting the chosen values as `5 5 5 5 5 5 10`, the first inequality becomes `10 < 5 + 5`, which is false. The correct solution leaves the 10 unused.

## Approaches

The direct approach is to try every set of seven cards, sort those seven values, and check the two conditions. It is correct because every possible answer is considered. The issue is the number of possibilities. Choosing seven cards from 500000 gives an enormous number of combinations, so this method cannot finish.

The key observation is that a valid group of seven has a very specific structure. Sort all card values increasingly. Consider any valid selection:

```
a0 <= a1 <= a2 <= a3 <= a4 <= a5 <= a6
```

The two middle values `a4` and `a5` separate the conditions. The largest value only needs to be smaller than `a4 + a5`, while the first four values only need to have a sum larger than `a4 + a5`.

If a valid group is not already seven consecutive elements in the sorted array, we can replace the selected elements with a better consecutive window ending at the same largest selected element. Every replaced value is at least as large as the old one, and the two inequalities do not become harder to satisfy because the middle and lower parts only increase. Repeating this transformation gives an optimal answer that is a consecutive block of seven after sorting.

Now the problem becomes checking every window of size seven. Since the window size is fixed, every check is constant time using prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^7) | O(7) | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Sort all card values in increasing order. The optimal answer can be represented as seven consecutive values after sorting, so sorting allows us to examine only those candidates.
2. Build prefix sums of the sorted array. We need fast computation of the sum of any group of four or seven values while scanning.
3. For every starting index `i` of a window of size seven, let the values be:

`a[i], a[i+1], ..., a[i+6]`.

The first condition becomes:

`a[i+6] < a[i+4] + a[i+5]`.

The largest prize is compared with the two prizes below it, so these three positions are fixed inside the window.
4. Check the second condition:

`a[i+4] + a[i+5] < a[i] + a[i+1] + a[i+2] + a[i+3]`.

The last four prizes must outweigh the first three prizes. Prefix sums let us compute the four-element sum immediately.
5. If both conditions hold, update the answer with the sum of the seven values in this window.
6. If no window works, output `-1`.

Why it works: the transformation argument shows that an optimal valid choice can always be shifted into a consecutive sorted window without decreasing its total value or breaking the inequalities. The scan checks every possible optimal form, so the maximum valid window found is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    pref = [0] * (n + 1)
    for i, x in enumerate(a):
        pref[i + 1] = pref[i] + x

    ans = -1

    for i in range(n - 6):
        middle = a[i + 4] + a[i + 5]

        if a[i + 6] < middle:
            first_four = pref[i + 4] - pref[i]
            if middle < first_four:
                total = pref[i + 7] - pref[i]
                if total > ans:
                    ans = total

    print(ans)

if __name__ == "__main__":
    solve()
```

The sorting step places the cards in the order needed for the window argument. After sorting, a valid distribution can be checked without trying permutations because the sorted order uniquely determines the contestant ranking.

The prefix sum array stores the sum of every prefix of the sorted cards. The expression `pref[i + 7] - pref[i]` gives the sum of a complete seven-card window, while `pref[i + 4] - pref[i]` gives the four smallest cards inside the window.

The loop stops at `n - 7` because every checked segment must contain exactly seven elements. The inequalities use indices relative to the window, so the middle pair is always positions `i + 4` and `i + 5`. No overflow issue exists in Python because integers have arbitrary precision.

## Worked Examples

For the input:

```
8
1 2 3 4 5 6 7 8
```

the sorted array is already:

```
1 2 3 4 5 6 7 8
```

The scan checks:

| Window | Middle pair sum | First four sum | Valid | Total |
| --- | --- | --- | --- | --- |
| 1 2 3 4 5 6 7 | 11 | 10 | No | 28 |
| 2 3 4 5 6 7 8 | 13 | 14 | Yes | 35 |

The second window works because 8 is smaller than 13, and 13 is smaller than 14. The answer becomes 35.

For the input:

```
10
5 5 5 5 5 5 10 5 5 5
```

the sorted array is:

```
5 5 5 5 5 5 5 5 5 10
```

The windows behave as follows:

| Window start | Largest value | Middle pair sum | First four sum | Valid |
| --- | --- | --- | --- | --- |
| 0 | 5 | 10 | 20 | Yes |
| 1 | 5 | 10 | 20 | Yes |
| 2 | 5 | 10 | 20 | Yes |
| 3 | 5 | 10 | 20 | Yes |

The windows containing the value 10 fail because the largest value is too large compared with the middle pair. The best valid sum is 35.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates the single linear scan |
| Space | O(N) | The prefix sum array stores N + 1 values |

The constraints allow sorting 500000 values comfortably. After sorting, every window is checked once, so the remaining work is linear.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    pref = [0] * (n + 1)
    for i, x in enumerate(a):
        pref[i + 1] = pref[i] + x

    ans = -1
    for i in range(n - 6):
        mid = a[i + 4] + a[i + 5]
        if a[i + 6] < mid and mid < pref[i + 4] - pref[i]:
            ans = max(ans, pref[i + 7] - pref[i])

    return str(ans)

assert solution("7\n1 2 3 4 5 6 7\n") == "-1"
assert solution("8\n1 2 3 4 5 6 7 8\n") == "35"
assert solution("10\n5 5 5 5 5 5 10 5 5 5\n") == "35"

assert solution("7\n10 1 1 1 1 1 1\n") == "-1"
assert solution("7\n1 1 1 1 1 1 1\n") == "7"
assert solution("9\n1 2 3 4 5 6 7 8 100\n") == "35"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Seven increasing values | -1 | The largest seven cards may fail the fairness rules |
| Consecutive values from 1 to 8 | 35 | Basic valid window selection |
| Many equal values with one large value | 35 | Rejecting an attractive but invalid large prize |
| One dominant card | -1 | First inequality handling |
| All equal values | 7 | Equal-value boundary case |
| Large outlier after valid values | 35 | Correctly ignoring unusable high values |

## Edge Cases

For the case:

```
7
1 2 3 4 5 6 7
```

the algorithm has only one window. The middle pair is 6 and 5, giving 11. The largest value 7 satisfies the first inequality, but the first four values sum to 10, which is not larger than 11. The algorithm rejects the window and prints `-1`.

For the case:

```
10
5 5 5 5 5 5 10 5 5 5
```

the sorted array places the 10 at the end. Any window containing it has largest value 10 and middle pair sum 10, so the strict inequality `10 < 10` fails. The remaining windows contain only 5s, giving a valid total of 35.

For the case:

```
7
1 1 1 1 1 1 1
```

all values are equal. The largest value is 1 and the middle pair sum is 2. The first four values sum to 4, so both inequalities hold. The algorithm returns the full sum, 7.
