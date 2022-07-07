CREATE_PUMP_SETTING_LOG_QUERY = '''
    INSERT INTO pump_settings (plant_id, lower_limit_moist, upper_limit_moist)
    VALUES (:plant_id, :lower_limit_moist, :upper_limit_moist)
    RETURNING id, plant_id, lower_limit_moist, upper_limit_moist, created_at, updated_at;
'''
GET_PUMP_SETTING_LOG_BY_QUERY = '''
    SELECT id, plant_id, lower_limit_moist, upper_limit_moist, created_at, updated_at
    FROM pump_settings
    WHERE id = :id;
'''
GET_ALL_PUMP_SETTING_LOGS_QUERY = '''
    SELECT id, plant_id, lower_limit_moist, upper_limit_moist, created_at, updated_at
    FROM pump_settings;
'''
DELETE_PUMP_SETTING_LOG_BY_ID_QUERY = '''
    DELETE FROM pump_settings
    WHERE id = :id
    RETURNING id;
'''