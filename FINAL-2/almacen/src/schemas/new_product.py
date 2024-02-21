new_product = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'quantity': {'type': 'integer'}
    },
    'required': [
        'name', 'description', 'quantity'
    ]
}
