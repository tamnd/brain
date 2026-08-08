---
title: "CF 102437J - Delivery Robot"
description: "The robot starts at an integer point ((x1,y1)) and has to reach another integer point ((x2,y2)). There are two fixed radio towers, at (A=(0,0)) and (B=(1,0))."
date: "2026-08-09T00:41:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "J"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 725
verified: false
draft: false
---

[CF 102437J - Delivery Robot](https://codeforces.com/problemset/problem/102437/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 5s  
**Verified:** no  

## Solution
## Problem Understanding

The robot starts at an integer point ((x_1,y_1)) and has to reach another integer point ((x_2,y_2)). There are two fixed radio towers, at (A=(0,0)) and (B=(1,0)). Each command rotates the robot's current position by exactly (90^\circ), either clockwise or counterclockwise, around one of these two towers.

The four commands are thus affine transformations of the plane. Around (A), commands 1 and 2 perform clockwise and counterclockwise rotations. Around (B), commands 3 and 4 do the same. We only have to print a sequence of command numbers that reaches the destination, and its length must not exceed (10^6). Finding the shortest sequence is unnecessary.

The coordinates are bounded by (100000) in absolute value. The direct difference between two coordinates is consequently at most (200000). A solution that performs a number of operations proportional to this difference is easily fast enough, while exploring arbitrary command sequences is hopeless. The official limits are 2 seconds and 512 MB, so an algorithm with millions of simple operations is comfortable, whereas exponential search is completely ruled out.

The first non-obvious case is that some destinations are fundamentally unreachable. For example,

```
0 1
1 1
```

has no solution. The reason is not that a particular search failed to find one. Every command preserves the parity of (x+y), while the starting point has (x+y=1) and the destination has (x+y=2). A careless BFS with an arbitrary coordinate cutoff could report `-1` without identifying the actual invariant, or a construction based only on coordinate differences could accidentally attempt to use half-integer numbers of translations.

Another edge case is when both coordinate differences are even. For example,

```
0 0
2 0
```

is reachable even though moving directly in the positive (x)-direction is not one of the available operations. The construction must combine two diagonal translations. Here the difference is ((2,0)), which can be decomposed as ((1,1)+(1,-1)).

The final edge case is a negative difference. For example,

```
0 0
-1 -1
```

is reachable, but using the positive translation generator in the wrong direction would move the robot away from the target. The construction therefore needs inverse translation sequences as well.

## Approaches

A straightforward approach is to treat every integer point as a graph vertex and every command as an edge. From a point there are exactly four possible next points, so BFS would find a shortest sequence whenever one exists. This is correct because the effect of every command depends only on the current point, and BFS explores command sequences in increasing length.

The problem is the size of that search. In the worst case a naive exhaustive search over command sequences of length at most (10^6) considers

\Theta(4^{10^6})
]

sequences. Even BFS, which merges sequences that reach the same point, has no reason to be competitive without first exploiting the geometry. The useful reachable region can contain quadratically many lattice points in the required distance, so searching it explicitly is still far too large.

The key observation is that two rotations around different towers can cancel their rotational part and leave a pure translation.

Let command 1 be the clockwise rotation around (A), and command 4 the counterclockwise rotation around (B). Applying command 1 and then command 4 moves every point by exactly ((1,-1)). Similarly, command 2 followed by command 3 moves every point by exactly ((1,1)).

The inverse translations are also available. Commands 3 then 1 translate by ((-1,-1)), while commands 3 then 2 translate by ((-1,1)).

This reduces the entire problem to expressing the required displacement as a combination of the two vectors

[
(1,1)
\quad\text{and}\quad
(1,-1).
]

For

[
dx=x_2-x_1,\qquad dy=y_2-y_1,
]

we need

[
dx=a+b,\qquad dy=a-b.
]

Solving gives

[
a=\frac{dx+dy}{2},\qquad
b=\frac{dx-dy}{2}.
]

These are integers exactly when (dx) and (dy) have the same parity. That condition is equivalent to

[
x_1+y_1\equiv x_2+y_2\pmod 2.
]

So the same parity condition that appears as an invariant is also sufficient, because whenever it holds we can explicitly construct the required translation.

Each unit of (a) or (b) costs exactly two commands. Since

# \frac{|dx+dy|+|dx-dy|}{2}

\max(|dx|,|dy|),
]

the final sequence has length

[
2\max(|dx|,|dy|)\le 400000,
]

well below the (10^6) limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(4^{10^6})) sequences in the worst case | (O(10^6)) for a DFS stack | Too slow |
| Optimal | (O(\max( | dx | , | dy | ))) | (O(\max( | dx | , | dy | ))) for the output | Accepted |

## Algorithm Walkthrough

1. Compute the displacement

[
dx=x_2-x_1,\qquad dy=y_2-y_1.
]

