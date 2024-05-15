import numpy as np
neiToField = {
    0: [-1,-1],
    1: [0,-1],
    2: [1,-1],
    3: [-1,0],
    4: [1,0],
    5: [-1,1],
    6: [0,1],
    7: [1,1]
}
def nei_to_field(neiIndex, fieldX, fieldY):
    """does neighbor to field"""
    return  neiToField[neiIndex][1] + fieldY, neiToField[neiIndex][0] + fieldX

def neighbors(col:int, row:int, field:np.ndarray)-> np.ndarray:
    """x - x index, y - y index\n
    this function returns a 2 dimensional array of shape(8,3) signifying every spot around the ant where every cell of the array is an ant.\n
    the array is sorted like this where 4 is the ant: \n
    0 1 2
    3 * 4
    5 6 7 
    """
    count = 0
    nei = np.zeros((8,3))
    for i in range(0,3):
        for j in range(0,3):
            if j == 1 and i ==1:
                continue
            if not(row-1+i<0 or col-1+j<0 or row-1+i>=len(field[0]) or col-1+j>=len(field[0])):
                nei[count] = field[row-1+i, col-1+j]
            else:
                nei[count] = np.zeros(3)-1
            count +=1
    return nei

def warfare(field:np.ndarray, nei:np.ndarray, x:int, y:int):
   field = field.copy()
   team = field[y,x,0]
   for index,i in enumerate(nei): 
      if i[0] != -1 and i[0] != team:
         loc = nei_to_field(index, x,y)
         randnum = random.random()
         if randnum > 0.5: #other ant wins 
            field[y,x, 0] = 0 #kills ant
            field[loc[1], loc[0], 1] = 1 #gives other ant food (maybe) 
         else: #this ant wins 
            field[y,x][1] = 1 #gives ant food (maybe)
            field[loc[1], loc[0]][0] = 0 #kills ant
         break
   return field

def take_food(field:np.ndarray, nei:np.ndarray, antIndexY: int, antIndexX: int) -> np.ndarray: #only happend if the ant goes on the food
    """get the field and ant Indexes (x,y) and return the new field
     where the ant moved and takes the food
      if there is no food return None """
    field = field.copy()
    foodInd = -1
    for index in range(len(nei)):
        if(nei[index][0] == -1 and nei[index][1] == 1): #is food
            foodInd = index
            break
    
    if(foodInd == -1):
        return None
    x, y = nei_to_field(foodInd, antIndexX, antIndexY)

    field[y,x][1] = 0 #remove the food
    field[antIndexY,antIndexX][1] = 1 #add food
    smellAntPrev = field[antIndexY,antIndexX][2] + 1 # add smell to the place the ant was in
    field[antIndexY,antIndexX][2] = field[y,x][2] #put the smell of the place of the food in the the ant Array
    ant = field[antIndexY,antIndexX] #save the ant
    field[antIndexY,antIndexX] = [0,0,smellAntPrev] #put the new smell and the empty place at the old place of the ant
    field[y,x] = ant #replace the ant

    return field

def move_to_scent(field:np.ndarray, nei:np.ndarray, x:int, y:int) -> np.ndarray:
    field = field.copy()
    team = field[y,x,0]
    field[y,x,2] = field[y,x,2]+1*(1-2*team)
    ant = field[y,x].copy()
    for index,cell in enumerate(nei):
        if cell[1] != -1:
            smell_min = abs(ant[2]-nei[index,2])
            smell_min_ind = index
    for index,cell in enumerate(nei):
        if cell[1] == -1:
            continue
        if abs(ant[2]-cell[2])<=smell_min:
            smell_min = abs(ant[2]-cell[2])
            smell_min_ind = index
    new_pos = nei_to_field(smell_min_ind,x,y)
    print(new_pos)
    field[new_pos[1],new_pos[0],0] = ant[0]
    field[new_pos[1],new_pos[0],1] = ant[1]
    field[y,x] = np.array([-1,0,field[y,x,2]])
    return field