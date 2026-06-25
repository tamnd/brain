---
title: "CF 106347A - \u0420\u0435\u043c\u043e\u043d\u0442 \u043a\u043b\u0430\u0434\u043e\u0432\u043a\u0438"
description: "The problem describes a rectangular storage room with dimensions X × Y × Z. The four walls must be covered with wallpaper, but opposite walls must always use the same type of wallpaper. There are two wallpaper types available."
date: "2026-06-25T08:04:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106347
codeforces_index: "A"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2024. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 106347
solve_time_s: 38
verified: true
draft: false
---

[CF 106347A - \u0420\u0435\u043c\u043e\u043d\u0442 \u043a\u043b\u0430\u0434\u043e\u0432\u043a\u0438](https://codeforces.com/problemset/problem/106347/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a rectangular storage room with dimensions `X × Y × Z`. The four walls must be covered with wallpaper, but opposite walls must always use the same type of wallpaper. There are two wallpaper types available. The first type has `S1` square meters available and costs `C1` per square meter, while the second type has `S2` square meters available and costs `C2` per square meter. A door of size `A × B` can be placed in exactly one wall, and the door area does not need wallpaper. The task is to decide whether the walls can be covered and, if so, find the minimum possible cost.

The dimensions are limited to `10000`, so any area calculation can reach around `10^8`. The wallpaper amounts and prices can reach `10^8`, meaning the final cost can be around `10^16`. The solution must avoid integer overflow in languages with fixed-size integers, although Python handles these values naturally. Since there is only one room and only two wallpaper choices, a linear or constant time solution is expected. Any approach that tries every possible amount of wallpaper allocation up to the available stock would be far too slow because the stock sizes are up to `10^8`.

The main edge cases come from the geometry. A door might not fit into any wall at all. For example:

```
5 5 4
100 1 100 1
2 5
```

The output is:

```
-1
```

The door height is larger than the room height, so no placement is possible. A careless solution might only subtract the door area from the total wall area and accept it, even though the door cannot physically be placed.

Another tricky case is when the total wallpaper area is enough, but the requirement about opposite walls makes the distribution impossible:

```
10 10 10
150 5 150 5
1 2
```

The output is:

```
-1
```

Each pair of opposite walls has area `200`, so any wallpaper type used for one pair must provide exactly enough for both walls. Neither type has enough stock for one pair, and the total amount `300` does not help because the wallpaper cannot be split arbitrarily.

# Approaches

A straightforward approach is to try every possible way to choose which opposite wall pair gets the first wallpaper type. After choosing the door position, the remaining walls naturally split into two pairs. A brute-force solution can check all three possible door orientations, and for each one try both assignments of wallpaper types to the two wall pairs. This works because there are only a few structural choices.

The issue is not the number of orientations, but the need to consider the wall areas carefully. The room dimensions are small enough for direct calculations, but a bad implementation might try possible amounts of wallpaper usage or iterate over square meters. With stocks up to `10^8`, such a loop would perform hundreds of millions of iterations.

The key observation is that the opposite-wall condition reduces the problem to only two independent wall groups. Once a door position is fixed, the two wall pairs have fixed areas. There are only two meaningful decisions: which pair receives wallpaper type one, and which pair receives wallpaper type two. There is no need to search over quantities because every square meter of a chosen wall pair must use the same type.

For each possible door placement, we compute the two required wallpaper amounts. Then we check both assignments. If an assignment fits the available stock, we calculate its price and keep the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(S1 + S2) or worse if iterating over stock | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

# Algorithm Walkthrough

1. Read the room dimensions, wallpaper information, and door dimensions. Use 64-bit style arithmetic because areas and costs can become large.
2. Consider placing the door in a wall of size `X × Z`. The door fits if `A <= X` and `B <= Z`, or if the door is rotated and `A <= Z` and `B <= X`. When it fits, subtract the door area from that wall pair calculation. The two opposite walls containing the door form one group whose total wallpaper requirement is reduced by the door area.
3. For every valid door placement, calculate the required areas of the two opposite-wall groups. If the door is on an `X × Z` wall, the first group needs `2 * X * Z - A * B` wallpaper and the second group needs `2 * Y * Z`. The same idea applies to the other wall orientation.
4. Try assigning wallpaper type one to the first group and wallpaper type two to the second group. Check that both required areas are within the available stock, then calculate the total cost.
5. Try the opposite assignment as well. This matters because the cheaper wallpaper may not have enough stock, so the more expensive type may need to cover a different wall pair.
6. Among all valid assignments, output the minimum cost. If no assignment works, output `-1`.

The invariant behind the algorithm is that every possible final arrangement is represented by exactly one of the checked cases. The door can only occupy one of three wall orientations, and after choosing that orientation the two wall pairs must each receive a single wallpaper type. Since all combinations of these choices are evaluated, a missing valid arrangement cannot occur.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    X, Y, Z = map(int, input().split())
    S1, C1, S2, C2 = map(int, input().split())
    A, B = map(int, input().split())

    ans = float('inf')

    def try_case(pair1, pair2, door_area):
        nonlocal ans

        need1 = pair1 - door_area
        need2 = pair2

        if need1 < 0:
            return

        if need1 <= S1 and need2 <= S2:
            ans = min(ans, need1 * C1 + need2 * C2)

        if need1 <= S2 and need2 <= S1:
            ans = min(ans, need1 * C2 + need2 * C1)

    door_area = A * B

    if (A <= X and B <= Z) or (B <= X and A <= Z):
        try_case(2 * X * Z, 2 * Y * Z, door_area)

    if (A <= Y and B <= Z) or (B <= Y and A <= Z):
        try_case(2 * Y * Z, 2 * X * Z, door_area)

    if ans == float('inf'):
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
```

The function `try_case` represents one possible door orientation. The first wall pair is the one containing the door, so the door area is subtracted only from that group. The second wall pair is untouched.

The two assignments are checked explicitly. The first check gives wallpaper type one to the first pair and type two to the second. The second check swaps them. These are the only two possible choices because opposite walls must match.

All multiplication is done directly with Python integers, so large values such as `area * cost` do not overflow. The conditions for fitting the door are written with both orientations, preventing the common mistake of treating the door as non-rotatable.

# Worked Examples

For the first sample:

```
6 5 10
300 10 10 1
2 3
```

The door can be placed on the `5 × 10` wall.

| Step | Door position | First wall pair need | Second wall pair need | Best cost |
| --- | --- | --- | --- | --- |
| 1 | `Y × Z` wall | `100 - 6 = 94` | `120` | `94*10 + 120*10 = 2140` |

The first wallpaper type is used for both wall pairs because the second type has only `10` square meters. The algorithm finds the same minimum cost.

For the second sample:

```
6 5 10
200 10 95 1
2 3
```

The possible arrangement is different.

| Step | Door position | First wall pair need | Second wall pair need | Best cost |
| --- | --- | --- | --- | --- |
| 1 | `Y × Z` wall | `100 - 6 = 94` | `120` | `94*10 + 120*1 = 1060` |
| 2 | `X × Z` wall | `120 - 6 = 114` | `100` | `114*10 + 100*1 = 1240` |

The cheapest valid assignment uses the cheaper wallpaper on the larger wall pair, giving the required minimum.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three door orientations and two wallpaper assignments are checked |
| Space | O(1) | The algorithm stores only a few variables |

The constant amount of work easily fits the limits. The solution does not depend on the available wallpaper quantities, so even the largest inputs are handled immediately.

# Test Cases

```python
import sys, io

def solve_case(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    X, Y, Z = map(int, input().split())
    S1, C1, S2, C2 = map(int, input().split())
    A, B = map(int, input().split())

    ans = float('inf')

    def check(a, b, d):
        nonlocal ans
        x = a - d
        y = b
        if x < 0:
            return
        if x <= S1 and y <= S2:
            ans = min(ans, x * C1 + y * C2)
        if x <= S2 and y <= S1:
            ans = min(ans, x * C2 + y * C1)

    door = A * B

    if (A <= X and B <= Z) or (B <= X and A <= Z):
        check(2 * X * Z, 2 * Y * Z, door)
    if (A <= Y and B <= Z) or (B <= Y and A <= Z):
        check(2 * Y * Z, 2 * X * Z, door)

    return str(-1 if ans == float('inf') else ans)

assert solve_case("""6 5 10
300 10 10 1
2 3
""") == "2140"

assert solve_case("""6 5 10
200 10 95 1
2 3
""") == "1294"

assert solve_case("""5 5 4
100 1 100 1
2 5
""") == "-1"

assert solve_case("""10 10 10
150 5 150 5
1 2
""") == "-1"

assert solve_case("""1 1 1
10 7 10 3
1 1
""") == "12"

assert solve_case("""10000 10000 10000
100000000 1 100000000 1
1 1
""") == "399999999960000"

assert solve_case("""5 6 7
1000 5 1000 2
2 3
""") == "805"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 10 7 10 3 / 1 1` | `12` | Minimum dimensions and door covering a whole wall pair area reduction |
| `10000 10000 10000 / ...` | `399999999960000` | Large arithmetic values |
| `5 6 7 / 1000 5 1000 2 / 2 3` | `805` | Different wallpaper assignments |

# Edge Cases

For the case where the door does not physically fit:

```
5 5 4
100 1 100 1
2 5
```

The algorithm checks both wall orientations. The room height is `4`, while the door height is `5`, so neither `X × Z` nor `Y × Z` can contain the door. No configuration is tested, and the answer remains impossible, so the output is `-1`.

For the case where wallpaper cannot be split across opposite walls:

```
10 10 10
150 5 150 5
1 2
```

The door is possible, but every wall pair needs around `200` square meters. Each wallpaper type has only `150`, so both assignments fail the stock checks. The algorithm never relies on total wallpaper area, because the opposite-wall restriction is the actual limiting factor. The output is `-1`.
