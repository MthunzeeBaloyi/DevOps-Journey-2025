from src.optimizer import summarize_costs

def test_summarize_by_service():
    records = [
        {'service': 'EC2', 'cost': 10},
        {'service': 'S3', 'cost': 2},
        {'service': 'EC2', 'cost': 5},
        {'service': 'Lambda', 'cost': 1}
    ]
    top = summarize_costs(records, key='service', top_n=2)
    assert top[0][0] == 'EC2' and top[0][1] == 15
    assert top[1][0] == 'S3' and top[1][1] == 2

def test_handle_missing_costs():
    records = [{'service': 'S3'}, {'service':'S3','cost': None}, {'service':'EC2','cost':'3.5'}]
    top = summarize_costs(records, key='service', top_n=2)
    assert any(k == 'S3' for k,_ in top)

def test_summarize_by_tag_env():
    records = [
        {'resource_id': 'i-1', 'service': 'EC2', 'cost': 10, 'tags': {'env': 'prod'}},
        {'resource_id': 'i-2', 'service': 'EC2', 'cost': 5, 'tags': {'env': 'staging'}},
        {'resource_id': 'i-3', 'service': 'S3', 'cost': 2, 'tags': {'env': 'prod'}},
        {'resource_id': 'i-4', 'service': 'Lambda', 'cost': 1}
    ]
    top = summarize_costs(records, key='tags.env', top_n=2)
    # prod should be top with 12
    assert top[0][0] == 'prod' and abs(top[0][1] - 12.0) < 1e-6
