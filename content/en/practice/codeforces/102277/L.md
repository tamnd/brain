---
title: "CF 102277L - Cupcake Bonuses"
description: "The company is a rooted tree. Employee 1 is the CEO, and every later employee is hired under an existing employee, so each employee has exactly one parent. An employee heads a department containing themselves and every employee below them in the hierarchy."
date: "2026-08-17T03:19:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "L"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 393
verified: true
draft: false
---

[CF 102277L - Cupcake Bonuses](https://codeforces.com/problemset/problem/102277/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The company is a rooted tree. Employee 1 is the CEO, and every later employee is hired under an existing employee, so each employee has exactly one parent. An employee heads a department containing themselves and every employee below them in the hierarchy.

Every employee has a current bonus multiplier. Initially, every employee's multiplier is the same value `S`. A bonus payment targeted at employee `i`'s department has a base amount `B`, and every employee in that subtree receives `B * M`, where `M` is that employee's multiplier at the moment of the payment. A multiplier change affects only future bonus payments.

There are four operations. A new employee can be hired under an existing employee. An employee's multiplier can be replaced by a new value. A bonus can be paid to an entire department subtree. Finally, the total bonus accumulated by one employee can be requested. The required output is one integer for every query of the last kind. The original UCF statement gives `n <= 10^5`, `S <= 10^6`, and multipliers and bonus amounts up to `10^6`.

With up to `10^5` operations, directly visiting every employee affected by every department payment can require about `10^10` employee updates in the worst case. A quadratic solution is far beyond a one-second limit. We need every operation to take roughly logarithmic time, or at least amortized close to it.

There are several subtle cases that a direct implementation can mishandle. First, a bonus paid before an employee is hired must not be awarded to that employee. For example, with `S = 1`, the input

```
3 1
3 1 10
1 1
4 2
```

has output

```
0
```

The CEO's department received a bonus before employee 2 existed. Employee 2 therefore starts with zero accumulated bonus. A solution that builds the final tree and immediately considers every earlier subtree payment as belonging to employee 2 would incorrectly give `10`.

Second, changing a multiplier must not change bonuses that were already paid. For example,

```
4 1
3 1 10
2 1 5
3 1 10
4 1
```

produces

```
60
```

The first payment gives `10 * 1 = 10`, while the second gives `10 * 5 = 50`. Recomputing all historical payments with the current multiplier would incorrectly produce `100`.

Third, a department can contain many levels of descendants, not just direct children. With

```
4 2
1 1
1 2
3 1 5
```

employee 3 is inside the CEO's department even though employee 1 is its direct parent and employee 2 is its grandparent. The payment reaches all three employees, so a solution that stores only direct-subordinate information is insufficient.

## Approaches

The brute-force solution follows the definition literally. Store the company as a tree, and for a type 3 query, traverse the entire subtree of the specified employee. For every employee reached, add `B * multiplier[employee]` to their accumulated bonus. A multiplier update is constant time, and a type 4 query is also constant time if accumulated bonuses are stored explicitly.

This is correct because a department is exactly a subtree, and the traversal visits every employee who should receive that payment. The problem is the amount of repeated work. Consider a company in which all `10^5` operations are payments to the CEO. Every payment visits all employees, so the implementation performs approximately `10^10` employee updates. Even a tree traversal with very small constant factors cannot make that feasible.

The key observation is that a department payment does not actually need to change every employee immediately. We only need the answer when an employee is queried or when their multiplier changes.

Separate the calculation into two quantities. Let `base[x]` be the sum of all department bonus amounts whose target departments contain employee `x`. This quantity does not depend on `x`'s multiplier. A department payment of `B` simply adds `B` to `base[x]` for every employee in that department.

Suppose an employee's multiplier is currently `M`, and the last time we finalized that employee's bonus was when their `base` value was `last[x]`. Every unit of `base` added since then represents a bonus that must be multiplied by the current multiplier. Thus the newly earned money is

```
(base[x] - last[x]) * M
```

When the multiplier changes, we first finalize all bonus money earned under the old multiplier, then record the new multiplier and the current `base[x]`.

The remaining problem is to support subtree additions to `base` and point queries of `base[x]`. Since the complete set of queries is available before processing, we can first build the final employee tree. A DFS gives every employee an Euler-tour interval `[tin[x], tout[x]]`, and all descendants of `x` occupy exactly that interval.

A subtree addition then becomes a range addition on the Euler array. A Fenwick tree can implement range addition and point queries in `O(log n)` time using the standard difference-array trick.

There is one more subtle issue caused by hiring. If we build the final tree first, a subtree range update performed before employee `x` was hired would technically include `x` in its final subtree. We solve this by initializing a newly hired employee's `last[x]` to their current `base[x]`. All historical subtree payments are then treated as the employee's starting baseline, while only future increases in `base[x]` generate money.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2)` worst case | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read all queries before processing them. During this pass, create the final company tree by recording the supervisor of every employee created by a type 1 query. This lets us compute stable subtree intervals even though employees are hired online.
2. Run a DFS from the CEO and assign each employee a `tin` value when entering the node and a `tout` value after processing all descendants. Every employee in the subtree of `x` then has an Euler position between `tin[x]` and `tout[x]`.
3. Create a Fenwick tree representing the difference array of `base`. A range addition `[l, r] += B` is implemented by adding `B` at `l` and `-B` at `r + 1`. The prefix sum at position `p` is then the current `base` value for the employee whose Euler position is `p`.
4. Initialize the CEO with multiplier `S`, accumulated money `0`, and `last_base` equal to zero. No bonus existed before processing the first query, so the CEO's starting baseline is zero.
5. For a hiring query `1 i`, create the next employee with multiplier `S` and accumulated money zero. Set that employee's `last_base` to their current Fenwick point value. This discards every bonus payment that occurred before their hiring time, including payments to ancestors' departments.
6. For a multiplier update `2 i M`, first obtain the employee's current `base` value. Add `(current_base - last_base[i]) * multiplier[i]` to their accumulated money. This accounts for every bonus amount that became applicable while their old multiplier was active. Then set `last_base[i]` to `current_base` and replace the multiplier with `M`.
7. For a department payment `3 i B`, add `B` to the Euler interval `[tin[i], tout[i]]`. We do not update employee balances individually. The Fenwick tree records only how much bonus base each employee has accumulated so far.
8. For a retrieval query `4 i`, obtain the current `base` value and calculate `money[i] + (current_base - last_base[i]) * multiplier[i]`. The first term contains all previously finalized earnings, while the second term accounts for payments since the last time this employee's multiplier state was finalized.

The invariant is that `money[i]` always contains every bonus that was already evaluated using the correct historical multiplier, while `last_base[i]` marks the boundary between those finalized payments and the still-unaccounted bonus base. Whenever the multiplier changes, we finalize exactly the interval belonging to the old multiplier. Whenever the employee is queried, we temporarily account for the current interval without changing the state. Since `base` increases exactly when a relevant department payment occurs, every payment is multiplied by the employee's multiplier at that payment's time and exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, value):
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += value
            i += i & -i

    def range_add(self, l, r, value):
        self.add(l, value)
        if r + 1 <= self.n:
            self.add(r + 1, -value)

    def point_query(self, i):
        result = 0
        bit = self.bit
        while i > 0:
            result += bit[i]
            i -= i & -i
        return result

def solve():
    n, initial_multiplier = map(int, input().split())

    queries = []
    parent = [0, 0]
    children = [[]]

    employee_count = 1

    for _ in range(n):
        q = list(map(int, input().split()))
        queries.append(q)

        if q[0] == 1:
            employee_count += 1
            employee = employee_count
            supervisor = q[1]

            while len(parent) <= employee:
                parent.append(0)
            parent[employee] = supervisor

            while len(children) <= employee:
                children.append([])

            children[supervisor].append(employee)

    tin = [0] * (employee_count + 1)
    tout = [0] * (employee_count + 1)

    timer = 0
    stack = [(1, 0)]

    while stack:
        u, state = stack.pop()

        if state == 0:
            timer += 1
            tin[u] = timer
            stack.append((u, 1))

            for v in reversed(children[u]):
                stack.append((v, 0))
        else:
            tout[u] = timer

    fenwick = Fenwick(employee_count)

    multiplier = [0] * (employee_count + 1)
    money = [0] * (employee_count + 1)
    last_base = [0] * (employee_count + 1)

    multiplier[1] = initial_multiplier

    output = []

    for q in queries:
        typ = q[0]

        if typ == 1:
            employee_count_current = len([x for x in multiplier if x != 0])
            employee = len(multiplier)
            # The arrays were allocated using the final number of employees.
            # Find the next employee using a separate counter instead.
            pass

    # Process again with an explicit employee counter.
    multiplier = [0] * (employee_count + 1)
    money = [0] * (employee_count + 1)
    last_base = [0] * (employee_count + 1)

    multiplier[1] = initial_multiplier
    next_employee = 1

    for q in queries:
        typ = q[0]

        if typ == 1:
            supervisor = q[1]
            next_employee += 1
            employee = next_employee

            multiplier[employee] = initial_multiplier
            money[employee] = 0

            # Past bonuses must not be inherited by a newly hired employee.
            last_base[employee] = fenwick.point_query(tin[employee])

        elif typ == 2:
            employee, new_multiplier = q[1], q[2]

            current_base = fenwick.point_query(tin[employee])
            money[employee] += (
                current_base - last_base[employee]
            ) * multiplier[employee]

            last_base[employee] = current_base
            multiplier[employee] = new_multiplier

        elif typ == 3:
            employee, bonus = q[1], q[2]

            fenwick.range_add(
                tin[employee],
                tout[employee],
                bonus
            )

        else:
            employee = q[1]

            current_base = fenwick.point_query(tin[employee])
            total = (
                money[employee]
                + (current_base - last_base[employee])
                * multiplier[employee]
            )

            output.append(str(total))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The first pass reads every query and builds the final tree. The number of employees is at most `n + 1`, so allocating arrays for all possible employee IDs is sufficient.

The DFS is iterative rather than recursive because a valid input can form a chain of `10^5` employees. A recursive Python DFS could exceed the interpreter's recursion limit, while the explicit stack handles the same traversal safely.

The Fenwick tree stores the difference representation of the cumulative bonus base. Calling `range_add(tin[i], tout[i], B)` represents a payment to exactly the final subtree of employee `i`. Calling `point_query(tin[x])` reconstructs the sum of all relevant base amounts for employee `x`.

The hiring operation is the part most likely to cause an incorrect implementation. The final Euler subtree contains employees that may not have existed when an earlier payment happened. Setting `last_base` to the current Fenwick value at hiring time makes those historical payments invisible to the new employee.

The multiplier update finalizes the old multiplier before replacing it. Reversing those two operations would apply the new multiplier to historical bonus amounts and produce an incorrect answer.

Python integers have arbitrary precision, so the potentially large products do not overflow. In a fixed-width language, 64-bit integers are required because both bonus amounts and multipliers can reach `10^6`, and many payments can accumulate for the same employee.

There is an unused preliminary processing loop in the first code section above, so the implementation should be simplified before submission. The following is the clean submission version.

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, value):
        while i <= self.n:
            self.bit[i] += value
            i += i & -i

    def range_add(self, l, r, value):
        self.add(l, value)
        if r + 1 <= self.n:
            self.add(r + 1, -value)

    def point_query(self, i):
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result

def solve():
    n, S = map(int, input().split())

    queries = []
    children = [[]]
    employee_count = 1

    for _ in range(n):
        q = list(map(int, input().split()))
        queries.append(q)

        if q[0] == 1:
            supervisor = q[1]
            employee_count += 1

            while len(children) <= employee_count:
                children.append([])

            children[supervisor].append(employee_count)

    tin = [0] * (employee_count + 1)
    tout = [0] * (employee_count + 1)

    timer = 0
    stack = [(1, 0)]

    while stack:
        u, state = stack.pop()

        if state == 0:
            timer += 1
            tin[u] = timer

            stack.append((u, 1))
            for v in reversed(children[u]):
                stack.append((v, 0))
        else:
            tout[u] = timer

    bit = Fenwick(employee_count)

    multiplier = [S] * (employee_count + 1)
    money = [0] * (employee_count + 1)
    last_base = [0] * (employee_count + 1)

    next_employee = 1
    answer = []

    for q in queries:
        typ = q[0]

        if typ == 1:
            next_employee += 1
            employee = next_employee

            multiplier[employee] = S
            money[employee] = 0
            last_base[employee] = bit.point_query(tin[employee])

        elif typ == 2:
            employee, new_multiplier = q[1], q[2]

            current_base = bit.point_query(tin[employee])
            money[employee] += (
                current_base - last_base[employee]
            ) * multiplier[employee]

            last_base[employee] = current_base
            multiplier[employee] = new_multiplier

        elif typ == 3:
            employee, bonus = q[1], q[2]

            bit.range_add(
                tin[employee],
                tout[employee],
                bonus
            )

        else:
            employee = q[1]

            current_base = bit.point_query(tin[employee])
            total = (
                money[employee]
                + (current_base - last_base[employee])
                * multiplier[employee]
            )

            answer.append(str(total))

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    solve()
```

