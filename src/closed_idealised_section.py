from typing import List, Tuple
import json
class Load:
    def __init__(self, M_x, M_y, S_x, S_y, xi, eta):
        self.M_x = M_x
        self.M_y = M_y
        self.S_x = S_x
        self.S_y = S_y
        self.xi = xi
        self.eta = eta
    
    def set_xi(self, xi):
        self.xi = xi

    def set_eta(self, eta):
        self.eta = eta
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
        I_xy += b.area * (b.x - centroid.x) * (b.y - centroid.y)
    return SecondMomentOfArea(I_xx, I_yy, I_xy)

def convert_centroidal_coords(booms: List[Boom], centroid: Centroid):
    booms_centroidal = []
    for boom in booms:
        new_boom = Boom(boom.x - centroid.x, boom.y - centroid.y, boom.area)
        booms_centroidal.append(new_boom)
    return booms_centroidal

def load_to_centroid(load: Load, centroid: Centroid):
    load.xi = load.xi - centroid.x
    load.eta = load.eta - centroid.y
    return load

def calc_bending_stress(booms: List[Boom], I: SecondMomentOfArea, load: Load) -> List:
    bending_stresses = []
    C1 = (load.M_y * I.xx - load.M_x * I.xy) / (I.xx * I.yy - I.xy ** 2)
    C2 = (load.M_x * I.yy - load.M_y * I.xy) / (I.xx * I.yy - I.xy ** 2)
    for i in range(len(booms)):
        x = booms[i].x
        y = booms[i].y
        sigma_z = C1 * x + C2 * y
        bending_stresses.append(sigma_z)
    return bending_stresses

def area_subtended(x_1, y_1, x_2, y_2):
    return ((x_1 * y_2) - (x_2 * y_1)) / 2

def enclosed_panel_areas(booms: List[Boom], n_qb: int):
    area_panels = [0] * n_qb
    for i in range(0, n_qb - 1):
        area_panels[i] = area_subtended(booms[i].x, booms[i].y, booms[i + 1].x, booms[i + 1].y)
    area_panels[n_qb - 1] = area_subtended(booms[n_qb - 1].x, booms[n_qb - 1].y, booms[0].x, booms[0].y)
    return area_panels

def calc_shear_flow(booms: List[Boom], nPanels: int, I: SecondMomentOfArea, load: Load) -> List:
    A = -(load.S_x * I.xx - load.S_y * I.xy)/(I.xx * I.yy - I.xy ** 2)
    B = -(load.S_y * I.yy - load.S_x * I.xy)/(I.xx * I.yy - I.xy ** 2)
    q_b = [0] * nPanels
    for i in range(1, nPanels):
        q_b[i] = q_b[i - 1] + (A * booms[i].x * booms[i].area) + (B * booms[i].y * booms[i].area)
    areas = enclosed_panel_areas(booms, len(q_b))
    T_q = []
    for i in range(nPanels):
        T_q.append(q_b[i] * areas[i])
    qs_0 = ((load.S_y * load.xi - load.S_x * load.eta) - 2 * sum(T_q)) / (2 * sum(areas))
    q_s = [q + qs_0 for q in q_b]
    return q_s

def shear_flow_to_stress(q_s: List, t):
    return [q / t for q in q_s]

if __name__ == '__main__':
    booms = get_booms()
    centroid = calc_centroid(booms)
    print(f"Centroid location: {centroid}")
    I = calc_section_I(booms, centroid)
    print(f"Second Moments of Area: {I}")
    M_x, M_y, S_x, S_y, xi, eta = [float(x) for x in input("Enter M_x, M_y, S_x, S_y, xi, eta: ").split()]
    load = load_to_centroid(Load(M_x, M_y, S_x, S_y, xi, eta), centroid)
    sigma_z = calc_bending_stress(booms, I, load)
    print(f'Bending stress: {sigma_z}')
    q_s = calc_shear_flow(convert_centroidal_coords(booms, centroid), len(booms), I, load) # TODO: Process input + convert S into centroidal coords
    print(f'Shear flows: {q_s}')
    tau = shear_flow_to_stress(q_s, 3)
    print(f'Shear stress: {tau}')