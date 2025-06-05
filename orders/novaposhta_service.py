from novaposhta.client import NovaPoshtaApi
from pc_components_shop import settings


client = NovaPoshtaApi(api_key=settings.NOVA_POSHTA_API_KEY)

def get_city_suggestions(query):
    if not query:
        return []

    response = client.address.search_settlements(city_name=query)
    suggestions = []

    if response['success']:
        for city in response['data'][0]['Addresses']:
            suggestions.append({
                'label': city['Present'],
                'ref': city['DeliveryCity']
            })

    return suggestions

def get_warehouse_suggestions(city_ref, query):
    if not city_ref:
        return []

    response = client.address.get_warehouses(city_ref=city_ref, limit=10000)
    if not response.get("success"):
        return []

    warehouses = response["data"]
    result = [
        {
            "label": w["Description"],
            "ref": w["Ref"]
        }
        for w in warehouses if query.lower() in w["Description"].lower()
    ]
    return result