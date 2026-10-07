import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd
from flask import Flask, render_template
from sqlalchemy import create_engine
from etl.config import connection_url

app = Flask(__name__)

@app.route("/")
def index():
    engine = create_engine(connection_url())
    df = pd.read_sql("SELECT * FROM Sales", engine)
    return render_template("index.html", columns=df.columns, rows=df.values.tolist(),
                           total=df["total_amount"].sum(), orders=len(df))

if __name__ == "__main__":
    app.run(debug=True)