The construction only needs to know how far the target is from the starting point.
2. Check the parity of (dx) and (dy). If they have different parity, print `-1`.

This is the reachability test. A rotation by (90^\circ) around either tower preserves the parity of (x+y), so changing that parity is impossible.
3. Compute

[
a=(dx+dy)/2,\qquad b=(dx-dy)/2.
]

The value (a) tells us how many times to use the diagonal translation ((1,1)), while (b) tells us how many times to use ((1,-1)).
4. If (a>0), append command pair `23` exactly (a) times. If (a<0), append `31` exactly (-a) times.

The pair `23` is a translation by ((1,1)), and `31` is its inverse, a translation by ((-1,-1)).
5. If (b>0), append command pair `14` exactly (b) times. If (b<0), append `32` exactly (-b) times.

The pair `14` translates by ((1,-1)), while `32` translates by ((-1,1)).
6. Print the resulting command string.

Both generators are translations, so their order does not matter. Their combined displacement is

# (a+b,a-b)

(dx,dy),
]

exactly the displacement from the starting point to the destination.

### Why it works

The central invariant is the parity of (x+y). A clockwise or counterclockwise rotation around (A=(0,0)) changes ((x,y)) to either ((-y,x)) or ((y,-x)), and both new coordinate sums have the same parity as (x+y). Around (B=(1,0)), the two possible results are ((1+y,1-x)) and ((1-y,1+x)), whose coordinate sums also have the same parity as (x+y). Thus different parities can never be connected.

When the parities agree, (dx) and (dy) have the same parity, so (a) and (b) are integers. The command pairs `23`, `31`, `14`, and `32` realize the four signed diagonal translations. Their combined displacement is exactly ((dx,dy)), so the constructed sequence always reaches the destination. Its length is at most (400000), so it also satisfies the command limit.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x1, y1 = map(int, input().split())
    x2, y2 = map(int, input().split())

    dx = x2 - x1
    dy = y2 - y1

    # Reachability invariant: x + y modulo 2 is preserved.
    if (dx - dy) % 2 != 0:
        print(-1)
        return

    a = (dx + dy) // 2
    b = (dx - dy) // 2

    ans = []

    if a > 0:
        ans.append("23" * a)
    elif a < 0:
        ans.append("31" * (-a))

    if b > 0:
        ans.append("14" * b)
    elif b < 0:
        ans.append("32" * (-b))

    s = "".join(ans)

    print(len(s))
    print(s)

if __name__ == "__main__":
    solve()
```

The first two lines read the starting and target coordinates. There is only one test case, so no test-case loop is needed.

The parity test uses `(dx - dy) % 2 != 0`. This is equivalent to checking whether (dx) and (dy) have different parity. Python's integer arithmetic is exact, so there is no overflow issue even if the coordinates are at their limits.

The values `a` and `b` are computed only after the parity test. This matters because division by two must produce integers. The four command pairs are then selected according to the sign of each coefficient.

The strings are repeated directly instead of simulating every intermediate coordinate. The pair `23` is appended `a` times when (a) is positive, for example, so it contributes (a(1,1)). When (a) is negative, `31` supplies the opposite vector.

The starting and target points are guaranteed to differ. Consequently, when the parity condition succeeds, (a) and (b) cannot both be zero, so the produced command string is non-empty as required.

The largest possible coordinate difference is (200000), so the output contains at most (400000) characters. This is safely below the required (10^6) commands.

## Worked Examples

For the first sample,

```
0 1
1 -2
```

we have (dx=1) and (dy=-3). The parity condition succeeds because both differences are odd.

| Step | (dx) | (dy) | (a=(dx+dy)/2) | (b=(dx-dy)/2) | Action |
| --- | --- | --- | --- | --- | --- |
| Initial | 1 | -3 | -1 | 2 | Compute coefficients |
| After `31` | 1 | -3 | -1 | 2 | Add ((-1,-1)) |
| After `14` | 1 | -3 | -1 | 2 | Add ((1,-1)) |
| After `14` | 1 | -3 | -1 | 2 | Add ((1,-1)) |

The resulting translation is

[
(-1,-1)+(1,-1)+(1,-1)=(1,-3),
]

so the robot reaches ((1,-2)) from ((0,1)). One valid output is `311414`, although the official sample uses the shorter sequence `24`. The task accepts any valid sequence.

For the second sample,

```
0 1
1 1
```

the displacement is ((1,0)).

| Step | (dx) | (dy) | (dx\bmod2) | (dy\bmod2) | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | 1 | 0 | 1 | 0 | Different parity |
| Parity check | 1 | 0 | 1 | 0 | Print `-1` |

The robot cannot reach this point because (x+y) changes from (1) to (2). The algorithm rejects it before attempting to construct a sequence. This is exactly the official second sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\max( | dx | , | dy | ))) | Constructing the output string writes at most (400000) commands. |
| Space | (O(\max( | dx | , | dy | ))) | The command sequence itself occupies at most (400000) characters. |

Because each coordinate lies between (-100000) and (100000), each difference has absolute value at most (200000). The construction therefore emits at most (400000) commands, which is comfortably below the (10^6) limit. The algorithm performs only constant additional work beyond building the required output.

## Test Cases

The following tests validate the construction rather than comparing the exact command string, because the problem allows any valid sequence. The helper simulates all four commands and checks the final position.

```python
import sys
import io

