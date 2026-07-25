---
title: "CF 102878A - IQ difference"
description: "The task is to find the single number in a list whose parity is different from all the others. The input describes a sequence of integers. Every value except one is either even or odd, while the remaining value has the opposite parity."
date: "2026-07-25T12:49:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "A"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 33
verified: true
draft: false
---

[CF 102878A - IQ difference](https://codeforces.com/problemset/problem/102878/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to find the single number in a list whose parity is different from all the others. The input describes a sequence of integers. Every value except one is either even or odd, while the remaining value has the opposite parity. The output is the 1-based position of that different value in the original sequence.

The size of the sequence is small, but the intended lesson is about recognizing what information actually matters. The values themselves are irrelevant except for whether they are divisible by two. A linear scan is enough because every element only needs to be inspected once. Even if the sequence size were increased to around $10^5$ or $10^6$, an $O(n)$ solution would still fit comfortably in normal competitive programming limits, while approaches that compare every pair would become impossible because they require $O(n^2)$ operations.

A common mistake is to assume that the first value determines the majority parity. For example, if the input is:

```
3
1 2 4
```

the correct output is:

```
1
```

The first number is odd and the other two are even. A method that initializes the answer based only on the first element can fail if it does not properly count or verify the majority.

Another edge case is when the unusual value appears at the end:

```
5
2 4 6 8 7
```

The correct output is:

```
5
```

A scan that stops too early after finding matching parity among the first few values will miss the answer.

A third case is when the first two numbers have different parity:

```
3
1 2 3
```

The correct output is:

```
2
```

Here the majority parity is odd, and the middle value is the only even one. Any approach that assumes the first two elements are representative needs an extra check.

## Approaches

The brute-force way is to compare every number with every other number and count how many values share its parity. Since there are $n$ choices for the candidate number and up to $n$ comparisons for each candidate, the total work is $O(n^2)$. This is correct because the unique element will be the only one whose parity count differs from the rest, but the repeated comparisons are unnecessary.

The observation that makes the problem simple is that parity has only two possible states. We do not need to compare elements against each other. We only need to know how many odd numbers and how many even numbers exist. Since exactly one element differs, one of these counts will be one and the other will be $n-1$. After identifying the minority parity, a single scan gives the position of the element with that parity.

The brute-force solution works because it directly checks the property we need, but it repeats the same parity checks many times. Counting the two possible parity groups compresses all that information into two counters, reducing the problem to a linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow for large inputs |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many numbers in the sequence are even and how many are odd. The majority count tells us which parity the normal numbers have, while the smaller count identifies the unusual parity.
2. Store the index of the last even number and the last odd number while scanning. Keeping these positions avoids needing another pass later.
3. Compare the counts of even and odd numbers. If there are fewer even numbers, the answer is the stored even position. Otherwise, the answer is the stored odd position.
4. Print the chosen position using 1-based indexing because the problem numbers positions starting from one.

Why it works: the input guarantees that exactly one number has a different parity. Therefore, the parity appearing once must be the answer's parity, and the other parity appears for every remaining element. The algorithm identifies this minority parity by counting, then returns the only index belonging to that group. Since every element is counted exactly once and every possible parity is considered, no other index can satisfy the condition.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    even_count = 0
    odd_count = 0
    even_pos = -1
    odd_pos = -1

    for i, x in enumerate(a, start=1):
        if x % 2 == 0:
            even_count += 1
            even_pos = i
        else:
            odd_count += 1
            odd_pos = i

    if even_count == 1:
        print(even_pos)
    else:
        print(odd_pos)

if __name__ == "__main__":
    solve()
```

The scan stores only four pieces of information: the number of even values, the number of odd values, and the most recent position of each type. The exact values are never needed after their parity is determined.

The condition `even_count == 1` selects the unusual group when the single different value is even. Otherwise, the single different value must be odd because the problem guarantees exactly one exception. The stored positions are already 1-based because the enumeration starts from one, which avoids an indexing correction at the end.

## Worked Examples

For the first example:

```
5
2 4 7 8 10
```

The scan behaves as follows.

| Index | Value | Even Count | Odd Count | Even Position | Odd Position |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 0 | 1 | -1 |
| 2 | 4 | 2 | 0 | 2 | -1 |
| 3 | 7 | 2 | 1 | 2 | 3 |
| 4 | 8 | 3 | 1 | 4 | 3 |
| 5 | 10 | 4 | 1 | 5 | 3 |

There is only one odd number, so the algorithm outputs position 3. This demonstrates that the values themselves do not matter, only their parity groups.

For the second example:

```
4
1 2 1 1
```

The scan behaves as follows.

| Index | Value | Even Count | Odd Count | Even Position | Odd Position |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | -1 | 1 |
| 2 | 2 | 1 | 1 | 2 | 1 |
| 3 | 1 | 1 | 2 | 2 | 3 |
| 4 | 1 | 1 | 3 | 2 | 4 |

There is only one even number, so the algorithm outputs position 2. This confirms that the same logic handles the opposite situation where the odd numbers form the majority.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every number is inspected once to count its parity. |
| Space | O(1) | Only counters and two positions are stored. |

The algorithm only performs a constant amount of work per element, so it scales linearly with the input size. The memory usage does not depend on the sequence length after the input has been read.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    even_count = 0
    odd_count = 0
    even_pos = -1
    odd_pos = -1

    for i, x in enumerate(a, start=1):
        if x % 2 == 0:
            even_count += 1
            even_pos = i
        else:
            odd_count += 1
            odd_pos = i

    ans = even_pos if even_count == 1 else odd_pos

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert solution("5\n2 4 7 8 10\n") == "3\n", "sample 1"
assert solution("4\n1 2 1 1\n") == "2\n", "sample 2"

assert solution("3\n2 4 1\n") == "3\n", "single odd value"
assert solution("3\n7 8 10\n") == "1\n", "single odd value at start"
assert solution("7\n6 2 4 8 12 14 3\n") == "7\n", "single odd value at end"
assert solution("5\n1 3 5 8 7\n") == "4\n", "single even value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 2 4 1` | `3` | The different parity appears at the end. |
| `3 / 7 8 10` | `1` | The different parity appears at the beginning. |
| `7 / 6 2 4 8 12 14 3` | `7` | A large majority group with a late exception. |
| `5 / 1 3 5 8 7` | `4` | The single even value case. |

## Edge Cases

For the case where the unusual number is the first element:

```
3
7 8 10
```

The algorithm counts two even numbers and one odd number. Since the even count is not one, it selects the stored odd position, which is 1. It correctly handles the fact that the first value does not establish the majority.

For the case where the unusual number is last:

```
5
2 4 6 8 7
```

The scan records four even values and one odd value. The stored odd position becomes 5, and the algorithm returns it after the full scan. It does not rely on early assumptions about the sequence.

For the case where the first two values have different parity:

```
3
1 2 3
```

The final counts are two odd values and one even value. The algorithm chooses the stored even position, which is 2. The majority is discovered from the complete count rather than from the first few elements, avoiding the common mistake of guessing too early.
