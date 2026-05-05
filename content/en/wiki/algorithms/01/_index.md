## Searching and Sorting

This 350 page list is usable as the final page inventory for **Searching and Sorting**.

Total check:

| category                                       | count | range   |
| ---------------------------------------------- | ----: | ------- |
| Linear and sequential search                   |    20 | 1-20    |
| Binary search and ordered search               |    35 | 21-55   |
| Hashing and table search                       |    25 | 56-80   |
| Tree and indexed search                        |    35 | 81-115  |
| Selection and order statistics                 |    35 | 116-150 |
| Elementary sorting                             |    30 | 151-180 |
| Divide and conquer sorting                     |    35 | 181-215 |
| Integer and distribution sorting               |    40 | 216-255 |
| Partial, online, and adaptive sorting          |    30 | 256-285 |
| External memory, cache, and database sorting   |    25 | 286-310 |
| Parallel, distributed, and GPU sorting         |    25 | 311-335 |
| Specialized search and sorted-order procedures |    15 | 336-350 |



One small cleanup: item 211, `akra-bazzi-merge-sort-variant`, feels more like an analysis technique than a named sorting algorithm. Better replacement:

| old                           | new                        |
| ----------------------------- | -------------------------- |
| Akra Bazzi Merge Sort Variant | Cache Efficient Merge Sort |



### 6. Elementary sorting, 30

| index | slug                      | name                           |
| ----: | ------------------------- | ------------------------------ |
|   151 | bubble-sort               | Bubble Sort                    |
|   152 | optimized-bubble-sort     | Optimized Bubble Sort          |
|   153 | cocktail-shaker-sort      | Cocktail Shaker Sort           |
|   154 | odd-even-sort             | Odd Even Sort                  |
|   155 | gnome-sort                | Gnome Sort                     |
|   156 | selection-sort            | Selection Sort                 |
|   157 | stable-selection-sort     | Stable Selection Sort          |
|   158 | double-selection-sort     | Double Selection Sort          |
|   159 | insertion-sort            | Insertion Sort                 |
|   160 | binary-insertion-sort     | Binary Insertion Sort          |
|   161 | shell-sort                | Shell Sort                     |
|   162 | shell-sort-shell-gaps     | Shell Sort with Shell Gaps     |
|   163 | shell-sort-hibbard-gaps   | Shell Sort with Hibbard Gaps   |
|   164 | shell-sort-sedgewick-gaps | Shell Sort with Sedgewick Gaps |
|   165 | comb-sort                 | Comb Sort                      |
|   166 | cycle-sort                | Cycle Sort                     |
|   167 | pancake-sort              | Pancake Sort                   |
|   168 | stooge-sort               | Stooge Sort                    |
|   169 | slow-sort                 | Slow Sort                      |
|   170 | bead-sort                 | Bead Sort                      |
|   171 | strand-sort               | Strand Sort                    |
|   172 | library-sort              | Library Sort                   |
|   173 | patience-sort             | Patience Sort                  |
|   174 | tree-sort                 | Tree Sort                      |
|   175 | tournament-sort           | Tournament Sort                |
|   176 | smoothsort                | Smoothsort                     |
|   177 | weak-heap-sort            | Weak Heap Sort                 |
|   178 | cartesian-tree-sort       | Cartesian Tree Sort            |
|   179 | bingo-sort                | Bingo Sort                     |
|   180 | exchange-sort             | Exchange Sort                  |

### 7. Divide and conquer sorting, 35

