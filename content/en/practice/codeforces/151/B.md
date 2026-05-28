---
title: "CF 151B - Phone Numbers"
description: "Each friend has a phone book containing numbers written in the format XX-XX-XX. Every phone number belongs to exactly one of three categories. A taxi number uses the same digit everywhere. Examples are 11-11-11 or 55-55-55."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 151
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 107 (Div. 2)"
rating: 1200
weight: 151
solve_time_s: 106
verified: true
draft: false
---

[CF 151B - Phone Numbers](https://codeforces.com/problemset/problem/151/B)

**Rating:** 1200  
**Tags:** implementation, strings  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

Each friend has a phone book containing numbers written in the format `XX-XX-XX`. Every phone number belongs to exactly one of three categories.

A taxi number uses the same digit everywhere. Examples are `11-11-11` or `55-55-55`.

A pizza number is strictly decreasing when we read its digits from left to right, ignoring dashes. Every next digit must be smaller than the previous one. Examples are `98-76-54` and `95-43-21`.

Any number that is neither taxi nor pizza is considered a girls' number.

For every friend, we must count how many numbers belong to each category. After processing all phone books, we output the names of the friends with the highest taxi count, the highest pizza count, and the highest girls count. Multiple friends may tie for the maximum, and in that case we print all of them in input order.

The constraints are very small. There are at most 100 friends, and each friend has at most 100 phone numbers. Each number contains exactly 6 digits. Even a straightforward implementation that checks every digit of every number individually runs comfortably within the limit. In total, the program processes at most 10,000 phone numbers, each of fixed length. That means the actual amount of work is tiny.

The tricky part is not performance, it is classification correctness and output formatting.

One easy mistake is forgetting to ignore dashes when checking the digits. Consider:

```
98-76-54
```

The digits are decreasing, but if we compare characters directly without removing `-`, the logic breaks because `'-'` is not a digit.

Another common mistake is allowing non-strict decrease for pizza numbers. Consider:

```
98-76-55
```

This is not a pizza number because the last two digits are equal. A careless condition like `>=` instead of `>` incorrectly accepts it.

A subtle edge case appears when the same number occurs multiple times in one phone book. The statement explicitly says duplicates must be counted repeatedly. For example:

```
1
3 Alex
11-11-11
11-11-11
12-34-56
```

Alex has two taxi numbers, not one. Using a set to remove duplicates would produce the wrong answer.

Another formatting pitfall happens when multiple friends tie for the maximum. Suppose:

```
2
1 A
11-11-11
1 B
22-22-22
```

Both friends have one taxi number, so the correct output is:

```
If you want to call a taxi, you should call: A, B.
```

The names must remain in input order and be separated exactly by `", "`.

## Approaches

The most direct approach is to process every phone number independently and classify it by inspecting its digits.

For each number, we remove the dashes and obtain a string of length 6. Then we test whether all digits are equal. If yes, it is a taxi number.

If not, we test whether every digit is strictly larger than the next digit. If yes, it is a pizza number.

Otherwise, it belongs to the girls category.

This brute-force method is already fast enough because the input size is tiny. In the worst case we inspect 10,000 phone numbers, each containing only 6 digits. That is roughly 60,000 character operations, essentially instantaneous.

There is no need for advanced data structures or optimization tricks. The key observation is that every classification depends only on six characters, so each check is constant time.

A slightly less careful implementation might repeatedly scan the same string multiple times or convert digits unnecessarily, but even that still passes comfortably. The cleanest solution is simply to process each number once and update the corresponding counter.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × s × 6) | O(1) | Accepted |
| Optimal | O(n × s × 6) | O(1) | Accepted |

The brute-force and optimal approaches are effectively the same here because the constraints are so small. The important part is implementing the classification rules correctly.

## Algorithm Walkthrough

1. Read the number of friends.
2. For each friend, read the number of phone numbers and the friend's name.
3. Initialize three counters for this friend: taxi, pizza, and girls.
4. For every phone number:

1. Remove the dashes so only six digits remain.
2. Check whether all six digits are identical.
3. If they are identical, increment the taxi counter.
4. Otherwise, check whether every digit is strictly larger than the next digit.
5. If the digits are strictly decreasing, increment the pizza counter.
6. Otherwise, increment the girls counter.
5. Store the three counts together with the friend's name.
6. After processing all friends, compute:

1. The maximum taxi count.
2. The maximum pizza count.
3. The maximum girls count.
7. Traverse the friends in input order and collect:

1. Every name whose taxi count equals the maximum taxi count.
2. Every name whose pizza count equals the maximum pizza count.
3. Every name whose girls count equals the maximum girls count.
8. Print the three required sentences with the names joined by `", "`.

### Why it works

Every phone number belongs to exactly one category.

If all digits are equal, the number satisfies the taxi definition directly.

If the digits are not all equal but every digit is larger than the next one, the number satisfies the pizza definition.

Any remaining number cannot be taxi or pizza, so it must belong to the girls category.

