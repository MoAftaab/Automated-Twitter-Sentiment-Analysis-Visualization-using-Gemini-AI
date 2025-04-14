from twikit import Client
from configparser import ConfigParser
import asyncio  # Add this import

# Create an async main function for authentication
async def authenticate():
    #* login credentials
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    #* authenticate to X.com
    client = Client(language='en-US')
    # Use await here for the async login method
    await client.login(auth_info_1=username, auth_info_2=email, password=password)
    client.save_cookies('cookies.json')
    print("Login successful and cookies saved!")

# Run the async authentication function
if __name__ == "__main__":
    asyncio.run(authenticate())