| index | slug                          | name                          |
| ----: | ----------------------------- | ----------------------------- |
|   181 | merge-sort                    | Merge Sort                    |
|   182 | top-down-merge-sort           | Top Down Merge Sort           |
|   183 | bottom-up-merge-sort          | Bottom Up Merge Sort          |
|   184 | natural-merge-sort            | Natural Merge Sort            |
|   185 | in-place-merge-sort           | In Place Merge Sort           |
|   186 | block-merge-sort              | Block Merge Sort              |
|   187 | timsort                       | Timsort                       |
|   188 | powersort                     | Powersort                     |
|   189 | quicksort                     | Quicksort                     |
|   190 | randomized-quicksort          | Randomized Quicksort          |
|   191 | three-way-quicksort           | Three Way Quicksort           |
|   192 | dual-pivot-quicksort          | Dual Pivot Quicksort          |
|   193 | introsort                     | Introsort                     |
|   194 | pdqsort                       | Pattern Defeating Quicksort   |
|   195 | block-quicksort               | Block Quicksort               |
|   196 | stable-quicksort              | Stable Quicksort              |
|   197 | quicksort-median-of-three     | Quicksort Median of Three     |
|   198 | quicksort-ninther             | Quicksort Ninther             |
|   199 | quicksort-hoare-partition     | Hoare Partition Quicksort     |
|   200 | quicksort-lomuto-partition    | Lomuto Partition Quicksort    |
|   201 | heapsort                      | Heapsort                      |
|   202 | bottom-up-heapsort            | Bottom Up Heapsort            |
|   203 | ternary-heapsort              | Ternary Heapsort              |
|   204 | weak-heapsort                 | Weak Heapsort                 |
|   205 | merge-insertion-sort          | Merge Insertion Sort          |
|   206 | ford-johnson-sort             | Ford Johnson Sort             |
|   207 | bitonic-sort                  | Bitonic Sort                  |
|   208 | odd-even-merge-sort           | Odd Even Merge Sort           |
|   209 | pairwise-sorting-network      | Pairwise Sorting Network      |
|   210 | batcher-merge-sort            | Batcher Merge Sort            |
|   211 | akra-bazzi-merge-sort-variant | Akra Bazzi Merge Sort Variant |
|   212 | cache-oblivious-merge-sort    | Cache Oblivious Merge Sort    |
|   213 | sample-sort                   | Sample Sort                   |
|   214 | multiway-merge-sort           | Multiway Merge Sort           |
|   215 | tournament-merge-sort         | Tournament Merge Sort         |

### 8. Integer and distribution sorting, 40

| index | slug                        | name                             |
| ----: | --------------------------- | -------------------------------- |
|   216 | counting-sort               | Counting Sort                    |
|   217 | stable-counting-sort        | Stable Counting Sort             |
|   218 | key-indexed-counting        | Key Indexed Counting             |
|   219 | radix-sort                  | Radix Sort                       |
|   220 | lsd-radix-sort              | LSD Radix Sort                   |
|   221 | msd-radix-sort              | MSD Radix Sort                   |
|   222 | american-flag-sort          | American Flag Sort               |
|   223 | in-place-radix-sort         | In Place Radix Sort              |
|   224 | binary-radix-sort           | Binary Radix Sort                |
|   225 | burstsort                   | Burstsort                        |
|   226 | bucket-sort                 | Bucket Sort                      |
|   227 | uniform-bucket-sort         | Uniform Bucket Sort              |
|   228 | histogram-sort              | Histogram Sort                   |
|   229 | pigeonhole-sort             | Pigeonhole Sort                  |
|   230 | flashsort                   | Flashsort                        |
|   231 | spreadsort                  | Spreadsort                       |
|   232 | burstsort-string-sorting    | Burstsort String Sorting         |
|   233 | radix-exchange-sort         | Radix Exchange Sort              |
|   234 | ska-sort                    | Ska Sort                         |
|   235 | ips4o                       | IPS4o                            |
|   236 | integer-sample-sort         | Integer Sample Sort              |
|   237 | word-radix-sort             | Word Radix Sort                  |
|   238 | bytewise-radix-sort         | Bytewise Radix Sort              |
|   239 | most-significant-byte-sort  | Most Significant Byte Sort       |
|   240 | least-significant-byte-sort | Least Significant Byte Sort      |
|   241 | american-flag-string-sort   | American Flag String Sort        |
|   242 | multikey-quicksort          | Multikey Quicksort               |
|   243 | three-way-string-quicksort  | Three Way String Quicksort       |
|   244 | suffix-array-doubling-sort  | Suffix Array Doubling Sort       |
|   245 | suffix-array-radix-sort     | Suffix Array Radix Sort          |
|   246 | induced-sorting             | Induced Sorting                  |
|   247 | sais                        | SA IS                            |
|   248 | skew-suffix-array-sort      | Skew Suffix Array Sort           |
|   249 | dc3-suffix-array-sort       | DC3 Suffix Array Sort            |
|   250 | dc7-suffix-array-sort       | DC7 Suffix Array Sort            |
|   251 | counting-sort-negative-keys | Counting Sort with Negative Keys |
|   252 | coordinate-compression-sort | Coordinate Compression Sort      |
|   253 | sparse-key-counting-sort    | Sparse Key Counting Sort         |
|   254 | radix-sort-floating-point   | Floating Point Radix Sort        |
|   255 | signed-integer-radix-sort   | Signed Integer Radix Sort        |

