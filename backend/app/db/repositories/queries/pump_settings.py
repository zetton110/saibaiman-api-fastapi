CREATE_PUMP_SETTING_LOG_QUERY = '''
    INSERT INTO pump_settings (plant_id, need_pump, complete_pump)
    VALUES (:plant_id, :need_pump, :complete_pump)
    RETURNING id, plant_id, need_pump, complete_pump, created_at, updated_at;
'''
GET_PUMP_SETTING_LOG_BY_QUERY = '''
    SELECT id, plant_id, need_pump, complete_pump, created_at, updated_at
    FROM pump_settings
    WHERE id = :id;
'''
GET_ALL_PUMP_SETTING_LOGS_QUERY = '''
    SELECT id, plant_id, need_pump, complete_pump, created_at, updated_at
    FROM pump_settings;
'''
DELETE_PUMP_SETTING_LOG_BY_ID_QUERY = '''
    DELETE FROM pump_settings
    WHERE id = :id
    RETURNING id;
'''