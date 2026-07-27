---
title: "CF 102784C - Optimal Trick or Treating"
description: "Timmy knows the candy offers that Alice will accept. Each candy type has a fixed exchange value, meaning every piece of that candy contributes the same number of Chuckles bars. There are several houses, and each house provides a collection of candy types with certain quantities."
date: "2026-07-27T19:53:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102784
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 1"
rating: 0
weight: 102784
solve_time_s: 61
verified: true
draft: false
---

[CF 102784C - Optimal Trick or Treating](https://codeforces.com/problemset/problem/102784/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

Timmy knows the candy offers that Alice will accept. Each candy type has a fixed exchange value, meaning every piece of that candy contributes the same number of Chuckles bars. There are several houses, and each house provides a collection of candy types with certain quantities. Timmy can visit only a limited number of houses, and after visiting a house he takes every candy from it. The goal is to choose the best set of houses so that the total exchange value of all collected candy is as large as possible.

The first part of the input describes the exchange table. For each candy name, we learn how many Chuckles bars one piece of that candy is worth. The remaining input describes each house and the candies available there. The output is the maximum number of Chuckles bars Timmy can obtain after visiting exactly the allowed number of houses.

The constraints are small. There are at most 200 candy types and at most 200 houses, with each house containing information about at most 200 candy types. This means we can afford to inspect every candy entry once and perform operations proportional to the number of houses. A solution that tries every possible group of houses would require exploring combinations of up to 200 houses, which is impossible because the number of choices grows exponentially.

The key observation is that the houses do not interact with each other. Taking one house does not change the value of another house, and there is no restriction on which candy types can be collected together. The only decision is which houses to include. That turns the problem into finding the k largest independent house values.

Several edge cases can break careless implementations. If Timmy can visit only one house, the answer is simply the value of the single most profitable house.

Input:

```
1
Candy 10
3 1
1
Candy 5
1
Candy 2
1
Candy 8
```

Output:

```
50
```

A mistake would be to sum all houses or accidentally choose the first house instead of the maximum one. The third house is the correct choice because five candies worth 10 each give 50 Chuckles bars.

Another edge case is when multiple houses have the same value. The algorithm must allow choosing any of them because the total result is identical.

Input:

```
1
Candy 4
2 2
1
Candy 3
1
Candy 3
```

Output:

```
24
```

A careless implementation that removes duplicate values or uses a set would lose one of the houses and produce the wrong answer. Both houses are needed because Timmy can visit two houses.

A final boundary case is when every house contains different candy types and every house must be visited. In that situation, sorting should still work because the requested number of houses equals the total number of houses.

## Approaches

The direct approach is to calculate the value of every house and then try every possible group of k houses. The value calculation itself is easy: for each candy in a house, multiply the quantity by the exchange value and add it to the house total. The problem appears only when selecting houses. With h houses, checking every possible subset requires 2^h choices. For h = 200, this is far beyond what any program can process.

The reason brute force fails is not because the house calculation is expensive. It fails because the choices are independent but numerous. The important observation is that every house has a final numeric value, and choosing a house never changes the value of another house. Once each house has been converted into its Chuckles bar contribution, the original candy details no longer matter.

This reduces the problem to selecting the k largest numbers from a list of h values. Sorting the list is the simplest way to do this. After sorting in descending order, the first k values are exactly the houses that maximize the total reward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^h * h) | O(h) | Too slow |
| Optimal | O(total candy entries + h log h) | O(h + n) | Accepted |

## Algorithm Walkthrough

1. Read the candy exchange table and store the value of each candy name. The later house descriptions refer back to these names, so we need constant time access to each candy's value.
2. Process each house independently. For every candy type in the house, multiply the number of pieces by its Chuckles bar value and add the result to the house's total value. After this step, each house is represented by a single number.
3. Sort all house values from largest to smallest. The best choices are the houses with the highest individual contributions because there is no interaction between choices.
4. Add the first k values after sorting and output the result. These are the exact houses Timmy should visit.

