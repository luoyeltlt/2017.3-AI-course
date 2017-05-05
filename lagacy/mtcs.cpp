#include <vector>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <cmath>

extern "C"{

using namespace std;
//using ChessType = enum { white, black, noChess };
enum ChessType {white, black, noChess};
#define nullptr 0
const char* myprint()
{
   printf("hello world\n");
   int myints[] = {16,2,77,29};
   vector<int> first;
   vector<int> second (4,100);

    vector<int> fifth (myints, myints + sizeof(myints) / sizeof(int) );
    for ( vector<int>::iterator it = fifth.begin(); it != fifth.end(); ++it)
    printf("%d ",*it);
    printf("\n");

    return "hello";
}

struct Row {
	Row() {
		for (int i(0); i != 8; ++i) {
			row[i] = noChess;
		}
	}
	Row(Row& r) {
		memcpy(row, r.row, 8 * sizeof(int));
	}
	int& operator [](int i) {
		return row[i];
	}
	Row& operator = (Row& r) {
		memcpy(row, r.row, 8 * sizeof(int));
	}
	int row[8];
};
struct State {
	Row& operator [](int i) {
		return board[i];
	}
	Row board[8];
};
struct Position {
	Position(int xx = 0, int yy = 0) : x(xx), y(yy) {}
	int x, y;
};

void initial();
void execute(State& s, Position nextPosition, ChessType type);
int isWin(State& s, ChessType type);
bool canInput(State& s, ChessType type);
vector<Position> getSelection(State& s, ChessType type);
Position getNextPosition2(State& s, ChessType type);
void printState(ChessType type);
bool canExecute(State& s, Position nextPosition, ChessType type);
void putCheck();
bool isFinal(State& s);
bool isEnd(false);

void execute(State& s, Position nextPosition, ChessType type) {
	int x(nextPosition.x), y(nextPosition.y);
	if (x < 0)
		return;
	s[x][y] = type;
	int differentNum(0);
	for (int i(x); i != 8; ++i) {
		if (i == x) {
			continue;
		}
		if (s[i][y] == noChess) {
			break;
		}
		else if (s[i][y] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			for (int k(x + 1); k != i; ++k) {
				s[k][y] = type;
			}
			break;
		}
	}
	differentNum = 0;
	for (int i(x); i >= 0; --i) {
		if (i == x) {
			continue;
		}
		if (s[i][y] == noChess) {
			break;
		}
		else if (s[i][y] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			for (int k(x - 1); k != i; --k) {
				s[k][y] = type;
			}

			break;
		}
	}
	differentNum = 0;
	for (int j(y); j != 8; ++j) {
		if (j == y) {
			continue;
		}
		if (s[x][j] == noChess) {
			break;
		}
		else if (s[x][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			for (int k(y + 1); k != j; ++k) {
				s[x][k] = type;
			}

			break;
		}
	}
	differentNum = 0;
	for (int j(y); j >= 0; --j) {
		if (j == y) {
			continue;
		}
		if (s[x][j] == noChess) {
			break;
		}
		else if (s[x][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			for (int k(y - 1); k != j; --k) {
				s[x][k] = type;
			}

			break;
		}
	}
	differentNum = 0;
	for (int i(x), j(y); i >= 0 && j >= 0; --i, --j) {
		if (j == y) {
			continue;
		}
		if (s[i][j] == noChess) {
			break;
		}
		else if (s[i][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			for (int ii(x - 1), jj(y - 1); ii != i && jj != j; --ii, --jj) {
				s[ii][jj] = type;
			}

			break;
		}
	}
	differentNum = 0;
	for (int i(x), j(y); i != 8 && j >= 0; ++i, --j) {
		if (j == y) {
			continue;
		}
		if (s[i][j] == noChess) {
			break;
		}
		else if (s[i][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			for (int ii(x + 1), jj(y - 1); ii != i && jj != j; ++ii, --jj) {
				s[ii][jj] = type;
			}

			break;
		}
	}
	differentNum = 0;
	for (int i(x), j(y); i >= 0 && j != 8; --i, ++j) {
		if (j == y) {
			continue;
		}
		if (s[i][j] == noChess) {
			break;
		}
		else if (s[i][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			for (int ii(x - 1), jj(y + 1); ii != i && jj != j; --ii, ++jj) {
				s[ii][jj] = type;
			}

			break;
		}
	}
	differentNum = 0;
	for (int i(x), j(y); i != 8 && j != 8; ++i, ++j) {
		if (j == y) {
			continue;
		}
		if (s[i][j] == noChess) {
			break;
		}
		else if (s[i][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			for (int ii(x + 1), jj(y + 1); ii != i && jj != j; ++ii, ++jj) {
				s[ii][jj] = type;
			}

			break;
		}
	}
}

int isWin(State& s, ChessType type) {
	int result[2] = { 0, 0 };
	for (int i(0); i != 8; ++i) {
		for (int j(0); j != 8; ++j) {
			if (s[i][j] == noChess)
				continue;
			++result[s[i][j]];

		}
	}
	if (result[type] > result[!type]) {
		return 2;
	}
	else if (result[type] == result[!type]) {
		return 1;
	}
	return 0;
}

bool canExecute(State& s, Position nextPosition, ChessType type) {
	int x(nextPosition.x), y(nextPosition.y);
	if (x < 0 || x > 7 || y < 0 || y > 7) {
		return false;
	}
	if (s[x][y] != noChess) {
		return false;
	}
	int differentNum(0);
	for (int i(x); i != 8; ++i) {
		if (i == x) {
			continue;
		}
		if (s[i][y] == noChess) {
			break;
		}
		else if (s[i][y] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			return true;
		}
	}
	differentNum = 0;
	for (int i(x); i >= 0; --i) {
		if (i == x) {
			continue;
		}
		if (s[i][y] == noChess) {
			break;
		}
		else if (s[i][y] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			return true;
		}
	}
	differentNum = 0;
	for (int j(y); j != 8; ++j) {
		if (j == y) {
			continue;
		}
		if (s[x][j] == noChess) {
			break;
		}
		else if (s[x][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			return true;
		}
	}
	differentNum = 0;
	for (int j(y); j >= 0; --j) {
		if (j == y) {
			continue;
		}
		if (s[x][j] == noChess) {
			break;
		}
		else if (s[x][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			return true;
		}
	}
	differentNum = 0;
	for (int i(x), j(y); i >= 0 && j >= 0; --i, --j) {
		if (j == y) {
			continue;
		}
		if (s[i][j] == noChess) {
			break;
		}
		else if (s[i][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			return true;
		}
	}
	differentNum = 0;
	for (int i(x), j(y); i != 8 && j >= 0; ++i, --j) {
		if (j == y) {
			continue;
		}
		if (s[i][j] == noChess) {
			break;
		}
		else if (s[i][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			return true;
		}
	}
	differentNum = 0;
	for (int i(x), j(y); i >= 0 && j != 8; --i, ++j) {
		if (j == y) {
			continue;
		}
		if (s[i][j] == noChess) {
			break;
		}
		else if (s[i][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			return true;
		}
	}
	differentNum = 0;
	for (int i(x), j(y); i != 8 && j != 8; ++i, ++j) {
		if (j == y) {
			continue;
		}
		if (s[i][j] == noChess) {
			break;
		}
		else if (s[i][j] != type) {
			++differentNum;
		}
		else if (differentNum == 0) {
			break;
		}
		else {
			return true;
		}
	}
	return false;
}

bool canInput(State& s, ChessType type) {
	Position nextPosition;
	for (int i(0); i != 8; ++i) {
		nextPosition.x = i;
		for (int j(0); j != 8; ++j) {
			nextPosition.y = j;
			if (canExecute(s, nextPosition, type)) {
				return true;
			}
		}
	}
	return false;
}

vector<Position> getSelection(State& s, ChessType type) {
	vector<Position> result;
	Position nextPosition;
	for (int i(0); i != 8; ++i) {
		nextPosition.x = i;
		for (int j(0); j != 8; ++j) {
			nextPosition.y = j;
			if (canExecute(s, nextPosition, type)) {
				result.push_back(nextPosition);
			}
		}
	}
	return result;
}

struct Vertex {
	Vertex(State ss, Position last, ChessType type, Vertex* father) : parent(father),
		q(0), visitedNum(0), lastPosition(last),
		child(nullptr), brother(nullptr), lastType(type),
		isKnown(64, false), s(ss), childNum(0) {
		execute(s, last, type);
		selectionSet = getSelection(s, static_cast<ChessType>(1-lastType));
	}
	vector<Position> selectionSet;
	vector<bool> isKnown;
	State s;
	Position lastPosition;
	ChessType lastType;
	int q;
	int childNum;
	int visitedNum;
	Vertex* parent, *child, *brother;
};

void freeTree(Vertex* root) {
	if (root == nullptr) {
		return;
	}
	freeTree(root->child);
	freeTree(root->brother);
	delete root;
}

void addChild(Vertex* parent, Vertex* child) {
	if (parent->child == nullptr) {
		parent->child = child;
	}
	else {
		Vertex* lastChild = parent->child;
		while (lastChild->brother != nullptr) {
			lastChild = lastChild->brother;
		}
		lastChild->brother = child;
	}
	++(parent->childNum);
}

Vertex* treePolicy(Vertex * v);

int defaultPolicy(State s, ChessType type);

Vertex* bestChild(Vertex* v, int c);

Vertex* expand(Vertex* v);

void backUp(Vertex* v, int deta);

Position getNextPosition2(State& s ,ChessType type) {
	Vertex* v0 = new Vertex(s, Position(-1, -1),static_cast<ChessType>(1-type), nullptr);
	Position result;
	int i(0);
	isEnd = false;
	time_t start = clock(), end;
	while (true) {
		Vertex* vl = treePolicy(v0);
		end = clock();
		if (end - start > 300000 || isEnd) {
			break;
		}
		int deta = defaultPolicy(vl->s, vl->lastType);
		backUp(vl, deta);
		++i;
	}
	result = bestChild(v0, 0)->lastPosition;
	freeTree(v0);
//	std::cout << "Consume time: "<< (clock() - start) / 1000.0 << endl; //TODO cmd line win : time + confidence
	return result;
}
int* getNextPosition3(int* arr,int type){
    ChessType chess_type =static_cast<ChessType>(type);
    State state;
    for (int i =0;i<8;i++){
        for (int j=0;j<8;j++){
            state.board[i][j]=arr[8*i+j];
        }
    }
    Position pos=getNextPosition2(state,chess_type);
//    printf("%d %d ",pos.x,pos.y);
    int* pos_arr=new int[2];
    pos_arr[0]=pos.x;
    pos_arr[1]=pos.y;
    return pos_arr;
}
bool canExpand(Vertex* v) {
	// TODO
	if (v->child == nullptr) {
		return true;
	}
	if (v->selectionSet.size() == 0) {
		return v->childNum == 0 ? true : false;
	}
	if (v->childNum < v->selectionSet.size()) {
		return true;
	}
	return false;
}

bool isFinal(State& s) {
	bool isFull(true);
	for (int i(0); i != 8; ++i) {
		for (int j(0); j != 8; ++j) {
			if (s[i][j] == noChess) {
				isFull = false;
				break;
			}
		}
	}
	if (isFull) {
		return true;
	}
	if (!canInput(s, black) && !canInput(s, white)) {
		return true;
	}
	return false;
}

Vertex* treePolicy(Vertex * v) {
	while (!isFinal(v->s)) {
		if (canExpand(v)) {
			return expand(v);
		}
		v = bestChild(v, 1);
	}
	isEnd = true; // TODO when choice is small, still need to exploit?
	return v;
}

Vertex* expand(Vertex* v) {
	int nodeNum = v->selectionSet.size();
	if (nodeNum == 0) {
		Vertex* newNode = new Vertex(v->s, Position( -1, -1 ), static_cast<ChessType>(1 - v->lastType), v);
		addChild(v, newNode);
		v->isKnown[0] = true;
		return newNode;
	}
	for (int i(0); i != nodeNum; ++i) {
		if (v->isKnown[i])
			continue;
		Vertex* newNode = new Vertex(v->s, v->selectionSet[i], static_cast<ChessType>(1 - v->lastType), v);
		addChild(v, newNode);
		v->isKnown[i] = true;
		return newNode;
	}
}

Vertex* bestChild(Vertex* v, int c) {
	Vertex* child = v->child;
	Vertex* result = child;
	int x, y;
	double value = 0, temp = 0, boundValue = 0;
	while (child != nullptr) {
		x = child->lastPosition.x;
		y = child->lastPosition.y;
		if ((x == 0 && y == 0) || (x == 7 && y == 7) || (x == 0 && y == 7) || (x == 7 && y == 0)) {
			return child;
		}
		temp = child->q*1.0 / child->visitedNum + c*1.0 * sqrt(2 * log(v->visitedNum) / child->visitedNum);
		if (temp > value) {
			result = child;
			value = temp;
		}
		child = child->brother;
	}
	return result;
}

int defaultPolicy(State s, ChessType type) {
	int tempType = 1 - type;
	while (!isFinal(s)) {
		vector<Position> selectionSet = getSelection(s, static_cast<ChessType>(tempType));
		if (selectionSet.size() == 0) {
			tempType = 1 - tempType;
			continue;
		}
		int i = rand() % selectionSet.size();
		execute(s, selectionSet[i], static_cast<ChessType>(tempType));
		tempType = 1 - tempType;
	}
	return isWin(s, type);
	// win 2 lose 1 TODO calculate chess number and normaliza to 0-1 0.5 means balance?
	// TODO should judge for 1-type whether win?
}

void backUp(Vertex* v, int deta) {
	while (v != nullptr) {
		++(v->visitedNum);
		v->q += deta;
		deta = -deta;//TODO 1-deta
		v = v->parent;
	}
}
}
