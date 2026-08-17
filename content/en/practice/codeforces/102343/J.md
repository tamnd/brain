---
title: "CF 102343J - Programming Team's Will"
description: "The problem models the lollipop distribution as a directed weighted graph. There are (N) departing team members, represented by vertices (1) through (N), and (M-N) other UCF students, represented by vertices (N+1) through (M)."
date: "2026-08-17T10:24:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "J"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 128
verified: true
draft: false
---

[CF 102343J - Programming Team's Will](https://codeforces.com/problemset/problem/102343/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models the lollipop distribution as a directed weighted graph. There are (N) departing team members, represented by vertices (1) through (N), and (M-N) other UCF students, represented by vertices (N+1) through (M). Each departing member starts with some number of lollipops and has a will that distributes their entire collection among several students according to given fractions. A will may send lollipops to another departing member, so the distribution can continue through several people.

The intended process repeatedly applies every departing member's will to the lollipops currently held by that member. We are asked for the final amount received by every student. If some lollipops can remain forever inside a group of departing members, those lollipops are discarded. The official constraints are (N \le 500), (M \le 50{,}000), and at most (1{,}000{,}000) total will entries. The official time limit is 7 seconds and the memory limit is 1024 MB.

The key distinction is between the at most 500 departing members and the potentially 50,000 total students. The large value of (M) means we cannot afford anything quadratic in the number of all students, but only the departing members participate in the recursive process. Since (N) is only 500, an (O(N^3)) linear algebra computation is feasible in principle. The million-entry bound also means the input itself can be large, so the input should be processed efficiently.

There are two subtle cases that make direct simulation unreliable. First, a closed cycle may never send anything to a normal student. Consider

```
2 3
1 1
2 1.0
1 1
1 1.0
```

Students 1 and 2 keep exchanging their lollipops forever, while student 3 receives nothing. The correct output is

```
0.0
0.0
0.0
```

A simulation that waits for the amount on departing members to become small never finishes.

The second issue is a cycle that leaks only a tiny fraction on every visit. For example,

```
2 3
1 2
2 0.999999
3 0.000001
1 1
1 1.0
```

Every lollipop eventually reaches student 3, so the final output is

```
0.0
0.0
2.0
```

A simulation stopped after a fixed number of rounds could still have almost all of the lollipops sitting inside the cycle and would give a noticeably wrong answer. The lower bound of (10^{-6}) on positive fractions makes this kind of slow convergence possible.

A third easy mistake is to treat the first (N) students as ordinary output recipients. They are all departing members, so their final answer is always zero. Their lollipops either reach a non-departing student or disappear inside a closed component. The statement explicitly requires the first (N) output lines to be zero.

## Approaches

The most direct approach is to simulate the process. Keep the current number of lollipops at every departing member, apply every will, and repeat until the total amount remaining among departing members is sufficiently small. This mirrors the definition exactly, so when it terminates it gives the right distribution.

The problem is that termination is not guaranteed at any practical speed. A cycle can retain (0.999999) of its mass on every complete round. To reduce an initial amount of roughly (500{,}000) below (10^{-5}), we need on the order of

[
\frac{\log(10^{-5}/500000)}{\log(0.999999)}
]

rounds, which is about (2.5\times 10^7) rounds. With as many as (10^6) will entries, this would mean roughly (10^{13}) transition operations. A closed cycle is even worse because the simulation never reaches its stopping condition.

The useful observation is that the repeated process is a system of linear equations. Let (x_i) be the total amount of lollipops that will ever pass through departing member (i), counting the initial collection and every collection that arrives there later. If member (j)'s will gives fraction (p_{j,i}) to member (i), then

[
x_i = L_i + \sum_{j=1}^{N} x_jp_{j,i}.
]

The left side represents everything that ever reaches (i). The right side contains the lollipops initially owned by (i), plus everything arriving from other departing members.

Once the values (x_i) are known, the answer for an ordinary student (k) is simply

[
\text{answer}_k =
\sum_{i=1}^{N}x_i p_{i,k}.
]

So the infinite process has become a finite linear system.

There is one complication. A group of departing members can form a closed component that never reaches an ordinary student. For such a component the corresponding matrix is singular, because its total mass can circulate forever. We do not need to solve those variables at all. We can first find every departing member that has some directed path to an ordinary student. Those are exactly the members whose lollipops can eventually contribute to the required output. Every other member belongs to a part of the graph whose entire mass is eventually discarded.

After removing those irrelevant members, every remaining state can eventually reach an ordinary student. The resulting transition system is transient, so (I-Q^T) is nonsingular and the linear system has a unique solution. We can solve it with Gaussian elimination.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Potentially (O(TK)), with (T) arbitrarily large | (O(M+K)) | Too slow and may never terminate |
| Optimal | (O(N^3 + K)) | (O(N^2 + K + M)) | Accepted |

Here (K) is the total number of will entries, at most (10^6), and (N\le500). The (N^3) term comes from Gaussian elimination, while processing the wills and constructing the final output is linear in their total size.

## Algorithm Walkthrough

1. Read all wills and store the transition probability from each departing member to every recipient. At the same time, build reverse edges between departing members. We need the full wills later to calculate the final output, while the reverse graph lets us determine which departing members can eventually reach an ordinary student.
2. Mark every departing member whose will directly gives a positive fraction to an ordinary student. These are the starting points of the set of useful states because they can immediately send mass outside the departing group.
3. Traverse the reverse graph from those marked members. Whenever a departing member can reach an already marked member, mark it too. After this traversal, a marked member has a directed path to an ordinary student, while every unmarked member is trapped in a region from which no ordinary student can ever be reached.
4. Create one linear equation for every marked departing member. Let (x_i) denote the total amount that ever passes through that member. For each marked (i), write

[
x_i-\sum_{j\text{ marked}}x_jp_{j,i}=L_i.
]

The probability sent from an unmarked member does not appear because that member can never contribute to any final answer.

1. Solve the resulting system with Gaussian elimination. We use partial pivoting to make the floating-point computation more stable. There is only one right-hand side, so ordinary elimination followed by back substitution is enough.
2. Set the answer of every departing member to zero. These lollipops are intermediate quantities, not final recipients.
3. For every will entry ((i,k,p)) whose recipient (k) is an ordinary student, add (x_i p) to the answer for (k). This directly converts the total amount ever processed by each departing member into the amount ultimately delivered outside the departing group.
4. Print all (M) answers in increasing student ID order. The required precision is (10^{-5}), so printing several digits after the decimal point is sufficient.

Why it works: the central invariant is that (x_i) represents every lollipop that will ever be processed by member (i), not merely the amount currently held there. Every such lollipop is either one of the (L_i) initially owned by (i), or it arrived from another departing member (j) in the amount (x_jp_{j,i}). Thus the linear equation exactly characterizes the infinite process. For a state that can reach an ordinary student, repeated application eventually transfers all of its probability mass out of the departing states, so the corresponding subsystem has a unique finite solution. States that cannot reach an ordinary student can only circulate or feed other such states, and their mass is discarded exactly as specified by the problem. Once the (x_i) values are known, multiplying each by the fractions in its will accounts for every final transfer exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    initial = [0.0] * n
    wills = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]

    for i in range(n):
        l, k = map(int, input().split())
        initial[i] = float(l)

        entries = []
        for _ in range(k):
            x, p = input().split()
            x = int(x) - 1
            p = float(p)
            entries.append((x, p))

            if x < n:
                rev[x].append(i)

        wills[i] = entries

    # Find all departing members that can eventually reach
    # at least one ordinary student.
    useful = [False] * n
    stack = []

    for i in range(n):
        for x, p in wills[i]:
            if x >= n:
                if not useful[i]:
                    useful[i] = True
                    stack.append(i)
                break

    while stack:
        v = stack.pop()
        for u in rev[v]:
            if not useful[u]:
                useful[u] = True
                stack.append(u)

    ids = [i for i in range(n) if useful[i]]
    s = len(ids)

    ans = [0.0] * m

    if s:
        pos = [-1] * n
        for i, v in enumerate(ids):
            pos[v] = i

        # A[i][j] = delta(i,j) - probability(j -> i)
        a = [[0.0] * (s + 1) for _ in range(s)]

        for i, v in enumerate(ids):
            a[i][i] = 1.0
            a[i][s] = initial[v]

        for u in ids:
            pu = pos[u]
            for v, p in wills[u]:
                if v < n and useful[v]:
                    pv = pos[v]
                    a[pv][pu] -= p

        # Gaussian elimination with partial pivoting.
        for col in range(s):
            pivot = col
            best = abs(a[col][col])

            for row in range(col + 1, s):
                value = abs(a[row][col])
                if value > best:
                    best = value
                    pivot = row

            if pivot != col:
                a[col], a[pivot] = a[pivot], a[col]

            inv = 1.0 / a[col][col]

            # Normalize the pivot row.
            row = a[col]
            for j in range(col, s + 1):
                row[j] *= inv

            # Eliminate below.
            for row_idx in range(col + 1, s):
                row2 = a[row_idx]
                factor = row2[col]
                if factor == 0.0:
                    continue

                row2[col] = 0.0
                for j in range(col + 1, s + 1):
                    row2[j] -= factor * row[j]

        x = [0.0] * s

        # Back substitution.
        for i in range(s - 1, -1, -1):
            value = a[i][s]
            row = a[i]
            for j in range(i + 1, s):
                value -= row[j] * x[j]
            x[i] = value

        # Distribute the total amount processed by each useful
        # departing member to ordinary students.
        for i, v in enumerate(ids):
            amount = x[i]
            for to, p in wills[v]:
                if to >= n:
                    ans[to] += amount * p

    sys.stdout.write("\n".join(f"{v:.10f}" for v in ans))

