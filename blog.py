class Blog:
    def __init__(self):
        self.users = set()
        self.posts = list()
        self.current_user = None # attribute used to determine if ther is a logged in user

    # Private method for getting a post instance from the blog based on it ID, 
    # returns Non if the post with ID does not exhist
    
    def _get_post_from_id(self, post_id):
        for post in self.posts:
            if post.id == int(post_id):
                return post
        return None
            

    # Method to add new user to the blog
    def create_new_user(self):
        # get user info from input
        username = input("Please enter a username: ")
        # Check if there is a user by that name already
        if username in {u.username for u in self.users}:
            print(f"That username, {username}, already exists")
        else:
            # Get password
            password = input("Please enter a password: ")
            # Create a new user instance with info from inputs
            new_user = User(username, password)
            # add new user instance to the blog user set
            self.users.add(new_user)
            print(f"{new_user} has been created.")

    # method to log user in
    def log_user_in(self):
        # Get user credentials
        username = input("What is your username? ")
        password = input("What is your password? ")
        # Loop through each user in blog
        for user in self.users:
            # Check if a user has the same username and then check the password
            if user.username == username and user.check_password(password):
                # If user has good creds, set the blog's current user to that user instance
                self.current_user = user
                print(f"{user} has been logged in.")
                break
        #if no users in blog user set have that name/password, alert invalid creds
        else:
            print("Username and/or passowrd is incorrect.")

    
    #m Method to log user out
    def log_user_out(self):
        # Change current_user attribute on this instance to none
        self.current_user = None
        print("You have successfully logged out.")

    # Method to create a new post if a user is logged in
    def create_post(self):
        # Check to make sure user is logged in before creating
        if self.current_user is not None:
            # Get the title and body from user input
            title = input("Enter the title of your post: ")
            body = input("Enter the body of your post: ")
            # Create a new post
            new_post = Post(title, body, self.current_user)
            # Add new post instance to our blog's list of posts
            self.posts.append(new_post)
            print(f"{new_post.title} has been created!")
        else:
            print("You must be logged in to perform this action.")

    # Method to view ALL posts
    def view_posts(self):
        # Check to see if there any posts
        if self.posts:
            # Loop through all of the posts
            for post in self.posts:
                # Display the post
                print(post)
        # If no posts
        else:
            print("There are currently no posts for this blog :(")

    # Method to view a single post by its ID
    def view_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:
            print(post)
        else:
            print(f"Post with an ID of {post_id} does not exist.")

    # Method to edit a single post
    def edit_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:
            # Check that the user is logged in AND that the logged in user is the owner of this post
            if self.current_user is not None and self.current_user == post.author:
                print(post)
                # Ask the user which part of the post they would like to edit
                edit_part = input("Would you like to edit the Title, Body, Both, or Exit? ").lower()
                # Make sure the user response is valid
                while edit_part not in {'title', 'body', 'both', 'exit'}:
                    edit_part = input("Invalid. Please choose Title, Body, Both, or Exit: ").lower()
                # if the user puts exit, exit the function
                if edit_part == 'exit':
                    return
                elif edit_part == 'both':
                    # Get a new title and body
                    new_title = input('Enter the new title: ').title()
                    new_body = input('Enter the new body: ')
                    # Edit the post with the post.update method
                    post.update(title=new_title, body=new_body)
                elif edit_part == 'title':
                     # Get a new title
                    new_title = input('Enter the new title: ').title()
                    post.update(title=new_title)
                elif edit_part == 'body':
                    # Get a new body
                    new_body = input('Enter the new body: ')
                    post.update(body=new_body)
                print(f"{post.title} has been updated")

            # If the user is logged in but not the owner of the post
            elif self.current_user is not None and self.current_user != post.author:
                print("You do not have permission to edit this post") # 403 HTTP Status Code (we know you but you can't do that)
            # If the user is not logged in
            else:
                print("You must be logged in to perform this action") # 401 HTTP Status Code (we don't know who you ar)
        else:
            print(f"Post with an ID of {post_id} does not exist") # 404 HTTP Status Code (this just doesn't exist)


    # Method to delete a single post by its ID
    def delete_post(self, post_id):
        # Get the post by id or return None
        post = self._get_post_from_id(post_id)
        # If Post Object
        if post:
            # Check that the user is logged in AND that the logged in user is the owner of this post
            if self.current_user is not None and self.current_user == post.author:
                # Remove the post from the blog's list of posts
                self.posts.remove(post)
                print(f"{post.title} has been deleted")
            # If the user is logged in but not the owner of the post
            elif self.current_user is not None and self.current_user != post.author:
                print("You do not have permission to delete this post") # 403 HTTP Status Code
            # If the user is not logged in
            else:
                print("You must be logged in to perform this action") # 401 HTTP Status Code
        else:
            print(f"Post with an ID of {post_id} does not exist") # 404










