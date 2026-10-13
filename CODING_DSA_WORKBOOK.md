# FAANG / MANGA Coding & DSA Master Patterns Workbook
## Candidate: Gunaseelan N | 15 High-Frequency LeetCode Patterns with Production Java Implementations

---

# Pattern 1: Sliding Window (Dynamic Length)
### Problem: Minimum Window Substring (LeetCode 76 - Hard)
* **Frequency**: Meta, Google, Amazon.
* **Core Idea**: Expand `right` pointer until window contains all required characters; contract `left` pointer to find minimum valid window.

```java
import java.util.*;

public class MinimumWindowSubstring {
    public static String minWindow(String s, String t) {
        if (s == null || t == null || s.length() < t.length()) return "";

        int[] targetMap = new int[128];
        for (char c : t.toCharArray()) {
            targetMap[c]++;
        }

        int required = 0;
        for (int count : targetMap) {
            if (count > 0) required++;
        }

        int[] windowMap = new int[128];
        int formed = 0;
        int left = 0, right = 0;
        int minLen = Integer.MAX_VALUE;
        int minLeft = 0;

        while (right < s.length()) {
            char rChar = s.charAt(right);
            windowMap[rChar]++;

            if (targetMap[rChar] > 0 && windowMap[rChar] == targetMap[rChar]) {
                formed++;
            }

            while (left <= right && formed == required) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    minLeft = left;
                }

                char lChar = s.charAt(left);
                windowMap[lChar]--;
                if (targetMap[lChar] > 0 && windowMap[lChar] < targetMap[lChar]) {
                    formed--;
                }
                left++;
            }
            right++;
        }

        return minLen == Integer.MAX_VALUE ? "" : s.substring(minLeft, minLeft + minLen);
    }
}
```
* **Complexity**: Time: $O(M + N)$, Space: $O(1)$ (constant 128 array).

---

# Pattern 2: Monotonic Stack
### Problem: Daily Temperatures (LeetCode 739 - Medium)
* **Frequency**: Google, Amazon, Apple.
* **Core Idea**: Store indices of unresolved elements in a strictly decreasing stack. When a larger element arrives, pop and resolve distances.

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class DailyTemperatures {
    public static int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>(); // stores indices

        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int prevIndex = stack.pop();
                result[prevIndex] = i - prevIndex;
            }
            stack.push(i);
        }
        return result;
    }
}
```
* **Complexity**: Time: $O(N)$ (each index pushed and popped at most once), Space: $O(N)$.

---

# Pattern 3: Topological Sort via Kahn's Algorithm (BFS)
### Problem: Course Schedule II / Task Dependency Resolution (LeetCode 210 - Medium)
* **Frequency**: Google, Meta, Microsoft (Directly mirrors job scheduling workflows!).

```java
import java.util.*;

public class TaskDependencyScheduler {
    public static int[] findOrder(int numTasks, int[][] dependencies) {
        List<List<Integer>> graph = new ArrayList<>();
        int[] inDegree = new int[numTasks];

        for (int i = 0; i < numTasks; i++) {
            graph.add(new ArrayList<>());
        }

        for (int[] dep : dependencies) {
            int task = dep[0];
            int prerequisite = dep[1];
            graph.get(prerequisite).add(task);
            inDegree[task]++;
        }

        Queue<Integer> queue = new ArrayDeque<>();
        for (int i = 0; i < numTasks; i++) {
            if (inDegree[i] == 0) {
                queue.offer(i);
            }
        }

        int[] executionOrder = new int[numTasks];
        int visitedCount = 0;

        while (!queue.isEmpty()) {
            int curr = queue.poll();
            executionOrder[visitedCount++] = curr;

            for (int neighbor : graph.get(curr)) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    queue.offer(neighbor);
                }
            }
        }

        return visitedCount == numTasks ? executionOrder : new int[0]; // Empty if cycle detected
    }
}
```
* **Complexity**: Time: $O(V + E)$, Space: $O(V + E)$.

---

# Pattern 4: Top 'K' Elements via Heap
### Problem: Merge k Sorted Lists (LeetCode 23 - Hard)
* **Frequency**: Amazon, Meta, Google.

```java
import java.util.PriorityQueue;

public class MergeKSortedLists {
    public static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public static ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));

        for (ListNode head : lists) {
            if (head != null) {
                pq.offer(head);
            }
        }

        ListNode dummy = new ListNode(0);
        ListNode current = dummy;

        while (!pq.isEmpty()) {
            ListNode node = pq.poll();
            current.next = node;
            current = current.next;

            if (node.next != null) {
                pq.offer(node.next);
            }
        }

        return dummy.next;
    }
}
```
* **Complexity**: Time: $O(N \log K)$ where $N$ is total nodes and $K$ is number of lists, Space: $O(K)$.

---

# Pattern 5: Dynamic Programming (Memoization & Tabulation)
### Problem: Word Break (LeetCode 139 - Medium)
* **Frequency**: Meta, Amazon, Google.

```java
import java.util.*;

public class WordBreak {
    public static boolean wordBreak(String s, List<String> wordDict) {
        Set<String> wordSet = new HashSet<>(wordDict);
        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true; // empty string base case

        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && wordSet.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[n];
    }
}
```
* **Complexity**: Time: $O(N^2 \cdot L)$ where $L$ is max word length, Space: $O(N)$.

---

# Pattern 6: Two Pointers (Inward Convergence)
### Problem: Trapping Rain Water (LeetCode 42 - Hard)
* **Frequency**: Google, Amazon, Meta.

```java
public class TrappingRainWater {
    public static int trap(int[] height) {
        if (height == null || height.length < 3) return 0;

        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0;
        int totalWater = 0;

        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) {
                    leftMax = height[left];
                } else {
                    totalWater += leftMax - height[left];
                }
                left++;
            } else {
                if (height[right] >= rightMax) {
                    rightMax = height[right];
                } else {
                    totalWater += rightMax - height[right];
                }
                right--;
            }
        }

        return totalWater;
    }
}
```
* **Complexity**: Time: $O(N)$, Space: $O(1)$.
