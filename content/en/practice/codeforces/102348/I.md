---
title: "CF 102348I - Radio Stations"
description: "We have (p) radio stations. Choosing station (i) means signing a contract with it, and this is possible only when the chosen signal power (f) lies inside its interval ([li,ri]). For a fixed (f), a station outside its interval is forced to remain unselected."
date: "2026-08-13T01:06:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "I"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 362
verified: true
draft: false
---

[CF 102348I - Radio Stations](https://codeforces.com/problemset/problem/102348/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (p) radio stations. Choosing station (i) means signing a contract with it, and this is possible only when the chosen signal power (f) lies inside its interval ([l_i,r_i]). For a fixed (f), a station outside its interval is forced to remain unselected.

Every complaint gives a pair ((x_i,y_i)) and requires at least one of those two stations to be selected. Every interference pair ((u_i,v_i)) requires at most one of those two stations to be selected. The task is to choose both (f) and a set of stations satisfying all these conditions, or report that no such choice exists. The official constraints allow all four main parameters to reach (4\cdot10^5), with a 7 second limit and 256 MB of memory.

For the station-selection part alone, this is already a 2-SAT instance. Let (S_i) mean that station (i) is selected. A complaint becomes (S_x\lor S_y), while an interference pair becomes (\lnot S_u\lor\lnot S_v). The difficulty is that (f) is not known beforehand, and choosing (f) can force many stations to false.

A direct implementation could try every (f), construct the corresponding 2-SAT instance, and run SCC each time. One check costs (O(p+n+m)), so all (M) choices cost (O(M(p+n+m))). At the maximum constraints this is about (4\cdot10^5\cdot1.2\cdot10^6=4.8\cdot10^{11}) input-scale operations, far beyond what the time limit permits.

There are several boundary cases that easily break an implementation. A station whose interval is ([l,r]) is usable at both endpoints, so replacing the conditions by (l<f<r) silently loses valid answers. For example,

```
2 3 2 2
1 2
2 3
1 1
1 2
2 2
1 2
2 3
```

has the valid answer (f=2) with only station 2 selected. Station 2 is usable exactly at its upper endpoint, and selecting it satisfies both complaints.

Another failure occurs when different complaints can only be served at disjoint powers. For example,

```
2 4 2 2
1 2
3 4
1 1
1 1
2 2
2 2
1 2
3 4
```

has answer `-1`. At (f=1), only stations 1 and 2 can be selected, so the second complaint cannot be satisfied. At (f=2), only stations 3 and 4 are usable, so the first complaint cannot be satisfied. Checking only whether the station-selection formula is satisfiable without representing (f) would incorrectly accept this instance.

A third subtle case is that the signal power itself has to be represented by a valid integer from 1 through (M). If the construction permits an artificial value 0 or (M+1), it can produce a Boolean assignment that has no corresponding signal power. The threshold construction below explicitly prevents that.

## Approaches

The brute-force solution is conceptually straightforward. Fix a value of (f), mark every station whose interval does not contain (f) as forced unselected, add the complaint and interference clauses, and solve the resulting 2-SAT instance using strongly connected components. If the formula is satisfiable, the SCC assignment gives the selected stations. Trying all (M) powers is correct because every possible answer uses exactly one of them.

The problem is the repeated SCC computation. Even though a single 2-SAT check is linear, multiplying it by (M) produces roughly (4.8\cdot10^{11}) operations in the worst case. The large (M) is specifically there to rule out this approach.

The key observation is that we do not actually need to enumerate (f). Instead, represent the statement “(f) is at least (t)” as another Boolean variable. Call it (T_t). We add (T_{t+1}\rightarrow T_t), so the truth values of these variables must form a prefix of true values. We also force (T_1) to true and (T_{M+1}) to false. Consequently, every satisfying assignment contains exactly one cutoff, and that cutoff is a legal value of (f).

This lets station intervals become ordinary 2-SAT implications. If station (i) is selected, then (f\ge l_i), so (S_i\rightarrow T_{l_i}). Also (f\le r_i), which is equivalent to (f<r_i+1), so (S_i\rightarrow\lnot T_{r_i+1}). Both are ordinary implications between Boolean literals.

The entire problem is consequently one 2-SAT instance with (p+M+1) Boolean variables. The construction has only (O(n+p+m+M)) clauses and can be solved by one SCC computation. This is the same prefix-optimization viewpoint commonly used for this problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(M(p+n+m))) | (O(p+n+m)) | Too slow |
| Optimal | (O(p+n+m+M)) | (O(p+n+m+M)) | Accepted |

