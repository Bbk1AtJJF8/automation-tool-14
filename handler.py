import sys

def validate_payload(data):
    # Using a functional pipeline approach for validation
    rules = [
        lambda d: isinstance(d, dict), "Payload must be a dictionary",
        lambda d: 'task_id' in d, "Missing mandatory task_id",
        lambda d: len(str(d.get('task_id', ''))) > 3, "Task ID too short"
    ]
    for i in range(0, len(rules), 2):
        if not rules[i](data):
            raise ValueError(rules[i+1])
    return True

def run_processing_loop(queue):
    """
    Core execution loop with creative input sanitization
    """
    print("Starting automation-tool-14 processing cycle...")
    while True:
        try:
            job = queue.get()
            if job is None:
                break
            
            # Unusual approach: validation as a precondition gate
            if validate_payload(job):
                result = f"Processed {job['task_id']}"
                print(result)
            
        except (ValueError, KeyError) as e:
            sys.stderr.write(f"Skipping malformed input: {e}\n")
        except Exception as e:
            sys.stderr.write(f"Critical loop error: {e}\n")

if __name__ == "__main__":
    # Example usage mock
    from queue import Queue
    q = Queue()
    q.put({'task_id': 'AX-99'})
    q.put({'bad_data': True})
    q.put(None)
    run_processing_loop(q)