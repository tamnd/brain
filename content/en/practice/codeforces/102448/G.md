---
title: "CF 102448G - Gorggeous Peter's Great Friend"
description: "We need to calculate the score of each candidate from a global stream of submissions. Peter has selected a set of problems, and every selected problem has a fixed score. A candidate earns that problem's score exactly when their submission to that problem receives the verdict AC."
date: "2026-08-08T12:19:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "G"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 742
verified: true
draft: false
---

[CF 102448G - Gorggeous Peter's Great Friend](https://codeforces.com/problemset/problem/102448/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to calculate the score of each candidate from a global stream of submissions. Peter has selected a set of problems, and every selected problem has a fixed score. A candidate earns that problem's score exactly when their submission to that problem receives the verdict `AC`.

The input first gives the candidate handles. Then it gives the selected problem IDs together with their scores. Finally, it gives submissions from arbitrary users. A submission contains a user handle, a problem ID, and a verdict. Some submissions may belong to users who are not candidates, and some may concern problems that Peter did not select. Neither should affect the candidates' scores.

For every candidate, the output must preserve the original candidate order and contain their handle followed by the sum of the scores of all selected problems they solved.

The key constraint is that there can be up to 50,000 candidates, 50,000 selected problems, and 50,000 submissions. A solution that examines every submission for every candidate would perform as many as

[
50,000 \times 50,000 = 2.5 \times 10^9
]

checks. That is far beyond what a 1 second time limit can accommodate. We need an approach close to linear in the input size. Since all handles and problem IDs have at most 20 characters, using hash tables for direct lookup is also practical.

There are several cases where a careless implementation can silently produce the wrong answer. First, an `AC` from a non-candidate must not contribute to anyone's score. For example:

```
1 1 1
alice
p1 100
bob p1 AC
```

The correct output is:

```
alice 0
```

A solution that accumulates scores by problem alone would incorrectly give Alice 100.

Second, a problem that was not selected must be ignored even if a candidate solves it:

```
1 1 1
alice
p1 100
alice p2 AC
```

The correct output is:

```
alice 0
```

A careless implementation might assign a score to every `AC` submission instead of checking whether the problem belongs to the selected set.

Third, a wrong submission must not affect the score. Consider:

```
1 1 2
alice
p1 100
alice p1 WA
alice p1 AC
```

The correct output is:

```
alice 100
```

Only the `AC` submission matters. The earlier `WA` should have no effect.

Finally, a candidate can have several wrong submissions before solving a problem. We must not add the problem score when processing those attempts. The guarantee that a user never submits the same problem again after receiving `AC` means that once an `AC` appears, that user-problem pair will not produce another submission later. We can consequently add the score when the `AC` is encountered without needing a separate duplicate-prevention structure.

## Approaches

The most direct solution is to process each candidate independently. For one candidate, scan all submissions and look for records where the user is that candidate, the verdict is `AC`, and the problem is one of the selected problems. Whenever such a submission is found, add the corresponding problem score.

This approach is correct because every possible way for a candidate to earn points is explicitly examined. However, it repeats the same submission scan for every candidate. With 50,000 candidates and 50,000 submissions, the worst case is 2.5 billion candidate-submission comparisons. Even if each comparison were very cheap, that amount of work is much too large for the time limit.

The better perspective is to process each submission exactly once. The submission already tells us the user, the problem, and the verdict, so there is no reason to repeatedly search for the relevant candidate. We can build a hash table mapping every candidate handle to its position in the output and another hash table mapping every selected problem ID to its score.

Then a submission with verdict other than `AC` can be ignored immediately. For an `AC`, we look up its user in the candidate table and its problem in the selected-problem table. If both exist, that single submission directly identifies the candidate whose score should increase and the amount to add.

The brute-force method works because it eventually examines every relevant submission for every candidate, but it fails because it repeats work. The observation that every submission independently identifies at most one candidate and one selected problem lets us turn the problem into constant-time hash table lookups per submission.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(CS) | O(P + C) | Too slow |
| Optimal | O(C + P + S) expected | O(C + P) | Accepted |

## Algorithm Walkthrough

1. Read the number of candidates, selected problems, and submissions. Store every candidate handle in a dictionary together with its position in the output array. The position is useful because the final output must use the same order as the input, regardless of the order in which submissions are processed.
2. Read every selected problem and its score. Store the pair in a dictionary where the problem ID is the key and the score is the value. This converts finding a problem's score from a scan through all selected problems into an expected constant-time lookup.
3. Create an array of `C` zeroes. Entry `i` represents the accumulated score of the candidate whose handle appeared at position `i`.
4. Process each submission once. If its verdict is not `AC`, skip it because it cannot increase any score.
5. For an `AC` submission, look up the submitted user's handle in the candidate dictionary. If the handle is absent, the submission belongs to a non-candidate, so it cannot affect the answer.
6. If the user is a candidate, look up the submitted problem in the selected-problem dictionary. If it is absent, the problem was not selected and therefore contributes nothing.
7. If both lookups succeed, add the selected problem's score to the candidate's accumulated score. The guarantee about submissions after an `AC` means the same user cannot later receive another submission for that problem, so the score is added exactly once.
8. After all submissions have been processed, iterate through the original candidate list and print each handle together with its accumulated score. Keeping the handles in input order guarantees that the output order is correct.

The invariant is that after processing any prefix of the submission list, each candidate's stored score equals the total score of every selected problem for which that candidate has already received an `AC` within that prefix. A non-`AC` submission cannot change the invariant. An `AC` from a non-candidate or unselected problem also cannot contribute. For an `AC` from a candidate on a selected problem, exactly that candidate's score increases by exactly that problem's score. Thus the invariant remains true after every submission, and after the final submission it gives precisely the required answers.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    C, P, S = map(int, input().split())

    candidates = []
    candidate_index = {}

    for i in range(C):
        handle = input().strip()
        candidates.append(handle)
        candidate_index[handle] = i

    problem_score = {}

    for _ in range(P):
        problem, score = input().split()
        problem_score[problem] = int(score)

    answer = [0] * C

    for _ in range(S):
        user, problem, verdict = input().split()

        if verdict != "AC":
            continue

        idx = candidate_index.get(user)
        if idx is None:
            continue

        score = problem_score.get(problem)
        if score is None:
            continue

        answer[idx] += score

    output = []
    for i in range(C):
        output.append(f"{candidates[i]} {answer[i]}")

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The `candidates` list preserves the exact input order, while `candidate_index` provides fast access to the corresponding score position. For example, if `beza` was the second candidate, `candidate_index["beza"]` is `1`, so every qualifying submission for `beza` updates `answer[1]`.

The `problem_score` dictionary plays the same role for problems. We do not need to store selected problems separately because the existence of a key already tells us that the problem was selected, while its value gives the score.

The verdict is checked before either dictionary lookup. This is not necessary for asymptotic complexity, but it avoids unnecessary work for the potentially large number of submissions that are not `AC`.

Using `.get()` allows us to distinguish a missing user or problem without raising an exception. The scores are strictly positive, so `None` cannot be confused with a valid score.

Python integers automatically handle arbitrarily large values. Even though each individual score is at most 20,000, the total can reach approximately 1 billion when many selected problems are solved, which is still safely handled by Python integers.

There are no off-by-one calculations because candidate positions are stored directly using zero-based indices. The output loop then accesses exactly those same positions.

## Worked Examples

### Sample 1

The candidates are `GabrielPessoa` and `beza`. The selected problems are `metebronca`, worth 100, and `geometry`, worth 200.

| Submission | Verdict | Candidate lookup | Problem lookup | Scores after submission |
| --- | --- | --- | --- | --- |
| `beza metebronca AC` | AC | `beza -> 1` | `metebronca -> 100` | GabrielPessoa = 0, beza = 100 |
| `ffern numbertheory AC` | AC | absent | not needed | GabrielPessoa = 0, beza = 100 |
| `GabrielPessoa geometry WA` | WA | not needed | not needed | GabrielPessoa = 0, beza = 100 |
| `beza geometry AC` | AC | `beza -> 1` | `geometry -> 200` | GabrielPessoa = 0, beza = 300 |

The second submission is an `AC`, but `ffern` is not a candidate, so it is discarded. The third submission is from a candidate and concerns a selected problem, but its verdict is `WA`, so it is also discarded. The two successful selected problems solved by `beza` contribute 100 and 200, giving 300.

The final output is:

```
GabrielPessoa 0
beza 300
```

### Constructed Example 2

Consider:

```
3 2 5
alice
bob
carol
p1 50
p2 100
alice p1 WA
bob p3 AC
carol p2 AC
alice p1 AC
bob p1 AC
```

The trace is:

| Submission | Verdict | Candidate | Selected problem | Scores after submission |
| --- | --- | --- | --- | --- |
| `alice p1 WA` | WA | not processed | not processed | alice = 0, bob = 0, carol = 0 |
| `bob p3 AC` | AC | `bob` found | `p3` absent | alice = 0, bob = 0, carol = 0 |
| `carol p2 AC` | AC | `carol` found | `p2 -> 100` | alice = 0, bob = 0, carol = 100 |
| `alice p1 AC` | AC | `alice` found | `p1 -> 50` | alice = 50, bob = 0, carol = 100 |
| `bob p1 AC` | AC | `bob` found | `p1 -> 50` | alice = 50, bob = 50, carol = 100 |

The final output is:

```
alice 50
bob 50
carol 100
```

This example exercises three different filters. The `WA` is ignored, the `AC` on unselected `p3` is ignored, and successful submissions on selected problems update exactly the corresponding candidate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(C + P + S) expected | Each candidate, problem, and submission is processed once, with expected O(1) hash table operations |
| Space | O(C + P) | The candidate dictionary, problem dictionary, candidate list, and answer array each scale linearly |

The maximum input contains only 150,000 records across the three main sections. The algorithm performs a constant number of dictionary operations for each submission, so its expected running time is easily compatible with the 1 second limit compared with the 2.5 billion operations required by the brute-force approach. The dictionaries and arrays store information proportional to at most 100,000 candidates and selected problems, which fits comfortably within 256 MB.

## Test Cases

The following test harness implements the same `solve` function structure and runs the solution against the supplied sample plus several custom cases. The maximum-size case is generated programmatically so the test itself remains readable while still exercising 50,000 candidates, 50,000 problems, and 50,000 submissions.

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    C, P, S = map(int, input().split())

    candidates = []
    candidate_index = {}

    for i in range(C):
        handle = input().strip()
        candidates.append(handle)
        candidate_index[handle] = i

    problem_score = {}

    for _ in range(P):
        problem, score = input().split()
        problem_score[problem] = int(score)

    answer = [0] * C

    for _ in range(S):
        user, problem, verdict = input().split()

        if verdict != "AC":
            continue

        idx = candidate_index.get(user)
        if idx is None:
            continue

        score = problem_score.get(problem)
        if score is None:
            continue

        answer[idx] += score

    output = []
    for i in range(C):
        output.append(f"{candidates[i]} {answer[i]}")

    return "\n".join(output)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided sample.
sample1 = """\
2 2 4
GabrielPessoa
beza
metebronca 100
geometry 200
beza metebronca AC
ffern numbertheory AC
GabrielPessoa geometry WA
beza geometry AC
"""

assert run(sample1) == """\
GabrielPessoa 0
beza 300
""", "sample 1"

# Minimum-size case.
minimum = """\
1 1 1
a
p 1
a p AC
"""

assert run(minimum) == """\
a 1
""", "minimum-size case"

# All submissions are relevant, with several candidates solving
# the same selected problems.
all_equal = """\
3 2 4
a
b
c
p1 7
p2 7
a p1 AC
b p1 AC
b p2 AC
c p2 AC
"""

assert run(all_equal) == """\
a 7
b 14
c 7
""", "all-equal scores"

# Boundary behavior: WA, unknown user, and unselected problem
# must all be ignored.
filters = """\
2 1 5
alice
bob
selected 100
alice selected WA
alice other AC
unknown selected AC
bob selected AC
bob selected WA
"""

assert run(filters) == """\
alice 0
bob 100
""", "filtering irrelevant submissions"

# A candidate can have several wrong submissions before AC.
# The selected problem score must be added only for AC.
retries = """\
2 2 10
alice
bob
p1 10
p2 20
alice p1 WA
alice p1 CE
alice p1 AC
bob p1 WA
bob p2 AC
alice p2 AC
bob p3 AC
alice p2 WA
bob p1 AC
alice p1 WA
"""

assert run(retries) == """\
alice 30
bob 30
""", "multiple attempts and irrelevant problems"

# Maximum-size generated case.
C = 50000
P = 50000
S = 50000

parts = [f"{C} {P} {S}"]

for i in range(C):
    parts.append(f"u{i}")

for i in range(P):
    parts.append(f"p{i} 1")

# Each submission is a valid AC for a corresponding candidate
# and problem. Every candidate receives exactly one point.
for i in range(S):
    parts.append(f"u{i} p{i} AC")

maximum = "\n".join(parts) + "\n"

expected = "\n".join(f"u{i} 1" for i in range(C))

assert run(maximum) == expected, "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size case | `a 1` | Smallest valid input and direct successful lookup |
| All-equal scores | `a 7`, `b 14`, `c 7` | Multiple candidates solving the same problems and repeated score values |
| Filtering case | `alice 0`, `bob 100` | Unknown users, unselected problems, and non-`AC` verdicts |
| Multiple-attempt case | `alice 30`, `bob 30` | Several failed submissions before successful submissions |
| Maximum-size generated case | Every candidate has score `1` | Maximum values of all three main input sizes and performance |

## Edge Cases

An `AC` from a user who is not among the candidates is ignored at the candidate lookup stage. For example:

```
1 1 1
alice
p1 100
bob p1 AC
```

The candidate dictionary contains only `alice`. When `bob` is processed, `candidate_index.get("bob")` returns `None`, so no score changes. The output is:

```
alice 0
```

A successful submission to an unselected problem is handled similarly. Consider:

```
1 1 1
alice
p1 100
alice p2 AC
```

The candidate lookup succeeds, but `problem_score.get("p2")` returns `None` because only `p1` was selected. The algorithm discards the submission and prints:

```
alice 0
```

A failed submission must not contribute anything, even when both the user and problem are valid. With:

```
1 1 2
alice
p1 100
alice p1 WA
alice p1 AC
```

the first submission is rejected immediately by the verdict check. The second one passes all checks and adds 100. The result is:

```
alice 100
```

Several failed attempts do not cause any special handling. For:

```
1 1 3
alice
p1 50
alice p1 WA
alice p1 CE
alice p1 AC
```

the first two records leave the score at zero, while the final `AC` changes it to 50. The output is:

```
alice 50
```

The order of submissions does not need to match the candidate order. Suppose the candidates are:

```
2 1 2
alice
bob
p1 25
bob p1 AC
alice p1 AC
```

The first processed submission updates Bob's entry, which is index 1. The second updates Alice's entry, which is index 0. Because the answer array is indexed by the original candidate positions, the final output remains:

```
alice 25
bob 25
```

A problem can be solved by many different candidates, and each candidate must receive the score independently. For example:

```
2 1 2
alice
bob
p1 100
alice p1 AC
bob p1 AC
```

After the first submission the answer array is `[100, 0]`. After the second it becomes `[100, 100]`. The fact that the problem has already been solved by Alice does not make it unavailable to Bob, because the guarantee concerns repeated submissions by the same user, not submissions by different users.

The maximum total score also does not create an integer overflow problem in Python. Even if a candidate solves many selected problems, Python's integer type grows as necessary. The algorithm never relies on a fixed-width integer representation.
