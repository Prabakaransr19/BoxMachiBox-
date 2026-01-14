from pathlib import Path
import pickle
import pandas as pd
from pprint import pprint

ROOT = Path(__file__).parent
mp = pickle.load(open(ROOT / 'my_f1_model_FINAL_OPTIMIZED.pkl','rb'))
print('keys:', list(mp.keys()))
print('models type:', type(mp['models']))
# print models info
try:
    for i, (name, model, weight) in enumerate(mp['models']):
        print(i, name, type(model), weight)
except Exception as e:
    print('models structure:', mp['models'][:3])

print('weights:', mp.get('weights'))
print('threshold:', mp.get('threshold'))
print('categorical cols:', mp.get('categorical_cols')[:10])
print('num features:', len(mp.get('features',[])))

# Try a sample driver
drivers = pickle.load(open(ROOT / '2025_final_standings.pkl','rb'))
print('drivers columns:', drivers.columns.tolist()[:20])
driver = drivers.iloc[0].to_dict()
driver['grid_position'] = 5
# Build feature dict similar to app
feat = {}
for f in mp['features']:
    feat[f] = driver.get(f, 0)
# encode cats
for col in mp.get('categorical_cols',[]):
    if col in feat:
        le = mp['label_encoders'].get(col)
        if le:
            try:
                feat[col] = le.transform([str(feat[col])])[0]
            except Exception as e:
                feat[col] = -1

X_pred = pd.DataFrame([feat])[mp['features']]
print('X_pred shape:', X_pred.shape)
# compute probas
probas = []
for name, model, weight in mp['models']:
    p = model.predict_proba(X_pred)[:,1][0]
    probas.append(p)
print('probas', probas)
print('final proba', sum(p* w for p,w in zip(probas, mp['weights'])) / sum(mp['weights']))
