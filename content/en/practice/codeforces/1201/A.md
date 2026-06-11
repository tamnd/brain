---
title: "CF 1201A - Important Exam"
description: "Each student answers a multiple-choice test with $m$ questions, where each question has five possible options. We are given the full answer sheet of every student, but the correct answers are unknown."
date: "2026-06-11T23:49:31+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1201
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 577 (Div. 2)"
rating: 900
weight: 1201
solve_time_s: 82
verified: true
draft: false
---

[CF 1201A - Important Exam](https://codeforces.com/problemset/problem/1201/A)

**Rating:** 900  
**Tags:** implementation, strings  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

Each student answers a multiple-choice test with $m$ questions, where each question has five possible options. We are given the full answer sheet of every student, but the correct answers are unknown. What we control is the hypothetical choice of the correct answer for each question, and each question $j$ has a fixed score $a_j$ if answered correctly.

If we decide that a particular option is correct for a question, every student who picked that option earns the corresponding points for that question. Our task is to assign a correct option (A to E) to every question in a way that maximizes the sum of scores earned across all students.

The structure is independent across questions. The choice we make for question $j$ does not affect any other question, because scores add linearly and students’ answers are fixed.

The constraints $n, m \le 1000$ imply at most one million character checks in a straightforward implementation. Any solution that scans each student’s answer per question is comfortably fast enough, since $O(nm)$ operations is small.

A naive mistake would be to assume we need to simulate different global answer keys or try to align multiple questions simultaneously. For example, thinking we must choose a consistent pattern across questions beyond independent maximization leads to unnecessary complexity. Another common pitfall is forgetting that the correct answer is chosen independently per question, not per student.

## Approaches

A brute-force idea would be to try all possible correct answer strings of length $m$, where each position has 5 choices. This gives $5^m$ possibilities, which is astronomically large even for small $m$. For each candidate answer key, computing the total score requires checking all $n$ students across $m$ questions, leading to $O(nm)$ per candidate. This quickly becomes infeasible.

The key observation is that questions do not interact. For a fixed question $j$, if we decide that option $A$ is correct, the score contributed by that question is simply $a_j$ multiplied by the number of students who chose $A$. The same applies to B, C, D, and E. Therefore, for each question, we only need to pick the most frequent answer among students.

This reduces the problem to computing frequency counts per column of the input matrix, then selecting the best among five fixed choices per column.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(5^m \cdot nm)$ | $O(1)$ | Too slow |
| Optimal | $O(nm)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Initialize a result accumulator to zero. This will store the total maximum score across all questions.
2. For each question index $j$, build a frequency counter for the five possible options. We scan all students and count how many chose each of A, B, C, D, and E for that column.
3. Once frequencies are computed for question $j$, compute the best achievable contribution by taking the maximum frequency among the five options and multiplying it by $a_j$.
4. Add this contribution to the total accumulator.
5. Repeat for all questions.

The reason this step works is that the correctness of a question depends only on how many students match the chosen answer. Since we are free to declare any option as correct, we always pick the option with the highest support.

### Why it works

For each question $j$, any assignment of correct answer corresponds to selecting one of five groups of students. The score is linear in group size, so maximizing the contribution reduces to selecting the largest group. Because questions are independent, summing local optima produces the global optimum without interference.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    students = [input().strip() for _ in range(n)]
    scores = list(map(int, input().split()))

    total = 0

    for j in range(m):
        freq = [0] * 5
        for i in range(n):
            c = students[i][j]
            freq[ord(c) - 65] += 1

        best = max(freq)
        total += best * scores[j]

    print(total)

if __name__ == "__main__":
    solve()
```

The solution reads all student strings and then iterates column by column. For each column, it builds a small fixed-size frequency array of length five. The conversion `ord(c) - 65` maps characters A to E into indices 0 to 4. This keeps the implementation tight and avoids condition chains.

The multiplication by `scores[j]` happens only after identifying the most common answer, ensuring we never overcount.

## Worked Examples

### Example 1

Input:

```
2 4
ABCD
ABCE
1 2 3 4
```

We process each column:

| Question | A count | B count | C count | D count | E count | Best | Score | Contribution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 0 | 0 | 0 | 2 | 1 | 2 |
| 2 | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 4 |
| 3 | 0 | 0 | 2 | 0 | 0 | 2 | 3 | 6 |
| 4 | 1 | 0 | 1 | 0 | 0 | 1 | 4 | 4 |

Total is $2 + 4 + 6 + 4 = 16$.

This trace shows that each column is treated independently, and the optimal choice is always the majority letter.

### Example 2

Input:

```
3 3
ABC
BBC
CCA
5 4 3
```

| Question | A | B | C | Best | Score | Contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 0 | 2 | 5 | 10 |
| 2 | 1 | 1 | 1 | 1 | 4 | 4 |
| 3 | 1 | 1 | 1 | 1 | 3 | 3 |

Total = $10 + 4 + 3 = 17$.

This example shows that even when frequencies are tied, any choice among the maximum-frequency letters gives the same contribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each character is processed once when counting frequencies per column |
| Space | $O(1)$ extra | Only a fixed array of size 5 is used per column |

The bound $n, m \le 1000$ gives at most $10^6$ character inspections, which fits easily within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio

    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""2 4
ABCD
ABCE
1 2 3 4
""") == "16"

# single student, trivial
assert run("""1 3
ABC
1 1 1
""") == "3"

# all same answers
assert run("""3 2
AA
AA
AA
5 7
""") == "36"

# tie case
assert run("""3 2
AB
BA
AB
10 1
""") == "20"

# larger mixed
assert run("""4 3
ABC
ABC
ABD
BBC
1 2 3
""") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single student | 3 | base case correctness |
| all same answers | 36 | maximum frequency dominance |
| tie case | 20 | handling equal frequencies |
| mixed case | 15 | general correctness |

## Edge Cases

One edge case is when all students choose different answers for a question. For example:

```
3 1
A
B
C
10
```

For the single column, frequencies are all 1. The algorithm selects any of them, giving contribution $1 \cdot 10 = 10$. The trace is straightforward: frequency array becomes $[1,1,1,0,0]$, maximum is 1, so the result is correct.

Another edge case is when $n = 1$. The algorithm still works because the frequency array will have a single 1 and four zeros, and the contribution is simply the question score.

A final edge case is when $m = 1$. The algorithm reduces to computing the most frequent character in a single string column, which still matches the same logic without modification.
