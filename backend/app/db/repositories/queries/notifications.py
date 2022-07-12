CREATE_NOTIFICATION_QUERY = '''
    INSERT INTO notifications (plant_id, service_type, message, notified_to_service, snapshot_id)
    VALUES (:plant_id, :service_type, :message, :notified_to_service, :snapshot_id)
    RETURNING id, plant_id, service_type, message, notified_to_service, snapshot_id, created_at, updated_at;
'''
GET_NOTIFICATION_BY_ID_QUERY = '''
    SELECT id, plant_id, service_type, message, notified_to_service, snapshot_id, created_at, updated_at
    FROM notifications
    WHERE id = :id;
'''
GET_LATEST_NOTIFICATION_BY_PLANT_ID_AND_SERVICE_TYPE_QUERY = '''
    SELECT id, plant_id, service_type, message, notified_to_service, snapshot_id, created_at, updated_at
    FROM notifications
    WHERE plant_id = :plant_id and service_type = :service_type
    ORDER BY created_at desc limit 1;
'''
GET_ALL_NOTIFICATIONS_QUERY = '''
    SELECT id, plant_id, service_type, message, notified_to_service, snapshot_id, created_at, updated_at
    FROM notifications
    ORDER BY created_at desc;
'''
GET_ALL_NOTIFICATIONS_QUERY_BY_PLANT_ID = '''
    SELECT id, plant_id, service_type, message, notified_to_service, snapshot_id, created_at, updated_at
    FROM notifications
    WHERE plant_id = :plant_id
    ORDER BY created_at desc;
'''
DELETE_NOTIFICATION_BY_ID_QUERY = '''
    DELETE FROM notifications
    WHERE id = :id
    RETURNING id;
'''
UPDATE_NOTIFICATION_BY_ID = '''
    UPDATE notifications
    SET plant_id            = :plant_id,
        service_type        = :service_type,
        message             = :message,
        notified_to_service = :notified_to_service
    WHERE id = :id
    RETURNING id, plant_id, service_type, message, notified_to_service, created_at, updated_at;
'''