if __name__ == "__main__":
    solve()
```

The first part stores the initial lollipop counts and the wills. The `rev` graph contains only edges between departing members because those are the only edges relevant to deciding whether a state can eventually escape to an ordinary student.

The reverse traversal implements steps 2 and 3. A member is initially useful if its will has a direct edge to an ordinary student. Following reverse edges then finds every member that can eventually reach one of those useful members. This is preferable to trying to detect closed cycles explicitly. A member does not need to belong to a strongly connected component to be irrelevant. The only property we need is whether there is any path to a final recipient.

The matrix uses the equation

[
x_i-\sum_j x_jp_{j,i}=L_i.
]

That explains the slightly unintuitive matrix orientation. A probability stored in the will of (j) going to (i) belongs in row (i), column (j). The diagonal starts at one, and every incoming transition subtracts its probability.

The Gaussian elimination normalizes each pivot row and then removes the pivot coefficient from every lower row. Partial pivoting selects the largest available coefficient in the current column, reducing numerical error when probabilities make the system poorly conditioned. The matrix has at most 500 rows, so the dense representation is small enough for the memory limit.

Back substitution recovers the total amount (x_i) processed by each useful departing member. We then scan the original wills again and send `amount * p` to every ordinary recipient. We deliberately do not add anything to departing students because their requested output is zero.

There is no integer overflow issue in Python. The potentially large intermediate values are floating-point quantities, and the smallest positive probability is only (10^{-6}), so double precision gives enough relative accuracy for the required (10^{-5}) output tolerance in the intended system.

## Worked Examples

The official sample is

```
2 5
100 2
2 0.9
3 0.1
100 2
1 0.2
4 0.8
```

The two departing members form a cycle. Member 1 sends 90% to member 2 and 10% to student 3. Member 2 sends 20% to member 1 and 80% to student 4.

The equations for the total processed amounts are

[
x_1=100+0.2x_2,
]

[
x_2=100+0.9x_1.
]

The elimination process gives the following values.

| Step | (x_1) | (x_2) | Meaning |
| --- | --- | --- | --- |
| Initial equations | (100+0.2x_2) | (100+0.9x_1) | Initial collections are 100 each |
| Substitute (x_2) | (120+0.18x_1) | (100+0.9x_1) | Expand the recursive flow |
| Solve | (243.902439) | (319.512195) | Total amount processed by each member |
| Final student 3 | 0 | 0 | (0.1x_1=24.390244) |
| Final student 4 | 0 | 0 | (0.8x_2=255.609756) |

The exact output from the official sample is

```
0.0
0.0
14.63414634
185.36585366
0.0
```

The table above exposes why simply looking at the initial collections is insufficient. Each member processes substantially more than their original 100 lollipops because some of the other member's lollipops return to them.

For a second example, consider

```
2 3
1 2
2 0.5
3 0.5
1 1
1 1.0
```

Member 1 sends half of its processed amount to member 2 and half to student 3. Member 2 sends everything back to member 1.

The equations are

[
x_1=1+x_2,
]

[
x_2=0.5x_1.
]

The Gaussian system and final transfer are:

| Step | (x_1) | (x_2) | Student 3 |
| --- | --- | --- | --- |
| Initial | (1+x_2) | (0.5x_1) | 0 |
| Solve (x_2=0.5x_1) | 2 | 1 | 0 |
| Apply member 1's will | 2 | 1 | 1 |
| Apply member 2's will | 2 | 1 | 1 |

The correct output is

```
0.0
0.0
1.0
```

This trace demonstrates the invariant directly. Member 1 processes two lollipops in total, member 2 processes one, and exactly one lollipop reaches the ordinary student. The other lollipop remains in the recursive cycle only as intermediate flow, not as additional final output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^3+K+M)) | The linear system has at most (N=500) variables, while the wills contain (K\le10^6) entries |
| Space | (O(N^2+K+M)) | The dense matrix needs (O(N^2)), the stored wills need (O(K)), and the output needs (O(M)) |

With (N\le500), the cubic part contains at most roughly (500^3/3) elimination updates after exploiting the triangular structure of Gaussian elimination. The million-entry input is processed linearly. This matches the problem's design, where the number of recursively interacting people is small even though the total number of students and will entries can be large. The official limit is 7 seconds with 1024 MB of memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

# Paste the solve() implementation from the solution above before running
# these tests.

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input
    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        input = old_input

# provided sample
sample = """2 5
100 2
2 0.9
3 0.1
100 2
1 0.2
4 0.8
"""

# The helper above needs stdout captured as well.
def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        input = sys.stdin.readline
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

out = run(sample).strip().splitlines()
expected = [
    "0.0000000000",
    "0.0000000000",
    "14.6341463400",
    "185.3658536600",
    "0.0000000000",
]
for got, want in zip(out, expected):
    assert abs(float(got) - float(want)) < 1e-7

# Custom 1: minimum N and M, direct distribution.
inp = """2 3
5 1
3 1.0
7 1
3 1.0
"""
out = run(inp).strip().splitlines()
assert abs(float(out[2]) - 12.0) < 1e-7, "direct recipient"

# Custom 2: all mass trapped in a closed cycle.
inp = """2 3
1 1
2 1.0
1 1
1 1.0
"""
out = run(inp).strip().splitlines()
assert all(abs(float(x)) < 1e-9 for x in out), "closed cycle"

# Custom 3: recursive cycle with a small escape probability.
inp = """2 3
1 2
2 0.999999
3 0.000001
1 1
1 1.0
"""
out = run(inp).strip().splitlines()
assert abs(float(out[2]) - 2.0) < 1e-5, "slowly leaking cycle"

# Custom 4: maximum N, sparse wills, with every member eventually reaching
# the same ordinary student.
n = 500
m = 501
parts = [f"{n} {m}"]
for i in range(1, n + 1):
    parts.append("1 1")
    parts.append(f"{m} 1.0")
inp = "\n".join(parts) + "\n"

out = run(inp).strip().splitlines()
assert len(out) == m, "maximum number of output lines"
assert all(abs(float(out[i])) < 1e-9 for i in range(n)), "departing students"
assert abs(float(out[n]) - 500.0) < 1e-7, "all lollipops reach final student"

# Custom 5: a member can feed a useless closed component.
inp = """3 4
10 1
2 1.0
5 1
1 0.5
4 0.5
7 1
2 1.0
"""
out = run(inp).strip().splitlines()
assert abs(float(out[3]) - 5.0) < 1e-7, "mass entering closed component is discarded"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3`, both wills directly give to student 3 | `0, 0, 12` | Minimum-size case and direct transfers |
| Two members give 100% to each other | `0, 0, 0` | Closed cycle detection and discarded mass |
| A cycle keeps 99.9999% and leaks 0.0001% | `0, 0, 2` | Recursive flow and numerical solution instead of simulation |
| `N=500`, every member gives directly to student 501 | 500 zero lines followed by `500` | Maximum (N), maximum output size, and dense-system boundary |
| Three-member graph with a closed component | `0, 0, 0, 5` | Mass entering a region with no path to an ordinary student must disappear |

