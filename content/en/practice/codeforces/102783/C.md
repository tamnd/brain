---
title: "CF 102783C - Optimal Trick or Treating"
description: "Timmy wants to maximize the number of Chuckles bars he can obtain. Each house in the neighborhood contains some collection of candies. Alice has a fixed exchange rate for each candy type, meaning every candy type is worth a certain number of Chuckles bars."
date: "2026-07-27T20:02:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102783
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 2"
rating: 0
weight: 102783
solve_time_s: 60
verified: true
draft: false
---

[CF 102783C - Optimal Trick or Treating](https://codeforces.com/problemset/problem/102783/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

Timmy wants to maximize the number of Chuckles bars he can obtain. Each house in the neighborhood contains some collection of candies. Alice has a fixed exchange rate for each candy type, meaning every candy type is worth a certain number of Chuckles bars. When Timmy visits a house, he takes every candy that house offers, converts all of those candies through Alice’s rates, and receives the corresponding number of Chuckles bars. He can visit only a limited number of houses, so the task is to choose the best set of houses. The problem asks for the largest total value Timmy can obtain.

The input first describes the exchange market. Each candy name has a value representing how many Chuckles bars Alice gives for one piece of that candy. After that, the houses are described. Each house lists the candy types it contains and the quantities of those candies. The output is the maximum Chuckles bar total after selecting at most the allowed number of houses.

The limits are small enough to allow direct processing. There are at most 200 candy types and 200 houses. A solution that performs a small amount of work per candy entry is easily fast enough because the total number of house entries is bounded by the number of houses times the number of candy types. A quadratic approach over the houses is also acceptable here, but anything involving enumerating every possible subset of houses would become impossible because 2^200 possible choices cannot be explored.

The main edge cases come from incorrectly handling houses with small values or assuming that exactly k houses must always contribute. For example, if there is only one house and Timmy can visit one house, the answer must simply be the value of that house.

Example input:

```
1
Chocolate 5
1 1
1
Chocolate 3
```

The output is:

```
15
```

A careless implementation might accidentally multiply by the number of candy types instead of the quantity of candies, producing 5 instead of 15.

Another common mistake is ignoring houses that contain multiple candy types.

Example input:

```
2
A 2
B 10
2 1
1
A 5
1
B 1
```

The output is:

```
10
```

Choosing the second house is better because it gives 10 Chuckles bars. An implementation that only tracks the number of candy types or the first candy seen in each house could choose incorrectly.

A final boundary case is when all houses have identical values.

Example input:

```
1
Candy 7
3 2
1
Candy 1
1
Candy 1
1
Candy 1
```

The output is:

```
14
```

The chosen houses do not matter, but the algorithm must still correctly select exactly the best k values rather than relying on strict comparisons that fail when values are equal.

## Approaches

The brute-force idea is to consider every possible group of houses Timmy could visit. For each subset, we calculate the total number of Chuckles bars obtained and keep the maximum. This approach is correct because every valid choice of houses is examined. However, the number of subsets is exponential. With 200 houses, there can be 2^200 possible choices, which is far beyond what can be processed.

The reason brute force is unnecessary comes from the fact that houses do not interact with each other. Visiting one house does not change the value of another house. The value of a house can be calculated independently by summing the value of each candy inside it. Once every house has a single score, the original problem becomes choosing k numbers with the largest sum.

The optimal approach is to compute the value of every house, sort those values in descending order, and add the first k values. Sorting is sufficient because there is no dependency between choices. The best k houses are simply the k houses with the highest individual contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^h * h) | O(h) | Too slow |
| Optimal | O(n + h log h) | O(n + h) | Accepted |

## Algorithm Walkthrough

1. Store the Chuckles bar value of every candy type in a map. The candy names are strings, so the map lets us quickly find the value of any candy appearing in a house.
2. Process each house independently. For every candy in that house, multiply its quantity by its exchange value and add the result to the house’s total value. This converts a collection of different candies into one number representing how valuable the entire house is.
3. Store the total value of every house in an array. At this point, the candy details are no longer needed because all decisions depend only on the total contribution of each house.
4. Sort the house values from largest to smallest. The first k values represent the houses that give Timmy the greatest possible reward.
5. Add those first k values and print the result. Since every selected house contributes independently, choosing any lower-valued house instead of a higher-valued one can never improve the answer.

Why it works:

The key invariant is that after computing all house values, every possible visit decision can be represented only by choosing among these values. If a chosen set contains a house with a smaller value than an unchosen house, swapping those two houses never decreases the total. Repeating this exchange argument leads to exactly the k largest house values, proving that the algorithm always finds an optimal selection.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    value = {}

    for _ in range(n):
        name, v = input().split()
        value[name] = int(v)

    h, k = map(int, input().split())

    houses = []

    for _ in range(h):
        c = int(input())
        total = 0
        for _ in range(c):
            name, amount = input().split()
            total += value[name] * int(amount)
        houses.append(total)

    houses.sort(reverse=True)

    print(sum(houses[:k]))

