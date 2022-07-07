CREATE_SNAPSHOT_QUERY = '''
    INSERT INTO snapshots (plant_id, image_file)
    VALUES (:plant_id, :image_file)
    RETURNING id, plant_id, image_file, created_at, updated_at;
'''
GET_SNAPSHOT_BY_QUERY = '''
    SELECT id, plant_id, image_file, created_at, updated_at
    FROM snapshots
    WHERE id = :id;
'''
GET_ALL_SNAPSHOTS_QUERY = '''
    SELECT id, plant_id, image_file, created_at, updated_at
    FROM snapshots;
'''
DELETE_SNAPSHOT_BY_ID_QUERY = '''
    DELETE FROM snapshots
    WHERE id = :id
    RETURNING id;
'''