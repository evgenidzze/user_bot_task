from pyrogram import Client
from pyrogram.errors import FloodWait
from time import sleep
import random
import requests

app = Client("me")


# Function to send messages to a user base
def send_message_to_users(user_list, message):
    for user in user_list:
        try:
            app.send_message(user, message)
            print(f"Message sent to user {user}")
            # Sleep for random time to avoid flooding
            sleep(random.randint(1, 5))
        except FloodWait as e:
            # Handle flood wait exception
            print(f"Flood wait of {e.x} seconds")
            sleep(e.x)
        except Exception as e:
            # Handle other exceptions
            print(f"Error sending message to user {user}: {str(e)}")


# Function to generate HTML report
def generate_html_report(successful_users, failed_users):
    # Generate HTML code for the report
    html = "<html><head><title>Report</title></head><body>"
    html += f"<h2>Successful Users ({len(successful_users)})</h2>"
    html += "<ul>"
    for user in successful_users:
        html += f"<li>{user}</li>"
    html += "</ul>"
    html += f"<h2>Failed Users ({len(failed_users)})</h2>"
    html += "<ul>"
    for user in failed_users:
        html += f"<li>{user}</li>"
    html += "</ul>"
    html += "</body></html>"
    return html


# Main function to send messages and generate report
def send_messages_and_generate_report(user_list, message):
    app.start()
    successful_users = []
    failed_users = []
    total_users = len(user_list)
    i = 0
    while i < total_users:
        # Send messages to 1000 users in one session
        users_batch = user_list[i:i + 1000]
        try:
            send_message_to_users(users_batch, message)
            successful_users += users_batch
        except Exception as e:
            # Handle exceptions
            print(f"Error sending messages to batch {i}: {str(e)}")
            failed_users += users_batch
        i += 1000
    # Generate HTML report
    html_report = generate_html_report(successful_users, failed_users)
    # Save HTML report to a file
    with open("report.html", "w") as f:
        f.write(html_report)
    # Upload HTML report to a web server
    url = "https://example.com/upload"
    files = {'file': ('report.html', open('report.html', 'rb'), 'text/html')}
    response = requests.post(url, files=files)
    print("HTML report uploaded to web server")
    app.stop()


# Call the main function to send messages and generate report
user_list = []  # List of user IDs
message = "Hello, this is a test message"
send_messages_and_generate_report(user_list, message)
