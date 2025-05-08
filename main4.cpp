#include <iostream>
#include <unordered_map>
#include <vector>
#include <set>
using namespace std;

class Graph {
    unordered_map<int, vector<int>> adjList;

public:
    void addEdge(int u, int v) {
        adjList[u].push_back(v);
        adjList[v].push_back(u);
    }

    bool isSafe(int node, int color, unordered_map<int, int>& color_assignment) {
        for (int neighbor : adjList[node]) {
            if (color_assignment.count(neighbor) && color_assignment[neighbor] == color)
                return false;
        }
        return true;
    }

    bool colorGraph(vector<int>& nodes, int index, int maxColors, unordered_map<int, int>& color_assignment) {
        if (index == nodes.size())  // All nodes colored
            return true;

        int node = nodes[index];

        for (int color = 1; color <= maxColors; color++) {
            if (isSafe(node, color, color_assignment)) {
                color_assignment[node] = color;
                if (colorGraph(nodes, index + 1, maxColors, color_assignment))
                    return true;
                color_assignment.erase(node); // backtrack
            }
        }
        return false;
    }

    void solveGraphColoring(int maxColors) {
        unordered_map<int, int> color_assignment;
        bool solved = false;
        int minColorsUsed = 0;

        // Collect all nodes into a list (since keys can be arbitrary)
        vector<int> nodes;
        for (const auto& pair : adjList)
            nodes.push_back(pair.first);

        for (int colors = 1; colors <= maxColors; colors++) {
            color_assignment.clear();
            if (colorGraph(nodes, 0, colors, color_assignment)) {
                solved = true;
                minColorsUsed = colors;
                break;
            }
        }

        if (solved) {
            cout << "\nSolution found with " << minColorsUsed << " colors:" << endl;
            for (const auto& node : nodes) {
                cout << "Node " << node << " -> Color " << color_assignment[node] << endl;
            }

            set<int> unique_colors;
            for (const auto& entry : color_assignment) {
                unique_colors.insert(entry.second);
            }

            cout << "\n{Colors Used: " << unique_colors.size() << "} Used as follows:" << endl;
            for (int color : unique_colors) {
                cout << "Color " << color << endl;
            }
        } else {
            cout << "\nNo solution possible with " << maxColors << " colors." << endl;
        }
    }

    void printAdjacencyList() {
        cout << "\nAdjacency List:" << endl;
        for (const auto& pair : adjList) {
            cout << "Node " << pair.first << ": ";
            for (int neighbor : pair.second) {
                cout << neighbor << " ";
            }
            cout << endl;
        }
    }
};

int main() {
    int e, maxColors;
    cout << "Enter number of edges: ";
    cin >> e;

    Graph g;

    cout << "Enter edges (u v):" << endl;
    for (int i = 0; i < e; i++) {
        int u, v;
        cin >> u >> v;
        g.addEdge(u, v);
    }

    cout << "Enter number of colors available: ";
    cin >> maxColors;

    g.printAdjacencyList();

    g.solveGraphColoring(maxColors);

    return 0;
}
