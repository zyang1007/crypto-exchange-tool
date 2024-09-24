# crypto-exchange-tool

# Planed Structure:
```
src/
│
├── strategies/            # Strategy implementations
│   ├── __init__.py        # Make it a package
│   ├── grid.py
│   └── other_strategy.py   
│
├── config/                # Configuration files
│   ├── config.json
│   └── test_config        # Consider renaming to something like `config_test.json`
│
├── exchange/              # Separate directory for exchange interactions
│   └── __init__.py        
│   └── ccxt_exchange.py    # Renamed for clarity
│
├── utils/                 
│   ├── __init__.py        
│   ├── logger.py
│   ├── launcher.py  
│   └── edge_cases_handler.py      
│
├── routes/                # Separate directory for Flask routes
│   ├── __init__.py        
│   ├── main_routes.py     # General routes
│   └── config_routes.py   # Routes related to configurations
│
├── forms/                 # Forms for handling user inputs
│   ├── __init__.py        
│   └── user_forms.py      # Rename to be more descriptive
│
├── templates/             # HTML templates
│   ├── index.html
│   ├── data.html
│   └── set_config.html
│
└── app.py                 # Main entry point for the application
```
