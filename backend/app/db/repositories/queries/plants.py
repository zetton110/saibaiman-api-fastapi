CREATE_PLANT_QUERY = '''
    INSERT INTO plants (name, fullname, plant_type, description)
    VALUES (:name, :fullname, :plant_type, :description)
    RETURNING id, name, fullname, plant_type, description, created_at, updated_at;
'''
GET_PLANT_BY_QUERY = '''
    SELECT id, name, fullname, plant_type, description, created_at, updated_at
    FROM plants
    WHERE id = :id;
'''
GET_ALL_PLANTS_QUERY = '''
    SELECT id, name, fullname, plant_type, description, created_at, updated_at
    FROM plants;
'''
UPDATE_PLANT_BY_ID_QUERY = '''
    UPDATE plants
    SET name        = :name,
        fullname    = :fullname,
        plant_type  = :plant_type,
        description = :description
    WHERE id = :id
    RETURNING id, name, fullname, plant_type, description, created_at, updated_at;
'''
DELETE_PLANT_BY_ID_QUERY = '''
    DELETE FROM plants
    WHERE id = :id
    RETURNING id;
'''