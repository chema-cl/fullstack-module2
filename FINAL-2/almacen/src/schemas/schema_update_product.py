update_product = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'quantity': {'type': 'integer', 'minimun': 1},
        "available": {'type': 'boolean'}
    },
    'required': [
        'name', 'description', 'quantity', 'available'
    ]
}
