import pandas as pd

import tracksim
from tracksim import reader
from tracksim.analysis import shared
from tracksim.analysis import report

report.add_header('Generated Parameter Space Analysis')

results_path = tracksim.load_configs().get('path.group_comparison')
results = reader.all_groups(results_path=results_path)

couplings = dict()
trial_info = []

for trial in results['trials']:
    group = trial['group']
    id_parts = trial['id'].split('-')

    trial_info.append({
        'index': trial['global_index'],
        'trial_index': trial['index'],
        'group_index': group['index'],
        'group_id': group['id'],
        'size': id_parts[2].lower(),
        'size_id': id_parts[2][0].upper(),
        'id': trial['id'],
        'duty_cycle': 0.01 * int(id_parts[-1]),
        'print_interval': int(id_parts[5].replace('m', '-')),
        'phase': int(id_parts[1])
    })

    trial_data = reader.read('trial', trial['id'], results_path)
    couplings[trial['id']] = trial_data['couplings']

trial_info = pd.DataFrame(trial_info)

shared.put(
    results=results,
    trial_info=trial_info,
    couplings=couplings
)