### 9. Partial, online, and adaptive sorting, 30

| index | slug                           | name                           |
| ----: | ------------------------------ | ------------------------------ |
|   256 | partial-sort                   | Partial Sort                   |
|   257 | top-k-sort                     | Top K Sort                     |
|   258 | incremental-sort               | Incremental Sort               |
|   259 | online-insertion-sort          | Online Insertion Sort          |
|   260 | adaptive-merge-sort            | Adaptive Merge Sort            |
|   261 | natural-runs-sort              | Natural Runs Sort              |
|   262 | patience-sorting-lis           | Patience Sorting for LIS       |
|   263 | replacement-selection          | Replacement Selection          |
|   264 | nearly-sorted-insertion-sort   | Nearly Sorted Insertion Sort   |
|   265 | k-sorted-array-sort            | K Sorted Array Sort            |
|   266 | min-heap-k-sorted-sort         | Min Heap K Sorted Sort         |
|   267 | timsort-run-detection          | Timsort Run Detection          |
|   268 | galloping-merge                | Galloping Merge                |
|   269 | adaptive-samplesort            | Adaptive Samplesort            |
|   270 | adaptive-shivers-sort          | Adaptive Shivers Sort          |
|   271 | patience-sort-with-piles       | Patience Sort with Piles       |
|   272 | online-topological-sort        | Online Topological Sort        |
|   273 | insertion-sort-with-sentinel   | Insertion Sort with Sentinel   |
|   274 | binary-tree-online-sort        | Binary Tree Online Sort        |
|   275 | stream-sort-by-buffer          | Stream Sort by Buffer          |
|   276 | sliding-window-sort            | Sliding Window Sort            |
|   277 | rolling-median-sort            | Rolling Median Sort            |
|   278 | external-replacement-selection | External Replacement Selection |
|   279 | adaptive-heap-sort             | Adaptive Heap Sort             |
|   280 | smoothsort-adaptive-heap-sort  | Smoothsort Adaptive Heap Sort  |
|   281 | cartesian-tree-adaptive-sort   | Cartesian Tree Adaptive Sort   |
|   282 | tournament-tree-partial-sort   | Tournament Tree Partial Sort   |
|   283 | lazy-sort                      | Lazy Sort                      |
|   284 | lazy-selection-sort            | Lazy Selection Sort            |
|   285 | order-maintenance-sort         | Order Maintenance Sort         |

### 10. External memory, cache, and database sorting, 25

| index | slug                                 | name                                 |
| ----: | ------------------------------------ | ------------------------------------ |
|   286 | external-merge-sort                  | External Merge Sort                  |
|   287 | two-phase-multiway-merge-sort        | Two Phase Multiway Merge Sort        |
|   288 | polyphase-merge-sort                 | Polyphase Merge Sort                 |
|   289 | balanced-k-way-merge-sort            | Balanced K Way Merge Sort            |
|   290 | cascade-merge-sort                   | Cascade Merge Sort                   |
|   291 | distribution-sweeping-sort           | Distribution Sweeping Sort           |
|   292 | cache-aware-sorting                  | Cache Aware Sorting                  |
|   293 | cache-oblivious-sorting              | Cache Oblivious Sorting              |
|   294 | funnel-sort                          | Funnel Sort                          |
|   295 | buffer-tree-sort                     | Buffer Tree Sort                     |
|   296 | b-tree-bulk-load-sort                | B Tree Bulk Load Sort                |
|   297 | lsm-tree-compaction-sort             | LSM Tree Compaction Sort             |
|   298 | database-external-sort               | Database External Sort               |
|   299 | sort-merge-join-sort-phase           | Sort Merge Join Sort Phase           |
|   300 | replacement-selection-run-generation | Replacement Selection Run Generation |
|   301 | tape-merge-sort                      | Tape Merge Sort                      |
|   302 | memory-mapped-external-sort          | Memory Mapped External Sort          |
|   303 | chunked-sort                         | Chunked Sort                         |
|   304 | spill-sort                           | Spill Sort                           |
|   305 | parallel-external-merge-sort         | Parallel External Merge Sort         |
|   306 | external-radix-sort                  | External Radix Sort                  |
|   307 | external-sample-sort                 | External Sample Sort                 |
|   308 | external-bucket-sort                 | External Bucket Sort                 |
|   309 | k-way-loser-tree-merge               | K Way Loser Tree Merge               |
|   310 | k-way-winner-tree-merge              | K Way Winner Tree Merge              |

