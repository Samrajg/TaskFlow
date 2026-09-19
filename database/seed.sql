-- Seed data for development
INSERT INTO users (id, name, email, password_hash)
VALUES ('usr_1', 'Dev User', 'dev@example.com', 'hashed_password_here');

INSERT INTO categories (id, user_id, name, color, icon)
VALUES ('cat_1', 'usr_1', 'Work', '#ff0000', 'briefcase');

INSERT INTO tasks (id, user_id, category_id, title, description, priority, status)
VALUES ('tsk_1', 'usr_1', 'cat_1', 'Setup Project', 'Initialize TaskFlow project foundation', 'HIGH', 'IN_PROGRESS');
