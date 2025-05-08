#include <iostream>
#include <unordered_map>
#include <vector>
#include <stack>
#include <queue>
#include <set>
#include <algorithm>
using namespace std;

class Graph {
    unordered_map<int, vector<int>> adj;

public:
    vector<int> dfsRecOrder;
    vector<int> dfsItrOrder;
    vector<int> bfsItrOrder;
    vector<int> bfsRecOrder;

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);  // undirected
    }

    void dfsRecursiveHelper(int node, set<int>& visited, unordered_map<int, int>& level) {
        visited.insert(node);
        dfsRecOrder.push_back(node);
        cout << "Node: " << node << ", Level: " << level[node] << endl;

        for (int neighbor : adj[node]) {
            if (!visited.count(neighbor)) {
                level[neighbor] = level[node] + 1;
                dfsRecursiveHelper(neighbor, visited, level);
            }
        }
    }

    void dfsRecursive(int start) {
        dfsRecOrder.clear();
        set<int> visited;
        unordered_map<int, int> level;
        level[start] = 0;

        cout << "DFS Recursive with Levels:\n";
        dfsRecursiveHelper(start, visited, level);
        cout << endl;
    }

    void dfsIterative(int start) {
        dfsItrOrder.clear();
        set<int> visited;
        stack<int> stk;
        unordered_map<int, int> level;

        stk.push(start);
        level[start] = 0;

        cout << "DFS Iterative with Levels:\n";
        while (!stk.empty()) {
            int node = stk.top();
            stk.pop();

            if (!visited.count(node)) {
                visited.insert(node);
                dfsItrOrder.push_back(node);
                cout << "Node: " << node << ", Level: " << level[node] << endl;

                for (int neighbor : adj[node]) {
                    if (!visited.count(neighbor)) {
                        stk.push(neighbor);
                        level[neighbor] = level[node] + 1;
                    }
                }
            }
        }
        cout << endl;
    }

    void bfsIterative(int start) {
        bfsItrOrder.clear();
        set<int> visited;
        queue<int> q;
        unordered_map<int, int> level;

        q.push(start);
        visited.insert(start);
        level[start] = 0;

        cout << "BFS Iterative with Levels:\n";
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            bfsItrOrder.push_back(node);
            cout << "Node: " << node << ", Level: " << level[node] << endl;

            for (int neighbor : adj[node]) {
                if (!visited.count(neighbor)) {
                    visited.insert(neighbor);
                    q.push(neighbor);
                    level[neighbor] = level[node] + 1;
                }
            }
        }
        cout << endl;
    }

    void bfsRecursiveHelper(queue<int>& q, set<int>& visited, unordered_map<int, int>& level) {
        if (q.empty()) return;

        int node = q.front();
        q.pop();
        bfsRecOrder.push_back(node);
        cout << "Node: " << node << ", Level: " << level[node] << endl;

        for (int neighbor : adj[node]) {
            if (!visited.count(neighbor)) {
                visited.insert(neighbor);
                q.push(neighbor);
                level[neighbor] = level[node] + 1;
            }
        }

        bfsRecursiveHelper(q, visited, level);
    }

    void bfsRecursive(int start) {
        bfsRecOrder.clear();
        set<int> visited;
        queue<int> q;
        unordered_map<int, int> level;

        q.push(start);
        visited.insert(start);
        level[start] = 0;

        cout << "BFS Recursive with Levels:\n";
        bfsRecursiveHelper(q, visited, level);
        cout << endl;
    }

    // Simple Search Functions for Traversal Vectors
    void search_dfsRecursive(int target) {
        printPathUntilFound(dfsRecOrder, target, "DFS Recursive");
    }

    void search_dfsIterative(int target) {
        printPathUntilFound(dfsItrOrder, target, "DFS Iterative");
    }

    void search_bfsIterative(int target) {
        printPathUntilFound(bfsItrOrder, target, "BFS Iterative");
    }

    void search_bfsRecursive(int target) {
        printPathUntilFound(bfsRecOrder, target, "BFS Recursive");
    }

    void printPathUntilFound(const vector<int>& order, int target, const string& label) {
        cout << label << " Search to find " << target << ":\n";
        vector<int> path;
        for (int node : order) {
            path.push_back(node);
            if (node == target) {
                cout << "Found" << endl;
                break;
            }
        }
        cout << "Path: ";
        for (int node : path) cout << node << " ";
        cout << endl << endl;
    }
};

int main() {
    Graph g;
    int vertices, edges;

    cout << "Enter number of vertices: ";
    cin >> vertices;

    cout << "Enter number of edges: ";
    cin >> edges;

    cout << "Enter " << edges << " edges (u v):\n";
    for (int i = 0; i < edges; ++i) {
        int u, v;
        cin >> u >> v;
        g.addEdge(u, v);
    }

    int start;
    cout << "Enter the start node: ";
    cin >> start;

    g.dfsRecursive(start);
    g.dfsIterative(start);
    g.bfsIterative(start);
    g.bfsRecursive(start);

    int target;
    cout << "Enter node to search in each traversal: ";
    cin >> target;

    g.search_dfsRecursive(target);
    g.search_dfsIterative(target);
    g.search_bfsIterative(target);
    g.search_bfsRecursive(target);

    return 0;
}