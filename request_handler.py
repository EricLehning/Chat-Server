import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import os
import openai

# For potential Cors Issues
import copy
import json
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define the proxy URL
proxy_url = "http://localhost:8088"

# Create a ProxyHandler object with the proxy URL
proxy_handler = urllib.request.ProxyHandler({"http": proxy_url})

# Create an opener object with the proxy handler
opener = urllib.request.build_opener(proxy_handler)

# Install the opener object as the default global opener
urllib.request.install_opener(opener)

# Rest of the code


openai.api_key = os.getenv("OPENAI_API_KEY")


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.

    # def do_GET(self):
    # """Doc string
    # """

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Doc string"""
        self._set_headers(200)
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)
        # What are the requirements on how we pass bodies to 3rd party api?
        if resource == "chat":
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=post_body
            )

        result = ""
        # for choice in response.choices:
        #     result += choice.message.content

        self.wfile.write(json.dumps(result).encode())

        # Encode the new animal and send in response

    # A method that handles any PUT request.
    # def do_PUT(self):
    #     """Doc string
    #     """

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    def parse_url(self, path):
        """Doc string"""
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    # def do_DELETE(self):
    #     """Doc string
    #     """


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
