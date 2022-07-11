CREATE_NOTIFICATION_SETTING_QUERY = '''
    INSERT INTO notification_settings (plant_id,  service_type, api_url, access_token, access_secret, consumer_key, consumer_secret, enabled)
    VALUES (:plant_id, :service_type, :api_url, :access_token, :access_secret, :consumer_key, :consumer_secret, :enabled)
    RETURNING id, plant_id, service_type, api_url, access_token, access_secret, consumer_key, consumer_secret, enabled, created_at, updated_at;
'''
GET_NOTIFICATION_SETTING_BY_ID_QUERY = '''
    SELECT id, plant_id, service_type, api_url, access_token, access_secret, consumer_key, consumer_secret, enabled, created_at, updated_at
    FROM notification_settings
    WHERE id = :id;
'''
GET_NOTIFICATION_SETTING_BY_PLANT_ID_AND_SERVICE_TYPE_QUERY = '''
    SELECT id, plant_id, service_type, api_url, access_token, access_secret, consumer_key, consumer_secret, enabled, created_at, updated_at
    FROM notification_settings
    WHERE plant_id = :plant_id, service_type = :service_type;
'''
GET_ALL_NOTIFICATION_SETTINGS_QUERY = '''
    SELECT id, plant_id, service_type, api_url, access_token, access_secret, consumer_key, consumer_secret, enabled, created_at, updated_at
    FROM notification_settings
    ORDER BY created_at desc;
'''
GET_ALL_NOTIFICATION_SETTINGS_QUERY_BY_PLANT_ID = '''
    SELECT id, plant_id, service_type, api_url, access_token, access_secret, consumer_key, consumer_secret, enabled, created_at, updated_at
    FROM notification_settings
    WHERE plant_id = :plant_id
    ORDER BY created_at desc;
'''
DELETE_NOTIFICATION_SETTING_BY_ID_QUERY = '''
    DELETE FROM notification_settings
    WHERE id = :id
    RETURNING id;
'''