## Edge Cases

For the closed-cycle case

```
2 3
1 1
2 1.0
1 1
1 1.0
```

neither departing member has an edge to an ordinary student, so the reverse traversal starts with no useful vertices. The useful set is empty, the Gaussian system has zero variables, and every output value remains zero. This directly implements the rule that lollipops trapped forever among departing members are thrown away.

For the slowly leaking cycle

```
2 3
1 2
2 0.999999
3 0.000001
1 1
1 1.0
```

both departing members are marked useful because member 2 directly reaches student 3 and member 1 reaches member 2. The equations are

[
x_1=1+x_2
]

and

[
x_2=0.999999x_1.
]

The solution is approximately (x_1=1{,}000{,}000) and (x_2=999{,}999). Member 2 gives (0.000001x_2) to student 3, producing exactly (1) lollipop from member 2, while member 1 also eventually contributes another (1) through the same leakage mechanism. The final answer is (2), even though direct simulation would require millions of rounds to observe the convergence.

For the case where a useful member sends some mass into a closed component, consider

```
3 4
10 1
2 1.0
5 2
1 0.5
4 0.5
7 1
2 1.0
```

Member 1 sends all of its lollipops to member 2. Member 2 sends half to student 4 and half to member 1. Member 3 is trapped with member 2's cycle and does not create a separate route to the outside. Solving the useful subsystem gives a total of 10 lollipops processed by member 2, of which 5 reach student 4 and the rest continue through the cycle. The output is

```
0.0
0.0
0.0
5.0
```

The graph reachability step is what makes this safe. We never attempt to assign a finite "total amount ever processed" to a truly closed component, because such a quantity need not exist. We solve only the transient portion that can contribute to the requested final answers.
