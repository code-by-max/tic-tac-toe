import os, random, time, datetime
#import msvcrt 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

good_data = '/Users/max/Dropbox/Projects/tictactoe/excel_export.xlsx'
bad_data = '/Users/max/Dropbox/Projects/tictactoe/bad_export.xlsx'

class moveSet:
    def __init__(self):
        self.states = []
        self.moves = []

def printState(game):
    for array in game:
        print( array[0] + " " + array[1] + " " + array[2])
    print()

def testWin(game):
    #test x
    for array in game:
        if array[0] == "x" and array[1] == "x" and array[2] == "x":
            return 1
    
    for num in range(3):
        if game[0][num] == "x" and game[1][num] == "x" and game[2][num] == "x":
            return 1
    
    if (game[0][0] == "x" and game[1][1] == "x" and game[2][2] == "x") or (game[0][2] == "x" and game[1][1] == "x" and game[2][0] == "x"):
        return 1
    
    #test o
    for array in game:
        if array[0] == "o" and array[1] == "o" and array[2] == "o":
            return 2
    
    for num in range(3):
        if game[0][num] == "o" and game[1][num] == "o" and game[2][num] == "o":
            return 2
    
    if (game[0][0] == "o" and game[1][1] == "o" and game[2][2] == "o") or (game[0][2] == "o" and game[1][1] == "o" and game[2][0] == "o"):
        return 2
    return -1

def testDraw(game):
    for i in range(len(game)):
        for j in range(len(game[i])):
                if game[i][j] == "_":
                    return 0
    return 1

def getY(char):
    if char == "7": return 0
    if char == "8": return 0
    if char == "9": return 0
    if char == "4": return 1
    if char == "5": return 1
    if char == "6": return 1
    if char == "1": return 2
    if char == "2": return 2
    if char == "3": return 2
    return 0

def getX(char):
    if char == "7": return 0
    if char == "8": return 1
    if char == "9": return 2
    if char == "4": return 0
    if char == "5": return 1
    if char == "6": return 2
    if char == "1": return 0
    if char == "2": return 1
    if char == "3": return 2
    return 0

def convertBoard(game, num):
    out = [[0 for i in range(3)] for j in range(3)]
    for i in range(len(game)):
        for j in range(len(game[i])):
                if game[i][j] == "_":
                    out[i][j] = 0
                elif (game[i][j] == "x" and num == 1):
                    out[i][j] = 1
                elif (game[i][j] == "x" and num == 2):
                    out[i][j] = -1
                elif (game[i][j] == "o" and num == 1):
                    out[i][j] = -1
                else:
                    out[i][j] = 1
    return out

def buildDataFrame(move_set, df): #input is a moveSet object
    result = []
    count = 0
    for game in move_set.states:
        temp_dict = {}
        for i in range(len(game)):
            for j in range(len(game[i])):
                temp_dict["{0},{1}".format(i, j)] = game[i][j]
        temp_dict["Move"] = move_set.moves[count]
        temp_dict["count"] = 1
        count = count + 1
        result.append(temp_dict)
    df_temp = pd.DataFrame(result)
    print(df_temp)
    if df is None:
        df_temp.to_excel(good_data, index = False, header=True)
    else:
        for index, row in df_temp.iterrows():
            row_search = df.loc[(df['0,0'] == row['0,0']) & (df['0,1'] == row['0,1']) & (df['0,2'] == row['0,2']) & (df['1,0'] == row['1,0']) & (df['1,1'] == row['1,1']) & (df['1,2'] == row['1,2']) & (df['2,0'] == row['2,0']) & (df['2,1'] == row['2,1']) & (df['2,2'] == row['2,2']) & (df['Move'] == row['Move'])]
            if not row_search.empty:
                df.loc[(df['0,0'] == row['0,0']) & (df['0,1'] == row['0,1']) & (df['0,2'] == row['0,2']) & (df['1,0'] == row['1,0']) & (df['1,1'] == row['1,1']) & (df['1,2'] == row['1,2']) & (df['2,0'] == row['2,0']) & (df['2,1'] == row['2,1']) & (df['2,2'] == row['2,2']) & (df['Move'] == row['Move']), 'count'] += 1 
                df_temp = df_temp.loc[(df_temp['0,0'] != row['0,0']) | (df_temp['0,1'] != row['0,1']) | (df_temp['0,2'] != row['0,2']) | (df_temp['1,0'] != row['1,0']) | (df_temp['1,1'] != row['1,1']) | (df_temp['1,2'] != row['1,2']) | (df_temp['2,0'] != row['2,0']) | (df_temp['2,1'] != row['2,1']) | (df_temp['2,2'] != row['2,2']) | (df_temp['Move'] != row['Move'])].dropna()

        df = pd.concat([df, df_temp], ignore_index=True, sort=False)
        #result = removeDups(result)
        df.to_excel(good_data, index = False, header=True)
    return df_temp

