---
title: "CF 102202B - Gosu"
description: "The match results form a directed tournament graph. Each student is a vertex, and for every pair of different students exactly one directed edge exists: if student (i) defeated student (j), there is an edge (i to j). A winning path is simply a directed path in this graph."
date: "2026-08-18T01:03:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "B"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 201
verified: false
draft: false
---

[CF 102202B - Gosu](https://codeforces.com/problemset/problem/102202/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 21s  
**Verified:** no  

## Solution
## Problem Understanding

The match results form a directed tournament graph. Each student is a vertex, and for every pair of different students exactly one directed edge exists: if student (i) defeated student (j), there is an edge (i \to j).

A winning path is simply a directed path in this graph. The distance from (x) to (y) is the shortest directed-path length, with the special value (9000) when (y) is unreachable. The weakness of a student is the largest distance from that student to any student. We need to output a student whose weakness is as small as possible, together with that minimum weakness.

The input is an (N \times N) character matrix. Row (i) describes every match involving student (i), where `W` means the edge goes from (i) to that column's student and `L` means the edge goes in the opposite direction. Since every pair plays exactly once, this is a tournament rather than an arbitrary directed graph.

The constraint (N \le 3000) is the central clue. Reading the entire matrix already costs (O(N^2)), which is about nine million characters at the maximum size and is completely reasonable. An (O(N^3)) algorithm, however, performs up to (27) billion basic graph operations when (N=3000), far beyond what a one-second time limit can tolerate. We need to extract more information directly from the tournament structure instead of computing all-pairs shortest paths.

There are two easy cases that a careless solution can mishandle. First, the distance from a student to themselves is zero, not one. For example,

```
2
-W
L-
```

Student 1 directly beats student 2, so the distances from student 1 are (0,1), giving weakness (1). The correct output is `1 1`. A solution that counts the starting vertex as requiring one step could incorrectly report (2).

The second case is when nobody beats everybody directly. Consider the cyclic tournament

```
3
-LW
W-L
LW-
```

Student 1 loses to student 2, but student 1 beats student 3, and student 3 beats student 2. Thus student 1 reaches every student within two wins, giving weakness (2). The correct output is `2 1`. Simply choosing the student with the largest number of direct wins and assuming the answer is always (1) would fail here.

A third subtlety is that the special value (9000) never needs to appear in the answer. A tournament always contains a student who can reach every other student in at most two directed edges. The solution below constructs such a student directly, so the optimal weakness is always either (1) or (2).

## Approaches

The direct approach is to treat the results as a directed graph and run a breadth-first search from every student. One BFS computes all shortest distances from one starting student, so after (N) BFS runs we know every student's weakness and can select the smallest one. With an adjacency matrix, each BFS may inspect (N) possible outgoing edges for each of (N) vertices, giving (O(N^2)) work per source and (O(N^3)) overall. At (N=3000), this is as many as (3000^3 = 27{,}000{,}000{,}000) adjacency checks, which is much too slow.

The brute-force method works because BFS exactly matches the definition of winning-path distance. The problem is that the tournament contains much stronger structure than a general directed graph.

The key observation is that a vertex with maximum outdegree is always able to reach every other vertex in at most two steps. Here, the outdegree is simply the number of `W` characters in that student's row.

Take a maximum-outdegree student (v), and consider another student (u) whom (v) loses to. If (v) could not reach (u) in two steps, then there would be no student (w) such that (v) beats (w) and (w) beats (u). Since every pair has exactly one winner, every student beaten by (v) must then be beaten by (u).

That gives a contradiction. Student (u) beats (v), and (u) also beats every student that (v) beats. Consequently, (u)'s number of direct wins is strictly larger than (v)'s, contradicting the choice of (v) as a maximum-outdegree student.

So every student either loses directly to (v), in which case there is a two-edge route through some intermediate student, or is already beaten directly by (v). Hence the weakness of a maximum-outdegree student is at most (2).

This reduces the entire problem to counting direct wins. If some student has (N-1) wins, their weakness is exactly (1), because every other student is reached directly. Otherwise, no student's weakness can be (1), while the maximum-outdegree student has weakness at most (2). Its weakness is consequently exactly (2).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with BFS from every student | (O(N^3)) | (O(N^2)) | Too slow |
| Maximum outdegree | (O(N^2)) | (O(N^2)) | Accepted |

## Algorithm Walkthrough

1. Read the complete result matrix. We need to inspect every character because the number of direct wins of every student determines the candidate.
2. For each row, count how many characters are `W`. This count is the student's outdegree, meaning the number of opponents that student defeated directly.
3. Keep the student with the largest outdegree. We do not need to construct any paths yet, because the maximum-outdegree property already guarantees that this student reaches everyone within two steps.
4. If the maximum outdegree is (N-1), output weakness (1) and that student. Every other student is a direct outgoing neighbor, so no positive distance larger than one is needed.
5. Otherwise, output weakness (2) and the same student. The maximum-outdegree argument proves that every opponent who is not beaten directly can be reached through one intermediate student. Since the chosen student does not beat everyone directly, its weakness cannot be (1), so it is exactly (2).

### Why it works

Let (v) be a student with maximum outdegree. Suppose (v) loses to some student (u). Assume for contradiction that (v) cannot reach (u) in two steps. For every student (w) that (v) beats, (u) must also beat (w), because otherwise (v \to w \to u) would be a valid two-step path. Since (u) additionally beats (v), every direct win of (v) is also a direct win of (u), plus (u)'s win over (v). Thus (u) has strictly larger outdegree than (v), contradicting maximality.

So every vertex is at distance at most two from (v). If (v) has (N-1) direct wins, its weakness is (1). If it has fewer, its weakness is at least (2), and the argument above gives an upper bound of (2). Hence the selected student's weakness is exactly the minimum possible value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    best_player = 0
    best_wins = -1

    for i in range(n):
        row = input().strip()
        wins = row.count('W')

        if wins > best_wins:
            best_wins = wins
            best_player = i

    weakness = 1 if best_wins == n - 1 else 2

    print(weakness, best_player + 1)

if __name__ == "__main__":
    solve()
```

The input loop reads one complete row at a time and uses `count('W')` to obtain the student's outdegree. The diagonal `-` and all `L` characters need no special handling because neither represents a direct win by the current row's student.

The comparison uses `>` rather than `>=`. Either choice would be correct because multiple maximum-outdegree students are allowed, but using `>` simply keeps the first such student.

The final test is `best_wins == n - 1`, not `best_wins == n`. A student cannot beat themselves, so there are only (N-1) possible direct wins. If that condition holds, every other vertex is reached in one edge. Otherwise the maximum-outdegree theorem gives a weakness of exactly two.

The answer converts the zero-based Python index back to the one-based student numbering required by the problem.

There is no integer-overflow issue in Python, and the largest count stored in `best_wins` is only (N-1). The matrix itself does not need to be stored after processing each row, which keeps the extra memory usage very small.

## Worked Examples

### Sample 1

The input describes a direct win from student 1 to student 2.

| Student | Row | Direct wins | Best after row | Weakness decision |
| --- | --- | --- | --- | --- |
| 1 | `-W` | 1 | student 1, 1 win | pending |
| 2 | `L-` | 0 | student 1, 1 win | pending |
| Final |  |  | student 1 | (1), since (1=N-1) |

Student 1 has one direct win and (N-1=1) is the maximum possible. Thus every opponent is reached directly, so the weakness is (1), giving `1 1`.

This example exercises the boundary between zero-length self-distance and one-edge distance. The student's own entry does not contribute to the win count.

### Sample 2

The result matrix is

```
-LW
W-L
LW-
```

Student 1 beats student 3 but loses to student 2. Student 2 also has one direct win, and student 3 has one direct win.

| Student | Row | Direct wins | Best after row | Weakness decision |
| --- | --- | --- | --- | --- |
| 1 | `-LW` | 1 | student 1, 1 win | pending |
| 2 | `W-L` | 1 | student 1, 1 win | pending |
| 3 | `LW-` | 1 | student 1, 1 win | pending |
| Final |  |  | student 1 | (2), since (1<N-1) |

For student 1, the path to student 2 has length two: (1 \to 3 \to 2). The maximum-outdegree theorem guarantees such a path without requiring us to search for it explicitly.

No student has two direct wins, so weakness (1) is impossible. Student 1 reaches everyone within two steps, so the minimum weakness is exactly (2). The output `2 1` is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2)) | Every one of the (N^2) matrix characters is read or examined once |
| Space | (O(N)) | One input row is stored at a time, with only a few counters and indices |

At (N=3000), (N^2=9{,}000{,}000), which is practical in the given limits. The algorithm avoids the (27) billion operations that an all-sources BFS approach could require. Python's string implementation also makes counting the `W` characters in each row efficient enough for this input size.

## Test Cases

The following test harness implements the same algorithm as a function so that the returned result can be checked. Since the problem permits any Gosu when several exist, the validator checks that the reported student has the claimed weakness rather than requiring one exact student index.

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.strip().splitlines()
    n = int(data[0])

    best_player = 0
    best_wins = -1

    for i in range(n):
        wins = data[i + 1].count('W')
        if wins > best_wins:
            best_wins = wins
            best_player = i

    weakness = 1 if best_wins == n - 1 else 2
    return f"{weakness} {best_player + 1}"

def brute_weakness(rows, start):
    n = len(rows)
    dist = [-1] * n
    dist[start] = 0
    queue = [start]

    for v in queue:
        for u in range(n):
            if rows[v][u] == 'W' and dist[u] == -1:
                dist[u] = dist[v] + 1
                queue.append(u)

    if -1 in dist:
        return 9000
    return max(dist)

def check(inp: str, out: str):
    lines = inp.strip().splitlines()
    n = int(lines[0])
    rows = lines[1:]

    weakness, player = map(int, out.split())
    assert 1 <= player <= n
    assert weakness == brute_weakness(rows, player - 1)

    all_weaknesses = [brute_weakness(rows, i) for i in range(n)]
    assert weakness == min(all_weaknesses)

def run(inp: str) -> str:
    out = solve_data(inp)
    check(inp, out)
    return out

# Provided samples
run("""2
-W
L-
""")

run("""3
-LW
W-L
LW-
""")

run("""5
-WLLW
L-LLW
WW-LL
WWW-W
LLWL-
""")

# Minimum size
run("""2
-W
L-
""")

# Three-cycle, where every student has weakness 2
run("""3
-LW
W-L
LW-
""")

# Transitive tournament, where student 1 beats everyone directly
run("""4
-WWW
L-WW
LL-W
LLL-
""")

# Maximum-size input, a transitive tournament.
# Student 1 beats everybody, so the answer must have weakness 1.
n = 3000
rows = []
for i in range(n):
    row = ['-'] * n
    for j in range(i + 1, n):
        row[j] = 'W'
        row[i] = 'L'
    rows.append(''.join(row))

large_input = str(n) + '\n' + '\n'.join(rows) + '\n'
large_output = solve_data(large_input)
assert large_output == "1 1", "maximum-size transitive tournament"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / -W / L-` | `1 1` | Minimum (N), direct winner, and correct handling of the diagonal |
| `3 / -LW / W-L / LW-` | `2 1` or another valid Gosu | A tournament with no universal direct winner |
| `4 / -WWW / L-WW / LL-W / LLL-` | `1 1` | Boundary case where the maximum outdegree is (N-1) |
| Transitive tournament with (N=3000) | `1 1` | Maximum input size and (O(N^2)) scalability |

A literal "all-equal values" tournament is impossible for (N>2), because every pair must have exactly one winner and one loser. The closest relevant test is the three-cycle, where every student has exactly one direct win and the direct-win counts are equal. The algorithm must still choose a valid student and correctly return weakness (2).

## Edge Cases

For the minimum-size tournament

```
2
-W
L-
```

the first student's outdegree is (1=N-1), while the second student's outdegree is zero. The algorithm selects student 1 and returns weakness (1). The self-distance is zero, and the only other distance is one, so the result matches the definition exactly.

For a tournament with no universal winner,

```
3
-LW
W-L
LW-
```

all three students have outdegree one. The algorithm keeps student 1 because it is the first maximum. Student 1 directly reaches student 3 and reaches student 2 through student 3, so its weakness is (2). Since no student has (N-1=2) direct wins, weakness (1) is impossible.

For the boundary case where one student wins every match,

```
4
-WWW
L-WW
LL-W
LLL-
```

student 1 has outdegree three, which equals (N-1). The algorithm immediately assigns weakness (1). Every other student's outdegree is smaller, so selecting student 1 is also clearly optimal.

The maximum-size case contains 3000 students. A transitive tournament can be formed by making student (i) beat every student with a larger index. Student 1 then has 2999 direct wins, so the algorithm returns `1 1`. The implementation processes exactly 3000 rows and counts their `W` characters, about nine million matrix entries in total. It never performs BFS or constructs a distance matrix, which is why the quadratic approach remains practical at the upper bound.
