import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import sqlite3
import os
import datetime
from typing import Optional

app = FastAPI(title="VENµS Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# נתיב בסיס הנתונים (מקומי לבדיקות - נעדכן ביום חמישי)
DB_PATH = r"C:\Users\nitsa\Desktop\venus_project\venus_archive.sqlite"

def create_stac_item(row):
    date_str = f"{row['Year']}-{row['Month']}-{row['Day']} {row['Hour']}"
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    file_path = f"V:/PRODUCTS/{row['Site']}/{row['Year']}/{row['Filename (DBL or HDR)']}.DBL"

    return {
        "id": row['Filename (DBL or HDR)'],
        "properties": {
            "datetime": dt.isoformat(),
            "cloud_cover": row['Cloud percentage'],
            "mission": row['Mission phase'],
            "level": row['Level'],
            "site": row['Site']
        },
        "assets": {
            "data": {"href": file_path}
        }
    }

@app.get("/get_sites")
def get_sites(mission: Optional[str] = None):
    """שליפת אריחים לפי משימה - עבור ה-Dropdown הדינמי"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if mission:
        query = "SELECT DISTINCT Site FROM venus_archive WHERE [Mission phase] = ? ORDER BY Site"
        cursor.execute(query, (mission,))
    else:
        query = "SELECT DISTINCT Site FROM venus_archive ORDER BY Site"
        cursor.execute(query)
    sites = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"sites": sites}

@app.get("/search")
async def search(mission: str = None, level: str = None, site: str = None, 
                 start_date: str = None, end_date: str = None, max_cloud: float = 100.0):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = "SELECT * FROM venus_archive WHERE [Cloud percentage] <= ?"
    params = [max_cloud]
    
    if mission: query += " AND [Mission phase] = ?"; params.append(mission)
    if level: query += " AND Level = ?"; params.append(level)
    if site: query += " AND Site = ?"; params.append(site)
    if start_date: query += " AND printf('%04d-%02d-%02d', Year, Month, Day) >= ?"; params.append(start_date)
    if end_date: query += " AND printf('%04d-%02d-%02d', Year, Month, Day) <= ?"; params.append(end_date)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return {"results": [create_stac_item(row) for row in rows]}

@app.get("/download")
async def download(file_path: str):
    if not os.path.exists(file_path):
        return {"error": "File not found. Check VPN and Drive V connection."}
    return FileResponse(path=file_path, filename=os.path.basename(file_path))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)