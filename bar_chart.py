import plotly.express as px

def draw_bar_chart(data, arrond, criterion, top):
    if criterion == 'Rue':
        pretty_criterion = 'Rues'
    elif criterion == 'Emplacement':
        pretty_criterion = 'Emplacements'
    elif criterion == 'Essence_fr':
        pretty_criterion = 'Espèces'
    
    if arrond:
        data = data[data['ARROND_NOM'] == arrond]
        title = f"<b>Top 10 {pretty_criterion.lower()} de l'arrondissement {arrond}</b>"
        
    else:
        title = f"<b>Top 10 {pretty_criterion.lower()} de la Ville de Montréal</b>"
        
    tree_counts = data.groupby(criterion).size().reset_index(name='Count')
    
    if top:
        top_10_tree_counts = tree_counts.sort_values(by='Count').tail(10)
    else:
        top_10_tree_counts = tree_counts.sort_values(by='Count').head(10)

    fig = px.bar(top_10_tree_counts,
                x='Count',
                y=criterion,
                orientation='h',
                color_discrete_sequence=['#36749d'],
                )

    fig.update_layout(
        title=title,
        title_x=0.5,
        xaxis=dict(title="Nombre d'arbres", showline=True, linecolor='black'),
        yaxis=dict(title=pretty_criterion, showline=True, linecolor='black'),
        showlegend=False
    )
    
    fig.update_traces(hovertemplate='%{x}')

    return fig