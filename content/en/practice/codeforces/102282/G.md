---
title: "CF 102282G - \u0411\u0430\u044f\u043d"
description: "The building is organized into entrances, floors, and apartments. Every entrance contains exactly n floors, and every floor contains exactly m apartments."
date: "2026-08-13T09:11:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102282
codeforces_index: "G"
codeforces_contest_name: "2011, \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u0441\u0442 \u0421\u0413\u0410\u0423 \u043d\u0430 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b ACM ICPC"
rating: 0
weight: 102282
solve_time_s: 72
verified: true
draft: false
---

[CF 102282G - \u0411\u0430\u044f\u043d](https://codeforces.com/problemset/problem/102282/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The building is organized into entrances, floors, and apartments. Every entrance contains exactly `n` floors, and every floor contains exactly `m` apartments. Apartment numbers increase continuously from one entrance to the next: the first entrance contains apartments `1` through `n*m`, the second contains the next `n*m` apartments, and so on.

We are given the apartment number `k`. The task is to determine two things: the entrance containing apartment `k`, and the floor containing it inside that entrance.

For example, with `n = 3` and `m = 4`, one entrance contains `3 * 4 = 12` apartments. Apartments `1..4` are on floor 1, apartments `5..8` are on floor 2, and apartments `9..12` are on floor 3. Thus apartment `10` belongs to entrance 1, floor 3.

All three input values can be as large as `10^9`. A solution that examines apartments, floors, or entrances one by one can consequently require up to about one billion iterations. Under a one-second limit, that is far beyond what we want. The structure of the numbering gives us a direct arithmetic formula, so the intended solution should use constant time and constant memory.

The first boundary case is when `k` is exactly divisible by `m`. For example, `n = 3, m = 4, k = 8` gives output `1 2`. Apartment 8 is the last apartment on floor 2. A careless formula such as `k / m + 1` would produce floor 3 because it forgets that division must be based on zero-based positions.

The second boundary case is when `k` is exactly the last apartment of an entrance. For `n = 3, m = 4, k = 12`, the correct output is `1 3`. Apartment 12 still belongs to entrance 1. Using `k // (n*m) + 1` directly would incorrectly produce entrance 2.

The third case is the very first apartment. For `n = 1, m = 1, k = 1`, the answer is `1 1`. Any formula that uses ordinary division without shifting the apartment number first risks producing zero-based answers or an extra increment.

## Approaches

A direct brute-force solution can simulate the numbering. Starting from apartment 1, we can keep track of the current entrance and floor, moving to the next floor after every `m` apartments and to the next entrance after every `n` floors. Once apartment `k` is reached, the stored entrance and floor are the answer. This works because it follows exactly the same ordering used to assign apartment numbers.

The problem is the number of iterations. In the worst case, consider `n = 1`, `m = 1`, and `k = 10^9`. There is one apartment per floor, so a simulation has to process all `10^9` apartments before reaching the target. Even with a more efficient simulation that skips complete floors, the worst case can still require up to `10^9` floor or entrance transitions. That is not suitable for a one-second competitive programming limit.

The key observation is that every entrance contains exactly `n*m` apartments. Instead of simulating all previous entrances, we can ask directly which block of `n*m` consecutive apartment numbers contains `k`. Once that entrance is known, we only need the position of `k` inside that entrance. The same idea applies to the floor: every floor contains exactly `m` apartments, so the position inside the entrance determines the floor with one integer division.

The cleanest way to handle all boundaries is to temporarily make the apartment number zero-based by considering `k - 1`. Then the first apartment has position 0, the last apartment of the first floor has position `m - 1`, and the last apartment of the first entrance has position `n*m - 1`. Integer division and remainder then match the desired groups exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) in the worst case | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the number of apartments in one entrance as `n * m`. This gives the size of one complete entrance block in the global apartment numbering.
2. Replace `k` with `k - 1` conceptually and compute `(k - 1) // (n * m) + 1` for the entrance. Dividing the zero-based position by the size of one entrance block tells us how many complete entrance blocks occur before the target, and adding one converts the zero-based block index to a one-based entrance number.
3. Compute `(k - 1) % (n * m)` to obtain the zero-based position of apartment `k` inside its entrance. The remainder discards all complete entrances before the target.
4. Divide that position by `m` and add one: `(position_inside_entrance // m) + 1`. Every group of `m` consecutive positions belongs to one floor, so the quotient identifies the zero-based floor.
5. Print the entrance number followed by the floor number.

### Why it works

Let `p = k - 1`. Since each entrance contains exactly `n*m` apartments, the quotient `p // (n*m)` is precisely the number of complete entrances before apartment `k`. Thus adding one gives the correct entrance. The remainder `p % (n*m)` is the apartment's zero-based position inside that entrance. Since every floor contains exactly `m` apartments, dividing this remainder by `m` gives the number of complete floors before the apartment, and adding one gives its one-based floor. Both calculations use the same zero-based position, so apartments at the ends of floors and entrances are assigned to the correct group.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())

apartments_per_entrance = n * m
position = k - 1

entrance = position // apartments_per_entrance + 1
floor = (position % apartments_per_entrance) // m + 1

