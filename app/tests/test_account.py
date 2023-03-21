


async def test_balance_view(test_client):
    response =  await test_client.get('pay/balance/account/1')
    response_json = response.json()
    assert response_json


async def test_balance_change(test_client):
    data = {
        'user_id': 1,
        'summa': 10,
        'method': 'plus'
    }
    response_old_value = await test_client.get('pay/balance/account/1')
    response_json_old_value = response_old_value.json()
    old_balance = response_json_old_value.get('balance')
    response = await test_client.post('/pay/balance/account/change', json=data)
    response_json = response.json()
    new_balance = response_json.get('balance')
    assert new_balance - data['summa'] == old_balance