## Algorithm Walkthrough

1. Create a Boolean variable (S_i) for every station. Its true value means that station (i) is selected, and its false value means that it is not selected. Represent every Boolean variable by two implication-graph vertices, one for the literal and one for its negation.
2. Convert every complaint ((x,y)) into the clause (S_x\lor S_y). In an implication graph this gives the two edges (\lnot S_x\rightarrow S_y) and (\lnot S_y\rightarrow S_x). These edges express exactly the two ways in which the complaint could become forced to hold.
3. Convert every interference pair ((u,v)) into the clause (\lnot S_u\lor\lnot S_v). Its implication edges are (S_u\rightarrow\lnot S_v) and (S_v\rightarrow\lnot S_u). Thus selecting either endpoint forces the other endpoint to be unselected.
4. Introduce a Boolean variable (T_t) for every (t) from 1 through (M+1), where the intended meaning is (T_t=(f\ge t)). Add the clauses (\lnot T_{t+1}\lor T_t) for every (t) from 1 through (M). These clauses force the threshold variables to be monotone.
5. Force (T_1) to true and (T_{M+1}) to false. Because the threshold variables are monotone, there is now exactly one boundary between true and false values. If the largest true threshold is (f), then (T_t) is true precisely for (t\le f), so this Boolean assignment represents the integer signal power (f).
6. For every station (i), add (S_i\rightarrow T_{l_i}). If station (i) is selected, the threshold for (l_i) must be true, which means (f\ge l_i).
7. For every station (i), add (S_i\rightarrow\lnot T_{r_i+1}). Since (T_{r_i+1}) means (f\ge r_i+1), its negation means (f\le r_i). Together with the previous implication, selecting station (i) forces (l_i\le f\le r_i).
8. Build the implication graph from all these clauses and compute its strongly connected components with Tarjan's algorithm. A 2-SAT instance is impossible exactly when some variable and its negation belong to the same SCC. We check this for both the station variables and the threshold variables.
9. If the formula is satisfiable, assign each variable using the SCC order. With Tarjan's component numbering, components are produced in reverse topological order, so the literal with the smaller component number is the selected truth value. For a station, (S_i) is true when its true literal has a smaller component number than its false literal.
10. Scan (T_1,\ldots,T_M) and take the largest threshold whose true literal is selected. Monotonicity guarantees that these true thresholds form a prefix, so this largest index is exactly the required (f). Output every station whose (S_i) variable is true.

