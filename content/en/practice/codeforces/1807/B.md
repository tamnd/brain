---
title: "CF 1807B - Grab the Candies"
description: "We have several bags of candies. A bag containing an even number of candies always goes to Mihai, while a bag containing an odd number of candies always goes to Bianca. The order of the bags is not fixed. We may rearrange them however we want before the game starts."
date: "2026-06-09T09:02:16+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1807
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 859 (Div. 4)"
rating: 800
weight: 1807
solve_time_s: 86
verified: true
draft: false
---

[CF 1807B - Grab the Candies](https://codeforces.com/problemset/problem/1807/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several bags of candies. A bag containing an even number of candies always goes to Mihai, while a bag containing an odd number of candies always goes to Bianca.

The order of the bags is not fixed. We may rearrange them however we want before the game starts. As the bags are processed from left to right, each player accumulates candies from the bags they receive.

The goal is to determine whether there exists some ordering such that after every processed bag, except before the game starts, Mihai's total number of candies is strictly greater than Bianca's total.

The constraints are very small. Each test case has at most 100 bags, and there are at most 1000 test cases. Even an $O(n^2)$ solution would be easily fast enough. The challenge is not efficiency, but recognizing the property that determines whether a valid ordering exists.

A common mistake is to focus on maintaining the inequality after every step by constructing an explicit ordering. For example:

```
1
4
1 2 3 4
```

A greedy simulation can find an ordering, but the problem only asks whether one exists. There is a much simpler condition.

Another subtle case is when there is only one even bag:

```
1
4
1 1 1 2
```

The total even candies are $2$, while the total odd candies are $3$. Mihai cannot stay ahead forever because Bianca's total eventually exceeds Mihai's. The correct answer is `NO`.

A third edge case is when all bags are odd:

```
1
3
1 3 5
```

The first processed bag must go to Bianca, making Mihai's total $0$ and Bianca's positive. The required inequality fails immediately. The correct answer is `NO`.

Finally, consider:

```
1
3
2 2 1
```

The even sum is $4$ and the odd sum is $1$. The correct answer is `YES`. A careless approach that only checks the largest even value against the largest odd value would miss this.

## Approaches

The most direct brute-force idea is to try every possible permutation of the bags and simulate the game. For each permutation, we process the bags one by one, updating Mihai's and Bianca's totals and checking whether Mihai remains strictly ahead after every step.

This approach is correct because it examines every possible ordering. The problem is that there are $n!$ permutations. Even for $n = 10$, this is already about 3.6 million permutations. For $n = 100$, it is completely impossible.

To find a better solution, we need to understand what actually matters.

Suppose we place all even bags first. Every one of those bags increases only Mihai's total. This is clearly the best possible way to build an advantage. After all even bags have been processed, Mihai has collected the entire sum of even-valued bags, while Bianca still has collected nothing.

Now the odd bags can be processed in any order. Every odd bag increases only Bianca's total. Mihai's total never changes again.

This observation is crucial. If the total sum of all even bags is greater than the total sum of all odd bags, then after processing all even bags first, Mihai starts the odd phase with a lead larger than Bianca's eventual final total. Bianca can never catch up, so every intermediate state is also safe.

If the total sum of even bags is less than or equal to the total sum of odd bags, then at the end of the entire process Mihai's total is not strictly greater than Bianca's total. Since the requirement must hold after every step, it certainly must hold after the last step. Such an ordering cannot exist.

The entire problem reduces to comparing two sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For a test case, initialize two variables: `even_sum` and `odd_sum`.
2. Traverse all bags.
3. If a bag contains an even number of candies, add its value to `even_sum`.
4. Otherwise, add its value to `odd_sum`.
5. After processing all bags, compare the two totals.
6. If `even_sum > odd_sum`, print `YES`.
7. Otherwise, print `NO`.

Why it works:

The final totals are fixed regardless of ordering. Mihai always ends with the sum of all even-valued bags, and Bianca always ends with the sum of all odd-valued bags.

If `even_sum <= odd_sum`, the required inequality already fails at the final state, so no ordering can work.

If `even_sum > odd_sum`, place every even bag before every odd bag. During the first phase, Bianca's total remains zero while Mihai's total increases. During the second phase, Mihai's total stays equal to `even_sum`, and Bianca's running total never exceeds `odd_sum`. Since `even_sum > odd_sum`, Mihai remains strictly ahead throughout the process.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    even_sum = 0
    odd_sum = 0

    for x in a:
        if x % 2 == 0:
            even_sum += x
        else:
            odd_sum += x

    print("YES" if even_sum > odd_sum else "NO")
```

The solution follows the proof directly.

The loop separates all bag values into two groups according to parity. `even_sum` represents Mihai's eventual total, while `odd_sum` represents Bianca's eventual total.

After all values are processed, only one comparison is needed. The strict inequality is important. Using `>=` would be wrong because the statement requires Mihai to have strictly more candies at every valid moment, including the final state.

No special handling is needed for empty parity groups. If there are no even bags, `even_sum` becomes zero and the comparison naturally produces the correct result.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 4
```

| Bag Value | Parity | even_sum | odd_sum |
| --- | --- | --- | --- |
| 1 | Odd | 0 | 1 |
| 2 | Even | 2 | 1 |
| 3 | Odd | 2 | 4 |
| 4 | Even | 6 | 4 |

Final comparison:

| even_sum | odd_sum | Answer |
| --- | --- | --- |
| 6 | 4 | YES |

The even-valued bags contribute a total of 6 candies, while the odd-valued bags contribute 4. Since 6 is greater than 4, placing all even bags first guarantees Mihai stays ahead.

### Example 2

Input:

```
4
1 1 1 2
```

| Bag Value | Parity | even_sum | odd_sum |
| --- | --- | --- | --- |
| 1 | Odd | 0 | 1 |
| 1 | Odd | 0 | 2 |
| 1 | Odd | 0 | 3 |
| 2 | Even | 2 | 3 |

Final comparison:

| even_sum | odd_sum | Answer |
| --- | --- | --- |
| 2 | 3 | NO |

The final total available to Bianca is larger than Mihai's final total. Since the required inequality must also hold after the last bag, no ordering can succeed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each bag is examined exactly once |
| Space | $O(1)$ | Only two running sums are stored |

With at most 100 bags per test case, the running time is tiny. Even across 1000 test cases, the solution performs only about 100,000 operations, comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        even_sum = sum(x for x in a if x % 2 == 0)
        odd_sum = sum(x for x in a if x % 2 == 1)

        ans.append("YES" if even_sum > odd_sum else "NO")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""3
4
1 2 3 4
4
1 1 1 2
3
1 4 3
"""
) == "YES\nNO\nNO"

# minimum size
assert run(
"""1
1
2
"""
) == "YES"

# single odd bag
assert run(
"""1
1
1
"""
) == "NO"

# all equal even values
assert run(
"""1
5
2 2 2 2 2
"""
) == "YES"

# equality boundary
assert run(
"""1
2
1 1
"""
) == "NO"

# larger mixed case
assert run(
"""1
6
2 4 6 1 3 5
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 2` | `YES` | Minimum size with an even bag |
| `1 / 1 / 1` | `NO` | Minimum size with an odd bag |
| `2 2 2 2 2` | `YES` | All values even |
| `1 1` | `NO` | Strict inequality, equality is insufficient |
| `2 4 6 1 3 5` | `YES` | Mixed parities with larger even total |

## Edge Cases

### All Bags Are Odd

Input:

```
1
3
1 3 5
```

The algorithm computes:

| even_sum | odd_sum |
| --- | --- |
| 0 | 9 |

Since `0 > 9` is false, it prints `NO`.

This matches reality. The first processed bag must go to Bianca, so Mihai cannot be strictly ahead after the first move.

### Equal Totals

Input:

```
1
2
1 1
```

The algorithm computes:

| even_sum | odd_sum |
| --- | --- |
| 0 | 2 |

The answer is `NO`.

More generally, whenever the two totals are equal, the final state would have Mihai and Bianca tied. The condition requires Mihai to be strictly ahead, so equality cannot be accepted.

### Only One Even Bag

Input:

```
1
4
1 1 1 2
```

The algorithm computes:

| even_sum | odd_sum |
| --- | --- |
| 2 | 3 |

The answer is `NO`.

Even if the bag containing 2 candies is placed first, Mihai's maximum possible final total is still only 2. Bianca eventually reaches 3, so the required inequality cannot hold until the end.

### Large Even Advantage

Input:

```
1
3
2 2 1
```

The algorithm computes:

| even_sum | odd_sum |
| --- | --- |
| 4 | 1 |

The answer is `YES`.

Place the even bags first: `[2, 2, 1]`.

After processing the bags, the running totals are:

| Step | Mihai | Bianca |
| --- | --- | --- |
| After 2 | 2 | 0 |
| After 2 | 4 | 0 |
| After 1 | 4 | 1 |

Mihai stays strictly ahead throughout, exactly as predicted by the condition `even_sum > odd_sum`.
