from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import get_all_posts, get_single_post, create_post, get_user_posts, update_post, delete_post, filter_by_category, search_posts_by_title
from views.user import create_user, login_user
from views import get_all_tags, get_single_tag, create_tag
from views.categories import add_category, get_all_categories, get_single_category
from views.categories import delete_category
from views import get_all_users, get_single_user
from views import create_subscription

class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url()

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"

            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"

            elif resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"

        elif len(parsed) == 3:
            ( resource, key, value ) = parsed
            
            if key == "user" and resource == "posts":
                response = get_user_posts(value)
                
            if key == "category" and resource == "posts":
                response = filter_by_category(value)
            
            if key == "title" and resource == "posts":
                response = search_posts_by_title(value)


        self.wfile.write(response.encode())


    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == "posts":
            response = create_post(post_body)
        if resource == "tags":
            response = create_tag(post_body)
        if resource == "categories":
            response = add_category(post_body)
        if resource == "subcriptions":
            response = create_subscription(post_body)

        self.wfile.write(f"{response}".encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url()

        success = False
        
        if resource == "posts":
            success = update_post(id, post_body)
        
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
            
        self.wfile.write("".encode())
            

    def do_DELETE(self):
        self._set_headers(204)
        
        (resource, id) = self.parse_url()
        
        if resource == "posts":
            delete_post(id)
        elif resource == "categories":
            delete_category(id)
        
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