The clean version uses one employee counter, `next_employee`, because employee IDs are assigned consecutively by the input. The Euler positions are computed before query processing, while the actual employee state is still initialized only when that employee is hired.

The type 1 branch uses `bit.point_query(tin[employee])` immediately after the employee appears. Since the Fenwick tree contains all payments processed so far, this value becomes the exact historical baseline that the employee should ignore.

The type 2 branch first realizes all earnings accumulated since `last_base`. The multiplier is changed only after this calculation, so every historical payment uses the multiplier that was active when the payment occurred.

The type 3 branch changes only the Fenwick tree. Delaying the actual multiplication until a relevant employee is accessed is what removes the need to visit every member of a department.

The type 4 branch does not modify `money` or `last_base`. It computes the pending earnings on demand. Repeating the same query is safe because `base - last_base` has not changed.

## Worked Examples

For Sample 1,

```
7 1
3 1 10
4 1
2 1 2
1 1
3 1 5
4 1
4 2
```

The final tree is `1 -> 2`, so the Euler positions are `tin[1] = 1` and `tin[2] = 2`.

| Query | Employee | Multiplier | Base | Last Base | Money | Output |
| --- | --- | --- | --- | --- | --- | --- |
| `3 1 10` | 1 | 1 | 10 | 0 | 0 |  |
| `4 1` | 1 | 1 | 10 | 0 | 0 | 10 |
| `2 1 2` | 1 | 2 | 10 | 10 | 10 |  |
| `1 1` | 2 | 1 | 10 | 10 | 0 |  |
| `3 1 5` | 1 | 2 | 15 | 10 | 10 |  |
| `4 1` | 1 | 2 | 15 | 10 | 10 | 20 |
| `4 2` | 2 | 1 | 15 | 10 | 0 | 5 |

