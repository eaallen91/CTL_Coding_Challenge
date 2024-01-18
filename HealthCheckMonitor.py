import sys
import requests

# Set urls for healthcheck endpoints
healthcheck_url = 'https://u3mpbqz6ki.execute-api.us-east-1.amazonaws.com/prod/healthcheck'
todo_url = 'https://u3mpbqz6ki.execute-api.us-east-1.amazonaws.com/prod/todo'

# Exit codes:
warning = 1
error = 2

# Query the todo_url and check the response
# Checks needed:
#  1) Check the URL returned a response. NULL Check
#  2) Check the response status is 200
# If all checks are successful, get_todo will exit with code 0
def get_todo():

    # Set the request body, and post to todo_url
    post_request_body = '{"title": "walk the dog"}'
    response = requests.post(todo_url, post_request_body)

    # Check for 200 status code
    # Any response code other than 200, return error exit code
    if response.status_code != 200:
        sys.exit(error)


# Query the healthcheck url to verify current status
# Checks needed:
#  1) Check the URL returned a response. NULL Check
#  2) Check the response status is 200
#  3) Check the health status is "ok"
# If all checks are successful, continue on to the get_todo function
def check_healthcheck_url():

    # Execute the rest GET to healthcheck_url
    response = requests.get(healthcheck_url)

    # Check for 200 status code
    # if the status code is 400, return warning exit code
    # if the status code is 500, return error exit code
    if response.status_code == 400:
        sys.exit(warning)
    elif response.status_code == 500:
        sys.exit(error)

    # Attempt to extract the response body as long as body is not null
    # If body of response is empty, throw error exit code
    try:
        response_body = response.json()
    except ValueError:
        sys.exit(error)

    # Check the health is "ok", if not throw error exit code
    if response_body['health'] != "ok":
        sys.exit(error)


# Execute the check_healthcheck_url function
# If successful, execute the get_todo function
# If both are successful, script will exit with code 0
if __name__ == '__main__':
    check_healthcheck_url()
    get_todo()
