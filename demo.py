import ast
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, learning_curve
import matplotlib.pyplot as plt

card_dict = {'Archers': 3,
             'Arrows': 3,
             'Barbarians': 5,
             'Bats': 2,
             'Bomber': 3,
             'Cannon': 3,
             'Elite Barbarians': 6,
             'Fire Spirits': 2,
             'Goblin Gang': 3,
             'Goblins': 2,
             'Ice Spirit': 1,
             'Knight': 3,
             'Minion Horde': 5,
             'Minions': 3,
             'Mortar': 4,
             'Royal Giant': 6,
             'Skeletons': 1,
             'Spear Goblins': 2,
             'Tesla': 4,
             'Zap': 2,
             'Barbarian Hut': 7,
             'Battle Ram': 4,
             'Bomb Tower': 5,
             'Dart Goblin': 3,
             'Elixir Collector': 6,
             'Fireball': 4,
             'Furnace': 4,
             'Giant': 5,
             'Goblin Hut': 5,
             'Heal': 3,
             'Hog Rider': 4,
             'Ice Golem': 2,
             'Inferno Tower': 5,
             'Mega Minion': 3,
             'Mini P.E.K.K.A': 4,
             'Musketeer': 4,
             'Rocket': 6,
             'Three Musketeers': 9,
             'Tombstone': 3,
             'Valkyrie': 4,
             'Wizard': 5,
             'Baby Dragon': 4,
             'Balloon': 5,
             'Bowler': 5,
             'Clone': 3,
             'Dark Prince': 4,
             'Executioner': 5,
             'Freeze': 4,
             'Flying Machine': 4,
             'Giant Skeleton': 6,
             'Goblin Barrel': 3,
             'Golem': 8,
             'Guards': 3,
             'Lightning': 6,
             'Mirror': 0,
             'P.E.K.K.A': 7,
             'Poison': 4,
             'Prince': 5,
             'Rage': 2,
             'Skeleton Army': 3,
             'Tornado': 3,
             'Witch': 5,
             'X-Bow': 6,
             'Bandit': 3,
             'Electro Wizard': 4,
             'Graveyard': 5,
             'Ice Wizard': 3,
             'Inferno Dragon': 4,
             'Lava Hound': 7,
             'Lumberjack': 4,
             'Miner': 3,
             'Night Witch': 4,
             'Princess': 3,
             'Sparky': 6,
             'The Log': 2,
             'Cannon Cart': 5}

card_dict_list = list(card_dict.keys())

# mirror card takes elixir : +1 previous card elixir
# so we put average + 1 for mirror

avg = sum(card_dict.values()) / len(card_dict)
card_dict['Mirror'] = int(avg + 1)

file = open('matches.txt', encoding='utf-8')
raw_data = file.readlines()

# deleting erroneous row
del raw_data[277790]
del raw_data[200000:]
del raw_data[0:100000]
# too many rows to handle, deleting some

print(len(raw_data))
data_dict = [ast.literal_eval(row) for row in raw_data]

# removing unwanted data
# adding trophy difference

for row in data_dict:
    del row['type']
    del row['time']
    del row['players']['left']['clan']
    del row['players']['right']['clan']
    del row['players']['left']['name']
    del row['players']['right']['name']
    row['trophy_diff'] = int(row['players']['right']['trophy']) - int(row['players']['left']['trophy'])

# adding average elixir and difference
for row in data_dict:
    sum_left = 0
    for card in row['players']['left']['deck']:
        sum_left += card_dict[card[0]]
    row['players']['left']['avg_elixir'] = str(sum_left / 8)

    sum_right = 0
    for card in row['players']['right']['deck']:
        sum_right += card_dict[card[0]]
    row['players']['right']['avg_elixir'] = str(sum_right / 8)

    row['avg_elixir_diff'] = str(sum_right / 8 - sum_left / 8)

# simplifying result
# 0->draw; 1-> right win; 2-> left win

for row in data_dict:
    if row['result'][0] > row['result'][1]:
        row['result'] = str(1)
    elif row['result'][0] < row['result'][1]:
        row['result'] = str(2)
    else:
        row['result'] = str(0)

# adding average level of cards and difference
for row in data_dict:
    sum_right = 0
    for card in row['players']['right']['deck']:
        sum_right += int(card[1])
    row['players']['right']['avg_level'] = str(sum_right / 8)

    sum_left = 0
    for card in row['players']['left']['deck']:
        sum_left += int(card[1])
    row['players']['left']['avg_level'] = str(sum_left / 8)

    row['avg_level_diff'] = str(sum_right / 8 - sum_left / 8)

for row in data_dict:
    temp1 = [0] * card_dict_list.__len__()
    temp2 = [0] * card_dict_list.__len__()

    for card in row['players']['right']['deck']:
        temp1[card_dict_list.index(card[0])] = card[1]

    row['players']['right']['deck'] = temp1

    for card in row['players']['left']['deck']:
        temp2[card_dict_list.index(card[0])] = card[1]

    row['players']['left']['deck'] = temp2

# creating a list with the correct tabular form now
final_list = []

for row in data_dict:
    temp = [*row['players']['right']['deck'], *row['players']['left']['deck'], row['players']['right']['avg_elixir'],
            row['players']['left']['avg_elixir'], row['avg_elixir_diff'], row['players']['right']['avg_level'],
            row['players']['left']['avg_level'], row['avg_level_diff'], row['players']['right']['trophy'],
            row['players']['left']['trophy'], row['trophy_diff'], row['result']]
    final_list.append(temp)

classifier = LogisticRegression(random_state=0)
X = []
Y = []
for row in final_list:
    X.append(row[:-1])
    Y.append(row[-1])

X = np.array(X, dtype='float')
Y = np.array(Y, dtype='float')

X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

classifier.fit(X_train, Y_train)

pred = classifier.predict(X_test)

conf_matrix = confusion_matrix(Y_test, pred)
print(conf_matrix)

print(classifier.score(X_test, Y_test))
print(classification_report(Y_test, pred))

train_sizes, train_scores, test_scores = learning_curve(classifier, X, Y)

train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.figure()
plt.title("Logistic Regression")
plt.legend(loc="best")
plt.xlabel("Training examples")
plt.ylabel("Score")
plt.ylim((0.6, 1.01))
plt.gca().invert_yaxis()
plt.grid()

plt.plot(train_sizes, train_scores_mean, 'o-', color="b", label="Training score")
plt.plot(train_sizes, test_scores_mean, 'o-', color="r", label="Test score")

plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std,
                 alpha=0.1, color="b")
plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std,
                 alpha=0.1, color="r")

plt.draw()
plt.show()
plt.gca().invert_yaxis()

# adding headers at the top
# temp = [*[s + '1' for s in card_dict_list], *[s + '2' for s in card_dict_list], 'Player1 avg_elixir',
#        'Player2 avg_elixir', 'Elixir diff',
#       'Player1 avg_card_level',
#        'Player2 avg_card_level', 'Level diff', 'Player1 trophy', 'Player2 trophy', 'Trophy diff', 'Result']

# final_list.insert(0, temp)


# with open('final_data.csv', 'a', newline='') as file:
#   writer = csv.writer(file)
# writer.writerows(final_list)
