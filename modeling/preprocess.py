import pickle
from sklearn.preprocessing import LabelEncoder

def preprocess_for_tabnet(df, train=True):
    categorical_columns = []
    categorical_dims =  {}
    if train:
        l_encs = {}
    else:
        l_encs = pickle.load(open('encoders.p','rb'))
    for col in df.columns[df.dtypes == object]:
        df[col] = df[col].fillna("VV_likely")
        if train:
            l_enc = LabelEncoder()
            df[col] = l_enc.fit_transform(df[col].values)
            l_encs[col] = l_enc
        else:
            print(col)
            l_enc = l_encs[col]
            df[col] = l_enc.transform(df[col].values)
        categorical_columns.append(col)
        categorical_dims[col] = len(l_enc.classes_)
    if train:
        pickle.dump(l_encs, open('encoders.p','wb'))

    if train:
        x = df.drop(['RATING', 'TIMESTAMP'], axis=1)
        y = df[['RATING']]
        features = [ col for col in x.columns]
        pickle.dump(features, open('schema.p','wb'))
    else:
        x = df.drop(['TIMESTAMP'], axis=1)
        features = pickle.load(open('schema.p','rb'))
        x = x[features]
        y = None
    
    return x, y, categorical_columns, categorical_dims
    