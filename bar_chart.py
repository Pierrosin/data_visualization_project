import plotly.express as px

def draw_bar_chart(data, arrond, criterion):
    # On modifie le nom du critère pour le titre
    if criterion == 'Rue':
        pretty_criterion = 'Rues'
    elif criterion == 'Emplacement':
        pretty_criterion = 'Emplacements'
    elif criterion == 'Essence_fr':
        pretty_criterion = 'Espèces'
    
    # On adapte le titre si c'est la carte de l'arrondissement ou de la ville
    if arrond:
        data = data[data['ARROND_NOM'] == arrond]
        title = f"<b>Top 10 {pretty_criterion.lower()} de l'arrondissement {arrond}</b>"
        if len(title) > 65:
            title = f"<b>Top 10 {pretty_criterion.lower()} de l'arrondissement<br>{arrond}</b>"    
    else:
        title = f"<b>Top 10 {pretty_criterion.lower()} de la Ville de Montréal</b>"
    
    # On compte le nombre d'arbres pour chaque catégorie du critère    
    tree_counts = data.groupby(criterion).size().reset_index(name='Count')
    
    # On trie et on garde le top 10
    top_10_tree_counts = tree_counts.sort_values(by='Count').tail(10)

    # Création du bar chart
    fig = px.bar(top_10_tree_counts,
                x='Count',
                y=criterion,
                orientation='h',
                color_discrete_sequence=['#36749d'],
                )

    # Mise en page du bar chart
    fig.update_layout(
        title=title,
        title_x=0.5,
        title_y=0.96,
        xaxis=dict(title="Nombre d'arbres", showline=False, linecolor='black'),
        yaxis=dict(title="", showline=False, linecolor='black'),
        showlegend=False,
        dragmode=False
    )
    
    # Ajout des hovers
    fig.update_traces(hovertemplate='%{x}')

    return fig