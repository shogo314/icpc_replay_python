# htmlから適当に抜き出したものを気合いでフォーマットするコード
import json
with open('standings-section_2023_yokohama.html', 'r', encoding='utf-8') as f:
    html_content = [l.strip() for l in f.readlines()]
i = 2
d = {'StandingsData': []}
while True:
    e = {}
    assert html_content[i][:15] == '<div data-key="'
    i += 1
    assert html_content[i][:24] == '<div class="team-row  ">'
    i += 1
    assert html_content[i][:23] == '<div class="team-left">'
    i += 1
    assert html_content[i][:11] == '<div></div>'
    i += 1
    assert html_content[i][:36] == '<div class="team-col team-mark"><i c'
    i += 1
    assert html_content[i][:6] == '</div>'
    i += 1
    assert html_content[i][:38] == '<div class="team-col team-rank"><span>'
    assert html_content[i][-32:] == '<br><small></small></span></div>'
    if html_content[i][38:-32] == '-':
        break
    Rank = int(html_content[i][38:-32])
    e['Rank'] = Rank
    i += 1
    assert html_content[i][:24] == '<div class="team-right">'
    i += 1
    assert html_content[i][:33] == '<div class="team-col team-score">'
    i += 1
    assert html_content[i][:32] == '<div class="team-colored-col-bg"'
    i += 1
    assert html_content[i][:33] == '<div class="team-colored-col-fg">'
    assert html_content[i][-15:] == ')</small></div>'
    assert '<br><small class="d-none d-md-inline">(' in html_content[i]
    sp = html_content[i][33:-
                         15].split('<br><small class="d-none d-md-inline">(')
    e['TotalResult'] = {}
    Score = int(sp[0])
    Penalty = int(sp[1])
    e['TotalResult']['Score'] = Score
    e['TotalResult']['Penalty'] = Penalty
    i += 1
    assert html_content[i] == '</div>'
    i += 1
    assert html_content[i][:38] == '<div class="team-col team-name"><span>'
    assert html_content[i][-7:] == '<small>'
    assert '<br><small><span>' in html_content[i]
    sp = html_content[i][38:-7].split('<br><small><span>')
    TeamName = sp[0]
    University = sp[1]
    e['TeamName'] = TeamName
    e['University'] = University
    i += 1
    assert html_content[i][-36:] == '</small></span></small></span></div>'
    UniversityStanding = html_content[i][:-36]
    i += 1
    assert html_content[i][:27] == '<div class="team-problems">'
    i += 1
    e['TaskResults'] = {}
    for c in 'ABCDEFGHIJK':
        e['TaskResults'][c] = {}
        assert html_content[i] == '<div class="team-col team-problem">'
        i += 1
        assert html_content[i][:35] == '<div class="team-colored-col-bg bg-'
        i += 1
        assert html_content[i][:39] == '<div class="team-colored-col-fg"><span>'
        if html_content[i][-6:] == '</div>':
            assert html_content[i][-21:] == '</small></span></div>'
            assert '<br><small>' in html_content[i]
            sp = html_content[i][39:-21].split('<br><small>')
            Elapsed = sp[0]
            Penalty = sp[1]
            i += 1
        else:
            assert html_content[i][-15:] == '</small></span>'
            assert '<br><small>' in html_content[i]
            sp = html_content[i][39:-15].split('<br><small>')
            Elapsed = sp[0]
            Penalty = sp[1]
            i += 1
            assert html_content[i] == '</div>'
            i += 1
        e['TaskResults'][c]['Elapsed'] = Elapsed
        if Penalty == '-' or Penalty == '':
            e['TaskResults'][c]['Penalty'] = 0
        else:
            if Penalty[:2] == '(+' and Penalty[-1:] == ')':
                e['TaskResults'][c]['Penalty'] = int(Penalty[2:-1])
            elif Penalty[:8] == '<span>(+' and Penalty[-8:] == ')</span>':
                e['TaskResults'][c]['Penalty'] = int(Penalty[8:-8])
            else:
                exit(1)
        assert html_content[i] == '</div>'
        i += 1
    print(e)
    for _ in range(4):
        # print(html_content[i])
        assert html_content[i] == '</div>'
        i += 1
    d['StandingsData'].append(e)
    if e['Rank']==58:
        break
with open('standings_2023_yokohama.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
