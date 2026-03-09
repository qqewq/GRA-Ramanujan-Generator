import csv
import os

def init_logs():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/conjectures.csv'):
        with open('data/conjectures.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['generation','machine_id','constant','formula_id',
                             'accuracy','complexity','beauty','expression'])
    if not os.path.exists('data/machines.csv'):
        with open('data/machines.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['generation','machine_id','mean_beauty','best_beauty','vitality'])

def log_conjecture(generation, machine_id, formula):
    with open('data/conjectures.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            generation,
            machine_id,
            formula['constant'],
            f"{formula['constant']}_{generation}_{machine_id}",
            formula.get('accuracy',0),
            formula.get('complexity',0),
            formula.get('beauty',0),
            str(formula['tree'])
        ])

def log_machine(generation, machine):
    mean_beauty = 0.0
    best_beauty = 0.0
    vals = [f['beauty'] for f in machine.best_formulas.values() if f]
    if vals:
        mean_beauty = sum(vals)/len(vals)
        best_beauty = max(vals)
    with open('data/machines.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([generation, machine.id, mean_beauty, best_beauty, machine.vitality])