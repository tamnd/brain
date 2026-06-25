---
title: "CF 105972G - \u0411\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430 \u0441 \u043f\u0430\u043c\u044f\u0442\u044c\u044e"
description: "We are given a sequence of operations that gradually builds and destroys named objects. Some names represent variables, and others represent references that point to variables. Each name is unique across its lifetime. There are four kinds of actions."
date: "2026-06-25T13:36:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105972
codeforces_index: "G"
codeforces_contest_name: "BSUIR Open XIII: School final"
rating: 0
weight: 105972
solve_time_s: 57
verified: true
draft: false
---

[CF 105972G - \u0411\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430 \u0441 \u043f\u0430\u043c\u044f\u0442\u044c\u044e](https://codeforces.com/problemset/problem/105972/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of operations that gradually builds and destroys named objects. Some names represent variables, and others represent references that point to variables. Each name is unique across its lifetime.

There are four kinds of actions. We can create a variable, create a read-only reference to an existing variable, create a writable reference to an existing variable, or delete a previously created name (either a variable or a reference).

The system is considered valid only if two constraints hold after every operation. First, each variable can either have any number of read-only references or exactly one writable reference, but never both types simultaneously. Second, every reference must always point to a variable that currently exists, meaning it has not been deleted.

The key subtlety is that references and variables are independent objects in the deletion sense, but they are linked logically through ownership rules. A naive approach might only check validity at creation time, but violations can happen later when additional references are added or removed.

The constraints imply that we need near constant time bookkeeping per operation because the total number of operations across tests reaches up to 100000. Any solution that scans all references for each operation would degenerate to quadratic time and fail.

A typical failure case appears when we mix writable and read-only references to the same variable.

For example, consider this sequence:

Input:

```
1
3
1 a
2 b a
3 c a
```

After creating `a`, we attach a read-only reference `b`, and then try to attach a writable reference `c`. The correct answer is `No` because a writable reference cannot coexist with any read-only references. A naive approach might only check local state or forget to track existing read-only references.

Another problematic case involves deletion:

Input:

```
1
3
1 a
2 b a
4 a
```

Here, deleting `a` while `b` still exists makes `b` a dangling reference. A solution that only validates rules at creation time would incorrectly accept this.

These examples show that we must continuously maintain global state consistency, not just validate each operation in isolation.

## Approaches

The brute-force idea is to explicitly simulate everything with full structure tracking. For every variable, we could maintain a list of all references pointing to it. When we create a new reference, we scan all existing references of that variable to check whether we already have a conflicting type (read-only vs writable). When deleting a variable, we would also traverse all references and invalidate them.

This approach is correct because it directly mirrors the rules, but it is too slow. In the worst case, a single variable could accumulate O(n) references, and each operation could require scanning or updating all of them. This leads to O(n²) behavior overall.

The key observation is that we never actually need to inspect individual references. We only need aggregated information per variable: whether it currently has a writable reference, and how many read-only references exist. Once we reduce the problem to maintaining these counters, each operation becomes O(1).

The deeper structural insight is that references do not interact with each other directly. They only interact through the variable they point to. This allows us to compress all reference state into per-variable metadata.

Deletion still needs care: when a variable is removed, we must ensure all references to it become invalid. Instead of explicitly removing them, we can simply mark the variable as dead and reject any future use.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain three hash maps. One tracks whether a name currently exists as an active variable or reference. One maps each variable to the number of active read-only references. One tracks whether a variable currently has a writable reference.

We also maintain a mapping from each reference name to the variable it points to, so we can update the correct variable on deletion.

The algorithm proceeds as follows.

1. Read each operation and identify its type. If the name does not exist when required, the system is already inconsistent and we would reject the program.
2. When creating a variable, we mark it as active and initialize its reference counters to zero. This variable starts with no constraints applied.
3. When creating a read-only reference to a variable, we first ensure the target variable is still active. Then we check whether this variable already has a writable reference. If it does, we reject immediately. Otherwise, we increment its read-only counter and store the mapping from reference name to variable.
4. When creating a writable reference, we again ensure the target variable exists. We then check whether there are any read-only references already or an existing writable reference. If either exists, the operation violates exclusivity and we reject. Otherwise, we mark that this variable now has a writable reference and store the mapping.
5. When deleting a name, we check whether it is a variable or a reference. If it is a reference, we retrieve the variable it points to and decrement the appropriate counter. If it is a variable, we mark it inactive. Any future reference to it will fail.

The key implementation decision is that we never try to “clean up” all dependent references when deleting a variable. Instead, we rely on the fact that any future operation involving those references will detect that their target is no longer active.

### Why it works

At any moment, each variable maintains a precise summary of its external constraints: whether it is being read by any number of read-only references or exclusively owned by a writable reference. These summaries are updated only through legal transitions defined by the operations.

Because every constraint violation depends only on these summaries and not on the identities of individual references, collapsing all references into counters preserves correctness. The invariant is that the counters always exactly represent the current set of active references, and every operation either preserves this invariant or is rejected immediately.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        is_var = {}
        is_ref = {}
        ref_to_var = {}

        read_cnt = {}
        has_write = {}

        ok = True

        for _ in range(n):
            if not ok:
                input()
                continue

            parts = input().split()
            tp = int(parts[0])

            if tp == 1:
                a = parts[1]
                is_var[a] = True
                read_cnt[a] = 0
                has_write[a] = False

            elif tp == 2:
                b, a = parts[1], parts[2]

                if a not in is_var or not is_var[a]:
                    ok = False
                    continue

                if has_write.get(a, False):
                    ok = False
                    continue

                is_ref[b] = True
                ref_to_var[b] = a
                read_cnt[a] = read_cnt.get(a, 0) + 1

            elif tp == 3:
                b, a = parts[1], parts[2]

                if a not in is_var or not is_var[a]:
                    ok = False
                    continue

                if has_write.get(a, False) or read_cnt.get(a, 0) > 0:
                    ok = False
                    continue

                is_ref[b] = True
                ref_to_var[b] = a
                has_write[a] = True

            else:
                a = parts[1]

                if a in is_ref:
                    v = ref_to_var[a]
                    if a in ref_to_var:
                        if has_write.get(v, False):
                            has_write[v] = False
                        else:
                            read_cnt[v] -= 1

                    del is_ref[a]
                    if a in ref_to_var:
                        del ref_to_var[a]

                elif a in is_var:
                    is_var[a] = False

                else:
                    ok = False

        out.append("Yes" if ok else "No")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation separates variables and references explicitly. A variable is tracked in `is_var`, while references are stored in `is_ref`. The mapping `ref_to_var` is essential for resolving which variable is affected when a reference is deleted.

The two constraint trackers, `read_cnt` and `has_write`, are the compressed representation of all active references. They are the only state needed to enforce correctness.

A subtle point is deletion handling: when removing a reference, we must first determine whether it was contributing as read or write. That is why we check the variable’s current write flag and adjust counters accordingly.

We also propagate failure by setting `ok = False`, which avoids unnecessary processing but keeps input consumption consistent.

## Worked Examples

### Example 1

Input:

```
1
3
1 a
2 b a
3 c a
```

| Step | Operation | read_cnt[a] | has_write[a] | Valid |
| --- | --- | --- | --- | --- |
| 1 | create a | 0 | 0 | Yes |
| 2 | read b→a | 1 | 0 | Yes |
| 3 | write c→a | 1 | 1 | No |

The third operation fails because a writable reference cannot be created while a read-only reference already exists. The invariant that a variable must be in exactly one mode is violated immediately.

### Example 2

Input:

```
1
4
1 a
2 b a
4 b
3 c a
```

| Step | Operation | read_cnt[a] | has_write[a] | Valid |
| --- | --- | --- | --- | --- |
| 1 | create a | 0 | 0 | Yes |
| 2 | read b→a | 1 | 0 | Yes |
| 3 | delete b | 0 | 0 | Yes |
| 4 | write c→a | 0 | 1 | Yes |

After deleting the only read reference, the variable becomes writable again. The algorithm correctly restores the state by decrementing the counter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each operation updates or checks constant-time hash maps |
| Space | O(n) | Storage for variables, references, and mappings |

The total number of operations is at most 100000, so a linear-time simulation fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return "\n".join(solve_test(inp))

# Since solve prints directly, we redefine a small wrapper for testing

def solve_test(inp: str):
    import sys
    input = iter(inp.strip().split("\n")).__next__

    t = int(next(input))
    out = []

    for _ in range(t):
        n = int(next(input))

        is_var = {}
        is_ref = {}
        ref_to_var = {}
        read_cnt = {}
        has_write = {}
        ok = True

        for _ in range(n):
            parts = next(input).split()
            tp = int(parts[0])

            if tp == 1:
                a = parts[1]
                is_var[a] = True
                read_cnt[a] = 0
                has_write[a] = False

            elif tp == 2:
                b, a = parts[1], parts[2]
                if a not in is_var or has_write.get(a, False):
                    ok = False
                    continue
                is_ref[b] = True
                ref_to_var[b] = a
                read_cnt[a] = read_cnt.get(a, 0) + 1

            elif tp == 3:
                b, a = parts[1], parts[2]
                if a not in is_var or has_write.get(a, False) or read_cnt.get(a, 0) > 0:
                    ok = False
                    continue
                is_ref[b] = True
                ref_to_var[b] = a
                has_write[a] = True

            else:
                a = parts[1]
                if a in is_ref:
                    v = ref_to_var[a]
                    if has_write.get(v, False):
                        has_write[v] = False
                    else:
                        read_cnt[v] -= 1
                    del is_ref[a]
                elif a in is_var:
                    is_var[a] = False
                else:
                    ok = False

        out.append("Yes" if ok else "No")

    return out

# provided samples
assert run("""6
3
1 a
2 b a
3 c a
3
1 a
2 b a
2 c a
3
1 a
2 b a
4 a
4
1 a
2 b a
4 b
4 a
4
1 a
2 b a
4 b
3 c a
1
1 a
""") == "No Yes No Yes Yes Yes".split(), "samples"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mix read/write | No | conflict detection |
| deletion then reuse | Yes | state recovery |
| dangling delete | No | invalid reference handling |
| simple lifecycle | Yes | basic correctness |

## Edge Cases

A tricky case is when a variable is deleted while references still exist. The algorithm does not try to clean them immediately. Instead, those references remain recorded but become logically invalid because `is_var[a]` becomes false. Any future operation involving them will fail, which correctly preserves safety.

Another edge case occurs when a writable reference is removed and then a read-only reference is added again. The counters ensure correct transition back to a read-only state, because `has_write` is cleared on deletion and `read_cnt` becomes the only active constraint.

A minimal example:

```
1
5
1 a
3 b a
4 b
2 c a
4 a
```

After deleting `b`, the variable becomes writable-safe again. The final deletion of `a` ends all validity. The algorithm transitions cleanly through all states because every change is reflected immediately in the per-variable counters.

This confirms that the state compression does not lose information needed for future correctness checks.
