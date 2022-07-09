CREATE_MOIST_LOG_QUERY = '''
    INSERT INTO moist_logs (plant_id, moist)
    VALUES (:plant_id, :moist)
    RETURNING id, plant_id, moist, created_at, updated_at;
'''
GET_MOIST_LOG_BY_ID_QUERY = '''
    SELECT id, plant_id, moist, created_at, updated_at
    FROM moist_logs
    WHERE id = :id;
'''
GET_ALL_MOIST_LOGS_QUERY = '''
    SELECT id, plant_id, moist, created_at, updated_at
    FROM moist_logs
    ORDER BY created_at desc;
'''
GET_ALL_MOIST_LOGS_QUERY_BY_PLANT_ID = '''
    SELECT id, plant_id, moist, created_at, updated_at
    FROM moist_logs
    WHERE plant_id = :plant_id
    ORDER BY created_at desc;
'''
DELETE_MOIST_LOG_BY_ID_QUERY = '''
    DELETE FROM moist_logs
    WHERE id = :id
    RETURNING id;
'''