def buildBadData(move_set, df_bad):
    result = []
    count = 0
    for game in move_set.states:
        temp_dict = {}
        for i in range(len(game)):
            for j in range(len(game[i])):
                temp_dict["{0},{1}".format(i, j)] = game[i][j]
        temp_dict["Move"] = move_set.moves[count]
        temp_dict["count"] = 1
        count = count + 1
        result.append(temp_dict)
    df_temp = pd.DataFrame(result)
    print(df_temp)
    if df_bad is None:
        df_temp.to_excel(bad_data, index = False, header=True)
    else:
        for index, row in df_temp.iterrows():
            row_search = df_bad.loc[(df_bad['0,0'] == row['0,0']) & (df_bad['0,1'] == row['0,1']) & (df_bad['0,2'] == row['0,2']) & (df_bad['1,0'] == row['1,0']) & (df_bad['1,1'] == row['1,1']) & (df_bad['1,2'] == row['1,2']) & (df_bad['2,0'] == row['2,0']) & (df_bad['2,1'] == row['2,1']) & (df_bad['2,2'] == row['2,2']) & (df_bad['Move'] == row['Move'])]
            if not row_search.empty:
                df_bad.loc[(df_bad['0,0'] == row['0,0']) & (df_bad['0,1'] == row['0,1']) & (df_bad['0,2'] == row['0,2']) & (df_bad['1,0'] == row['1,0']) & (df_bad['1,1'] == row['1,1']) & (df_bad['1,2'] == row['1,2']) & (df_bad['2,0'] == row['2,0']) & (df_bad['2,1'] == row['2,1']) & (df_bad['2,2'] == row['2,2']) & (df_bad['Move'] == row['Move']), 'count'] += 1 
                df_temp = df_temp.loc[(df_temp['0,0'] != row['0,0']) | (df_temp['0,1'] != row['0,1']) | (df_temp['0,2'] != row['0,2']) | (df_temp['1,0'] != row['1,0']) | (df_temp['1,1'] != row['1,1']) | (df_temp['1,2'] != row['1,2']) | (df_temp['2,0'] != row['2,0']) | (df_temp['2,1'] != row['2,1']) | (df_temp['2,2'] != row['2,2']) | (df_temp['Move'] != row['Move'])].dropna()

        df_bad = pd.concat([df_bad, df_temp], ignore_index=True, sort=False)
        #result = removeDups(result)
        df_bad.to_excel(bad_data, index = False, header=True)
    return df_temp

def deleteBadRows(move_set):
    count = 0
    length = len(move_set.states)

    for convert in move_set.states:
        if( count >= length - 2):
            df_temp = df.loc[(df['0,0'] != convert[0][0]) | (df['0,1'] != convert[0][1]) | (df['0,2'] != convert[0][2]) | (df['1,0'] != convert[1][0]) | (df['1,1'] != convert[1][1]) | (df['1,2'] != convert[1][2]) | (df['2,0'] != convert[2][0]) | (df['2,1'] != convert[2][1]) | (df['2,2'] != convert[2][2]) | (df['Move'] != move_set.moves[count])]
            df_temp.dropna().to_excel(good_data, index = False, header=True)
        count += 1

def analyzePossibleMoves(game, num, classifier):
    movesList = {"{0, 0}" : "7", "{0, 1}" : "8", "{0, 2}" : "9", "{1, 0}" : "4", "{1, 1}" : "5", "{1, 2}" : "6", "{2, 0}" : "1", "{2, 1}" : "2", "{2, 2}" : "3"}
    converted = convertBoard(game, num)
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
    #print(classifier.predict(result))

    return classifier.predict(result)
    #results = []

    #greatest = -99999999
    #for i in range(len(game)):
        #for j in range(len(game[i])):
            #if game[i][j] == "_":
                #converted = convertBoard(game, num)
                #cur_move ="{" + "{0}, {1}".format(i, j) + "}"
                #numRows = getNumRows(converted, cur_move) - getBadRows(converted, cur_move)
                #if numRows == greatest:
                #    results.append([cur_move, numRows])
                #if numRows > greatest:
                #    results = []
                #    results.append([cur_move, numRows])
                #    greatest = numRows
                    
    #print(results)
    #spot = random.randint(0, len(results)-1)
    #return movesList[results[spot][0]]

def getNumRows(convert, move):
    df2 = df.loc[(df['0,0'] == convert[0][0]) & (df['0,1'] == convert[0][1]) & (df['0,2'] == convert[0][2]) & (df['1,0'] == convert[1][0]) & (df['1,1'] == convert[1][1]) & (df['1,2'] == convert[1][2]) & (df['2,0'] == convert[2][0]) & (df['2,1'] == convert[2][1]) & (df['2,2'] == convert[2][2]) & (df['Move'] == move)]
    if df2.empty:
        return 0
    else:
        return df2.iloc[0]['count']