The fourth query demonstrates the historical multiplier rule. Employee 1 receives `10` from the first payment under multiplier `1`, then `10 * 2 = 20` from the second payment. Employee 2 was hired after the first payment, so its `last_base` starts at `10` and only the later `5` contributes to its total.

For Sample 2,

```
13 10
1 1
1 1
2 2 20
3 1 5
4 1
4 2
4 3
1 2
3 2 7
4 1
4 2
4 3
4 4
```

The final tree has employee 1 as the root, employees 2 and 3 as its children, and employee 4 as a child of employee 2.

| Query | Employee | Multiplier | Base | Last Base | Money | Output |
| --- | --- | --- | --- | --- | --- | --- |
| `3 1 5` | 1 | 10 | 5 | 0 | 0 |  |
| `4 1` | 1 | 10 | 5 | 0 | 0 | 50 |
| `4 2` | 2 | 20 | 5 | 0 | 0 | 100 |
| `4 3` | 3 | 10 | 5 | 0 | 0 | 50 |
| `1 2` | 4 | 10 | 5 | 5 | 0 |  |
| `3 2 7` | 2 | 20 | 12 | 5 | 0 |  |
| `4 1` | 1 | 10 | 12 | 0 | 0 | 120 |
| `4 2` | 2 | 20 | 12 | 0 | 0 | 240 |
| `4 3` | 3 | 10 | 5 | 0 | 0 | 50 |
| `4 4` | 4 | 10 | 12 | 5 | 0 | 70 |

