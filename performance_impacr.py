import numpy as np
import parameters as p
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def get_CD(CD_min, DR, k, CL, CL_minD):
    CD = CD_min * (1 - DR) + k * (CL - CL_minD)**2
    return CD

def get_CL(m, g, rho, V, S):
    CL = 2 * m * g / (rho * S * V**2)
    return CL

def get_R(E_star, n_prop, g, CL, CD, bat_mf, retr_mf, Ecr_Et):
    R = E_star * n_prop / g * CL / CD * (bat_mf - retr_mf) * Ecr_Et
    return R

def get_E_loiter(m, bat_mf, retr_mf, E_star, Eloit_Et):
    E = m * (bat_mf - retr_mf) * E_star * Eloit_Et
    return E

def get_Endurance(E_loiter, P_req, n_prop):
    t = E_loiter / P_req * n_prop
    return  t

def get_Preq(rho, V, S, CD):
    P_req =  rho * S * CD * V**3 / 2
    return P_req

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()
fig5, ax5 = plt.subplots()
fig6, ax6 = plt.subplots()

V = np.linspace(15, 30, 100)
# V = np.linspace(40, 90, 100)
DR = 0
retr_mf = 0
CL = get_CL(p.m, p.g, p.rho, V, p.S)
CD = get_CD(p.CD_min, DR, p.k, CL, p.CL_minD)
R_baseline = get_R(p.E_star, p.n_prop, p.g, CL, CD, p.bat_mf, retr_mf, p.Ecr_Et)
P_req_baseline = get_Preq(p.rho, V, p.S, CD)
P_400_baseline = P_req_baseline[P_req_baseline < 400][-1]
V_max_baseline = V[P_req_baseline == P_400_baseline]
E_loiter = get_E_loiter(p.m, p.bat_mf, retr_mf, p.E_star, p.E_loit_Et)
End_baseline = get_Endurance(E_loiter, P_req_baseline, p.n_prop)
ax1.plot(V, R_baseline / 1000, label = 'Baseline', color = 'black')
ax3.plot(V, End_baseline/3600, label = 'Baseline', color = 'black')
ax5.plot(V, P_req_baseline,    label = 'Baseline', color = 'black')
ax5.plot(V, 400 * np.ones(V.shape), label = r'Power limit, $\eta$ = 0.5')
ax6.plot(V, 0.5 * 1.225 * V**2 * p.S * CD, label='Baseline', color='black')
ax1.scatter(V_max_baseline, R_baseline[V==V_max_baseline]/1000, color = 'black', label = 'Max Speed')
ax3.scatter(V_max_baseline, End_baseline[V==V_max_baseline]/3600, color = 'black', label = 'Max Speed')




colors = ['red', 'darkorange', 'midnightblue', 'lawngreen']
linestyles = ['-', '--', '-.', ':']

for i in range(4):
    DR = 0.1 + 0.1 * i
    for j in range(3):
        retr_mf = 0.03 + 0.005 * j
        m_r = retr_mf * p.m / (1 - retr_mf)
        m = p.m + m_r
        print(m)
        CL = get_CL(m, p.g, p.rho, V, p.S)
        CD = get_CD(p.CD_min, DR, p.k, CL, p.CL_minD)
        R = get_R(p.E_star, p.n_prop, p.g, CL, CD, p.bat_mf, retr_mf, p.Ecr_Et)
        R_diff = 100 * (R - R_baseline) / R_baseline
        P_req = get_Preq(p.rho, V, p.S, CD)
        P_400 = P_req[P_req < 400][-1]
        V_max = V[P_req == P_400]
        E_loiter = get_E_loiter(m, p.bat_mf, retr_mf, p.E_star, p.E_loit_Et)
        End = get_Endurance(E_loiter, P_req, p.n_prop)
        End_diff = 100 * (End - End_baseline) / End_baseline
        print(End_diff[V == V_max])
        ax1.plot(V, R/1000, label = 'DR = ' + str(round(DR,3)) + ', retr_mf = ' + str(round(retr_mf,3)), color = colors[i], linestyle = linestyles[j])
        ax2.plot(V, R_diff, label = 'DR = ' + str(round(DR,3)) + ', retr_mf = ' + str(round(retr_mf,3)), color = colors[i], linestyle = linestyles[j])
        ax3.plot(V, End/3600, label = 'DR = ' + str(round(DR,3)) + ', retr_mf = ' + str(round(retr_mf,3)), color = colors[i], linestyle = linestyles[j])
        ax4.plot(V, End_diff, label = 'DR = ' + str(round(DR,3)) + ', retr_mf = ' + str(round(retr_mf,3)), color = colors[i], linestyle = linestyles[j])
        ax5.plot(V, P_req, label = 'DR = ' + str(round(DR,3)) + ', retr_mf = ' + str(round(retr_mf,3)), color = colors[i], linestyle = linestyles[j])
        ax6.plot(V, 0.5 * 1.225 * V**2 * p.S * CD, label = 'DR = ' + str(round(DR,3)) + ', retr_mf = ' + str(round(retr_mf,3)), color = colors[i], linestyle = linestyles[j])
        ax1.scatter(V_max, R[V == V_max] / 1000, color=colors[i])
        ax2.scatter(V_max, R_diff[V == V_max], color=colors[i])
        ax3.scatter(V_max, End[V == V_max] / 3600, color=colors[i])
        ax4.scatter(V_max, End_diff[V == V_max], color=colors[i])

ax1.set_title('Range vs. Speed')
ax1.set_xlabel('Speed [m/s]')
ax1.set_ylabel('Range [km]')
ax1.legend(fontsize = 8)
ax1.minorticks_on()
ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

ax2.set_title('Range vs. Speed')
ax2.set_xlabel('Speed [m/s]')
ax2.set_ylabel('Difference with baseline [%]')
ax2.legend(fontsize = 8)
ax2.minorticks_on()
ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

ax3.set_title('Endurance vs. Speed')
ax3.set_xlabel('Speed [m/s]')
ax3.set_ylabel('Endurance [h]')
ax3.legend(fontsize = 10)
ax3.minorticks_on()
ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

ax4.set_title('Endurance vs. Speed')
ax4.set_xlabel('Speed [m/s]')
ax4.set_ylabel('Difference with baseline [%]')
ax4.legend(fontsize = 8)
ax4.minorticks_on()
ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

ax5.set_title('Power vs. Speed')
ax5.set_xlabel('Speed [m/s]')
ax5.set_ylabel('Powrer [W]')
ax5.legend(fontsize = 8)
ax5.minorticks_on()
ax5.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

ax6.set_title('Drag vs. Speed')
ax6.set_xlabel('Speed [m/s]')
ax6.set_ylabel('Drag [N]')
ax6.legend(fontsize = 8)
ax6.minorticks_on()
ax6.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.show()