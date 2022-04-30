from typing import List, Tuple
import json

class Boom:
    def __init__(self, x, y, area):
        self.x = x
        self.y = y
        self.area = area

    def x(self):
        return self.x
    
    def y(self):
        return self.y

    def area(self):
        return self.area


    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.area})"

def get_booms():
    with open("booms.json", "r") as read_file:
        data = json.load(read_file)

    booms = []

    for boom in data['booms']:
        new_boom = Boom(boom['x'], boom['y'], boom['area'])
        booms.append(new_boom)

    return booms

def get_centroid(booms: List[Boom]) -> Tuple[float, float]:
    A_x = A_y = area_total = 0
    for b in booms:
        A_x += b.area * b.x
        A_y += b.area * b.y
        area_total += b.area
    cen_x = A_x / area_total
    cen_y = A_y / area_total
    return(cen_x, cen_y)

def get_section_I(booms: List[Boom], cen_x, cen_y):
    I_xx = I_yy = I_xy = 0
    for b in booms:
        I_xx += b.area * (b.y - cen_y) ** 2
        I_yy += b.area * (b.x - cen_x) ** 2
        I_xy += b.area * b.x * b.y
    return (I_xx, I_yy, I_xy)

if __name__ == '__main__':
    booms = get_booms()
    cen_x, cen_y = get_centroid(booms)
    print(get_section_I(booms, cen_x, cen_y))
    