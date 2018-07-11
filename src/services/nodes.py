import pandas as pd

def get_nodes():
    '''Used to retreive the node list stored in a .csv file.

        Returns: nodes (a list of nodes, each one contains a dict with
        info about the node).
    '''

    df=pd.read_csv('./data/nodelist.csv')
    nodes = []
    for row in range(0,df.shape[0]): # get number of rows
        nodes.append(dict(ip=df.at[row,'ip'],
            wallet=df.at[row,'wallet']))
    return nodes