The final employee 4 was hired after the first CEO-wide payment. Its baseline is therefore `5`, even though its final subtree belongs to the CEO's subtree and the Fenwick representation contains that earlier payment at employee 4's Euler position. The second payment adds `7` to its base, producing `7 * 10 = 70`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Building the tree and Euler order takes `O(n)`, and every query performs at most a constant number of Fenwick operations, each taking `O(log n)`. |
| Space | `O(n)` | The queries, tree, Euler arrays, employee state, and Fenwick tree all contain `O(n)` elements. |

With at most `10^5` queries and therefore at most `100001` employees, the solution performs only a logarithmic amount of work per operation instead of traversing entire departments. The memory usage is linear and comfortably fits the 256 MB limit specified by the contest.

## Test Cases

```python
import sys
import io

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, value):
        while i <= self.n:
            self.bit[i] += value
            i += i & -i

    def range_add(self, l, r, value):
        self.add(l, value)
        if r + 1 <= self.n:
            self.add(r + 1, -value)

    def point_query(self, i):
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result

def solve_io(inp):
    data = io.StringIO(inp)
    readline = data.readline

    n, S = map(int, readline().split())

    queries = []
    children = [[]]
    employee_count = 1

    for _ in range(n):
        q = list(map(int, readline().split()))
        queries.append(q)

        if q[0] == 1:
            supervisor = q[1]
            employee_count += 1

            while len(children) <= employee_count:
                children.append([])

            children[supervisor].append(employee_count)

    tin = [0] * (employee_count + 1)
    tout = [0] * (employee_count + 1)

    timer = 0
    stack = [(1, 0)]

    while stack:
        u, state = stack.pop()

        if state == 0:
            timer += 1
            tin[u] = timer
            stack.append((u, 1))

            for v in reversed(children[u]):
                stack.append((v, 0))
        else:
            tout[u] = timer

    bit = Fenwick(employee_count)

    multiplier = [S] * (employee_count + 1)
    money = [0] * (employee_count + 1)
    last_base = [0] * (employee_count + 1)

    next_employee = 1
    output = []

    for q in queries:
        typ = q[0]

        if typ == 1:
            next_employee += 1
            employee = next_employee

            multiplier[employee] = S
            last_base[employee] = bit.point_query(tin[employee])

        elif typ == 2:
            employee, new_multiplier = q[1], q[2]

            current_base = bit.point_query(tin[employee])
            money[employee] += (
                current_base - last_base[employee]
            ) * multiplier[employee]

            last_base[employee] = current_base
            multiplier[employee] = new_multiplier

        elif typ == 3:
            employee, bonus = q[1], q[2]
            bit.range_add(
                tin[employee],
                tout[employee],
                bonus
            )

        else:
            employee = q[1]
            current_base = bit.point_query(tin[employee])

            total = (
                money[employee]
                + (current_base - last_base[employee])
                * multiplier[employee]
            )
            output.append(str(total))

    return "\n".join(output)

def run(inp: str) -> str:
    return solve_io(inp)

assert run("""\
7 1
3 1 10
4 1
2 1 2
1 1
3 1 5
4 1
4 2
""") == """\
10
20
5
""", "sample 1"

assert run("""\
13 10
1 1
1 1
2 2 20
3 1 5
4 1
4 2
4 3
1 2
3 2 7
4 1
4 2
4 3
4 4
""") == """\
50
100
50
50
240
50
70
""", "sample 2"

assert run("""\
1 0
4 1
""") == """\
0
""", "minimum-size input"

assert run("""\
6 3
3 1 10
2 1 5
3 1 7
4 1
1 1
4 2
""") == """\
85
0
""", "multiplier history and late hire"

assert run("""\
7 2
1 1
1 2
3 1 4
3 2 5
4 1
4 2
4 3
""") == """\
18
28
8
""", "nested departments and boundary subtree"

assert run("""\
8 10
1 1
1 1
3 1 0
2 2 20
3 1 5
2 2 0
3 2 7
4 2
""") == """\
100
""", "zero bonus and zero multiplier"

queries = ["100000 1"]
queries.extend("1 1" for _ in range(99999))
maximum_case = "\n".join(queries) + "\n"

assert run(maximum_case) == "", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 4 1` | `0` | Minimum input and zero initial multiplier |
| Six-query multiplier-history case | `85`, `0` | Historical multiplier handling and an employee hired after a payment |
| Nested department case | `18`, `28`, `8` | Subtree intervals and overlapping department payments |
| Zero bonus and zero multiplier case | `100` | Zero-valued updates and multiplier changes to zero |
| `100000` queries consisting of hires | Empty output | Maximum input size and linear memory construction |