The invariant behind the construction is that every satisfying assignment of the threshold variables corresponds to exactly one legal integer (f), while every selected station is forced to have its entire interval contain that (f). Conversely, any valid choice of (f) and stations can be translated into truth values for all (S_i) and (T_t) that satisfy every constructed clause. Thus the constructed 2-SAT instance is satisfiable exactly when the original problem has an answer.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    input = sys.stdin.readline

    n, p, M, m = map(int, input().split())

    # Store complaints temporarily. Conflicts can be processed later.
    complaints = array('i')
    for _ in range(n):
        x, y = map(int, input().split())
        complaints.append(x - 1)
        complaints.append(y - 1)

    left = array('i')
    right = array('i')
    for _ in range(p):
        l, r = map(int, input().split())
        left.append(l)
        right.append(r)

    # Variables:
    #   0 .. p-1          : station variables
    #   p .. p+M          : threshold variables T_1 .. T_{M+1}
    variables = p + M + 1
    vertices = variables * 2

    # Store clauses as pairs of literal IDs.
    # Literal 2*v is v=True, literal 2*v+1 is v=False.
    clauses = array('i')

    # Complaint: S_x OR S_y
    for i in range(0, 2 * n, 2):
        x = complaints[i]
        y = complaints[i + 1]
        clauses.append(2 * x)
        clauses.append(2 * y)

    del complaints

    # Station interval:
    # S_i -> T_l
    # S_i -> !T_{r+1}
    for i in range(p):
        station_true = 2 * i

        tl_var = p + left[i] - 1
        tr1_var = p + right[i]

        clauses.append(station_true ^ 1)
        clauses.append(2 * tl_var)

        clauses.append(station_true ^ 1)
        clauses.append(2 * tr1_var + 1)

    del left
    del right

    # Conflict: !S_u OR !S_v
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        clauses.append(2 * u + 1)
        clauses.append(2 * v + 1)

    # T_{t+1} -> T_t
    # Equivalent to !T_{t+1} OR T_t.
    for t in range(1, M + 1):
        cur = p + t - 1
        nxt = cur + 1
        clauses.append(2 * nxt + 1)
        clauses.append(2 * cur)

    # T_1 must be true.
    t1 = p
    clauses.append(2 * t1)

    # T_{M+1} must be false.
    tm1 = p + M
    clauses.append(2 * tm1 + 1)

    # Build adjacency in CSR form.
    # For clause (a OR b):
    #   !a -> b
    #   !b -> a
    degree = array('i', [0]) * vertices

    clen = len(clauses)
    for i in range(0, clen, 2):
        a = clauses[i]
        b = clauses[i + 1]
        degree[a ^ 1] += 1
        degree[b ^ 1] += 1

    start = array('i', [0]) * (vertices + 1)
    total = 0
    for i in range(vertices):
        start[i] = total
        total += degree[i]
    start[vertices] = total

    edge = array('i', [0]) * total
    pos = array('i', start)

    for i in range(0, clen, 2):
        a = clauses[i]
        b = clauses[i + 1]

        u = a ^ 1
        idx = pos[u]
        edge[idx] = b
        pos[u] = idx + 1

        u = b ^ 1
        idx = pos[u]
        edge[idx] = a
        pos[u] = idx + 1

    del clauses
    del degree
    del pos

    # Iterative Tarjan SCC.
    #
    # Recursive Tarjan is unsafe here because the graph can have more
    # than 1.6 million vertices.
    dfn = array('i', [0]) * vertices
    low = array('i', [0]) * vertices
    comp = array('i', [0]) * vertices
    on_stack = bytearray(vertices)

    scc_stack = array('i')
    dfs_vertices = array('i')
    dfs_edges = array('i')

    timer = 0
    component_count = 0

    for root in range(vertices):
        if dfn[root]:
            continue

        timer += 1
        dfn[root] = timer
        low[root] = timer
        on_stack[root] = 1
        scc_stack.append(root)

        dfs_vertices.append(root)
        dfs_edges.append(start[root])

        while dfs_vertices:
            v = dfs_vertices[-1]
            e = dfs_edges[-1]

            if e < start[v + 1]:
                w = edge[e]
                dfs_edges[-1] = e + 1

                if dfn[w] == 0:
                    timer += 1
                    dfn[w] = timer
                    low[w] = timer
                    on_stack[w] = 1
                    scc_stack.append(w)

                    dfs_vertices.append(w)
                    dfs_edges.append(start[w])
                elif on_stack[w]:
                    dw = dfn[w]
                    if dw < low[v]:
                        low[v] = dw
            else:
                dfs_vertices.pop()
                dfs_edges.pop()

                if dfs_vertices:
                    parent = dfs_vertices[-1]
                    lv = low[v]
                    if lv < low[parent]:
                        low[parent] = lv

                if low[v] == dfn[v]:
                    component_count += 1
                    while True:
                        w = scc_stack.pop()
                        on_stack[w] = 0
                        comp[w] = component_count
                        if w == v:
                            break

    del dfn
    del low
    del on_stack
    del scc_stack
    del dfs_vertices
    del dfs_edges

    # Every variable must be different from its negation.
    for v in range(variables):
        if comp[2 * v] == comp[2 * v + 1]:
            print(-1)
            return

    # Tarjan numbers SCCs in reverse topological order.
    # Smaller component number means the literal is chosen.
    selected = []
    for i in range(p):
        if comp[2 * i] < comp[2 * i + 1]:
            selected.append(i + 1)

    # Recover f from the threshold variables.
    f = 1
    for t in range(1, M + 1):
        var = p + t - 1
        if comp[2 * var] < comp[2 * var + 1]:
            f = t

    print(len(selected), f)
    print(*selected)

if __name__ == "__main__":
    solve()
