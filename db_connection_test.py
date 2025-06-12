from sqlalchemy import create_engine, text  # Added 'text' import

# # Replace these with your actual MySQL credentials
user = "root"
password = "root"
host = "localhost"
port = "3306"
database = "ipl_historical_data" #ipl_live_data

# SQLAlchemy engine (using pymysql as driver)
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# # Test the connection
# try:
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT VERSION();"))
#         version = result.scalar()
#         print(f"✅ Connected successfully. MySQL version: {version}")
# except Exception as e:
#     print(f"❌ Connection failed: {e}")






from sqlalchemy import inspect

inspector = inspect(engine)
print(inspector.get_table_names())
