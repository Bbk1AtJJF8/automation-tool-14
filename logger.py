import logging

# Configure logging settings
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize logger
logger = logging.getLogger(__name__)

def log_error(message):
    logger.error(message)

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def main_loop(data_list):
    for data in data_list:
        if not isinstance(data, dict):
            log_error('Invalid input: Expected dictionary')
            continue
        if 'name' not in data:
            log_warning('Missing name field')
            continue
        log_info(f'Processing: {data['name']}')
        # Simulate processing
        # ... processing logic ...

if __name__ == '__main__':
    sample_data = [{'name': 'Task1'}, {'data': 'Invalid'}, 'String instead of dict']
    main_loop(sample_data)