# TimeTuner

TimeTuner is a Python application that facilitates scheduling appointments using OpenAI's GPT-3.5 model and Google Calendar API. It parses office hours, checks availability, and creates events in the calendar.

## Features

- Parses office hours from a text document.
- Interacts with users to schedule appointments within specified office hours.
- Checks availability on Google Calendar.
- Creates events in Google Calendar if the slot is available.
  
![image](https://github.com/harshithsaiv/TimeTuner/assets/68597202/562b3cd0-c43f-4277-a548-796b2dd754bf)
## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/harshithsaiv/TimeTuner.git
    cd TimeTuner
    ```
    
2. **Set up environment variables**:
    Create a `.env` file in the root directory with your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. **Run the main script**:
    ```bash
    python main.py
    ```

2. **Follow the prompts** to interact with the ChatGPT interface and schedule appointments.

## Configuration

- **Google Drive API**: The script downloads office hours from a Google Drive document named `office_hours`.
- **Office Hours**: Ensure the `office_hours` document in Google Drive contains the office hours in the following format:
    ```
    Mon: 9:00am to 5:00pm
    Tue: 9:00am to 5:00pm
    ...
    ```

## Code Overview

### `chatgpt_interface.py`

- **parse_office_hours(office_hours_str)**: Parses office hours from a multi-line string into a dictionary.
- **is_appointment_valid(day, time_str, office_hours)**: Checks if the proposed appointment time is within office hours.
- **get_response(client, message)**: Gets a response from the GPT-3.5 model.
- **chat_with_chatgpt(office_hours_str)**: Main function to interact with users and schedule appointments.

### `calendar_manager.py`

- **authenticate_google_calendar()**: Authenticates and returns a Google Calendar service object.
- **check_availability(service, day, time_str, office_hours, next_week=False)**: Checks the availability of a time slot.
- **create_event(service, start_time, end_time, summary, description='')**: Creates a calendar event.

### `google_drive_api.py`

- **get_credentials(token_file='token.json', creds_file='credentials.json')**: Retrieves or creates credentials based on token and credentials files.
- **download_office_hours_doc(creds)**: Downloads content of the `office_hours` document as plain text.

### `main.py`

- **main()**: Main function that orchestrates the document download and interaction with ChatGPT.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature-name
    ```
3. **Commit your changes**:
    ```bash
    git commit -m 'Add some feature'
    ```
4. **Push to the branch**:
    ```bash
    git push origin feature-name
    ```
5. **Create a new Pull Request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact Harshith Sai Veeraiah at harshithsaiveeraiah@gmail.com.



