import os, random, time, datetime
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from operator import itemgetter

class MoveSet:
    def __init__(self):
        self.states = []
        self.moves = []

class Data:
    def __init__(self, location):
        self.address = location

        if os.path.isfile(location):
            start = datetime.datetime.now()
            self.df = pd.read_excel(location)
            self.df_ex = self.expand(self.df)
            X = self.df_ex[['0,0', '0,1', '0,2', '1,0', '1,1', '1,2', '2,0', '2,1', '2,2']]
            y = self.df_ex['Move']
            self.clf = DecisionTreeClassifier().fit(X, y)
            end = datetime.datetime.now()
            print("Time to train:", str(end-start))
    
    def expand(self, input):
        moves_list = {"{0, 0}" : "7", "{0, 1}" : "8", "{0, 2}" : "9", "{1, 0}" : "4", "{1, 1}" : "5", "{1, 2}" : "6", "{2, 0}" : "1", "{2, 1}" : "2", "{2, 2}" : "3"}
        result = []
        temp_dict = {}

        for index, row in input.iterrows():
            num = row['count']
            for iteration in range(num):
                temp_dict['0,0'] = row['0,0']
                temp_dict['0,1'] = row['0,1']
                temp_dict['0,2'] = row['0,2']
                temp_dict['1,0'] = row['1,0']
                temp_dict['1,1'] = row['1,1']
                temp_dict['1,2'] = row['1,2']
                temp_dict['2,0'] = row['2,0']
                temp_dict['2,1'] = row['2,1']
                temp_dict['2,2'] = row['2,2']
                temp_dict['Move'] = moves_list[row['Move']]
                result.append(temp_dict)
                temp_dict = {}

        return pd.DataFrame(result)
    
    def refresh_df(self, new_df):
        self.df = new_df

class GameBoard:
    def __init__(self):
        self.turn = 0
        self.game_state = 0
        self.board = [["_" for i in range(3)] for j in range(3)]
        self.p1 = MoveSet()
        self.p2 = MoveSet()
    
    def __str__(self):
        result = ''
        for array in self.board:
            result += str(array[0]) + " " + str(array[1]) + " " + str(array[2]) + '\n'
        return result

    def move(self, x, y):
        self.board[y][x] = 'x' if self.turn == 0 else 'o'
        self.turn = 1 if self.turn == 0 else 0
        if self.turn == 0:
            self.p1.moves.append("{" + "{0}, {1}".format(y, x) + "}")
        else:
            self.p2.moves.append("{" + "{0}, {1}".format(y, x) + "}")

    def Xwin(self):
        print("x wins")
        self.game_state = 1
        return self.p1, 0

    def Owin(self):
        print("o wins")
        self.game_state = 1
        return self.p2, 1 

    def testWin(self):
        #test x winning
        for array in self.board:
            if array[0] == "x" and array[1] == "x" and array[2] == "x":
                return self.Xwin()

        for num in range(3):
            if self.board[0][num] == "x" and self.board[1][num] == "x" and self.board[2][num] == "x":
                return self.Xwin()

        if (self.board[0][0] == 'x' and self.board[1][1] == 'x' and self.board[2][2] == 'x') or (self.board[0][2] == 'x' and self.board[1][1] == 'x' and self.board[2][0] == 'x'):
            return self.Xwin()

        #test o winning
        for array in self.board:
            if array[0] == "o" and array[1] == "o" and array[2] == "o":
                return self.Owin()

        for num in range(3):
            if self.board[0][num] == "o" and self.board[1][num] == "o" and self.board[2][num] == "o":
                return self.Owin()

        if (self.board[0][0] == 'o' and self.board[1][1] == 'o' and self.board[2][2] == 'o') or (self.board[0][2] == 'o' and self.board[1][1] == 'o' and self.board[2][0] == 'o'):
            return self.Owin()
        
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == "_":
                    return None, None
        return self.p1, 2
    
    def convertBoard(self, num):
        out = [[0 for i in range(3)] for j in range(3)]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                    if self.board[i][j] == "_":
                        out[i][j] = 0
                    elif self.board[i][j] == "x" and num == 1:
                        out[i][j] = 1
                    elif self.board[i][j] == "x" and num == 2:
                        out[i][j] = -1
                    elif self.board[i][j] == "o" and num == 1:
                        out[i][j] = -1
                    else:
                        out[i][j] = 1
        return out

