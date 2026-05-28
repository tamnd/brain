---
title: "CF 28D - Don't fear, DravDe is kind"
description: "We have a fixed sequence of trucks. For every truck we know its value, the number of people inside it, and two fear cons"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "hashing"]
categories: ["algorithms"]
codeforces_contest: 28
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 28 (Codeforces format)"
rating: 2400
weight: 28
solve_time_s: 100
verified: true
draft: false
---

[CF 28D - Don't fear, DravDe is kind](https://codeforces.com/problemset/problem/28/D)

**Rating:** 2400  
**Tags:** binary search, data structures, dp, hashing  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fixed sequence of trucks. For every truck we know its value, the number of people inside it, and two fear constraints.

If a truck survives and enters the tunnel, then among all surviving trucks:

- the total number of people before it must equal `l`
- the total number of people after it must equal `r`

We may delete any subset of trucks, but the relative order of the remaining trucks cannot change. Our goal is to maximize the sum of values of the surviving trucks.

The important detail is that the constraints are expressed in terms of surviving people, not original positions. If the surviving convoy contains trucks with passenger counts:

`c[a1], c[a2], ..., c[ak]`

then for every chosen truck `ai`:

- `c[a1] + ... + c[a(i-1)] = l[ai]`
- `c[a(i+1)] + ... + c[ak] = r[ai]`

Adding both equations gives:

`total_people = l[i] + c[i] + r[i]`

This is the first structural observation. Every surviving truck must agree on the same total number of people inside the final convoy.

The constraints are large enough that quadratic dynamic programming is impossible. With `n = 10^5`, an `O(n^2)` transition count would reach roughly `10^10` operations, far beyond the limit. We need something close to `O(n log n)`.

The tricky part is that the conditions are global. A truck is valid only if the total people before and after it match exactly. A naive implementation that checks trucks independently will fail because choosing one truck changes the prefix sums seen by every later truck.

Consider this example:

```
3
5 2 0 2
5 2 2 0
100 1 0 0
```

Truck 3 alone is valid with total people `1`.

Trucks 1 and 2 together are valid with total people `4`.

The correct answer is truck 3 only, because value `100` is larger than `10`.

A greedy strategy that always extends a compatible chain would incorrectly keep trucks 1 and 2.

Another subtle case appears when several trucks share the same prefix requirement.

```
4
10 1 0 2
1 1 0 2
10 1 1 1
10 1 2 0
```

Truck 2 can never coexist with truck 3 because both require incompatible prefixes inside the same total. A careless DP that only checks local compatibility may accidentally chain them together.

There is also an edge case where no two trucks can coexist.

```
2
5 1 0 0
7 2 0 0
```

Each truck individually forms a valid convoy. The answer should pick truck 2 only.

This means the DP must naturally allow starting a new convoy from any truck.

## Approaches

A brute-force approach would enumerate every subset of trucks, preserve order, compute the surviving prefix sums, and verify every constraint. This works because the definition of validity is explicit, but even `2^40` is already hopeless, and here `n` reaches `10^5`.

A more realistic brute-force DP would try all predecessors. Suppose we process trucks left to right and define:

`dp[i] = best value of a valid convoy ending at i`

To transition from `j` to `i`, we would need:

- both trucks belong to the same total population
- the people before `i` equal the people before `j` plus `c[j]`

This already suggests a chain structure. If truck `i` has prefix requirement `l[i]`, then its predecessor must satisfy:

`l[j] + c[j] = l[i]`

and both must share the same:

`T = l + c + r`

The quadratic DP checks all previous trucks `j` for every `i`. That gives `O(n^2)` transitions, still too slow.

The key observation is that every transition depends only on two values:

- the convoy total `T`
- the required prefix population `l`

Suppose we know the best convoy for a fixed total `T` that finishes with prefix population `x`. Then a truck with:

- total `T`
- prefix `l = x + c_prev`

can extend it immediately.

This transforms the problem into a sparse state DP indexed by `(T, l)`.

For each truck:

- compute `T = l + c + r`
- any predecessor must have the same `T`
- predecessor's ending prefix must equal `l`

So we maintain:

`best[T][prefix] = best achievable state`

Each state stores the maximum value and reconstruction information.

Using hash maps gives average `O(1)` transitions, so the whole solution becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | O(n²) | O(n) | Too slow |
| Optimal Hash-DP | O(n) average | O(n) | Accepted |

## Algorithm Walkthrough

1. Process trucks from left to right.

Order matters because the convoy order cannot change. Any valid predecessor of truck `i` must appear earlier in the input.
2. For every truck, compute:

```
T = l[i] + c[i] + r[i]
```

All trucks inside the same surviving convoy must share this exact total population.
3. Maintain a hash map for DP states.

For every total `T`, we store another hash map indexed by prefix population.

A state represents:

```
best[T][p]
```

meaning the best convoy whose total population is `T` and whose current prefix population equals `p`.
4. Interpret the meaning of prefix carefully.

If a convoy ends at truck `j`, then after taking it, the total people accumulated in the convoy become:

```
l[j] + c[j]
```

That becomes the prefix required by the next compatible truck.
5. For truck `i`, look for a predecessor state:

```
best[T][l[i]]
```

because any previous convoy extended by truck `i` must already contain exactly `l[i]` people.
6. If such a state exists, extend it:

```
new_value = previous_value + v[i]
```

Otherwise, truck `i` can start a new convoy only if `l[i] == 0`.

A convoy beginning with truck `i` has no people before it.
7. The new convoy ends with accumulated prefix:

```
l[i] + c[i]
```

Update:

```
best[T][l[i] + c[i]]
```

if the new value is better.
8. Store parent pointers during updates.

For reconstruction we keep:

- previous state
- previous truck index
9. Among all states whose accumulated prefix equals `T`, choose the maximum value.

A convoy is complete only when total accumulated people equal the convoy total.

### Why it works

Every surviving convoy defines a strictly increasing sequence of prefix populations:

```
0,
c[a1],
c[a1]+c[a2],
...
```

For truck `ai`, the people before it equal exactly the accumulated population before adding its own passengers. That value is `l[ai]`.

The DP state `best[T][p]` represents the optimal partial convoy with total population `p` already accumulated inside a convoy whose final total must be `T`.

A transition is legal precisely when the next truck requires `l[i] = p`. Since all trucks in the convoy share the same total `T`, every constructed sequence satisfies both front and back fear conditions automatically.

No valid convoy is missed because every convoy can be reconstructed uniquely by following its increasing prefix sums.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    trucks = [None]

    for _ in range(n):
        v, c, l, r = map(int, input().split())
        trucks.append((v, c, l, r))

    # dp[T][prefix] = (best_value, state_id)
    dp = {}

    # state:
    # value, previous_state, truck_index, T, prefix
    states = [None]

    best_final = -1
    best_state = -1

    for i in range(1, n + 1):
        v, c, l, r = trucks[i]

        T = l + c + r

        if T not in dp:
            dp[T] = {}

        cur_map = dp[T]

        best_val = -1
        prev_state = -1

        if l == 0:
            best_val = v

        if l in cur_map:
            prev_val, st_id = cur_map[l]

            if prev_val + v > best_val:
                best_val = prev_val + v
                prev_state = st_id

        if best_val == -1:
            continue

        new_prefix = l + c

        new_state_id = len(states)
        states.append((best_val, prev_state, i, T, new_prefix))

        if (
            new_prefix not in cur_map
            or best_val > cur_map[new_prefix][0]
        ):
            cur_map[new_prefix] = (best_val, new_state_id)

        if new_prefix == T and best_val > best_final:
            best_final = best_val
            best_state = new_state_id

    ans = []

    while best_state != -1:
        value, prev_state, truck_idx, T, prefix = states[best_state]
        ans.append(truck_idx)
        best_state = prev_state

    ans.reverse()

    print(len(ans))
    print(*ans)

solve()
```

The central idea in the implementation is the interpretation of a DP state.

For a fixed total population `T`, the key that identifies progress inside the convoy is the accumulated population so far. After selecting a truck with parameters `(c, l)`, the accumulated population becomes `l + c`.

The transition step:

```
if l in cur_map:
```

means we already constructed a valid partial convoy containing exactly `l` people. Truck `i` can legally come next because its fear constraint requires exactly `l` people before it.

The initialization:

```
if l == 0:
    best_val = v
```

allows a convoy to start from this truck.

A subtle point is that we update the state for `new_prefix = l + c`, not for `l`. The new state describes the convoy after inserting the current truck.

Another easy mistake is forgetting that multiple paths may lead to the same `(T, prefix)` state. We keep only the maximum-value one because future transitions depend only on these two numbers. Any weaker state can never become optimal later.

The reconstruction stores parent state IDs instead of copying arrays of indices. This keeps memory linear.

## Worked Examples

### Example 1

Input:

```
5
1 1 0 3
1 1 1 2
1 1 2 1
1 1 3 0
2 1 3 0
```

All trucks have:

```
T = 4
```

| Truck | l | c | r | Needed state | New prefix | Best value |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 3 | start | 1 | 1 |
| 2 | 1 | 1 | 2 | prefix 1 | 2 | 2 |
| 3 | 2 | 1 | 1 | prefix 2 | 3 | 3 |
| 4 | 3 | 1 | 0 | prefix 3 | 4 | 4 |
| 5 | 3 | 1 | 0 | prefix 3 | 4 | 5 |

Truck 5 produces a better final value than truck 4, so the optimal convoy becomes:

```
1 2 3 5
```

This trace demonstrates the meaning of the DP state. Every truck extends the convoy whose accumulated population equals its required prefix.

### Example 2

Input:

```
3
5 2 0 2
5 2 2 0
100 1 0 0
```

| Truck | T | Needed state | New prefix | Best value |
| --- | --- | --- | --- | --- |
| 1 | 4 | start | 2 | 5 |
| 2 | 4 | prefix 2 | 4 | 10 |
| 3 | 1 | start | 1 | 100 |

Two separate totals exist.

For `T = 4`, the best convoy has value `10`.

For `T = 1`, the single-truck convoy has value `100`.

The algorithm correctly compares completed convoys across all totals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) average | Each truck performs a constant number of hash map operations |
| Space | O(n) | One DP state per successful transition |

The solution easily fits the limits. With `10^5` trucks, linear processing with hash maps is well within a 2-second time limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    sys.stdout = out

    import sys
    input = sys.stdin.readline

    def solve():
        n = int(input())

        trucks = [None]

        for _ in range(n):
            v, c, l, r = map(int, input().split())
            trucks.append((v, c, l, r))

        dp = {}
        states = [None]

        best_final = -1
        best_state = -1

        for i in range(1, n + 1):
            v, c, l, r = trucks[i]

            T = l + c + r

            if T not in dp:
                dp[T] = {}

            cur_map = dp[T]

            best_val = -1
            prev_state = -1

            if l == 0:
                best_val = v

            if l in cur_map:
                prev_val, st_id = cur_map[l]

                if prev_val + v > best_val:
                    best_val = prev_val + v
                    prev_state = st_id

            if best_val == -1:
                continue

            new_prefix = l + c

            new_state_id = len(states)
            states.append((best_val, prev_state, i))

            if (
                new_prefix not in cur_map
                or best_val > cur_map[new_prefix][0]
            ):
                cur_map[new_prefix] = (best_val, new_state_id)

            if new_prefix == T and best_val > best_final:
                best_final = best_val
                best_state = new_state_id

        ans = []

        while best_state != -1:
            value, prev_state, truck_idx = states[best_state]
            ans.append(truck_idx)
            best_state = prev_state

        ans.reverse()

        print(len(ans))
        print(*ans)

    solve()

    return out.getvalue().strip()

# provided sample
assert run(
"""5
1 1 0 3
1 1 1 2
1 1 2 1
1 1 3 0
2 1 3 0
"""
) == "4\n1 2 3 5", "sample 1"

# minimum size
assert run(
"""1
10 5 0 0
"""
) == "1\n1", "single truck"

# no compatible pairs
assert run(
"""2
5 1 0 0
7 2 0 0
"""
) == "1\n2", "choose larger single truck"

# chain of three
assert run(
"""3
3 1 0 2
4 1 1 1
5 1 2 0
"""
) == "3\n1 2 3", "full chain"

# competing totals
assert run(
"""3
5 2 0 2
5 2 2 0
100 1 0 0
"""
) == "1\n3", "better separate convoy"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single valid truck | `1 1` | Base case initialization |
| Two incompatible trucks | Larger value truck only | Starting new convoys correctly |
| Full compatible chain | All trucks selected | DP transitions |
| Competing totals | Best total chosen globally | Separation by `T` |

## Edge Cases

Consider the case where every truck is individually valid but incompatible with all others.

```
2
5 1 0 0
7 2 0 0
```

Truck 1 creates state:

```
T = 1
prefix = 1
value = 5
```

Truck 2 creates:

```
T = 2
prefix = 2
value = 7
```

Neither can extend the other because totals differ. The algorithm keeps both completed convoys and finally chooses the larger value, producing truck 2 only.

Now consider incompatible prefix requirements.

```
4
10 1 0 2
1 1 0 2
10 1 1 1
10 1 2 0
```

Both truck 1 and truck 2 create states with:

```
T = 3
prefix = 1
```

The DP keeps only the better one, truck 1 with value `10`.

Truck 3 extends that state:

```
value = 20
prefix = 2
```

Truck 4 extends again:

```
value = 30
prefix = 3
```

The weaker state through truck 2 never survives because future transitions depend only on `(T, prefix)`. Keeping the maximum value is sufficient.

Finally, consider multiple completed convoys with different totals.

```
3
5 2 0 2
5 2 2 0
100 1 0 0
```

The algorithm independently builds:

- convoy `{1,2}` with value `10`
- convoy `{3}` with value `100`

Since completed states are compared globally, the correct answer remains truck 3 only.
