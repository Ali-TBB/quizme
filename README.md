# QuizMe AI

QuizMe AI is an AI-powered application that generates quizzes based on specified topics, difficulty levels, and question types using the Gemini AI API. This project is designed to enhance the learning experience by providing customized quizzes for users.

## Getting Started

To get started with QuizMe AI, follow these steps:

### Setup

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Ali-TBB/QuizMe
   cd QuizMe
   ```

2. **Install Requirements**
Install the necessary Python packages:

   ```bash
    pip install -r requirements.txt
   ```
3.**Set Up the API Key**

Create an account on [Google AI Studio](https://aistudio.google.com) to obtain your API key. After creating your account, get your API key and set it in the `.env` file, which is already included in the project. Open the `.env` file and add your API key:
   ```bash
    API_KEY="your API Key"
   ```
4.**Initialize the Database**

Run the following command to initialize the database:
   ```bash
    python parse.py
   ```

5.**Run the Application**

To start the application, run:
   ```bash
    python main.py
   ```

### Usage

You can run the program either in the console or through a web browser. Follow the prompts in the terminal to choose your preferred mode.

### Features

- Generates quizzes based on specified topics by either uploading a file or simply entering the topic.
- Customizable difficulty levels and question types.
- Allows you to set the number of questions you want to generate.

## Future Improvements

- **User Accounts and Profiles:** Implement user registration and login features to allow users to save their progress and customize their quiz preferences.
  
- **Feedback Mechanism:** Add a feature for users to provide feedback on quizzes to improve the question generation process over time.

- **Analytics Dashboard:** Create an analytics dashboard for users to track their quiz performance, including scores and progress over time.

- **Adaptive Learning:** Develop an adaptive learning algorithm that adjusts the difficulty of quizzes based on user performance.

- **Social Sharing:** Allow users to share their quiz results on social media platforms to encourage engagement and participation.

- **Gamification Elements:** Incorporate gamification elements such as badges, leaderboards, and rewards to enhance user motivation.
