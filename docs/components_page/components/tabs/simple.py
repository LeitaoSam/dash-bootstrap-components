import dash_bootstrap_components as dbc

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardText("This is tab 1!"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardText("This is tab 2!"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(
            "This tab's content is never seen", label="Tab 3", disabled=True
        ),
    ]
)
