#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// ------------------------- JOB SCHEDULING -------------------------

struct Job {
    int id;
    int deadline;
    int profit;
};

bool compareJobs(Job a, Job b) {
    return a.profit > b.profit;
}

void jobScheduling(vector<Job>& jobs) {
    int n = jobs.size();
    sort(jobs.begin(), jobs.end(), compareJobs);

    int maxDeadline = 0;
    for (int i = 0; i < n; i++) {
        if (jobs[i].deadline > maxDeadline)
            maxDeadline = jobs[i].deadline;
    }

    vector<int> slot(maxDeadline + 1, -1);
    int totalProfit = 0;
    int countJobs = 0;

    for (int i = 0; i < n; i++) {
        for (int j = min(jobs[i].deadline, maxDeadline); j >= 1; j--) {
            if (slot[j] == -1) {
                slot[j] = jobs[i].id;
                totalProfit += jobs[i].profit;
                countJobs++;
                break;
            }
        }
    }

    cout << "\n--- Job Scheduling Result ---\n";
    cout << "Number of jobs scheduled: " << countJobs << endl;
    cout << "Total profit: " << totalProfit << endl;
    cout << "Job sequence: ";
    for (int i = 1; i <= maxDeadline; i++) {
        if (slot[i] != -1)
            if (i == maxDeadline){
                cout << "Job " << slot[i] << "";
                continue;
            }
            cout << "Job " << slot[i] << " -> ";
    }
    cout << endl;
}

// ------------------------- KRUSKAL'S MST -------------------------

struct Edge {
    int src, dest, weight;
};

bool compareEdges(const Edge& e1, const Edge& e2) {
    return e1.weight < e2.weight;
}

int findParent(vector<int>& parent, int u) {
    if (parent[u] != u)
        parent[u] = findParent(parent, parent[u]);
    return parent[u];
}

void unionSets(vector<int>& parent, vector<int>& rank, int x, int y) {
    int xroot = findParent(parent, x);
    int yroot = findParent(parent, y);

    if (rank[xroot] < rank[yroot])
        parent[xroot] = yroot;
    else if (rank[xroot] > rank[yroot])
        parent[yroot] = xroot;
    else {
        parent[yroot] = xroot;
        rank[xroot]++;
    }
}

vector<Edge> KruskalsMST(vector<Edge>& edges, int V, int& totalCost) {
    vector<Edge> result;
    vector<int> parent(V);
    vector<int> rank(V, 0);

    sort(edges.begin(), edges.end(), compareEdges);
    for (int i = 0; i < V; i++)
        parent[i] = i;

    int i = 0;
    while (result.size() < V - 1 && i < edges.size()) {
        Edge next_edge = edges[i];
        i++;
        int x = findParent(parent, next_edge.src);
        int y = findParent(parent, next_edge.dest);

        if (x != y) {
            result.push_back(next_edge);
            totalCost += next_edge.weight;
            unionSets(parent, rank, x, y);
        }
    }

    return result;
}

// ------------------------- MAIN -------------------------

int main() {
    // ----------------- Input for Job Scheduling -----------------
    int n;
    cout << "Enter number of jobs: ";
    cin >> n;
    vector<Job> jobs(n);
    cout << "Enter job details (id deadline profit) for each job:\n";
    for (int i = 0; i < n; i++) {
        cout << "Job " << (i + 1) << ": ";
        cin >> jobs[i].id >> jobs[i].deadline >> jobs[i].profit;
    }

    jobScheduling(jobs);

    // ----------------- Input for Kruskal's MST -----------------
    int V, E;
    cout << "\nEnter number of vertices: ";
    cin >> V;
    cout << "Enter number of edges: ";
    cin >> E;
    vector<Edge> edges(E);
    cout << "Enter edge details (src dest weight) for each edge:\n";
    for (int i = 0; i < E; i++) {
        cout << "Edge " << (i + 1) << ": ";
        cin >> edges[i].src >> edges[i].dest >> edges[i].weight;
    }

    int totalMSTCost = 0;
    vector<Edge> mst = KruskalsMST(edges, V, totalMSTCost);

    cout << "\n--- Kruskal's MST Result ---\n";
    for (Edge edge : mst) {
        cout << edge.src << " -- " << edge.dest << " == " << edge.weight << endl;
    }
    cout << "Total cost of MST: " << totalMSTCost << endl;

    return 0;
}