def solution(inp: str) -> str:
    data = inp.split()
    x1, y1, x2, y2 = map(int, data)

    dx = x2 - x1
    dy = y2 - y1

    if (dx - dy) % 2 != 0:
        return "-1\n"

    a = (dx + dy) // 2
    b = (dx - dy) // 2

    ans = []

    if a > 0:
        ans.append("23" * a)
    elif a < 0:
        ans.append("31" * (-a))

    if b > 0:
        ans.append("14" * b)
    elif b < 0:
        ans.append("32" * (-b))

    s = "".join(ans)
    return f"{len(s)}\n{s}\n"

def run(inp: str) -> str:
    return solution(inp)

def simulate(inp: str, out: str):
    x1, y1, x2, y2 = map(int, inp.split())

    if out.strip() == "-1":
        assert (x2 - x1 - (y2 - y1)) % 2 != 0
        return

    lines = out.splitlines()
    k = int(lines[0])
    s = lines[1].strip()

    assert k == len(s)
    assert 0 < k <= 10**6
    assert all(c in "1234" for c in s)

    x, y = x1, y1

    for c in s:
        if c == "1":
            x, y = -y, x
        elif c == "2":
            x, y = y, -x
        elif c == "3":
            dx = x - 1
            dy = y
            x = 1 + dy
            y = -dx
        else:
            dx = x - 1
            dy = y
            x = 1 - dy
            y = dx

    assert (x, y) == (x2, y2)

# Provided sample 1.
inp = "0 1 1 -2\n"
out = run(inp)
simulate(inp, out)

# Provided sample 2.
inp = "0 1 1 1\n"
assert run(inp).strip() == "-1"

# Minimum-size displacement.
inp = "0 0 1 1\n"
out = run(inp)
simulate(inp, out)

# Equal coordinate differences.
inp = "5 5 7 7\n"
out = run(inp)
simulate(inp, out)

# Negative diagonal displacement.
inp = "0 0 -1 -1\n"
out = run(inp)
simulate(inp, out)

# Boundary-size construction.
inp = "-100000 -100000 100000 100000\n"
out = run(inp)
simulate(inp, out)
assert int(out.splitlines()[0]) == 400000

# Off-by-one style case: (2, 0) requires both generators.
inp = "0 0 2 0\n"
out = run(inp)
simulate(inp, out)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 1 1 -2` | Any valid sequence | Provided reachable sample |
| `0 1 1 1` | `-1` | Parity invariant |
| `0 0 1 1` | Any valid sequence of length 2 | Smallest nonzero diagonal translation |
| `5 5 7 7` | Any valid sequence | Equal positive coordinate differences |
| `0 0 -1 -1` | Any valid sequence of length 2 | Negative coefficient and inverse generator |
| `-100000 -100000 100000 100000` | Any valid sequence of length 400000 | Maximum coordinate differences and output bound |
| `0 0 2 0` | Any valid sequence | Combining the two diagonal generators |

## Edge Cases

The unreachable parity case is handled before any construction. For

```
0 1
1 1
```

we get (dx=1) and (dy=0). Their parities differ, so the algorithm prints `-1`. This is correct because every command preserves (x+y) modulo 2.

For an even displacement such as

```
0 0
2 0
```

we obtain

[
a=(2+0)/2=1,\qquad b=(2-0)/2=1.
]

The algorithm outputs `2314`. The pair `23` moves by ((1,1)), and `14` moves by ((1,-1)), giving a total displacement of ((2,0)). This catches the common mistake of assuming that each coordinate must be changed independently.

For a negative displacement,

```
0 0
-1 -1
```

we get (a=-1) and (b=0). The algorithm uses `31`, which is the inverse of `23` and translates by ((-1,-1)). A sign error here would instead move the robot to ((1,1)).

For the maximum-size case,

```
-100000 -100000
100000 100000
```

we have (dx=dy=200000), so (a=200000) and (b=0). The algorithm emits `23` repeated (200000) times, producing exactly (400000) commands. This is safely below (10^6), so even the largest allowed coordinate difference is handled without a special case.

Finally, the starting point is guaranteed to differ from the destination. Once the parity test passes, that means ((dx,dy)\ne(0,0)), so at least one of (a) and (b) is nonzero. The resulting command sequence is consequently positive in length, satisfying the output requirement without needing an artificial extra pair of commands.
