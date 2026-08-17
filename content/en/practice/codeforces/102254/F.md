---
title: "CF 102254F - Friendship Matters"
description: "There are (n) students, each identified by a unique name. Initially every student belongs to a separate team. A type 1 operation merges the teams containing two specified students. A type 2 operation asks whether those two students currently belong to the same team."
date: "2026-08-17T21:20:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102254
codeforces_index: "F"
codeforces_contest_name: "IME++ Starters Try-outs 2019"
rating: 0
weight: 102254
solve_time_s: 446
verified: false
draft: false
---

[CF 102254F - Friendship Matters](https://codeforces.com/problemset/problem/102254/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 26s  
**Verified:** no  

## Solution
## Problem Understanding

There are (n) students, each identified by a unique name. Initially every student belongs to a separate team. A type 1 operation merges the teams containing two specified students. A type 2 operation asks whether those two students currently belong to the same team.

The names are strings, so before processing the operations we need a way to translate each name into a compact integer identifier. Once that is done, the actual problem is purely about maintaining connected groups under merges and answering connectivity queries.

The input contains up to (10^5) students and (10^5) operations. With that size, an (O(nq)) solution can perform as many as (10^{10}) elementary operations, which is far beyond what a 1 second time limit allows. An (O(n^2)) preprocessing step is also impossible. We need operations that are effectively constant time, or very close to it, for each query.

There are several cases where a careless implementation can give the wrong result. A student can be merged into a group that was itself previously merged with another group. For example:

```
3 3
Ana
Bob
Cat
1 Ana Bob
1 Bob Cat
2 Ana Cat
```

The correct output is:

```
yes
```

A solution that only remembers the most recent partner of each student could incorrectly answer `no`, because Ana was never directly merged with Cat. Team membership is transitive, so the whole connected component matters.

A type 1 query can also involve two students who are already in the same team:

```
2 2
Ana
Bob
1 Ana Bob
1 Ana Bob
```

There is no second change to make. A careless merge implementation that assumes the roots are different might corrupt its data structure if it does not handle this case.

Finally, a query can refer to students whose teams have very different sizes:

```
4 2
Ana
Bob
Cat
Dan
1 Ana Bob
2 Cat Dan
```

The answer is `no`, because neither Cat nor Dan has been connected to the other. A solution that accidentally treats unrelated indices as connected because of default parent values can fail here. Every student must begin as the root of its own component.

## Approaches

The most direct approach is to explicitly store the members of every team. Initially each team contains one student. When a merge asks us to combine the teams of (x) and (y), we can take every student from one team and change its team identifier to the identifier of the other team. A type 2 query then compares the two stored team identifiers.

This is correct because after every merge, every student in the resulting team receives the same identifier. The problem is the amount of work required by a merge. In the worst case, a team can contain (10^5) students, and a long sequence of queries can repeatedly force us to inspect a large team. With (10^5) queries, the straightforward implementation can reach (10^5 \times 10^5 = 10^{10}) student updates.

The brute-force method works because the only information a query really needs is whether two students have the same component identifier. The failure comes from physically maintaining that information for every member after every merge. We need a representation where joining two teams changes only a small amount of stored information, regardless of how many students are already inside the teams.

The key observation is that teams form disjoint connected components. A student does not need to know every other student in its team. It only needs to lead us to a representative of that team. If two students eventually reach the same representative, they are in the same component.

This is exactly the setting for a disjoint set union structure, also called DSU or union-find. Each component is represented by a root. A merge joins two roots instead of rewriting every member of either component. Path compression makes future searches very short, while union by size or rank prevents the internal trees from becoming unnecessarily deep.

With both optimizations, each operation takes amortized (O(\alpha(n))) time, where (\alpha) is the inverse Ackermann function and is effectively constant for all practical input sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nq)) worst case | (O(n)) | Too slow |
| DSU with path compression and union by size | (O((n+q)\alpha(n))) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Assign every student an integer ID from (0) to (n-1), using a dictionary from name to ID. Integer IDs make the DSU arrays compact and avoid repeatedly storing or comparing strings inside the data structure.
2. Create a `parent` array where `parent[i] = i` for every student. Initially each student is the only member of its team, so every student is its own representative.
3. Create a `size` array initialized to (1). The value records how many students belong to the component represented by each root. It will be used to decide which root should become the parent during a merge.
4. For a type 1 query, convert both names to their integer IDs and find their roots with `find`. If the roots are equal, the students are already in the same team, so the operation changes nothing.
5. If the roots differ, compare the component sizes and make the smaller component's root point to the larger component's root. Add the smaller size to the larger root's size. Attaching the smaller tree below the larger one keeps the DSU trees shallow.
6. For a type 2 query, find the roots of both students. Print `yes` if the roots are equal and `no` otherwise. The roots are the representatives of their current teams, so equality of roots is exactly the condition that the students belong to the same team.
7. In `find`, follow parent pointers until reaching a vertex that is its own parent. While returning, replace each visited student's parent with that root. This is path compression, and it makes future queries involving those students much faster.

