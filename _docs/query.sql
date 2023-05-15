SELECT jsonb_array_elements(task_properties_definition) AS dict
FROM project_project
WHERE task_properties_definition @> '[{"key": "value"}]'