Why it works: the value of a group of houses is the sum of their individual values. Since every house contributes independently, replacing a chosen house with a larger unchosen house can never decrease the answer. After sorting, the first k houses are at least as valuable as every house outside that group, so no other selection can produce a larger total.

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

The dictionary stores the exchange value of every candy name. Since house descriptions use names rather than numeric identifiers, a dictionary avoids repeatedly searching through the list of candy types.

While reading a house, the code immediately converts all candy information into a single total value. This prevents unnecessary storage of individual candy lists because only the final contribution of each house matters.

The descending sort places the most valuable houses at the beginning. Taking `houses[:k]` selects exactly the number of houses Timmy can visit. Python integers handle the possible total safely, so no manual overflow handling is needed.

The only subtle boundary condition is that k can equal h. In that case the slice simply contains the entire list, which matches the requirement that Timmy visits every house.

## Worked Examples

Sample 1:

Input:

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

The algorithm evaluates each house independently.

| Step | House processed | House value | Sorted values |
| --- | --- | --- | --- |
| 1 | LactoseyWay and Twicks | 2 * 3 + 3 * 1 = 9 | [9] |
| 2 | DigDog | 5 * 2 = 10 | [10, 9] |
| 3 | Choose k = 1 | 10 | [10, 9] |

The most profitable house gives two DigDog candies. Each is worth five Chuckles bars, so the answer is 10. This trace demonstrates why only the largest house values matter.

Sample 2:

Input:

```
2
CandyA 4
CandyB 7
3 2
1
CandyA 5
2
CandyB 2
CandyA 1
1
CandyB 3
```

| Step | House processed | House value | Sorted values |
| --- | --- | --- | --- |
| 1 | House 1 | 4 * 5 = 20 | [20] |
| 2 | House 2 | 7 * 2 + 4 * 1 = 18 | [20, 18] |
| 3 | House 3 | 7 * 3 = 21 | [21, 20, 18] |
| 4 | Choose k = 2 | 21 + 20 = 41 | [21, 20, 18] |

The selected houses are the third and first houses. This shows that the input order has no meaning, and the algorithm must compare all houses before choosing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total candy entries + h log h) | Each candy entry is processed once, then the h house values are sorted. |
| Space | O(n + h) | The candy values and computed house values are stored. |

The maximum input sizes are small enough that sorting 200 house values is trivial. The dominant work is reading and converting candy information, so the solution easily fits within the given limits.

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
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

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
Candy 10
3 1
1
Candy 5
1
Candy 2
1
Candy 8
""") == "50\n", "single best house"

assert run("""1
Candy 4
2 2
1
Candy 3
1
Candy 3
""") == "24\n", "equal houses"

assert run("""2
A 1
B 100
2 2
1
A 100
1
B 1
""") == "200\n", "visit all houses"

assert run("""3
A 5
B 6
C 7
4 2
1
A 1
1
B 1
1
C 1
3
A 10
B 10
C 10
""") == "390\n", "large individual house value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 10 | Basic house selection |
| Single best house case | 50 | k = 1 boundary |
| Equal houses | 24 | Duplicate values must be kept |
| Visit all houses | 200 | k = h handling |
| Large individual house value | 390 | Correct multiplication and summation |

## Edge Cases

The first edge case is choosing exactly one house. For the input:

```
1
Candy 10
3 1
1
Candy 5
1
Candy 2
1
Candy 8
```

the computed house values are 50, 20, and 80. Sorting gives 80, 50, 20, and selecting one house returns 80. The algorithm never depends on the input order, so the highest value is selected correctly.

The second edge case is multiple identical house values. For:

```
1
Candy 4
2 2
1
Candy 3
1
Candy 3
```

each house has value 12. The sorted list is [12, 12], and taking both houses gives 24. The algorithm keeps duplicate values because a house is a separate choice, not just a unique number.

The final edge case is when every house must be visited. If k equals h, the sorted prefix contains all houses. Sorting changes nothing about the sum, and the algorithm returns the total value of every house, which matches the required behavior.