### Why it works

The invariant is that every DSU component represents exactly one current team, and every student in that team eventually reaches the same root. Initially this is true because every student is alone. A merge only connects two different roots, so it combines exactly the two corresponding teams into one component without connecting unrelated teams. Path compression changes only the internal representation of a component, not which vertices belong to it. Consequently, two students have the same root exactly when their teams have been joined through some sequence of type 1 operations, so every type 2 answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())

    name_to_id = {}
    for i in range(n):
        name = input().strip()
        name_to_id[name] = i

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []

    for _ in range(q):
        t, sx, sy = input().split()
        x = name_to_id[sx]
        y = name_to_id[sy]

        rx = find(x)
        ry = find(y)

        if t == '1':
            if rx == ry:
                continue

            if size[rx] < size[ry]:
                rx, ry = ry, rx

            parent[ry] = rx
            size[rx] += size[ry]

        else:
            out.append("yes" if rx == ry else "no")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The dictionary is built first because all later queries identify students by name. Each name receives one stable integer ID, so the DSU never has to operate directly on strings.

The `parent` array stores the forest structure. A root satisfies `parent[root] == root`, which gives `find` a precise stopping condition. The iterative implementation avoids Python recursion depth concerns, while `parent[x] = parent[parent[x]]` performs path halving during the search.

For a union, the roots are found before changing anything. If they are already equal, the operation is ignored. Otherwise, the smaller component is attached to the larger component. The size of the new root is increased only after the parent relationship has been changed, and the size stored at the child root no longer matters.

For a query, no structure is modified intentionally beyond the path compression performed by `find`. The two roots are compared directly. There are no indexing boundary issues because IDs range from (0) through (n-1), and Python integers do not have an overflow problem.

The output is accumulated in a list and written once at the end. With up to (10^5) queries, this avoids unnecessary repeated output calls and keeps I/O comfortably within the limit.

## Worked Examples

### Sample 1

The important DSU state can be represented by the component sets. The root names below describe the components conceptually, while the implementation stores integer roots.

| Query | Operation | Components after operation | Output |
| --- | --- | --- | --- |
| 1 | `1 Naum Rebeca` | `{Naum, Rebeca}`, `{Navarro}`, `{Arnon}`, `{Matheus}`, `{Xavier}` |  |
| 2 | `2 Rebeca Naum` | unchanged | `yes` |
| 3 | `1 Matheus Xavier` | `{Matheus, Xavier}`, `{Naum, Rebeca}`, `{Navarro}`, `{Arnon}` |  |
| 4 | `1 Navarro Arnon` | `{Navarro, Arnon}`, `{Matheus, Xavier}`, `{Naum, Rebeca}` |  |
| 5 | `2 Matheus Navarro` | unchanged | `no` |
| 6 | `2 Rebeca Matheus` | unchanged | `no` |
| 7 | `1 Navarro Matheus` | `{Navarro, Arnon, Matheus, Xavier}`, `{Naum, Rebeca}` |  |
| 8 | `2 Xavier Arnon` | unchanged | `yes` |
| 9 | `2 Xavier Rebeca` | unchanged | `no` |
| 10 | `1 Rebeca Arnon` | `{Navarro, Arnon, Matheus, Xavier, Naum, Rebeca}` |  |
| 11 | `2 Naum Rebeca` | unchanged | `yes` |
| 12 | `2 Naum Matheus` | unchanged | `yes` |
| 13 | `2 Naum Xavier` | unchanged | `yes` |

