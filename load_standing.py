from typing import *


class Standings:
    def __init__(self) -> None:
        import json
        with open('standings_2023_yokohama.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
        self.val: dict[str, list[tuple[Optional[int], int]]] = {}
        for e in d['StandingsData']:
            TeamName = e['TeamName']
            self.val[TeamName]: list[tuple[Optional[int], int]] = []
            for c in 'ABCDEFGHIJK':
                if e['TaskResults'][c]['Elapsed'] == '-':
                    Elapsed = None
                else:
                    sp = e['TaskResults'][c]['Elapsed'].split(':')
                    sp.reverse()
                    Elapsed = sum(int(sp[i])*(60**i) for i in range(len(sp)))
                self.val[TeamName].append(
                    (Elapsed, e['TaskResults'][c]['Penalty']))

    def exist_team(self, team_name) -> bool:
        return team_name in self.val

    def _time_result(self, tm, team_name) -> tuple[int, int]:
        '''
        result
        ---
        Score, Penalty
        '''
        assert self.exist_team(team_name)
        score = 0
        penalty = 0
        for Elapsed, Penalty in self.val[team_name]:
            if Elapsed is None or tm < Elapsed:
                continue
            else:
                score += 1
                penalty += Elapsed
                penalty += Penalty*20
        return (score, penalty)

    def time_rank(self, tm, team_name) -> int:
        '''
        特定の時刻での順位を取得する。

        Parameters
        ---
        tm : int
            開始時刻から経過した時間（秒）
        team_name : str
            チーム名

        Returns
        ---
        rank : int
            順位
        '''
        assert self.exist_team(team_name)
        l = []
        for TeamName in self.val:
            Score, Penalty = self._time_result(tm, TeamName)
            l.append((-Score, Penalty))
        l.sort()
        Score, Penalty = self._time_result(tm, team_name)
        return 1+l.index((-Score, Penalty))
