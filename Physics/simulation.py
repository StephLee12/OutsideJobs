import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint


class Simulation:
    def __init__(self):
        self.e = 1.602176565e-19
        self.m_pr = 1.672621777e-27
        self.m_el = 9.10938291e-31
        self.c = float(299792458)
        self.Re = float(6378137)
        self.B0, self.R0 = 2.0, 1.85
        self.rel = 1
        self.solution = None

    def set_rr(self, x, y, z, t=0):
        term_1 = np.sqrt(np.sum(np.square([x, y]))) - self.R0
        term_1 = np.sqrt(np.sum(np.square([term_1, z]))) + 1e-10
        return term_1

    def set_qq(self, x, y, z, t=0):
        return 1.0 + np.square(self.set_rr(x, y, z))

    def set_Bt(self, x, y, t=0):
        return self.B0 * self.R0 / np.sqrt(np.sum(np.square([x, y])))

    def set_Bp(self, x, y, z, t=0):
        return self.set_Bt(x, y) * self.set_rr(
            x, y, z) / (self.set_qq(x, y, z) * self.R0)

    def set_Bt_kmk_x(self, x, y, z, t=0):
        term_1 = y / np.sqrt(np.sum(np.square([x, y])))
        term_2 = x / np.sqrt(np.sum(np.square([x, y])))

        term_1 *= (-self.set_Bt(x, y))
        term_2 *= (self.set_Bp(x, y, z) * z / self.set_rr(x, y, z))

        return term_1 - term_2

    def set_Bt_kmk_y(self, x, y, z, t=0):
        term_1 = x / np.sqrt(np.sum(np.square([x, y])))
        term_2 = y / np.sqrt(np.sum(np.square([x, y])))

        term_1 *= (self.set_Bt(x, y))
        term_2 *= (self.set_Bp(x, y, z) * z / self.set_rr(x, y, z))

        return term_1 - term_2

    def set_Bt_kmk_z(self, x, y, z, t=0):
        term = np.sqrt(np.sum(np.square([x, y]))) - self.R0
        return self.set_Bp(x, y, z) * term / self.set_rr(x, y, z)

    def set_BBt_kmk(self, x, y, z, t=0):
        return np.sqrt(
            np.sum(
                np.square([
                    self.set_Bt_kmk_x(x, y, z),
                    self.set_Bt_kmk_y(x, y, z),
                    self.set_Bt_kmk_z(x, y, z)
                ])))

    def set_B_tokamak(self, x, y, z, t=0):
        return [
            self.set_Bt_kmk_x(x, y, z),
            self.set_Bt_kmk_y(x, y, z),
            self.set_Bt_kmk_z(x, y, z)
        ]

    def solve_newton_lorenz(self, y, t, q, m):
        vsq = np.sum(np.square([y[3], y[4], y[5]]))
        gamma = 0
        if self.rel == 1:
            gamma = 1.0 / np.sqrt(1 - vsq / np.square(self.c))
        else:
            gamma = 1

        Bvec = self.set_B_tokamak(y[0], y[1], y[2], t)
        Bx, By, Bz = Bvec[0], Bvec[1], Bvec[2]

        fac = q / (m * gamma)
        return np.array([
            y[3], y[4], y[5], fac * (Bz * y[4] - By * y[5]),
            fac * (Bx * y[5] - Bz * y[3]), fac * (By * y[3] - Bx * y[4])
        ])

    def run(self):
        m, q = self.m_pr, self.e
        K = 3.5e5 * self.e
        x0, y0, z0 = 1.2 * self.R0, 0, 0
        pitch_angle = 70
        v = self.c / np.sqrt(1 + (self.m_pr * np.square(self.c) / K))
        v_para0 = v * np.cos(pitch_angle * np.pi / 180)
        v_perp0 = v * np.sin(pitch_angle * np.pi / 180)

        Bt_kmk_x0 = self.set_Bt_kmk_x(x0, y0, z0, 0)
        Bt_kmk_y0 = self.set_Bt_kmk_y(x0, y0, z0, 0)
        Bt_kmk_z0 = self.set_Bt_kmk_z(x0, y0, z0, 0)
        BBt_kmk_0 = self.set_BBt_kmk(x0, y0, z0, 0)

        tmp = np.sqrt(np.sum(np.square([Bt_kmk_x0, Bt_kmk_y0])))
        v_x0 = (v_para0 * Bt_kmk_x0 +
                v_perp0 * Bt_kmk_x0 * Bt_kmk_z0 / tmp) / BBt_kmk_0
        v_y0 = (v_para0 * Bt_kmk_y0 +
                v_perp0 * Bt_kmk_y0 * Bt_kmk_z0 / tmp) / BBt_kmk_0
        v_z0 = (v_para0 * Bt_kmk_z0 - v_perp0 * tmp) / BBt_kmk_0

        T = 2 * np.pi * m / (abs(q) * self.B0)
        dt = T / 16
        tend = 800 * T
        t_series = np.arange(0, tend, dt)
        yy0 = np.array([x0, y0, z0, v_x0, v_y0, v_z0])
        sol = odeint(self.solve_newton_lorenz, yy0, t_series, args=(q, m))
        self.solution = sol

        fig = plt.figure()
        ax = Axes3D(fig)

        ax.scatter(xs=x0, ys=y0, zs=z0, marker='o')
        ax.plot(sol[:, 0], sol[:, 1], sol[:, 2], color='r')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        #v0 = np.sqrt(np.sum(np.square([v_x0, v_y0, v_z0])))
        ax.quiver(x0, y0, z0, v_x0, v_y0, v_z0, length=1.5)
        ax.set_title('Tokamak,R_0={},m,E={}keV'.format(self.R0,
                                                       K / (self.c * 1e3)))
        u, v = np.meshgrid(np.arange(0, 2 * np.pi, 2 * np.pi / 50),
                           np.arange(0, 1.5 * np.pi, 2 * np.pi / 50))
        X = (self.R0 + 0.5 * self.R0 * np.cos(u)) * np.cos(v)
        Y = (self.R0 + 0.5 * self.R0 * np.cos(u)) * np.sin(v)
        Z = 0.5 * self.R0 * np.sin(u)
        ax.plot_surface(X, Y, Z, cmap='rainbow')
        #ax.axis('equal')
        plt.show()


if __name__ == "__main__":
    sim_obj = Simulation()
    sim_obj.run()
