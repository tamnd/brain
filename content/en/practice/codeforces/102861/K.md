---
title: "CF 102861K - Between Us"
description: "We are given an undirected friendship graph. Every vertex represents a player and every edge represents a friendship relation. We need to split the players into at most two groups so that, for every player, the number of friends that belong to the same group is odd."
date: "2026-07-25T14:07:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102861
codeforces_index: "K"
codeforces_contest_name: "2020-2021 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102861
solve_time_s: 46
verified: true
draft: false
---

[CF 102861K - Between Us](https://codeforces.com/problemset/problem/102861/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected friendship graph. Every vertex represents a player and every edge represents a friendship relation. We need to split the players into at most two groups so that, for every player, the number of friends that belong to the same group is odd. The actual names of the two groups do not matter, only whether two players are placed together.

The input gives up to 100 players and their friendship edges. The answer is `Y` if some assignment of players to the two possible groups satisfies the odd-friend condition for every player, and `N` otherwise.

The small limit on the number of players is the key observation about the intended complexity. With 100 variables, algorithms based on linear algebra are practical. A brute force assignment tries every possible split, which means checking up to (2^{100}) possibilities, far beyond what any program can handle. We need to transform the graph condition into a system with at most 100 unknowns, where Gaussian elimination is easily fast enough.

There are a few cases where an intuitive approach can fail. A common mistake is to think that placing every player into one group should always work if all degrees are odd. This is false when some vertices have even degree. For example:

```
3 2
1 2
2 3
```

The middle player has two friends, so if everyone is in the same group, that player sees two friends, which is even. The correct output is `N`. A method that only checks the total degree of the graph misses the fact that each vertex has its own condition.

Another tricky case is that the two groups do not need to both be non-empty. For example:

```
2 1
1 2
```

Putting both players into the same group gives each player one friend inside the group. The correct output is `Y`. A solution that forces a non-empty second group would incorrectly reject this case.

A third case is when several valid partitions exist. For example:

```
4 4
1 2
2 3
3 4
4 1
```

The cycle can be split in multiple ways, and the algorithm only needs to find one valid assignment. It should not assume that a unique partition exists.

## Approaches

The direct brute force approach is to decide the group of every player independently. For each of the (2^P) possible assignments, we count, for every player, how many adjacent vertices have the same assigned group. If all counts are odd, the partition exists.

This approach is correct because it examines every possible partition. However, with (P=100), the number of assignments is (2^{100}), which is approximately (1.27 \times 10^{30}). Even if checking one assignment took only a few operations, this would be impossible.

The important structure of the problem is that the condition only depends on parity. We do not need the exact number of friends in the same group, only whether that number is odd or even. Parity naturally leads to arithmetic modulo 2, where every value is either zero or one.

Let (x_i) describe the group of player (i). We use (0) and (1) for the two groups. For a neighbor (j), the value indicating whether (j) is in the same group as (i) can be written as:

[
1 + x_i + x_j
]

when calculations are performed modulo 2. The expression is one when the two players have equal group values and zero otherwise.

For a player (i), adding this expression over all friends gives the parity of the number of same-group friends:

[
deg_i + \sum_{j \in N(i)} x_j + deg_i \cdot x_i
]

All operations are modulo 2. This value must be equal to 1 because the number of same-group friends must be odd.

Rearranging gives a linear equation:

[
\sum_{j \in N(i)} x_j + (deg_i \bmod 2)x_i = 1 + (deg_i \bmod 2)
]

Every player contributes one equation, and every player is one variable. The problem becomes checking whether a system of at most 100 linear equations over GF(2) has a solution. Gaussian elimination works directly for this.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^P · P²) | O(P²) | Too slow |
| Optimal | O(P³) | O(P²) | Accepted |

## Algorithm Walkthrough

1. Build a binary matrix representing the linear system. Each row corresponds to one player and each column corresponds to one player's group variable. The final column stores the required value on the right side of the equation.

The coefficient of variable (x_j) is one if player (j) is a friend of player (i). Additionally, if player (i) has odd degree, the coefficient of (x_i) is toggled because of the (deg_i \cdot x_i) term.
2. Apply Gaussian elimination over modulo 2. Find a row with a one in the current column and swap it into the current pivot position.

Swapping is needed because a pivot can appear below the current row, and without moving it upward the column cannot be eliminated correctly.
3. Use the pivot row to remove the current variable from every other row.

Since all operations are modulo 2, removing a variable is just XORing the pivot row with another row. This keeps the matrix values binary.
4. After elimination, inspect every row. If all variable coefficients are zero but the final value is one, the equation is impossible, so no valid partition exists.

Such a row represents a contradiction like (0 = 1).
5. If no contradiction exists, the system has at least one assignment of group values, so the answer is `Y`.

Why it works:

The transformation from the graph problem to equations preserves the exact condition we need. Any valid partition produces values for the variables that satisfy every equation, and any solution of the equations gives group values where every player has an odd number of friends in the same group. Gaussian elimination over GF(2) does not change the set of solutions, it only transforms the equations into an easier form. The final contradiction check distinguishes systems with no possible partition from systems that have at least one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    P, F = map(int, input().split())
    adj = [[0] * P for _ in range(P)]
    deg = [0] * P

    for _ in range(F):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a][b] = 1
        adj[b][a] = 1
        deg[a] += 1
        deg[b] += 1

    mat = [[0] * (P + 1) for _ in range(P)]

    for i in range(P):
        for j in range(P):
            mat[i][j] = adj[i][j]
        if deg[i] % 2 == 1:
            mat[i][i] ^= 1
        mat[i][P] = 1 ^ (deg[i] % 2)

    row = 0
    for col in range(P):
        pivot = row
        while pivot < P and mat[pivot][col] == 0:
            pivot += 1

        if pivot == P:
            continue

        mat[row], mat[pivot] = mat[pivot], mat[row]

        for i in range(P):
            if i != row and mat[i][col]:
                for j in range(col, P + 1):
                    mat[i][j] ^= mat[row][j]

        row += 1

    for i in range(P):
        all_zero = True
        for j in range(P):
            if mat[i][j]:
                all_zero = False
                break
        if all_zero and mat[i][P]:
            print("N")
            return

    print("Y")

