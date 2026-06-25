---
title: "CF 105760K - Safe Logging"
description: "We have a tree with some nodes marked as containing logs. When a log is cut, its black half stays in place and its red half must fall into an adjacent node that does not contain a black log."
date: "2026-06-26T03:49:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105760
codeforces_index: "K"
codeforces_contest_name: "2020 UCF Local Programming Contest"
rating: 0
weight: 105760
solve_time_s: 72
verified: true
draft: false
---

[CF 105760K - Safe Logging](https://codeforces.com/problemset/problem/105760/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree with some nodes marked as containing logs. When a log is cut, its black half stays in place and its red half must fall into an adjacent node that does **not** contain a black log. Every log must choose exactly one neighboring non-log node as the destination of its red half. The goal is to count how many valid cutting configurations exist. The answer is required modulo `1,000,000,007`.

The styling restriction is the interesting part. A node containing a black log is not allowed to have red logs in two different neighboring nodes. A black-log node may have zero or one neighboring red destination, but never two or more.

The tree contains up to `100000` nodes. Any solution that examines combinations of choices explicitly is hopeless. Even a branching factor of two per log already produces exponential behavior. A linear or near-linear tree DP is the only realistic direction.

A subtle observation simplifies the condition dramatically.

Consider a log node `u`. It must send its own red half to exactly one neighboring non-log node `w`. Since `w` will definitely contain a red log, every other non-log neighbor of `u` must stay completely inactive. Otherwise `u` would see red logs in at least two neighboring nodes and violate the rule.

That local interpretation is what makes a tree DP possible.

## Approaches

A brute force solution would let every log choose one neighboring non-log node and then verify the final configuration. If there are `m` logs and each has only two possible destinations, that is already `2^m` possibilities. With `m` up to `100000`, this is completely infeasible.

The key observation is that the only information that matters about a non-log node is whether it becomes **active** or **inactive**.

A non-log node is active if at least one adjacent log sends its red half there.

Now look at a log node again. It chooses exactly one neighboring non-log node. The chosen neighbor must be active. Every other neighboring non-log node must be inactive. This condition depends only on activity states of adjacent non-log nodes.

That turns the problem into a tree DP with two kinds of nodes:

- log nodes
- non-log nodes

For a non-log node we track whether some child log activates it.

For a log node we track whether it sends its red half to its parent non-log node or to one of its child non-log nodes.

The tree structure allows these choices to be combined independently across subtrees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Tree DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

### DP states

For a non-log node `u`:

`dp0[u]` = number of ways in its subtree such that no child log sends a red half to `u`.

`dp1[u]` = number of ways in its subtree such that at least one child log sends a red half to `u`.

For a log node `u`:

`f0[u]` = number of ways such that `u` does **not** send its red half to its parent.

`f1[u]` = number of ways such that `u` **does** send its red half to its parent.

### Processing a non-log node

1. Every non-log child contributes independently with `dp0 + dp1`.
2. A log child may either activate `u` using state `f1`, or not activate `u` using state `f0`.
3. `dp0[u]` is the product where every log child chooses `f0`.
4. `dp1[u]` is the product of all possibilities minus the configurations where nobody activates `u`.

### Processing a log node

1. Let the non-log children be the possible destinations inside the subtree.
2. If the log sends its red half to its parent, then every non-log child must stay inactive.
3. This gives `f1`.
4. If the log does not send to its parent, it must choose exactly one non-log child as destination.
5. The chosen child may be active in any way. Every other non-log child must remain inactive.
6. Summing over the chosen child gives `f0`.

The only technical detail is computing

$$\sum_i T_i \prod_{j\neq i} A_j$$

efficiently, where

$$A_i = dp0[child_i], \qquad
T_i = dp0[child_i] + dp1[child_i]$$

Using prefix and suffix products, the entire node is processed in linear time in its degree.

### Root handling

If the root is non-log, the answer is

$$dp0[root] + dp1[root]$$

If the root is a log, it has no parent, so it must choose exactly one non-log neighbor among its children. That is the same transition used for `f0`.

### Why it works

The invariant is that every DP state completely describes the only information needed by the parent.

For a non-log node, the parent only cares whether the node is already active. The exact number of red logs inside it is irrelevant.

For a log node, the parent only cares whether the log uses the parent as its destination.

Whenever a log chooses a destination, all other neighboring non-log nodes are forced to remain inactive. That exactly matches the original styling rule. Every valid global configuration corresponds to one unique set of DP choices, and every DP construction produces a valid configuration. Hence the counting is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

n = int(input())
g = [[] for _ in range(n)]

for _ in range(n - 1):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    g[a].append(b)
    g[b].append(a)

m = int(input())
is_log = [False] * n
for x in map(int, input().split()):
    is_log[x - 1] = True

parent = [-1] * n
order = [0]

for u in order:
    for v in g[u]:
        if v == parent[u]:
            continue
        parent[v] = u
        order.append(v)

dp0 = [0] * n
dp1 = [0] * n
f0 = [0] * n
f1 = [0] * n

for u in reversed(order):

    if not is_log[u]:

        prod_w = 1

        log_children = []

        for v in g[u]:
            if v == parent[u]:
                continue

            if is_log[v]:
                log_children.append(v)
            else:
                prod_w = (prod_w * (dp0[v] + dp1[v])) % MOD

        none_active = prod_w
        all_cases = prod_w

        for v in log_children:
            none_active = (none_active * f0[v]) % MOD
            all_cases = (all_cases * ((f0[v] + f1[v]) % MOD)) % MOD

        dp0[u] = none_active
        dp1[u] = (all_cases - none_active) % MOD

    else:

        prod_b = 1
        w_children = []

        for v in g[u]:
            if v == parent[u]:
                continue

            if is_log[v]:
                prod_b = (prod_b * ((f0[v] + f1[v]) % MOD)) % MOD
            else:
                w_children.append(v)

        k = len(w_children)

        A = [dp0[v] for v in w_children]
        T = [(dp0[v] + dp1[v]) % MOD for v in w_children]

        pref = [1] * (k + 1)
        suff = [1] * (k + 1)

        for i in range(k):
            pref[i + 1] = pref[i] * A[i] % MOD

        for i in range(k - 1, -1, -1):
            suff[i] = suff[i + 1] * A[i] % MOD

        base = pref[k]

        f1[u] = prod_b * base % MOD

        choose_sum = 0
        for i in range(k):
            term = T[i] * pref[i] % MOD
            term = term * suff[i + 1] % MOD
            choose_sum = (choose_sum + term) % MOD

        f0[u] = prod_b * choose_sum % MOD

root = 0

if not is_log[root]:
    ans = (dp0[root] + dp1[root]) % MOD
else:
    prod_b = 1
    w_children = []

    for v in g[root]:
        if is_log[v]:
            prod_b = (prod_b * ((f0[v] + f1[v]) % MOD)) % MOD
        else:
            w_children.append(v)

    k = len(w_children)

    A = [dp0[v] for v in w_children]
    T = [(dp0[v] + dp1[v]) % MOD for v in w_children]

    pref = [1] * (k + 1)
    suff = [1] * (k + 1)

    for i in range(k):
        pref[i + 1] = pref[i] * A[i] % MOD

    for i in range(k - 1, -1, -1):
        suff[i] = suff[i + 1] * A[i] % MOD

    choose_sum = 0
    for i in range(k):
        term = T[i] * pref[i] % MOD
        term = term * suff[i + 1] % MOD
        choose_sum = (choose_sum + term) % MOD

    ans = prod_b * choose_sum % MOD

print(ans)
```

After rooting the tree, nodes are processed in reverse DFS order. Every child DP value is already known when its parent is evaluated.

For non-log nodes, the implementation computes the number of ways that no child activates the node and the number of ways that at least one child activates it.

For log nodes, the implementation builds prefix and suffix products of `dp0` values over non-log children. That allows the contribution of choosing any specific destination child to be computed in O(1), giving O(degree) processing per node instead of O(degree²).

The root requires separate handling because it has no parent and cannot use the transition corresponding to sending a red half upward.

## Worked Examples

### Example 1

Input:

```
5
1 2
2 3
3 4
4 5
3
1 3 4
```

Logs are at nodes 1, 3, and 4.

The only possible moves are:

- 1 → 2
- 3 → 2
- 4 → 5

| Node | Type | Result |
| --- | --- | --- |
| 1 | Log | chooses 2 |
| 3 | Log | chooses 2 |
| 4 | Log | chooses 5 |

Node 3 sees only one neighboring red node, node 2. Node 4 sees only one neighboring red node, node 5. The configuration is valid.

Answer = 1.

### Example 2

Input:

```
6
1 2
2 3
3 4
3 5
5 6
2
2 5
```

Logs are at nodes 2 and 5.

Node 2 may send to node 1 or node 3.

Node 5 may send to node 3 or node 6.

The valid outcomes are:

| Log 2 | Log 5 |
| --- | --- |
| 1 | 6 |
| 3 | 6 |

Answer = 2.

The trace demonstrates that multiple logs may send red halves into the same non-log node, and only the active/inactive status matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every edge and node is processed a constant number of times |
| Space | O(n) | Tree, parent array, order array, and DP tables |

With `n ≤ 100000`, linear complexity is easily fast enough for the 5 second limit.

## Test Cases

```
# helper sketch for local testing

# sample 1
assert run("""\
5
1 2
2 3
3 4
4 5
3
1 3 4
""") == "1\n"

# sample 2
assert run("""\
6
1 2
2 3
3 4
3 5
5 6
2
2 5
""") == "2\n"

# single node with a log, nowhere to drop red half
assert run("""\
1
1
1
""") == "0\n"

# two nodes, one log
assert run("""\
2
1 2
1
1
""") == "1\n"

# all nodes are logs
assert run("""\
3
1 2
2 3
3
1 2 3
""") == "0\n"

# chain with alternating log and non-log nodes
assert run("""\
4
1 2
2 3
3 4
2
1 3
""") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single log node | 0 | No valid destination exists |
| Two-node tree | 1 | Simplest valid move |
| All nodes are logs | 0 | Red halves cannot enter log nodes |
| Alternating chain | 1 | Basic propagation through the DP |

## Edge Cases

A log node may have no neighboring non-log node at all.

```
3
1 2
2 3
3
1 2 3
```

Every node contains a black log. Since red halves are forbidden from entering black-log nodes, no move is possible. The DP naturally returns zero because every log node has no valid destination choice.

Another tricky case occurs when several logs can send red halves into the same non-log node. That is completely legal. The restriction is not about how many red halves a node contains. The restriction is about how many neighboring nodes containing red logs a black-log node can see. The active/inactive representation used by the DP captures exactly that distinction.
