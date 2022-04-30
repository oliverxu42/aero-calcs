from prettytable import PrettyTable
import math

table = PrettyTable(["k", "E", "nu", "t", "b"])


k = float(input("Enter k: "))
E = float(input("Enter E: "))
nu = float(input("Enter nu: "))
t = float(input("Enter t: "))
b = float(input("Enter b: "))

table.add_row([k, E, nu, t, b])
print(table)


sigma_cr = (k * (math.pi ** 2) * E)/(12 * (1 - nu ** 2)) * (t / b) ** 2
print(sigma_cr)