if __name__ == "__main__":
    solve()
```

The adjacency matrix stores only whether two players are friends. Since the constraints are small, using a (P \times P) matrix keeps the equation construction simple and avoids needing extra graph traversal logic.

The matrix construction follows the derived equation directly. Every friendship contributes a coefficient for the friend's variable. For a player with odd degree, the player's own variable receives an additional coefficient. The right side is computed as (1 + deg_i) modulo 2.

The elimination uses XOR because addition and subtraction are identical in modulo 2 arithmetic. The pivot search skips columns that cannot currently be used as pivots, which is necessary because some variables may be free variables.

The final scan checks only for impossible rows. A row containing no variables but a nonzero result means the system demands a false statement. Any other final form still has at least one assignment.

## Worked Examples

For the first sample:

```
4 4
4 2
1 3
2 3
1 4
```

The equation system is built from the four players.

| Step | Current operation | Pivot row | Result |
| --- | --- | --- | --- |
| 1 | Build equations | None | Four parity equations created |
| 2 | Eliminate first variable | Row 0 | Other rows updated by XOR |
| 3 | Eliminate remaining variables | Rows 1 to 3 | System reaches reduced form |
| 4 | Check contradictions | None found | Output `Y` |

The elimination succeeds without creating a row representing an impossible equation. This confirms that at least one assignment of players to groups exists.

For the second sample:

```
4 3
4 2
2 3
1 2
```

| Step | Current operation | Pivot row | Result |
| --- | --- | --- | --- |
| 1 | Build equations | None | Four parity equations created |
| 2 | Select pivots | Available columns found | Variables are constrained |
| 3 | XOR elimination | All pivot columns cleared | Equivalent system obtained |
| 4 | Check contradictions | None found | Output `Y` |

This example shows that the graph does not need to be regular or highly connected. The linear system handles each player's local condition independently while keeping the equations consistent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(P³) | Gaussian elimination performs up to P pivot operations, and each may update P rows of length P |
| Space | O(P²) | The equation matrix contains P rows and P+1 columns |

With (P \le 100), the cubic running time is about one million elementary operations, which is easily within typical limits. The memory usage is also small because the entire system contains only around ten thousand stored values.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    data = inp.strip().split()
    if not data:
        return ""
    it = iter(data)
    P = int(next(it))
    F = int(next(it))

    adj = [[0] * P for _ in range(P)]
    deg = [0] * P

    for _ in range(F):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        adj[a][b] = adj[b][a] = 1
        deg[a] += 1
        deg[b] += 1

    mat = [[0] * (P + 1) for _ in range(P)]
    for i in range(P):
        for j in range(P):
            mat[i][j] = adj[i][j]
        if deg[i] % 2:
            mat[i][i] ^= 1
        mat[i][P] = 1 ^ (deg[i] % 2)

    row = 0
    for col in range(P):
        pivot = row
        while pivot < P and mat[pivot][col] == 0:
            pivot += 1
        if pivot == P:
            continue
        mat[row], mat[pivot] = mat[pivot], mat[row]
        for i in range(P):
            if i != row and mat[i][col]:
                for j in range(col, P + 1):
                    mat[i][j] ^= mat[row][j]
        row += 1

    for i in range(P):
        if all(mat[i][j] == 0 for j in range(P)) and mat[i][P]:
            return "N\n"
    return "Y\n"

assert solve_case("""4 4
4 2
1 3
2 3
1 4
""") == "Y\n", "sample 1"

assert solve_case("""4 3
4 2
2 3
1 2
""") == "Y\n", "sample 2"

assert solve_case("""5 5
3 5
3 1
1 4
2 5
2 4
""") == "N\n", "sample 3"

assert solve_case("""2 1
1 2
""") == "Y\n", "minimum size"

assert solve_case("""3 2
1 2
2 3
""") == "N\n", "even degree contradiction"

assert solve_case("""4 4
1 2
2 3
3 4
4 1
""") == "Y\n", "cycle graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two connected players | Y | Allows a single non-empty group |
| Three-player path | N | Detects a contradiction caused by an even internal degree |
| Four-player cycle | Y | Handles multiple valid assignments |
| Provided samples | Y, Y, N | Confirms the implementation against official cases |

## Edge Cases

For the path of three players:

```
3 2
1 2
2 3
```

The middle player has degree two. The equation for that player cannot be satisfied by simply putting everyone together because the same-group friend count would be two. During elimination, this appears as a row with all variable coefficients equal to zero and the right side equal to one. The algorithm returns `N`.

For two connected players:

```
2 1
1 2
```

Both players can belong to the same group. Each sees exactly one friend in that group. The linear system has a solution, so elimination finishes without contradiction and returns `Y`.

For a graph where several partitions work:

```
4 4
1 2
2 3
3 4
4 1
```

The algorithm does not attempt to choose a special partition. It only verifies that the corresponding equations are consistent. Since the reduced matrix has no impossible row, some assignment exists and the answer is `Y`.

I can also adapt the editorial to a shorter Codeforces-style format if you want a more contest-submission-length version.