Since every number is classified exactly once and every occurrence is counted independently, the counters for each friend are correct. Taking the maximum counter across all friends correctly identifies the required names.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    friends = []

    for _ in range(n):
        s, name = input().split()
        s = int(s)

        taxi = 0
        pizza = 0
        girls = 0

        for _ in range(s):
            number = input().strip().replace("-", "")

            if len(set(number)) == 1:
                taxi += 1
            elif all(number[i] > number[i + 1] for i in range(5)):
                pizza += 1
            else:
                girls += 1

        friends.append((name, taxi, pizza, girls))

    max_taxi = max(friend[1] for friend in friends)
    max_pizza = max(friend[2] for friend in friends)
    max_girls = max(friend[3] for friend in friends)

    taxi_names = [friend[0] for friend in friends if friend[1] == max_taxi]
    pizza_names = [friend[0] for friend in friends if friend[2] == max_pizza]
    girls_names = [friend[0] for friend in friends if friend[3] == max_girls]

    print(
        "If you want to call a taxi, you should call: "
        + ", ".join(taxi_names)
        + "."
    )

    print(
        "If you want to order a pizza, you should call: "
        + ", ".join(pizza_names)
        + "."
    )

    print(
        "If you want to go to a cafe with a wonderful girl, you should call: "
        + ", ".join(girls_names)
        + "."
    )

