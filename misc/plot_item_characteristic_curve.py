import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def item_c_curve_func(theta, delta):
    return np.exp(theta - delta) / (1 + np.exp(theta - delta))

theta_list = np.linspace(-4, 4, 1000, endpoint=True)
delta_list = np.round(np.linspace(-1, 1, 5, endpoint=True), 2)

custom_palette = ['#cf4456', '#f29566', '#831c64', '#2f0f3e', '#feedb0']
plt.rcParams['axes.prop_cycle'] = plt.cycler('color', custom_palette)
# plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'sans-serif'

fig, (ax) = plt.subplots(nrows=1, ncols=1, figsize=(8,5))

for delta in delta_list:
    plt.plot(theta_list, item_c_curve_func(theta_list, delta), lw = 3, label = r'$\delta$ = ' + f"{delta}")


ax.legend(prop={'size': 14})
ax.set_xlabel(f'Latent Ability, ' + r'$\theta$', fontsize=14)
ax.set_ylabel(f'Probability Correct ' + r'($P(X = 1| \theta, \delta)$)', fontsize=14)
fmt = matplotlib.ticker.StrMethodFormatter("{x:.1f}")
ax.xaxis.set_major_formatter(fmt)
ax.yaxis.set_major_formatter(fmt)
ax.tick_params(labelsize=14)

fig.tight_layout()
filename = './misc/item_characteristic_curve_example.png'
plt.savefig(filename)
plt.savefig(filename.replace(".png", ".svg"))