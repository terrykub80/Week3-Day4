class Blog:
    def __init__(self):
        self.users = set()
        self.posts = list()
        self.current_user = None # attribute used to determine if ther is a logged in user

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
    pass







# Define a function to run the blog
def run_blog():
    # Create an instance of the blog class
    my_blog = Blog()
    # Keep looping while the blog is 'running'
    while True:
        # if there is no current user logged in
        if my_blog.current_user is None:
            # Pring menu options
            print("1. Sign Up\n2. Log In\n3. View All Posts\n4. View Single Post\n5. Quit")
            # Ask which option they want to do
            to_do = input("Which option would you like to do? ")
            # Keep asking if user chooses invalid option
            if to_do not in {'1', '2', '5'}:
                to_do = input("Invalid option. Please choose 1, 2, 3, 4, or 5: ")
            if to_do == '5':
                print("Thanks for stopping by!")
                break
            elif to_do == '1':
                # method to create new user
                my_blog.create_new_user()
            elif to_do == '2':
                # method to log user in
                my_blog.log_user_in()
        # if the current user is not "none" (aka a user is not logged in)
        else:
            # Print options for logged in user
            print("Quit")
            to_do = input("Which option would you like to choose? ")
            if to_do.lower() == 'quit':
                break



run_blog()
