# AI Travel Assistant

An intelligent travel assistant that helps users plan their trips, search for flights, and learn from user interactions to improve its responses.

## Features

- Flight information search
- Web search integration
- Chat-based interface
- User feedback collection
- Machine learning capabilities
- Session management
- User preferences storage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-assistant.git
cd travel-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_key
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
travel-assistant/
├── api/
│   ├── flight_search.py
│   └── web_search.py
├── db/
│   ├── models.py
│   └── setup.py
├── llm/
│   ├── model_trainer.py
│   └── setup_llm.py
├── memory/
│   ├── chat_manager.py
│   ├── memory_manager.py
│   └── training_manager.py
├── app.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 