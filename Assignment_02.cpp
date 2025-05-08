#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <cmath>
#include <algorithm>
#include <string>

using namespace std;

vector<pair<int, int>> directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

struct PuzzleState {
    vector<int> puzzle;   
    int blank_pos;        
    int g, h, f;            
    PuzzleState* parent; 
    
    PuzzleState(vector<int> p, int blank, int g_val, int h_val, PuzzleState* parent_state = nullptr)
        : puzzle(p), blank_pos(blank), g(g_val), h(h_val), f(g_val + h_val), parent(parent_state) {}
    
    bool operator>(const PuzzleState& other) const {
        return f > other.f;
    }
};
int calculateHeuristic(const vector<int>& puzzle, const vector<int>& goal) {
    int misplaced = 0;
    for (int i = 0; i < puzzle.size(); ++i) {
        if (puzzle[i] != goal[i] && puzzle[i] != 0) {
            misplaced++;
        }
    }
    return misplaced;
}


vector<PuzzleState*> getNeighbors(PuzzleState* state, const vector<int>& goal) {
    vector<PuzzleState*> neighbors;
    int blank_row = state->blank_pos / 3;
    int blank_col = state->blank_pos % 3;
    
    for (auto dir : directions) {
        int new_row = blank_row + dir.first;
        int new_col = blank_col + dir.second;
        
        if (new_row >= 0 && new_row < 3 && new_col >= 0 && new_col < 3) {
            int new_blank_pos = new_row * 3 + new_col;
            vector<int> new_puzzle = state->puzzle;
            swap(new_puzzle[state->blank_pos], new_puzzle[new_blank_pos]);
            int new_h = calculateHeuristic(new_puzzle, goal);
            neighbors.push_back(new PuzzleState(new_puzzle, new_blank_pos, state->g + 1, new_h, state));
        }
    }
    return neighbors;
}

void printPuzzle(const vector<int>& puzzle) {
    for (int i = 0; i < 9; ++i) {
        cout << (puzzle[i] == 0 ? "_" : to_string(puzzle[i])) << " ";
        if (i % 3 == 2) cout << endl;
    }
    cout << endl;   
}

vector<vector<int>> solvePuzzle(vector<int>& initial, vector<int>& goal) {
    priority_queue<PuzzleState*, vector<PuzzleState*>, greater<PuzzleState*>> openList;
    unordered_map<string, bool> closedList;
    
    int blank_pos = find(initial.begin(), initial.end(), 0) - initial.begin();
    
    PuzzleState* startState = new PuzzleState(initial, blank_pos, 0, calculateHeuristic(initial, goal));
    openList.push(startState);
    closedList[string(initial.begin(), initial.end())] = true;

    int stepCount = 0; // To keep track of the step number
    int MAX_STEPS = 20000;

    while (!openList.empty()) {
        PuzzleState* current = openList.top();
        openList.pop();

        stepCount++;
        

        cout << "Step " << stepCount << " (State Expanded):\n";
        printPuzzle(current->puzzle);
        cout << "g = " << current->g << ", h = " << current->h << ", f = " << current->f << endl;
        
        if (current->puzzle == goal) {
            cout<<"FOUND THE SOLUTION!"<<endl;
            vector<vector<int>> solution;
            while (current) {
                solution.push_back(current->puzzle);
                current = current->parent;
            }
            reverse(solution.begin(), solution.end());
            return solution;
        }
        
        vector<PuzzleState*> neighbors = getNeighbors(current, goal);
        
        for (auto neighbor : neighbors) {
            string neighborStr(neighbor->puzzle.begin(), neighbor->puzzle.end());
            if (closedList.find(neighborStr) == closedList.end()) {
                openList.push(neighbor);
                closedList[neighborStr] = true;
                cout << "  -> New state added to the queue:\n";
                printPuzzle(neighbor->puzzle);
                cout << "  g = " << neighbor->g << ", h = " << neighbor->h << ", f = " << neighbor->f << endl;
            }

        }
        
        if (stepCount == MAX_STEPS){
            break;
        }

    }
    return {};  // If no solution is found
}

int main() {
    vector<int> initial(9), goal(9);
    
    cout << "Enter the initial configuration of the 8-tile puzzle (0 for the empty space):\n";
    for (int i = 0; i < 9; ++i) {
        cin >> initial[i];
    }
    
    cout << "Enter the goal configuration of the 8-tile puzzle (0 for the empty space):\n";
    for (int i = 0; i < 9; ++i) {
        cin >> goal[i];
    }

    vector<vector<int>> solution = solvePuzzle(initial, goal);
    
    if (!solution.empty()) {
        cout << "Moves are as follows:\n";
        for (auto& step : solution) {
            printPuzzle(step);
        }
    } else {
        cout << "No solution found.\n";
    }
    
    return 0;
}