print(entrance, floor)
```

The first line reads the three integers from the only input line. There are no multiple test cases in this problem.

`apartments_per_entrance` is the size of one complete entrance block. Although the input values are at most `10^9`, their product can reach `10^18`. Python integers have arbitrary precision, so this multiplication is safe without any special handling.

`position = k - 1` is the central implementation detail. The original apartment numbers are one-based, while division and remainder naturally describe zero-based groups. Shifting by one makes apartment `1` position `0`, apartment `m` position `m - 1`, and apartment `m + 1` position `m`. This removes the usual divisibility off-by-one errors.

The entrance calculation uses integer division by the complete entrance size. The floor calculation first takes the remainder inside the entrance, then divides by `m`. The order matters because the floor number depends only on the position within the current entrance, not on all apartments before it.

Python's integer arithmetic also avoids the overflow that a fixed-width 32-bit implementation would encounter with `n * m`. A 64-bit integer would be sufficient here as well because the maximum product is `10^18`.

## Worked Examples

For Sample 1, the input is `3 4 10`. Each entrance contains `3 * 4 = 12` apartments. The target is the tenth apartment, so its zero-based position is 9.

| `n` | `m` | `k` | Apartments per entrance | Zero-based position | Entrance | Position inside entrance | Floor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 4 | 10 | 12 | 9 | 1 | 9 | 3 |

The quotient `9 // 12` is 0, so the entrance is `0 + 1 = 1`. The remainder `9 % 12` is 9. Dividing 9 by 4 gives 2, so the floor is `2 + 1 = 3`. The result is `1 3`.

For Sample 2, the input is `5 2 20`. Each entrance contains `5 * 2 = 10` apartments. Apartment 20 has zero-based position 19.

| `n` | `m` | `k` | Apartments per entrance | Zero-based position | Entrance | Position inside entrance | Floor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 2 | 20 | 10 | 19 | 2 | 9 | 5 |

The quotient `19 // 10` is 1, giving entrance 2. The remainder is 9, which is the last position of that entrance. Since every floor has two apartments, `9 // 2` is 4, giving floor 5. The result is `2 5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed. |
| Space | O(1) | The algorithm stores only a few integer variables. |

The maximum input values do not affect the number of operations. Even when `n`, `m`, and `k` are close to `10^9`, the solution performs the same constant amount of work. The memory usage is also constant, and Python's arbitrary-precision integers safely handle the largest intermediate value, `n*m <= 10^18`.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n, m, k = map(int, input().split())

    apartments_per_entrance = n * m
    position = k - 1

    entrance = position // apartments_per_entrance + 1
    floor = (position % apartments_per_entrance) // m + 1

    print(entrance, floor)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert run("3 4 10\n") == "1 3", "sample 1"
assert run("5 2 20\n") == "2 5", "sample 2"

assert run("1 1 1\n") == "1 1", "minimum-size input"
assert run("1000000000 1000000000 1000000000\n") == "1 1", \
    "large dimensions with target in the first entrance and first floor"
assert run("3 4 12\n") == "1 3", \
    "last apartment of an entrance"
assert run("3 4 13\n") == "2 1", \
    "first apartment of the next entrance"
assert run("1000000000 1 1000000000\n") == "1 1000000000", \
    "target on the last floor when each floor has one apartment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1 1` | Minimum values and the first apartment |
| `1000000000 1000000000 1000000000` | `1 1` | Very large values and large multiplication |
| `3 4 12` | `1 3` | Last apartment of an entrance |
| `3 4 13` | `2 1` | First apartment of the next entrance |
| `1000000000 1 1000000000` | `1 1000000000` | A very large floor number |

## Edge Cases

When `k` is the first apartment, the zero-based position is zero. For input `1 1 1`, the entrance block contains one apartment, so `0 // 1 + 1 = 1`. The position inside the entrance is also zero, giving `0 // 1 + 1 = 1`. The output is `1 1`.

When `k` is exactly divisible by the number of apartments on a floor, the target is on the previous floor, not the next one. For input `3 4 8`, the zero-based position is 7. The entrance is `7 // 12 + 1 = 1`, and the floor is `7 // 4 + 1 = 2`. The output is `1 2`. A formula based directly on `k // m` would incorrectly move apartment 8 to floor 3.

When `k` is exactly the final apartment of an entrance, the target must remain in that entrance. For input `3 4 12`, the zero-based position is 11. Since `11 // 12 = 0`, the entrance is 1. The position inside the entrance is 11, and `11 // 4 + 1 = 3`, so the output is `1 3`. The zero-based shift is what makes the boundary behave correctly.

When `k` is the first apartment after an entrance boundary, the entrance must increase while the floor resets to 1. For input `3 4 13`, the zero-based position is 12. Now `12 // 12 = 1`, so the entrance is 2. The remainder is zero, giving floor `0 // 4 + 1 = 1`. The output is `2 1`.

Finally, large products must not cause arithmetic problems. For input `1000000000 1000000000 1000000000`, one entrance contains `10^18` apartments, while the target is only apartment `10^9`. Its zero-based position is `999999999`, which is still inside the first entrance and the first floor because `999999999 // 1000000000 = 0`. The output is `1 1`. The calculation is constant time despite the entrance containing an enormous number of apartments.