class User:
    id_counter = 1 # Class attribute keeping track of User IDs

    def __init__(self, username, password):
        self.username = username
        self.password = password[::-2] # stores the password as every other letter from back to front = "dosalorps"
        self.id = User.id_counter
        User.id_counter += 2

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"

    def check_password(self, password_guess):
        return self.password == password_guess[::-2]

    

class Post:
    id_counter = 1

    def __init__(self, title, body, author):
        """
        title: str
        body: str
        author: User
        """
        self.title = title
        self.body = body
        self.author = author
        self.id = Post.id_counter
        Post.id_counter += 1

    def __str__(self):
        formatted_post = f"""
        {self.id} - {self.title.title()}
        By: {self.author}
        {self.body}
        """
        return formatted_post

    def __rpr__(self):
        return f"<Post|{self.id}|{self.title}>"

    # Define method to update posts
    def update(self, **kwargs): # **kwargs means 2 strings
        for key, value in kwargs.items():
            setattr(self, key, value)

# Define a function to run the blog
def run_blog():
    # Create an instance of the blog class
    my_blog = Blog()

    # Add pre-loaded data for the Blog
    initial_user = User('brians', 'abc123')
    my_blog.users.add(initial_user)
    initial_post = Post('Pre-Loaded', 'This post was preloaded', initial_user)
    my_blog.posts.append(initial_post)
    # Keep looping while the blog is 'running'
    while True:
        # if there is no current user logged in
        if my_blog.current_user is None:
            # Pring menu options
            print("1. Sign Up\n2. Log In\n3. View All Posts\n4. View Single Post\n5. Quit")
            # Ask which option they want to do
            to_do = input("Which option would you like to do? ")
            # Keep asking if user chooses invalid option
            if to_do not in {'1', '2', '3', '4', '5'}:
                to_do = input("Invalid option. Please choose 1, 2, 3, 4 or 5: ")
            if to_do == '5':
                print("Thanks for stopping by!")
                break
            elif to_do == '1':
                # method to create new user
                my_blog.create_new_user()
            elif to_do == '2':
                # method to log user in
                my_blog.log_user_in()
            elif to_do == '3':
                #method to vew ALL posts
                my_blog.view_posts()
            elif to_do == '4':
                # Get the id of the post from the user
                post_id = input("What is the ID of the post you would like to view? ")
                # Call the view single post method
                my_blog.view_post(post_id)
        # if the current user is not "none" (aka a user is not logged in)
        else:
            # Print options for logged in user
            print("1. Log Out\n2. Create New Post\n3. View All Posts\n4. View Single Post\n5. Edit Post\n6. Delete Post")
            to_do = input("Which option would you like to choose? ")
            while to_do not in {'1', '2', '3', '4', '5', '6'}:
                to_do = input("Invalid option. Please choose 1, 2, 3, 4, 5 or 6: ")
            if to_do == '1':
                my_blog.log_user_out()
            elif to_do == '2':
                my_blog.create_post()
            elif to_do == '3':
                #method to vew ALL posts
                my_blog.view_posts()
            elif to_do == '4':
                # Get the id of the post from the user
                post_id = input("What is the ID of the post you would like to view? ")
                # Call the view single post method
                my_blog.view_post(post_id)
            elif to_do == '5':
                # Get the id of the post the user wants to edit
                post_id = input("What is the ID of the post you would like to edit? ")
                # Call edit post method with post id as argument
                my_blog.edit_post(post_id)
            elif to_do == '6':
                # Get the id of the post the user wants to delete
                post_id = input("What is the ID of the post you would like to delete? ")
                # Call edit post method with post id as argument
                my_blog.delete_post(post_id)




# Execute the run_blog function
run_blog()