```

The first part of the implementation reads the complaints and intervals. Complaints have to be stored temporarily because the station interval data comes afterward, while the interference pairs arrive after the intervals and can be converted directly into clauses.

Each Boolean variable occupies two consecutive literal IDs. Even IDs represent the true literal and odd IDs represent the false literal, so negation is simply `literal ^ 1`. This makes the implication construction compact and avoids storing separate objects for literals.

The code stores all 2-SAT clauses temporarily as an `array('i')`. A normal Python list would consume substantially more memory because its integer elements are Python objects. The same reason motivates using `array('i')` for the graph and SCC arrays.

The implication graph is stored in CSR form rather than as a list of Python lists. The `start[v]` and `start[v+1]` range contains exactly the outgoing edges of vertex `v`. This avoids millions of Python list objects and keeps every graph index at four bytes.

The SCC computation is iterative Tarjan. A recursive DFS can reach a depth proportional to the number of graph vertices, which can exceed 1.6 million here. The two explicit DFS stacks preserve the same state that recursive calls would have preserved: the current vertex and the next outgoing edge that still needs to be examined.

The interval encoding deliberately uses (r_i+1). The upper condition is (f\le r_i), which is exactly (\lnot(f\ge r_i+1)). Since (r_i) can equal (M), the additional threshold (T_{M+1}) is necessary. It is forced false, so a station with (r_i=M) receives the correct unrestricted upper bound.

No integer can overflow in Python, and every graph index is at most about 1.6 million, which also fits comfortably inside the four-byte arrays used by the implementation.

## Worked Examples

For Sample 1, consider the valid assignment with (f=3) and stations 1 and 3 selected. The threshold variables describe (f=3) as (T_1=T_2=T_3=\text{true}) and (T_4=\text{false}).

| Stage | State |
| --- | --- |
| Signal power | (f=3) |
| (T_1,T_2,T_3,T_4) | true, true, true, false |
| Selected stations | 1, 3 |
| Station 1 interval | ([1,4]), valid |
| Station 3 interval | ([3,4]), valid |
| Complaint ((1,3)) | satisfied by station 1 or 3 |
| Complaint ((2,3)) | satisfied by station 3 |
| Conflict ((1,4)) | station 4 is unselected |
| Conflict ((3,4)) | station 4 is unselected |
| Result | valid |

The SCC assignment may choose a different satisfying assignment because the problem allows arbitrary answers. What matters is that the selected threshold variables form a prefix, and every selected station is compatible with the resulting cutoff.

For Sample 2, stations 1 and 2 are available only for powers 1 and 2, while stations 3 and 4 are available only for powers 3 and 4.

| Signal power | Available stations | First complaint | Second complaint | Conflict | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1, 2 | requires 1 or 2 | requires 2 or 4, so 2 | 1 and 2 cannot both be selected | impossible |
| 2 | 1, 2 | requires 1 or 2 | requires 2 or 4, so 2 | 1 and 2 cannot both be selected | impossible |
| 3 | 3, 4 | requires 1 or 3, so 3 | requires 2 or 4, so 4 | 3 and 4 cannot both be selected | impossible |
| 4 | 3, 4 | requires 1 or 3, so 3 | requires 2 or 4, so 4 | 3 and 4 cannot both be selected | impossible |

The threshold formulation represents all four possibilities in one 2-SAT instance instead of rebuilding a formula four times. The SCC computation discovers the contradiction between the required selections and the interference clauses, so the program prints `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+p+m+M)) | There are (O(n+p+m+M)) clauses and vertices, and Tarjan examines every vertex and implication edge once. |
| Space | (O(n+p+m+M)) | The temporary clauses, CSR graph, SCC arrays, and input intervals are all linear in the input size. |

At the maximum constraints there are at most about (8\cdot10^5) Boolean variables and about (4\cdot10^6) implication edges. The implementation uses packed four-byte integer arrays and an iterative SCC traversal, which keeps memory substantially below the 256 MB limit. The linear construction and SCC pass replace the brute-force (4.8\cdot10^{11})-scale work with a few million graph operations.

## Test Cases

Because the output is not unique, an exact string comparison is not appropriate for these tests. The test harness below checks that a returned solution is semantically valid. The maximum-size test only checks that the solver finds a solution, since fully parsing and independently validating hundreds of thousands of lines would make the test harness itself unnecessarily expensive.

