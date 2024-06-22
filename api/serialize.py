def serializeDict(a):
    # Asegura que el '_id' se convierte en string si existe y es un ObjectId
    if "_id" in a:
        a['_id'] = str(a['_id'])
    return a

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