The interesting part is query 10. Rebeca belongs to the component containing Naum, while Arnon belongs to the component containing Navarro, Matheus, and Xavier. The union joins those two roots, so all six students now have the same representative. The final three queries demonstrate transitivity: Naum was never directly merged with Matheus or Xavier, but all three became members of the same component.

### Sample 2

| Query | Operation | Components after operation | Output |
| --- | --- | --- | --- |
| 1 | `1 Sergio Mateus` | `{Sergio, Mateus}`, `{Cesar}`, `{Gustavo}`, `{Caio}`, `{Yu}` |  |
| 2 | `1 Cesar Yu` | `{Cesar, Yu}`, `{Sergio, Mateus}`, `{Gustavo}`, `{Caio}` |  |
| 3 | `1 Cesar Gustavo` | `{Cesar, Yu, Gustavo}`, `{Sergio, Mateus}`, `{Caio}` |  |
| 4 | `2 Cesar Sergio` | unchanged | `no` |
| 5 | `1 Caio Mateus` | `{Caio, Sergio, Mateus}`, `{Cesar, Yu, Gustavo}` |  |
| 6 | `1 Gustavo Yu` | unchanged, already same component |  |
| 7 | `2 Caio Sergio` | unchanged | `yes` |
| 8 | `2 Gustavo Sergio` | unchanged | `no` |

Query 6 is a useful edge case. Gustavo and Yu are already connected through Cesar, so the union does not create a new component. The DSU detects this because both names produce the same root. Query 7 then confirms that connecting Caio to Mateus also connects Caio to Sergio through the existing component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+q)\alpha(n))) | Building the name map takes (O(n)), and every DSU operation has amortized (O(\alpha(n))) cost. |
| Space | (O(n)) | The name map, parent array, size array, and output storage all grow linearly with the input size. |

For (n,q \le 10^5), the DSU operations are effectively constant time. The solution performs only a linear amount of preprocessing and a very small number of operations per query, so it fits comfortably within the 1 second and 256 MB limits. The maximum number of stored students and queries is also small enough for Python's dictionaries and integer arrays.

## Test Cases

The test helper below uses the same `solve` logic as the submitted program, but accepts a string and captures its output so the cases can be checked with assertions.

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, q = map(int, input().split())

    name_to_id = {}
    for i in range(n):
        name_to_id[input().strip()] = i

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []

    for _ in range(q):
        t, sx, sy = input().split()
        x = name_to_id[sx]
        y = name_to_id[sy]

        rx = find(x)
        ry = find(y)

        if t == '1':
            if rx == ry:
                continue

            if size[rx] < size[ry]:
                rx, ry = ry, rx

            parent[ry] = rx
            size[rx] += size[ry]
        else:
            out.append("yes" if rx == ry else "no")

    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample1 = """\
6 13
Navarro
Arnon
Matheus
Xavier
Rebeca
Naum
1 Naum Rebeca
2 Rebeca Naum
1 Matheus Xavier
1 Navarro Arnon
2 Matheus Navarro
2 Rebeca Matheus
1 Navarro Matheus
2 Xavier Arnon
2 Xavier Rebeca
1 Rebeca Arnon
2 Naum Rebeca
2 Naum Matheus
2 Naum Xavier
"""

assert run(sample1) == """\
yes
no
no
yes
no
yes
yes
yes""", "sample 1"

sample2 = """\
6 8
Sergio
Yu
Mateus
Cesar
Gustavo
Caio
1 Sergio Mateus
1 Cesar Yu
1 Cesar Gustavo
2 Cesar Sergio
1 Caio Mateus
1 Gustavo Yu
2 Caio Sergio
2 Gustavo Sergio
"""

assert run(sample2) == """\
no
yes
no""", "sample 2"