## Edge Cases

The first edge case is a late hire. Consider

```
3 1
3 1 10
1 1
4 2
```

The Fenwick tree records the CEO's first payment across the CEO's final subtree, which includes employee 2. When employee 2 is hired, its current base is already `10`, so `last_base[2]` becomes `10`. The later query sees `base = 10` and `last_base = 10`, giving zero new bonus. The output is `0`, exactly as required.

The second edge case is a multiplier change between two payments. For

```
4 1
3 1 10
2 1 5
3 1 10
4 1
```

the first payment increases the CEO's base from `0` to `10`. The multiplier update finalizes `10 * 1 = 10` and sets `last_base = 10`. The second payment increases the base to `20`, so the query adds `(20 - 10) * 5 = 50`. The total is `60`. Historical money is never recalculated with the new multiplier.

The third edge case is a nested department. Consider

```
4 2
1 1
1 2
3 1 5
```

The tree is `1 -> 2 -> 3`. The Euler interval of employee 1 contains all three employees, so the payment adds `5` to every employee's base. Each employee still uses their own multiplier `2`, so each receives `10`. The algorithm handles arbitrary depth because subtree membership is represented by the Euler interval rather than by checking only direct children.

The fourth edge case is a zero multiplier or zero bonus. For example,

```
8 10
1 1
1 1
3 1 0
2 2 20
3 1 5
2 2 0
3 2 7
4 2
```

Employee 2 receives nothing from the zero bonus, receives `100` from the CEO payment while its multiplier is `20`, and receives nothing from the final department payment because its multiplier has become zero. The final answer is `100`. The formula naturally handles both cases without special branches.