class Player:
    def __init__(self, num_game, data):
        self.games = num_game
        self.win_lose_draw = [0, 0, 0]
        self.data = data
    
    def play(self):
        self.startTime = datetime.datetime.now()
        for num in range(1, self.games+1):
            if os.path.isfile(self.data.address):
                self.data.refresh_df(pd.read_excel(self.data.address))
            else:
                temp = MoveSet()
                temp.moves.append('{2, 2}')
                temp.states.append([[1, 1, 1], [1, 1, 1], [1, 1, 0]])
                self.data.refresh_df(self.buildDataFrame(temp, None))

            game = GameBoard()

            while game.game_state == 0:
                print(game)
                moves, winner = game.testWin()
                if moves is not None:
                    #self.buildDataFrame(moves, self.data.df)
                    self.win_lose_draw[winner] += 1
                    break
                
                if game.turn == 0:
                    game.p1.states.append(game.convertBoard(1))
                    x, y = self.analyzePossibleMoves(game, 1)
                    game.move(x, y)
                    continue
                
                if game.turn == 1:
                    game.p2.states.append(game.convertBoard(2))
                    while True:
                        char = str(random.randint(1,10))
                        #char = input("make a move: ")
                        x, y = self.getXY(char)
                        if game.board[y][x] == '_':
                            game.move(x, y)
                            break
                    continue
            print(str(num) + '    ' + str(self.win_lose_draw[0]) + ' : ' + str(self.win_lose_draw[1]))
        self.endTime = datetime.datetime.now()
        self.printStat()

    def printStat(self):
        print("Number of games:", str(self.games))
        print("Wins:", str(self.win_lose_draw[0]))
        print("Lose:", str(self.win_lose_draw[1]))
        print("Draw:", str(self.win_lose_draw[2]))
        print("Start time:", str(self.startTime))
        print("End time:", str(self.endTime))
        print("Time elapsed:", str(self.endTime-self.startTime))
                    
    def buildDataFrame(self, move_set, df):
        result = []
        count = 0
        for game in move_set.states:
            temp_dict = {}
            for i in range(len(game)):
                for j in range(len(game[i])):
                    temp_dict["{0},{1}".format(i, j)] = game[i][j]
            temp_dict["Move"] = move_set.moves[count]
            temp_dict["count"] = 1
            count += 1
            result.append(temp_dict)
        df_temp = pd.DataFrame(result)

        if df is None:
            df_temp.to_excel(self.data.address, index=False, header=True)
        else:
            for index, row in df_temp.iterrows():
                row_search = df.loc[(df['0,0'] == row['0,0']) & (df['0,1'] == row['0,1']) & (df['0,2'] == row['0,2']) & (df['1,0'] == row['1,0']) & (df['1,1'] == row['1,1']) & (df['1,2'] == row['1,2']) & (df['2,0'] == row['2,0']) & (df['2,1'] == row['2,1']) & (df['2,2'] == row['2,2']) & (df['Move'] == row['Move'])]
                if not row_search.empty:
                    df.loc[(df['0,0'] == row['0,0']) & (df['0,1'] == row['0,1']) & (df['0,2'] == row['0,2']) & (df['1,0'] == row['1,0']) & (df['1,1'] == row['1,1']) & (df['1,2'] == row['1,2']) & (df['2,0'] == row['2,0']) & (df['2,1'] == row['2,1']) & (df['2,2'] == row['2,2']) & (df['Move'] == row['Move']), 'count'] += 1 
                    df_temp = df_temp.loc[(df_temp['0,0'] != row['0,0']) | (df_temp['0,1'] != row['0,1']) | (df_temp['0,2'] != row['0,2']) | (df_temp['1,0'] != row['1,0']) | (df_temp['1,1'] != row['1,1']) | (df_temp['1,2'] != row['1,2']) | (df_temp['2,0'] != row['2,0']) | (df_temp['2,1'] != row['2,1']) | (df_temp['2,2'] != row['2,2']) | (df_temp['Move'] != row['Move'])].dropna()

            df = pd.concat([df, df_temp], ignore_index=True, sort=False)
            df.to_excel(self.data.address, index=False, header=True)
        return df
    
    def getXY(self, char):
        if char == "7": return 0, 0
        if char == "8": return 1, 0
        if char == "9": return 2, 0
        if char == "4": return 0, 1
        if char == "5": return 1, 1
        if char == "6": return 2, 1
        if char == "1": return 0, 2
        if char == "2": return 1, 2
        else: return 2, 2

    def analyzePossibleMoves(self, game, num):
        converted = game.convertBoard(num)
        state = []
        result = []
        state.append(converted[0][0]) 
        state.append(converted[0][1]) 
        state.append(converted[0][2]) 
        state.append(converted[1][0]) 
        state.append(converted[1][1]) 
        state.append(converted[1][2]) 
        state.append(converted[2][0]) 
        state.append(converted[2][1]) 
        state.append(converted[2][2])  
        result.append(state)

        probs = self.data.clf.predict_proba(result)[0]
        item = { 'spot': '-1', 'prob': -1 }
        arr = []
        for num in range(len(probs)):
            item['prob'] = probs[num]
            item['spot'] = str(num + 1)
            arr.append(item.copy())

        new_arr = sorted(arr, key=itemgetter('prob'), reverse=True)
        for place in new_arr:
            x, y = self.getXY(place['spot'])

            if game.board[y][x] == '_':
                return x, y
        return x, y

data_loc = '/Users/max/Dropbox/Projects/tic-tac-toe/excel_export.xlsx'

dataset = Data(data_loc)

initial_test = Player(1000, dataset)
initial_test.play()