if __name__ == "__main__":
    solve()
```

The dictionary stores the exchange rates because candy names are arbitrary strings and direct lookup avoids repeatedly searching through all deals.

Each house is converted into a single integer value. The multiplication step is essential because a house may contain many copies of one candy type, and each copy contributes independently.

Sorting in reverse order places the most profitable houses at the beginning of the list. Python integers handle the possible multiplication results without overflow concerns.

The slice `houses[:k]` is safe because the input guarantees that k is not larger than the number of houses. The final sum only includes the houses Timmy is allowed to visit.

## Worked Examples

For the sample input:

```
3
LactoseyWay 2
Twicks 3
DigDog 5
2 1
2
LactoseyWay 3
Twicks 1
1
DigDog 2
```

The house calculations are:

| House | Candy calculation | House value |
| --- | --- | --- |
| 1 | 3 * 2 + 1 * 3 | 9 |
| 2 | 2 * 5 | 10 |

After sorting:

| Sorted position | Value |
| --- | --- |
| 1 | 10 |
| 2 | 9 |

Only one house can be visited, so Timmy chooses the value 10 house.

The output is:

```
10
```

This trace shows why the problem reduces to selecting the largest independent values.

For another example:

```
2
Cookie 4
Candy 1
3 2
2
Cookie 2
Candy 5
1
Cookie 1
1
Candy 10
```

The calculations are:

| House | Calculation | House value |
| --- | --- | --- |
| 1 | 2 * 4 + 5 * 1 | 13 |
| 2 | 1 * 4 | 4 |
| 3 | 10 * 1 | 10 |

Sorting gives:

| Sorted position | Value |
| --- | --- |
| 1 | 13 |
| 2 | 10 |
| 3 | 4 |

Timmy can visit two houses, so the answer is 23.

This example confirms that a house with many different candies can still be compared directly against a house with only one candy type.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + h log h) | Reading the candy values takes O(n), processing house contents takes O(total candy entries), and sorting h house values takes O(h log h). |
| Space | O(n + h) | The map stores candy values and the array stores one value per house. |

The largest possible input contains only a few hundred houses and candy types, so this complexity easily fits within the limits. The algorithm spends almost all of its work on simple arithmetic and one small sort.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    value = {}

    for _ in range(n):
        name, v = input().split()
        value[name] = int(v)

    h, k = map(int, input().split())

    houses = []

    for _ in range(h):
        c = int(input())
        total = 0
        for _ in range(c):
            name, amount = input().split()
            total += value[name] * int(amount)
        houses.append(total)

    houses.sort(reverse=True)
    print(sum(houses[:k]))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert run("""3
LactoseyWay 2
Twicks 3
DigDog 5
2 1
2
LactoseyWay 3
Twicks 1
1
DigDog 2
""") == "10\n", "sample 1"

assert run("""1
Candy 7
1 1
1
Candy 3
""") == "21\n", "single house"

assert run("""2
A 2
B 10
2 1
1
A 5
1
B 1
""") == "10\n", "choose best house"

assert run("""1
Candy 7
3 2
1
Candy 1
1
Candy 1
1
Candy 1
""") == "14\n", "equal houses"

assert run("""2
X 100
Y 1
3 2
2
X 1
Y 100
1
X 2
1
Y 1000
""") == "301\n", "large quantities and mixed candies"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample input | 10 | Original problem example |
| Single house | 21 | Minimum number of houses |
| Two competing houses | 10 | Correct selection of highest values |
| Equal houses | 14 | Handling identical house values |
| Mixed large quantities | 301 | Multiplication and accumulation correctness |

## Edge Cases

For the single-house case:

```
1
Candy 7
1 1
1
Candy 3
```

The algorithm computes the only house value as 3 * 7 = 21. Sorting does nothing because there is only one value, and the answer is 21.

For the multiple-candy case:

```
2
A 2
B 10
2 1
1
A 5
1
B 1
```

The first house is worth 5 * 2 = 10, while the second house is worth 1 * 10 = 10. Since only one house can be chosen, either choice gives the same answer. This demonstrates that equal values do not require special handling.

For identical houses:

```
1
Candy 7
3 2
1
Candy 1
1
Candy 1
1
Candy 1
```

Each house contributes 7. After sorting, the array remains three copies of 7, and the first two values are selected. The result is 14.

The algorithm handles all of these cases because it never relies on the order of houses or the uniqueness of their values. It only depends on the fact that each house can be evaluated independently.

This can also be adapted into a shorter contest-style editorial or a more formal teaching note if needed.