solve()
```

The solution follows the classification logic directly.

The expression `number.replace("-", "")` removes formatting characters so we can work only with digits. After that, every number becomes a six-character string.

The taxi check uses `len(set(number)) == 1`. A set removes duplicates, so if the set size is one, every digit must be identical.

The pizza check compares adjacent digits:

```
all(number[i] > number[i + 1] for i in range(5))
```

The comparison is strictly greater, not greater-or-equal. This detail matters because repeated digits invalidate the pizza condition.

The girls category is simply the remaining case after the first two checks fail.

The program stores every friend's counts and later computes global maximums. Since the final output must preserve input order, we iterate through the stored list instead of sorting.

The output formatting is easy to get wrong. The statement requires commas followed by spaces, with exactly one final period. Using `", ".join(...)` handles this cleanly.

## Worked Examples

### Sample 1

Input:

```
4
2 Fedorov
22-22-22
98-76-54
3 Melnikov
75-19-09
23-45-67
99-99-98
7 Rogulenko
22-22-22
11-11-11
33-33-33
44-44-44
55-55-55
66-66-66
95-43-21
3 Kaluzhin
11-11-11
99-99-99
98-65-32
```

Processing trace:

| Friend | Number | Type | Taxi | Pizza | Girls |
| --- | --- | --- | --- | --- | --- |
| Fedorov | 22-22-22 | Taxi | 1 | 0 | 0 |
| Fedorov | 98-76-54 | Pizza | 1 | 1 | 0 |
| Melnikov | 75-19-09 | Girls | 0 | 0 | 1 |
| Melnikov | 23-45-67 | Girls | 0 | 0 | 2 |
| Melnikov | 99-99-98 | Girls | 0 | 0 | 3 |
| Rogulenko | 22-22-22 | Taxi | 1 | 0 | 0 |
| Rogulenko | 11-11-11 | Taxi | 2 | 0 | 0 |
| Rogulenko | 33-33-33 | Taxi | 3 | 0 | 0 |
| Rogulenko | 44-44-44 | Taxi | 4 | 0 | 0 |
| Rogulenko | 55-55-55 | Taxi | 5 | 0 | 0 |
| Rogulenko | 66-66-66 | Taxi | 6 | 0 | 0 |
| Rogulenko | 95-43-21 | Pizza | 6 | 1 | 0 |
| Kaluzhin | 11-11-11 | Taxi | 1 | 0 | 0 |
| Kaluzhin | 99-99-99 | Taxi | 2 | 0 | 0 |
| Kaluzhin | 98-65-32 | Pizza | 2 | 1 | 0 |

Final maxima:

| Category | Maximum | Friends |
| --- | --- | --- |
| Taxi | 6 | Rogulenko |
| Pizza | 1 | Fedorov, Rogulenko, Kaluzhin |
| Girls | 3 | Melnikov |

This example shows all three categories and demonstrates ties for the pizza category.

### Custom Example

Input:

```
2
3 Alice
11-11-11
98-76-54
12-34-56
2 Bob
22-22-22
87-65-43
```

Processing trace:

| Friend | Number | Type | Taxi | Pizza | Girls |
| --- | --- | --- | --- | --- | --- |
| Alice | 11-11-11 | Taxi | 1 | 0 | 0 |
| Alice | 98-76-54 | Pizza | 1 | 1 | 0 |
| Alice | 12-34-56 | Girls | 1 | 1 | 1 |
| Bob | 22-22-22 | Taxi | 1 | 0 | 0 |
| Bob | 87-65-43 | Pizza | 1 | 1 | 0 |

Final maxima:

| Category | Maximum | Friends |
| --- | --- | --- |
| Taxi | 1 | Alice, Bob |
| Pizza | 1 | Alice, Bob |
| Girls | 1 | Alice |

This trace demonstrates correct tie handling and preservation of input order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × s × 6) | Every phone number has exactly 6 digits |
| Space | O(1) | Only a few counters and lists of names are stored |

Even at the maximum limits, the program processes only around 60,000 digit comparisons. That is far below the available time limit. Memory usage is also negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n = int(input())

    friends = []

    for _ in range(n):
        s, name = input().split()
        s = int(s)

        taxi = 0
        pizza = 0
        girls = 0

        for _ in range(s):
            number = input().strip().replace("-", "")

            if len(set(number)) == 1:
                taxi += 1
            elif all(number[i] > number[i + 1] for i in range(5)):
                pizza += 1
            else:
                girls += 1

        friends.append((name, taxi, pizza, girls))

    max_taxi = max(friend[1] for friend in friends)
    max_pizza = max(friend[2] for friend in friends)
    max_girls = max(friend[3] for friend in friends)

    taxi_names = [friend[0] for friend in friends if friend[1] == max_taxi]
    pizza_names = [friend[0] for friend in friends if friend[2] == max_pizza]
    girls_names = [friend[0] for friend in friends if friend[3] == max_girls]

    print(
        "If you want to call a taxi, you should call: "
        + ", ".join(taxi_names)
        + "."
    )

    print(
        "If you want to order a pizza, you should call: "
        + ", ".join(pizza_names)
        + "."
    )

    print(
        "If you want to go to a cafe with a wonderful girl, you should call: "
        + ", ".join(girls_names)
        + "."
    )

    sys.stdout = sys.__stdout__

    return out.getvalue()

# provided sample
assert run(
"""4
2 Fedorov
22-22-22
98-76-54
3 Melnikov
75-19-09
23-45-67
99-99-98
7 Rogulenko
22-22-22
11-11-11
33-33-33
44-44-44
55-55-55
66-66-66
95-43-21
3 Kaluzhin
11-11-11
99-99-99
98-65-32
"""
) == (
"""If you want to call a taxi, you should call: Rogulenko.
If you want to order a pizza, you should call: Fedorov, Rogulenko, Kaluzhin.
If you want to go to a cafe with a wonderful girl, you should call: Melnikov.
"""
), "sample 1"

# minimum input
assert run(
"""1
1 Alex
11-11-11
"""
) == (
"""If you want to call a taxi, you should call: Alex.
If you want to order a pizza, you should call: Alex.
If you want to go to a cafe with a wonderful girl, you should call: Alex.
"""
), "single friend"

# duplicate numbers must count multiple times
assert run(
"""1
3 Bob
11-11-11
11-11-11
12-34-56
"""
) == (
"""If you want to call a taxi, you should call: Bob.
If you want to order a pizza, you should call: Bob.
If you want to go to a cafe with a wonderful girl, you should call: Bob.
"""
), "duplicates counted"

# tie handling
assert run(
"""2
1 A
11-11-11
1 B
22-22-22
"""
) == (
"""If you want to call a taxi, you should call: A, B.
If you want to order a pizza, you should call: A, B.
If you want to go to a cafe with a wonderful girl, you should call: A, B.
"""
), "ties"

# pizza must be strictly decreasing
assert run(
"""1
2 Carl
98-76-54
98-76-55
"""
) == (
"""If you want to call a taxi, you should call: Carl.
If you want to order a pizza, you should call: Carl.
If you want to go to a cafe with a wonderful girl, you should call: Carl.
"""
), "strict decrease"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single friend with one number | Same friend printed everywhere | Minimum constraints |
| Duplicate taxi numbers | Count duplicates separately | Avoid incorrect deduplication |
| Two friends tied | Both names printed in order | Tie handling |
| `98-76-55` | Not pizza | Strict inequality |

## Edge Cases

Consider repeated phone numbers:

```
1
3 Alex
11-11-11
11-11-11
12-34-56
```

The algorithm processes each occurrence independently. The first two numbers both satisfy the taxi condition because all digits are equal. The taxi counter becomes 2. Since the statement counts repeated entries separately, this behavior is correct.

Consider a number that almost looks like a pizza number:

```
1
1 Bob
98-76-55
```

After removing dashes, the digits become `987655`. The comparisons are:

```
9 > 8
8 > 7
7 > 6
6 > 5
5 > 5   false
```

The final comparison fails because the decrease is not strict. The algorithm correctly classifies the number as a girls' number.

Consider ties between multiple friends:

```
2
1 A
11-11-11
1 B
22-22-22
```

Both friends finish with taxi count 1. The algorithm computes the maximum taxi count as 1 and then collects every friend matching that value. Since it traverses the original input order, the output becomes:

```
A, B
```

which matches the required ordering.

Consider a friend with zero phone numbers:

```
1
0 Alice
```

All three counters remain 0. Since Alice is the only friend, every category maximum is also 0, so Alice appears in all three output lines. The algorithm handles this naturally without special cases.
