# Price Tracker

Price Tracker is a Python application designed to help users monitor the prices of products online and receive notifications when the prices drop below a specified threshold.

## Features

- **Web Scraping**: Utilizes web scraping techniques with the BeautifulSoup library to extract product prices from online stores.
- **Email Notifications**: Sends email notifications to users when product prices drop below their specified thresholds.
- **User Authentication**: Implements a secure user authentication system to ensure only authorized users can access the application.
- **Persistent Storage**: Stores user login credentials and product URLs with their corresponding affordable prices in CSV files for persistence across sessions.
- **Automated Price Checks**: Utilizes the Schedule library to schedule automated price checks at regular intervals and notify users of price drops.

## Installation

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/yourusername/price-tracker.git
    ```

2. Install the required Python libraries:

    ```
    pip install -r requirements.txt
    ```

3. Update the `config.json` file with your email credentials and SMTP server details.

## Usage

1. Run the `main.py` file to start the Price Tracker application:

    ```
    python main.py
    ```

2. Choose the desired option:
    - Login as Admin: Access administrative functionalities to manage product URLs and affordable prices.
    - Login as User: Access user functionalities to view product price alerts and update preferences.

3. Follow the prompts to add product URLs and specify affordable prices, or log in to receive price drop notifications.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
