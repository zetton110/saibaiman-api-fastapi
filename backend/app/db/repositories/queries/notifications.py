CREATE_NOTIFICATION_QUERY = '''
    INSERT INTO notifications (plant_id, service_type, message, notified_to_service)
    VALUES (:plant_id, :service_type, :message, :notified_to_service)
    RETURNING id, plant_id, service_type, message, notified_to_service, created_at, updated_at;
'''
GET_NOTIFICATION_BY_ID_QUERY = '''
    SELECT plant_id, service_type, message, notified_to_service
    FROM notifications
    WHERE id = :id;
'''
GET_ALL_NOTIFICATIONS_QUERY = '''
    SELECT id, plant_id, service_type, message, notified_to_service, created_at, updated_at
    FROM notifications
    ORDER BY created_at desc;
'''
GET_ALL_NOTIFICATIONS_QUERY_BY_PLANT_ID = '''
    SELECT id, plant_id, service_type, message, notified_to_service, created_at, updated_at
    FROM notifications
    WHERE plant_id = :plant_id
    ORDER BY created_at desc;
'''
DELETE_NOTIFICATION_BY_ID_QUERY = '''
    DELETE FROM notifications
    WHERE id = :id
    RETURNING id;
'''