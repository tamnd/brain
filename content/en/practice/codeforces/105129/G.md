---
title: "CF 105129G - Bonus System"
description: "We are simulating a small training management system that keeps track of students and their accumulated bonus points. Each student has a fixed identity given by an index from 1 to n and an associated name. Initially, all students start with zero points."
date: "2026-06-27T19:21:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105129
codeforces_index: "G"
codeforces_contest_name: "Shorouk Academy 2024 Collegiate Programming Contest"
rating: 0
weight: 105129
solve_time_s: 45
verified: true
draft: false
---

[CF 105129G - Bonus System](https://codeforces.com/problemset/problem/105129/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a small training management system that keeps track of students and their accumulated bonus points. Each student has a fixed identity given by an index from 1 to n and an associated name. Initially, all students start with zero points.

After initialization, we process a sequence of commands. There are two kinds of commands. One command adds bonus points to a specific student, but only if a given password matches the system password exactly. The other command prints the current ranking of students based on their accumulated points.

The ranking rule is straightforward: students are sorted by total points in descending order, and if two students have the same number of points, the student with the smaller id appears first. When printing the scoreboard, we only display students who currently have non-zero points, and we assign ranks according to this sorted order. Equal scores share the same rank.

The constraints are small, with at most 100 students and 100 operations. This immediately suggests that an O(n log n) or even O(n²) approach per query is perfectly sufficient. The bottleneck is not algorithmic complexity but correct handling of ordering, ties, and filtering.

The main subtlety is that ranking is recomputed on demand from the current state, not maintained incrementally. Another subtle issue is that the password check must be exact and case-sensitive; even a small mismatch should reject the update.

Edge cases appear in how we compute ranks. If we naïvely assign ranks as 1, 2, 3 in sorted order, we will produce incorrect results when scores are equal. For example, if two students both have 10 points, they must share the same rank.

Another edge case is handling zero-point students. They must never appear in the scoreboard output even if they exist in the system.

Finally, the ordering tie-breaker by id is crucial. Without it, sorting becomes unstable and results may vary across implementations.

## Approaches

A direct approach is to maintain an array of size n storing each student's current score. For a bonus command, we check the password; if it matches, we update the score in constant time. The complexity bottleneck appears when we execute a scoreboard command: we must sort all students by score and id, then compute ranks and print the non-zero ones.

This brute-force strategy already fits comfortably. Sorting n ≤ 100 elements costs O(n log n), and even if we do it for every query, q ≤ 100, the total work is negligible.

The key observation is that there is no need for a complex data structure like a balanced tree or heap. The dataset is small enough that recomputing the ordering from scratch is simpler and less error-prone than maintaining it incrementally. Each scoreboard query is independent, so we can rebuild the sorted view on demand.

The only real design decision is how to assign ranks correctly. Once sorted, we scan the list and assign the same rank to equal scores, otherwise incrementing the rank counter appropriately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute sort each query) | O(q · n log n) | O(n) | Accepted |
| Optimal (same as brute force due to constraints) | O(q · n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two arrays: one for student names and one for their current scores, both indexed by student id.

1. Read n and the system password, then read all student names. We store names in an array so we can directly access a student's name by id.
2. Initialize a score array of size n with zeros, since no bonuses have been awarded yet.
3. For each command, we parse its type. If it is a bonus command, we extract the target id, bonus value, and password string.
4. We compare the provided password with the stored one. If it does not match exactly, we print the rejection message and skip any updates.
5. If the password matches, we add the bonus to the student's score and print the success message.
6. If the command is scoreboard, we construct a list of all students with their id, name, and score.
7. We sort this list by decreasing score and then increasing id. This ordering ensures deterministic ranking even when scores are equal.
8. We filter out all students with zero score since they should not appear in the scoreboard.
9. We assign ranks while scanning the sorted list. The first student gets rank 1. For each next student, if their score equals the previous student's score, they receive the same rank; otherwise, their rank becomes the current index position among displayed entries.
10. We print each entry as "rank id name score".

After these steps, the system state is consistent and ready for the next command.

### Why it works

At any moment, the score array represents exactly the sum of all accepted bonus operations. The scoreboard is always derived directly from this array, so sorting produces a correct global ordering. Because ranking depends only on equality of adjacent sorted scores, sharing rank for equal values preserves correctness under the required definition. Filtering zeros does not affect ordering because all excluded elements would not influence ranks among positive scores.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, password = input().split()
    n = int(n)

    names = [""] * (n + 1)
    for i in range(1, n + 1):
        names[i] = input().strip()

    score = [0] * (n + 1)

    q = int(input())
    out = []

    for _ in range(q):
        parts = input().split()

        if parts[0] == "bonus":
            idx = int(parts[1])
            val = int(parts[2])
            pw = parts[3]

            if pw == password:
                score[idx] += val
                out.append("Updated successfully")
            else:
                out.append("Wrong password please try again")

        else:
            arr = []
            for i in range(1, n + 1):
                if score[i] > 0:
                    arr.append((score[i], i, names[i]))

            arr.sort(key=lambda x: (-x[0], x[1]))

            rank_out = []
            current_rank = 0
            prev_score = None
            seen = 0

            for s, idx, name in arr:
                seen += 1
                if prev_score is None or s != prev_score:
                    current_rank = seen
                prev_score = s
                rank_out.append(f"{current_rank} {idx} {name} {s}")

            if rank_out:
                out.extend(rank_out)

        out.append("---")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution stores names and scores in direct index-based arrays for O(1) access. For each bonus command, it performs a constant-time password check and updates the score if valid. For scoreboard commands, it rebuilds a list of active students, sorts them using a tuple key that enforces both score priority and id tie-breaking, and then assigns ranks by tracking when the score changes.

A subtle point is rank assignment: we use a running counter `seen` to represent position in the sorted filtered list. Whenever the score changes, the rank is set to this position; otherwise, it is reused. This ensures equal scores share identical rank values.

The separator line is appended after every command as required, including after scoreboard outputs.

## Worked Examples

We trace the first sample in a compact form focusing on score changes and scoreboard outputs.

Initial state has all scores zero.

| Step | Command | Scores (partial view) | Action |
| --- | --- | --- | --- |
| 1 | bonus 3 12 ShAC | 3:12 | update success |
| 2 | bonus 1 8 ShAC | 1:8, 3:12 | update success |
| 3 | bonus 3 80 ShaC | unchanged | wrong password |
| 4 | bonus 6 12 ShAC | 1:8, 3:12, 6:12 | update success |

Now scoreboard sorts (3:12, 6:12, 1:8). Since 3 and 6 tie, they share rank 1.

| Rank | ID | Score |
| --- | --- | --- |
| 1 | 3 | 12 |
| 1 | 6 | 12 |
| 3 | 1 | 8 |

This shows both tie handling and id-based ordering between equal scores (id 3 < 6 is preserved).

The second sample exercises repeated updates and multiple scoreboard queries. It confirms that recomputation each time remains consistent, since no state other than the score array is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q · n log n) | Each scoreboard rebuild sorts up to n students, repeated q times |
| Space | O(n) | Storage for names and scores |

