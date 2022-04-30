def get_sections():
    num_sec = int(input("How many sections? "))

    sections = []

    for i in range(num_sec):
        print(f"Enter section properties for section {i+1} (in mm): ")
        b = float(input("Enter b: "))
        h = float(input("Enter h: "))
        x_prime = float(input("Enter x': "))
        y_prime = float(input("Enter y': "))
        area = b * h
        section = {'b': b, 'h': h, 'area': area, 'x_prime': x_prime, 'y_prime': y_prime}
        sections.append(section)

    return sections

def total_area(sections):
    area_total: float = 0
    for section in sections:
        area_total += section['area']
    return area_total

def centroidal_coords(sections, area):
    x_bar = y_bar = Sx = Sy = 0
    for section in sections:
        Sx += (section['area'] * section['x_prime'])
        Sy += (section['area'] * section['y_prime'])

    x_bar = Sx/area
    y_bar = Sy/area

    return (x_bar, y_bar)

def calc_I(b, h, x, y, area):
    I_xx = (b*(h**3))/12 + area*(y**2)
    I_yy = (h*(b**3))/12 + area*(x**2)
    I_xy = area * x * y
    return (I_xx, I_yy, I_xy)

def sec_mom_area(sections, x_bar, y_bar):
    I_xx = I_yy = I_xy = 0
    for section in sections:
        x = section['x_prime'] - x_bar
        y = section['y_prime'] - y_bar
        sec_I_xx, sec_I_yy, sec_I_xy = calc_I(section['b'], section['h'], x, y, section['area'])
        I_xx += sec_I_xx
        I_yy += sec_I_yy
        I_xy += sec_I_xy
    return (I_xx, I_yy, I_xy)

def bending_stress(M_x, M_y, x, y, I_xx, I_yy, I_xy):
    den = I_xx * I_yy - I_xy ** 2
    A = (M_y * I_xx - M_x * I_xy) / den
    B = (M_x * I_yy - M_y * I_xy) / den
    sigma_z = A * x + B * y
    return sigma_z

if __name__ == "__main__":
    sections = get_sections()
    area = total_area(sections)
    x_bar, y_bar = centroidal_coords(sections, area)
    print(f"Centroid location: x_bar = {x_bar}, y_bar = {y_bar}")
    I_xx, I_yy, I_xy = sec_mom_area(sections, x_bar, y_bar)
    print(f"Section properties: I_xx = {I_xx}, I_yy = {I_yy}, I_xy = {I_xy}")
    M_x = float(input("Enter M_x: "))
    M_y = float(input("Enter M_y: "))
    while True:
        x = float(input("Enter x: "))
        y = float(input("Enter y: "))
        print(f"sigma_z = {bending_stress(M_x, M_y, x, y, I_xx, I_yy, I_xy)}")