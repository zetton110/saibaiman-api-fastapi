CREATE_PUMP_LOG_QUERY = '''
    INSERT INTO pump_logs (plant_id)
    VALUES (:plant_id)
    RETURNING id, plant_id, created_at, updated_at;
'''
GET_PUMP_LOG_BY_ID_QUERY = '''
    SELECT id, plant_id, created_at, updated_at
    FROM pump_logs
    WHERE id = :id;
'''
GET_ALL_PUMP_LOGS_QUERY = '''
    SELECT id, plant_id, created_at, updated_at
    FROM pump_logs
    ORDER BY created_at desc;
'''
GET_ALL_PUMP_LOGS_BY_PLANT_ID_QUERY = '''
    SELECT id, plant_id, created_at, updated_at
    FROM pump_logs
    WHERE plant_id = :plant_id
    ORDER BY created_at desc;
'''
DELETE_PUMP_LOG_BY_ID_QUERY = '''
    DELETE FROM pump_logs
    WHERE id = :id
    RETURNING id;
'''