```python
# Assume the submitted solution is saved as solution.py.
# Its solve() function reads stdin and writes stdout.

import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str, possible: bool):
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    p = next(it)
    M = next(it)
    m = next(it)

    complaints = []
    for _ in range(n):
        complaints.append((next(it), next(it)))

    intervals = []
    for _ in range(p):
        intervals.append((next(it), next(it)))

    conflicts = []
    for _ in range(m):
        conflicts.append((next(it), next(it)))

    out = out.strip()

    if not possible:
        assert out == "-1"
        return

    tokens = list(map(int, out.split()))
    assert len(tokens) >= 2

    k, f = tokens[0], tokens[1]
    chosen = tokens[2:]

    assert 1 <= f <= M
    assert k == len(chosen)
    assert len(set(chosen)) == k
    assert all(1 <= x <= p for x in chosen)

    chosen_set = set(chosen)

    for x, y in complaints:
        assert x in chosen_set or y in chosen_set

    for u, v in conflicts:
        assert not (u in chosen_set and v in chosen_set)

    for x in chosen:
        l, r = intervals[x - 1]
        assert l <= f <= r

# Provided sample 1
sample1 = """\
2 4 4 2
1 3
2 3
1 4
1 2
3 4
1 4
1 2
3 4
"""
validate(sample1, run(sample1), True)

# Provided sample 2
sample2 = """\
2 4 4 2
1 3
2 4
1 2
1 2
3 4
3 4
1 2
3 4
"""
validate(sample2, run(sample2), False)

# Minimum feasible size under the distinct-pair condition.
case_min = """\
2 3 2 2
1 2
2 3
1 1
1 2
2 2
1 2
2 3
"""
validate(case_min, run(case_min), True)

# All intervals are equal, so the signal power is unrestricted inside [1, 2].
case_equal = """\
2 4 2 2
1 2
3 4
1 2
1 2
1 2
1 2
1 2
3 4
"""
validate(case_equal, run(case_equal), True)

# The two complaints require disjoint signal ranges.
case_impossible = """\
2 4 2 2
1 2
3 4
1 1
1 1
2 2
2 2
1 2
3 4
"""
validate(case_impossible, run(case_impossible), False)

# Endpoint test: station 2 is usable at both l=1 and r=2,
# and f=2 gives a valid solution using only station 2.
case_endpoint = """\
2 3 2 2
1 2
2 3
1 1
1 2
2 2
1 2
2 3
"""
validate(case_endpoint, run(case_endpoint), True)

# Maximum-size stress test.
# An even cycle is both the complaint graph and the conflict graph.
# Every interval is [1, M], so an alternating selection is valid.
N = 400000
P = 400000
MM = 400000
E = 400000

parts = [f"{N} {P} {MM} {E}\n"]

for i in range(1, N):
    parts.append(f"{i} {i + 1}\n")
parts.append(f"1 {N}\n")

parts.extend(["1 400000\n"] * P)

for i in range(1, N):
    parts.append(f"{i} {i + 1}\n")
parts.append(f"1 {N}\n")

maximum_case = "".join(parts)
assert not run(maximum_case).startswith("-1")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Any valid assignment | Basic satisfiable instance with different station intervals |
| Sample 2 | `-1` | Interaction between complaints, conflicts, and disjoint frequency ranges |
| `case_min` | Any valid assignment | Smallest practically valid configuration under distinct-pair requirements |
| `case_equal` | Any valid assignment | All intervals equal and multiple possible signal powers |
| `case_impossible` | `-1` | Complaints that require mutually separated frequency ranges |
| `case_endpoint` | Any valid assignment, with (f=2) possible | Inclusive lower and upper interval boundaries |
| `maximum_case` | Any valid assignment | Maximum values of all four major input parameters and memory pressure |

## Edge Cases

The inclusive endpoint case is handled by the upper implication (S_i\rightarrow\lnot T_{r_i+1}). In `case_endpoint`, station 2 has interval ([1,2]). When the SCC assignment chooses (T_2=\text{true}) and (T_3=\text{false}), station 2 is allowed because the required inequalities are (f\ge1) and (f<3), giving (f\le2). The algorithm can consequently return station 2 with (f=2).

The disjoint-frequency case is handled because the threshold variables are global rather than being tested independently. In `case_impossible`, selecting a station from the first complaint forces (f=1), while selecting a station from the second complaint forces (f=2). The threshold clauses make these requirements part of the same Boolean system, and the resulting contradiction places a variable and its negation in the same SCC. The algorithm returns `-1`.

The boundary of the allowed power range is protected by the forced variables (T_1=\text{true}) and (T_{M+1}=\text{false}). For a hypothetical assignment corresponding to (f=0), (T_1) would have to be false, contradicting the first unit clause. For an assignment corresponding to (f=M+1), (T_{M+1}) would have to be true, contradicting the second unit clause. Every surviving threshold assignment consequently corresponds to some (f\in[1,M]).

Finally, the algorithm does not assume that the interference relation is transitive. Each listed pair contributes exactly one “not both selected” clause. If station 1 conflicts with station 2 and station 2 conflicts with station 3, the construction does not invent a conflict between stations 1 and 3. This matches the graph in the input and prevents a common mistake where interference pairs are incorrectly treated as connected components.
