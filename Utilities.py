import math
import random
from re import sub


#Clamp a value to range (min,max)
def clamp(min,max,value):
    if value < min:
        return min
    if value > max:
        return max
    return value

#check if a list has duplicates
def ListHasDuplicates(inputlist):
    if len(inputlist) == len(set(inputlist)):
        return False
    else:
        return True 

#takes float from 0.0 to 1.0 and displays color gradient equivalent in hex
def interpolateRedtoGreen(amount):
    r,g,b = 0,0,0
    if amount < .5:
        r = 255
        g = 510 * amount
    elif amount >= .5 and amount <= 1:
        g = 255
        r = (1-amount) * 510
    elif amount > 1:
        g = 255
        b =  255 * (1-amount)/.3
    
    r = clamp(0,255,r)
    g = clamp(0,255,g)
    b = clamp(0,255,b)
    return '#%02x%02x%02x' % (int(r), int(g), int(b))

#count the number of places for a given number
def countPlaces(number):
    count = 0
    while number != 0:
        number //= 10
        count += 1
    return count

def getRandomValue(min,max):
    '''get a random number between min and max, inclusive'''
    result = random.randint(min,max)
    return result


def stitchString(string,index,substring,removalAmount = -1):
    '''returns a string with substring replacing the characters at index, replaces removalAmount characters'''
    #if the substring does not start the new string
    if index != 0:
        resultstring = string[:index]
        resultstring += substring
    else:
        resultstring = substring

    if removalAmount == -1:
        resultstring += string[index+len(substring):]
    else:
        resultstring += string[index+removalAmount:]
    return resultstring

