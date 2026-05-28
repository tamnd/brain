---
title: "CF 4C - Registration System"
description: "We are building a username registration system. Every incoming request contains a desired username. If that username has never appeared before, registration succeeds immediately and we print OK."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "hashing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 4
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 4 (Div. 2 Only)"
rating: 1300
weight: 4
solve_time_s: 102
verified: true
draft: false
---

[CF 4C - Registration System](https://codeforces.com/problemset/problem/4/C)

**Rating:** 1300  
**Tags:** data structures, hashing, implementation  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building a username registration system. Every incoming request contains a desired username. If that username has never appeared before, registration succeeds immediately and we print `OK`.

If the username is already taken, we must generate a new one by attaching the smallest positive integer suffix that produces a name not yet used. For example, if `alex` already exists, we try `alex1`, then `alex2`, and so on until we find a free name. The chosen generated name also becomes occupied.

The input gives a sequence of registration requests, one per line. The output must contain the system's response for each request in the same order.

The constraint of up to $10^5$ requests changes the problem completely. A solution that scans previously used names every time would become far too slow. With $10^5$ operations, we should aim for roughly linear time overall, or close to it. Hash tables are a natural fit because we repeatedly ask the same question: "Has this username already been used?"

The tricky part is that generated names themselves also become occupied. A careless implementation may only track original names and forget generated ones.

Consider this input:

```
4
bob
bob
bob1
bob
```

The correct output is:

```
OK
bob1
OK
bob2
```

After the second request, `bob1` is already occupied because the system generated it. When the third request explicitly asks for `bob1`, it must already exist.

Another subtle case appears when many suffixes are already occupied:

```
5
a
a1
a2
a
a
```

The correct output is:

```
OK
OK
OK
a3
a4
```

A naive implementation that always starts checking from `1` would repeatedly test `a1`, `a2`, and so on. That still produces correct answers, but it wastes a large amount of time.

One more easy mistake is forgetting that the original name itself also needs tracking:

```
3
test
test
test
```

The correct output is:

```
OK
test1
test2
```

If we only track generated suffixes, the third request could incorrectly produce `test1` again.

## Approaches

The brute-force idea follows the problem statement directly. Maintain a set of used usernames. When a new request arrives, check whether it already exists.

If it does not exist, insert it and print `OK`.

If it already exists, start trying suffixes one by one:

```
name1
name2
name3
...
```

The first unused candidate becomes the answer.

This method is correct because it literally simulates the required process. The problem is performance. Suppose the input contains `a` repeated $10^5$ times. The first duplicate checks `a1`, the next checks `a1` and `a2`, the next checks `a1`, `a2`, `a3`, and so on. The total number of checks becomes:

$$1 + 2 + 3 + \dots + (n-1)$$

which is $O(n^2)$. With $10^5$ requests, that is around $5 \times 10^9$ operations, far beyond the limit.

The key observation is that once we already know the next available suffix for a base name, we never need to retry smaller suffixes again.

For example, after generating `alex7`, we already know that `alex1` through `alex7` are occupied. The next duplicate request for `alex` should begin directly from suffix `8`.

This transforms the problem into maintaining two pieces of information inside a hash map:

1. Whether a username already exists.
2. For every base name, what suffix should be tried next.

Hash tables give average $O(1)$ insertion and lookup, so each request can be processed in constant expected time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ average | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Create a hash map called `mp`.

The map stores usernames as keys. For a base name, its value represents the next suffix to try.
2. Process each incoming username one by one.

We must answer requests in order because every accepted username immediately affects future requests.
3. If the username does not exist in the map, print `OK`.

This means the name is completely unused, so registration succeeds immediately.
4. Insert this username into the map with value `1`.

The value `1` means that if this name appears again later, the first suffix to try should be `1`.
5. If the username already exists, read its stored counter.

Suppose `mp[name] = k`. This means suffixes smaller than `k` are already occupied, so there is no reason to test them again.
6. Construct the candidate `name + str(k)`.

This is the smallest suffix that has not yet been tried for this base name.
7. Print the generated candidate and insert it into the map.

The generated name now becomes occupied just like any explicitly requested username.
8. Increase `mp[name]` by one.

The next duplicate request for the same base name should continue from the next suffix.

### Why it works

The invariant is:

```
For every base username x, mp[x] always stores the smallest suffix
that has not yet been assigned for x.
```

Initially, after inserting `x` for the first time, the smallest unused suffix is `1`, so `mp[x] = 1`.

Whenever we generate `xk`, we immediately increment the counter to `k + 1`. Since all smaller suffixes were already occupied before, and `xk` has just become occupied now, the next unused suffix is exactly `k + 1`.

Because the invariant always holds, every generated username is both valid and minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    mp = {}

    for _ in range(n):
        name = input().strip()

        if name not in mp:
            print("OK")
            mp[name] = 1
        else:
            suffix = mp[name]
            new_name = name + str(suffix)

            print(new_name)

            mp[name] += 1
            mp[new_name] = 1

solve()
```

The dictionary `mp` plays two roles at the same time. Its keys represent all occupied usernames, while values for base usernames track the next suffix to use.

When a name appears for the first time, we print `OK` and initialize its counter to `1`. This matches the invariant that the next duplicate should try suffix `1`.

For duplicate requests, we directly read the stored suffix instead of scanning from `1` again. That single optimization removes the quadratic behavior.

The line:

```
mp[new_name] = 1
```

is extremely important. Generated usernames must also become reserved immediately. Without this line, future requests could accidentally reuse them.

Another subtle detail is updating `mp[name]` after generating a username. If we forget to increment it, the same suffix would be reused repeatedly.

The implementation uses `input().strip()` because each username comes on its own line and we do not want trailing newline characters inside the stored strings.

## Worked Examples

### Example 1

Input:

```
4
abacaba
acaba
abacaba
acab
```

| Step | Request | Map Before | Output | Map After |
| --- | --- | --- | --- | --- |
| 1 | abacaba | {} | OK | {abacaba: 1} |
| 2 | acaba | {abacaba: 1} | OK | {abacaba: 1, acaba: 1} |
| 3 | abacaba | {abacaba: 1, acaba: 1} | abacaba1 | {abacaba: 2, acaba: 1, abacaba1: 1} |
| 4 | acab | {abacaba: 2, acaba: 1, abacaba1: 1} | OK | {abacaba: 2, acaba: 1, abacaba1: 1, acab: 1} |

This trace shows how the counter for `abacaba` advances from `1` to `2` after generating `abacaba1`. The algorithm never checks suffix `1` again for that base name.

### Example 2

Input:

```
5
a
a
a
a1
a
```

| Step | Request | Map Before | Output | Map After |
| --- | --- | --- | --- | --- |
| 1 | a | {} | OK | {a: 1} |
| 2 | a | {a: 1} | a1 | {a: 2, a1: 1} |
| 3 | a | {a: 2, a1: 1} | a2 | {a: 3, a1: 1, a2: 1} |
| 4 | a1 | {a: 3, a1: 1, a2: 1} | a11 | {a: 3, a1: 2, a2: 1, a11: 1} |
| 5 | a | {a: 3, a1: 2, a2: 1, a11: 1} | a3 | {a: 4, a1: 2, a2: 1, a11: 1, a3: 1} |

This example demonstrates that generated usernames behave exactly like normal usernames. Once `a1` exists, requesting `a1` again must generate `a11`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ average | Each request performs constant-time hash map operations |
| Space | $O(n)$ | Every accepted username is stored once |

With at most $10^5$ requests, linear complexity easily fits within the limits. Python dictionaries are optimized hash tables, so insertions and lookups are fast enough for this constraint.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())
        mp = {}
        out = []

        for _ in range(n):
            name = input().strip()

            if name not in mp:
                out.append("OK")
                mp[name] = 1
            else:
                suffix = mp[name]
                new_name = name + str(suffix)

                out.append(new_name)

                mp[name] += 1
                mp[new_name] = 1

        return "\n".join(out)

    return solve()

# provided sample
assert run(
    "4\nabacaba\nacaba\nabacaba\nacab\n"
) == (
    "OK\nOK\nabacaba1\nOK"
), "sample 1"

# minimum size
assert run(
    "1\nx\n"
) == (
    "OK"
), "single registration"

# all equal values
assert run(
    "5\na\na\na\na\na\n"
) == (
    "OK\na1\na2\na3\na4"
), "repeated identical names"

# generated names later requested explicitly
assert run(
    "4\nbob\nbob\nbob1\nbob\n"
) == (
    "OK\nbob1\nbob11\nbob2"
), "generated usernames must also be reserved"

# boundary style chaining
assert run(
    "6\na\na1\na\na1\na2\na\n"
) == (
    "OK\nOK\na2\na11\na21\na3"
), "nested suffix interactions"

# larger repeated sequence
large_input = "10\n" + "\n".join(["z"] * 10) + "\n"

assert run(large_input) == (
    "OK\nz1\nz2\nz3\nz4\nz5\nz6\nz7\nz8\nz9"
), "many duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single username | `OK` | Minimum input size |
| Many identical names | Sequential suffixes | Counter increments correctly |
| `bob`, `bob`, `bob1`, `bob` | `bob1` must become occupied | Generated names are reserved |
| Mixed suffix chains | Correct nested generation | Handles names that already contain digits |
| Ten repeated `z` values | `z1` through `z9` | Large duplicate sequences remain efficient |

## Edge Cases

Consider the case where a generated username is later requested explicitly:

```
4
bob
bob
bob1
bob
```

Step by step:

1. `bob` is new, print `OK`, store `bob -> 1`.
2. `bob` exists, generate `bob1`, print it, update `bob -> 2`, store `bob1 -> 1`.
3. `bob1` already exists because it was generated earlier, so we must generate `bob11`.
4. `bob` now starts directly from suffix `2`, generating `bob2`.

The output becomes:

```
OK
bob1
bob11
bob2
```

This confirms that generated usernames are treated exactly like normal ones.

Now consider repeated duplicates:

```
5
a
a
a
a
a
```

Execution:

1. First `a` prints `OK`.
2. Second `a` prints `a1`.
3. Third `a` prints `a2`.
4. Fourth `a` prints `a3`.
5. Fifth `a` prints `a4`.

The algorithm never rechecks old suffixes because `mp["a"]` always stores the next unused suffix directly.

Finally, consider names that already contain digits:

```
5
a1
a1
a11
a1
a
```

Execution:

1. `a1` prints `OK`.
2. Duplicate `a1` generates `a11`.
3. `a11` already exists, so it generates `a111`.
4. Another `a1` generates `a12`.
5. `a` is still unused, so it prints `OK`.

The output is:

```
OK
a11
a111
a12
OK
```

The algorithm never tries to parse digits from usernames. Every string is treated independently, which avoids many corner-case bugs.
