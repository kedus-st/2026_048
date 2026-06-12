import math
wetstore_cell = 'D4'
column = ord(wetstore_cell[0]) - ord('A')
row = int(wetstore_cell[1:]) - 1
print(column)
print(row)            
easting = 0 + column*(20/math.sqrt(25))*math.cos(30*math.pi/180)+(20/math.sqrt(25))/2
northing = 0 - row*(20/math.sqrt(25))*math.sin((60-0)*math.pi/180)-(20/math.sqrt(25))/2

print(easting)
print(northing)