def getBadRows(convert, move):
    mask = (df_bad['0,0'] == convert[0][0]) & (df_bad['0,1'] == convert[0][1]) & (df_bad['0,2'] == convert[0][2]) & (df_bad['1,0'] == convert[1][0]) & (df_bad['1,1'] == convert[1][1]) & (df_bad['1,2'] == convert[1][2]) & (df_bad['2,0'] == convert[2][0]) & (df_bad['2,1'] == convert[2][1]) & (df_bad['2,2'] == convert[2][2]) & (df_bad['Move'] == move)
    df_b = df_bad.loc[mask]

    if df_b.empty:
        return 0
    else:
        return df_b.iloc[0]['count']

def removeDups(data):
    cols = ['0,0', '0,1', '0,2', '1,0', '1,1', '1,2', '2,0', '2,1', '2,2', 'Move']
    if 'count' not in data.columns:
        data['count'] = data.groupby(cols)['0,0'].transform('size')
    return data.drop_duplicates()

def expand(data):
    moves_list = {"{0, 0}" : "7", "{0, 1}" : "8", "{0, 2}" : "9", "{1, 0}" : "4", "{1, 1}" : "5", "{1, 2}" : "6", "{2, 0}" : "1", "{2, 1}" : "2", "{2, 2}" : "3"}
    result = []
    temp_dict = {}
    #print(data)
    for index, row in data.iterrows():
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
    #print(result)
    #print(pd.DataFrame(result))
    return pd.DataFrame(result)

#begin games adjust games to change the number of games played
startTime = datetime.datetime.now()
games = 100
total_moves = 0
win_lose_draw = [0, 0, 0]

if os.path.isfile(good_data):
    df = pd.read_excel(good_data)
expanded = expand(df)
#for index, row in expanded.iterrows():
    #print(row['Move'])
X = expanded[['0,0', '0,1', '0,2', '1,0', '1,1', '1,2', '2,0', '2,1', '2,2']]
y = expanded['Move']

clf = DecisionTreeClassifier().fit(X, y)

for num in range(1,games + 1):
    if os.path.isfile(good_data):
        df = pd.read_excel(good_data)
    else:
        temp = moveSet()
        temp.moves.append("{2, 2}")
        temp.states.append([[1, 1, 1], [1, 1, 1], [1, 1, 0]])
        buildDataFrame(temp, None)
        df = pd.read_excel(good_data)

    if os.path.isfile(bad_data):
        df_bad = pd.read_excel(bad_data)
    else:
        temp = moveSet()
        temp.moves.append("{2, 2}")
        temp.states.append([[1, 1, 1], [1, 1, 1], [1, 1, 0]])
        buildBadData(temp, None)
        df_bad = pd.read_excel(bad_data)
    y = 0
    x = 0
    turn = 0
    game_state = 0
    gameBoard = [["_" for i in range(3)] for j in range(3)]

    p1 = moveSet()
    p2 = moveSet()
    while game_state == 0:
        printState(gameBoard)
        #time.sleep(1)
        win = testWin(gameBoard)
        if win == 1:
            print("x wins")
            game_state = 1
            total_moves += len(p1.moves)
            print(("Moves: " + str(len(p1.moves))))
            #buildDataFrame(p1, df)
            #deleteBadRows(p2)
            win_lose_draw[0] += 1
            break
        if win == 2:
            print("o wins")
            game_state = 1
            total_moves += len(p1.moves)
            #buildBadData(p1, df_bad)
            #buildDataFrame(p2)
            #deleteBadRows(p1)
            win_lose_draw[1] += 1
            break
        win = testDraw(gameBoard)
        if win == 1:
            print("Draw!")
            total_moves += len(p1.moves)
            #buildDataFrame(p1, df)
            game_state = 1
            win_lose_draw[2] += 1
            break
        
        if turn == 0: #player 1
            p1.states.append(convertBoard(gameBoard, 1)) #adds the current board to the players moveset
            
            char = analyzePossibleMoves(gameBoard, 1, clf)
            y = getY(char)
            x = getX(char)
            gameBoard[y][x] = "x"
            turn = 1
            
            p1.moves.append("{" + "{0}, {1}".format(y, x) + "}") #adds the move the player chose to the moveset
            continue
        
        if turn == 1: #player 2
            p2.states.append(convertBoard(gameBoard, 2)) #adds the current board to the players moveset
            done = 0
            while done == 0:
                char = str(random.randint(1,10))
                #char = input("Make a move: ")
                y = getY(char)
                x = getX(char)
                if gameBoard[y][x] == "_":
                    done = 1
                #else:
                 #   print("Try again")
            gameBoard[y][x] = "o"
            turn = 0

            p2.moves.append("{" + "{0}, {1}".format(y, x) + "}") #adds the move the player chose to the moveset
            continue
    print(str(num) + '    ' + str(win_lose_draw[0]) + ' : ' + str(win_lose_draw[1]))
endTime = datetime.datetime.now()

#Now we'll get some stats on the games played
print("Number of games: " + str(games))
print("Average number of moves per game: " + str(total_moves / games))
print("Win: " + str(win_lose_draw[0]))
print("Lose: " + str(win_lose_draw[1]))
print("Draw: " + str(win_lose_draw[2]))
print("Start time: " + str(startTime))
print("End time: " + str(endTime))
print("Time elapsed: " + str(endTime-startTime))

    