from load_standing import Standings
import matplotlib.pyplot as plt
Standing = Standings()
TeamName = 'KSS908111314'
if not Standing.exist_team(TeamName):
    raise ValueError
x = []
y = []
score = 0
solve_x = []
solve_y = []
for i in range(0, 3*60*60+1):
    x.append(i)
    y.append(Standing.time_rank(i, TeamName))
    if Standing._time_result(i, TeamName)[0] > score:
        score = Standing._time_result(i, TeamName)[0]
        solve_x.append(x[-1])
        solve_y.append(y[-1])
    print('\r'+'{:.2f}'.format(100*i/(3*60*60))+'%', end='')

fig, ax = plt.subplots()
ax.invert_yaxis()
ax.plot(x, y, '-')
for sx, sy in zip(solve_x, solve_y):
    ax.annotate(str(sy), (sx, sy), textcoords="offset points",
                xytext=(0, 10), ha='center')
ax.set_xlabel('経過時間（秒）', fontname="MS Gothic")
ax.set_ylabel('順位', fontname="MS Gothic")
ax.set_title(TeamName)
plt.show()
