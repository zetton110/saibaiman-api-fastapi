CREATE_MOIST_LOG_QUERY = '''
    INSERT INTO moist_logs (plant_id, moist)
    VALUES (:plant_id, :moist)
    RETURNING id, plant_id, moist, created_at, updated_at;
'''
GET_MOIST_LOG_BY_QUERY = '''
    SELECT id, plant_id, moist, created_at, updated_at
    FROM moist_logs
    WHERE id = :id;
'''
GET_ALL_MOIST_LOGS_QUERY = '''
    SELECT id, plant_id, moist, created_at, updated_at
    FROM moist_logs;
'''
DELETE_MOIST_LOG_BY_ID_QUERY = '''
    DELETE FROM moist_logs
    WHERE id = :id
    RETURNING id;
'''