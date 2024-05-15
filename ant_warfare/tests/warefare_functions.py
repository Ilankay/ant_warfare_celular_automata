import numpy as np
import random


def build_field(food_amount: int, field_size: int) -> np.ndarray:
    """returns the first of size field_size with a set amount of food food_amount"""
    assert food_amount < (field_size-1)*(field_size-1)
    field = np.zeros((field_size, field_size, 3))
    field[:, :, 0] = -1
    for _ in range(food_amount):
        randx = random.randint(1, field_size-2)
        randy = random.randint(0, field_size-1)
        while field[randy, randx, 1] != 0:
            randx = random.randint(1, field_size-2)
            randy = random.randint(0, field_size-1)
        field[randy, randx, 1] = 1
    # return np.reshape(field,(field_size,field_size))
    return field


neiToField = {
    0: [-1, -1],
    1: [0, -1],
    2: [1, -1],
    3: [-1, 0],
    4: [1, 0],
    5: [-1, 1],
    6: [0, 1],
    7: [1, 1]
}


def nei_to_field(neiIndex, fieldX, fieldY):
    """does neighbor to field"""
    return neiToField[neiIndex][1] + fieldY, neiToField[neiIndex][0] + fieldX


def neighbors(col: int, row: int, field: np.ndarray) -> np.ndarray:
    """x - x index, y - y index\n
    this function returns a 2 dimensional array of shape(8,3) signifying every spot around the ant where every cell of the array is an ant.\n
    the array is sorted like this where 4 is the ant: \n
    0 1 2
    3 * 4
    5 6 7 
    """
    count = 0
    nei = np.zeros((8, 3))
    for i in range(0, 3):
        for j in range(0, 3):
            if j == 1 and i == 1:
                continue
            if not (row-1+i < 0 or col-1+j < 0 or row-1+i >= len(field[0]) or col-1+j >= len(field[0])):
                nei[count] = field[row-1+i, col-1+j]
            else:
                nei[count] = np.zeros(3)-1
            count += 1
    return nei


def warfare(field: np.ndarray, nei: np.ndarray, x: int, y: int):
    field = field.copy()
    team = field[y, x, 0]
    for index, i in enumerate(nei):
        if i[0] != -1 and i[0] != team:
            loc = nei_to_field(index, x, y)
            randnum = random.random()
            if randnum > 0.5:  # other ant wins
                field[y, x, 0] = -1  # kills ant
                field[loc[0], loc[1], 1] = 1  # gives other ant food (maybe)
                field[x,y,1]=0 # removes the old food
            else:  # this ant wins
                field[y, x][1] = 1  # gives ant food (maybe)
                field[loc[0], loc[1],0] = -1  # kills ant
                field[loc[0],loc[1]][1]=0 # removes the old food
            break
    return field


test_field = build_field(0, 4)

test_field[1][1][0] = 1
test_field[1][1][1] = 1
test_field[2][1][0] = 0

print(test_field, "\n")
nei = neighbors(1, 1, test_field)
# print(nei)
test_field = warfare(test_field, nei, 1, 1)
print(test_field)
print(test_field[1,1,0]== -1 or test_field[2,1,0] ==-1)