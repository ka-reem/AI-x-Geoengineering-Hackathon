
# Autonomous Climate Intelligence Agent

An AI-powered application that generates comprehensive "Geoengineering Weekly Intelligence Reports" by aggregating and analyzing data from multiple climate-related sources.

## Features

- Automated data collection from NASA satellite observations
- Weekly report generation with structured sections
- Expandable data source integration
- Intelligent analysis and synthesis of climate data

## Project Structure

```
.
├── src/
│   ├── data_sources/      # Data source connectors
│   ├── utils/            # Utility functions
│   └── templates/        # Report templates
├── tests/               # Test files
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd autonomous-climate-intelligence
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_key_here
NASA_API_KEY=your_key_here
```

## Usage

Run the report generator:
```bash
python src/main.py
```

## Report Structure

The generated reports include:
- Header with title and date
- Data source information
- Executive summary
- Key data updates
- New developments & analysis
- Potential action items
- References
- Next update schedule

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
=======
To run deepseek

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python main.py

