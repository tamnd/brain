---
title: "CF 106050N - Name of the Marathon?"
description: "The problem asks us to count votes for the name of a programming marathon. Each vote is either 1, meaning the first proposed name, or 2, meaning the second proposed name. After counting the votes, we print the name that received more votes."
date: "2026-06-25T12:29:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106050
codeforces_index: "N"
codeforces_contest_name: "Cataratas do Pinh\u00e3o 2025"
rating: 0
weight: 106050
solve_time_s: 31
verified: true
draft: false
---

[CF 106050N - Name of the Marathon?](https://codeforces.com/problemset/problem/106050/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to count votes for the name of a programming marathon. Each vote is either `1`, meaning the first proposed name, or `2`, meaning the second proposed name. After counting the votes, we print the name that received more votes. If both names receive the same number of votes, the result is undecided and we print the special tie message. The input consists of the number of votes followed by the individual votes, and the output is the winning name or the tie message.

The number of votes can reach $10^5$, so the algorithm needs to comfortably process one hundred thousand values. This immediately rules out approaches that repeatedly scan the whole vote list for every vote or simulate unnecessary work, because those can grow to $O(N^2)$, which would mean around $10^{10}$ operations at the maximum size. A single pass through the votes is more than enough, since the only information we need is how many votes each option received.

The tricky cases are mostly about comparison logic. A common mistake is forgetting that a tie is a separate outcome. For example, with:

```
6
1 1 1 2 2 2
```

the correct output is:

```
Cascatiba?
```

A careless solution that uses `>=` when checking the first candidate could incorrectly print the first name, even though both candidates have exactly the same support.

Another edge case is when the winning margin is only one vote. For example:

```
7
1 1 1 1 2 2 2
```

the correct output is:

```
Cataratas do Pinhao
```

The counts are four votes for option `1` and three votes for option `2`. Code that only checks whether one value appears "more often" using the wrong threshold could incorrectly treat close results as ties.

The smallest valid input also deserves attention. For:

```
11
2 2 2 2 2 2 1 1 1 1 1
```

the correct output is:

```
Pinhao das Cataratas
```

The algorithm should not depend on a specific balance of votes or assume that one candidate appears first in the input.

## Approaches

The straightforward solution is to inspect every vote and count the two possible choices. A brute-force interpretation might try to determine the winner by comparing every vote with every other vote, but that is unnecessary. Such a method would perform roughly $N^2$ comparisons in the worst case, which becomes about $10^{10}$ operations for $N = 10^5$. It is correct because it eventually discovers the frequency of each choice, but it wastes the structure of the problem.

The key observation is that every vote contributes only one piece of information: one candidate's total increases by one. We never need to know the positions of the votes or how they are distributed. The entire problem reduces to maintaining two counters while reading the array. This turns the solution into a single linear scan.

After counting, the decision is constant time. If the first counter is larger, the first name wins. If the second counter is larger, the second name wins. Otherwise, the counters are equal and the tie message is printed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Counting votes | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of votes and initialize two counters, one for each possible vote value. The counters represent the current score of each marathon name.
2. Process each vote once. If the vote is `1`, increase the counter for the first name. If it is `2`, increase the counter for the second name. Each vote is handled immediately because future votes do not affect the meaning of previous ones.
3. Compare the two counters after all votes have been processed. The larger counter identifies the winner because the vote totals are exactly what the problem asks us to maximize.
4. If the two counters are equal, output the tie message because neither option has more votes than the other.

Why it works: during the scan, the counters always store the exact number of votes seen so far for each candidate. When the scan finishes, every vote has been included exactly once, so both counters equal the final totals. Comparing these totals directly gives the correct result.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
votes = list(map(int, input().split()))

first = 0
second = 0

for vote in votes:
    if vote == 1:
        first += 1
    else:
        second += 1

if first > second:
    print("Cataratas do Pinhao")
elif second > first:
    print("Pinhao das Cataratas")
else:
    print("Cascatiba?")
```

The implementation keeps only two integer variables, which directly match the mathematical state needed by the solution. Reading all votes at once is simple and efficient for $10^5$ values, and the loop performs exactly one operation per vote.

The comparison uses strict inequalities first. This matters because the equal case must only happen when neither side has a greater count. Using `>=` would accidentally classify ties as wins.

The solution does not need arrays, sorting, or extra memory. The order of the votes is irrelevant, so storing them is only a convenience for parsing.

## Worked Examples

### Sample 1

Input:

```
12
1 1 1 1 1 1 2 2 2 2 2 2
```

| Step | Vote | First count | Second count |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 2 | 1 | 2 | 0 |
| 3 | 1 | 3 | 0 |
| 4 | 1 | 4 | 0 |
| 5 | 1 | 5 | 0 |
| 6 | 1 | 6 | 0 |
| 7 | 2 | 6 | 1 |
| 8 | 2 | 6 | 2 |
| 9 | 2 | 6 | 3 |
| 10 | 2 | 6 | 4 |
| 11 | 2 | 6 | 5 |
| 12 | 2 | 6 | 6 |

The final counts are equal, so the algorithm reaches the tie branch and prints the undecided result.

### Sample 2

Input:

```
12
1 1 1 1 1 1 1 2 2 2 2 2
```

| Step | Vote | First count | Second count |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 2 | 1 | 2 | 0 |
| 3 | 1 | 3 | 0 |
| 4 | 1 | 4 | 0 |
| 5 | 1 | 5 | 0 |
| 6 | 1 | 6 | 0 |
| 7 | 1 | 7 | 0 |
| 8 | 2 | 7 | 1 |
| 9 | 2 | 7 | 2 |
| 10 | 2 | 7 | 3 |
| 11 | 2 | 7 | 4 |
| 12 | 2 | 7 | 5 |

The first name has seven votes while the second has five, so the first candidate is printed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every vote is read and counted exactly once |
| Space | O(1) | Only two counters are stored |

The maximum input size is $10^5$, and the algorithm performs only a constant amount of work per vote. This easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(data):
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)

    input = sys.stdin.readline
    n = int(input())
    votes = list(map(int, input().split()))

    first = 0
    second = 0

    for vote in votes:
        if vote == 1:
            first += 1
        else:
            second += 1

    if first > second:
        ans = "Cataratas do Pinhao"
    elif second > first:
        ans = "Pinhao das Cataratas"
    else:
        ans = "Cascatiba?"

    sys.stdin = old_stdin
    return ans

# provided samples
assert solve("""12
1 1 1 1 1 1 2 2 2 2 2 2
""") == "Cascatiba?", "sample 1"

assert solve("""12
1 1 1 1 1 1 1 2 2 2 2 2
""") == "Cataratas do Pinhao", "sample 2"

# custom cases
assert solve("""11
2 2 2 2 2 2 1 1 1 1 1
""") == "Pinhao das Cataratas", "minimum size"

assert solve("""11
1 2 1 2 1 2 1 2 1 2 1
""") == "Cataratas do Pinhao", "boundary one vote difference"

assert solve("""100000
""" + " ".join(["1"] * 100000) + "\n") == "Cataratas do Pinhao", "large input"

assert solve("""11
1 1 1 1 1 1 2 2 2 2 2
""") == "Cascatiba?", "tie case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 11 votes with six `2`s and five `1`s | Pinhao das Cataratas | Smallest valid input and second candidate win |
| Alternating votes with one extra `1` | Cataratas do Pinhao | Off-by-one comparison handling |
| 100000 votes all equal to `1` | Cataratas do Pinhao | Maximum input size and linear processing |
| Six `1`s and five `2`s | Cataratas do Pinhao | Close non-tie result |

## Edge Cases

For the tie case:

```
6
1 1 1 2 2 2
```

the algorithm increments the first counter three times and the second counter three times. The final comparison sees equal values and selects the tie branch. This avoids the common mistake of treating equality as a victory for the first option.

For a one-vote difference:

```
7
1 1 1 1 2 2 2
```

the counters finish at four and three. Since the first value is strictly larger, the first name is printed. The algorithm does not need any special handling for close scores because all decisions are based on the final totals.

For a large repeated input:

```
11
1 1 1 1 1 1 1 1 1 1 1
```

the loop simply increments the first counter for every element. The solution remains efficient because it never creates extra structures or performs repeated searches.