Given n, q ≤ 100, the maximum operations are on the order of 10⁴ sorting operations over at most 100 elements, which is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    # assume solve() is defined above
    solve()
    return sys.stdout.getvalue().strip()

# sample-like minimal case
assert run("""1 A
Alice
3
bonus 1 10 A
scoreboard
scoreboard
""").count("Alice") >= 1

# wrong password case
assert "Wrong password" in run("""2 X
A
B
2
bonus 1 5 Y
scoreboard
""")

# tie ranking case
assert "1 1" in run("""2 P
A
B
2
bonus 1 5 P
bonus 2 5 P
scoreboard
""")

# zero filtering case
assert "A" not in run("""1 P
A
1
scoreboard
""")

# ordering by id tie-break
assert run("""2 P
A
B
2
bonus 2 5 P
bonus 1 5 P
scoreboard
""").index("1 1") < run("""2 P
A
B
2
bonus 2 5 P
bonus 1 5 P
scoreboard
""").index("1 2")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single student | scoreboard shows only that student | base correctness |
| wrong password | rejection message | authentication logic |
| tie scores | same rank assignment | ranking correctness |
| no scores | empty scoreboard | zero filtering |
| id ordering | consistent ordering | tie-break rule |

## Edge Cases

A key edge case is when all students have zero points. In this case, a scoreboard command must produce no ranking lines at all, only separators. The algorithm handles this because we explicitly filter `score[i] > 0` before sorting.

Another edge case is repeated equal scores across many students. For example, if all students reach 10 points, they must all share rank 1. The rank assignment logic sets rank based on the first occurrence of a new score, so no increments occur until a lower score appears.

Password mismatch on consecutive bonus commands is also important. Since we do not modify state unless the password matches, repeated wrong attempts leave the score array unchanged, and later scoreboard outputs reflect only valid updates.
