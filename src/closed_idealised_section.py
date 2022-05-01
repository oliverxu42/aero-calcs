from typing import List, Tuple
import json

class Boom:
    def __init__(self, x, y, area):
        self.x = x
        self.y = y
        self.area = area
class Centroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'
class SecondMomentOfArea:
    def __init__(self, I_xx, I_yy, I_xy):
        self.xx = I_xx
        self.yy = I_yy
        self.xy = I_xy
    
    def __str__(self) -> str:
        return f'({self.xx}, {self.yy}, {self.xy})'

def get_booms():
    with open("booms.json", "r") as read_file:
        data = json.load(read_file)

    booms = []

    for boom in data['booms']:
        new_boom = Boom(boom['x'], boom['y'], boom['area'])
        booms.append(new_boom)

    return booms

def calc_centroid(booms: List[Boom]) -> Centroid:
    A_x = A_y = area_total = 0
    for b in booms:
        A_x += b.area * b.x
        A_y += b.area * b.y
        area_total += b.area
    cen_x = A_x / area_total
    cen_y = A_y / area_total
    return Centroid(cen_x, cen_y)

def calc_section_I(booms: List[Boom], centroid: Centroid):
    I_xx = I_yy = I_xy = 0
    for b in booms:
        I_xx += b.area * (b.y - centroid.y) ** 2
        I_yy += b.area * (b.x - centroid.x) ** 2
        I_xy += b.area * b.x * b.y
    return SecondMomentOfArea(I_xx, I_yy, I_xy)

def convert_centroidal_coords(booms: List[Boom], centroid: Centroid):
    booms_centroidal = []
    for boom in booms:
        new_boom = Boom(boom.x - centroid.x, boom.y - centroid.y, boom.area)
        booms_centroidal.append(new_boom)
    return booms_centroidal

def area_subtended(x_1, y_1, x_2, y_2):
    return ((x_1 * y_2) - (x_2 * y_1)) / 2

def enclosed_panel_areas(booms: List[Boom], n_qb: int):
    area_panels = [0] * n_qb
    for i in range(0, n_qb - 1):
        area_panels[i] = area_subtended(booms[i].x, booms[i].y, booms[i + 1].x, booms[i + 1].y)
    area_panels[n_qb - 1] = area_subtended(booms[n_qb - 1].x, booms[n_qb - 1].y, booms[0].x, booms[0].y)
    return area_panels

def calc_shear_flow(booms: List[Boom], nPanels: int, I: SecondMomentOfArea, Sx, Sy, xi, eta) -> List:
    A = -(Sx * I.xx - Sy * I.xy)/(I.xx * I.yy - I.xy ** 2)
    B = -(Sy * I.yy - Sx * I.xy)/(I.xx * I.yy - I.xy ** 2)
    q_b = [0] * nPanels
    for i in range(1, nPanels):
        print(booms[i].x, booms[i].y, booms[i].area)
        q_b[i] = q_b[i - 1] + (A * booms[i].x * booms[i].area) + (B * booms[i].y * booms[i].area)
        print(q_b)
    areas = enclosed_panel_areas(booms, len(q_b))
    T_q = []
    for i in range(nPanels):
        T_q.append(q_b[i] * areas[i])
    qs_0 = ((Sy * xi - Sx * eta) - 2 * sum(T_q)) / (2 * sum(areas))
    print(qs_0)
    q_s = [q + qs_0 for q in q_b]
    return q_s

if __name__ == '__main__':
    booms = get_booms()
    centroid = calc_centroid(booms)
    print(f"Centroid location: {centroid}")
    I = calc_section_I(booms, centroid)
    print(f"Second Moments of Area: {I}")
    q_s = calc_shear_flow(convert_centroidal_coords(booms, centroid), len(booms), I, 0, 10e3, 150 - centroid.x, 0) # TODO: Process input + convert S into centroidal coords
    print(q_s)