minimum_case = """\
2 4
Aa
Bb
2 Aa Bb
1 Aa Bb
2 Aa Bb
1 Aa Bb
"""

assert run(minimum_case) == """\
no
yes""", "minimum size and repeated union"

transitive_case = """\
5 8
Aa
Bb
Cc
Dd
Ee
1 Aa Bb
1 Cc Dd
2 Aa Dd
1 Bb Cc
2 Aa Dd
2 Bb Dd
1 Aa Dd
2 Aa Ee
"""

assert run(transitive_case) == """\
no
yes
yes
no""", "transitive connectivity"

repeated_queries_case = """\
4 7
Aa
Bb
Cc
Dd
2 Aa Bb
2 Cc Dd
1 Aa Bb
2 Aa Bb
1 Aa Bb
1 Cc Dd
2 Cc Dd
"""

assert run(repeated_queries_case) == """\
no
no
yes
yes""", "repeated queries and no-op unions"

n = 100000
names = [f"A{i}" for i in range(n)]
maximum_case = [f"{n} 3"]
maximum_case.extend(names)
maximum_case.append(f"1 {names[0]} {names[-1]}")
maximum_case.append(f"2 {names[0]} {names[-1]}")
maximum_case.append(f"2 {names[1]} {names[-2]}")
maximum_case = "\n".join(maximum_case) + "\n"

assert run(maximum_case) == """\
yes
no""", "maximum size"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `yes`, `no`, `no`, `yes`, `no`, `yes`, `yes`, `yes` | Multiple merges, transitive connectivity, and merging two large components |
| Sample 2 | `no`, `yes`, `no` | A no-op union and separate components |
| Minimum case | `no`, `yes` | Minimum number of students and repeated union of an existing component |
| Transitive case | `no`, `yes`, `yes`, `no` | Connectivity through several intermediate students |
| Repeated queries case | `no`, `no`, `yes`, `yes` | Queries before and after unions, including repeated unions |
| Maximum case | `yes`, `no` | (10^5) students and boundary IDs at both ends of the arrays |

## Edge Cases

A chain of unions tests whether the solution understands connectivity rather than direct relationships. For example:

```
3 3
Ana
Bob
Cat
1 Ana Bob
1 Bob Cat
2 Ana Cat
```

After the first union, Ana and Bob have the same root. After the second union, Bob's component is joined with Cat's component. Ana and Cat consequently reach the same root, so the output is:

```
yes
```

The DSU handles this without explicitly connecting every pair of students.

A repeated union must not create a new component or corrupt its size. Consider:

```
2 4
Aa
Bb
1 Aa Bb
1 Aa Bb
2 Aa Bb
2 Bb Aa
```

The first union creates one component. The second union finds identical roots and returns immediately. Both queries then compare the same root and produce:

```
yes
yes
```

A query made before any union must distinguish separate singleton components. For example:

```
2 1
Aa
Bb
2 Aa Bb
```

Both students are initially their own roots, so the roots differ and the output is:

```
no
```

This checks the initialization of `parent`, since assigning every student an accidental common default root would incorrectly produce `yes`.

The maximum-size boundary case uses the first and last student IDs:

```
4 3
Aaaa
Bbbb
Cccc
Dddd
1 Aaaa Dddd
2 Aaaa Dddd
2 Bbbb Dddd
```

After the first operation, only `Aaaa` and `Dddd` share a component. The output is:

```
yes
no
```

The implementation never assumes that a student's ID is related to its name or position beyond the dictionary mapping, so students at both ends of the ID range are handled identically.

A final subtle case is when a union connects two components that already contain many students:

```
5 6
Aa
Bb
Cc
Dd
Ee
1 Aa Bb
1 Cc Dd
1 Aa Cc
2 Bb Dd
2 Aa Dd
2 Bb Ee
```

After the third union, the first four students belong to one component. Both `Bb Dd` and `Aa Dd` therefore produce `yes`, while `Bb Ee` produces `no`. The DSU achieves this by changing one root pointer rather than updating all four students individually, which is the central reason the method scales to (10^5) operations.
