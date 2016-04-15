import pandas as pd

from tracksim import analysis
from tracksim import gather

analysis.initialize_path()
results = gather.group_results()

couplings = []
trial_info = []

for item in results['trials']:
    group = item['group']
    trial = item['trial']
    id_parts = trial['id'].split('-')

    trial_info.append({
        'index': item['index'],
        'trial_index': item['trial_index'],
        'group_index': item['group_index'],
        'group_id': group['id'],
        'size': id_parts[2].lower(),
        'size_id': id_parts[2][0].upper(),
        'id': trial['id'],
        'duty_cycle': 0.01 * int(id_parts[-1]),
        'print_interval': int(id_parts[5].replace('m', '-')),
        'phase': int(id_parts[1])
    })

    bounds = group['couplings']['bounds'][item['trial_index']]
    couplings.append({
        'value': group['couplings']['values'][item['trial_index']],
        'lower_1s': bounds['one_sigma'][0],
        'upper_1s': bounds['one_sigma'][1],
        'lower_2s': bounds['two_sigma'][0],
        'upper_2s': bounds['two_sigma'][1]
    })


trial_info = pd.DataFrame(trial_info)
couplings = pd.concat([pd.DataFrame(couplings), trial_info], axis=1)

analysis.cacher.put(
    results=results,
    trial_info=trial_info,
    couplings=couplings
)


