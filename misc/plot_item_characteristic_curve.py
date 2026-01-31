import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def item_c_curve_func(theta, delta):
    return np.exp(theta - delta) / (1 + np.exp(theta - delta))

theta_list = np.linspace(-4, 4, 1000, endpoint=True)
delta_list = np.round(np.linspace(-1, 1, 5, endpoint=True), 2)

custom_palette = ['#cf4456', '#f29566', '#831c64', '#2f0f3e', '#feedb0']
plt.rcParams['axes.prop_cycle'] = plt.cycler('color', custom_palette)
plt.rcParams['text.usetex'] = True
font = {'size'   : 16}

matplotlib.rc('font', **font)

fig, (ax) = plt.subplots(nrows=1, ncols=1, figsize=(10,6))

for delta in delta_list:
    plt.plot(theta_list, item_c_curve_func(theta_list, delta), lw = 3, label = r'$\delta$ = ' + f"{delta}")


ax.legend()
ax.set_xlabel(f'Latent Ability, ' + r'$\theta$')
ax.set_ylabel(f'Probability Correct ' + r'($P(X = 1| \theta, \delta)$)')
fmt = matplotlib.ticker.StrMethodFormatter("{x:.1f}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt)
fig.tight_layout()
plt.savefig('./misc/item_characteristic_curve_example.png')