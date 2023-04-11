import matplotlib.pyplot as plt

def showfig(x, y, gtype='plot', xlabel='', ylabel='', title='', savetitle=''):
  fig, ax = plt.subplots()
  if gtype == 'plot':
    ax.plot(x, y, linewidth=2, label='')
  elif gtype == 'bar':
    ax.bar(x, y, linewidth=2, label='')

  ax.set_xlim()
  ax.set_ylim()

  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel) 
  ax.set_title(title)

  ax.minorticks_on()
  ax.tick_params(which='both', top='on', right='on', direction='in')
  ax.grid(which='major', axis='both')

  ax.legend(loc='lower right')
  plt.show()
  if savetitle:
    plt.savefig(f'{savetitle}')