### 11. Parallel, distributed, and GPU sorting, 25

| index | slug                             | name                                 |
| ----: | -------------------------------- | ------------------------------------ |
|   311 | parallel-merge-sort              | Parallel Merge Sort                  |
|   312 | parallel-quicksort               | Parallel Quicksort                   |
|   313 | parallel-sample-sort             | Parallel Sample Sort                 |
|   314 | parallel-radix-sort              | Parallel Radix Sort                  |
|   315 | parallel-bitonic-sort            | Parallel Bitonic Sort                |
|   316 | parallel-odd-even-sort           | Parallel Odd Even Sort               |
|   317 | parallel-counting-sort           | Parallel Counting Sort               |
|   318 | gpu-bitonic-sort                 | GPU Bitonic Sort                     |
|   319 | gpu-radix-sort                   | GPU Radix Sort                       |
|   320 | gpu-merge-sort                   | GPU Merge Sort                       |
|   321 | gpu-sample-sort                  | GPU Sample Sort                      |
|   322 | cuda-warp-sort                   | CUDA Warp Sort                       |
|   323 | cuda-block-sort                  | CUDA Block Sort                      |
|   324 | simd-bitonic-sort                | SIMD Bitonic Sort                    |
|   325 | simd-sorting-network             | SIMD Sorting Network                 |
|   326 | bitonic-sorting-network          | Bitonic Sorting Network              |
|   327 | odd-even-sorting-network         | Odd Even Sorting Network             |
|   328 | bitonic-merge-network            | Bitonic Merge Network                |
|   329 | mapreduce-sort                   | MapReduce Sort                       |
|   330 | terasort                         | TeraSort                             |
|   331 | distributed-sample-sort          | Distributed Sample Sort              |
|   332 | distributed-range-partition-sort | Distributed Range Partition Sort     |
|   333 | psrs                             | Parallel Sorting by Regular Sampling |
|   334 | bitonic-sort-on-hypercube        | Bitonic Sort on Hypercube            |
|   335 | shear-sort                       | Shear Sort                           |

### 12. Specialized search and sorted-order procedures, 15

| index | slug                                     | name                               |
| ----: | ---------------------------------------- | ---------------------------------- |
|   336 | exponential-backoff-search               | Exponential Backoff Search         |
|   337 | finger-search                            | Finger Search                      |
|   338 | interpolation-sequential-search          | Interpolation Sequential Search    |
|   339 | learned-index-search                     | Learned Index Search               |
|   340 | recursive-model-index-search             | Recursive Model Index Search       |
|   341 | binary-search-with-branchless-comparison | Branchless Binary Search           |
|   342 | eytzinger-layout-search                  | Eytzinger Layout Search            |
|   343 | van-emde-boas-layout-search              | Van Emde Boas Layout Search        |
|   344 | cache-aware-binary-search                | Cache Aware Binary Search          |
|   345 | branchless-lower-bound                   | Branchless Lower Bound             |
|   346 | simd-linear-search                       | SIMD Linear Search                 |
|   347 | simd-binary-search                       | SIMD Binary Search                 |
|   348 | interpolation-search-with-fallback       | Interpolation Search with Fallback |
|   349 | galloping-intersection-search            | Galloping Intersection Search      |
|   350 | merge-path-search                        | Merge Path Search                  |
