import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

def analyze_top_clients(orders, clients):
    df = pd.DataFrame([
        {'client_id': o['client_id'], 'order_id': k} 
        for k, o in orders.items()
    ])
    if df.empty:
        return []
    top = df['client_id'].value_counts().head(5).reset_index()
    top.columns = ['client_id', 'count']
    top['name'] = top['client_id'].apply(lambda x: clients.get(str(x), {}).get('name', 'Unknown'))
    return top.to_dict('records')

def analyze_orders_by_date(orders):
    df = pd.DataFrame([
        {'date': o['date'], 'order_id': k} 
        for k, o in orders.items()
    ])
    if df.empty:
        return []
    df['date'] = pd.to_datetime(df['date'])
    daily = df.groupby('date').size().reset_index(name='count')
    return daily.to_dict('records')

def build_client_graph(orders, clients):
    G = nx.Graph()
    for o in orders.values():
        client_id = o['client_id']
        if str(client_id) not in clients:
            continue
        client_city = clients[str(client_id)].get('city', 'Unknown')
        G.add_node(client_id, city=client_city)
        for pid in o.get('product_ids', []):
            G.add_edge(client_id, f'prod_{pid}', relation='bought')
    return G

def plot_top_clients(top_clients):
    if not top_clients:
        return
    names = [c['name'] for c in top_clients]
    counts = [c['count'] for c in top_clients]
    plt.figure(figsize=(8, 4))
    sns.barplot(x=names, y=counts, palette='viridis')
    plt.title('Top 5 Clients by Orders')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_orders_by_date(daily_data):
    if not daily_data:
        return
    df = pd.DataFrame(daily_data)
    df['date'] = pd.to_datetime(df['date'])
    plt.figure(figsize=(8, 4))
    sns.lineplot(x='date', y='count', data=df, marker='o')
    plt.title('Orders Dynamics')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()