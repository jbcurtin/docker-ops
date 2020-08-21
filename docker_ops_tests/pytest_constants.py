import os
import uuid

TESTING_DIR = f'/tmp/docker-ops-testing/{uuid.uuid4()}'
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TESTING_TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'docker_ops_test_templates')
